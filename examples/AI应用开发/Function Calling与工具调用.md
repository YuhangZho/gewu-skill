---
title: Function Calling与工具调用
category: AI应用开发
status: 已完成
track: 标准轨
importance: 5
prereqs: ["ChatGPT API与对话系统"]
groups: ["Agent与工具调用"]
goal_tags: ["求职", "工程"]
aliases: ["Function Calling", "Tool Use", "工具调用"]
tags: ["Function Calling", "JSON Schema", "工具", "Agent基础"]
created: 2026-06-28
related: ["ChatGPT API与对话系统", "Agent架构与ReAct模式", "LangChain框架"]
sources: ["https://platform.openai.com/docs/guides/function-calling", "https://docs.anthropic.com/en/docs/build-with-claude/tool-use", "https://docs.llamaindex.ai/en/stable/agent/"]
viz: "AI应用开发/_viz/Function Calling与工具调用.svg"
viz_source: "AI应用开发/_viz/Function Calling与工具调用.mmd"
viz_chart: "flow"
viz_reason: ""
---

# Function Calling与工具调用

## 一句话定位
> 它属于AI应用开发，是用来解决〔让模型按结构化 JSON 格式输出以调用外部函数〕的——是 LLM 从"聊天"走向"做事"的接口层。

## 🎯 核心收获 · 重点知识

**一句话成果**：学完你现在能定义工具 schema、解析模型返回的函数调用、执行后把结果喂回模型，搭一个能"做事"的 AI。

**重点结论**（7 条）：
1. **Function Calling = 结构化输出+执行钩子**：模型不直接回答，而是返回"我要调用函数 X，参数是 {...}"，应用层解析后执行函数，把结果喂回模型让它生成最终回答。
2. **用 JSON Schema 定义工具**：每个工具声明 name/description/parameters(JSON Schema)，模型据此判断"该不该调用""参数怎么填"。
3. **两段式交互**：① 用户消息+工具定义→模型返回 tool_call（函数名+参数）；② 应用执行函数→把结果作为 tool_result 喂回→模型生成最终回答。
4. **模型不执行，只决策**：模型只决定"调什么、传什么参数"，真正的函数执行在应用层——这是安全边界。
5. **多工具并行**：模型可一次返回多个 tool_call，应用并行执行后全部喂回，减少往返。
6. **工具描述要精准**：description 写不清模型就乱调；要写清"什么时候用""输入是什么""输出是什么"。
7. **是 Agent 的地基**：Agent 本质就是"循环调 Function Calling + 把结果喂回"——ReAct/工具调用都建在这层之上。

**重点知识大纲**：
- Function Calling 机制
  - JSON Schema 定义工具
  - 模型返回 tool_call
  - 应用层执行函数
  - 结果喂回模型
- 两段式交互
  - 第一段：消息+工具定义→tool_call
  - 第二段：tool_result→最终回答
- 关键原则
  - 模型只决策不执行（安全边界）
  - 工具描述要精准
  - 多工具可并行
- 工程要点
  - 参数校验（模型可能传错）
  - 错误处理（函数失败要反馈给模型）
  - 工具版本管理
- Agent 地基
  - 循环调用 = Agent
  - ReAct 建于此之上

## 📝 轻笔记
<details>
<summary>📝 轻笔记（点开看推演摘要与卡壳细节）</summary>

**起点认知**：以为 Function Calling 就是"让模型输出 JSON"，不知道两段式交互和应用层执行这层。

**视觉模型（五问）**：
- 对象：用户消息、工具定义(JSON Schema)、模型、tool_call、应用层、函数实现、tool_result
- 连接：消息+工具定义→模型→tool_call→应用层→函数→tool_result→模型→最终回答
- 流向：两段式循环，第一段决策调用，第二段执行回填
- 边界：模型可能传错参数（要校验）；函数可能失败（要反馈）；模型可能不调用工具（要 fallback）
- 变化：工具数量↑→模型选择难度↑；多 tool_call 并行→应用层要并发执行

**视觉模型结构**：chart_type=flow。用户消息(data)+工具定义(rule)→模型(process)→tool_call(data)→应用层(actor)→函数(process)→tool_result(data)→模型→最终回答(data)。两段循环。

**类比**：模型像餐厅服务员——客人点菜（用户问题），服务员不自己做饭，而是写单子给厨房（tool_call），厨房做好（应用执行函数）服务员端给客人（结果喂回模型生成回答）。服务员只决策"给哪个厨房""点什么"，不亲自做。

