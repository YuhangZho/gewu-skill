---
title: GitHub 发现性优化
category: 开源项目冷启动
status: 已完成
track: 标准轨
importance: 4
prereqs: ["项目定位与价值主张", "README工程"]
groups: ["渠道"]
goal_tags: ["知识变现"]
aliases: ["发现性优化", "Discoverability", "GitHub SEO", "topics优化"]
tags: []
created: 2026-06-26
related: ["项目定位与价值主张", "README工程", "内容营销与Build in Public", "增长飞轮", "冷启动渠道矩阵"]
sources: ["https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics", "https://ask.csdn.net/questions/9369771"]
viz: "开源项目冷启动/_viz/GitHub发现性优化.svg"
viz_source: "开源项目冷启动/_viz/GitHub发现性优化.mmd"
viz_chart: "flow"
viz_reason: ""
---

# GitHub 发现性优化

## 一句话定位
> 它属于开源项目冷启动的渠道层，是用来解决"别人怎么在 GitHub 上找到你的项目"的——被动被发现的基础设施。

## 🎯 核心收获 · 重点知识
**一句话成果**：学完你现在能给 gewu-skill 做完整的发现性优化（topics/description/social preview/About），让访客在搜索和浏览时能找到你、在搜索结果里愿意点进来。

**重点结论**（AI 与你达成的最终共识）：
- **GitHub 发现路径有 6 种**：①Trending ②外部链接（推广文/朋友介绍）③**GitHub 搜索**（关键词匹配 topics+description+README+仓库名）④**Topics 浏览**（github.com/topics/ai）⑤用户主页/组织页 ⑥Explore 推荐。**站内搜索和 Topics 浏览是被动发现的主力**——只靠外部引流=发现性没做。
- **description vs README 标语是两块不同招牌**：description 是店外招牌（搜索结果里显示，SEO 权重最高，0.5 秒直白识别"这跟我有关吗"），README 标语是店内介绍（点进来才看，3-30 秒可好奇可隐喻）。**description 写不好=搜索结果没人点=流量在门口断**。两块招牌服务不同场景，都不能失效。
- **发现性优化 ≠ 冲 Trending**：发现性=被动被发现的基础设施（topics/description/preview，持续长效），冲 Trending=主动冲榜的运营动作（24h star 增量，一次性日粒度重置）。**发现性是地基，Trending 是楼——发现性差=即使冲上 Trending 访客点进来看到空 About/无 topics/差 description 也不留。先修基础设施，再冲榜单，顺序不能反。**
- **topics 规范**（GitHub 官方）：小写字母+数字+连字符，≤50 字符，最多 20 个；GitHub 自动分析公开仓库建议 topics（管理员可接受/拒绝）；最佳实践 4-8 个，混合"类别+技术栈+场景+语言"。
- **social preview**=社交分享预览图（1200×630px），仓库链接发到 Twitter/微信/Slack 时显示的卡片图。不设=GitHub 用默认丑截图=社交点击率低；设了=精心设计（logo+定位语+视觉冲击）点击率高 2-3 倍。设置路径：Settings→Social preview→Upload image。
- **6 项发现性优化清单**：①topics（4-8 个）②description（1 句话≤350 字符）③About 完整填写 ④social preview（1200×630）⑤README 首屏 SEO（Google 搜索抓）⑥Release 标签（订阅通知+版本感知）。
- **description 吸引力优化**：原版"A Feynman-method learning system with vault auto setup"缺为谁/技术实现非用户价值/缺差异化。优化版 A（推荐）："Turn 'ask AI' into a goal-driven learning roadmap with Feynman method and auto knowledge vault."——保留对比结构+目标驱动+费曼+vault 翻译成用户价值。
- **gewu-skill 发现性现状**：topics ✅已加、About ✅有、Release ✅有、README 首屏 ✅有标语、description ❓需改、social preview ❌没设（最大流失点之一）。
- **发现性漏斗末端 = README 漏斗起点**：两个漏斗接力——发现性负责"让人点进来"（搜索/浏览→description 闸门→点击），README 负责"让人留下来"（首屏→Demo→Features→安装→wow→star）。中间接力棒=About 区域+README 首屏。

**重点知识大纲 / 脑图**：
- 6 种发现路径
  - Trending（24h star 增量榜）
  - 外部链接（推广文/朋友/社交媒体）
  - GitHub 搜索（关键词匹配，主力被动发现）
  - Topics 浏览（github.com/topics/xxx，主力被动发现）
  - 用户主页/组织页
  - Explore 推荐（基于 topics 和 star 行为）
