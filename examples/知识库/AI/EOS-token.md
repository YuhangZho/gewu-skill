---
title: EOS token
category: AI
status: 已学透
importance: 3
prereqs: [Token]
groups: ["模型基础"]
goal_tags: []
aliases: ["结束符", "End of Sequence", "结束 token"]
tags: [AI]
created: 2026-06-19
related: [Token, 贪心解码]
sources: ["https://huggingface.co/docs/transformers/main/en/main_classes/text_generation"]
viz: ""
---

# EOS token

## 一句话定位
> 它属于 AI 大模型，是词表里一个**特殊 token**：模型生成出它，就表示"我说完了"，解码循环据此**停止**。

## 🎯 核心收获 · 重点知识
**一句话成果**：你现在能解释"模型怎么知道该停"，以及回答"被截断没说完"是怎么回事。

**重点结论**
- **EOS = End Of Sequence**，是词表里一个专门的特殊 token（常见写法 `</s>`、`<|endoftext|>`），**不对应任何人话**。
- 自回归模型一个接一个吐 token，本身没有"句号"概念；**采样到 EOS 就停止生成**。
- 训练时在每条样本结尾放上 EOS，模型于是学会"该结束时把它输出来"。
- 若 `max_tokens` 上限先到，会在**还没吐 EOS** 时被强行截断 → 回答看起来"没说完"。

**例子**：你问"1+1=?"，模型吐出 `2` 然后吐出 EOS → 接口收到 EOS 停止，返回"2"。
**换场景举例**：代码补全时，模型写完一个函数后吐 EOS，表示"这段补全到此结束"。

## 📂 学习过程记录
<details>
<summary>📂 学习过程记录（点开看分诊与快轨推演）</summary>

**起点认知**：只知道"模型会自己停下来"，不知道靠什么停。

**分诊定轨**：Q1 部件数=1（单一哨兵 token + 一个停止条件）；Q2 未学前置=0（Token 已学透）；Q3 转化/枢纽=0（不反直觉、非枢纽）。**合计 1 → 快轨**。

**快轨流程（已跑）**：设问 1 个（"模型怎么知道该停？"）→ 直接讲清 + 1 例 → 自己换场景举 1 例 → 轻落盘。**跳过**：视觉建模渲染、三套讲法、_viz 动效、隔天重讲（依据：冗余效应 + 4C/ID 重复性技能）。
</details>

## 参考资料
- HuggingFace Text Generation 文档（special tokens / eos_token_id），来源类型：官方文档，抓取 2026-06-19。可信度：高

## 相关
[[Token]] · [[贪心解码]]
