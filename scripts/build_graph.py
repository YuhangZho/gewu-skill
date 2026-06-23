#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
build_graph.py — 扫描知识库的 Markdown 笔记，生成 Obsidian 风格的力导向知识图谱。
输出：<vault>/知识图谱.html（单文件、离线可用）和 <vault>/graph_data.json。

用法:
    python build_graph.py                 # 默认扫描脚本上一级的 ../../知识库
    python build_graph.py --vault "路径"   # 指定知识库根目录
    python build_graph.py --vault "路径" --out "输出.html"
"""
import os, re, json, argparse, datetime

# 已掌握＝已学透 或 浅学。浅学只是"没走完整费曼七步"的轻学，地位与已学透同级：
# 一样解锁下游、一样计入进度、一样满足前置；唯一区别是配色图标 + 可被「融合」成大类。
LEARNED = ('已学透', '浅学')

# ---------- frontmatter 极简解析 ----------
def parse_scalar(v):
    v = v.strip()
    if v.startswith('[') and v.endswith(']'):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(x) for x in split_list(inner)]
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    return v

def split_list(s):
    out, buf, q = [], '', None
    for ch in s:
        if q:
            buf += ch
            if ch == q:
                q = None
        elif ch in '"\'':
            q = ch; buf += ch
        elif ch == ',':
            out.append(buf); buf = ''
        else:
            buf += ch
    if buf.strip():
        out.append(buf)
    return out

def strip_inline_comment(val):
    """剥离行内注释：识别引号与方括号嵌套，仅在最外层、且 # 前是空白(或行首)时截断。
    这样 `["前期准备"]   # 分类名…`、`[a,b] # x` 都能正确去掉注释，
    而引号/括号内的 # 不会被误删。"""
    q, depth = None, 0
    for i, ch in enumerate(val):
        if q:
            if ch == q:
                q = None
        elif ch in '"\'':
            q = ch
        elif ch == '[':
            depth += 1
        elif ch == ']':
            depth = max(0, depth - 1)
        elif ch == '#' and depth == 0 and (i == 0 or val[i-1] in ' \t'):
            return val[:i].rstrip()
    return val.rstrip()

def parse_frontmatter(text):
    fm, body = {}, text
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end != -1:
            raw = text[3:end].strip('\n')
            body = text[end+4:].lstrip('\n')
            for line in raw.split('\n'):
                if not line.strip() or line.strip().startswith('#'):
                    continue
                m = re.match(r'^([A-Za-z_][\w-]*)\s*:\s*(.*)$', line)
                if m:
                    key, val = m.group(1), strip_inline_comment(m.group(2))
                    fm[key] = parse_scalar(val)
    return fm, body

WIKILINK = re.compile(r'\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]')
SKIP_NOTE_DIRS = {'_transcript', '_system', '_viz'}

def collect(vault):
    notes = {}
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if d.lower() not in SKIP_NOTE_DIRS]
        for fn in files:
            if not fn.lower().endswith('.md'):
                continue
            path = os.path.join(root, fn)
            try:
                text = open(path, encoding='utf-8').read()
            except Exception:
                continue
            fm, body = parse_frontmatter(text)
            title = (fm.get('title') or os.path.splitext(fn)[0]).strip()
            cat = (fm.get('category') or os.path.basename(os.path.dirname(path)) or '未分类')
            if isinstance(cat, list):
                cat = cat[0] if cat else '未分类'
            status = fm.get('status') or '待学'
            aliases = fm.get('aliases') or []
            if isinstance(aliases, str):
                aliases = [aliases]
            related = fm.get('related') or []
            if isinstance(related, str):
                related = [related]
            prereqs = fm.get('prereqs') or []
            if isinstance(prereqs, str):
                prereqs = [prereqs]
            try:
                importance = int(str(fm.get('importance', 3)).strip())
            except Exception:
                importance = 3
            viz = fm.get('viz') or ''
            if isinstance(viz, list):
                viz = viz[0] if viz else ''
            groups = fm.get('groups') or []
            if isinstance(groups, str):
                groups = [groups]
            links = [m.strip() for m in WIKILINK.findall(body)]
            links += [str(r).strip() for r in related]
            notes[title] = {
                'title': title, 'category': str(cat).strip(), 'status': str(status).strip(),
                'importance': max(1, min(5, importance)),
                'viz': str(viz).strip(),
                'groups': [str(g).strip() for g in groups],
                'prereqs': [str(p).strip() for p in prereqs],
                'aliases': [str(a).strip() for a in aliases],
                'links': links, 'body': body.strip(),
                'rel': os.path.relpath(path, vault).replace('\\', '/'),
            }
    return notes

