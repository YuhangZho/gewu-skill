# 格物 · Gewu

**a Feynman-method learning system · 费曼学习系统**

> *「格一物，致真知 —— 能讲清楚，才算真懂。」*
> *"Investigate one thing to its core — you don't understand it until you can explain it."*

<!-- 徽章里的 YuhangZho/gewu-skill 请替换为你的实际仓库路径 -->
[![License](https://img.shields.io/github/license/YuhangZho/gewu-skill?style=flat-square&color=green)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/YuhangZho/gewu-skill?style=flat-square)](https://github.com/YuhangZho/gewu-skill/stargazers)
[![Forks](https://img.shields.io/github/forks/YuhangZho/gewu-skill?style=flat-square)](https://github.com/YuhangZho/gewu-skill/network/members)
[![Issues](https://img.shields.io/github/issues/YuhangZho/gewu-skill?style=flat-square)](https://github.com/YuhangZho/gewu-skill/issues)
[![Last commit](https://img.shields.io/github/last-commit/YuhangZho/gewu-skill?style=flat-square)](https://github.com/YuhangZho/gewu-skill/commits)
![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/deps-none%20(stdlib)-success?style=flat-square)
![Offline](https://img.shields.io/badge/offline-ready-success?style=flat-square)

**格物（Gewu）是一套目标驱动的费曼学习系统**：一步步把你输入的概念真正学透，自动落盘成带双链/分类/出处的 Markdown 笔记，并长出一个会「呼吸」的知识站（学习路线图 + 知识图谱 + 概念文档 + 目标规划）。纯本地、离线、无外部依赖。

A goal-driven **Feynman-method learning system** for AI agents. It coaches you through truly understanding a concept, saves the result as linked Markdown notes, and grows an interactive offline "knowledge site" (roadmap + graph + concept docs + goal planner).

[看效果](#-效果--demo) · [它做什么](#它做什么--what-it-does) · [怎么用](#怎么用--quick-start) · [安装](#安装--install) · [许可](#许可--license)

---

## 🎬 效果 · Demo

[![格物 · Gewu — 输入概念 → 费曼七步 → 落盘笔记 → 图谱呼吸 → 品牌显形](./assets/hero.svg)](./assets/hero.svg)

▲ 16 秒循环动画 · `输入一个概念 → 费曼七步 → 学透落盘 → 目标达成时知识在图谱里「呼吸」`
👉 [打开动画 SVG（可单独查看 / 离线）](./assets/hero.svg) — 本宣传动画用 [huashu-design](https://github.com/alchaincyf/huashu-design) 的「HTML 原生 hero 叙事」设计理念制作。

> GitHub 会内联渲染这支动画 SVG；若你的浏览器未播放，点开上方链接即可。

---

## 它做什么 · What it does

两个层级：

- **领域层**：开始一个新领域时，先总览、建知识地图、问你的**具体学习目标**、按"依赖优先 + 重要度"规划学习路线。
- **概念层（费曼七步）**：`立靶 → 启动·点火(设问→联网取权威源→丑陋初稿) → 视觉建模(草稿图) → 讲给外行 → 卡壳回溯 → 简化迭代 → 三重验证 → 落盘`。
- **落盘产物**：每个学透的概念 = 一篇 Markdown 笔记 + 一张成稿动态画面(HTML) + 进入知识图谱/路线图/文档站。
- **目标闭环**：设定具体目标（如「应聘 AI 应用开发工程师」「CET-4」），AI 联网对照真实要求算出匹配度与缺口、规划下一步；目标完成后图谱里对应知识「活」起来（缓慢呼吸）。

核心信条：**输出倒逼输入 —— 能讲清楚才算懂**；最关键、最易省略的是"把概念还原成时空关系结构 / 动态图像"的内部建模。

---

## 目录结构 · Structure

```
gewu-skill/
  SKILL.md                      技能主文件(流程 + 触发词 + 视觉规范)
  README.md                     本文件
  templates/concept-template.md 概念笔记模板
  scripts/build_graph.py        扫描笔记 → 知识图谱 HTML(力导向、依赖箭头、目标呼吸)
  scripts/plan_path.py          → 知识站单页(路线图/概念文档/目标规划/嵌入图谱)
  assets/hero.svg               宣传动画
```

运行后在你的学习目录生成(示例)：

```
知识库/
  知识图谱.html               全局总览
  AI/                         一个大类
    概念.md                   每个概念一篇笔记
    _viz/概念.html            成稿动态画面
    AI-知识图谱.html          该类图谱
    AI-路线图.html            知识站单页(起始页；含路线图/图谱/目标规划/概念文档)
  _system/                    机器数据(graph_data/roadmap_data/domains/goals.json)
```

---

## 怎么用 · Quick start

对你的 AI 助手说(任一即可触发)：

- 「用费曼法学 **Token**」 / "Teach me **X** with the Feynman method"
- 「我开始学 **C 语言**，帮我规划学习路线」
- 「接下来该学什么 / 我走到哪了」
- 「我的目标是 **应聘 AI 工程师**，分析我和目标的差距」

助手会按 `SKILL.md` 的七步主持你学习，每学透一个概念就刷新知识站。手动刷新：

```bash
python scripts/build_graph.py            # 刷新知识图谱
python scripts/plan_path.py --goal 面试  # 刷新知识站(--goal 可选)
```

用浏览器打开 `知识库/<大类>/<大类>-路线图.html` 即可浏览(默认浅色，右上角可切深色)。

---

## 安装 · Install

### Claude Code / Cowork
- **设置 Settings → Capabilities** 添加本 `gewu-skill` 文件夹；或保存随附的 `gewu-skill.skill`(一键安装包)。
- 装好后用上面的关键词即可自动触发。

### 其他智能体(ChatGPT / Codex / Kimi / Marvis / 通用 Agent)
本技能**平台无关**——核心是 `SKILL.md`(纯指令) + 两个纯 Python 脚本(仅标准库、离线)。

1. 把 `SKILL.md` 的内容贴进该平台的**系统提示 / 自定义指令 / 项目说明 / GPT Instructions**。
2. 确保该智能体能：① 读写本地文件；② 运行 Python 3；(可选)③ 联网搜索(点火取权威源与目标分析)。
3. 把 `templates/` 和 `scripts/` 放到智能体可访问的工作目录。
4. 像上面那样对它说「用费曼法学 X」。

> `.skill` 文件本质是一个 zip。非 Claude 平台可把它**改名为 `.zip` 解压**，取出 `SKILL.md` / `scripts/` / `templates/` 使用。

---

## 依赖 · Requirements
- **Python 3**(脚本仅用标准库，离线可跑；无需 pip)。
- **现代浏览器**(看生成的 HTML；离线、单文件)。
- 可选：**联网**(点火取出处、目标联网对照)；**Node.js**(仅开发时 `node --check` 校验内嵌 JS)。

## 自定义 · Customize
- 笔记 frontmatter：`importance`(重要度 1-5)、`prereqs`(前置依赖)、`groups`(知识站左侧目录分类，可多个)、`goal_tags`、`sources`、`viz`。
- `_system/domains.json`：各领域学完后的扩展方向。
- `_system/goals.json`：每个大类的目标(目标文本/分类/匹配度/缺口/推荐/状态)，由 AI 联网分析后写入。

## 致谢 · Credits
- 宣传 hero 动画(`assets/hero.svg`)采用 [huashu-design](https://github.com/alchaincyf/huashu-design) 的「HTML 原生 hero 叙事 + 反 AI-slop」设计理念制作。
- README 版式参考 [nuwa-skill](https://github.com/alchaincyf/nuwa-skill)(格言 → 徽章 → 价值主张 → 效果 → 安装)。

## 许可 · License
**MIT** © 2026 宇航 ([@YuhangZho](https://github.com/YuhangZho)) — 见 [`LICENSE`](./LICENSE)。可自由使用、修改、分发、商用，保留版权与许可声明即可。
注：费曼学习法本身是公共方法论、不受版权约束；本许可仅覆盖本仓库的具体实现(SKILL.md 文本与脚本)。

## 说明 · Notes
- 「格物」出自《大学》「格物致知」——穷究一物以求真知，正是费曼法的内核。
- 脚本对大文件尾部的健壮性：如需手改 `scripts/*.py`，改完用 `python -c "import ast;ast.parse(open(f).read())"` 校验。
