---
title: LangChain框架
category: AI应用开发
status: 已完成
track: 标准轨
importance: 5
prereqs: ["Prompt工程基础", "ChatGPT API与对话系统"]
groups: ["开发框架与工程化"]
goal_tags: ["求职", "工程"]
aliases: ["LangChain"]
tags: ["LangChain", "Chain", "Memory", "Retriever", "Tool"]
created: 2026-06-28
related: ["Prompt工程基础", "ChatGPT API与对话系统", "RAG基础架构", "Agent架构与ReAct模式", "LCEL与LangGraph"]
sources: ["https://python.langchain.com/docs/get_started/introduction", "https://docs.langchain.com/", "https://github.com/langchain-ai/langchain"]
viz: "AI应用开发/_viz/LangChain框架.svg"
viz_source: "AI应用开发/_viz/LangChain框架.mmd"
viz_chart: "hierarchy"
viz_reason: ""
---

# LangChain框架

## 一句话定位
> 它属于AI应用开发，是用来解决〔LLM 应用编排框架的核心抽象〕的——Chain/Memory/Retriever/Tool 是 AI 应用开发的"事实标准"。

## 🎯 核心收获 · 重点知识

**一句话成果**：学完你现在能用 LangChain 组装一个完整 AI 应用（LLM+Prompt+Memory+Retriever+Tool），并知道每个抽象解决什么问题。

**重点结论**（7 条）：
1. **LangChain = LLM 应用的"脚手架"**：封装 LLM/Prompt/Memory/Retriever/Tool/Agent 为可组合组件，让你像搭积木做应用而不是从 API 写起。
2. **六大核心抽象**：① Models（LLM/Chat/Embedding）；② Prompts（模板/管理）；③ Memory（对话记忆）；④ Retrievers（检索器）；⑤ Tools/Agents（工具/智能体）；⑥ Chains（串联一切）。
3. **Chain 是核心编排原语**：把多个组件串成管道（Prompt→LLM→OutputParser），LCEL 是声明式语法（`prompt | llm | parser`）。
4. **Memory 管理对话状态**：BufferMemory（全留）/SummaryMemory（摘要）/VectorStoreMemory（向量检索过往），解决 API 无状态问题。
5. **Retriever 抽象检索**：统一向量库/SQL/关键词检索接口，让 RAG 切换数据源不改代码。
6. **Agent = LLM+Tools+循环**：LangChain 的 Agent 抽象封装了 ReAct 循环，配合 Tool 使用。
7. **生产化要配 LangSmith**：LangChain 应用调试/监控/评估用 LangSmith，看每步输入输出和 token 消耗。

**重点知识大纲**：
- LangChain 定位
  - LLM 应用脚手架
  - 可组合组件
  - 事实标准
- 六大核心抽象
  - Models（LLM/Chat/Embedding）
  - Prompts（模板/管理）
  - Memory（对话状态）
  - Retrievers（检索统一接口）
  - Tools/Agents（工具/智能体）
  - Chains（编排串联）
- Chain 与 LCEL
  - Chain = 组件管道
  - LCEL 声明式语法
  - Runnable 接口
- Memory 类型
  - Buffer（全留）
  - Summary（摘要）
  - VectorStore（向量检索）
- Retriever 抽象
  - 统一检索接口
  - 切换数据源不改码
- 生产化
  - LangSmith 调试监控
  - LangServe 部署

## 📝 轻笔记
<details>
<summary>📝 轻笔记（点开看推演摘要与卡壳细节）</summary>

**起点认知**：以为 LangChain 就是"封装 OpenAI API"，不知道六大抽象和 Chain 编排这层。

**视觉模型（五问）**：
- 对象：Models、Prompts、Memory、Retriever、Tools、Chains、LCEL、应用
- 连接：Prompt+LLM+Parser 组成 Chain；Chain 可嵌 Memory/Retriever/Tool；Agent 是带 Tools 的 Chain
- 流向：用户输入→Prompt 填充→LLM→（可选 Retriever/Memory/Tool）→OutputParser→输出
- 边界：LangChain 抽象有学习成本；过度封装可能限制灵活性；生产要配 LangSmith
- 变化：换模型/换检索器/换 Memory 类型→改组件不改 Chain 结构

**视觉模型结构**：chart_type=hierarchy。LangChain(concept)→[Models/Prompts/Memory/Retrievers/Tools/Chains](各 concept)，Chains 下挂 LCEL(process)。

