---
title: LLM工作原理与Token机制
category: AI应用开发
status: 已完成
track: 标准轨
importance: 5
prereqs: []
groups: ["LLM基础认知"]
goal_tags: ["求职", "工程"]
aliases: ["Tokenization", "BPE分词", "自回归生成"]
tags: ["LLM基础", "Token", "上下文窗口", "KV Cache", "计费"]
created: 2026-06-28
related: ["Prompt工程基础", "ChatGPT API与对话系统", "Embedding与向量表示", "Transformer架构原理"]
sources: ["https://platform.openai.com/tokenizer", "https://github.com/openai/tiktoken", "https://platform.claude.com/docs/en/build-with-claude/context-windows", "https://machinelearningmastery.com/kv-caching-in-llms-a-guide-for-developers/", "https://aclanthology.org/P16-1162/"]
viz: "AI应用开发/_viz/LLM工作原理与Token机制.svg"
viz_source: "AI应用开发/_viz/LLM工作原理与Token机制.mmd"
viz_chart: "flow"
viz_reason: ""
---

# LLM工作原理与Token机制

## 一句话定位
> 它属于AI应用开发，是用来解决〔大模型如何逐 Token 生成文字、上下文窗口与成本计费的本质〕的——是理解一切 LLM 应用的地基。

## 🎯 核心收获 · 重点知识

**一句话成果**：学完你现在能讲清"模型怎么把文字切碎、怎么一个一个往外蹦字、为什么有长度限制、为什么按用量收钱"，并在面试和排错时不再把"上下文窗口"和"最大输出长度"混为一谈。

**重点结论**（7 条）：
1. **Token 是子词不是词/字**：BPE 用预训练合并表反复粘高频字节对，切分确定且可逆，不同模型合并表不同所以 token 数不同。
2. **"1 token ≈ 4 字节"**：是字节不是字符，中文/代码/特殊符号 token 密度远高于英文，成本估算必须实跑 tokenizer。
3. **上下文窗口 ≠ 最大输出长度**：窗口是输入+输出共用总容量（如 1M），`max_tokens` 是单次输出上限（如 128k），两个独立参数；且窗口越长越容易 context rot。
4. **自回归生成 + KV cache**：模型一个 token 一个 token 生成，每步 attention 要看全部历史，但历史 K/V 算过即缓存复用，prefill 并行填缓存、decode 每步只传新 token 的 Q。
5. **计费输入便宜输出贵**：输出通常贵 3-4 倍，因为生成需逐 token 串行 + 维护 KV cache；prompt caching / batch API 可降本。
6. **越长越慢越贵**：上下文变长 → 每步 attention 计算量线性增 + KV cache 显存线性增 + 输入 token 计费线性增，三重叠加。
7. **应用工程含义**：控上下文长度=控成本和延迟；中文场景别用字符数估 token；长对话要做摘要/压缩对抗 context rot。

**重点知识大纲 / 脑图**：
- Token 是什么
  - 子词级（不是词也不是字符）
  - BPE 合并表（预训练、确定、可逆）
  - 不同模型编码不同 → token 数不同
- 计量换算
  - 1 token ≈ 4 字节（非字符）
  - 英文 ~4 字符/token，中文 1 字 ≈ 1-2 token
  - 估算必须实跑 tokenizer（tiktoken）
- 上下文窗口
  - 输入+输出共用总容量
  - ≠ max_tokens（单次输出上限）
  - context rot：越长越不准
- 生成机制
  - 自回归：一个 token 一个 token 蹦
  - 每步 attention 看全部历史
  - KV cache：历史 K/V 复用，不重算
  - prefill 并行 / decode 串行
- 计费
  - 输入便宜、输出贵 3-4 倍
  - 按用量计费，prompt caching 可降本
  - 控长度 = 控成本+延迟

## 📝 轻笔记
<details>
<summary>📝 轻笔记（点开看推演摘要与卡壳细节）</summary>

**起点认知**：token≈一个词/一个字，1token≈4字符中英文通用，上下文窗口=最大输出长度，每步重算整个上下文，输入输出同价。（5 个设问猜了 4 个半错）

**视觉模型（五问 · 先自己讲后校准）**：
- **对象**：原始文本、分词器(BPE)、token ID 序列、模型(Transformer)、上下文窗口、KV Cache、概率分布、采样策略、新 token、计费规则
- **连接**：文本→分词器→ID→上下文窗口→模型→概率分布→采样→新token→回填上下文（自回归环）；模型↔KV Cache（旁路复用）；上下文窗口/新token→计费规则
- **流向**：单向流水线 + 自回归反馈回路；前面的 token 决定后面的预测
- **边界**：上下文窗口是硬上限；token 表外的字走字节级拆分；context rot（越长越不准）
- **变化**：每生成一个新 token 触发一次前向；上下文逐轮累加；EOS/max_tokens 触发停止

