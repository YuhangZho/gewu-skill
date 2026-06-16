# 格物 · Gewu

**a Feynman-method learning system · 费曼学习系统**

> *"Investigate one thing to reach true knowledge — if you can explain it clearly, you truly understand it."*

<video src="./assets/merged_output.mp4" controls=""></video>



[![License](https://img.shields.io/github/license/YuhangZho/gewu-skill?style=flat-square&color=green)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/YuhangZho/gewu-skill?style=flat-square)](https://github.com/YuhangZho/gewu-skill/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/YuhangZho/gewu-skill?style=flat-square)](https://github.com/YuhangZho/gewu-skill/commits)
![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/deps-none%20%28stdlib%29-success?style=flat-square)
![Offline](https://img.shields.io/badge/offline-ready-success?style=flat-square)
![Agent Skills](https://img.shields.io/badge/Agent_Skills-Standard-3fb950?style=flat-square)
[![skills.sh](https://skills.sh/b/YuhangZho/gewu-skill)](https://skills.sh/YuhangZho/gewu-skill)
![Runtime](https://img.shields.io/badge/Runtime-Claude_·_ChatGPT_·_Codex_·_Cursor_·_Kimi-8957e5?style=flat-square)

<br>

**格物 · Gewu — stop bookmarking and streak-chasing; learn things deeply until your knowledge starts to «breathe».**

<br>

Gewu learns *with* you through Feynman-style Q&A, until you truly get it.<br>

Bring your goal, and learn for real use.<br>

Automatically get a knowledge graph + learning path + goal planning.

[What it does](#what-it-does) · [Quick start](#quick-start) · [Install](#install) · [License](#license)

<br>

**Other languages / 其他语言:**

[中文](README.md) · [English](README_EN.md) · [Español](README_ES.md)

<br>

---

## What it does

**Gewu guides you to "say a concept out loud" — not to take notes that gather dust, but to truly understand it, and to grow everything you've learned into a "breathing" knowledge site.**

- **Domain layer**: when you start a new domain, it first gives an overview, builds a knowledge map, asks for your **specific learning goal**, and plans a learning path by "dependencies first + importance".
- **Concept layer (Feynman 7 steps)**: `set the target → ignite (ask → pull authoritative sources online → first draft) → visual modeling (sketch) → explain to a layperson → backtrack where you get stuck → simplify & iterate → triple verification → save`.
- **What gets saved**: each concept you master = a Markdown note + an animated final picture (HTML) + entry into the knowledge graph / roadmap / doc site.
- **Goal loop**: set a concrete goal (e.g. "apply for an AI application engineer role", "CET-4"), and the AI agent computes your match and gaps against real requirements and plans the next step; once a goal is met, the matching knowledge starts to "breathe".

Core belief: **output forces input — you only understand it if you can explain it clearly.**

---

## Quick start

Say to your AI assistant (any of these triggers it):

- "Learn **AI** with Gewu"
- "Teach me **Token** with the Feynman method"
- "I'm starting **C language** — plan a learning path for me"
- "What should I learn next / where am I?"
- "My goal is to **get hired as an AI engineer** — analyze the gap between me and that goal"

The assistant hosts your learning through the 7 steps in `SKILL.md`, refreshing the knowledge site every time you master a concept. To refresh manually:

```bash
python scripts/build_graph.py                  # refresh the knowledge graph
python scripts/plan_path.py --goal interview   # refresh the knowledge site (--goal optional)
```

Open `知识库/<category>/<category>-路线图.html` in your browser to explore (light by default; toggle dark at top right).

---

## Install

Gewu follows the open Agent Skills standard (a single `SKILL.md` at the root) and runs in any skills-compatible agent.

### Requirements

```bash
python --version
```

- Shows `Python 3.x` → jump to "Install" below.
- Command not found → install it:
  - **Windows** → [python.org/downloads](https://www.python.org/downloads/), check *Add Python to PATH* during setup
  - **macOS** → `brew install python` or via python.org
  - **Linux** → `sudo apt install python3`

### Option 1: one-click (recommended, cross-agent)

Just tell the agent you're using:

```
Install this skill for me: https://github.com/YuhangZho/gewu-skill
```

Or run from the command line:

```bash
npx skills add YuhangZho/gewu-skill
```

### Option 2: manual install (clone into the right directory)

<details><summary>Expand: skills directory per agent</summary>

| Agent | skills directory (global) |
|---|---|
| Claude Code | `~/.claude/skills/gewu/` |
| Claude desktop / Cowork | **Settings → Capabilities**, add the `gewu-skill` folder, or save the bundled `gewu-skill.skill` |
| Codex | `~/.codex/skills/gewu/` |
| Cursor | `~/.cursor/skills/gewu/` |
| OpenClaw | `~/.openclaw/skills/gewu/` |
| Qoder | `~/.qoder/skills/gewu/` |
| Kimi Code CLI | `~/.config/agents/skills/gewu/` |
| 50+ other agents | paths vary, see the [vercel-labs/skills support table](https://github.com/vercel-labs/skills#supported-agents) |


</details>

---

## Customize

### Appearance/behavior switch → `config.json`

Just want to change the accent color or default light/dark, without touching code? Copy the template to `知识库/_system/config.json`, **set `enabled` to `true`**, then change the parameters (everything falls back to built-in defaults while it's off):

```jsonc
// 知识库/_system/config.json   (template: templates/config.example.json)
{
  "enabled": true,                  // ← master switch, default false
  "theme_default": "dark",          // knowledge-site default theme: light / dark
  "accent": { "light": "#34c759", "dark": "#30d158" }  // accent: buttons / links / active card
}
```

Re-run `python scripts/plan_path.py` — the knowledge site now defaults to dark with a green accent.

`enabled: false` (default) ignores the above and uses the built-in light + blue.

---

## Structure

```
gewu-skill/
  SKILL.md                      main skill file (flow + triggers + visual spec)
  README.md                     this file
  templates/concept-template.md concept note template
  scripts/build_graph.py        scan notes → knowledge graph HTML (force-directed, dependency arrows, goal breathing)
  scripts/plan_path.py          → knowledge-site single page (roadmap / concept docs / goal planning / embedded graph)
  assets/hero.svg               promo animation
```

Generated in your learning directory after a run (example):

```
知识库/
  知识图谱.html               global overview
  AI/                         one category
    概念.md                   one note per concept
    _viz/概念.html            animated final picture
    AI-知识图谱.html          this category's graph
    AI-路线图.html            knowledge-site single page (entry; roadmap / graph / goal planning / concept docs)
  _system/                    machine data (graph_data / roadmap_data / domains / goals.json)
```



## Credits
The promo animation draft was made with the [huashu-design](https://github.com/alchaincyf/huashu-design) skill.

## License
**MIT** © 2026 宇航 ([@YuhangZho](https://github.com/YuhangZho)) — see [`LICENSE`](./LICENSE). Free to use, modify, distribute, and use commercially, as long as the copyright and license notice are retained.
