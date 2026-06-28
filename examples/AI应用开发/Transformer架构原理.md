---
title: Transformer架构原理
category: AI应用开发
status: 已完成
track: 标准轨
importance: 4
prereqs: ["LLM工作原理与Token机制"]
groups: ["模型原理"]
goal_tags: ["求职", "工程"]
aliases: ["Transformer", "自注意力"]
tags: ["Transformer", "Self-Attention", "位置编码", "Encoder-Decoder"]
created: 2026-06-28
related: ["LLM工作原理与Token机制", "模型微调入门", "Embedding与向量表示"]
sources: ["https://arxiv.org/abs/1706.03762", "https://jalammar.github.io/illustrated-transformer/", "https://nlp.seas.harvard.edu/annotated-transformer/"]
viz: "AI应用开发/_viz/Transformer架构原理.svg"
viz_source: "AI应用开发/_viz/Transformer架构原理.mmd"
viz_chart: "hierarchy"
viz_reason: ""
---

# Transformer架构原理

## 一句话定位
> 它属于AI应用开发，是用来解决〔自注意力机制与 Encoder-Decoder 架构〕的——是读懂一切大模型论文和做微调的理论门槛。

## 🎯 核心收获 · 重点知识

**一句话成果**：学完你现在能讲清 Self-Attention 怎么让 token 互相"注意"、位置编码为什么必要、Encoder/Decoder 区别，面试时不再怕"讲讲 Transformer"。

**重点结论**（7 条）：
1. **Self-Attention 是核心**：每个 token 用 Q/K/V 三个投影"查询"其他 token，算注意力权重加权求和——让每个词"看到"整句上下文，捕捉长程依赖。
2. **Q/K/V 机制**：Q（查询）× K（键）算注意力分数→softmax→权重→乘 V（值）求和。是"查字典"的泛化：Q 是查询词，K 是词条，V 是释义。
3. **Multi-Head Attention**：并行多组 Q/K/V（如 8 头），各头学不同关系（语法/语义/指代），拼接后投影。多头比单头表达力强。
4. **位置编码**：Self-Attention 本身无序（打乱 token 顺序结果一样），要加位置编码告诉模型"谁在前谁在后"。正弦/可学习两种。
5. **Encoder vs Decoder**：Encoder 双向看全句（适合理解）；Decoder 自回归+Masked Attention（只看左边，适合生成）。GPT 是 Decoder-only，BERT 是 Encoder-only，T5 是 Encoder-Decoder。
6. **残差连接 + LayerNorm**：每个子层（Attention/FFN）都加残差和归一化，解决深层梯度问题，是能堆深的关键。
7. **Feed-Forward 网络**：每个位置独立过一个两层 FFN（升维→激活→降维），是模型的"记忆容量"。

**重点知识大纲**：
- Self-Attention
  - Q/K/V 三个投影
  - 注意力分数 = softmax(QK/√d)
  - 加权 V 求和
  - 捕捉长程依赖
- Multi-Head
  - 并行多组 Q/K/V
  - 各头学不同关系
  - 拼接投影
- 位置编码
  - 弥补无序性
  - 正弦 / 可学习
- Encoder vs Decoder
  - Encoder 双向（理解）
  - Decoder 自回归+Mask（生成）
  - GPT/BERT/T5 三架构
- 工程细节
  - 残差连接
  - LayerNorm
  - FFN 记忆容量

## 📝 轻笔记
<details>
<summary>📝 轻笔记（点开看推演摘要与卡壳细节）</summary>

**起点认知**：知道 Transformer 是大模型基础，但 Self-Attention 的 Q/K/V 一直没搞懂，以为就是"加权求和"。

**视觉模型（五问）**：
- 对象：Token、Embedding、位置编码、Q/K/V 矩阵、Attention 头、FFN、残差+LayerNorm
- 连接：Token→Embedding+位置→Multi-Head Attention→残差+LN→FFN→残差+LN→输出
- 流向：每个 token 并行流过 Attention+FFN，堆叠 N 层
- 边界：Self-Attention 无序需位置编码；计算量 O(n²)（序列长平方增长）
- 变化：序列变长→Attention 计算平方增→是长上下文瓶颈

**视觉模型结构**：chart_type=hierarchy。Transformer(concept)→[Self-Attention/Multi-Head/位置编码/Encoder-Decoder/残差LN/FFN]。

**类比**：Self-Attention 像会议室每个人同时听所有人发言并判断"谁说的对我重要"，加权综合形成自己的理解。Q 是"我想问什么"，K 是"每个人的标签"，V 是"每个人的内容"。

