---
title: Prompt工程基础
category: AI应用开发
status: 已完成
track: 标准轨
importance: 5
prereqs: ["LLM工作原理与Token机制"]
groups: ["LLM基础认知"]
goal_tags: ["求职", "工程"]
aliases: ["Prompt Engineering", "提示工程"]
tags: ["Prompt", "Few-shot", "CoT", "结构化输出"]
created: 2026-06-28
related: ["LLM工作原理与Token机制", "ChatGPT API与对话系统", "Agent架构与ReAct模式"]
sources: ["https://platform.openai.com/docs/guides/prompt-engineering", "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering", "https://learnprompting.org/"]
viz: "AI应用开发/_viz/Prompt工程基础.svg"
viz_source: "AI应用开发/_viz/Prompt工程基础.mmd"
viz_chart: "hierarchy"
viz_reason: ""
---

# Prompt工程基础

## 一句话定位
> 它属于AI应用开发，是用来解决〔如何构造提示词让模型稳定产出预期结果〕的——含角色设定、Few-shot、CoT等核心技法，是所有 LLM 应用的"接口层"。

## 🎯 核心收获 · 重点知识

**一句话成果**：学完你现在能针对不同任务设计稳定的 Prompt（角色+指令+上下文+示例+输出格式），并在模型输出不稳定时知道调哪个维度。

**重点结论**（7 条）：
1. **Prompt 五要素**：角色（你是谁）+ 指令（做什么）+ 上下文（背景/输入）+ 示例（Few-shot）+ 输出格式（JSON/Markdown/Schema）。前两个必填，后三个按任务配。
2. **Zero-shot vs Few-shot**：Few-shot 用示例"演示"期望映射，比纯指令更稳；但示例会吃 token 且可能过拟合到示例风格。复杂任务用 Few-shot，简单分类用 Zero-shot。
3. **CoT（Chain-of-Thought）**：让模型"先思考再回答"，"Let's think step by step"一句能显著提升推理任务准确率；但会增输出 token 成本。适合数学/逻辑/多步推理，不适合简单事实。
4. **结构化输出靠指令+Schema**：要求 JSON 时给完整 schema + 示例，比"返回 JSON"稳得多；用 `response_format`（OpenAI）或 XML 标签（Anthropic）能强制结构化。
5. **Prompt 越具体越稳**：模糊指令（"总结一下"）→ 不可控；具体指令（"用3句话，面向产品经理，突出用户痛点和解决方案"）→ 稳定。
6. **负向指令弱于正向**：模型对"不要做X"理解弱，改写成"只做Y"更有效。
7. **Prompt 是应用的核心资产**：线上应用的 Prompt 要版本管理、A/B 测试、回归测试，像代码一样对待。

**重点知识大纲**：
- Prompt 五要素
  - 角色（系统消息设定身份）
  - 指令（任务动词+约束）
  - 上下文（输入数据/背景）
  - 示例（Few-shot 演示映射）
  - 输出格式（Schema/格式约束）
- 技法分层
  - Zero-shot（纯指令）
  - Few-shot（示例演示）
  - CoT（思维链推理）
  - Self-Consistency（多次采样取众数）
  - Prompt Chaining（拆步串联）
- 结构化输出
  - JSON Schema 约束
  - response_format / XML 标签
  - Function Calling 强制结构
- 稳定性工程
  - 具体 > 模糊
  - 正向 > 负向
  - 版本管理 + A/B + 回归测试

## 📝 轻笔记
<details>
<summary>📝 轻笔记（点开看推演摘要与卡壳细节）</summary>

**起点认知**：以为 Prompt 就是"把话说清楚"，加点角色设定就行；Few-shot 听过但不知道什么时候用。

**视觉模型（五问）**：
- 对象：System Message（角色）、User Message（指令+上下文）、Examples（Few-shot）、Output Schema、模型输出
- 连接：System 定基调 → User 给任务 → Examples 演示映射 → Schema 约束输出 → 模型生成
- 流向：线性构造，但 Examples 和 Schema 是"约束边"，不是数据流
- 边界：模型能力上限决定 Prompt 上限；Prompt 修不好模型本身的幻觉；超长 Few-shot 吃 context
- 变化：任务复杂度↑ → 需要的技法↑（Zero-shot→Few-shot→CoT→Chaining）

**视觉模型结构**：chart_type=hierarchy（Prompt 五要素的组成结构）。节点：Prompt(concept)→[角色/指令/上下文/示例/输出格式](各 rule/concept)，示例下挂 Few-shot(process)，输出格式下挂 Schema(rule)。

**类比**：像给新员工的 task brief——角色=工种，指令=任务清单，上下文=项目背景，示例=参考样例，输出格式=交付模板。brief 越完整，交付越符合预期。