**类比**：LangChain 像 AI 应用版的 Django/Express——不让你从 socket 写起，而是提供 Model/Router/Middleware 抽象，你组装就行。Chain 是管道（像 Unix pipe），Memory 是会话存储，Retriever 是数据源适配器。

**大白话讲解**：它属于AI应用开发，解决怎么快速搭 AI 应用。直接调 API 要自己管状态/检索/工具，LangChain 把这些封装成可拼装的积木——记忆积木、检索积木、工具积木，用 Chain 把它们串起来。就像用 Django 建站不用从 TCP 写起，LangChain 让你专注业务逻辑。

**三个应用例子**：
1. RAG 问答：Retriever+Memory+LLM 组 Chain，10 行代码搭起来。
2. 客服 Agent：Tool（查订单/退换货）+Agent 抽象，自主调用。
3. 文档对话：VectorStoreMemory+Retriever，长文档分块检索对话。

**失效边界**：
- 抽象泄漏（底层问题还是要懂 API）
- 版本迭代快，API 常变
- 过度封装限制灵活性

**边界补丁**：
- 边界1（抽象泄漏）→ 关键路径还是懂底层 API
- 边界2（版本变）→ 锁版本 + 关注 changelog
- 边界3（灵活性）→ 复杂场景自己实现，LangChain 做 80% 通用

**卡壳点复盘**：
1. Chain 和 LCEL 区别：原以为一样→校准为 Chain 是概念，LCEL 是声明式语法（`|` 管道）。
2. Memory 什么时候用：原以为都用→校准为单轮不用，多轮才需要，且要选类型（摘要 vs 向量）。
3. Agent 和 Chain 区别：原以为一样→校准为 Chain 是固定流程，Agent 是自主决策，复杂度不同。

**成长对比**：起点（LangChain=API封装）→ 现在（六大抽象+Chain编排+Memory类型+Retriever统一+LangSmith生产化）。

</details>

📎 [完整对话记录](_transcript/LangChain框架.jsonl)

## 视觉模型图
- 打开图：[_viz/LangChain框架.svg](_viz/LangChain框架.svg)
- Mermaid 源：[_viz/LangChain框架.mmd](_viz/LangChain框架.mmd)

## 📚 参考资料
<details>
<summary>📚 参考资料（点开查看本轮引用来源）</summary>

- **LangChain Python 文档**（官方文档，2026-06-28）https://python.langchain.com/docs/get_started/introduction
  - 原话：LangChain 提供 Models/Prompts/Memory/Retrievers/Tools/Chains 六大抽象。
- **LangChain 新版文档**（官方，2026-06-28）https://docs.langchain.com/
  - 原话：LCEL 是声明式链构建语法。
- **LangChain GitHub**（开源，2026-06-28）https://github.com/langchain-ai/langchain
  - 原话：最流行的 LLM 应用框架。

</details>

## 🔭 视野拓展 · 行业洞见
<details>
<summary>🔭 视野拓展 · 行业洞见（点开看多维度权威参照）</summary>

### 1. Harrison Chase · LangChain 创始人
- **身份**：LangChain Inc CEO
- **与本概念的关系**：LangChain 的设计者和推动者，定义了 LLM 应用框架的范式
- **核心洞见**：LLM 应用需要"可组合抽象"，像 Web 框架一样让开发者专注业务
- **代表作**：LangChain、LangGraph、LangSmith
- **扩展阅读**：[LangChain 官网](https://www.langchain.com/)

### 2. Greg Kamradt · LangChain 教学布道者
- **身份**：技术博主
- **与本概念的关系**：写了最流行的 LangChain 教程系列，让框架普及
- **核心洞见**：框架的价值在"标准化"，让 AI 应用开发从手工作坊变工业化
- **代表作**：LangChain 教程系列
- **扩展阅读**：[Greg Kamradt GitHub](https://github.com/gkamradt)

### 3. Jerry Liu · LlamaIndex 创始人（对照视角）
- **身份**：LlamaIndex 创始人
- **与本概念的关系**：LlamaIndex 是 LangChain 的主要对照，专注 RAG 数据层
- **核心洞见**：LangChain 通用编排，LlamaIndex 专注数据连接和 RAG，两者互补
- **代表作**：LlamaIndex
- **扩展阅读**：[LlamaIndex 官网](https://www.llamaindex.ai/)

</details>

## 相关
[[Prompt工程基础]] · [[ChatGPT API与对话系统]] · [[RAG基础架构]] · [[Agent架构与ReAct模式]] · [[LCEL与LangGraph]]
