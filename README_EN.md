# Gewu · 格物

**AI answered your question — you "got it," but you can't explain it.**

> Turn "ask AI when I have a question" into "ask AI with a goal" — it guides you to explain clearly; if you can't explain it, you don't truly understand.
>
> > Study one thing thoroughly to attain true knowledge: if you can explain it clearly, you truly understand it.
>

[![License](https://img.shields.io/github/license/YuhangZho/gewu-skill?style=flat-square&color=green)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/YuhangZho/gewu-skill?style=flat-square)](https://github.com/YuhangZho/gewu-skill/stargazers)
![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/deps-none%20%28stdlib%29-success?style=flat-square)
![Offline](https://img.shields.io/badge/offline-ready-success?style=flat-square)
![Agent Skills](https://img.shields.io/badge/Agent_Skills-Standard-3fb950?style=flat-square)
[![skills.sh](https://skills.sh/b/YuhangZho/gewu-skill)](https://skills.sh/YuhangZho/gewu-skill)
![Runtime](https://img.shields.io/badge/Runtime-Claude_·_Codex_·_Cursor_·_Kimi·_OpenClaw·_WorkBuddy-8957e5?style=flat-square)

[Who it's for](#let-gewu-take-you) · [What you'll get](#you-focus-on-learning-we-handle-the-rest) · [How to start](#how-to-start) · [Installation](#installation) · [Directory structure](#directory-structure)

**Other Languages:** [简体中文](README.md) · [Español](README_ES.md)

---

## **Let Gewu take you —**

> - 🃏 Become a Doudizhu (Fight the Landlord) pro: understand **why experts hold bombs but don't play them first**
> - 🧮 Grasp what "chickens and rabbits in a cage" is really calculating — then help **your child** truly understand (not just memorize a formula)
> - 💼 Switch to AI application development — lay out a **prioritized** learning map from scratch
> - 📖 Three weeks to CET-4 — first figure out **what you actually need to learn**
> - 💗 Win over your partner, negotiate a raise: understand **why the playbook works**

```
You  : A token is just splitting text into chunks, right?
Gewu : How many chunks would "unhappiness" be split into? Why not by letter, or by whole word?
You  : Uh… by word? No, there are too many words… I can't explain it.
Gewu : Right — that's where you're stuck. What is subword tokenization balancing? Let's fill that gap.
```

Gewu's trade-off:

> Gewu is not a quick Q&A bot. It's **slow** and process-driven — because it's pushing you to truly understand.

**If you want a quick answer on demand, it's not for you; if you want to truly master something, that's what it's built for.**

----

## You focus on learning — we handle the rest

You just need to master each concept. Notes, bidirectional links, knowledge graphs, goal progress — Gewu generates them as you learn, without you typing an extra word or drawing a single line.

### A planned learning route

Just say "I want to learn AI / frontend / CET-4," and Gewu breaks down a progressive route around your goal.

### Auto-generated local knowledge station

- **Learning roadmap**: where you are now and what the next stop is.
- **Knowledge graph**: how concepts connect.
- **Goal planning**: sub-goals and current progress.
- **Concept documents**: review every concept you've learned.
  - One-sentence positioning
  - Core takeaways
  - Stuck points and corrections
  - Boundaries, common pitfalls
  - Flowcharts and reference views


<img src="./assets/学习站示例.gif" alt="Knowledge station example" width="100%" style="display:block;margin-left:0;margin-right:auto;">

---

## Installation

Gewu follows the open Agent Skills standard and can be used in agents that support skills.

### Environment check

```bash
python3 --version
```

- Requires `Python 3.8` or higher;
- Python install or upgrade:
  - Windows: [python.org/downloads](https://www.python.org/downloads/), check `Add Python to PATH` during installation
  - macOS (with Homebrew installed): `brew install python`
  - Ubuntu / Debian: `sudo apt install python3`

### Option 1: One-click install

Say to the agent you're using:

```text
Help me install this skill: https://github.com/YuhangZho/gewu-skill
```

Or run via command line:

```bash
npx skills add YuhangZho/gewu-skill
```

### Option 2: Manual install

Copy the `gewu-skill` folder to the corresponding agent path.

<details>
<summary>Expand: skills directories for common agents</summary>


| Agent                  | skills directory                                                  |
| ---------------------- | ------------------------------------------------------------ |
| Claude Code            | `~/.claude/skills/`                                          |
| Claude Desktop / Cowork | Settings → Capabilities, add the `gewu` folder                      |
| Codex                  | `~/.codex/skills/`                                           |
| Cursor                 | `~/.cursor/skills/`                                          |
| WorkBuddy              | `~/.workbuddy/skills/`                                       |
| Kimi Work              | `~/AppData/Roaming/kimi-desktop/daimon-share/daimon/skills/` |
| Marvis                 | `~/AppData/Roaming/Tencent/Marvis/User/xx/skills/custom/`    |
| Trae CN                | `~/.trae-cn/skills/`                                         |
| Qoder CN               | `~/.qoder-cn/skills/`                                        |
| OpenClaw               | `~/.openclaw/skills/`                                        |
| Other 50+ agents       | Paths vary, see [vercel-labs/skills support table](https://github.com/vercel-labs/skills#supported-agents) |

</details>

---

## How to start

Say one sentence to your AI:

```text
Use Gewu to help me become a Doudizhu pro
```

You can also say:

```text
Three weeks to CET-4 — first help me figure out what I actually need to learn
```

```text
I want to switch to AI application development — plan a learning route from scratch
```

```text
Help me understand my child's "chickens and rabbits in a cage" problem so I can quiz them
```

On first use, Gewu will ask where your knowledge base is stored. Pick a long-term location, for example:

```text
D:\gewu-vault
```

After that, the same knowledge base will keep accumulating — no need to set it up each time (path can be manually adjusted in ~/.gewu/glb_vault_path.json).

---

## How Gewu works

Gewu's core actions:

1. **Ask the goal first**: learning it for an exam, interview, role transfer, project onboarding, or pure interest.
2. **Lay out the route**: arrange the learning order by prerequisite dependencies and importance.
3. **Learn concept by concept**: pose questions, explain, ask you to restate, probe the stuck points.
4. **Pass validation, then close**: only when you can rephrase it and know when it breaks is it considered learned.
5. **Settle immediately**: update notes, roadmap, knowledge graph, and goal progress.

Core belief: **Output drives input. If you can explain it clearly, you truly understand it.**

---

## Directory structure

```text
gewu-skill/
  SKILL.md                        Skill main file
  templates/concept-template.md   Concept note template
  scripts/render_viz.py           Generate concept structure diagrams
  scripts/build_graph.py          Generate knowledge graph
  scripts/plan_path.py            Generate knowledge station
  scripts/set_goal.py             Write goals and refresh pages
  assets/merged_output_720p.webp  Demo video
```

After running, your knowledge base looks roughly like this:

```text
gewu-vault/
  AI/
    Token.md
    Context.md
    AI-路线图.html
    AI-知识图谱.html
    _viz/
      Token.model.json
      Token.mmd
      Token.svg
    _transcript/
      Token.jsonl
  fragment/
    small-concepts-learned-on-the-fly.md
  _system/
    graph_data.json
    roadmap_data.json
    goals.json
    config.json
```

---

## Author

Yuhang 🧪 distilling himself.

<p align="left">
  <img src="./assets/wechat-search.png" alt="WeChat Search: Zhou Yuhang" width="620" style="display:block;margin-left:0;margin-right:auto;">
</p>

## License

**MIT** © 2026 Yuhang ([@YuhangZho](https://github.com/YuhangZho)). Free to use and modify, just keep the copyright and license notice.
