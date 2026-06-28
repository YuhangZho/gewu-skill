---
title: LCEL与LangGraph
category: AI应用开发
status: 已完成
track: 标准轨
importance: 4
prereqs: ["LangChain框架", "Agent架构与ReAct模式"]
groups: ["开发框架与工程化"]
goal_tags: ["求职", "工程"]
aliases: ["LCEL", "LangGraph", "Runnable"]
tags: ["LCEL", "LangGraph", "声明式", "状态图", "生产级"]
created: 2026-06-28
related: ["LangChain框架", "Agent架构与ReAct模式", "多Agent协作与工作流编排"]
sources: ["https://python.langchain.com/docs/expression_language/", "https://langchain-ai.github.io/langgraph/", "https://docs.smith.langchain.com/"]
viz: "AI应用开发/_viz/LCEL与LangGraph.svg"
viz_source: "AI应用开发/_viz/LCEL与LangGraph.mmd"
viz_chart: "hierarchy"
viz_reason: ""
---

# LCEL与LangGraph

## 一句话定位
> 它属于AI应用开发，是用来解决〔声明式链构建 LCEL + 有状态工作流 LangGraph〕的——是从 demo 走向生产级 Agent 的关键。

## 🎯 核心收获 · 重点知识

**一句话成果**：学完你现在能用 LCEL 声明式构建链，用 LangGraph 实现有状态/有环/人在回路的 Agent 工作流，知道为什么这俩是生产标配。

**重点结论**（7 条）：
1. **LCEL = 声明式链语法**：`prompt | llm | parser` 用管道符组合 Runnable 组件，自动处理批处理/异步/流式/重试，比命令式 Chain 更简洁强大。
2. **Runnable 统一接口**：所有组件（Prompt/LLM/Retriever/Parser）实现 Runnable 接口（invoke/batch/stream），可无缝组合。
3. **LangGraph = 状态图编排**：节点=函数/Agent，边=条件跳转，状态=共享 dict；支持环（循环）、分支、并行，比线性 Chain 强大。
4. **生产级特性**：① Checkpoint（持久化状态，崩溃恢复）；② 人在回路（interrupt 暂停等人审批）；③ 流式（每步增量输出）；④ 并行（多节点同时跑）。
5. **LCEL 适合线性流程**：Prompt→LLM→Parser 这种直线管道用 LCEL 最简洁。
6. **LangGraph 适合复杂流程**：Agent 循环/多 Agent 协作/条件分支/状态恢复用 LangGraph，可控可观测。
7. **配 LangSmith 可观测**：LCEL/LangGraph 的每步自动记录到 LangSmith，看输入输出/token/延迟，是生产调试标配。

**重点知识大纲**：
- LCEL 声明式链
  - 管道符语法（|）
  - Runnable 统一接口
  - 自动批处理/异步/流式/重试
  - 适合线性流程
- LangGraph 状态图
  - 节点+边+条件
  - 共享状态 dict
  - 支持环/分支/并行
  - 适合复杂流程
- 生产级特性
  - Checkpoint 持久化
  - 人在回路 interrupt
  - 流式输出
  - 并行执行
- 选型
  - 线性 → LCEL
  - 复杂/Agent → LangGraph
- 可观测
  - LangSmith 集成
  - 每步输入输出记录

## 📝 轻笔记
<details>
<summary>📝 轻笔记（点开看推演摘要与卡壳细节）</summary>

**起点认知**：以为 LCEL 就是个语法糖，LangGraph 没听过，不知道生产级特性这层。

**视觉模型（五问）**：
- 对象：Runnable 组件、管道符|、StateGraph、节点、边、Checkpoint、Interrupt
- 连接：LCEL：组件1|组件2|组件3；LangGraph：节点通过边连接，条件边控制跳转
- 流向：LCEL 线性流；LangGraph 图流（可环可分支）
- 边界：LCEL 不适合复杂循环；LangGraph 学习曲线陡
- 变化：状态 dict 更新驱动 LangGraph 流程推进

**视觉模型结构**：chart_type=hierarchy。LCEL与LangGraph(concept)→[LCEL(线性)/LangGraph(图)]，各下挂特性。

**类比**：LCEL 像 Unix 管道（`cat | grep | sort`），简单线性；LangGraph 像工作流引擎（Airflow/Temporal），有分支有循环有状态，适合复杂业务流。

