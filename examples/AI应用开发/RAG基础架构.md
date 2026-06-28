---
title: RAG基础架构
category: AI应用开发
status: 已完成
track: 标准轨
importance: 5
prereqs: ["Embedding与向量表示", "向量数据库与相似度检索", "Prompt工程基础"]
groups: ["RAG检索增强"]
goal_tags: ["求职", "工程"]
aliases: ["RAG", "检索增强生成"]
tags: ["RAG", "检索", "知识库", "幻觉"]
created: 2026-06-28
related: ["Embedding与向量表示", "向量数据库与相似度检索", "Prompt工程基础", "高级RAG技术", "LangChain框架"]
sources: ["https://research.ibm.com/blog/retrieval-augmented-generation-RAG", "https://docs.llamaindex.ai/en/stable/", "https://python.langchain.com/docs/use_cases/question_answering/"]
viz: "AI应用开发/_viz/RAG基础架构.svg"
viz_source: "AI应用开发/_viz/RAG基础架构.mmd"
viz_chart: "flow"
viz_reason: ""
---

# RAG基础架构

## 一句话定位
> 它属于AI应用开发，是用来解决〔检索-增强-生成的完整管道〕的——解决大模型知识滞后、幻觉、私域知识缺失三大痛点。

## 🎯 核心收获 · 重点知识

**一句话成果**：学完你现在能从 0 搭一个 RAG 问答系统：文档解析→分块→embed→入库→检索→构造 prompt→生成，并知道每步的坑。

**重点结论**（7 条）：
1. **RAG = 检索+生成**：先从知识库检索相关文档块，再把检索结果塞进 prompt 让模型"看着答"，用检索 grounding 对抗幻觉。
2. **三大痛点对应**：知识滞后（知识库可实时更新）+ 幻觉（有引用可追溯）+ 私域知识缺失（企业文档入库）。
3. **完整管道六步**：文档解析→分块（chunking）→embed→入库（indexing）→检索（retrieval）→生成（generation）。
4. **分块是关键**：块太大检索不精准、太小丢上下文；常用 500-1000 token + 重叠 50-100；语义分块（按段落/标题）比固定长度好。
5. **检索质量决定生成质量**："garbage in garbage out"——检索召回率低，模型再强也答不好；要监控 recall@k。
6. **Prompt 要给引用**：让模型基于检索内容回答，并标注来源（"根据[文档1]..."），便于人工核查。
7. **评估三指标**：检索指标（recall@k/MRR）+ 生成指标（faithfulness/answer relevance）+ 端到端（用户满意度）。

**重点知识大纲**：
- 为什么需要 RAG
  - 知识滞后（模型训练有截止）
  - 幻觉（无引用）
  - 私域知识缺失（没见过企业文档）
- 完整管道
  - 文档解析（PDF/HTML/Word）
  - 分块（固定/语义/递归）
  - Embedding
  - 入库（向量化+索引）
  - 检索（top-k 相关块）
  - 生成（检索内容+prompt→LLM）
- 关键工程点
  - 分块策略（大小/重叠/语义边界）
  - 检索质量监控（recall@k）
  - Prompt 给引用
- 评估
  - 检索：recall@k / MRR
  - 生成：faithfulness / relevance
  - 端到端：用户满意度

## 📝 轻笔记
<details>
<summary>📝 轻笔记（点开看推演摘要与卡壳细节）</summary>

**起点认知**：知道 RAG 是"检索+生成"，但以为就是"搜文档塞给模型"，不知道分块、检索质量、评估这些工程细节。

**视觉模型（五问）**：
- 对象：原始文档、分块器、Embedding、向量库、查询、检索器、Prompt 构造器、LLM、回答
- 连接：文档→分块→embed→入库；查询→embed→检索→top-k→prompt→LLM→回答
- 流向：离线索引（一次性）+ 在线查询（实时）两条流
- 边界：检索不到相关内容时模型会硬编（幻觉）；文档更新要重新索引
- 变化：文档增删→重新 embed 入库；查询不同→检索结果不同→prompt 不同

**视觉模型结构**：chart_type=flow。离线流：文档(data)→分块(process)→embed(process)→向量库(state)。在线流：查询(data)→embed→检索(process)→top-k(data)→prompt组装(process)→LLM(process)→回答(data)。

**类比**：像开卷考试——模型是考生（会做题但记不住所有知识），知识库是课本，RAG 是"先翻书找相关页再答题"。不翻书硬答=幻觉，翻到错页=答非所问，翻对页+会答题=RAG 成功。