**视觉模型结构（AI 校准后）**：
- **chart_type**：flow（带反馈回路的有向流）
- **节点 kind**：原始文本(data)、分词器BPE(process)、Token ID序列(data)、上下文窗口(boundary)、Transformer模型(process)、KV Cache(state)、概率分布(data)、采样策略(process)、新Token(data)、计费规则(rule)
- **结构纠偏**：学习者原以为"每步重算整个上下文"→校准为"看全部但 KV cache 复用 K/V 不重算"；原以为"上下文窗口=最大输出"→校准为两个独立参数。

**类比**：它像**接龙游戏机+固定面积的桌子**——把你的话切成积木摆桌上（桌子面积=上下文窗口），一块一块猜着接（自回归），桌子越长找得越慢越容易找错（context rot），接出来比看进去费劲所以贵（输出贵 3-4 倍）。

**大白话讲解（讲给外行）**：它属于人工智能里的"语言模型"，解决怎么让电脑像人一样接话。想象一个超级有文化但只会接一个字的接龙游戏机：它先把你的话切成小积木（每块可能是字、半个字或词尾），每块有编号，摆到固定面积的桌上；然后看桌上积木猜下一块该接什么，蹦一块放桌上再猜下一块，所以打字是慢慢往外冒的。按用量收钱因为每蹦一块都要算一次，且"吐字"比"读字"贵好几倍。

**三个应用例子**：
1. 代码补全（Copilot）：长函数前面 200 行吃掉一两千 token，留给补全的窗口变少，attention 越分散越易跑偏。
2. 长对话摘要：对话越长累计 token 越多，要做摘要压缩对抗 context rot。
3. 中文客服 bot：5000 中文字实际 ~2400 token，按"4字符"估会严重低估成本。

**失效边界**：
- 边界 1：上下文窗口 ≠ 无限记忆，越长越 context rot
- 边界 2：中文/代码 token 成本被"4字符"经验严重低估
- 边界 3：上下文窗口 ≠ max output，输出会被单独的上限截断

**边界补丁**（失败边界 → 最小补救动作；本轮演练最容易翻车的边界 2）：
- 边界 1 → 补救：长对话做摘要压缩，只保留最近几轮 + 关键事实
- 边界 2 → 补救：上线前用 tiktoken 实跑真实 prompt 算 token 数，别用字符数估
- 边界 3 → 补救：设 max_tokens 留窗口余量，长输出改流式分段续写
- **本轮演练（边界 2）**：同事按"1token≈4字符"估中文客服 prompt 5000字≈1250token，上线账单翻 1.5 倍。回应动作：`enc = tiktoken.encoding_for_model("gpt-4o"); print(len(enc.encode(prompt)))` 实测 ~2400 token；改估算口径为"中文 1字≈1.3token 粗估，英文 1token≈4字符"；所有成本预估必须实跑 tokenizer 校准。

**卡壳点复盘**：
1. **BPE 切分规则含糊**：原讲不清"积木怎么切"→查 tiktoken README：BPE 拆单字节后反复合并最高频相邻字节对，靠一张训练时定死的合并表（mergeable_ranks），表里有的就合并没有就保持字节级，切分确定且可逆。
2. **"4字符"还是"4字节"搞混**：原以为 4 字符中英文通用→查 tiktoken README 原文是 "4 bytes"；中文 UTF-8 一字 3 bytes，一字常 1-2 token；日语"お誕生日おめでとう" r50k_base=14 token、o200k_base=8 token，强依赖编码表。
3. **KV cache 漏讲**：原说"每步重算整个上下文"→只对一半。查 KV cache 文档：attention 每步 Q 是新的但历史 K/V 不变，缓存复用；prefill 并行填缓存、decode 每步只传新 token 的 Q。是"看全部但不重算全部"。

**成长对比**：起点认知（token≈词/字、4字符通用、窗口=输出、重算全部、输入输出同价）→ 现在的理解（子词级BPE、4字节非字符、窗口≠max_tokens、KV cache复用、输出贵3-4倍）。5 个设问错 4 个半，校准后才能在面试讲清。

</details>

📎 [完整对话记录](_transcript/LLM工作原理与Token机制.jsonl)

## 视觉模型图
- 打开图：[_viz/LLM工作原理与Token机制.svg](_viz/LLM工作原理与Token机制.svg)
- Mermaid 源：[_viz/LLM工作原理与Token机制.mmd](_viz/LLM工作原理与Token机制.mmd)

