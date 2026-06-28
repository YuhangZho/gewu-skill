---
title: 多Agent协作与工作流编排
category: AI应用开发
status: 已完成
track: 标准轨
importance: 4
prereqs: ["Agent架构与ReAct模式"]
groups: ["Agent与工具调用"]
goal_tags: ["求职", "工程"]
aliases: ["Multi-Agent", "LangGraph", "Agent编排"]
tags: ["多Agent", "LangGraph", "工作流", "状态机", "人在回路"]
created: 2026-06-28
related: ["Agent架构与ReAct模式", "LCEL与LangGraph", "LangChain框架", "AI应用评估与可观测性"]
sources: ["https://langchain-ai.github.io/langgraph/", "https://arxiv.org/abs/2308.08155", "https://docs.crewai.com/"]
viz: "AI应用开发/_viz/多Agent协作与工作流编排.svg"
viz_source: "AI应用开发/_viz/多Agent协作与工作流编排.mmd"
viz_chart: "flow"
viz_reason: ""
---

# 多Agent协作与工作流编排

## 一句话定位
> 它属于AI应用开发，是用来解决〔用 LangGraph 等编排多智能体有状态协作〕的——解决复杂业务流程的自动化。

## 🎯 核心收获 · 重点知识

**一句话成果**：学完你现在能设计多 Agent 协作流程（分工/通信/状态管理），用 LangGraph 实现有状态工作流和人在回路。

**重点结论**（7 条）：
1. **单 Agent 搞不定复杂任务**：任务复杂时单 Agent 上下文爆炸/工具过多/跑偏；拆成多 Agent 各司其职更可靠。
2. **协作模式**：① 串行（A 做完给 B）；② 并行（A/B 同时做不同部分再合并）；③ 主管-工人（Supervisor 分派给 Worker）；④ 辩论（多 Agent 观点对抗再裁决）。
3. **LangGraph = 状态图**：把 Agent 协作建模成有向图，节点=Agent/函数，边=条件跳转，状态=共享 dict。比纯 ReAct 更可控。
4. **状态管理是核心**：多 Agent 要共享状态（如任务进度/中间产物），LangGraph 用 shared state + checkpoint 实现持久化和恢复。
5. **人在回路（Human-in-the-loop）**：关键节点加人工审批（如发邮件前确认/Agent 不确定时求助），LangGraph 用 interrupt 实现。
6. **通信机制**：① 共享状态（简单但耦合）；② 消息传递（解耦但复杂）；③ 黑板模式（共享工作区）。
7. **可靠性工程**：超时/死锁/Agent 失败都要处理；用 checkpoint 恢复 + 重试 + 降级；监控每个 Agent 的成功率。

**重点知识大纲**：
- 为什么需要多 Agent
  - 单 Agent 上下文爆炸
  - 工具过多跑偏
  - 拆分各司其职
- 协作模式
  - 串行（流水线）
  - 并行（分治合并）
  - 主管-工人（Supervisor）
  - 辩论（对抗裁决）
- LangGraph 核心
  - 状态图（节点+边+条件）
  - 共享状态
  - Checkpoint 持久化
- 人在回路
  - 关键节点人工审批
  - interrupt 机制
  - 不确定时求助
- 通信机制
  - 共享状态
  - 消息传递
  - 黑板模式
- 可靠性
  - 超时/死锁/失败处理
  - Checkpoint 恢复
  - 监控成功率

## 📝 轻笔记
<details>
<summary>📝 轻笔记（点开看推演摘要与卡壳细节）</summary>

**起点认知**：以为多 Agent 就是"多个 Agent 串联"，不知道协作模式和状态管理这层。

**视觉模型（五问）**：
- 对象：多个 Agent、Supervisor、共享状态、消息、Checkpoint、人工审批节点
- 连接：Supervisor→分派→Workers→结果回 Supervisor；或 A→B→C 串行；或 A/B 并行→合并
- 流向：取决于协作模式（串行/并行/主管-工人）
- 边界：Agent 间通信延迟；死锁（互相等待）；状态一致性
- 变化：任务进度更新共享状态→驱动流程推进

**视觉模型结构**：chart_type=flow。Supervisor(actor)→分派→Worker1/Worker2(process)→结果→合并(process)→人工审批(boundary)→输出(data)。体现主管-工人+人在回路。

**类比**：像项目组——单 Agent 是一个人从头干到尾，多 Agent 是有项目经理（Supervisor）分派给开发/测试/设计（Workers），关键决策点找老板审批（人在回路），用 Jira（共享状态）跟踪进度。

