---
title: 高级RAG技术
category: AI应用开发
status: 已完成
track: 标准轨
importance: 4
prereqs: ["RAG基础架构"]
groups: ["RAG检索增强"]
goal_tags: ["求职", "工程"]
aliases: ["Advanced RAG", "RAG优化"]
tags: ["分块策略", "混合检索", "重排序", "Self-RAG", "Agentic RAG"]
created: 2026-06-28
related: ["RAG基础架构", "向量数据库与相似度检索", "Agent架构与ReAct模式", "AI应用评估与可观测性"]
sources: ["https://arxiv.org/abs/2310.11511", "https://python.langchain.com/docs/use_cases/question_answering/", "https://docs.llamaindex.ai/en/stable/optimizing/"]
viz: "AI应用开发/_viz/高级RAG技术.svg"
viz_source: "AI应用开发/_viz/高级RAG技术.mmd"
viz_chart: "hierarchy"
viz_reason: ""
---

# 高级RAG技术

## 一句话定位
> 它属于AI应用开发，是用来解决〔分块策略、混合检索、重排序、Self-RAG/Agentic RAG 等进阶优化〕的——把检索准确率拉到生产可用。

## 🎯 核心收获 · 重点知识

**一句话成果**：学完你现在能诊断 RAG 系统的检索/生成瓶颈，选对优化手段（分块/混合检索/重排/查询改写）把效果拉到生产级。

**重点结论**（7 条）：
1. **分块策略进阶**：固定长度→语义分块（按段落/标题）→递归分块（保持层级）→语义边界分块（用模型找断点）。语义分块召回率显著优于固定长度。
2. **混合检索（Hybrid）**：向量（语义）+ BM25（关键词）并行检索，RRF（Reciprocal Rank Fusion）融合排序，取长补短——向量补 BM25 的语义盲区，BM25 补向量的精确关键词盲区。
3. **重排序（Reranking）**：检索 top-50→用 cross-encoder 重排取 top-5。cross-encoder 比 bi-encoder 准但慢，所以先粗检索再精排。常用 BGE-reranker、Cohere Rerank。
4. **查询改写（Query Rewriting）**：用户原问题可能模糊/口语化，先让 LLM 改写成更好的检索 query（如"咋退货"→"商品退换货流程"），或多 query 并行检索取并集。
5. **Self-RAG**：模型自己判断"要不要检索""检索结果相不相关""回答有没有依据"，动态决策，减少不必要的检索和不相关的 grounding。
6. **Agentic RAG**：把 RAG 包成 Agent 工具，模型自主决定查不查、查哪个库、查几次，适合多源知识库场景。
7. **评估驱动优化**：用 RAGAS / TruLens 评 faithfulness（回答有没有依据）+ context_recall（检索召回）+ context_precision（检索精度），用数据指导优化方向。

**重点知识大纲**：
- 检索侧优化
  - 分块策略（语义/递归/边界）
  - 混合检索（向量+BM25+RRF）
  - 重排序（cross-encoder）
  - 查询改写（单/多query）
- 生成侧优化
  - Self-RAG（动态决策检索）
  - Agentic RAG（Agent 调用 RAG 工具）
  - 引用与可追溯
- 评估驱动
  - RAGAS（faithfulness/recall/precision）
  - TruLens / DeepEval
  - 黄金数据集
- 工程化
  - 索引更新策略
  - 多路召回并发
  - 缓存（query/embedding）

## 📝 轻笔记
<details>
<summary>📝 轻笔记（点开看推演摘要与卡壳细节）</summary>

**起点认知**：以为 RAG 优化就是"换个更好的 Embedding 模型"，不知道分块/混合检索/重排这些手段。

**视觉模型（五问）**：
- 对象：原始查询、查询改写器、多路检索器（向量+BM25）、融合器、重排器、上下文、LLM、Self-RAG 判断器
- 连接：查询→改写→多路检索→融合→重排→上下文→LLM；Self-RAG 在关键点做决策
- 流向：检索侧多路并行+融合+精排；生成侧动态决策
- 边界：优化手段叠加有边际递减；过度优化增加延迟和成本
- 变化：用户问题类型不同→激活不同优化（简单问题不需要改写）

**视觉模型结构**：chart_type=hierarchy。高级RAG(concept)下分三类：检索侧优化(process)、生成侧优化(process)、评估驱动(process)，每类下挂具体手段。

**类比**：基础 RAG 像单本词典查词，高级 RAG 像有个研究助理——先帮你把模糊问题问清楚（查询改写），同时查几本词典（混合检索），查完帮你挑最相关的几页（重排），还会判断"这个问题要不要查词典"（Self-RAG）。