def build_graph(notes):
    # 标题/别名 -> 规范标题 的索引，便于解析双链
    index = {}
    for t, n in notes.items():
        index[t.lower()] = t
        for a in n['aliases']:
            index[a.lower()] = t

    categories = {}
    for n in notes.values():
        categories.setdefault(n['category'], 0)
        categories[n['category']] += 1

    nodes, links, seen, depseen = [], [], set(), set()

    # outer fringe（知识空间理论 KST）：前置全部已掌握、自身未掌握 → ready=可学的"下一站"
    def is_ready(n):
        if n['status'] in LEARNED:
            return False
        for raw in n['prereqs']:
            src = index.get(str(raw).strip().lower())
            if src is None or notes[src]['status'] not in LEARNED:
                return False
        return True
    # 大类中心节点
    for cat, cnt in categories.items():
        nodes.append({'id': 'cat::' + cat, 'label': cat, 'type': 'category',
                      'category': cat, 'count': cnt})
    # 概念节点 + 概念->大类 连边
    for t, n in notes.items():
        nodes.append({'id': t, 'label': t, 'type': 'concept', 'category': n['category'],
                      'status': n['status'], 'importance': n['importance'],
                      'ready': is_ready(n),
                      'aliases': n['aliases'], 'body': n['body'], 'rel': n['rel'],
                      'viz': n.get('viz', '')})
        links.append({'source': t, 'target': 'cat::' + n['category'], 'kind': 'belong'})
    # 依赖有向边：prereq -> concept（前置解锁后续）
    for t, n in notes.items():
        for raw in n['prereqs']:
            src = index.get(raw.lower())
            if src and src != t:
                key = (src, t)
                if key in depseen:
                    continue
                depseen.add(key)
                seen.add(tuple(sorted((src, t))))  # 依赖对不再重复画关联线
                links.append({'source': src, 'target': t, 'kind': 'dep'})
    # 概念之间的关联双链（跳过已是依赖关系的对）
    for t, n in notes.items():
        for raw in n['links']:
            tgt = index.get(raw.lower())
            if tgt and tgt != t:
                key = tuple(sorted((t, tgt)))
                if key in seen:
                    continue
                seen.add(key)
                links.append({'source': t, 'target': tgt, 'kind': 'link'})
    return {'nodes': nodes, 'links': links,
            'categories': sorted(categories.keys()),
            'generated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}

def _goal_alive(notes, sysdir):
    """返回 (potential, baked)：potential=有目标的领域里"将会呼吸"的节点(前端按需点亮)；baked=目标已完成、生成时即点亮。"""
    gp = os.path.join(sysdir, 'goals.json'); potential = {}; baked = {}
    if not os.path.isfile(gp):
        return potential, baked
    try:
        goals = json.load(open(gp, encoding='utf-8'))
    except Exception:
        return potential, baked
    def fill(target, gc, related):
        for t, n in notes.items():
            if n['category'] == gc and n['status'] in LEARNED:
                target.setdefault(t, 'full')
        for rd in (related or []):
            for t, n in notes.items():
                if n['category'] == rd and n['status'] in LEARNED and t not in target:
                    target[t] = 'weak'
    for gc, go in goals.items():
        if not isinstance(go, dict):
            continue
        rel = go.get('related_domains') or []
        fill(potential, gc, rel)
        if go.get('status') == '已完成':
            fill(baked, gc, rel)
    return potential, baked

def _apply_alive(graph, potential, baked):
    for nd in graph['nodes']:
        if nd.get('type') == 'concept':
            nd['alivep'] = potential.get(nd['label'], '')
            nd['alive'] = baked.get(nd['label'], '')

# ---------- HTML 模板（单文件、离线、自带力导向模拟）----------
HTML = r"""<!DOCTYPE html>
<html lang="zh" data-theme="dark"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>知识图谱 · Knowledge Graph</title>
<style>
:root[data-theme="dark"]{color-scheme:dark;--bg:#0f1115;--panel:#171a21;--line:#2a2f3a;--text:#e7e9ee;--muted:#9aa3b2;--accent:#7aa2f7;--linkw:#39404f;--linkm:#56607a;--node:#202637;--ring:#565f73;--bq:#1c2230;--bqt:#cdd6f4;--mdtext:#cfd4df;--hudbg:rgba(23,26,33,.7);--alive:#34c759}
:root[data-theme="light"]{color-scheme:light;--bg:#f7f8fa;--panel:#ffffff;--line:#e2e5ea;--text:#1f2430;--muted:#6b7280;--accent:#3b5bdb;--linkw:#c5cad4;--linkm:#9aa3b2;--node:#eef1f6;--ring:#9aa3b2;--bq:#eef1fb;--bqt:#26324d;--mdtext:#3a4150;--hudbg:rgba(255,255,255,.82);--alive:#2bb24c}
/* 中国水墨 · 宣纸（浅）*/
:root[data-theme="ink"]{color-scheme:light;--bg:#efe5cf;--panel:#f6f0e1;--line:#d8ccae;--text:#2b2620;--muted:#8a7c64;--accent:#9c3b2e;--linkw:#cdc1a3;--linkm:#b1a181;--node:#e6dbbf;--ring:#b1a486;--bq:#ece1c8;--bqt:#4a4030;--mdtext:#403a2d;--hudbg:rgba(246,240,225,.82);--alive:#5a8f6d}
/* 中国水墨 · 夜墨（深）*/
:root[data-theme="inkdark"]{color-scheme:dark;--bg:#181813;--panel:#222218;--line:#36362b;--text:#ece3d0;--muted:#9a9079;--accent:#d6604d;--linkw:#3a3a2e;--linkm:#575747;--node:#2a2a1f;--ring:#5a5a4b;--bq:#23231b;--bqt:#d8cfb6;--mdtext:#cbc2a9;--hudbg:rgba(34,34,24,.74);--alive:#79c79a}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:var(--bg);color:var(--text);
font-family:-apple-system,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;overflow:hidden}
#wrap{display:flex;height:100%}
#graph{flex:1;position:relative}
svg{width:100%;height:100%;display:block;cursor:grab}
svg.dragging{cursor:grabbing}
.link{stroke:var(--linkw);stroke-width:1}
.link.link-strong{stroke:var(--linkm);stroke-width:1.6}
.link.link-dep{stroke:var(--accent);stroke-width:1.7;stroke-dasharray:5 4}
.node circle{cursor:pointer;transition:stroke .15s}
.node text{font-size:11px;fill:var(--muted);pointer-events:none;paint-order:stroke;
stroke:var(--bg);stroke-width:3px}
.node.cat text{font-size:13px;fill:var(--text);font-weight:600}
.dim{opacity:.12;transition:opacity .2s}
.hl text{fill:var(--text)}
#hud{position:absolute;top:14px;left:14px;right:14px;display:flex;gap:10px;align-items:center;
flex-wrap:wrap;pointer-events:none}
#search{pointer-events:auto;background:var(--panel);border:1px solid var(--line);color:var(--text);
padding:8px 12px;border-radius:8px;width:240px;outline:none}
#legend{pointer-events:auto;display:flex;gap:12px;flex-wrap:wrap;background:var(--hudbg);
padding:6px 10px;border-radius:8px;font-size:12px;color:var(--muted)}
#legend span{display:inline-flex;align-items:center;gap:5px}
#legend i{width:10px;height:10px;border-radius:50%;display:inline-block}
#meta{margin-left:auto;font-size:12px;color:var(--muted);background:var(--hudbg);
padding:6px 10px;border-radius:8px;pointer-events:auto}
#panel{width:380px;max-width:42%;background:var(--panel);border-left:1px solid var(--line);
padding:22px;overflow:auto;display:none}
#panel.open{display:block}
#panel h1{font-size:20px;margin:.1em 0 .2em}
#panel .badge{display:inline-block;font-size:12px;color:var(--muted);border:1px solid var(--line);
border-radius:20px;padding:2px 10px;margin:0 6px 10px 0}
#panel .md{font-size:14px;line-height:1.7;color:var(--mdtext)}
#panel .md h2{font-size:15px;margin:1.2em 0 .3em;color:var(--text)}
#panel .md blockquote{margin:.4em 0;padding:.4em .8em;border-left:3px solid var(--accent);
background:var(--bq);color:var(--bqt);border-radius:0 6px 6px 0}
#panel .md a{color:var(--accent);text-decoration:none;cursor:pointer}
#panel .md a:hover{text-decoration:underline}
#close{float:right;cursor:pointer;color:var(--muted);font-size:20px;line-height:1;border:none;
background:none}
#hint{position:absolute;bottom:12px;left:14px;font-size:11px;color:var(--muted);opacity:.7}
#themebtn{pointer-events:auto;background:var(--panel);border:1px solid var(--line);color:var(--text);padding:8px 11px;border-radius:8px;cursor:pointer;font-size:13px;transition:background .2s,border-color .2s,color .2s}
#themebtn:hover{border-color:var(--accent);color:var(--accent)}
#arrow path{fill:var(--accent)}
@keyframes nodeBreath{0%,100%{filter:drop-shadow(0 0 1px var(--alive))}50%{filter:drop-shadow(0 0 8px var(--alive))}}
.node.alive-full circle{animation:nodeBreath 3s ease-in-out infinite}
.node.alive-weak circle{animation:nodeBreath 4.8s ease-in-out infinite;opacity:.92}
/* —— 水墨主题质感（宣纸纹理 / 墨晕 / 楷书标题）—— */
:root[data-theme="ink"] body,:root[data-theme="inkdark"] body{
background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.045'/%3E%3C/svg%3E");
background-size:160px 160px}
:root[data-theme="ink"] .node.cat circle,:root[data-theme="inkdark"] .node.cat circle{filter:drop-shadow(0 1px 3px rgba(0,0,0,.22))}
:root[data-theme="ink"] #panel h1,:root[data-theme="inkdark"] #panel h1,
:root[data-theme="ink"] .node.cat text,:root[data-theme="inkdark"] .node.cat text{
font-family:"Kaiti SC","STKaiti","KaiTi","Songti SC","SimSun",serif;letter-spacing:.5px}
:root[data-theme="ink"] #search,:root[data-theme="inkdark"] #search,
:root[data-theme="ink"] #themebtn,:root[data-theme="inkdark"] #themebtn{border-radius:4px}
:root[data-theme="ink"] #panel .md blockquote,:root[data-theme="inkdark"] #panel .md blockquote{border-left-width:4px;font-style:italic}
</style></head><body>
<div id="wrap">
  <div id="graph">
    <div id="hud">
      <input id="search" placeholder="搜索概念… / search"><button id="themebtn">◐ 深/浅</button>
      <div id="legend"></div>
      <div id="meta"></div>
    </div>
    <svg id="svg"><defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7"
        orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#7aa2f7"></path></marker>
    </defs><g id="scene"><g id="links"></g><g id="nodes"></g></g></svg>
    <div id="hint">滚轮缩放 · 拖动空白平移 · 拖动节点定位 · 点击节点看笔记</div>
  </div>
  <div id="panel"><button id="close">×</button><div id="panelbody"></div></div>
</div>
<script>
(function(){var p=new URLSearchParams(location.search).get('theme');if(p)document.documentElement.dataset.theme=p;window.addEventListener('message',function(e){if(e&&e.data&&e.data.theme){if(typeof applyTheme==='function')applyTheme(e.data.theme);else document.documentElement.dataset.theme=e.data.theme;}});})();
const DATA = __DATA__;
// 两套色板：modern（科技黑白）与 ink（传统国画颜料：花青·朱砂·石绿·赭石·黛紫·藤黄·石青·胭脂·墨青）
const PALETTES = {
  modern:{cat:["#7aa2f7","#9ece6a","#e0af68","#bb9af7","#f7768e","#2ac3de","#ff9e64","#73daca","#c0caf5"],
          status:{"已学透":"#9ece6a","浅学":"#56b6c2","待学":"#565f73"}},
  ink:{cat:["#2e5b7c","#b83a2e","#5a8f6d","#9c6b3f","#6a5a7d","#c89a3c","#3f6f8f","#a23b53","#4a5a66"],
       status:{"已学透":"#5a8f6d","浅学":"#5a86a0","待学":"#9a8f78"}}};
function themeFamily(){var t=document.documentElement.dataset.theme;return (t==='ink'||t==='inkdark')?'ink':'modern';}
let CATCOLORS, STATUSRING; const catColor = {};
function buildPalette(){var p=PALETTES[themeFamily()];CATCOLORS=p.cat;STATUSRING=p.status;
  DATA.categories.forEach((c,i)=>catColor[c]=CATCOLORS[i%CATCOLORS.length]);}
buildPalette();

const svg=document.getElementById('svg'), scene=document.getElementById('scene');
const gLinks=document.getElementById('links'), gNodes=document.getElementById('nodes');
const NS="http://www.w3.org/2000/svg";
let W=svg.clientWidth, H=svg.clientHeight;

const nodes=DATA.nodes.map(n=>Object.assign({},n));
const byId={}; nodes.forEach(n=>byId[n.id]=n);
const links=DATA.links.map(l=>({source:byId[l.source],target:byId[l.target],kind:l.kind})).filter(l=>l.source&&l.target);
const deg={}; nodes.forEach(n=>deg[n.id]=0);
links.forEach(l=>{deg[l.source.id]++;deg[l.target.id]++;});

// 初始布局：大类围成圈，概念散在附近
let ci=0; const cats=nodes.filter(n=>n.type==='category');
nodes.forEach(n=>{
  if(n.type==='category'){const a=(ci++/Math.max(1,cats.length))*2*Math.PI;
    n.x=W/2+Math.cos(a)*Math.min(W,H)*0.22; n.y=H/2+Math.sin(a)*Math.min(W,H)*0.22;}
  else{n.x=W/2+(Math.random()-.5)*W*0.6; n.y=H/2+(Math.random()-.5)*H*0.6;}
  n.vx=0;n.vy=0;
});

// 建 SVG 元素
const linkEls=links.map(l=>{const e=document.createElementNS(NS,'line');
  let cls='link'; if(l.kind==='link')cls+=' link-strong'; if(l.kind==='dep')cls+=' link-dep';
  e.setAttribute('class',cls);
  if(l.kind==='dep')e.setAttribute('marker-end','url(#arrow)');
  gLinks.appendChild(e);return e;});
const nodeEls=nodes.map(n=>{
  const g=document.createElementNS(NS,'g'); g.setAttribute('class','node'+(n.type==='category'?' cat':'')+(n.alive?' alive-'+n.alive:''));
  const c=document.createElementNS(NS,'circle');
  const r=n.type==='category'?(12+Math.min(14,(n.count||1)*1.6)):(4+(n.importance||3)*2.2);
  n.r=r; c.setAttribute('r',r);
  c.style.fill = n.type==='category'?catColor[n.category]:'var(--node)';
  c.style.stroke = n.type==='category'?'var(--bg)':(STATUSRING[n.status]||'var(--ring)');
  c.setAttribute('stroke-width', n.type==='category'?3:2);
  const t=document.createElementNS(NS,'text'); t.setAttribute('x',r+4); t.setAttribute('y',4);
  t.textContent=n.label;
  g.appendChild(c); g.appendChild(t); gNodes.appendChild(g);
  g._node=n; n._g=g; n._c=c;
  return g;
});

// 力导向模拟
function tick(){
  const k=0.018, rep=2600, center=0.012;
  for(let i=0;i<nodes.length;i++){const a=nodes[i];
    for(let j=i+1;j<nodes.length;j++){const b=nodes[j];
      let dx=a.x-b.x, dy=a.y-b.y, d2=dx*dx+dy*dy||0.01; let d=Math.sqrt(d2);
      let f=rep/d2; let fx=dx/d*f, fy=dy/d*f;
      a.vx+=fx;a.vy+=fy;b.vx-=fx;b.vy-=fy;}}
  links.forEach(l=>{const a=l.source,b=l.target;
    let dx=b.x-a.x, dy=b.y-a.y, d=Math.sqrt(dx*dx+dy*dy)||0.01;
    let target=l.kind==='belong'?90:(l.kind==='dep'?105:130); let f=(d-target)*k;
    let fx=dx/d*f, fy=dy/d*f;
    a.vx+=fx;a.vy+=fy;b.vx-=fx;b.vy-=fy;});
  nodes.forEach(n=>{
    n.vx+=(W/2-n.x)*center; n.vy+=(H/2-n.y)*center;
    if(n._fix){n.vx=0;n.vy=0;return;}
    n.vx*=0.82; n.vy*=0.82;
    n.x+=Math.max(-30,Math.min(30,n.vx)); n.y+=Math.max(-30,Math.min(30,n.vy));
  });
}
function render(){
  linkEls.forEach((e,i)=>{const l=links[i];
    let dx=l.target.x-l.source.x, dy=l.target.y-l.source.y, d=Math.sqrt(dx*dx+dy*dy)||1;
    let ux=dx/d, uy=dy/d; let rs=(l.source.r||5)+1, rt=(l.target.r||5)+3;
    e.setAttribute('x1',l.source.x+ux*rs);e.setAttribute('y1',l.source.y+uy*rs);
    e.setAttribute('x2',l.target.x-ux*rt);e.setAttribute('y2',l.target.y-uy*rt);});
  nodeEls.forEach(g=>{const n=g._node; g.setAttribute('transform',`translate(${n.x},${n.y})`);});
}
let alpha=420;
function loop(){ if(alpha>0){for(let s=0;s<2;s++)tick(); alpha--; } render(); requestAnimationFrame(loop);}
loop();

// 视图变换（平移/缩放）
let tx=0,ty=0,scale=1;
function applyT(){scene.setAttribute('transform',`translate(${tx},${ty}) scale(${scale})`);}
svg.addEventListener('wheel',e=>{e.preventDefault();
  const f=e.deltaY<0?1.12:0.89; const mx=e.offsetX, my=e.offsetY;
  tx=mx-(mx-tx)*f; ty=my-(my-ty)*f; scale*=f; applyT();},{passive:false});

// 拖动：节点 vs 背景
let drag=null, dragNode=null, moved=false;
svg.addEventListener('mousedown',e=>{
  const g=e.target.closest('.node');
  if(g){dragNode=g._node; dragNode._fix=true; moved=false;}
  else{drag={x:e.clientX-tx,y:e.clientY-ty}; svg.classList.add('dragging');}
});
window.addEventListener('mousemove',e=>{
  if(dragNode){const p=screenToScene(e); dragNode.x=p.x; dragNode.y=p.y; alpha=Math.max(alpha,60); moved=true;}
  else if(drag){tx=e.clientX-drag.x; ty=e.clientY-drag.y; applyT();}
});
window.addEventListener('mouseup',e=>{
  if(dragNode){ if(!moved){openNode(dragNode);} dragNode._fix=false; dragNode=null;}
  drag=null; svg.classList.remove('dragging');
});
function screenToScene(e){const r=svg.getBoundingClientRect();
  return {x:(e.clientX-r.left-tx)/scale, y:(e.clientY-r.top-ty)/scale};}

// 高亮邻居
const adj={}; nodes.forEach(n=>adj[n.id]=new Set([n.id]));
links.forEach(l=>{adj[l.source.id].add(l.target.id);adj[l.target.id].add(l.source.id);});
function focus(id){
  nodeEls.forEach(g=>{const n=g._node; const on=!id||adj[id].has(n.id);
    g.classList.toggle('dim',!on); g.classList.toggle('hl',!!id&&on);});
  linkEls.forEach((e,i)=>{const l=links[i]; const on=!id||(adj[id].has(l.source.id)&&adj[id].has(l.target.id)&&(l.source.id===id||l.target.id===id));
    e.classList.toggle('dim',!on);});
}

// 笔记面板
const panel=document.getElementById('panel'), pbody=document.getElementById('panelbody');
document.getElementById('close').onclick=()=>{panel.classList.remove('open');focus(null);};
function mdToHtml(md){
  if(!md) return '<p style="color:var(--muted)">（这个概念还没学透——用费曼引导器学一遍吧）</p>';
  const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  let out=[], inList=false;
  md.split('\n').forEach(line=>{
    let l=esc(line);
    l=l.replace(/\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]/g,(m,p1)=>`<a data-jump="${p1.trim()}">${p1.trim()}</a>`);
    l=l.replace(/\*\*([^*]+)\*\*/g,'<b>$1</b>');
    if(/^##\s+/.test(line)){out.push('<h2>'+l.replace(/^##\s+/,'')+'</h2>');}
    else if(/^#\s+/.test(line)){/*skip title*/}
    else if(/^>\s?/.test(line)){out.push('<blockquote>'+l.replace(/^&gt;\s?/,'')+'</blockquote>');}
    else if(/^\s*[-*]\s+/.test(line)){out.push('<div>• '+l.replace(/^\s*[-*]\s+/,'')+'</div>');}
    else if(line.trim()===''){out.push('');}
    else{out.push('<p>'+l+'</p>');}
  });
  return out.join('\n');
}
function openNode(n){
  if(n.type==='category'){ focus(n.id);
    const members=nodes.filter(x=>x.type==='concept'&&x.category===n.category)
      .map(x=>`<a data-jump="${x.label}">${x.label}</a>`).join(' · ');
    pbody.innerHTML=`<button id="close2" style="float:right;border:none;background:none;color:var(--muted);font-size:20px;cursor:pointer">×</button>
      <h1>${n.label}</h1><div class="badge">大类</div><div class="badge">${n.count} 个概念</div>
      <div class="md"><p>${members||'（暂无概念）'}</p></div>`;
  }else{
    focus(n.id);
    pbody.innerHTML=`<button id="close2" style="float:right;border:none;background:none;color:var(--muted);font-size:20px;cursor:pointer">×</button>
      <h1>${n.label}</h1>
      <div class="badge" style="border-color:${catColor[n.category]};color:${catColor[n.category]}">${n.category}</div>
      <div class="badge">${n.status||''}</div>
      ${(n.aliases&&n.aliases.length)?'<div class="badge">'+n.aliases.join(' / ')+'</div>':''}
      ${n.viz?'<div style="margin:8px 0 12px"><a href="'+((DATA.prefix||'')+n.viz)+'" target="_blank" style="display:inline-block;color:var(--accent);border:1px solid var(--accent);border-radius:8px;padding:5px 12px;text-decoration:none;font-weight:600">▶ 动态画面 / Dynamic View</a></div>':''}
      ${window.self!==window.top?'<div style="margin:0 0 12px"><a data-open="'+n.label+'" style="display:inline-block;cursor:pointer;color:var(--accent);border:1px solid var(--accent);border-radius:8px;padding:5px 12px;text-decoration:none;font-weight:600">📖 在知识站打开</a></div>':''}
      <div class="md">${mdToHtml(n.body)}</div>`;
  }
  panel.classList.add('open');
  pbody.querySelectorAll('[data-jump]').forEach(a=>a.onclick=()=>{const t=byId[a.dataset.jump]; if(t)openNode(t);});
  pbody.querySelectorAll('[data-open]').forEach(a=>a.onclick=()=>{try{parent.postMessage({goto:a.dataset.open},'*');}catch(e){}});
  const c2=document.getElementById('close2'); if(c2)c2.onclick=()=>{panel.classList.remove('open');focus(null);};
}

// 搜索
document.getElementById('search').addEventListener('input',e=>{
  const q=e.target.value.trim().toLowerCase(); if(!q){focus(null);return;}
  nodeEls.forEach(g=>{const n=g._node;
    const hit=n.label.toLowerCase().includes(q)||(n.aliases||[]).some(a=>a.toLowerCase().includes(q));
    g.classList.toggle('dim',!hit); g.classList.toggle('hl',hit);});
  linkEls.forEach(e2=>e2.classList.add('dim'));
});

// 图例 + 元信息
document.getElementById('legend').innerHTML=DATA.categories.map(c=>`<span><i style="background:${catColor[c]}"></i>${c}</span>`).join('')
  +'　|　'+Object.entries(STATUSRING).map(([k,v])=>`<span><i style="background:transparent;border:2px solid ${v}"></i>${k}</span>`).join('')
  +'　|　<span>⇢ 依赖</span><span>— 关联</span><span>· 大小=重要度</span>';
document.getElementById('meta').textContent=`${nodes.filter(n=>n.type==='concept').length} 概念 · ${DATA.categories.length} 大类 · 更新于 ${DATA.generated}`;
window.addEventListener('resize',()=>{W=svg.clientWidth;H=svg.clientHeight;alpha=Math.max(alpha,80);});
const THEMES=[["light","◐ 浅"],["dark","◑ 深"],["ink","❖ 宣纸"],["inkdark","❖ 夜墨"]];
function themeIdx(name){for(var i=0;i<THEMES.length;i++)if(THEMES[i][0]===name)return i;return 1;}
function applyPalette(){buildPalette();
  nodeEls.forEach(function(g){var n=g._node;
    if(n.type==='category')n._c.style.fill=catColor[n.category];
    else n._c.style.stroke=(STATUSRING[n.status]||'var(--ring)');});
  var li=document.querySelectorAll('#legend i'),k=0;
  DATA.categories.forEach(function(c){if(li[k])li[k].style.background=catColor[c];k++;});
  Object.keys(STATUSRING).forEach(function(s){if(li[k])li[k].style.borderColor=STATUSRING[s];k++;});}
function applyTheme(name){document.documentElement.dataset.theme=name;applyPalette();
  document.getElementById('themebtn').textContent=THEMES[themeIdx(name)][1];}
document.getElementById('themebtn').onclick=function(){
  var cur=document.documentElement.dataset.theme||'dark';
  applyTheme(THEMES[(themeIdx(cur)+1)%THEMES.length][0]);};
applyTheme(document.documentElement.dataset.theme||'dark');
function setGoalDone(on){nodeEls.forEach(function(g){var n=g._node;if(!n||n.type!=='concept')return;g.classList.remove('alive-full','alive-weak');var lv=on?(n.alivep||''):(n.alive||'');if(lv)g.classList.add('alive-'+lv);});}
(function(){var gd=new URLSearchParams(location.search).get('goaldone');if(gd==='1')setGoalDone(true);})();
window.addEventListener('message',function(e){if(e&&e.data&&('goalDone' in e.data))setGoalDone(!!e.data.goalDone);});
</script></body></html>"""


def write_graph_html(graph, out):
    html = HTML.replace('__DATA__', json.dumps(graph, ensure_ascii=False))
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)