**大白话讲解**：它属于AI应用开发，解决怎么把 AI 应用做到生产级。LCEL 让你像搭管道一样串组件（`prompt | llm | parser`），简洁还能自动处理并发流式。LangGraph 适合更复杂的——有循环（Agent 反复调工具）、有分支（条件跳转）、要暂停让人审批、要能崩溃恢复。简单流程用 LCEL，复杂 Agent 用 LangGraph。

**三个应用例子**：
1. 翻译管道：`prompt | llm | parser` LCEL 3 行搞定，自动流式。
2. 客服 Agent：LangGraph 建状态图，分类→路由→处理→必要时人工审批→回复，可恢复。
3. 研究助手：LangGraph 多步（搜→读→总结→不够再搜），有环能循环。

**失效边界**：
- LCEL 搞不定循环/条件跳转
- LangGraph 学习成本高，简单任务用它过重
- Checkpoint 存储要选对（内存/Redis/DB）

**边界补丁**：
- 边界1（LCEL 局限）→ 复杂流程换 LangGraph
- 边界2（LangGraph 过重）→ 简单任务还是 LCEL
- 边界3（Checkpoint）→ 生产用 Redis/Postgres，本地用内存

**卡壳点复盘**：
1. LCEL 和旧 Chain 区别：原以为语法糖→校准为 Runnable 统一接口，自动处理批/异步/流式/重试。
2. LangGraph 什么时候用：原以为都用→校准为有循环/分支/状态恢复才用，线性用 LCEL。
3. 人在回路怎么实现：原以为只是日志→校准为 interrupt 真能暂停流程等人审批后继续。

**成长对比**：起点（LCEL=语法糖）→ 现在（Runnable接口+LangGraph状态图+生产特性+选型判断）。

</details>

📎 [完整对话记录](_transcript/LCEL与LangGraph.jsonl)

## 视觉模型图
- 打开图：[_viz/LCEL与LangGraph.svg](_viz/LCEL与LangGraph.svg)
- Mermaid 源：[_viz/LCEL与LangGraph.mmd](_viz/LCEL与LangGraph.mmd)

## 📚 参考资料
<details>
<summary>📚 参考资料（点开查看本轮引用来源）</summary>

- **LCEL 文档**（官方文档，2026-06-28）https://python.langchain.com/docs/expression_language/
  - 原话：LCEL 用管道符组合 Runnable，自动支持批处理/异步/流式。
- **LangGraph 文档**（官方文档，2026-06-28）https://langchain-ai.github.io/langgraph/
  - 原话：LangGraph 用状态图编排，支持 checkpoint/人在回路/条件跳转。
- **LangSmith 文档**（官方文档，2026-06-28）https://docs.smith.langchain.com/
  - 原话：LCEL/LangGraph 自动记录到 LangSmith 供调试监控。

</details>

## 🔭 视野拓展 · 行业洞见
<details>
<summary>🔭 视野拓展 · 行业洞见（点开看多维度权威参照）</summary>

### 1. Harrison Chase · LCEL/LangGraph 设计者
- **身份**：LangChain Inc CEO
- **与本概念的关系**：主导 LCEL 和 LangGraph 的设计，从"链"进化到"图"
- **核心洞见**：生产 Agent 需要可控的状态图，不是自由循环；LCEL 让简单事简单，LangGraph 让复杂事可能
- **代表作**：LangChain、LangGraph
- **扩展阅读**：[LangGraph 博客](https://blog.langchain.dev/)

### 2. Eduardo Imhof · LangGraph 核心贡献者
- **身份**：LangChain 工程师
- **与本概念的关系**：LangGraph 的核心实现者，写了大量 LangGraph 教程
- **核心洞见**：状态图是把传统工作流引擎思想引入 LLM 应用的关键
- **代表作**：LangGraph 教程系列
- **扩展阅读**：[LangGraph 示例](https://github.com/langchain-ai/langgraph/tree/main/examples)

### 3. Swyx · 生产级 LLM 工程观察者
- **身份**：Latent Space 主理人
- **与本概念的关系**：系统观察 LLM 应用从 demo 到生产的工程化趋势
- **核心洞见**："AI 工程的核心矛盾是 demo 容易生产难"，LCEL/LangGraph 是解决这个矛盾的框架
- **代表作**：Latent Space 播客
- **扩展阅读**：[latent.space](https://www.latent.space/)

</details>

## 相关
[[LangChain框架]] · [[Agent架构与ReAct模式]] · [[多Agent协作与工作流编排]]