**大白话讲解**：它属于AI应用开发，解决怎么让 AI 稳定按你想要的来。就像给新来的同事布置活：你得说清"你是谁（角色）、做什么（指令）、背景是什么（上下文）、给个参考（示例）、要什么格式（输出）"。说得越具体，AI 越不会跑偏。复杂任务还得让它"先想想再答"（思维链），就像让新人先写思路再写答案。

**三个应用例子**：
1. 客服分类：Few-shot 给 5 个对话→标签的示例，比纯指令准确率高 15%。
2. 数学解题：加"Let's think step by step"（CoT），GPT-4 数学 benchmark 提升显著。
3. 数据抽取：给 JSON Schema + 1 个示例，结构化输出成功率从 70%→98%。

**失效边界**：
- 模型本身能力不足时，Prompt 再精巧也救不回（如让小模型做复杂推理）
- Few-shot 示例有偏差时，模型会放大偏差（过拟合示例风格）
- CoT 对简单事实任务反而增加成本无收益

**边界补丁**：
- 边界1（模型能力不足）→ 换更大模型或拆成更简单子任务
- 边界2（Few-shot 过拟合）→ 示例要多样化、覆盖边界情况，数量 3-5 个够
- 边界3（CoT 滥用）→ 只在推理任务用，事实类用 Zero-shot

**卡壳点复盘**：
1. Few-shot 示例数量：原以为越多越好→校准为 3-5 个最佳，太多吃 context 且过拟合。
2. CoT 为什么有效：原以为是"让模型想"→校准为是激活了模型训练时见过的推理模式，且分步生成让每步 attention 更聚焦。
3. 结构化输出不稳定：原以为加"返回JSON"就够→校准为必须给完整 Schema + 示例，最好用 response_format 强制。

**成长对比**：起点（Prompt=说清楚话）→ 现在（五要素框架+技法分层+稳定性工程，知道什么任务用什么技法、为什么不稳怎么调）。

</details>

📎 [完整对话记录](_transcript/Prompt工程基础.jsonl)

## 视觉模型图
- 打开图：[_viz/Prompt工程基础.svg](_viz/Prompt工程基础.svg)
- Mermaid 源：[_viz/Prompt工程基础.mmd](_viz/Prompt工程基础.mmd)

## 📚 参考资料
<details>
<summary>📚 参考资料（点开查看本轮引用来源）</summary>

- **OpenAI Prompt Engineering Guide**（官方文档，2026-06-28）https://platform.openai.com/docs/guides/prompt-engineering
  - 原话："Be specific, descriptive and as detailed as possible about the desired context, outcome, length, format, style."
- **Anthropic Prompt Engineering**（官方文档，2026-06-28）https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering
  - 原话：用 XML 标签分隔 prompt 结构（`<context>`、`<example>`），模型对标签结构敏感。
- **Learn Prompting**（开源教程，2026-06-28）https://learnprompting.org/
  - 系统化 Prompt 工程从入门到进阶。

</details>

## 🔭 视野拓展 · 行业洞见
<details>
<summary>🔭 视野拓展 · 行业洞见（点开看多维度权威参照）</summary>

### 1. Jason Wei · CoT 论文一作
- **身份**：OpenAI 研究员
- **与本概念的关系**：首次系统验证"Chain-of-Thought prompting"能显著提升大模型推理能力
- **核心洞见**："Chain-of-thought prompting elicits reasoning in large language models"——一句"let's think step by step"激活了模型的分步推理能力（ACL 2022）
- **代表作**：*Chain-of-Thought Prompting Elicits Reasoning in LLMs*
- **扩展阅读**：[arXiv 论文](https://arxiv.org/abs/2201.11903)

### 2. Lilian Weng · Prompt 工程系统综述作者
- **身份**：OpenAI 研究主管
- **与本概念的关系**：写了最被引用的 Prompt Engineering 综述博客，系统梳理 Zero/Few-shot/CoT/Self-Consistency 等技法
- **核心洞见**：把 Prompt 工程定位为"用自然语言编程"——Prompt 就是给模型的"程序"，稳定性工程一样要做
- **代表作**：*Prompt Engineering* 博客（Lilian Weng 个人博客）
- **扩展阅读**：[Lilian Weng Blog](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)

### 3. Eugene Yan · 应用工程视角
- **身份**：应用机器学习工程师、技术博主
- **与本概念的关系**：从工程实践角度讲 Prompt 的评估、A/B 测试、回归测试
- **核心洞见**：Prompt 是产品资产，要像代码一样版本管理+测试，不是"调到能用就完事"
- **代表作**：*Evaluating LLM Applications* 系列博客
- **扩展阅读**：[eugeneyan.com](https://eugeneyan.com/)

</details>

## 相关
[[LLM工作原理与Token机制]] · [[ChatGPT API与对话系统]] · [[Agent架构与ReAct模式]] · [[RAG基础架构]]