def global_vault_path():
    """读用户主目录的全局指针 ~/.gewu/glb_vault_path.json 的 vault_path（跨 agent 共享、跨 OS）；
    用 expanduser 适配 Windows(C:\\Users\\X)/mac(/Users/X)/Linux(/home/X)。库不存在则返回 None。"""
    try:
        gp = os.path.join(os.path.expanduser('~'), '.gewu', 'glb_vault_path.json')
        if os.path.isfile(gp):
            vp = (json.load(open(gp, encoding='utf-8')) or {}).get('vault_path')
            if vp and os.path.isdir(vp):
                return vp
    except Exception:
        pass
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    # 知识库根目录 = 主题名文件夹本身（不再套一层「知识库/」）
    default_vault = os.environ.get('GEWU_VAULT') or global_vault_path() or os.getcwd()
    ap = argparse.ArgumentParser()
    ap.add_argument('--vault', default=default_vault)
    args = ap.parse_args()
    vault = args.vault
    if not os.path.isdir(vault):
        raise SystemExit('找不到知识库目录: ' + vault)
    sysdir = os.path.join(vault, '_system')
    os.makedirs(sysdir, exist_ok=True)
    notes = collect(vault)
    _potential, _baked = _goal_alive(notes, sysdir)
    cats = sorted({n['category'] for n in notes.values()})
    # 全局数据仍写入 _system/graph_data.json（供路线图/呼吸态等读取），
    # 但不再在根目录输出 知识图谱.html（累赘；各大类页用各自的分类图谱即可）。
    g = build_graph(notes); g['prefix'] = ''; _apply_alive(g, _potential, _baked)
    with open(os.path.join(sysdir, 'graph_data.json'), 'w', encoding='utf-8') as f:
        json.dump(g, f, ensure_ascii=False, indent=2)
    # 清理历史遗留的根目录全局图谱
    _legacy = os.path.join(vault, '知识图谱.html')
    if os.path.isfile(_legacy):
        try: os.remove(_legacy)
        except OSError: pass
    # 各大类单独图谱（放进各自文件夹，prefix=../ 以正确链接 _viz）
    gen_cats = []
    for c in cats:
        if c in ('fragment', '碎片'): continue  # 碎片暂存区：纯 .md 存储，不出图谱
        sub = {t: n for t, n in notes.items() if n['category'] == c}
        gc = build_graph(sub); gc['prefix'] = '../'; _apply_alive(gc, _potential, _baked)
        cdir = os.path.join(vault, c)
        if not os.path.isdir(cdir):
            continue
        # 边触发门：仅当该类存在概念间的边(prereq/双链)才出图谱；否则只留 .md，并清理旧图
        has_edge = any(l.get('kind') in ('dep', 'link') for l in gc['links'])
        gp = os.path.join(cdir, c + '-知识图谱.html')
        if has_edge:
            write_graph_html(gc, gp); gen_cats.append(c)
        elif os.path.isfile(gp):
            try: os.remove(gp)
            except OSError: pass
    concepts = [n for n in g['nodes'] if n['type'] == 'concept']
    print('OK 全局概念=%d 大类=%d；出图谱的大类=%d（仅含概念间边者；根目录不再输出全局图谱）' % (len(concepts), len(cats), len(gen_cats)))


if __name__ == '__main__':
    main()
