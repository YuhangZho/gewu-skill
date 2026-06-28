---
title: AI应用评估与可观测性
category: AI应用开发
status: 已完成
track: 标准轨
importance: 4
prereqs: ["RAG基础架构", "Agent架构与ReAct模式"]
groups: ["部署与评估"]
goal_tags: ["求职", "工程"]
aliases: ["Evaluation", "Observability", "LLM监控"]
tags: ["评估", "RAGAS", "可观测性", "漂移", "监控"]
created: 2026-06-28
related: ["RAG基础架构", "高级RAG技术", "Agent架构与ReAct模式", "API服务与FastAPI"]
sources: ["https://docs.ragas.io/", "https://docs.smith.langchain.com/", "https://www.phoenix.arize.com/"]
viz: "AI应用开发/_viz/AI应用评估与可观测性.svg"
viz_source: "AI应用开发/_viz/AI应用评估与可观测性.mmd"
viz_chart: "hierarchy"
viz_reason: ""
---

# AI应用评估与可观测性

## 一句话定位
> 它属于AI应用开发，是用来解决〔评估指标 + 线上监控〕的——让 AI 应用可度量可维护。

## 🎯 核心收获 · 重点知识

**一句话成果**：学完你现在能为 RAG/Agent 应用设计评估指标（离线）+ 线上监控（漂移/成本/延迟/质量），让 AI 应用"可度量可维护"。

**重点结论**（7 条）：
1. **AI 应用必须评估+监控**：传统软件测 pass/fail，AI 应用输出概率性，要用指标量化质量，线上还要监控漂移。
2. **RAG 评估三维度（RAGAS）**：① 生成质量（faithfulness 答案有没有依据/relevance 相关性）；② 检索质量（context_recall 召回/context_precision 精度）；③ 端到端（answer_correctness）。
3. **Agent 评估**：任务成功率、步数（效率）、工具调用准确率、token 消耗、是否跑偏/死循环。
4. **线上监控四要素**：① 质量监控（用 LLM as judge 实时评）；② 成本监控（token/费用告警）；③ 延迟监控（首 token/总时间）；④ 漂移监控（输入分布/输出分布变化）。
5. **黄金数据集**：离线评估要用人工标注的黄金集回归测试，每次改 Prompt/换模型都跑，防止改坏。
6. **LLM as Judge**：用强模型评弱模型输出，是 AI 评估的常用手段，但有偏差要校准。
7. **工具栈**：RAGAS（RAG 评估）/ LangSmith / Phoenix（Arize）/ Langfuse（开源可观测），按场景选。

**重点知识大纲**：
- 为什么 AI 要评估
  - 输出概率性
  - 不能 pass/fail
  - 要量化质量
- RAG 评估（RAGAS）
  - 生成：faithfulness/relevance
  - 检索：context_recall/precision
  - 端到端：answer_correctness
- Agent 评估
  - 任务成功率
  - 步数/效率
  - 工具调用准确率
- 线上监控
  - 质量监控（LLM as judge）
  - 成本监控（token 告警）
  - 延迟监控（首token/总）
  - 漂移监控（分布变化）
- 黄金数据集
  - 人工标注
  - 回归测试
- 工具栈
  - RAGAS / LangSmith / Phoenix / Langfuse

## 📝 轻笔记
<details>
<summary>📝 轻笔记（点开看推演摘要与卡壳细节）</summary>

**起点认知**：以为 AI 应用"能用就行"，不知道评估指标和线上监控这套体系。

**视觉模型（五问）**：
- 对象：黄金数据集、评估指标、LLM as judge、线上日志、监控仪表盘、告警
- 连接：离线评估（黄金集→指标→报告）；线上监控（请求→日志→指标→告警）
- 流向：离线评估驱动迭代，线上监控保稳定
- 边界：LLM as judge 有偏差；漂移检测滞后；评估成本高
- 变化：模型/Prompt 变→重跑评估；线上分布变→漂移告警

**视觉模型结构**：chart_type=hierarchy。评估与可观测性(concept)→[离线评估(指标/黄金集)/线上监控(质量/成本/延迟/漂移)/工具栈]。

**类比**：像给 AI 应用配体检+监护仪——离线评估是定期体检（黄金集查健康），线上监控是 ICU 监护仪（实时盯生命体征）。没这两套，AI 应用上线就是黑盒瞎跑。

