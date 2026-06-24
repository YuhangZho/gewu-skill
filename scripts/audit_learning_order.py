#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
审计学习路线是否被后置概念污染。

检查已完成/学习中的笔记正文，若显式提到同大类路线中排在后面的概念名，
报告为“需要人工判断”的风险点。脚本只做文本级证据，不替代语义审查。
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from build_graph import collect, global_vault_path, DONE_STATUS, IN_PROGRESS_STATUS  # noqa: E402
from plan_path import plan_category  # noqa: E402


STUDIED = (DONE_STATUS, IN_PROGRESS_STATUS)
IGNORED_SECTION_RE = re.compile(r'^##\s+(相关|参考资料|🔭\s*视野拓展)', re.M)


def _body_for_learning_audit(body):
    m = IGNORED_SECTION_RE.search(body or '')
    return (body or '')[:m.start()] if m else (body or '')


def audit_vault(vault):
    notes = collect(vault)
    by_cat = {}
    for title, note in notes.items():
        by_cat.setdefault(note['category'], {})[title] = note

    findings = []
    for cat, items in sorted(by_cat.items()):
        if cat in ('fragment', '碎片'):
            continue
        plan = plan_category(items, None, notes)
        order = [o['title'] for o in plan.get('order', [])]
        pos = {title: i for i, title in enumerate(order)}
        for title, note in sorted(items.items(), key=lambda x: pos.get(x[0], 10**9)):
            if note.get('status') not in STUDIED:
                continue
            body = _body_for_learning_audit(note.get('body', ''))
            later = [
                other for other in order
                if other != title and pos.get(other, -1) > pos.get(title, -1) and other in body
            ]
            if later:
                findings.append({
                    'category': cat,
                    'concept': title,
                    'route_index': pos.get(title, -1) + 1,
                    'downstream_mentions': later,
                    'message': '正文显式提到路线后置概念；若这是解释前提，应改写为已学前置/日常语言，或调整 prereqs。',
                })
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--vault', default=os.environ.get('GEWU_VAULT') or global_vault_path() or os.getcwd())
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--fail-on-findings', action='store_true')
    args = ap.parse_args()

    findings = audit_vault(args.vault)
    if args.json:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
    elif not findings:
        print('OK：未发现已学/学习中笔记显式提到路线后置概念。')
    else:
        print('发现 %d 个后置概念提名风险：' % len(findings))
        for f in findings:
            print('【%s】%d. %s -> %s' % (
                f['category'], f['route_index'], f['concept'], '、'.join(f['downstream_mentions'])
            ))
            print('  ' + f['message'])
    if findings and args.fail_on_findings:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