**大白话讲解**：它属于AI应用开发，解决怎么让 AI 用你自己的文档回答问题。AI 本身记不住你公司的资料，所以先建个文档库，问问题时先搜相关段落，把段落和问题一起给 AI 让它"看着答"。这样答得准、能溯源、还能随时更新文档不用重训模型。关键在分块（文档切多大）和检索（搜得准不准）。

**三个应用例子**：
1. 企业知识库问答：员工问"年假怎么请"→检索员工手册相关段→AI 基于段答+引用。
2. 技术文档助手：开发者问"这个 API 怎么用"→检索文档→答+代码示例。
3. 客服 bot：用户问"怎么退货"→检索退换货政策→答+步骤。

**失效边界**：
- 检索召回率低→模型无依据→幻觉
- 文档过时未更新→答错
- 问题超出知识库范围→模型硬编

**边界补丁**：
- 边界1（召回低）→ 调分块/换 Embedding/混合检索/调 top-k
- 边界2（文档过时）→ 建增量更新机制，文档变更触发重新索引
- 边界3（超范围）→ Prompt 加"如果检索内容不足以回答，说'我不知道'"

**卡壳点复盘**：
1. 分块为什么重要：原以为随便切→校准为块大小直接影响检索精度和上下文完整性，是 RAG 最易翻车的工程点。
2. 检索质量怎么评：原以为看回答好不好→校准为要先评 recall@k（检索召回），检索不行生成再好也白搭。
3. 引用怎么给：原以为让模型自己标→校准为要在 prompt 里把检索块编号（[1][2]），让模型引用编号。

**成长对比**：起点（RAG=搜文档塞模型）→ 现在（六步管道+分块工程+检索评估+引用机制+失效边界）。

</details>

📎 [完整对话记录](_transcript/RAG基础架构.jsonl)

## 视觉模型图
- 打开图：[_viz/RAG基础架构.svg](_viz/RAG基础架构.svg)
- Mermaid 源：[_viz/RAG基础架构.mmd](_viz/RAG基础架构.mmd)

## 📚 参考资料
<details>
<summary>📚 参考资料（点开查看本轮引用来源）</summary>

- **IBM Research RAG 博客**（官方，2026-06-28）https://research.ibm.com/blog/retrieval-augmented-generation-RAG
  - 原话：RAG 通过检索外部知识 grounding 生成，对抗幻觉。
- **LlamaIndex 文档**（官方文档，2026-06-28）https://docs.llamaindex.ai/en/stable/
  - 原话：LlamaIndex 是 RAG 框架，提供数据连接/索引/检索/生成全流程。
- **LangChain Q&A 文档**（官方文档，2026-06-28）https://python.langchain.com/docs/use_cases/question_answering/
  - 原话：RAG 问答的标准实现流程。

</details>

## 🔭 视野拓展 · 行业洞见
<details>
<summary>🔭 视野拓展 · 行业洞见（点开看多维度权威参照）</summary>

### 1. Lewis et al · RAG 论文作者
- **身份**：Facebook AI Research（FAIR）
- **与本概念的关系**：2020 年首次提出 Retrieval-Augmented Generation 框架，奠定 RAG 范式
- **核心洞见**："retrieval-augmented generation"——把检索作为生成的一部分，让模型访问外部知识
- **代表作**：*Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*（NeurIPS 2020）
- **扩展阅读**：[arXiv 论文](https://arxiv.org/abs/2005.11401)

### 2. Jerry Liu · LlamaIndex 创始人
- **身份**：LlamaIndex 创始人
- **与本概念的关系**：LlamaIndex 是最主流的 RAG 框架之一，把 RAG 工程化标准化
- **核心洞见**：RAG 的工程复杂度在数据连接和索引，框架的价值在于抽象这些
- **代表作**：LlamaIndex
- **扩展阅读**：[LlamaIndex Docs](https://docs.llamaindex.ai/)

### 3. Greg Kamradt · RAG 教学布道者
- **身份**：技术博主、AI 工程师
- **与本概念的关系**：写了最流行的 RAG 从0到1教程，把工程细节讲透
- **核心洞见**：RAG 不是"搜文档塞模型"，分块/检索/评估每步都有坑，要系统化
- **代表作**：*RAG From Scratch* 教程系列
- **扩展阅读**：[Greg Kamradt GitHub](https://github.com/gkamradt)

</details>

## 相关
[[Embedding与向量表示]] · [[向量数据库与相似度检索]] · [[Prompt工程基础]] · [[高级RAG技术]] · [[LangChain框架]]
