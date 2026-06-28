---
title: Agent架构与ReAct模式
category: AI应用开发
status: 已完成
track: 标准轨
importance: 5
prereqs: ["Function Calling与工具调用", "Prompt工程基础"]
groups: ["Agent与工具调用"]
goal_tags: ["求职", "工程"]
aliases: ["Agent", "ReAct", "智能体"]
tags: ["Agent", "ReAct", "思考-行动-观察", "自主决策"]
created: 2026-06-28
related: ["Function Calling与工具调用", "Prompt工程基础", "多Agent协作与工作流编排", "LangChain框架", "LCEL与LangGraph"]
sources: ["https://arxiv.org/abs/2210.03629", "https://python.langchain.com/docs/modules/agents/", "https://lilianweng.github.io/posts/2023-06-23-agent/"]
viz: "AI应用开发/_viz/Agent架构与ReAct模式.svg"
viz_source: "AI应用开发/_viz/Agent架构与ReAct模式.mmd"
viz_chart: "cycle"
viz_reason: ""
---

# Agent架构与ReAct模式

## 一句话定位
> 它属于AI应用开发，是用来解决〔思考-行动-观察的自主决策循环〕的——让模型能规划、调工具、纠错地完成多步任务。

## 🎯 核心收获 · 重点知识

**一句话成果**：学完你现在能设计一个 ReAct Agent：定义工具集、写 system prompt 设定角色、实现 Thought-Action-Observation 循环、处理停止条件。

**重点结论**（7 条）：
1. **Agent = LLM + 工具 + 循环**：模型自主决定"下一步做什么"（调工具/回答/继续思考），循环直到完成。和单次 Function Calling 的区别是"自主决策+多步"。
2. **ReAct = Reasoning + Acting**：每步先 Thought（思考当前状态和下一步）→ Action（调工具）→ Observation（看工具结果）→ 再 Thought。思考让行动有依据，行动让思考有新信息。
3. **System Prompt 定义 Agent 人格**：角色（你是 XX 助手）+ 目标（帮用户完成 X）+ 约束（只用这些工具/最多 N 步/什么情况停止）+ 工具说明。
4. **停止条件**：任务完成（模型说"Final Answer"）+ 达到最大步数（防死循环）+ 工具连续失败 + 用户中断。
5. **记忆与状态**：短期=当前对话/工具历史；长期=向量库存过往交互；状态管理决定 Agent 能否处理复杂任务。
6. **规划能力是关键**：复杂任务 Agent 要先"拆解计划"再逐步执行，Plan-and-Execute 模式比纯 ReAct 更适合长任务。
7. **Agent 可靠性挑战**：循环可能死循环/跑偏/调错工具；生产 Agent 要加护栏（步数限制/工具白名单/结果校验/人工介入）。

**重点知识大纲**：
- Agent 本质
  - LLM + 工具 + 自主循环
  - vs 单次 Function Calling = 多步自主
- ReAct 循环
  - Thought（思考）
  - Action（调工具）
  - Observation（看结果）
  - 循环直到 Final Answer
- System Prompt 设计
  - 角色 + 目标 + 约束 + 工具
- 停止条件
  - Final Answer
  - 最大步数
  - 连续失败
  - 用户中断
- 记忆与状态
  - 短期（对话历史）
  - 长期（向量库）
  - 规划（Plan-and-Execute）
- 可靠性工程
  - 步数限制
  - 工具白名单
  - 结果校验
  - 人工介入

## 📝 轻笔记
<details>
<summary>📝 轻笔记（点开看推演摘要与卡壳细节）</summary>

**起点认知**：以为 Agent 就是"让模型调用工具"，不知道 ReAct 的思考-行动-观察循环和自主决策这层。

**视觉模型（五问）**：
- 对象：用户目标、System Prompt、LLM、工具集、Thought、Action、Observation、Final Answer
- 连接：目标→System Prompt→LLM→Thought→Action→工具→Observation→LLM→Thought...→Final Answer
- 流向：循环（Thought-Action-Observation 重复），最终 Final Answer 退出
- 边界：步数上限防死循环；工具失败要降级；模型可能跑偏需要护栏
- 变化：每步 Observation 改变状态→下一步 Thought 据此调整

**视觉模型结构**：chart_type=cycle（ReAct 是循环）。Thought(process)→Action(process)→Observation(data)→回到 Thought，循环 N 次直到 Final Answer(data)退出。

**类比**：Agent 像有个实习生——你给目标"帮我订下周去上海的机票"，他自己想：先查日历（Thought）→调日历工具（Action）→看到下周三有空（Observation）→再想查航班→调航班工具→看到 3 班→再想选最便宜的→调预订→完成。每步思考让行动有依据。

