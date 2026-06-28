---
title: AI应用作品集项目
category: AI应用开发
status: 已完成
track: 标准轨
importance: 5
prereqs: ["RAG基础架构", "Agent架构与ReAct模式", "LangChain框架"]
groups: ["作品集与落地"]
goal_tags: ["求职", "工程"]
aliases: ["Portfolio", "作品集"]
tags: ["作品集", "项目", "简历", "面试"]
created: 2026-06-28
related: ["RAG基础架构", "Agent架构与ReAct模式", "LangChain框架", "API服务与FastAPI", "Docker容器化部署", "AI应用评估与可观测性"]
sources: ["https://www.elastic.co/blog/llm-app-portfolio-projects", "https://www.datacamp.com/blog/llm-portfolio-project"]
viz: "AI应用开发/_viz/AI应用作品集项目.svg"
viz_source: "AI应用开发/_viz/AI应用作品集项目.mmd"
viz_chart: "flow"
viz_reason: ""
---

# AI应用作品集项目

## 一句话定位
> 它属于AI应用开发，是用来解决〔0-1 独立落地一个可写进简历的 AI 应用〕的——把所有技能串成端到端能力证明。

## 🎯 核心收获 · 重点知识

**一句话成果**：学完你现在能独立设计并落地一个完整的 AI 应用（RAG/Agent），写进简历并在面试时讲清技术选型和踩坑。

**重点结论**（7 条）：
1. **作品集是转岗的硬通货**：JD 要"有 LLM 应用经验"，作品集 = 经验证明。比刷题/八股更能打动面试官。
2. **好作品集三标准**：① 真实痛点（不是 toy）；② 端到端（数据→模型→API→部署）；③ 可演示（Docker 一键跑/有 demo URL）。
3. **推荐项目方向**：① RAG 知识库问答（企业文档/技术文档）；② Agent 工具调用（研究助手/旅行规划）；③ 垂直 Agent（代码审查/数据分析）。选你熟悉领域。
4. **技术栈标配**：LangChain/LangGraph 编排 + 向量库（Chroma/Milvus）+ FastAPI 服务 + Docker 部署 + RAGAS 评估 + GitHub README。
5. **简历讲法**：用 STAR（Situation/Task/Action/Result）讲——痛点是什么、你做了什么、技术选型为什么、量化结果（如召回率从 X 到 Y）。
6. **面试防翻车**：要能讲清每个技术决策的 why（为什么选 Chroma 不选 Milvus）、踩过的坑（分块/检索/幻觉怎么解）、改进方向。
7. **加分项**：① 用 LangGraph 做有状态 Agent；② 加评估指标；③ 有真实用户/上线；④ 写技术博客总结。

**重点知识大纲**：
- 作品集定位
  - 转岗硬通货
  - 经验证明
  - 比八股更能打动人
- 好作品三标准
  - 真实痛点（非 toy）
  - 端到端（数据→部署）
  - 可演示（Docker/demo URL）
- 推荐方向
  - RAG 知识库问答
  - Agent 工具调用
  - 垂直 Agent（代码/数据）
- 技术栈标配
  - LangChain/LangGraph
  - 向量库
  - FastAPI
  - Docker
  - RAGAS 评估
  - GitHub README
- 简历讲法
  - STAR 结构
  - 技术选型 why
  - 量化结果
- 面试防翻车
  - 每个决策的 why
  - 踩过的坑
  - 改进方向
- 加分项
  - LangGraph 状态 Agent
  - 评估指标
  - 真实用户
  - 技术博客

## 📝 轻笔记
<details>
<summary>📝 轻笔记（点开看推演摘要与卡壳细节）</summary>

**起点认知**：以为作品集就是"做个 demo 放 GitHub"，不知道三标准和面试讲法。

**视觉模型（五问）**：
- 对象：痛点、需求、技术选型、实现、评估、部署、简历、面试
- 连接：痛点→需求→选型→实现→评估→部署→简历→面试
- 流向：从问题到证明的端到端流
- 边界：toy 项目不被认可；不能演示等于没有；讲不清 why 等于没做
- 变化：面试官追问深度→要能下钻每层细节

**视觉模型结构**：chart_type=flow。痛点(data)→需求(rule)→选型(process)→实现(process)→评估(process)→部署(process)→简历(data)→面试(boundary)。