**大白话讲解**：它属于AI应用开发，解决怎么让 RAG 答得更准。基础 RAG 就是搜文档塞给模型，但搜得不够准。高级 RAG 加了几招：先把你的问题问得更清楚，同时用语义和关键词两种方式搜，搜完再用更准的模型挑最相关的几段，还会判断"这问题要不要查"。就像从"翻一本词典"升级到"有个研究助理帮你查多本书并挑重点"。

**三个应用例子**：
1. 企业知识库：加混合检索+重排，召回率从 70%→90%。
2. 客服 bot：查询改写把"咋退货"改成"商品退换货流程"，检索更精准。
3. 多源研究：Agentic RAG 让模型自主决定查内部库还是联网。

**失效边界**：
- 优化叠加边际递减，要评估驱动别盲目堆
- 重排器增加延迟（cross-encoder 慢），实时场景要权衡
- Self-RAG 判断不准会漏检索或过度检索

**边界补丁**：
- 边界1（边际递减）→ 用 RAGAS 量化每步收益，停止无效优化
- 边界2（重排延迟）→ top-50→top-5 改 top-20→top-5，或用轻量 reranker
- 边界3（Self-RAG 误判）→ 加 fallback：不确定就检索

**卡壳点复盘**：
1. 混合检索为什么有效：原以为纯向量最好→校准为向量漏关键词精确匹配，BM25 漏语义，互补。
2. 重排为什么用 cross-encoder：原以为和 bi-encoder 一样→校准为 cross-encoder 把 query+doc 一起编码能捕捉交互，更准但慢。
3. Self-RAG 什么时候该用：原以为都用→校准为简单事实问题不需要，复杂/多跳问题才值得动态决策。

**成长对比**：起点（RAG优化=换Embedding）→ 现在（分块/混合/重排/改写/Self-RAG/评估驱动六把刀）。

</details>

📎 [完整对话记录](_transcript/高级RAG技术.jsonl)

## 视觉模型图
- 打开图：[_viz/高级RAG技术.svg](_viz/高级RAG技术.svg)
- Mermaid 源：[_viz/高级RAG技术.mmd](_viz/高级RAG技术.mmd)

## 📚 参考资料
<details>
<summary>📚 参考资料（点开查看本轮引用来源）</summary>

- **Self-RAG 论文**（arXiv，2026-06-28）https://arxiv.org/abs/2310.11511
  - 原话：Self-RAG 让模型自主判断检索时机和相关性。
- **LangChain Q&A 优化**（官方文档，2026-06-28）https://python.langchain.com/docs/use_cases/question_answering/
  - 原话：混合检索+重排是生产 RAG 标配。
- **LlamaIndex 优化指南**（官方文档，2026-06-28）https://docs.llamaindex.ai/en/stable/optimizing/
  - 原话：分块策略/检索/重排/评估的系统性优化。

</details>

## 🔭 视野拓展 · 行业洞见
<details>
<summary>🔭 视野拓展 · 行业洞见（点开看多维度权威参照）</summary>

### 1. Akari Asai · Self-RAG 作者
- **身份**：华盛顿大学研究员
- **与本概念的关系**：Self-RAG 论文一作，让模型自主决策检索
- **核心洞见**：不是所有问题都需要检索，让模型自己判断能减少噪声提升质量
- **代表作**：*Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection*
- **扩展阅读**：[arXiv 论文](https://arxiv.org/abs/2310.11511)

### 2. Shahul Es · RAGAS 作者
- **身份**：RAGAS 维护者
- **与本概念的关系**：RAGAS 是最流行的 RAG 评估框架，定义了 faithfulness/recall/precision 指标
- **核心洞见**：RAG 优化必须评估驱动，没指标就是盲调
- **代表作**：RAGAS 框架
- **扩展阅读**：[RAGAS GitHub](https://github.com/explodinggradients/ragas)

### 3. 唐杰（Tang Jie）· 国产 RAG 生态
- **身份**：清华大学教授、智谱 AI
- **与本概念的关系**：BGE-reranker 是中文 RAG 重排的事实标准
- **核心洞见**：中文 RAG 的重排要用中文数据训练，英文 reranker 中文效果打折
- **代表作**：BGE 系列（含 reranker）
- **扩展阅读**：[FlagEmbedding GitHub](https://github.com/FlagOpen/FlagEmbedding)

</details>

## 相关
[[RAG基础架构]] · [[向量数据库与相似度检索]] · [[Agent架构与ReAct模式]] · [[AI应用评估与可观测性]]
