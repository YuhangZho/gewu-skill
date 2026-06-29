# 格物 · Gewu

**AI 回复了问题，你"看懂了"却讲不出来。**

> 把“有问题问 AI ”，变成"有目标问 AI"——它会引导你讲清楚，讲不清就是没真懂。
>
> > 格一物，致真知：能讲清楚，才算真懂。
>

[![License](https://img.shields.io/github/license/YuhangZho/gewu-skill?style=flat-square&color=green)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/YuhangZho/gewu-skill?style=flat-square)](https://github.com/YuhangZho/gewu-skill/stargazers)
![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/deps-none%20%28stdlib%29-success?style=flat-square)
![Offline](https://img.shields.io/badge/offline-ready-success?style=flat-square)
![Agent Skills](https://img.shields.io/badge/Agent_Skills-Standard-3fb950?style=flat-square)
[![skills.sh](https://skills.sh/b/YuhangZho/gewu-skill)](https://skills.sh/YuhangZho/gewu-skill)
![Runtime](https://img.shields.io/badge/Runtime-Claude_·_Codex_·_Cursor_·_Kimi·_OpenClaw·_WorkBuddy-8957e5?style=flat-square)

[适合谁](#适合谁) · [你会得到什么](#你会得到什么) · [怎么开始](#怎么开始) · [安装](#安装) · [目录结构](#目录结构)

**其他语言 / Other Languages:** [English](README_EN.md) · [Español](README_ES.md)

---

## **让格物带你——**

> - 🃏 成为斗地主高手：搞懂高手**为什么手里有炸却先不出**
> - 🧮 搞懂"鸡兔同笼"到底在算什么——再帮**孩子**真正搞懂(而不是背口诀)
> - 💼 转岗 AI 应用开发，从零铺一条**有先后的**学习地图
> - 📖 三周冲 CET-4，先弄清**到底要学哪些**
> - 💗 哄对象、谈加薪：套路背后**为什么管用**

```
你  ：Token 不就是把文字切成一块块嘛。
格物：那 "unhappiness" 会被切成几块？为什么不按字母、也不按整词？
你  ：呃……按词？不对，词太多了……我说不清。
格物：对，你卡的就是这儿——子词分词在权衡什么。我们从这补。
```

格物的短板：

> 格物不是秒回的问答机器人。它**慢**、有流程，因为在“逼”你真懂。

 **想要随手一个答案，它不适合；想要某件事真正学透，它就是为此而生。**


----

## 你只管学，沉淀全自动

你只管把概念学透，笔记、双链、知识图谱、目标进度——格物边学边自动生成，不用额外敲一个字、连一条线。

### 规划好的学习路线

你只要说“我想学 AI / 前端 / CET-4”，格物会按目标拆出递进路线。

### 自动生成本地知识站

- **学习路线图**：当前走到哪、下一站是什么。
- **知识图谱**：概念之间如何连接。
- **目标规划**：细分目标与当前进度。
- **概念文档**：学过概念可回看。
  - 一句话定位
  - 核心收获
  - 卡壳点和修正
  - 边界、易错点
  - 流程图和视野参考


<img src="./assets/学习站示例.gif" alt="学习站示例" width="100%" style="display:block;margin-left:0;margin-right:auto;">

---

## 安装

格物遵循开放的 Agent Skills 标准，可在支持 skills 的 agent 里使用。

### 环境检查

```bash
python3 --version
```

- 要求 `Python 3.8`或更高版本;
- python安装或升级参考：
  - Windows：[python.org/downloads](https://www.python.org/downloads/)，安装时勾选 `Add Python to PATH`
  - macOS（已安装 Homebrew）：`brew install python`
  - Ubuntu / Debian：`sudo apt install python3`

### 方式一：一键安装

对你正在用的 agent 说：

```text
帮我安装这个 skill：https://github.com/YuhangZho/gewu-skill
```

或命令行执行：

```bash
npx skills add YuhangZho/gewu-skill
```

### 方式二：手动安装

复制`gewu-skill` 文件夹到对应Agent路径

<details>
<summary>展开：常见 agent 的 skills 目录</summary>


| Agent                  | skills 目录                                                  |
| ---------------------- | ------------------------------------------------------------ |
| Claude Code            | `~/.claude/skills/`                                          |
| Claude 桌面端 / Cowork | 设置 → Capabilities，添加 `gewu` 文件夹 (<30MB && <200 files) |
| Codex                  | `~/.codex/skills/`                                           |
| Cursor                 | `~/.cursor/skills/`                                          |
| WorkBuddy              | `~/.workbuddy/skills/`                                       |
| Kimi Work              | `~/AppData/Roaming/kimi-desktop/daimon-share/daimon/skills/` |
| Marvis                 | `~/AppData/Roaming/Tencent/Marvis/User/xx/skills/custom/`    |
| Trae CN                | `~/.trae-cn/skills/`                                         |
| Qoder CN               | `~/.qoder-cn/skills/`                                        |
| OpenClaw               | `~/.openclaw/skills/`                                        |
| 其他 50+ agent         | 路径各异，见 [vercel-labs/skills 支持表](https://github.com/vercel-labs/skills#supported-agents) |

</details>

---

## 怎么开始

对你的 AI 说一句：

```text
用格物带我成为斗地主高手
```

也可以这样说：

```text
三周冲 CET-4，先帮我理清到底要学哪些
```

```text
我想转岗 AI 应用开发，从零规划一条学习路线
```

```text
帮我弄懂孩子的"鸡兔同笼"，好回去考考他
```

首次使用时，格物会先问你知识库存在哪里。选一个长期保存的位置即可，比如：

```text
D:\gewu-vault
```

之后同一个知识库会持续积累，不用每次重新设置( 可在 ~/.gewu/glb_vault_path.json 手动调整路径)。

---

## 格物机制

格物的核心动作：

1. **先问目标**：学它为了考试、面试、转岗、项目上手，还是纯兴趣。
2. **再铺路线**：按前置依赖和重要度安排学习顺序。
3. **逐个概念学**：设问、讲解、让你复述、追问卡壳点。
4. **通过验证再收尾**：能换说法讲清楚，知道什么时候会失效，才算学完。
5. **立刻沉淀**：更新笔记、路线图、知识图谱和目标进度。

核心信条：**输出倒逼输入。能讲清楚，才算真懂。**

---

## 目录结构

```text
gewu-skill/
  SKILL.md                        技能主文件
  templates/concept-template.md   概念笔记模板
  scripts/render_viz.py           生成概念结构图
  scripts/build_graph.py          生成知识图谱
  scripts/plan_path.py            生成知识站
  scripts/set_goal.py             写入目标并刷新页面
  assets/merged_output_720p.webp  演示视频
```

运行后，你的知识库大致长这样：

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
    临时学过的小概念.md
  _system/
    graph_data.json
    roadmap_data.json
    goals.json
    config.json
```

---

## 作者

宇航🧪蒸馏自己。

<p align="left">
  <img src="./assets/wechat-search.png" alt="微信搜一搜：周宇航" width="620" style="display:block;margin-left:0;margin-right:auto;">
</p>

## 许可

**MIT** © 2026 宇航 ([@YuhangZho](https://github.com/YuhangZho))。可自由使用、修改，保留版权与许可声明即可。
