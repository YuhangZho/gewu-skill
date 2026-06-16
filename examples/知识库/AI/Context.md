---
title: Context
category: AI
groups: ["模型基础"]
status: 已学透
importance: 5
prereqs: [Token]
goal_tags: []
aliases: ["上下文", "上下文窗口", "context window"]
tags: [AI]
created: 2026-06-15
related: [Token, Agent, Harness]
sources: ["https://platform.claude.com/docs/en/build-with-claude/context-windows", "https://arxiv.org/abs/2307.03172"]
viz: "AI/_viz/Context.html"
---

# Context

## 一句话定位
> 它属于 AI 大模型，是模型生成回答时**能参考的全部文本**（含它要生成的回答），即模型的**"工作记忆"**——容量固定，按 [[Token]] 计。

## 动态图像（视觉建模）
一个固定容量的窗口，自上而下喂给模型：System prompt(含 memory) / Skill（只放一次，在最前）→ 历史对话 → 本轮输入 →（模型生成的回答，也占容量，输入+输出共享）。
**递归累积**：每过一轮，`下一轮历史 = 旧历史 + {本轮输入 + 本轮回答}`，窗口线性填高。装满 → 压缩(compaction) 或 丢最早(FIFO)。
> 动态画面见 [[#动态画面]]（可交互：逐轮播放 + token 计数 + 注意力热区）。

## 类比
像 AI 的**便利贴**：它本身不记得你，你每次得把所有相关的话写在便利贴上递给它，它只看便利贴回答；便利贴大小固定，写满了就得擦掉最早的。
（心法版：context 是模型对外呈现的那层"界面/假我"，是它与世界沟通的介质。）

## 大白话讲解（讲给外行）
模型**本身无状态、没有记忆**。你聊十句它"记得"前九句，是因为应用**每一轮都把全部历史重新塞进 context 当输入**。
所谓"长期记忆 / Memory"是**应用层**的把戏——存在 context 之外，需要时再挑相关的喂回，不是模型自己记住。
为什么有限：① 硬上限——自注意力要算每对 token 的关系，计算量随长度约**平方增长**；② 软衰减——就算没满，token 越多准确率/召回越降（context rot）。

## 三个应用例子
1. 不相干的新问题 → 开新窗口，避免旧内容污染、稀释重点。
2. 检索代码 → 先用 codegraph 这类**预索引知识图谱**，按需查精准事实，而不是把整个代码库读进窗口。
3. 需要外部资料 → 用 MCP/外部索引让数据**按需、精准**进 context（注意：省的是"只取相关那一小段"，不是 MCP 本身）。

## 失效边界
- **最易混**：Context（这次对话的工作记忆，可装全新内容）≠ 训练知识（固化在**模型参数/权重**里，长期已学、有知识截止期、改不动）。
- 把什么都塞进一个窗口 → context rot，答不准。
- 关键信息别埋在中间（lost in the middle，放开头/结尾最稳）。
- 超出上限 → 报错(model_context_window_exceeded) 或 FIFO 丢最早；不触发压缩/截断时，容量内历史**逐字完整保留**（例外：扩展思考的旧 thinking 块会被自动剥掉）。

## 卡壳点复盘
- 误以为模型"自己记得"对话 → 其实无状态，靠应用每轮重发全部历史。
- 漏了"输出也占容量" → 输入+输出共享同一窗口。
- 把"省 context"归功于 MCP 本身 → 真正省的是"按需取精准外部数据"。

## 成长对比
- 起点认知：context 就是喂给 AI 的一段话，拆开是一堆 token。
- 现在的理解：context = 模型的固定容量工作记忆；模型无记忆、靠应用每轮重拼历史(递归累积)；有硬/软两重限制；区别于训练知识；满了压缩或丢弃；关键信息别埋中间。

## 动态画面
- 打开成稿动效：[_viz/Context.html](_viz/Context.html)（逐轮播放递归累积、token 计数、注意力热区、压缩/丢弃切换、深浅配色）

## 出处 / Sources
- 〔Anthropic 官方文档，一手，抓取 2026-06-15〕<https://platform.claude.com/docs/en/build-with-claude/context-windows>
  - 原话引述：「The "context window" refers to all the text a language model can reference when generating a response, including the response itself... a "working memory" for the model.」「As token count grows, accuracy and recall degrade, a phenomenon known as context rot.」「Previous turns are preserved completely.」「Input phase: Contains all previous conversation history plus the current user message.」
  - AI 转述（可信度：高）：context=工作记忆、按 token 计、输入输出共享、历史逐轮累积重发、满了压缩/FIFO。
- 〔Liu et al. 2023, arXiv，论文，抓取 2026-06-15〕<https://arxiv.org/abs/2307.03172>
  - AI 转述（可信度：高）：信息在上下文开头/结尾时模型用得最好，埋在中间显著变差（lost in the middle）。

## 相关
[[Token]] · [[Agent]] · [[Harness]]