**大白话讲解**：它属于AI应用开发，解决怎么让 AI 真能做事而不只是聊天。模型本身不会查数据库、不会发邮件，但它能说"我要调用查数据库函数，参数是 xxx"，你的程序收到后去执行，把结果告诉模型，模型再据此回答。这样 AI 就从"只会说"变成"会做事"。工具描述写清楚是关键，写不清模型就乱调。

**三个应用例子**：
1. 天气查询 bot：模型识别"北京天气"→调用 get_weather("北京")→结果喂回→回答"北京今天 25度晴"。
2. 数据库查询：用户问"本月销售额"→调用 query_db(SQL)→结果→生成分析回答。
3. 多工具 Agent：查日历+发邮件+建任务，模型一次返回 3 个 tool_call 并行执行。

**失效边界**：
- 模型传错参数（如类型错、缺字段）→ 函数报错
- 模型不调用工具直接编答案 → 失去工具价值
- 函数执行超时/失败 → 模型无结果可依据

**边界补丁**：
- 边界1（参数错）→ 应用层用 Pydantic 校验，失败时反馈"参数错误，期望 X"让模型重试
- 边界2（不调工具）→ Prompt 强调"必须用工具"+工具描述写清使用时机
- 边界3（函数失败）→ 捕获异常，把错误信息作为 tool_result 喂回，让模型降级回答

**卡壳点复盘**：
1. 模型怎么知道调哪个工具：原以为是关键词匹配→校准为模型理解工具 description 和参数 schema，靠语义判断。
2. 两段式还是多段：原以为一段就够→校准为至少两段（决策+执行回填），Agent 场景是多段循环。
3. 模型能执行函数吗：原以为模型直接执行→校准为模型只决策不执行，执行在应用层（安全边界）。

**成长对比**：起点（Function Calling=输出JSON）→ 现在（两段式交互+JSON Schema+应用层执行+多工具并行+Agent地基）。

</details>

📎 [完整对话记录](_transcript/Function Calling与工具调用.jsonl)

## 视觉模型图
- 打开图：[_viz/Function Calling与工具调用.svg](_viz/Function Calling与工具调用.svg)
- Mermaid 源：[_viz/Function Calling与工具调用.mmd](_viz/Function Calling与工具调用.mmd)

## 📚 参考资料
<details>
<summary>📚 参考资料（点开查看本轮引用来源）</summary>

- **OpenAI Function Calling Guide**（官方文档，2026-06-28）https://platform.openai.com/docs/guides/function-calling
  - 原话：模型返回 tool_call 含函数名和参数，应用层执行后把结果喂回。
- **Anthropic Tool Use**（官方文档，2026-06-28）https://docs.anthropic.com/en/docs/build-with-claude/tool-use
  - 原话：Claude 的 tool_use 同样是两段式交互。
- **LlamaIndex Agent 文档**（官方文档，2026-06-28）https://docs.llamaindex.ai/en/stable/agent/
  - 原话：Agent 建立在 Function Calling 之上。

</details>

## 🔭 视野拓展 · 行业洞见
<details>
<summary>🔭 视野拓展 · 行业洞见（点开看多维度权威参照）</summary>

### 1. Shreya Rajpal · Guardrails AI / 工具调用工程化
- **身份**：Guardrails AI 创始人
- **与本概念的关系**：专注 LLM 结构化输出和工具调用的可靠性
- **核心洞见**：模型输出不可靠，工具调用的参数校验和错误处理是生产应用的第一道防线
- **代表作**：Guardrails AI 框架
- **扩展阅读**：[Guardrails AI GitHub](https://github.com/guardrails-ai/guardrails)

### 2. Yao Shunyu · ReAct 论文作者
- **身份**：普林斯顿大学研究员
- **与本概念的关系**：ReAct 框架把 Function Calling 升级成"思考+行动"循环，是 Agent 的理论基础
- **核心洞见**：工具调用不是孤立的，要和推理交织——模型边想边调工具边根据结果再想
- **代表作**：*ReAct: Synergizing Reasoning and Acting in Language Models*
- **扩展阅读**：[arXiv 论文](https://arxiv.org/abs/2210.03629)

### 3. Swyx · 工具调用生态观察
- **身份**：Latent Space 主理人、AI 工程布道者
- **与本概念的关系**：系统观察 Function Calling 从 OpenAI 到全行业的标准化过程
- **核心洞见**：Function Calling 是 LLM 从"聊天接口"变成"应用编排接口"的转折点
- **代表作**：Latent Space 播客
- **扩展阅读**：[latent.space](https://www.latent.space/)

</details>

## 相关
[[ChatGPT API与对话系统]] · [[Agent架构与ReAct模式]] · [[LangChain框架]] · [[多Agent协作与工作流编排]]
