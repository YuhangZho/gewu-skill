#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
plan_path.py — 为每个大类生成「知识站」单页 <大类>/<大类>-路线图.html：
  · 顶栏固定 + 左侧目录固定 + 内容区内切换（单页，不跳独立页）
  · 起始视图=学习路线图（依赖分层/当前位置/下一步Top3/扩展）
  · 点击已学透概念 → 同页切换到该概念文档（md 总结 + _viz 动效 + 右侧"本文导读"锚点）
  · 全局统一主题，默认浅色
全量路线数据写入 _system/roadmap_data.json。
"""
import os, sys, re, json, html as H, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_graph import collect, global_vault_path

def desc_of(note):
    for line in note['body'].split('\n'):
        s = line.strip()
        if s.startswith('>'):
            return s.lstrip('> ').strip()
    return ''

def plan_category(items, goal=None, all_notes=None):
    index = {t.lower(): t for t in items}
    for t, n in items.items():
        for a in n['aliases']:
            index[a.lower()] = t
    # 跨大类前置：用全库索引解析"不在本类"的前置（修跨学科 gap：如生信的概念依赖编程大类的 Python基础）
    gidx = {}
    if all_notes:
        for gt, gn in all_notes.items():
            gidx[gt.lower()] = gt
            for a in (gn.get('aliases') or []):
                gidx[a.lower()] = gt
    def xprereq_info(n):
        out = []
        for r in (n.get('prereqs') or []):
            key = str(r).strip().lower()
            if key in index:
                continue  # 同类前置，走常规逻辑
            gt = gidx.get(key)
            if gt and all_notes and all_notes[gt]['category'] != n['category']:
                gn = all_notes[gt]
                out.append({'title': gt, 'category': gn['category'], 'status': gn['status']})
        return out
    def resolve(names):
        out = set()
        for r in names:
            tt = index.get(str(r).strip().lower())
            if tt and tt in items:
                out.add(tt)
        return out
    def imp(t):
        b = items[t]['importance']
        if goal and goal in (items[t].get('goal_tags') or []):
            b += 2
        return b
    prereqs = {t: resolve(n['prereqs']) for t, n in items.items()}
    neighbors = {t: (resolve(n['prereqs']) | resolve(n['links'])) for t, n in items.items()}
    xpre = {t: xprereq_info(n) for t, n in items.items()}
    def cross_ok(t):
        return all(x['status'] == '已学透' for x in xpre[t])
    stage = {}
    def depth(t, guard):
        if t in stage: return stage[t]
        if t in guard: return 0
        ps = prereqs[t]
        d = 0 if not ps else 1 + max((depth(p, guard | {t}) for p in ps), default=0)
        stage[t] = d; return d
    for t in items: depth(t, set())
    placed, placedset = [], set()
    while len(placed) < len(items):
        avail = [t for t in items if t not in placedset and prereqs[t] <= placedset]
        if not avail:
            avail = [t for t in items if t not in placedset]
        def score(t):
            rel = len(neighbors[t] & placedset)
            return (-imp(t), -rel, stage[t], t)
        avail.sort(key=score)
        nxt = avail[0]; placed.append(nxt); placedset.add(nxt)
    learned = {t for t in items if items[t]['status'] == '已学透'}
    # 浅学=已轻学，作侧节点；不抢占“当前/下一站”，保增量稳定（加零散浅学点不打乱规划路径）
    SKIP_NEXT = ('已学透', '浅学')
    planned = [t for t in placed if items[t]['status'] not in SKIP_NEXT]
    current = planned[0] if planned else next((t for t in placed if items[t]['status'] != '已学透'), None)
    base = set(learned) | ({current} if current else set())
    cand = [t for t in placed if items[t]['status'] not in SKIP_NEXT and t != current]
    if not cand:  # 已无待学 → 回退：让浅学点可作“深化”推荐
        cand = [t for t in placed if items[t]['status'] != '已学透' and t != current]
    def nscore(t):
        rel = len(neighbors[t] & base)
        return (-(rel * 2 + imp(t)), placed.index(t))
    # outer fringe 闸门（KST）：优先推荐前置全部已学透的概念；ready 非空时只从中选
    ready_cand = [t for t in cand if prereqs[t] <= learned and cross_ok(t)]
    pool = ready_cand if ready_cand else cand
    next3 = sorted(pool, key=nscore)[:3]
    order = []
    for t in placed:
        n = items[t]
        order.append({'title': t, 'status': n['status'], 'stage': stage[t],
                      'importance': imp(t), 'base_importance': n['importance'],
                      'prereqs': sorted(prereqs[t]), 'desc': desc_of(n),
                      'xprereqs': [x for x in xpre[t] if x['status'] != '已学透'],
                      'groups': n.get('groups', []), 'related': sorted(neighbors[t])})
    return {'order': order, 'current': current, 'next3': next3,
            'learned': len(learned), 'total': len(items),
            'max_stage': max(stage.values()) if stage else 0}

# ---------- Markdown -> HTML（带 ## / ### 锚点 + 目录） ----------
_IMG  = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
_LINK = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')   # 同时支持 http(s) 与相对路径（如 _viz/X.html）
_BARE = re.compile(r'&lt;(https?://[^&]+)&gt;')
_BOLD = re.compile(r'\*\*([^*]+)\*\*')
_CODE = re.compile(r'`([^`]+)`')
_WIKI = re.compile(r'\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]')

def _href(u):
    return u.strip().replace(' ', '%20')   # 路径里的空格转义，保证相对链接可点

def _inline(s, linkset):
    s = H.escape(s)
    def wl(m):
        nm = m.group(1).strip()
        if nm in linkset:
            return '<a class="xref" data-go="%s">%s</a>' % (H.escape(nm), H.escape(nm))
        return H.escape(nm)
    s = _WIKI.sub(wl, s)
    s = _IMG.sub(lambda m: '<img src="%s" alt="%s" style="max-width:100%%;border-radius:10px">' % (_href(m.group(2)), m.group(1)), s)
    s = _LINK.sub(lambda m: '<a href="%s" target="_blank" rel="noopener">%s</a>' % (_href(m.group(2)), m.group(1)), s)
    s = _BARE.sub(r'<a href="\1" target="_blank" rel="noopener">\1</a>', s)
    s = _BOLD.sub(r'<strong>\1</strong>', s)
    s = _CODE.sub(r'<code>\1</code>', s)
    return s

def _nested_list(items):
    """items: [(缩进空格数, 已转义内联HTML)] → 嵌套 <ul> 树（脑图/大纲效果）。"""
    html, stack = [], []
    for indent, txt in items:
        while stack and indent < stack[-1]:
            html.append('</li></ul>'); stack.pop()
        if not stack or indent > stack[-1]:
            html.append('<ul>'); stack.append(indent); html.append('<li>' + txt)
        else:
            html.append('</li><li>' + txt)
    while stack:
        html.append('</li></ul>'); stack.pop()
    return ''.join(html)

def md_render(body, linkset, viz_block=''):
    # 去掉首个 # 标题（与 dochead 重复）
    lines = body.split('\n')
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and re.match(r'^#\s+', lines[0].strip()):
        lines = lines[1:]
    out, toc, i, n, para, hid, fold, vizdone = [], [], 0, len(lines), [], [0], [0], [False]
    def flush():
        if para:
            out.append('<p>' + '<br>'.join(_inline(x, linkset) for x in para) + '</p>'); para.clear()
    while i < n:
        st = lines[i].strip()
        if not st:
            flush(); i += 1; continue
        # 折叠块：<details> / <summary> 透传（不转义），并记录折叠深度
        if st.startswith('<details'):
            flush(); out.append('<details class="lp-fold">'); fold[0] += 1; i += 1; continue
        if st == '</details>':
            flush(); out.append('</details>'); fold[0] = max(0, fold[0] - 1); i += 1; continue
        ms = re.match(r'^<summary>(.*)</summary>\s*$', st)
        if ms:
            flush(); out.append('<summary>' + _inline(ms.group(1), linkset) + '</summary>'); i += 1; continue
        if re.match(r'^-{3,}$', st):
            flush(); out.append('<hr>'); i += 1; continue
        m = re.match(r'^(#{1,6})\s+(.*)$', st)
        if m:
            flush(); lv = len(m.group(1)); txt = m.group(2)
            if lv in (2, 3):
                hid[0] += 1; sid = 'sec-%d' % hid[0]
                out.append('<h%d id="%s">%s</h%d>' % (lv, sid, _inline(txt, linkset), lv))
                if not fold[0]:  # 折叠区内的标题不进"本文导读"
                    toc.append({'lvl': lv, 'text': re.sub(r'<[^>]+>', '', _inline(txt, linkset)), 'id': sid})
                # 把动态画面 iframe 放到「动态画面」标题下，而不是落到全文末尾
                if viz_block and not vizdone[0] and ('动态画面' in txt or 'Dynamic View' in txt):
                    out.append(viz_block); vizdone[0] = True
            else:
                out.append('<h%d>%s</h%d>' % (lv, _inline(txt, linkset), lv))
            i += 1; continue
        if st.startswith('>'):
            flush(); buf = []
            while i < n and lines[i].strip().startswith('>'):
                buf.append(re.sub(r'^\s*>\s?', '', lines[i])); i += 1
            out.append('<blockquote>' + '<br>'.join(_inline(x, linkset) for x in buf) + '</blockquote>'); continue
        if re.match(r'^[-*]\s+', st):
            flush(); items = []
            while i < n and re.match(r'^\s*[-*]\s+', lines[i]):
                raw = lines[i]; indent = len(raw) - len(raw.lstrip(' '))
                txt = re.sub(r'^\s*[-*]\s+', '', raw)
                items.append((indent, _inline(txt, linkset))); i += 1
            out.append(_nested_list(items)); continue
        if re.match(r'^\d+\.\s+', st):
            flush(); buf = []
            while i < n and re.match(r'^\s*\d+\.\s+', lines[i]):
                buf.append(re.sub(r'^\s*\d+\.\s+', '', lines[i])); i += 1
            out.append('<ol>' + ''.join('<li>%s</li>' % _inline(x, linkset) for x in buf) + '</ol>'); continue
        para.append(st); i += 1
    flush()
    if viz_block and not vizdone[0]:  # 笔记没有「动态画面」标题时兜底追加
        out.append(viz_block)
    return '\n'.join(out), toc

def stars(k):
    k = max(0, min(5, int(k or 0)))
    return '★' * k + '<span class="se">' + '★' * (5 - k) + '</span>'

def build_docs(cat, items, plan, vault):
    learned = [o for o in plan['order'] if items[o['title']]['status'] == '已学透']
    linkset = set(o['title'] for o in learned)
    cdir = os.path.join(vault, cat)
    docs = {}
    for o in learned:
        t = o['title']; note = items[t]
        viz = note.get('viz', '')
        viz_block = ''
        if viz:
            rel = os.path.relpath(os.path.join(vault, viz), cdir).replace('\\', '/')
            href = rel.replace(' ', '%20')
            viz_block = ('<div class="vizwrap"><div class="vizbar"><span>动态画面</span>'
                         '<a href="%s" target="_blank" rel="noopener">新标签打开 ↗</a></div>'
                         '<iframe class="vizframe" data-src="%s" loading="lazy"></iframe></div>') % (href, href)
        body_html, toc = md_render(note['body'], linkset, viz_block)
        doc = ('<div class="dochead"><h1>%s <span class="stars">%s</span></h1>'
               '<span class="badge ok">✓ 已学透</span></div><div class="md">%s</div>'
               % (H.escape(t), stars(o['importance']), body_html))
        toc_html = '<div class="tochd">本文导读</div>' + (''.join(
            '<a class="tl lv%d" data-id="%s">%s</a>' % (x['lvl'], x['id'], x['text']) for x in toc)
            or '<div class="tnote">（无小节）</div>')
        docs[t] = {'doc': doc, 'toc': toc_html}
    return docs

def _load_config(vault):
    """读取 知识库/_system/config.json（用户自定义开关 + 参数）；缺省返回空。"""
    p = os.path.join(vault, '_system', 'config.json')
    if os.path.isfile(p):
        try:
            return json.load(open(p, encoding='utf-8'))
        except Exception:
            return {}
    return {}

def _apply_config(html, cfg):
    """enabled=true 时，按 config 覆盖知识站默认主题与强调色；否则原样返回。"""
    if not cfg or not cfg.get('enabled'):
        return html
    th = cfg.get('theme_default')
    if th in ('light', 'dark', 'ink', 'inkdark'):
        html = html.replace('<html lang="zh" data-theme="light">',
                            '<html lang="zh" data-theme="%s">' % th, 1)
    ac = cfg.get('accent') or {}
    if ac.get('light'):
        html = html.replace('--accent:#007aff', '--accent:' + str(ac['light']))
    if ac.get('dark'):
        html = html.replace('--accent:#0a84ff', '--accent:' + str(ac['dark']))
    return html


def _read_profile(here, mid):
    """读 mentors/<id>/profile.md 的 frontmatter（name_en/color/voice_mode 等）。"""
    p = os.path.join(here, '..', 'mentors', mid, 'profile.md')
    if not os.path.isfile(p):
        return None
    m = re.match(r'^---\s*\n(.*?)\n---', open(p, encoding='utf-8').read(), re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            mm = re.match(r'^(\w+):\s*(.*)$', line)
            if mm:
                v = mm.group(2).strip()
                if v[:1] in ('"', "'"):
                    q = v[0]; e = v.find(q, 1)
                    v = v[1:e] if e > 0 else v[1:]
                else:
                    h = v.find(' #')
                    if h >= 0:
                        v = v[:h]
                    v = v.strip()
                fm[mm.group(1)] = v
    return fm

def _mentor_tags(vault, here):
    """返回 {大类: 标签HTML}。_system/mentors.json enabled=false 或无绑定 → 空 dict。"""
    p = os.path.join(vault, '_system', 'mentors.json')
    if not os.path.isfile(p):
        return {}
    try:
        m = json.load(open(p, encoding='utf-8'))
    except Exception:
        return {}
    if not m.get('enabled'):
        return {}
    out = {}
    for cat, b in (m.get('bindings') or {}).items():
        if not b or not b.get('mentor'):
            continue
        prof = _read_profile(here, b['mentor'])
        if not prof:
            continue
        name = prof.get('name_en') or prof.get('name') or b['mentor']
        color = prof.get('color') or 'var(--accent)'
        traits = [t for t in (b.get('traits') or []) if t]
        if prof.get('voice_mode') == 'style_reference':
            disc = '导师风格 · 风格参照（非第一人称扮演）· 基于公开信息演绎'
        else:
            disc = '导师风格 · 基于公开信息的教学风格演绎，非本人'
        nameseg = '<span class="mt-name">%s</span>' % H.escape(name)
        if traits:
            tag = ('<span class="mentortag" title="%s"><span class="mt-trait" style="background:%s">%s</span>%s</span>'
                   % (H.escape(disc), color, H.escape('·'.join(traits)), nameseg))
        else:
            tag = '<span class="mentortag" title="%s">%s</span>' % (H.escape(disc), nameseg)
        out[cat] = tag
    return out


def _mech_cards(items):
    """从已学透笔记结构【零 token】派生兜底自测题（定位/边界/双链），
    供前期概念少、AI 卡池小时补足，避免抽卡 3 张就见底。质量不如 AI 整合题，故标 kind=自测。"""
    out = []
    for t, n in items.items():
        if n.get('status') != '已学透':
            continue
        body = n.get('body', '') or ''
        m = re.search(r'#+\s*一句话定位\s*\n+>?\s*(.+)', body)
        if m:
            a = m.group(1).strip().lstrip('>').strip()
            if a:
                out.append({"q": "用一句话说清「%s」是什么、解决什么问题？" % t, "kind": "自测", "answer": a[:240]})
        m2 = re.search(r'#+\s*[^\n]*(?:失效边界|边界)[^\n]*\n+(.+?)(?:\n#+\s|\Z)', body, re.S)
        if m2:
            a = m2.group(1).strip()
            if a:
                out.append({"q": "说出「%s」的失效边界——它什么时候不适用 / 会踩什么坑？" % t, "kind": "自测", "answer": a[:300]})
        rels = [x for x in (n.get('links') or []) if x and x != t]
        if rels:
            out.append({"q": "「%s」和「%s」是什么关系？先自己说，再翻两篇笔记对照。" % (t, rels[0]),
                        "kind": "自测", "answer": "（开放·对照两篇笔记的双链/前置关系自检，无标准答案）"})
    return out


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    # 知识库根目录 = 主题名文件夹本身（不再套一层「知识库/」）
    default_vault = os.environ.get('GEWU_VAULT') or global_vault_path() or os.getcwd()
    ap = argparse.ArgumentParser()
    ap.add_argument('--vault', default=default_vault)
    ap.add_argument('--goal', default=None)
    args = ap.parse_args()
    vault = args.vault
    notes = collect(vault)
    cfg = _load_config(vault)
    mtags = _mentor_tags(vault, here)
    sysdir = os.path.join(vault, '_system'); os.makedirs(sysdir, exist_ok=True)
    cats = {}
    for t, n in notes.items():
        cats.setdefault(n['category'], {})[t] = n
    expansions = {}
    dom = os.path.join(sysdir, 'domains.json')
    if os.path.isfile(dom):
        try: expansions = json.load(open(dom, encoding='utf-8')).get('domains', {})
        except Exception: expansions = {}
    goals_all = {}
    _gp = os.path.join(sysdir, 'goals.json')
    if os.path.isfile(_gp):
        try: goals_all = json.load(open(_gp, encoding='utf-8'))
        except Exception: goals_all = {}
    flash_all = {}
    _fp = os.path.join(sysdir, 'flashcards.json')
    if os.path.isfile(_fp):
        try: flash_all = json.load(open(_fp, encoding='utf-8'))
        except Exception: flash_all = {}
    flash_on = bool(cfg.get('flashcard_review')) if cfg else False
    # 抽卡卡背：按主题不撞色匹配（浅→obsidian / 深→cinnabar / 宣纸→pine / 夜墨→indigo），内联为 data-URI 保证离线自包含
    import base64 as _b64
    _card_map = {'light': 'card-back-obsidian.svg', 'dark': 'card-back-cinnabar.svg',
                 'ink': 'card-back-pine.svg', 'inkdark': 'card-back-indigo.svg'}
    _assets = os.path.join(here, '..', 'assets')
    _card_rules = []
    for _th, _fn in _card_map.items():
        _fp2 = os.path.join(_assets, _fn)
        if os.path.isfile(_fp2):
            try:
                _b = _b64.b64encode(open(_fp2, 'rb').read()).decode('ascii')
                _card_rules.append(':root[data-theme="%s"] .fcard.back{background-image:url("data:image/svg+xml;base64,%s")}' % (_th, _b))
            except Exception: pass
    card_css = '\n'.join(_card_rules)
    gen = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    full = {'generated': gen, 'goal': args.goal or '', 'categories': {}, 'expansions': expansions}
    for c in sorted(cats.keys()):
        full['categories'][c] = plan_category(cats[c], args.goal, notes)
    with open(os.path.join(sysdir, 'roadmap_data.json'), 'w', encoding='utf-8') as f:
        json.dump(full, f, ensure_ascii=False, indent=2)
    for c, items in sorted(cats.items()):
        cdir = os.path.join(vault, c)
        if not os.path.isdir(cdir): continue
        r = full['categories'][c]
        docs = build_docs(c, items, r, vault)
        data = {'generated': gen, 'goal': args.goal or '',
                'categories': {c: r}, 'expansions': {c: expansions.get(c, [])}}
        # 卡池 = AI 卡 + 机械兜底卡（零 token，从已学透笔记派生；去重、上限 12）
        _flash_obj = dict(flash_all.get(c) or {})
        _ai_cards = list(_flash_obj.get('cards') or [])
        if flash_on:
            _seen_q = {x.get('q') for x in _ai_cards}
            _mech = [m for m in _mech_cards(items) if m['q'] not in _seen_q]
            _flash_obj['cards'] = (_ai_cards + _mech)[:12]
        html = (HTML.replace('__CAT__', H.escape(c))
                    .replace('__DATA__', json.dumps(data, ensure_ascii=False))
                    .replace('__DOCS__', json.dumps(docs, ensure_ascii=False))
                    .replace('__GOAL__', json.dumps(goals_all.get(c, {}), ensure_ascii=False))
                    .replace('__FLASH__', json.dumps(_flash_obj, ensure_ascii=False))
                    .replace('__FLASH_ON__', 'true' if flash_on else 'false')
                    .replace('__CARDCSS__', card_css)
                    .replace('__MENTORTAG__', mtags.get(c, '')))
        html = _apply_config(html, cfg)
        # 边触发门：该类存在概念间边(prereq/双链)才出路线图；否则只留 .md，清理旧文件
        _has_edge = any(o.get('prereqs') or o.get('related') for o in r.get('order', []))
        _rp = os.path.join(cdir, c + '-路线图.html')
        if _has_edge:
            open(_rp, 'w', encoding='utf-8').write(html)
        elif os.path.isfile(_rp):
            try: os.remove(_rp)
            except OSError: pass
        # 清理旧的独立子页与连续手册
        for old in [os.path.join(cdir, c + '-学习手册.html')]:
            if os.path.isfile(old):
                try: os.remove(old)
                except OSError: pass
        pdir = os.path.join(cdir, '_pages')
        if os.path.isdir(pdir):
            for fn in os.listdir(pdir):
                try: os.remove(os.path.join(pdir, fn))
                except OSError: pass
            try: os.rmdir(pdir)
            except OSError: pass
        print('【%s】知识站：%d/%d 学透 · 当前 %s → %s-路线图.html'
              % (c, r['learned'], r['total'], r['current'] or '（全部学透）', c))

HTML = r"""<!DOCTYPE html>
<html lang="zh" data-theme="light"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__CAT__ · 知识站</title>
<style>
:root[data-theme="dark"]{color-scheme:dark;--bg:#0d1117;--panel:rgba(22,27,34,.72);--solid:#161b22;--line:rgba(48,54,61,.7);--text:#f0f2f5;--muted:#8b949e;--green:#30d158;--yellow:#ffd60a;--gray:#6e7681;--accent:#0a84ff;--track:rgba(84,84,88,.28);--starempty:#3a4150;--code:rgba(110,118,129,.25);--grad:#30d1c1;--red:#ff6b6b}
:root[data-theme="light"]{color-scheme:light;--bg:#f5f5f7;--panel:rgba(255,255,255,.86);--solid:#ffffff;--line:rgba(0,0,0,.08);--text:#1d1d1f;--muted:#6e6e73;--green:#34c759;--yellow:#ff9f0a;--gray:#aeaeb2;--accent:#007aff;--track:rgba(0,0,0,.06);--starempty:#d1d1d6;--code:rgba(0,0,0,.06);--grad:#30d1c1;--red:#ff3b30}
/* 中国水墨 · 宣纸（浅）*/
:root[data-theme="ink"]{color-scheme:light;--bg:#efe5cf;--panel:rgba(246,240,225,.86);--solid:#f6f0e1;--line:rgba(60,48,20,.14);--text:#2b2620;--muted:#8a7c64;--green:#5a8f6d;--yellow:#c89a3c;--gray:#b1a486;--accent:#9c3b2e;--track:rgba(60,48,20,.10);--starempty:#cdc1a3;--code:rgba(60,48,20,.08);--grad:#5a8f6d;--red:#b83a2e}
/* 中国水墨 · 夜墨（深）*/
:root[data-theme="inkdark"]{color-scheme:dark;--bg:#181813;--panel:rgba(34,34,24,.74);--solid:#222218;--line:rgba(120,110,80,.28);--text:#ece3d0;--muted:#9a9079;--green:#79c79a;--yellow:#d8b15a;--gray:#5a5a4b;--accent:#d6604d;--track:rgba(120,110,80,.20);--starempty:#4a4a3b;--code:rgba(120,110,80,.20);--grad:#79c79a;--red:#d6604d}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);
font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}
.topbar{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:12px;padding:11px 22px;
background:var(--panel);border-bottom:1px solid var(--line);backdrop-filter:blur(18px) saturate(180%)}
.topbar .brand{font-weight:700;font-size:15px;letter-spacing:-.01em}
.topbar .crumb{color:var(--muted);font-size:13px}
.topbar .crumb b{color:var(--text)}
.topbar .crumb .cl{color:var(--accent);cursor:pointer}
.topbar .sp{flex:1}
.mentortag{display:inline-flex;align-items:center;font-size:11px;line-height:1;border-radius:3px;overflow:hidden;margin-left:4px;font-weight:600;vertical-align:middle;box-shadow:0 1px 2px rgba(0,0,0,.14);cursor:default}
.mentortag .mt-trait{padding:4px 7px;color:#fff;white-space:nowrap}
.mentortag .mt-name{padding:4px 7px;background:#e7e7ea;color:#333;white-space:nowrap}
.themebtn{background:var(--solid);color:var(--text);border:1px solid var(--line);border-radius:8px;padding:6px 11px;font-size:13px;cursor:pointer}
.shell{display:grid;grid-template-columns:252px minmax(0,1fr)}
#sidenav{position:sticky;top:49px;align-self:start;height:calc(100vh - 49px);overflow-y:auto;padding:16px 12px;border-right:1px solid var(--line)}
#sidenav .navlink{display:flex;align-items:center;gap:8px;padding:7px 10px;border-radius:8px;color:var(--text);text-decoration:none;font-size:13.5px;cursor:pointer;transition:background .2s,color .2s}
#sidenav .navlink:hover{background:color-mix(in srgb,var(--accent) 12%,transparent)}
#sidenav .navlink.active{background:color-mix(in srgb,var(--accent) 16%,transparent);color:var(--accent);font-weight:600}
#sidenav .navlink.todo{color:var(--muted)}
#sidenav .navlink.home{font-weight:600;margin-bottom:6px}
#sidenav .nd{width:8px;height:8px;border-radius:50%;flex:none}
#sidenav .navgroup{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:12px 8px 4px}
#sidenav .navgrp{margin-bottom:2px}
#sidenav .navhd2{display:flex;align-items:center;gap:7px;padding:8px 8px;font-size:13.5px;font-weight:600;color:var(--text);cursor:pointer;border-radius:8px;user-select:none}
#sidenav .navhd2:hover{background:color-mix(in srgb,var(--accent) 8%,transparent)}
#sidenav .navhd2 .chev{font-size:10px;color:var(--muted);transition:transform .2s;flex:none}
#sidenav .navgrp:not(.collapsed) .navhd2 .chev{transform:rotate(90deg)}
#sidenav .navhd2 .gc{margin-left:auto;font-size:11px;font-weight:500;color:var(--muted);background:color-mix(in srgb,var(--muted) 14%,transparent);border-radius:10px;padding:1px 7px}
#sidenav .navgbody{overflow:hidden;padding-left:6px}
#sidenav .navgrp.collapsed .navgbody{display:none}
main{min-width:0}
#overview{padding:26px 32px 80px;max-width:1060px}
h1.ttl{font-size:26px;font-weight:700;letter-spacing:-.02em;margin:0 0 6px}
.sub{color:var(--muted);font-size:14px;margin-bottom:18px;line-height:1.5}
.bar{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-bottom:18px;padding:14px 18px;background:var(--panel);border:1px solid var(--line);border-radius:14px;backdrop-filter:blur(18px) saturate(180%)}
.goal{font-size:12px;color:var(--accent);border:1px solid var(--accent);border-radius:20px;padding:3px 10px}
.prog{flex:1;min-width:200px;height:10px;background:var(--track);border-radius:6px;overflow:hidden}
.prog>i{display:block;height:100%;background:linear-gradient(90deg,var(--green),var(--grad))}
.progtxt{font-size:13px;color:var(--muted)}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin-bottom:14px}
.legend i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:4px;vertical-align:middle}
.cols{display:grid;grid-template-columns:minmax(0,1fr) 290px;gap:22px}
@media(max-width:1000px){.cols{grid-template-columns:1fr}}
.stage{margin:0 0 6px;font-size:12px;letter-spacing:.08em;color:var(--muted);text-transform:uppercase;padding-top:14px;border-top:1px dashed var(--line)}
.stage:first-child{border-top:none;padding-top:0}
.card{display:flex;gap:12px;align-items:flex-start;background:var(--panel);border:1px solid var(--line);
border-radius:14px;padding:14px 16px;margin:9px 0;position:relative;backdrop-filter:blur(18px) saturate(180%);
transition:transform .3s cubic-bezier(.4,0,.2,1),box-shadow .3s,border-color .3s;animation:fadeInUp .4s ease-out backwards}
.card:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(0,0,0,.10)}
@keyframes fadeInUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.card.cur{border-color:var(--accent);animation:fadeInUp .4s ease-out backwards,breathe 2.6s ease-in-out infinite .4s}
@keyframes breathe{0%,100%{box-shadow:0 0 0 1px var(--accent),0 0 14px color-mix(in srgb,var(--accent) 22%,transparent)}50%{box-shadow:0 0 0 1px var(--accent),0 0 26px color-mix(in srgb,var(--accent) 45%,transparent)}}
.card.done{opacity:.9}.card.linkcard{cursor:pointer}.card.linkcard:hover{opacity:1}
.dot{width:12px;height:12px;border-radius:50%;margin-top:5px;flex:none;box-shadow:0 0 0 5px color-mix(in srgb,var(--muted) 16%,transparent);transition:transform .3s,box-shadow .3s}
.card:hover .dot{transform:scale(1.18);box-shadow:0 0 0 6px color-mix(in srgb,var(--muted) 24%,transparent)}
.t{font-weight:600}.t .stars{color:var(--yellow);font-size:12px;margin-left:6px}
.d{color:var(--muted);font-size:13px;margin-top:3px;line-height:1.5}
.pre{color:var(--muted);font-size:12px;margin-top:5px}.pre b{font-weight:500}
.xpre{color:var(--red)}.xpre b{color:var(--red)}
.tag{position:absolute;top:13px;right:15px;font-size:11px;font-weight:600;color:var(--accent);background:color-mix(in srgb,var(--accent) 12%,transparent);border:1px solid color-mix(in srgb,var(--accent) 34%,var(--line));border-radius:12px;padding:4px 11px}
.tag.ok{color:var(--green);background:color-mix(in srgb,var(--green) 14%,transparent);border-color:color-mix(in srgb,var(--green) 40%,var(--line))}
.side h3{font-size:12px;color:var(--muted);margin:0 0 8px;letter-spacing:.05em;text-transform:uppercase}
.next,.exp{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px;margin-bottom:18px;backdrop-filter:blur(18px) saturate(180%)}
.next .item{padding:8px 0;border-bottom:1px solid var(--line)}.next .item:last-child{border:none}
.next .item b{color:var(--accent);font-size:15px;font-weight:600}.next .why{font-size:12px;color:var(--muted);margin-top:2px}
.exp .e{padding:7px 0;border-bottom:1px solid var(--line)}.exp .e:last-child{border:none}
.exp .e .nm{color:var(--text);font-size:15px;font-weight:600}.exp .e .why{font-size:13px;color:var(--muted);margin-top:3px;line-height:1.5}
.stars .se{color:var(--starempty)}
/* 概念文档视图 */
#docwrap{display:grid;grid-template-columns:minmax(0,1fr) 212px;gap:30px;padding:28px 34px 90px;max-width:1140px}
@media(max-width:920px){#docwrap{grid-template-columns:1fr}#toc{display:none}}
.dochead{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:4px}
.dochead h1{font-size:26px;font-weight:700;letter-spacing:-.02em;margin:0}
.dochead .stars{color:var(--yellow);font-size:15px}
.badge.ok{font-size:12px;font-weight:600;border-radius:12px;padding:3px 10px;color:var(--green);background:color-mix(in srgb,var(--green) 14%,transparent);border:1px solid color-mix(in srgb,var(--green) 40%,var(--line))}
.md{font-size:15px;line-height:1.78;margin-top:14px}
.md h2{font-size:18px;margin:1.5em 0 .4em;scroll-margin-top:64px}.md h3{font-size:15px;margin:1.2em 0 .3em;color:var(--muted);scroll-margin-top:64px}
.md p{margin:.6em 0}.md ul,.md ol{margin:.5em 0;padding-left:1.4em}.md li{margin:.25em 0}
/* 嵌套大纲 = 树状脑图效果 */
.md ul ul{margin:.2em 0;padding-left:1.1em;border-left:1px dashed var(--line)}
.md ul ul li{position:relative}
/* 折叠块：学习过程记录默认收起 */
.md details.lp-fold{margin:16px 0;border:1px solid var(--line);border-radius:12px;background:var(--panel);overflow:hidden}
.md details.lp-fold>summary{cursor:pointer;list-style:none;user-select:none;padding:11px 16px;font-weight:600;font-size:14px;color:var(--text);background:color-mix(in srgb,var(--muted) 8%,transparent)}
.md details.lp-fold>summary::-webkit-details-marker{display:none}
.md details.lp-fold>summary::before{content:"▸ ";color:var(--muted)}
.md details.lp-fold[open]>summary{border-bottom:1px solid var(--line)}
.md details.lp-fold[open]>summary::before{content:"▾ "}
.md details.lp-fold>:not(summary){margin-left:16px;margin-right:16px}
.md details.lp-fold>:first-of-type:not(summary){margin-top:10px}
.md details.lp-fold>:last-child{margin-bottom:12px}
.md blockquote{margin:.7em 0;padding:.5em .9em;border-left:3px solid var(--accent);background:color-mix(in srgb,var(--accent) 8%,transparent);border-radius:0 8px 8px 0}
.md code{background:var(--code);padding:1px 6px;border-radius:5px;font-size:.92em;font-family:ui-monospace,Menlo,Consolas,monospace}
.md a{color:var(--accent);text-decoration:none}.md a:hover{text-decoration:underline}.md a.xref{cursor:pointer}
.md strong{font-weight:600}.md hr{border:none;border-top:1px solid var(--line);margin:1.1em 0}
.vizwrap{margin:20px 0 4px;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:var(--panel)}
.vizbar{display:flex;justify-content:space-between;align-items:center;padding:9px 14px;font-size:13px;color:var(--muted);border-bottom:1px solid var(--line)}
.vizbar a{color:var(--accent);text-decoration:none;font-size:12px}
.vizwrap iframe{width:100%;height:560px;border:0;display:block;background:var(--bg)}
#toc{position:sticky;top:69px;align-self:start;height:fit-content}
#toc .tochd{font-size:12px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}
#toc .tl{display:block;color:var(--muted);text-decoration:none;font-size:13px;padding:5px 0 5px 12px;border-left:2px solid var(--line);cursor:pointer;line-height:1.4}
#toc .tl:hover{color:var(--text)}
#toc .tl.active{color:var(--accent);border-left-color:var(--accent)}
#toc .tl.lv3{padding-left:24px;font-size:12.5px}
#toc .tnote{color:var(--muted);font-size:12px}
@media(max-width:860px){.shell{grid-template-columns:1fr}#sidenav{position:static;height:auto;border-right:none;border-bottom:1px solid var(--line)}}
#graphwrap{height:calc(100vh - 49px)}
.navlink.disabled{opacity:.4;pointer-events:none}
#goalwrap{padding:28px 34px 90px;max-width:880px}
.ghead{display:flex;align-items:center;gap:12px;flex-wrap:wrap}.ghead h1{font-size:25px;font-weight:700;letter-spacing:-.02em;margin:0}
.gtag{font-size:12px;color:var(--accent);border:1px solid var(--accent);border-radius:20px;padding:2px 10px}.gtag.sample{color:var(--muted);border-color:var(--line)}
.gsub{color:var(--muted);font-size:13px;margin:4px 0 16px}
.gmeter{margin:6px 0 14px}.gpct{font-size:34px;font-weight:700;letter-spacing:-.02em}
.gbar{height:10px;background:var(--track);border-radius:6px;overflow:hidden;margin:6px 0 4px}.gbar>i{display:block;height:100%;border-radius:6px;transition:width .6s}
.gtier{font-size:13px;color:var(--muted)}
.gsum{font-size:14.5px;line-height:1.7;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 16px}
.gh3{font-size:13px;letter-spacing:.05em;color:var(--muted);text-transform:uppercase;margin:22px 0 8px}
.greqs{display:flex;flex-direction:column;gap:6px}.greq{display:flex;gap:10px;align-items:flex-start;font-size:14px}.greq em{color:var(--muted);font-style:normal;font-size:12.5px}
.gck{width:20px;height:20px;border-radius:50%;flex:none;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;margin-top:1px}
.gck.ok{color:var(--green);background:color-mix(in srgb,var(--green) 16%,transparent)}.gck.no{color:var(--muted);background:color-mix(in srgb,var(--muted) 14%,transparent)}
.gck.part{color:transparent;box-shadow:0 0 0 1px color-mix(in srgb,var(--muted) 22%,transparent) inset}
.greqn{flex:1;line-height:1.5}
.gcap{font-size:12.5px;color:var(--muted);line-height:1.65;margin:0 0 10px}
.gpractice{background:color-mix(in srgb,var(--accent) 10%,var(--panel));border:1px solid color-mix(in srgb,var(--accent) 30%,var(--line));border-left:3px solid var(--accent);border-radius:10px;padding:11px 14px;margin:6px 0 14px;font-size:13px;line-height:1.6;color:var(--text)}
.gpractice b{color:var(--accent)}
.gvia1,.gviac{color:var(--accent);text-decoration:none;cursor:pointer;font-size:13px}
.gvia1:hover,.gviac:hover{text-decoration:underline}
.gexp{position:relative;display:inline}
.gexpb{color:var(--accent);cursor:pointer;font-size:12.5px;padding:1px 8px;border-radius:8px;white-space:nowrap;background:linear-gradient(90deg,transparent,color-mix(in srgb,var(--accent) 15%,transparent))}
.gexpb:hover{background:linear-gradient(90deg,transparent,color-mix(in srgb,var(--accent) 26%,transparent))}
.gexpbody{display:none;margin-left:7px}
.gexp.open .gexpbody{display:inline}
.gvsep{color:var(--muted);margin:0 6px}
.gpracts{display:flex;flex-direction:column;gap:6px}
.gpract{display:flex;gap:10px;align-items:flex-start;font-size:14px;cursor:default}
.gpck{width:20px;height:20px;flex:none;display:flex;align-items:center;justify-content:center;font-size:15px;color:var(--muted);margin-top:1px;transition:color .15s;cursor:pointer}
.gpck:hover{color:var(--green)}
.gpck.on{color:var(--green)}
.grecs{display:flex;flex-direction:column;gap:8px}.grec{display:flex;gap:12px;align-items:flex-start;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.gp{flex:none;font-size:12px;font-weight:700;color:#fff;background:var(--accent);border-radius:8px;padding:3px 8px}.grn{font-weight:600;font-size:15px}.grw{color:var(--muted);font-size:13px;margin-top:3px;line-height:1.5}
.celebrate{background:color-mix(in srgb,var(--green) 12%,transparent);border:1px solid color-mix(in srgb,var(--green) 40%,var(--line));border-radius:14px;padding:18px;margin-bottom:16px;animation:fadeInUp .5s ease-out}.celebrate .cbig{font-size:22px;font-weight:700;margin-bottom:4px}
.gacts{font-size:14px;line-height:1.8;padding-left:1.2em}
.gsrc{font-size:12px;color:var(--muted);margin-top:14px}.gsrc a{color:var(--accent);text-decoration:none}
.gfb{margin-top:24px;border-top:1px dashed var(--line);padding-top:16px}.gfb textarea{width:100%;min-height:70px;background:var(--panel);border:1px solid var(--line);border-radius:10px;color:var(--text);padding:10px 12px;font:inherit;font-size:14px;resize:vertical}
.gbtn{margin-top:10px;background:var(--green);color:#fff;border:none;border-radius:10px;padding:9px 18px;font-size:14px;font-weight:600;cursor:pointer}.gnote{font-size:12.5px;color:var(--muted);margin-left:10px}
.gempty{color:var(--muted);font-size:15px;line-height:1.8;max-width:620px}.gempty h1{color:var(--text);font-size:22px}.gref{font-size:13px;color:var(--accent);margin-top:10px}
#graphframe{width:100%;height:100%;border:0;display:block;background:var(--bg)}
.themebtn{transition:background .2s,border-color .2s,color .2s}
.themebtn:hover{border-color:var(--accent);color:var(--accent)}
/* —— 水墨主题质感（宣纸纹理 / 楷书标题 / 朱砂落款感）—— */
:root[data-theme="ink"] body,:root[data-theme="inkdark"] body{
background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.045'/%3E%3C/svg%3E");
background-attachment:fixed;background-size:160px 160px}
:root[data-theme="ink"] .topbar .brand,:root[data-theme="inkdark"] .topbar .brand,
:root[data-theme="ink"] h1.ttl,:root[data-theme="inkdark"] h1.ttl,
:root[data-theme="ink"] .dochead h1,:root[data-theme="inkdark"] .dochead h1,
:root[data-theme="ink"] .ghead h1,:root[data-theme="inkdark"] .ghead h1{
font-family:"Kaiti SC","STKaiti","KaiTi","Songti SC","SimSun",serif;letter-spacing:.5px}
:root[data-theme="ink"] .themebtn,:root[data-theme="inkdark"] .themebtn,
:root[data-theme="ink"] .card,:root[data-theme="inkdark"] .card,
:root[data-theme="ink"] .bar,:root[data-theme="inkdark"] .bar{border-radius:6px}
:root[data-theme="ink"] .md blockquote,:root[data-theme="inkdark"] .md blockquote{border-left-width:4px;font-style:italic}
</style></head><body>
<div class="topbar">
  <span class="brand">__CAT__ 学习站</span>__MENTORTAG__
  <span class="crumb" id="crumb"></span>
  <span class="sp"></span>
  <button class="themebtn" id="themebtn">◑ 深</button>
</div>
<div class="shell">
  <nav id="sidenav"><a class="navlink home" id="homelink">📋 学习路线图</a><a class="navlink home" id="graphlink">🕸 知识图谱</a><a class="navlink home" id="goallink">🎯 目标规划</a><a class="navlink home" id="flashlink" style="display:none">🎴 抽卡复习</a><div id="navbody"></div></nav>
  <main>
    <section id="overview">
      <h1 class="ttl">学习路线图 <span style="color:var(--muted);font-weight:400;font-size:15px">Learning Roadmap</span></h1>
      <div class="sub" id="sub"></div>
      <div class="bar">
        <span class="goal" id="goal" style="display:none"></span>
        <div class="prog"><i id="progbar"></i></div>
        <span class="progtxt" id="progtxt"></span>
      </div>
      <div class="legend">
        <span><i style="background:var(--green)"></i>已学透</span>
        <span><i style="background:var(--yellow)"></i>巩固中</span>
        <span><i style="background:var(--grad)"></i>浅学</span>
        <span><i style="background:var(--gray)"></i>待学</span>
        <span>★ = 重要度　|　按依赖顺序自上而下</span>
      </div>
      <div class="cols"><div id="timeline"></div>
        <div class="side"><h3>下一步推荐 · NEXT 3</h3><div class="next" id="next"></div>
          <h3>学完本领域后的扩展方向</h3><div class="exp" id="exp"></div></div></div>
    </section>
    <section id="docwrap" style="display:none"><div id="docview"></div><aside id="toc"></aside></section>
    <section id="graphwrap" style="display:none"><iframe id="graphframe" data-src="__CAT__-知识图谱.html"></iframe></section>
    <section id="goalwrap" style="display:none"><div id="goalbody"></div></section>
    <section id="flashwrap" style="display:none"><div id="flashbody"></div></section>
  </main>
</div>
<style>
#flashwrap{padding:26px 32px 80px;max-width:1060px}
#flashwrap .ttl{font-size:26px;font-weight:700;margin:0 0 16px}
.fbuild{background:var(--panel);border:1px dashed var(--line);border-radius:12px;padding:14px 16px;color:var(--muted);margin-bottom:16px}
.fdeck{display:flex;gap:16px;margin:8px 0 18px;flex-wrap:wrap}
.fcard{flex:0 1 190px;max-width:200px;aspect-ratio:360/504;border-radius:16px;border:1px solid var(--line);background:var(--panel);backdrop-filter:blur(18px) saturate(180%);display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;transition:transform .18s,box-shadow .18s;font-size:12px;color:var(--muted);overflow:hidden}
.fcard.back:hover{transform:translateY(-4px);box-shadow:0 10px 26px rgba(0,0,0,.18);border-color:var(--accent)}
.fcard.back{background-size:contain;background-position:center;background-repeat:no-repeat}
.fcard.flip{cursor:default;flex:1 1 100%;max-width:none;aspect-ratio:auto;align-items:flex-start;justify-content:flex-start;padding:16px;color:var(--text);background:color-mix(in srgb,var(--accent) 8%,var(--panel))}
.fqonly{font-size:15px;font-weight:600;line-height:1.5}
.fkind{display:inline-block;font-size:11px;font-weight:600;padding:1px 8px;border-radius:10px;background:color-mix(in srgb,var(--accent) 18%,transparent);color:var(--accent);margin-left:6px}
.fqbox,.fabox{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px;color:var(--muted);margin:10px 0;line-height:1.65}
.fqbox.show,.fabox.show,.fauser{color:var(--text)}
.fauser{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin:10px 0;line-height:1.65}
.finput{width:100%;min-height:90px;border-radius:12px;border:1px solid var(--line);background:var(--bg);color:var(--text);padding:12px 14px;font:inherit;resize:vertical;box-sizing:border-box}
.finput:disabled{opacity:.7}
.dim{opacity:.45;pointer-events:none;filter:grayscale(.4)}
.fmuted{color:var(--muted);font-size:13px;margin:8px 0}
.fhist{margin-top:22px;border-top:1px solid var(--line);padding-top:12px}
.fhist summary{cursor:pointer;font-weight:600;color:var(--text)}
.fhrec{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:10px 0;line-height:1.6}
.fhq{font-weight:600;margin-bottom:4px}
.fha{font-size:13px;color:var(--muted);margin-top:3px}
.fhts{font-size:11px;color:var(--muted);margin-top:6px}
__CARDCSS__
</style>
<script>
const DATA=__DATA__, DOCS=__DOCS__, GOAL=__GOAL__;
const FLASH=__FLASH__, FLASH_ON=__FLASH_ON__;
const CAT=Object.keys(DATA.categories)[0], R=DATA.categories[CAT];
const DOTC={"已学透":"var(--green)","巩固中":"var(--yellow)","浅学":"var(--grad)","待学":"var(--gray)"};
const cardEls={};
function stars(n){return '★'.repeat(n)+'<span class="se">'+'★'.repeat(Math.max(0,5-n))+'</span>';}
function theme(){return document.documentElement.dataset.theme;}
function renderOverview(){
  document.getElementById('sub').textContent=CAT+' · 共 '+R.total+' 个核心概念 · 依赖深度 '+(R.max_stage+1)+' 层 · 更新于 '+DATA.generated;
  if(DATA.goal){const g=document.getElementById('goal');g.style.display='';g.textContent='目标：'+DATA.goal;}
  const pct=R.total?Math.round(R.learned/R.total*100):0;
  document.getElementById('progbar').style.width=pct+'%';
  document.getElementById('progtxt').textContent=R.learned+'/'+R.total+' 已学透 · '+pct+'%';
  const tl=document.getElementById('timeline');tl.innerHTML='';let ls=-1;
  R.order.forEach(it=>{
    if(it.stage!==ls){const s=document.createElement('div');s.className='stage';
      s.textContent='阶段 '+(it.stage+1)+(it.stage===0?'（地基 · 无前置）':'（需先掌握前置）');tl.appendChild(s);ls=it.stage;}
    const done=it.status==='已学透';
    const card=document.createElement('div');
    card.className='card'+(it.title===R.current?' cur':'')+(done?' done linkcard':'');
    card.id='card-'+it.title;card.dataset.k=it.title;cardEls[it.title]=card;
    if(done)card.onclick=()=>go(it.title);
    card.innerHTML='<span class="dot" style="background:'+(DOTC[it.status]||'var(--gray)')+'"></span>'
      +'<div style="flex:1"><div class="t">'+it.title+'<span class="stars">'+stars(it.importance)+'</span></div>'
      +(it.desc?'<div class="d">'+it.desc+'</div>':'')
      +(it.prereqs.length?'<div class="pre"><b>前置：</b>'+it.prereqs.join(' · ')+'</div>':'')
      +((it.xprereqs&&it.xprereqs.length)?'<div class="pre xpre"><b>⚠ 跨类前置：</b>'+it.xprereqs.map(x=>x.title+'（在「'+x.category+'」大类，未学透）').join(' · ')+'</div>':'')+'</div>'
      +(it.title===R.current?'<span class="tag">▶ 你在这里 / 下一个</span>':(done?'<span class="tag ok">✓ 已学透 ›</span>':''));
    tl.appendChild(card);
  });
  const nx=document.getElementById('next');
  if(!R.next3.length)nx.innerHTML='<div class="why">本领域已全部学透 →</div>';
  else nx.innerHTML=R.next3.map(t=>{const it=R.order.find(o=>o.title===t);
    const sh=it.prereqs.length?('衔接 '+it.prereqs.join('、')):'关联当前知识';
    return '<div class="item"><b>'+t+'</b> <span style="color:var(--yellow);font-size:12px">'+stars(it.importance)+'</span>'
      +'<div class="why">'+(it.desc||'')+'</div><div class="why">'+sh+'</div></div>';}).join('');
  const ex=document.getElementById('exp');const list=(DATA.expansions||{})[CAT]||[];
  ex.innerHTML=list.length?list.slice().sort((a,b)=>b.importance-a.importance).map(e=>
    '<div class="e"><div class="nm">'+e.name+' <span style="color:var(--yellow);font-size:12px">'+stars(e.importance)+'</span></div>'
    +'<div class="why">'+(e.why||'')+'</div></div>').join(''):'<div class="why">（暂未配置扩展方向）</div>';
}
function buildNav(){
  const nb=document.getElementById('navbody');nb.innerHTML='';
  const groups=[],gmap={};
  R.order.forEach(it=>{(it.groups&&it.groups.length?it.groups:['未分类']).forEach(g=>{
    if(!gmap[g]){gmap[g]=[];groups.push(g);} gmap[g].push(it);});});
  groups.forEach(g=>{
    const wrap=document.createElement('div');wrap.className='navgrp';
    const hd=document.createElement('div');hd.className='navhd2';
    hd.innerHTML='<span class="chev">▸</span><span>'+g+'</span><span class="gc">'+gmap[g].length+'</span>';
    const body=document.createElement('div');body.className='navgbody';
    gmap[g].forEach(it=>{
      const done=it.status==='已学透';
      const a=document.createElement('a');a.className='navlink'+(done?'':' todo');a.dataset.k=it.title;
      a.innerHTML='<span class="nd" style="background:'+(DOTC[it.status]||'var(--gray)')+'"></span>'+it.title;
      a.onclick=function(e){e.stopPropagation(); if(done){go(it.title);} else {go('__overview__');setTimeout(()=>{const el=cardEls[it.title];if(el)el.scrollIntoView({behavior:'smooth',block:'center'});},60);} };
      body.appendChild(a);
    });
    hd.onclick=function(){wrap.classList.toggle('collapsed');};
    wrap.appendChild(hd);wrap.appendChild(body);nb.appendChild(wrap);
  });
}
function setActive(v){document.querySelectorAll('#sidenav .navlink').forEach(x=>x.classList.toggle('active',x.dataset.k===v));
  document.getElementById('homelink').classList.toggle('active',v==='__overview__');document.getElementById('graphlink').classList.toggle('active',v==='__graph__');document.getElementById('goallink').classList.toggle('active',v==='__goal__');var _fl=document.getElementById('flashlink');if(_fl)_fl.classList.toggle('active',v==='__flash__');}
function applyVizTheme(){document.querySelectorAll('#docview .vizframe').forEach(f=>{if(!f.src||f.src==='about:blank'){f.src=f.dataset.src+'?theme='+theme();}});}
function bindXref(){document.querySelectorAll('#docview a.xref').forEach(a=>a.onclick=()=>go(a.dataset.go));}
function bindToc(){
  const links=[...document.querySelectorAll('#toc .tl')];
  links.forEach(a=>a.onclick=()=>{const el=document.getElementById(a.dataset.id);if(el)el.scrollIntoView({behavior:'smooth',block:'start'});});
  if(window.__tio)window.__tio.disconnect();
  window.__tio=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){links.forEach(a=>a.classList.toggle('active',a.dataset.id===e.target.id));}});},{rootMargin:'-8% 0px -82% 0px'});
  document.querySelectorAll('#docview h2[id],#docview h3[id]').forEach(h=>window.__tio.observe(h));
}
function gIsDone(){if(!R||(R.learned||0)===0)return false;/*防呆：一个概念都没学透，目标不可能完成——拦住 AI 误写 status:已完成 / 空要求被当 100%*/var ls=false;try{ls=localStorage.getItem('goal_done_'+CAT)==='1';}catch(e){}return ls||(GOAL&&GOAL.status==='已完成');}
function gHasGoal(){return !!(GOAL&&GOAL.goal);}
// 解锁：本大类已设目标(goals.json 有该大类)即点亮；或已有概念学透。两者皆无才灰显。
function gUnlocked(){return gHasGoal()||R.learned>0;}
function gReqOk(r){return r&&(r.have===true||r.status==='✓'||r.status==='ok'||r.status===true);}
function gReqVia(r){return (r&&(r.via||r.refs||r.by))||[];}
function gReqName(r){return (typeof r==='string')?r:(r.name||r.req||'');}
function gReqKind(r){return (r&&r.kind&&(r.kind==='实践型'||r.kind==='practice'))?'实践型':'知识型';}
function gAttr(s){return String(s).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;');}
function gLearnedSet(){var s={};(R.order||[]).forEach(function(o){if(o.status==='已学透')s[o.title]=1;});return s;}
// 知识型覆盖度：via 概念里有多少已学透 / via 总数；via 空时回退 have 兜底
function gCov(r,LRN){var via=gReqVia(r);if(!via.length){var ok=gReqOk(r);return {pct:ok?100:0,n:0,tot:0,done:ok};}var n=0;via.forEach(function(c){if(LRN[c])n++;});return {pct:Math.round(n/via.length*100),n:n,tot:via.length,done:n>=via.length};}
function gCircle(c){if(c.done)return '<span class="gck ok">✓</span>';if(c.pct<=0)return '<span class="gck no">○</span>';return '<span class="gck part" title="'+c.n+'/'+c.tot+' 概念已学透" style="background:conic-gradient(var(--green) 0% '+c.pct+'%, color-mix(in srgb,var(--muted) 14%,transparent) '+c.pct+'% 100%)"></span>';}
// via 概念链接：单个直接可点；多个收成「{ N个概念 ⌄」点击展开
function gVia(via){if(!via.length)return '';if(via.length===1)return ' <a class="gvia1" data-go="'+gAttr(via[0])+'">'+via[0]+'</a>';var items=via.map(function(c){return '<a class="gviac" data-go="'+gAttr(c)+'">'+c+'</a>';}).join('<span class="gvsep">·</span>');return ' <span class="gexp"><span class="gexpb">{ '+via.length+'个概念 ⌄</span><span class="gexpbody">'+items+'</span></span>';}
function gPractOn(i){try{return localStorage.getItem('goal_pract_'+CAT+'_'+i)==='1';}catch(e){return false;}}
// 实时完成进度：知识型按覆盖比例 + 实践型按 ☑ 勾选，合计/总要求数
function gProgress(){
  var g=GOAL||{},done=gIsDone(),LRN=gLearnedSet(),reqs=g.requirements||[];
  var kreqs=reqs.filter(function(r){return gReqKind(r)!=='实践型';});
  var preqs=reqs.filter(function(r){return gReqKind(r)==='实践型';});
  var psum=0;
  kreqs.forEach(function(r){psum+=gCov(r,LRN).pct/100;});
  preqs.forEach(function(r,i){if(gPractOn(i))psum+=1;});
  var prog=reqs.length?Math.round(psum/reqs.length*100):0; if(done)prog=100;
  var ptier=prog>=80?'高':(prog>=50?'中':'低');
  return {prog:prog,ptier:ptier,tc:gTierColor(ptier)};
}
function gTierColor(t){return t==='高'?'var(--green)':(t==='中'?'var(--yellow)':'var(--red)');}
function updateGoalNav(){var gl=document.getElementById('goallink');if(!gl)return;gl.classList.toggle('disabled',!gUnlocked());gl.textContent=gIsDone()?'🎯 目标完成 ✅':'🎯 目标规划';}
function renderGoal(){
  var b=document.getElementById('goalbody');
  if(!gHasGoal()){b.innerHTML='<div class="gempty"><h1>🎯 目标规划</h1><p>你还没设定本领域的学习目标。告诉我你的<b>具体目标</b>（越细分越好：「CET-4 英语考试」优于「考试」，「企业内训分享」优于「分享」），我会联网对照真实要求、分析你与目标的差距并按优先级规划下一步。</p><p class="gref">参考分类：应试 · 求职 · 分享 · 知识变现 · 自主学习 · 无目标(AI自主发散)</p></div>';return;}
  var g=GOAL,done=gIsDone(),h='';
  h+='<div class="ghead"><h1>🎯 '+g.goal+'</h1>'+(g.goal_category?'<span class="gtag">'+g.goal_category+'</span>':'')+(g.sample?'<span class="gtag sample">示例</span>':'')+'</div><div class="gsub">更新于 '+(g.updated||'')+'</div>';
  if(done)h+='<div class="celebrate"><div class="cbig">🎉 目标完成！</div><div>恭喜拿下「'+g.goal+'」。</div></div>';
  if(g.practice_note)h+='<div class="gpractice">'+(g.domain_type?'<b>['+g.domain_type+'] </b>':'')+g.practice_note+'</div>';
  // 顶部进度＝实时完成进度（不再读 AI 写的 match，随 ✓/☑ 自动刷新）
  var LRN=gLearnedSet();
  var reqs=g.requirements||[];
  var kreqs=reqs.filter(function(r){return gReqKind(r)!=='实践型';});
  var preqs=reqs.filter(function(r){return gReqKind(r)==='实践型';});
  var P=gProgress();
  h+='<div class="gmeter"><div class="gpct" style="color:'+P.tc+'">'+P.prog+'%</div><div class="gbar"><i style="width:'+P.prog+'%;background:'+P.tc+'"></i></div><div class="gtier">目标完成进度 · '+(done?'已完成':P.ptier+' 档')+'</div></div>';
  if(g.summary)h+='<p class="gsum">'+g.summary+'</p>';
  if(reqs.length){
    if(kreqs.length){
      h+='<div class="gh3">目标要求对照 · 知识覆盖</div>';
      h+='<div class="gcap">真实世界对该目标的要求清单，用来查你的<b>学习覆盖度</b>；与左侧概念<b>非一一对应</b>——一条要求可能由多个概念覆盖，✓＝其覆盖概念已学透（部分学透按比例填充）。</div>';
      h+='<div class="greqs">'+kreqs.map(function(r){var c=gCov(r,LRN);return '<div class="greq">'+gCircle(c)+'<span class="greqn">'+gReqName(r)+gVia(gReqVia(r))+'</span></div>';}).join('')+'</div>';
    }
    if(preqs.length){
      h+='<div class="gh3">实践清单 · 靠动手达成（自检）</div>';
      h+='<div class="gpracts">'+preqs.map(function(r,i){var on=gPractOn(i);return '<div class="gpract"><span class="gpck'+(on?' on':'')+'" data-pi="'+i+'" role="checkbox" aria-checked="'+(on?'true':'false')+'" tabindex="0" title="点这个方框手动勾选">'+(on?'☑':'▢')+'</span><span class="greqn">'+gReqName(r)+'</span></div>';}).join('')+'</div>';
    }
  }
  if(!done&&P.ptier!=='高'&&g.recommend&&g.recommend.length)h+='<div class="gh3">下一步学习规划 · 按优先级</div><div class="grecs">'+g.recommend.map(function(r,i){if(typeof r==='string'){return '<div class="grec"><span class="gp">P'+(i+1)+'</span><div><div class="grn">'+r+'</div></div></div>';}var nm=r.concept||r.name||'',why=r.why||r.reason||'';return '<div class="grec"><span class="gp">P'+(r.priority||i+1)+'</span><div><div class="grn">'+nm+'</div>'+(why?'<div class="grw">'+why+'</div>':'')+'</div></div>';}).join('')+'</div>';
  if((done||P.ptier==='高')&&g.high_actions&&g.high_actions.length)h+='<div class="gh3">去实践 · 把知识用起来</div><ul class="gacts">'+g.high_actions.map(function(a){return '<li>'+a+'</li>';}).join('')+'</ul>';
  if(g.sources&&g.sources.length)h+='<div class="gsrc">目标要求来源：'+g.sources.map(function(s,i){return '<a href="'+s+'" target="_blank" rel="noopener">来源'+(i+1)+'</a>';}).join(' · ')+'</div>';
  h+='<div class="gfb"><div class="gh3">完成反馈</div><textarea id="gfbtext" placeholder="例如：参加 CET-4 考试通过！/ 已做完 3 套模拟题，阅读还需加强…"></textarea>';
  if(!done)h+='<div><button id="gdone" class="gbtn">🎉 标记目标完成</button><span class="gnote">点完成后请告诉我一声，我会更新数据、让知识图谱里这部分知识“活”起来。</span></div>';
  else h+='<div class="gnote">已完成。若有新目标，告诉我即可重新规划。</div>';
  h+='</div>';
  b.innerHTML=h;
  // via 概念点击跳转（单个 / 展开后的多个）
  b.querySelectorAll('[data-go]').forEach(function(a){a.onclick=function(e){e.stopPropagation();go(this.getAttribute('data-go'));};});
  // 多概念大括号：点击展开/收起（展开他人先收起）；点页面别处收回
  b.querySelectorAll('.gexpb').forEach(function(el){el.onclick=function(e){e.stopPropagation();var p=el.parentNode,wasOpen=p.classList.contains('open');document.querySelectorAll('.gexp.open').forEach(function(x){x.classList.remove('open');var bb=x.querySelector('.gexpb');if(bb)bb.textContent=bb.textContent.replace('⌃','⌄');});if(!wasOpen){p.classList.add('open');el.textContent=el.textContent.replace('⌄','⌃');}};});
  if(!window.__gexpBound){document.addEventListener('click',function(e){if(!(e.target.closest&&e.target.closest('.gexp'))){document.querySelectorAll('.gexp.open').forEach(function(x){x.classList.remove('open');var bb=x.querySelector('.gexpb');if(bb)bb.textContent=bb.textContent.replace('⌃','⌄');});}});window.__gexpBound=true;}
  // 实践清单自检：仅当用户【手动点击复选框本身】才切换；就地更新，绝不因重渲染/切回页面而自动改动
  b.querySelectorAll('.gpck[data-pi]').forEach(function(ck){
    ck.onclick=function(e){
      e.stopPropagation();
      var i=ck.getAttribute('data-pi'),k='goal_pract_'+CAT+'_'+i,on=false;
      try{on=localStorage.getItem(k)==='1';}catch(e){}
      var now=!on;
      try{localStorage.setItem(k,now?'1':'0');}catch(e){}
      ck.classList.toggle('on',now); ck.textContent=now?'☑':'▢'; ck.setAttribute('aria-checked',now?'true':'false');
      var P=gProgress();   // 仅就地刷新顶部进度，不整页重渲染
      var pe=b.querySelector('.gpct'); if(pe){pe.textContent=P.prog+'%';pe.style.color=P.tc;}
      var be=b.querySelector('.gbar>i'); if(be){be.style.width=P.prog+'%';be.style.background=P.tc;}
      var te=b.querySelector('.gtier'); if(te)te.textContent='目标完成进度 · '+(gIsDone()?'已完成':P.ptier+' 档');
    };
  });
  var db=document.getElementById('gdone');
  if(db)db.onclick=function(){try{localStorage.setItem('goal_done_'+CAT,'1');var fb=document.getElementById('gfbtext');if(fb&&fb.value)localStorage.setItem('goal_fb_'+CAT,fb.value);}catch(e){}updateGoalNav();renderGoal();try{var gf=document.getElementById('graphframe');if(gf&&gf.src&&gf.src!=='about:blank')gf.contentWindow.postMessage({goalDone:true},'*');}catch(e){}window.scrollTo(0,0);};
}
function flashKey(s){return 'flash_'+s+'_'+CAT;}
function flashHist(){try{return JSON.parse(localStorage.getItem(flashKey('hist'))||'[]');}catch(e){return [];}}
function flashBuildId(){return (FLASH&&FLASH.generated)||'0';}
function flashState(){try{return JSON.parse(localStorage.getItem(flashKey('st')+'_'+flashBuildId())||'{"round":0,"answers":{}}');}catch(e){return {round:0,answers:{}};}}
function setFlashState(st){try{localStorage.setItem(flashKey('st')+'_'+flashBuildId(),JSON.stringify(st));}catch(e){}}
function pushHist(rec){var h=flashHist();h.unshift(rec);try{localStorage.setItem(flashKey('hist'),JSON.stringify(h));}catch(e){}}
function fesc(x){return (x==null?'':String(x)).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function kindLabel(k){return k==='实践型'?'参考方案 · 方案与计划':(k==='自测'?'参考（笔记原文 / 自己先说再对照）':'参考答案 · 答案与分析');}
function updateFlashNav(){var fl=document.getElementById('flashlink');if(!fl)return;fl.style.display=FLASH_ON?'':'none';}
function histHtml(){var hist=flashHist();return '<details class="fhist"><summary>📋 已答记录（'+hist.length+'）</summary>'+(hist.length?hist.map(function(r){return '<div class="fhrec"><div class="fhq">'+fesc(r.q)+' <span class="fkind">'+fesc(r.kind)+'</span></div><div class="fha"><b>你的回答：</b>'+fesc(r.user||'（未填）')+'</div><div class="fha"><b>'+fesc(kindLabel(r.kind))+'：</b>'+fesc(r.answer)+'</div><div class="fhts">'+fesc(r.ts)+'</div></div>';}).join(''):'<div class="fmuted">还没有已答记录。</div>')+'</details>';}
function renderFlash(){
  var b=document.getElementById('flashbody');var learned=(R&&R.learned)||0;
  if(learned<2){
    b.innerHTML='<h1 class="ttl">🎴 抽卡复习</h1><div class="fbuild">建设中…　学满 2 个知识点后开启（当前 '+learned+'/2）</div>'+
      '<div class="fdeck dim">'+[0,1,2].map(function(i){return '<div class="fcard back"></div>';}).join('')+'</div>'+
      '<div class="fqbox dim">问题显示框</div><textarea class="finput dim" disabled placeholder="用户输入框（学满 2 个知识点后激活）"></textarea><div class="fabox dim">答案显示框</div>'+histHtml();
    return;
  }
  var cards=(FLASH&&FLASH.cards)||[];
  if(!cards.length){b.innerHTML='<h1 class="ttl">🎴 抽卡复习</h1><div class="fbuild">本次构建尚未生成卡池。下次刷新视图时会基于已学知识点生成卡池。</div>'+histHtml();return;}
  var rounds=Math.ceil(cards.length/3);
  var st=flashState(); if(st.round>rounds-1)st.round=rounds-1; if(st.round<0)st.round=0; var round=st.round;
  var head='<h1 class="ttl">🎴 抽卡复习 <span style="color:var(--muted);font-weight:400;font-size:14px">卡池 '+cards.length+' 张 · 第 '+(round+1)+'/'+rounds+' 批 · 每批翻 1 张'+(rounds>1?'（可刷新 '+(rounds-1)+' 次）':'')+'</span></h1>';
  var batch=cards.slice(round*3,round*3+3);
  function refreshBtn(){return round<rounds-1?'<div style="margin:12px 0"><button class="gbtn" id="frefresh">🔄 再抽一批（还剩 '+(rounds-1-round)+' 批）</button></div>':'<div class="fmuted">本卡池已抽完。下次构建刷新出新卡池，已答的进下方“已答记录”。</div>';}
  function bindRefresh(){var rb=document.getElementById('frefresh');if(rb)rb.onclick=function(){st.round=round+1;setFlashState(st);renderFlash();};}
  var ans=st.answers&&st.answers[round];
  if(ans){
    b.innerHTML=head+'<div class="fdeck"><div class="fcard flip"><div class="fqonly">'+fesc(ans.q)+' <span class="fkind">'+fesc(ans.kind)+'</span></div></div></div>'+
      '<div class="fqbox show"><b>问题：</b>'+fesc(ans.q)+'</div>'+
      '<div class="fauser"><b>你的回答：</b>'+fesc(ans.user||'（未填）')+'</div>'+
      '<div class="fabox show"><b>'+fesc(kindLabel(ans.kind))+'：</b><br>'+fesc(ans.answer)+'</div>'+
      refreshBtn()+histHtml();
    bindRefresh();return;
  }
  b.innerHTML=head+'<div class="fdeck" id="fdeck">'+batch.map(function(c,i){return '<div class="fcard back" data-i="'+i+'"></div>';}).join('')+'</div>'+
    '<div class="fqbox" id="fqbox">翻开一张卡，这里显示问题。</div>'+
    '<textarea class="finput" id="finput" disabled placeholder="翻牌后在此作答…"></textarea>'+
    '<div style="margin:8px 0"><button class="gbtn" id="fsubmit" disabled>提交答案</button></div>'+
    '<div class="fabox" id="fabox">提交后显示参考答案。</div>'+histHtml();
  var picked=null;
  document.querySelectorAll('#fdeck .fcard').forEach(function(el){
    el.onclick=function(){
      if(picked!==null)return;picked=parseInt(el.dataset.i,10);var c=batch[picked];
      document.querySelectorAll('#fdeck .fcard').forEach(function(x){if(x!==el)x.remove();});
      el.classList.remove('back');el.classList.add('flip');el.innerHTML='<div class="fqonly">'+fesc(c.q)+' <span class="fkind">'+fesc(c.kind)+'</span></div>';
      var qb=document.getElementById('fqbox');qb.classList.add('show');qb.innerHTML='<b>问题：</b>'+fesc(c.q);
      var inp=document.getElementById('finput');inp.disabled=false;inp.focus();document.getElementById('fsubmit').disabled=false;
    };
  });
  document.getElementById('fsubmit').onclick=function(){
    if(picked===null)return;var c=batch[picked];var user=document.getElementById('finput').value;
    var ab=document.getElementById('fabox');ab.classList.add('show');ab.innerHTML='<b>'+fesc(kindLabel(c.kind))+'：</b><br>'+fesc(c.answer);
    document.getElementById('finput').disabled=true;this.disabled=true;
    var rec={q:c.q,kind:c.kind,answer:c.answer,user:user,ts:new Date().toLocaleString()};
    if(!st.answers)st.answers={};st.answers[round]=rec;setFlashState(st);pushHist(rec);renderFlash();
  };
}
function go(v){
  const ov=document.getElementById('overview'),dw=document.getElementById('docwrap'),gw=document.getElementById('graphwrap'),goalw=document.getElementById('goalwrap'),flashw=document.getElementById('flashwrap');
  gw.style.display='none';goalw.style.display='none';flashw.style.display='none';
  if(v==='__goal__'){if(!gUnlocked()){go('__overview__');return;}ov.style.display='none';dw.style.display='none';goalw.style.display='block';renderGoal();setActive('__goal__');document.getElementById('crumb').innerHTML='/ <b>'+(gIsDone()?'目标完成 ✅':'目标规划')+'</b>';location.hash=encodeURIComponent('__goal__');window.scrollTo(0,0);return;}
  if(v==='__graph__'){ov.style.display='none';dw.style.display='none';gw.style.display='block';
    const gf=document.getElementById('graphframe');if(!gf.src||gf.src==='about:blank'){gf.src=gf.dataset.src+'?theme='+theme()+'&goaldone='+(gIsDone()?1:0);}else{try{gf.contentWindow.postMessage({theme:theme()},'*');gf.contentWindow.postMessage({goalDone:gIsDone()},'*');}catch(e){}}
    setActive('__graph__');document.getElementById('crumb').innerHTML='/ <b>知识图谱</b>';location.hash=encodeURIComponent('__graph__');window.scrollTo(0,0);return;}
  if(v==='__flash__'){if(!FLASH_ON){go('__overview__');return;}ov.style.display='none';dw.style.display='none';flashw.style.display='block';renderFlash();setActive('__flash__');document.getElementById('crumb').innerHTML='/ <b>抽卡复习</b>';location.hash=encodeURIComponent('__flash__');window.scrollTo(0,0);return;}
  if(v==='__overview__'||!DOCS[v]){ov.style.display='';dw.style.display='none';setActive('__overview__');
    document.getElementById('crumb').innerHTML='/ <b>学习路线图</b>';location.hash='';window.scrollTo(0,0);return;}
  ov.style.display='none';dw.style.display='grid';
  document.getElementById('docview').innerHTML=DOCS[v].doc;
  document.getElementById('toc').innerHTML=DOCS[v].toc;
  applyVizTheme();bindXref();bindToc();setActive(v);
  document.getElementById('crumb').innerHTML='/ <span class="cl" id="crmhome">学习路线图</span> / <b>'+v+'</b>';
  const ch=document.getElementById('crmhome');if(ch)ch.onclick=()=>go('__overview__');
  location.hash=encodeURIComponent(v);window.scrollTo(0,0);
}
const THEMES=[["light","◐ 浅"],["dark","◑ 深"],["ink","❖ 宣纸"],["inkdark","❖ 夜墨"]];
function themeIdx(name){for(var i=0;i<THEMES.length;i++)if(THEMES[i][0]===name)return i;return 1;}
function setTheme(t){var r=document.documentElement;r.dataset.theme=t;
  document.getElementById('themebtn').textContent=THEMES[themeIdx(t)][1];
  document.querySelectorAll('#docview .vizframe').forEach(f=>{try{f.contentWindow.postMessage({theme:t},'*');}catch(e){}});
  var gf=document.getElementById('graphframe');if(gf&&gf.src&&gf.src!=='about:blank'){try{gf.contentWindow.postMessage({theme:t},'*');}catch(e){}}}
document.getElementById('themebtn').onclick=function(){var cur=document.documentElement.dataset.theme||'dark';
  setTheme(THEMES[(themeIdx(cur)+1)%THEMES.length][0]);};
setTheme(document.documentElement.dataset.theme||'light');
document.getElementById('homelink').onclick=()=>go('__overview__');
document.getElementById('graphlink').onclick=()=>go('__graph__');
document.getElementById('goallink').onclick=()=>{if(gUnlocked())go('__goal__');};
document.getElementById('flashlink').onclick=()=>{if(FLASH_ON)go('__flash__');};
window.addEventListener('message',function(e){if(e&&e.data&&e.data.goto){var g=e.data.goto;if(DOCS[g])go(g);else{go('__overview__');setTimeout(function(){var el=cardEls[g];if(el)el.scrollIntoView({behavior:'smooth',block:'center'});},80);}}});
renderOverview();buildNav();updateGoalNav();updateFlashNav();
go(location.hash?decodeURIComponent(location.hash.slice(1)):'__overview__');
window.addEventListener('hashchange',()=>{go(location.hash?decodeURIComponent(location.hash.slice(1)):'__overview__');});
</script></body></html>"""

if __name__ == '__main__':
    main()
# end of plan_path.py