图表类型：`flow`（带自回归反馈回路的有向流）。核心回路：原始文本 → BPE 分词 → Token ID → 上下文窗口（boundary 硬约束）→ Transformer → 概率分布 → 采样 → 新 Token → 回填上下文（自回归循环）。旁路：模型 ↔ KV Cache（state，复用历史 K/V 不重算）；计费规则（rule）分别接上下文窗口（输入计数）和新 Token（输出计数，贵 3-4 倍）。

## 📚 参考资料
<details>
<summary>📚 参考资料（点开查看本轮引用来源）</summary>

- **OpenAI Tokenizer 官方页**（官方文档，2026-06-28 抓取）链接：https://platform.openai.com/tokenizer
  - 原话引述："OpenAI's large language models process text using tokens, which are common sequences of characters found in a set of text."
  - AI 转述（可信度：高）：token 是文本中常见的字符序列，模型学的是 token 间的统计关系。

- **OpenAI tiktoken README**（官方文档，2026-06-28 抓取）链接：https://github.com/openai/tiktoken
  - 原话引述："each token corresponds to about 4 bytes"（纠正了"4 字符"的错误）
  - AI 转述（可信度：高）：BPE 把高频字节对粘成子词，"ing" 这种常见子词会被单独切一个 token。

- **Anthropic Claude Context Windows 文档**（官方文档，2026-06-28 抓取）链接：https://platform.claude.com/docs/en/build-with-claude/context-windows
  - 原话引述："The context window refers to all the text a language model can reference when generating a response, including the response itself... As token count grows, accuracy and recall degrade, a phenomenon known as context rot."
  - AI 转述（可信度：高）：上下文窗口是输入+输出共用总容量，Claude Opus 4.6/4.7/4.8 窗口 1M、单次输出上限 128k。

- **Machine Learning Mastery · KV Caching**（工程教程，2026-06-28 抓取）链接：https://machinelearningmastery.com/kv-caching-in-llms-a-guide-for-developers/
  - 原话引述："When generating token, only Q changes. The K and V for all previous tokens are identical to what they were in the previous step."
  - AI 转述（可信度：高）：KV cache 让历史 K/V 复用，只算新 token 的 Q，3-5× 加速。

- **Sennrich et al. 2016 BPE 论文**（ACL 论文，2026-06-28 抓取）链接：https://aclanthology.org/P16-1162/
  - 原话引述："rare words can be translated by translating smaller units than words"
  - AI 转述（可信度：高）：BPE 用于把罕见词拆为子词单元，是现代 tokenizer 的理论源头。

</details>

## 🔭 视野拓展 · 行业洞见
<details>
<summary>🔭 视野拓展 · 行业洞见（点开看多维度权威参照）</summary>

### 1. Rico Sennrich · BPE 引入 NLP 的奠基人
- **身份**：爱丁堡大学副教授
- **与本概念的关系**：他把原本用于数据压缩的 BPE 算法引入神经机器翻译，解决罕见词问题，是今天所有 BPE tokenizer 的理论源头
- **核心洞见**："rare words can be translated by translating smaller units than words"——用比词更小的子词单元翻译罕见词，是 BPE 用于分词的原始动机
- **代表作**：*Neural Machine Translation of Rare Words with Subword Units*（ACL 2016）
- **扩展阅读**：[ACL Anthology 官方链接](https://aclanthology.org/P16-1162/)

### 2. Andrej Karpathy · 从零手搓 tokenizer 的工程布道者
- **身份**：前 Tesla AI 总监、OpenAI 创始成员
- **与本概念的关系**：用纯 Python 从零实现 BPE 分词器，把"黑盒 tokenizer"拆到字节级给工程师看
- **核心洞见**："tokenization is the most annoying part of LLMs"——分词是 LLM 工程里最易被忽视又最易出 bug 的环节（模型不会拼写、不会算数、对中文/代码不友好，根子都在分词）
- **代表作**：YouTube 视频 *Let's build the Tokenizer: BPE in Python*
- **扩展阅读**：[YouTube 视频](https://www.youtube.com/watch?v=zduSFxRajvE)

### 3. Jay Alammar · Transformer 可视化教学第一人
- **身份**：Cohere 工程总监、技术博主
- **与本概念的关系**：用图解把 Transformer/attention/自回归生成讲成小白能懂的流水线，是理解"token 怎么在模型里流动"的最佳入口
- **核心洞见**：用"每个词流向自己向量的流水线"图解 self-attention，让人一眼看懂 token 之间如何互相注意——这正是自回归生成和上下文窗口机制的底层
- **代表作**：*The Illustrated Transformer*
- **扩展阅读**：[Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)

</details>

## 相关
[[Prompt工程基础]] · [[ChatGPT API与对话系统]] · [[Embedding与向量表示]] · [[Transformer架构原理]]