- 两块不同招牌
  - description=店外招牌（搜索结果显示，SEO 最高，0.5 秒直白）
  - README 标语=店内介绍（点进来才看，3-30 秒好奇隐喻）
  - description 写不好=流量在门口断
- 发现性 vs 冲 Trending
  - 发现性=被动基础设施（持续长效）
  - 冲 Trending=主动运营动作（一次性日粒度）
  - 地基 vs 楼，顺序不能反
- 6 项优化清单
  - topics（4-8 个，小写+连字符）
  - description（1 句话，≤350 字符）
  - About 完整填写
  - social preview（1200×630）
  - README 首屏 SEO
  - Release 标签
- 发现性漏斗
  - 3 路径→搜索结果列表→description 闸门→点击→About+README 接力→star
  - 末端=README 漏斗起点
- 3 个失效边界
  - 无 topics=搜索/浏览都找不到
  - description 差=搜索结果没人点
  - 无 social preview=社交分享丑截图低点击

## 📝 轻笔记
<details>
<summary>📝 轻笔记（点开看推演摘要与卡壳细节）</summary>

**起点认知**：已加 topics（比前几个概念起点高），"加错了会吸引不同频的人"直觉准。
→ 校准：发现性优化不只是 topics，是 6 项基础设施。

**视觉模型（五问 · 用户先讲）**：
- **对象**：搜索框/topics 页面/搜索结果列表/About/description/social preview/README 首屏
- **连接**：搜索→结果→About/desc→social preview+README 首屏
- **流向**：3 路径汇入→结果列表→description 闸门→点击→About+README 接力→star
- **边界**：无 topics/加错
- **变化**：description 不同触发不同分支

**视觉模型结构（AI 校准后）**：
- **chart_type（AI 自主判定）**：flow（3 路径汇入+description 闸门+About+README 接力+3 失效边界）
- **节点 kind**：actor（访客）、process（3 路径、点击、star）、data（搜索结果、social preview）、rule（description 闸门）、state（点击进入）、concept（About+README 接力）、boundary（3 个失效边界）
- **结构纠偏**：用户初答只想到 trending+外部链接→补全 6 路径；验收时跳过 About+README 接力→补丁"发现性末端=README 漏斗起点"。

**类比 1（商店）**：先看招牌和橱窗外置菜单（=topics+description），再搜大众点评和朋友推荐（=外部链接+social preview），进来后看店内环境感受第一次服务（=About+README 接力）。

**类比 2（书店找书）**：读者先找分类书柜（=Topics 浏览），一本本看标题是否切合需求（=搜索结果列表+description），找到后看作者和简介（=About+README 接力），发现宝藏分享书皮封面给朋友（=social preview 助攻转发）。

**大白话讲解（讲给外行）**：它属于开源运营里的问题，是用来解决"别人怎么在 GitHub 上找到你的项目"的。好比书店找书——读者先找分类书柜（=Topics 浏览），一本本看标题（=搜索结果里的 description），标题切合需求才抽出来看作者和简介（=About+README 接力）。店外招牌（description）要直白让人 0.5 秒识别"这跟我有关吗"，店内介绍（README 标语）可以好奇可以隐喻。还有 6 种找书路径：主动搜、逛分类、朋友推荐、排行榜、店员推荐、路过看到。关键要先修好招牌和分类（发现性基础设施），再去冲排行榜（Trending），顺序不能反——招牌没修好即使上了排行榜，人家点进来看到空荡荡也不留。

**三重验证**：
1. **正向验证（nuwa-skill）**：topics/description/About/README 首屏都有，social preview 不确定。发现性做得相当完整。
2. **失效边界补丁**：description 差找不准用户定位 → 补救：Turn "ask AI" into a goal-driven learning roadmap with auto knowledge vault.
3. **换类比（书店找书）**：分类书柜=Topics 浏览，标题=description，作者简介=About+README 接力，书皮封面=social preview 助攻转发。

**卡壳点复盘**：
- 卡壳 1：只想到 trending+外部链接 → 补：6 种路径，站内搜索和 Topics 浏览是被动发现主力。
- 卡壳 2：description vs README 标语"不清楚" → 补：两块不同招牌，店外直白 vs 店内好奇。
- 卡壳 3（最深）：发现性 vs 冲 Trending"不清楚" → 补：发现性=地基（被动基础设施持续长效），冲 Trending=楼（主动运营一次性），顺序不能反。
- 卡壳 4：验收跳过 About+README 接力 → 补：发现性漏斗末端=README 漏斗起点，两者接力。

