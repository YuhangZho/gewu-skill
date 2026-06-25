# 格物 · Gewu

**a Feynman-method learning system · 费曼学习系统**

> *「格一物，致真知 —— 能讲清楚，才算真懂。」*

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

**格物 · Gewu——不再收藏打卡，学透知识「呼吸」起来。**

<br>

格物 · Gewu 费曼问答的方式，陪你真正学透。<br>

带上你的目标，学以致用。<br>

自动得到 知识图谱 + 学习路线 + 目标规划。

[它做什么](#它做什么--what-it-does) · [怎么用](#怎么用--quick-start) · [安装](#安装--install) · [许可](#许可--license)

<br>

**其他语言 / Other Languages:**

[English](README_EN.md) · [Español](README_ES.md)

<br>

---

## 格物做了什么 · What it does

**格物引导你把一个概念“描绘出来”——不是记录收藏，是让你真懂，把知识学「活」。**

- **领域层**：开始一个新领域时，先总览、建知识地图、问你**学习目标**、按"依赖优先 + 重要度"规划学习路线。
- **概念层（费曼五步）**：立靶 → 启动·点火(设问→联网取权威源→初稿) → 视觉建模(AI 判型 + 知识图解) → 讲给外行 → 卡壳回溯 → 三重验证(含边界补丁) → 落盘。
- **落盘产物**：每个学透的概念 = 一篇 Markdown 笔记 + 一张知识图解(Mermaid/SVG，固定 Unicode 图标) + 进入知识图谱/路线图/文档站。
- **目标闭环**：设定具体目标（如「应聘 AI 应用开发工程师」「CET-4」），AI Agent对照真实要求算出匹配度与缺口、规划下一步；每完成一个概念，节点点亮并进入「呼吸」态。

核心信条：**输出倒逼输入 —— 能讲清楚才算懂**。

---

## 使用 · Quick start

对你的 AI 助手说：

- 「用格物学 **AI**」
- 「用费曼法学 **Token**」 / "Teach me **X** with the Feynman method"
- 「我开始学 **C 语言**，帮我规划学习路线」
- 「接下来该学什么 / 我走到哪了」
- 「我的目标是 **应聘 AI 工程师**，分析我和目标的差距」

助手会按 `SKILL.md` 的五步主持你学习，每学透一个概念就刷新知识站。手动刷新：

```bash
python scripts/build_graph.py            # 刷新知识图谱
python scripts/plan_path.py --goal 面试  # 刷新知识站(--goal 可选)
python scripts/audit_learning_order.py   # 审计笔记是否显式提到路线后置概念
```

用浏览器打开 `知识库/<大类>/<大类>-路线图.html` 即可浏览(默认浅色；右上角可在 **浅 / 深 / 宣纸 / 夜墨** 四套主题间循环切换，后两套为中国水墨风)。

---

## 安装 · Install

格物遵循开放的 Agent Skills 标准，可在任意 skills 兼容的 agent 里运行。

### 环境检查 · Requirements

```bash
python --version
```

- 显示 `Python 3.x` → 跳到下面「安装」。
- 提示找不到命令 → 装一下：
  - **Windows** → [python.org/downloads](https://www.python.org/downloads/)，安装时勾选 *Add Python to PATH*
  - **macOS** → `brew install python` 
  - **Linux** → `sudo apt install python3`

### 方式一：一键安装（推荐，跨 agent）

对你正在用的 agent 直接说：

```
帮我安装这个 skill：https://github.com/YuhangZho/gewu-skill
```

或命令行执行

```bash
npx skills add YuhangZho/gewu-skill
```



### 方式二：手动安装（clone 到对应目录）

<details><summary>展开：各 agent 的 skills 目录</summary>

| Agent | skills 目录（global） |
|---|---|
| Claude Code | `~/.claude/skills/gewu/` |
| Claude 桌面端 / Cowork | **设置 → Capabilities** 添加 `gewu-skill` 文件夹，或保存随附的 `gewu-skill.skill` |
| Codex | `~/.codex/skills/gewu/` |
| Cursor | `~/.cursor/skills/gewu/` |
| OpenClaw | `~/.openclaw/skills/gewu/` |
| Qoder | `~/.qoder-cn/skills/gewu/`  // 对应Qoder CN |
| Trae | `~/.trae-cn/skills/gewu/`    //对应 Trae CN |
| Kimi Work | `~/AppData/Roaming/kimi-desktop/daimon-share/daimon/skills`  // 复制后需要重启 |
| 其他 50+ agent | 路径各异，见 [vercel-labs/skills 支持表](https://github.com/vercel-labs/skills#supported-agents) |

</details>

---

## 自定义 · Customize

### 外观/行为开关 → `config.json`

只想换主题色或默认明暗、又不想动代码？把模板复制到 `知识库/_system/config.json`，**`enabled` 改成 `true`** 再改参数（关着时一切走内置默认）：

```jsonc
// 知识库/_system/config.json   （模板：templates/config.example.json）
{
  "enabled": true,                  // ← 总开关，默认 false
  "theme_default": "dark",          // light(浅) / dark(深) / ink(宣纸) / inkdark(夜墨)
  "accent": { "light": "#34c759", "dark": "#30d158" }  // 强调色：按钮/链接/当前卡片
}
```

重跑 `python scripts/plan_path.py` —— 知识站默认就变深色、强调色变绿。

`enabled: false`（默认）则忽略以上、用内置浅色 + 蓝。

## 目录结构 · Structure

```
gewu-skill/
  SKILL.md                      技能主文件(流程 + 触发词 + 视觉规范)
  README.md                     本文件
  templates/concept-template.md 概念笔记模板
  scripts/render_viz.py         model.json → Mermaid/SVG 知识图解
  scripts/build_graph.py        扫描笔记 → 知识图谱 HTML(力导向、依赖箭头、完成节点呼吸)
  scripts/plan_path.py          → 知识站单页(路线图/概念文档/目标规划/嵌入图谱)
  assets/merged_output.mp4      宣传动画
```

运行后在你的学习目录生成(示例)：

```
知识库/
  知识图谱.html               全局总览
  AI/                         一个大类
    概念.md                   每个概念一篇笔记
    _viz/概念.model.json      AI 填写的结构化视觉模型
    _viz/概念.mmd             脚本生成的 Mermaid 源
    _viz/概念.svg             可选生成的知识图解
    AI-知识图谱.html          该类图谱
    AI-路线图.html            知识站单页(起始页；含路线图/图谱/目标规划/概念文档)
  _system/                    机器数据(graph_data/roadmap_data/domains/goals.json)
```



## 致谢 · Credits
宣传动画初稿采用 [huashu-design](https://github.com/alchaincyf/huashu-design) 的技能包设计制作。

## 许可 · License
**MIT** © 2026 宇航 ([@YuhangZho](https://github.com/YuhangZho)) — 见 [`LICENSE`](./LICENSE)。可自由使用、修改、分发、商用，保留版权与许可声明即可。
