# Gewu · 格物

**Turn "asking AI when I have a question" into a learning map with a compass.**

> Study one thing thoroughly to attain true knowledge: if you can explain it clearly, you truly understand it.

<img src="./assets/merged_output_720p.gif" alt="格物演示" width="100%" style="display:block;margin-left:0;margin-right:auto;">

[![License](https://img.shields.io/github/license/YuhangZho/gewu-skill?style=flat-square&color=green)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/YuhangZho/gewu-skill?style=flat-square)](https://github.com/YuhangZho/gewu-skill/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/YuhangZho/gewu-skill?style=flat-square)](https://github.com/YuhangZho/gewu-skill/commits)
![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/deps-none%20%28stdlib%29-success?style=flat-square)
![Offline](https://img.shields.io/badge/offline-ready-success?style=flat-square)
![Agent Skills](https://img.shields.io/badge/Agent_Skills-Standard-3fb950?style=flat-square)
[![skills.sh](https://skills.sh/b/YuhangZho/gewu-skill)](https://skills.sh/YuhangZho/gewu-skill)
![Runtime](https://img.shields.io/badge/Runtime-Claude_·_ChatGPT_·_Codex_·_Cursor_·_Kimi-8957e5?style=flat-square)

[Who it's for](#who-its-for) · [What you'll get](#what-youll-get) · [How to start](#how-to-start) · [Installation](#installation) · [Directory structure](#directory-structure)

**Other Languages:** [简体中文](README.md) · [Español](README_ES.md)

---

## Who it's for

Gewu fits these learning scenarios:

- **Want to systematically enter a new field**, but don't know what to learn first or next.
- **Have a clear goal**, such as an exam, role transfer, onboarding to a project, or getting into a business line, and need to know what you're missing.
- **Fragmented "learning"** — turn the time spent waiting for AI replies into bite-sized learning of interesting things.
- **Understand it when you ask AI, but forget it a few days later**, never truly mastering it.

Gewu acts like a learning host: it helps you set a goal, designs a knowledge map and learning path around that goal, guides you step by step to explain concepts clearly, and finally settles your learning outcomes locally.

---

## What you'll get

### A learning route you can actually walk

Just say "I want to learn AI / C / Amazon operations / CET-4", and Gewu will first ask you why, then break down a route based on your goal. It's not an encyclopedia table of contents, but "what to learn now, why learn it first, what to learn next".

### A set of truly digested notes

Each concept isn't just the AI explanation saved — it's the result of what you learned:

- A one-sentence positioning
- Core takeaways
- Stuck points and corrections
- Boundaries, common pitfalls
- Flowcharts and reference views when needed

### A local knowledge station

What you've learned turns into openable local pages:

- **Learning roadmap**: see where you are now and what the next stop is.
- **Knowledge graph**: see how concepts connect.
- **Goal planning**: see how far your current knowledge is from the goal.
- **Concept documents**: every concept you've learned can be reviewed.

<img src="./assets/学习站示例.gif" alt="学习站示例" width="100%" style="display:block;margin-left:0;margin-right:auto;">

### Pick up where you left off, even mid-concept

Gewu records your learning state. If a concept isn't finished, next time you can continue from where you got stuck, without re-explaining the background.

### Fragmented knowledge won't get lost

If today you only want to figure out one small concept, you can still record it. Once similar content accumulates, Gewu will organize them into the corresponding field, growing into routes and graphs.

---

## How to start

Say one sentence to your AI:

```text
Learn AI with Gewu
```

You can also say:

```text
I'm new to C, help me plan a learning route.
```

```text
Help me understand the field of Amazon operations.
```

```text
Guide me to learn how to keep my wife happy and smoothly get more pocket money.
```

On first use, Gewu will ask where your knowledge base is stored. Pick a long-term location, for example:

```text
D:\gewu-vault
```

After that, the same knowledge base will keep accumulating — no need to set it up each time (path can be manually adjusted in ~/.gewu/glb_vault_path.json).

---

## How it learns

Gewu's core actions are simple:

1. **Ask the goal first**: learning it for an exam, interview, role transfer, project onboarding, or pure interest.
2. **Lay out the route**: arrange the learning order by prerequisite dependencies and importance.
3. **Learn concept by concept**: pose questions, explain, ask you to restate, probe the stuck points.
4. **Pass validation, then close**: only when you can rephrase it, know when it breaks, is it considered learned.
5. **Settle immediately**: update notes, roadmap, knowledge graph, and goal progress.

Core belief: **Output drives input. If you can explain it clearly, you truly understand it.**

---

## Installation

Gewu follows the open Agent Skills standard and can be used in agents that support skills.

### Environment check

```bash
python --version
```

- Shows `Python 3.x`: environment is ready, you can continue installing the skill.
- Command not found: install Python first. (PS: you can use it without Python, but the knowledge base can't be persisted.)
  - Windows: [python.org/downloads](https://www.python.org/downloads/), check `Add Python to PATH` during installation
  - macOS: `brew install python`
  - Linux: `sudo apt install python3`

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

| Agent | skills directory |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Claude Desktop / Cowork | Settings → Capabilities, add the `gewu` folder |
| Codex | `~/.codex/skills/` |
| Cursor | `~/.cursor/skills/` |
| Kimi Work | `~/AppData/Roaming/kimi-desktop/daimon-share/daimon/skills/` |
| Marvis | `~/AppData/Roaming/Tencent/Marvis/User/xx/skills/custom/` |
| Trae CN | `~/.trae-cn/skills/` |
| Qoder CN | `~/.qoder-cn/skills/` |
| OpenClaw | `~/.openclaw/skills/` |
| Other 50+ agents | Paths vary, see [vercel-labs/skills support table](https://github.com/vercel-labs/skills#supported-agents) |

</details>

---

## Customize appearance

The knowledge station defaults to light, and also supports dark, xuan-paper, and night-ink themes. Copy the template to your knowledge base:

```text
your-knowledge-base/_system/config.json
```

Template at:

```text
templates/config.example.json
```

After editing, regenerate the knowledge station to take effect.

---

## Directory structure

```text
gewu-skill/
  SKILL.md                      Skill main file
  templates/concept-template.md Concept note template
  scripts/render_viz.py         Generate concept structure diagrams
  scripts/build_graph.py        Generate knowledge graph
  scripts/plan_path.py          Generate knowledge station
  scripts/set_goal.py           Write goals and refresh pages
  assets/merged_output.mp4      Demo video
```

After running, your knowledge base looks roughly like this:

```text
gewu-vault/
  AI/
    Token.md
    Context.md
    AI-roadmap.html
    AI-knowledge-graph.html
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

## Suitable and not suitable

Suitable for:

- Systematically learning a field
- Settling AI conversations into reviewable knowledge
- Filling knowledge gaps around a goal
- Using the Feynman method to check whether you truly understand

Not suitable for:

- Replacing question banks, Anki, or mass drilling
- Replacing real project practice
- Asking about the weather, etc.

---

## Acknowledgements

The promotional animation draft was designed and produced using the [huashu-design](https://github.com/alchaincyf/huashu-design) skill package.

## Author

Yuhang, an embedded coder currently distilling 🧪 himself.

* The fragmented-knowledge fusion effect still needs further testing;

* Although Marvis, Trae, and Qoder are supported, real-world testing shows mediocre results — the models may suffer from attention drift (2026.6.26).

* Cursor (auto) / Codex (5.5) / Claude (opus 4.8) / Kimi (K2.6) generation results have been verified as passing.

<p align="left">
  <img src="./assets/wechat-search.png" alt="WeChat Search: Zhou Yuhang" width="620" style="display:block;margin-left:0;margin-right:auto;">
</p>

## License

**MIT** © 2026 Yuhang ([@YuhangZho](https://github.com/YuhangZho)). Free to use and modify, just keep the copyright and license notice.