**类比**：作品集像程序员的"作品集画册"——不是堆代码，而是讲"我遇到什么问题、怎么解、为什么这么解、效果如何"。面试官看的是工程思维和解决问题的能力。

**大白话讲解**：它属于AI应用开发，是转岗找工作的关键。光说不练假把式，要做出一个真能用的 AI 应用放 GitHub——RAG 问答或 Agent 助手，用 LangChain+向量库+FastAPI+Docker 全套搭起来，写好 README 能一键跑。简历用 STAR 讲，面试能讲清每个技术选型的 why 和踩坑。这是"会做 AI 应用"的硬证明。

**三个应用例子**：
1. 企业文档 RAG：上传公司 wiki→问"年假怎么请"→答+引用。技术：LangChain+Milvus+RAGAS。
2. 研究助手 Agent：给主题→Agent 自主搜网+整理+出报告。技术：LangGraph+搜索工具+FastAPI。
3. 代码审查 Agent：提交 PR→Agent 审安全/性能/风格→评论。技术：LangGraph 多 Agent+GitHub API。

**失效边界**：
- toy 项目（如"Hello GPT"）不被认可
- 不能演示（只有代码没 demo）等于没有
- 讲不清技术选型 why 等于没做

**边界补丁**：
- 边界1（toy）→ 选真实痛点，最好有潜在用户
- 边界2（不能演示）→ Docker 化+部署 demo URL
- 边界3（讲不清）→ 写技术博客总结选型理由

**卡壳点复盘**：
1. 什么算"好"作品集：原以为功能多就好→校准为真实痛点+端到端+可演示三标准。
2. 简历怎么写：原以为列技术栈→校准为 STAR 讲故事+量化结果。
3. 面试防翻车：原以为会做就行→校准为要能讲清每个 why 和踩坑。

**成长对比**：起点（作品集=demo）→ 现在（三标准+技术栈标配+STAR+面试防翻车）。

</details>

📎 [完整对话记录](_transcript/AI应用作品集项目.jsonl)

## 视觉模型图
- 打开图：[_viz/AI应用作品集项目.svg](_viz/AI应用作品集项目.svg)
- Mermaid 源：[_viz/AI应用作品集项目.mmd](_viz/AI应用作品集项目.mmd)

## 📚 参考资料
<details>
<summary>📚 参考资料</summary>

- **LLM 应用作品集指南**（博客，2026-06-28）https://www.elastic.co/blog/llm-app-portfolio-projects
- **DataCamp 作品集建议**（教程，2026-06-28）https://www.datacamp.com/blog/llm-portfolio-project

</details>

## 🔭 视野拓展 · 行业洞见
<details>
<summary>🔭 视野拓展 · 行业洞见（点开看多维度权威参照）</summary>

### 1. Eugene Yan · 应用工程与求职视角
- **身份**：应用机器学习工程师、技术博主
- **与本概念的关系**：写了大量 ML/AI 求职作品集建议
- **核心洞见**：作品集要讲"解决问题的能力"不是"用过的技术"，STAR + 量化结果最打动人
- **代表作**：*Getting a Data Science Job* 系列
- **扩展阅读**：[eugeneyan.com](https://eugeneyan.com/)

### 2. Greg Kamradt · 从0到1实战
- **身份**：技术博主
- **与本概念的关系**：RAG From Scratch 等教程是作品集项目的最佳起点
- **核心洞见**：作品集要"小而完整"——一个端到端 RAG 比十个 demo 强
- **代表作**：RAG From Scratch 教程
- **扩展阅读**：[Greg Kamradt GitHub](https://github.com/gkamradt)

### 3. 招聘方视角 · AI 应用 JD 分析
- **身份**：AI 应用团队招聘负责人（多 JD 汇总）
- **与本概念的关系**：从 JD 反推作品集要展示什么
- **核心洞见**：JD 要"有 LLM 应用经验"，作品集是经验证明；端到端+可演示+讲得清是硬要求
- **代表作**：Boss 直聘 AI 应用开发 JD 汇总分析
- **扩展阅读**：[Boss 直聘 AI 应用开发岗](https://www.zhipin.com/)

</details>

## 相关
[[RAG基础架构]] · [[Agent架构与ReAct模式]] · [[LangChain框架]] · [[API服务与FastAPI]] · [[Docker容器化部署]] · [[AI应用评估与可观测性]]