**大白话讲解**：它属于AI应用开发，解决怎么让 AI 自己完成多步任务。普通 AI 你问一句答一句，Agent 会自己想"要完成这事得先做 X 再做 Y"，然后调工具一步步来，遇到结果还会调整计划。核心是"想-做-看"循环：先想下一步做什么，做（调工具），看结果，再想。就像派个实习生去办事，他不会一步到位，而是一步步摸索着完成。

**三个应用例子**：
1. 研究助手：用户问"对比 A/B 两款产品"→Agent 搜 A→搜 B→整理对比表→回答。
2. 代码助手：用户说"修这个 bug"→Agent 读代码→定位→改→跑测试→报告。
3. 旅行规划：用户说"规划 3 天上海行"→Agent 查景点→查天气→排日程→输出行程。

**失效边界**：
- 死循环（模型反复调同工具）
- 跑偏（工具结果误导，越走越远）
- 工具失败连锁（一个失败导致后续全错）

**边界补丁**：
- 边界1（死循环）→ 最大步数 + 检测重复 Action 强制停止
- 边界2（跑偏）→ System Prompt 强约束 + 关键步人工确认
- 边界3（工具失败）→ 重试 + 降级 + 反馈给模型让其换方案

**卡壳点复盘**：
1. Agent 和 Function Calling 区别：原以为一样→校准为 Function Calling 是单次，Agent 是多步自主循环。
2. ReAct 为什么有效：原以为就是"调工具"→校准为 Thought 让模型显式推理，行动有依据，比直接调工具更准。
3. 什么时候用 Agent：原以为都用→校准为简单任务用 Chain（固定流程），复杂/不确定流程才用 Agent（自主决策）。

**成长对比**：起点（Agent=调工具）→ 现在（ReAct循环+System Prompt设计+停止条件+记忆规划+可靠性工程）。

</details>

📎 [完整对话记录](_transcript/Agent架构与ReAct模式.jsonl)

## 视觉模型图
- 打开图：[_viz/Agent架构与ReAct模式.svg](_viz/Agent架构与ReAct模式.svg)
- Mermaid 源：[_viz/Agent架构与ReAct模式.mmd](_viz/Agent架构与ReAct模式.mmd)

## 📚 参考资料
<details>
<summary>📚 参考资料（点开查看本轮引用来源）</summary>

- **ReAct 论文**（arXiv，2026-06-28）https://arxiv.org/abs/2210.03629
  - 原话："synergize reasoning and acting"——思考和行动交织提升效果。
- **LangChain Agents 文档**（官方文档，2026-06-28）https://python.langchain.com/docs/modules/agents/
  - 原话：Agent = LLM + 工具 + 循环，ReAct 是主流模式。
- **Lilian Weng LLM Agent 综述**（博客，2026-06-28）https://lilianweng.github.io/posts/2023-06-23-agent/
  - 原话：Agent 的核心是规划+记忆+工具+行动。

</details>

## 🔭 视野拓展 · 行业洞见
<details>
<summary>🔭 视野拓展 · 行业洞见（点开看多维度权威参照）</summary>

### 1. Yao Shunyu · ReAct 论文作者
- **身份**：普林斯顿大学研究员
- **与本概念的关系**：ReAct 框架的提出者，奠定 Thought-Action-Observation 循环
- **核心洞见**：纯推理（CoT）会幻觉，纯行动（工具调用）无规划，ReAct 让两者协同
- **代表作**：*ReAct: Synergizing Reasoning and Acting in Language Models*
- **扩展阅读**：[arXiv 论文](https://arxiv.org/abs/2210.03629)

### 2. Lilian Weng · Agent 综述权威
- **身份**：OpenAI 研究主管
- **与本概念的关系**：写了最被引用的 LLM Agent 综述，系统梳理规划/记忆/工具/行动四要素
- **核心洞见**：Agent = 规划 + 记忆 + 工具 + 行动，缺一不可
- **代表作**：*LLM Powered Autonomous Agents* 博客
- **扩展阅读**：[Lilian Weng Blog](https://lilianweng.github.io/posts/2023-06-23-agent/)

### 3. Harrison Chase · LangChain/LangGraph 创始人
- **身份**：LangChain Inc CEO
- **与本概念的关系**：LangChain/LangGraph 是 Agent 工程化的事实标准框架
- **核心洞见**：Agent 的可靠性是工程问题，要靠框架提供状态管理/检查点/人工介入
- **代表作**：LangChain、LangGraph
- **扩展阅读**：[LangGraph 文档](https://langchain-ai.github.io/langgraph/)

</details>

## 相关
[[Function Calling与工具调用]] · [[Prompt工程基础]] · [[多Agent协作与工作流编排]] · [[LangChain框架]] · [[LCEL与LangGraph]]
