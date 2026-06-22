#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
set_goal.py — 一条命令把"用户的目标"原子地写进 _system/goals.json[大类] 并重生成所有页面。

为什么要它：拆成"手写 goals.json 的 JSON → 跑 build_graph → 跑 plan_path"这三步，
AI 经常只做一半（最常见：goal 根本没落盘 → 目标规划页灰显/空状态）。本脚本把这三步
焊成一步，schema 由脚本保证写对，写完立刻重生成路线图+图谱，目标规划页当场点亮并显示真实目标。

最小用法（够修两个 bug：点亮 + 显示真实目标）：
    python set_goal.py --vault "知识库路径" --cat "开源项目运营" --goal "3个月内让 gewu-skill 拿到第一批 star 和真实使用者"

带联网拆好的要求 / 候选目标 / 领域档位（推荐，目标页才有料）：
    python set_goal.py --vault V --cat C --goal "..." --goal-category 求职 \
        --requirements-file reqs.json --suggested-file sg.json \
        --domain-type 工具操作型 --practice-note "光懂不够，得真去发帖/建 demo" --summary "..."

其它：
    --status 进行中|已完成   （默认 进行中；已完成请走页面按钮，别在这里写）
    --sample                 （标"示例"角标）
    --no-regen               （只写 goals.json，不重生成页面）
    --requirements-json '...'  / --suggested-json '...'  （直接传 JSON 字符串，替代 --*-file）