**大白话讲解**：它属于AI应用开发，解决怎么知道 AI 应用好不好、坏没坏。AI 输出不是对错而是好坏，所以要量化评估：RAG 用 RAGAS 量检索准不准、答得有没有依据；Agent 量任务成功率。上线后还要实时盯——成本别爆、延迟别太长、用户输入分布变了要发现（漂移）。就像传统软件要测试+监控，AI 应用要评估+可观测。

**三个应用例子**：
1. RAG 上线前：用 100 条黄金问题跑 RAGAS，faithfulness 要 > 0.9 才发布。
2. Agent 监控：步数突增告警（可能死循环），成本突增告警（可能被刷）。
3. 模型升级回归：换 GPT-4o-mini 前跑黄金集，确认指标不降才切。

**失效边界**：
- LLM as judge 有偏差（评自己更宽容）
- 漂移检测滞后（要积累数据才发现）
- 评估成本高（用 GPT-4 评贵）

**边界补丁**：
- 边界1（judge 偏差）→ 用不同模型族 judge + 人工抽查校准
- 边界2（漂移滞后）→ 缩短窗口+主动监控关键词分布
- 边界3（成本）→ 抽样评估+用小模型 judge

**卡壳点复盘**：
1. RAG 怎么评：原以为看回答顺不顺→校准为 RAGAS 四指标（检索召回/精度+生成 faithfulness/relevance）。
2. 线上监控盯什么：原以为只看错误率→校准为质量+成本+延迟+漂移四要素。
3. LLM as judge 可信吗：原以为完全可信→校准为有偏差要校准，评自己更宽容。

**成长对比**：起点（AI能用就行）→ 现在（RAGAS指标+Agent评估+线上四要素监控+黄金集回归）。

</details>

📎 [完整对话记录](_transcript/AI应用评估与可观测性.jsonl)

## 视觉模型图
- 打开图：[_viz/AI应用评估与可观测性.svg](_viz/AI应用评估与可观测性.svg)
- Mermaid 源：[_viz/AI应用评估与可观测性.mmd](_viz/AI应用评估与可观测性.mmd)

## 📚 参考资料
<details>
<summary>📚 参考资料</summary>

- **RAGAS 文档**（官方，2026-06-28）https://docs.ragas.io/
  - 原话：RAGAS 提供 faithfulness/relevance/context_recall/precision 四指标。
- **LangSmith 文档**（官方，2026-06-28）https://docs.smith.langchain.com/
  - 原话：LangSmith 提供 LLM 应用的调试/监控/评估。
- **Arize Phoenix**（开源，2026-06-28）https://www.phoenix.arize.com/
  - 原话：开源 LLM 可观测性工具。

</details>

## 🔭 视野拓展 · 行业洞见
<details>
<summary>🔭 视野拓展 · 行业洞见（点开看多维度权威参照）</summary>

### 1. Shahul Es · RAGAS 作者
- **身份**：RAGAS 维护者
- **与本概念的关系**：RAGAS 是 RAG 评估的事实标准
- **核心洞见**：RAG 优化必须评估驱动，没指标就是盲调
- **代表作**：RAGAS
- **扩展阅读**：[RAGAS 文档](https://docs.ragas.io/)

### 2. Harrison Chase · LangSmith 设计者
- **身份**：LangChain Inc CEO
- **与本概念的关系**：LangSmith 把 LLM 应用的调试/监控/评估一体化
- **核心洞见**：LLM 应用的可观测性比传统软件更重要，因为输出不确定
- **代表作**：LangSmith
- **扩展阅读**：[LangSmith 文档](https://docs.smith.langchain.com/)

### 3. Jason Lopatecki · Arize AI 创始人
- **身份**：Arize AI 创始人
- **与本概念的关系**：Phoenix 是开源 LLM 可观测性工具，专注漂移和质量监控
- **核心洞见**：LLM 应用的漂移和质量监控要借鉴传统 ML 的可观测性经验
- **代表作**：Arize Phoenix
- **扩展阅读**：[Phoenix GitHub](https://github.com/Arize-ai/phoenix)

</details>

## 相关
[[RAG基础架构]] · [[高级RAG技术]] · [[Agent架构与ReAct模式]] · [[API服务与FastAPI]]