**成长对比**：
- 起点：已加 topics，"加错了吸引不同频的人"
- 现在：6 种发现路径；description vs README 两块招牌；发现性是地基 Trending 是楼；6 项优化清单；gewu-skill 需改 description+设 social preview。

</details>

📎 [完整对话记录](_transcript/GitHub发现性优化.jsonl)

## 视觉模型图
- 打开图：[_viz/GitHub发现性优化.svg](_viz/GitHub发现性优化.svg)
- Mermaid 源：[_viz/GitHub发现性优化.mmd](_viz/GitHub发现性优化.mmd)

## 📚 参考资料
<details>
<summary>📚 参考资料（点开查看本轮引用来源）</summary>

- 〔GitHub Docs · Classifying your repository with topics，2026-06-26 抓取〕 链接：https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics
  - 原话引述："With topics, you can explore repositories in a particular subject area, find projects to contribute to, and discover new solutions to a specific problem."
  - 原话引述："Use lowercase letters, numbers, and hyphens. Use 50 characters or less. Add no more than 20 topics."
  - AI 转述（可信度：高）：topics 出现在仓库主页，点击可看同 topic 其他仓库；GitHub 分析公开仓库内容自动建议 topics；公开+私有仓库都可加 topics 但私有的只在有权访问时出现在搜索结果。

- 〔CSDN · GitHub Trending 排序算法逆向研究，2026-06-26 抓取〕 链接：https://ask.csdn.net/questions/9369771
  - AI 转述（可信度：中-高）：主信号=过去 24h star 增量（Pearson r≈0.87），日粒度 UTC 00:00 重置，≤7 天新仓库 ×1.6 冷启动加权，过滤 fork/机器人/刷星。被动展示非主动算法推荐。

</details>

## 🔭 视野拓展 · 行业洞见
<details>
<summary>🔭 视野拓展 · 行业洞见（点开看多维度权威参照）</summary>

### 1. GitHub Explore Team · 「topics 分类体系设计者」
- **身份**：GitHub 官方 Explore 团队，维护 github/explore 仓库
- **与本概念的关系**：他们设计了 topics 分类体系，让仓库能被按主题发现——topics 是 GitHub 发现性基础设施的核心。
- **核心洞见**：topics 不是标签而是分类系统——好的 topics 让仓库同时出现在多个相关主题的浏览页里，等于多条被动发现路径。社区可贡献 featured topics 到 github/explore 仓库。
- **代表作**：github/explore 仓库（topics 分类体系）
- **扩展阅读**：[github/explore](https://github.com/github/explore) · [Topics 官方文档](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics)

### 2. Tj Holowaychuk · 「GitHub 发现性实战代表」
- **身份**：Express.js / Koa 作者，GitHub 早期高星项目代表
- **与本概念的关系**：Express.js 是 GitHub 发现性优化的经典案例——精准 topics（nodejs/web-framework/router/middleware）+ 简洁 description + 完整 About，让它在 Node.js 生态里被动发现率极高。
- **核心洞见**：发现性的关键是"站在搜索者角度想关键词"——你的 topics 要包含用户会搜的词，不是你自己想的词。Express 的 topics 里没有"express"（用户不会搜这个），但有"web-framework""middleware"（用户会搜）。
- **代表作**：Express.js（2010-）
- **扩展阅读**：[Express.js 仓库](https://github.com/expressjs/express)

### 3. Steve Yegge · 「README 驱动发现性理论代表」
- **身份**：博主、前 Google/Sourcegraph 工程师
- **与本概念的关系**：他写过"README 是最重要的营销文件"——README 首屏不只是给已点进来的人看，Google 搜索也抓 README 前几百字，所以 README 首屏是双重身份（发现性+转化）。
- **核心洞见**：README 前 200 字是整个项目的"SEO 窗口"——Google 抓它作为搜索摘要，GitHub 搜索也权重它。所以 README 首屏标语不能只顾好看，要含可搜索的关键词。
- **代表作**：《Declarative README》系列博文
- **扩展阅读**：[Steve Yegge 博客](https://steve-yegge.medium.com/)

**视角对照**：

| 参照 | 一句话 | 关键词 |
|---|---|---|
| GitHub Explore Team | topics 是分类系统不是标签，多条被动发现路径 | 分类体系 |
| Tj Holowaychuk | topics 要含用户会搜的词不是你自己想的词 | 搜索者角度 |
| Steve Yegge | README 前 200 字是 SEO 窗口，双重身份 | 发现性+转化 |

</details>

## 相关
[[项目定位与价值主张]] · [[README工程]] · [[内容营销与Build in Public]] · [[增长飞轮]] · [[冷启动渠道矩阵]]