requirements 每项形状：{"name":"要求条目","kind":"知识型|实践型","via":["覆盖它的概念名",...],"have":true|false}
（知识型才接 via；实践型 via 留空、归"实践清单"。脚本会容错补齐缺字段。）
"""
import os, sys, json, argparse, datetime, subprocess


def _load_json_arg(inline, path, label):
    """--*-json 字符串 优先，其次 --*-file 路径；都没有则 None。"""
    if inline:
        try:
            return json.loads(inline)
        except Exception as e:
            sys.exit('[set_goal] --%s-json 不是合法 JSON：%s' % (label, e))
    if path:
        if not os.path.isfile(path):
            sys.exit('[set_goal] 找不到 --%s-file：%s' % (label, path))
        try:
            return json.load(open(path, encoding='utf-8'))
        except Exception as e:
            sys.exit('[set_goal] --%s-file 解析失败：%s' % (label, e))
    return None


def _norm_requirements(reqs):
    """容错归一化：保证每项有 name/kind/via/have，字段名写对，知识型才留 via。"""
    out = []
    if not isinstance(reqs, list):
        return out
    for r in reqs:
        if isinstance(r, str):
            r = {'name': r}
        if not isinstance(r, dict):
            continue
        name = r.get('name') or r.get('req') or r.get('title') or ''
        if not str(name).strip():
            continue
        kind = r.get('kind') or '知识型'
        kind = '实践型' if kind in ('实践型', 'practice') else '知识型'
        via = r.get('via') or r.get('refs') or []
        if isinstance(via, str):
            via = [via]
        via = [str(v).strip() for v in via if str(v).strip()]
        if kind == '实践型':
            via = []  # 实践型不接概念，进"实践清单"
        have = r.get('have')
        if have is None:
            have = r.get('status') in (True, '✓', 'ok')
        out.append({'name': str(name).strip(), 'kind': kind, 'via': via, 'have': bool(have)})
    return out


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument('--vault', required=True, help='知识库根目录')
    ap.add_argument('--cat', required=True, help='大类名（goals.json 的键，须与领域分类一致）')
    ap.add_argument('--goal', help='一句话目标（写它=点亮目标规划页并显示标题；标记完成除外必填）')
    ap.add_argument('--goal-category', default=None, help='目标分类：应试/求职/分享/知识变现/自主学习/无目标 等')
    ap.add_argument('--domain-type', default=None,
                    help='领域档位：纯概念|理论+实践|强实践|记忆型应试|创意开放型|工具操作型')
    ap.add_argument('--practice-note', default=None, help='一句边界声明（目标页置顶横幅）')
    ap.add_argument('--summary', default=None, help='目标现状/差距小结')
    ap.add_argument('--status', default='进行中', choices=['进行中', '已完成'])
    ap.add_argument('--sample', action='store_true', help='标"示例"角标')
    ap.add_argument('--requirements-file', default=None)
    ap.add_argument('--requirements-json', default=None)
    ap.add_argument('--suggested-file', default=None)
    ap.add_argument('--suggested-json', default=None)
    ap.add_argument('--sources-file', default=None)
    ap.add_argument('--sources-json', default=None)
    ap.add_argument('--no-regen', action='store_true', help='只写 goals.json，不重生成页面')
    args = ap.parse_args()

    vault = args.vault
    if not os.path.isdir(vault):
        sys.exit('[set_goal] vault 不存在：%s' % vault)
    if args.status != '已完成' and not (args.goal and args.goal.strip()):
        sys.exit('[set_goal] 必须给 --goal（除非 --status 已完成）。没有 goal，目标规划页无法点亮/显示。')

    sysdir = os.path.join(vault, '_system')
    os.makedirs(sysdir, exist_ok=True)
    gp = os.path.join(sysdir, 'goals.json')
    goals = {}
    if os.path.isfile(gp):
        try:
            goals = json.load(open(gp, encoding='utf-8'))
        except Exception:
            goals = {}
    if not isinstance(goals, dict):
        goals = {}

    entry = dict(goals.get(args.cat) or {})  # 保留旧字段，增量覆盖
    if args.goal and args.goal.strip():
        entry['goal'] = args.goal.strip()
    entry['status'] = args.status
    entry['updated'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    if args.goal_category is not None:
        entry['goal_category'] = args.goal_category
    if args.domain_type is not None:
        entry['domain_type'] = args.domain_type
    if args.practice_note is not None:
        entry['practice_note'] = args.practice_note
    if args.summary is not None:
        entry['summary'] = args.summary
    entry['sample'] = bool(args.sample) if args.sample else entry.get('sample', False)

    reqs = _load_json_arg(args.requirements_json, args.requirements_file, 'requirements')
    if reqs is not None:
        entry['requirements'] = _norm_requirements(reqs)
    entry.setdefault('requirements', [])

    sg = _load_json_arg(args.suggested_json, args.suggested_file, 'suggested')
    if sg is not None:
        if isinstance(sg, str):
            sg = [sg]
        entry['suggested_goals'] = [str(s).strip() for s in sg if str(s).strip()]

    src = _load_json_arg(args.sources_json, args.sources_file, 'sources')
    if src is not None:
        entry['sources'] = src

    goals[args.cat] = entry
    with open(gp, 'w', encoding='utf-8') as f:
        json.dump(goals, f, ensure_ascii=False, indent=2)

    kn = sum(1 for r in entry['requirements'] if r['kind'] == '知识型')
    pr = sum(1 for r in entry['requirements'] if r['kind'] == '实践型')
    print('[set_goal] 已写 goals.json[%s]：goal=「%s」 状态=%s 要求=%d(知识%d/实践%d) 候选目标=%d'
          % (args.cat, entry.get('goal', ''), entry['status'],
             len(entry['requirements']), kn, pr, len(entry.get('suggested_goals', []))))
    print('[set_goal] → 目标规划页将点亮并显示该目标（解锁条件已满足：goal 非空）。')

    if args.no_regen:
        print('[set_goal] --no-regen：跳过重生成。记得手动跑 build_graph.py + plan_path.py。')
        return

    py = sys.executable or 'python3'
    for script in ('build_graph.py', 'plan_path.py'):
        sp = os.path.join(here, script)
        print('[set_goal] 重生成 → %s' % script)
        r = subprocess.run([py, sp, '--vault', vault], capture_output=True, text=True)
        if r.stdout:
            print('   ' + r.stdout.strip().replace('\n', '\n   '))
        if r.returncode != 0:
            print('   [警告] %s 退出码 %d' % (script, r.returncode))
            if r.stderr:
                print('   ' + r.stderr.strip().replace('\n', '\n   '))
    print('[set_goal] 完成。打开「🎯 目标规划」即可看到目标。')


if __name__ == '__main__':
    main()