**大白话讲解**：它属于AI应用开发，解决怎么让多个 AI 协作干复杂活。一个 AI 啥都干容易乱，拆成几个各管一摊——比如写报告：一个负责查资料，一个负责写初稿，一个负责审校，像项目组分工。用 LangGraph 这种工具编排流程，能管状态、能暂停让人确认、能出错恢复。

**三个应用例子**：
1. 内容生产：调研Agent→写作Agent→审校Agent 串行，审校不满意回退重写。
2. 客服系统：分类Agent→路由→技术/售后/投诉Agent，Supervisor 协调。
3. 代码审查：多个 Agent 不同视角审（安全/性能/风格）→合并报告。

**失效边界**：
- Agent 间通信开销大（多个 LLM 调用成本叠加）
- 死锁（A 等 B，B 等 A）
- 状态不一致（并发写共享状态）

**边界补丁**：
- 边界1（成本叠加）→ 简单任务别拆，用单 Agent；关键节点才多 Agent
- 边界2（死锁）→ 设超时 + 强制推进
- 边界3（状态不一致）→ 用 LangGraph 的状态图保证顺序

**卡壳点复盘**：
1. 多 Agent 什么时候值：原以为越多越好→校准为复杂任务才值，简单任务单 Agent 更省。
2. LangGraph 和 LangChain 区别：原以为一样→校准为 LangChain 是链式（线性），LangGraph 是图（有环/条件/状态），更适合 Agent。
3. 人在回路怎么实现：原以为只是日志→校准为 LangGraph 的 interrupt 能真暂停流程等人审批后继续。

**成长对比**：起点（多Agent=串联）→ 现在（四种协作模式+LangGraph状态图+人在回路+可靠性工程）。

</details>

📎 [完整对话记录](_transcript/多Agent协作与工作流编排.jsonl)

## 视觉模型图
- 打开图：[_viz/多Agent协作与工作流编排.svg](_viz/多Agent协作与工作流编排.svg)
- Mermaid 源：[_viz/多Agent协作与工作流编排.mmd](_viz/多Agent协作与工作流编排.mmd)

## 📚 参考资料
<details>
<summary>📚 参考资料（点开查看本轮引用来源）</summary>

- **LangGraph 官方文档**（官方文档，2026-06-28）https://langchain-ai.github.io/langgraph/
  - 原话：LangGraph 用状态图编排 Agent，支持 checkpoint/人在回路/条件跳转。
- **Multi-Agent 论文**（arXiv，2026-06-28）https://arxiv.org/abs/2308.08155
  - 原话：多 Agent 协作模式（串行/并行/主管-工人/辩论）的系统分析。
- **CrewAI 文档**（官方文档，2026-06-28）https://docs.crewai.com/
  - 原话：CrewAI 是角色化的多 Agent 框架。

</details>

## 🔭 视野拓展 · 行业洞见
<details>
<summary>🔭 视野拓展 · 行业洞见（点开看多维度权威参照）</summary>

### 1. Harrison Chase · LangGraph 创始人
- **身份**：LangChain Inc CEO
- **与本概念的关系**：LangGraph 是多 Agent 编排的事实标准，他定义了状态图+人在回路的范式
- **核心洞见**：生产 Agent 的可靠性来自可控的状态图，不是自由循环
- **代表作**：LangGraph
- **扩展阅读**：[LangGraph 文档](https://langchain-ai.github.io/langgraph/)

### 2. Michael Wooldridge · 多 Agent 系统理论权威
- **身份**：牛津大学计算机教授
- **与本概念的关系**：多 Agent 系统（MAS）的理论奠基者，把传统 MAS 理论和 LLM Agent 结合
- **核心洞见**：多 Agent 协作的核心是"协调"——通信/协商/冲突解决，理论早就有，LLM 让它落地
- **代表作**：*An Introduction to MultiAgent Systems*
- **扩展阅读**：[牛津主页](https://www.cs.ox.ac.uk/people/michael.wooldridge/)

### 3. Yohei Nakajima · BabyAGI / 多 Agent 实践者
- **身份**：OurCrowd 风投、BabyAGI 作者
- **与本概念的关系**：BabyAGI 是最早的自治多 Agent 任务管理原型，启发了一大批 Agent 框架
- **核心洞见**：多 Agent 的价值在"自主分解+委派+反思"，但要靠工程护栏防止失控
- **代表作**：BabyAGI
- **扩展阅读**：[BabyAGI GitHub](https://github.com/yoheinakajima/babyagi)

</details>

## 相关
[[Agent架构与ReAct模式]] · [[LCEL与LangGraph]] · [[LangChain框架]] · [[AI应用评估与可观测性]]
