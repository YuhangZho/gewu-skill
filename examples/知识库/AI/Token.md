---
title: Token
category: AI
groups: ["模型基础"]
status: 已学透
importance: 5
prereqs: []
goal_tags: []
aliases: ["令牌", "词元"]
tags: [AI]
created: 2026-06-15
related: [Context, Agent]
sources: ["https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them", "https://huggingface.co/docs/transformers/main/en/tokenizer_summary"]
---

# Token

## 一句话定位
> 它属于 AI 大模型，是模型处理文本的**最小单位**：一段"词的碎片"，也是衡量长度与计费的单位。

## 动态图像（视觉建模）
一条翻译流水线，进来是人话、出去也是人话，中间一段模型只认数字：
人话 → 分词器**切成碎片**（token）→ **查词表换成编号**（id）→ 模型在 id 上计算 → 吐出新 id → **拼回人话**。
关键两道工序：① 切碎片 ② 碎片↔id 查表。**token = 碎片本身，id = 它在词表里的门牌号**（id 数值大小没有含义，只是编号）。

## 类比
像拼高达：设计师把成品拆成一个个**最小零部件**（token），每个零件有**编号**（id）；拿到一袋带编号的零件，再按说明书拼回成品（解码）。

## 大白话讲解（讲给外行）
token 是"词的碎片"，不等于字 / 词 / 字符——分词器**不按词边界切，按语料里的高频片段切**。
例：`ChatGPT is great!` 实际是 **6 个 token**：`Chat | G | PT | ␣is | ␣great | !`（"ChatGPT"不是常见词被剪成三块，" great"带空格算一个）。
为什么要这层：模型只能吃**固定词表里的整数 id**。按整词建表 → 生僻词/新词爆表且认不出（OOV）；按单字符 → 序列太长。**子词分词（BPE）是折中**：常见词留成 1 个 token，罕见词拆成已知子词。
经验值：英文 **1 token ≈ 4 字符 ≈ ¾ 个词**。

## 三个应用例子
1. 数 token / 估长度：用 OpenAI Tokenizer 之类工具先数 token，再决定能不能塞进上下文。
2. 估成本：API 按 token 计费（输入/输出/缓存分开计价），不是按字数。
3. 压缩上下文：把啰嗦 prompt 改短、把中文换成等价英文，都能省 token。

## 失效边界（不懂 token 会踩的坑）
- **算钱**：以为按"文字数量"收费，实际按拆出的 **token 数** → 账单/预算算错（非英文尤甚）。
- **上下文上限**：塞了很多内容，拆成 token 后**超限被截断**，模型其实没看到后半段。
- **非英文**：同一个上下文窗口/同样预算，中文能装的实际内容比英文少一截；拿英文 demo 估的长度与成本，搬到中文会**双双爆掉**。
- 根因澄清：中文更费 token **不是因为中文啰嗦**（中文信息密度其实更高），而是**分词器主要在英文上训练、没给中文学到高效合并片段**——是工具偏科。

## 卡壳点复盘
- 起初把 token 和 id 混为一谈 → 其实是两样：碎片（token）↔ 编号（id），中间隔一次查表。
- "ChatGPT is great!" 直觉数成 5，实际 6 → 碎片按**高频片段**切，不按词/字边界。
- 误以为"中文费 token = 中文啰嗦" → 反了，是分词器对中文压缩效率低。

## 成长对比
- 起点认知：token 是 AI 计量的基本单位，可能是一个字或多字组合。
- 现在的理解：token = 高频"词碎片"（≠字/词），经查表变成 id 喂给模型；是长度与计费单位；中文更费源于分词器偏科；不懂它会在算钱/超限/非英文上踩坑。

## 出处 / Sources
- 〔OpenAI 官方帮助中心，一手，抓取 2026-06-15〕<https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them>
  - 原话引述：「Tokens can be thought of as pieces of words... tokens can include trailing spaces and even sub-words.」「1 token ~= 4 chars in English」「1 token ~= ¾ words」「The higher token-to-char ratio can make it more expensive to implement the API for languages other than English.」
  - AI 转述（可信度：高）：token 是词的碎片、按高频片段切、英文约 4 字符/词元、非英文 token-字符比更高更贵。
- 〔Hugging Face Transformers 分词文档，技术资料，抓取 2026-06-15〕<https://huggingface.co/docs/transformers/main/en/tokenizer_summary>
  - AI 转述（可信度：高）：子词分词（BPE）保留固定词表、常见词成单 token、罕见词拆子词以解决 OOV。
- 〔arXiv 2305.17179 多语言分词，论文，抓取 2026-06-15〕<https://arxiv.org/pdf/2305.17179>
  - AI 转述（可信度：中）：分词器在不同语言间的词表分配不均，影响非英文的 token 效率。

## 相关
[[Context]] · [[Agent]]