**大白话讲解**：它属于AI应用开发，解决大模型底层怎么工作。核心是"自注意力"——每个词同时看句子里所有词，判断谁跟自己最相关，加权吸收信息。这样"苹果"在"吃苹果"和"苹果手机"里能根据上下文有不同理解。多头就是多组这种注意力并行，各看不同关系。加位置编码是因为这套机制本身不分前后，得告诉它词序。

**三个应用例子**：
1. 语义理解：BERT 用双向 Attention 做情感/分类，比 RNN 强。
2. 文本生成：GPT 用 Masked Attention 自回归生成，逐 token 预测。
3. 翻译：T5 Encoder-Decoder，先理解再生成。

**失效边界**：
- 序列长→Attention O(n²) 计算爆炸（长上下文瓶颈）
- 位置编码对超长外推有限
- 训练成本高（数据+算力）

**边界补丁**：
- 边界1（长序列）→ 稀疏 Attention/Flash Attention/线性 Attention 优化
- 边界2（位置外推）→ RoPE/ALiBi 等相对位置编码
- 边界3（成本）→ 应用工程师用 API 不自己训，懂原理即可

**卡壳点复盘**：
1. Q/K/V 到底干嘛：原以为是三个向量→校准为三个投影矩阵，Q 查、K 被查、V 是内容，是"查字典"泛化。
2. 为什么要位置编码：原以为 Attention 自带顺序→校准为 Self-Attention 打乱顺序结果一样，必须显式加位置。
3. Encoder/Decoder 区别：原以为只是方向不同→校准为 Decoder 有 Masked Attention（只看左边）才能自回归生成。

**成长对比**：起点（Transformer=黑盒）→ 现在（Self-Attention Q/K/V+多头+位置编码+三大架构区别）。

</details>

📎 [完整对话记录](_transcript/Transformer架构原理.jsonl)

## 视觉模型图
- 打开图：[_viz/Transformer架构原理.svg](_viz/Transformer架构原理.svg)
- Mermaid 源：[_viz/Transformer架构原理.mmd](_viz/Transformer架构原理.mmd)

## 📚 参考资料
<details>
<summary>📚 参考资料</summary>

- **Attention Is All You Need**（arXiv，2026-06-28）https://arxiv.org/abs/1706.03762
  - 原话：Transformer 原始论文，提出 Self-Attention 取代 RNN。
- **Illustrated Transformer**（教程，2026-06-28）https://jalammar.github.io/illustrated-transformer/
  - 原话：图解 Transformer 各组件。
- **Annotated Transformer**（教程，2026-06-28）https://nlp.seas.harvard.edu/annotated-transformer/
  - 原话：逐行代码实现 Transformer。

</details>

## 🔭 视野拓展 · 行业洞见
<details>
<summary>🔭 视野拓展 · 行业洞见（点开看多维度权威参照）</summary>

### 1. Ashish Vaswani · Transformer 论文一作
- **身份**：前 Google研究员
- **与本概念的关系**：Transformer 原始论文一作，提出 Self-Attention 取代 RNN
- **核心洞见**："Attention is all you need"——纯注意力机制就够了，不需要循环
- **代表作**：*Attention Is All You Need*（NeurIPS 2017）
- **扩展阅读**：[arXiv 论文](https://arxiv.org/abs/1706.03762)

### 2. Jay Alammar · 可视化教学第一人
- **身份**：Cohere 工程总监
- **与本概念的关系**：Illustrated Transformer 是最流行的 Transformer 教程
- **核心洞见**：用图解把 Q/K/V 讲成小白能懂
- **代表作**：*The Illustrated Transformer*
- **扩展阅读**：[jalammar.github.io](https://jalammar.github.io/illustrated-transformer/)

### 3. Andrej Karpathy · 从零实现教学
- **身份**：前 Tesla AI 总监、OpenAI 创始成员
- **与本概念的关系**：用纯 NumPy/PyTorch 从零实现 GPT，把 Transformer 拆到最底
- **核心洞见**："you don't understand it until you build it"——从零实现是检验理解的试金石
- **代表作**：*Let's build GPT* YouTube 系列
- **扩展阅读**：[YouTube 视频](https://www.youtube.com/watch?v=kCc8FmEb1nY)

</details>

## 相关
[[LLM工作原理与Token机制]] · [[模型微调入门]] · [[Embedding与向量表示]]
