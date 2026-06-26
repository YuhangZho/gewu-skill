---
title: README 工程
category: 开源项目冷启动
status: 已完成
track: 标准轨
importance: 5
prereqs: ["项目定位与价值主张"]
groups: ["门面"]
goal_tags: ["知识变现"]
aliases: ["README", "README.md", "项目说明文档"]
tags: []
created: 2026-06-26
related: ["项目定位与价值主张", "Demo与可体验性", "贡献者友好设计", "GitHub发现性优化"]
sources: ["https://www.freecodecamp.org/news/how-to-structure-your-readme-file/", "https://github.com/matiassingers/awesome-readme", "https://open-awesome.com/projects/readme-best-practices", "https://github.com/alchaincyf/nuwa-skill"]
viz: "开源项目冷启动/_viz/README工程.svg"
viz_source: "开源项目冷启动/_viz/README工程.mmd"
viz_chart: "flow"
viz_reason: ""
---

# README 工程

## 一句话定位
> 它属于开源项目冷启动的门面层，是用来解决"访客来了留不住"的——把 README 当转化漏斗设计，让访客从看到到 star 走完 7 个节点。

## 🎯 核心收获 · 重点知识
**一句话成果**：学完你现在能把 gewu-skill README 按 7 节点漏斗诊断和改造，知道每个章节在漏斗里承担什么转化任务、卡点在哪、怎么补。

**重点结论**（AI 与你达成的最终共识）：
- **README ≠ 介绍，是转化设计**——介绍是单向信息输出；README 工程是转化漏斗，每个章节都是转化节点，目的是让访客从"看到"→"留下"→"试用"→"留存"。介绍是 README 的子集，不是本质。
- **7 节点转化漏斗**：首屏（30秒）→ 相关性识别 → Demo/截图 → Features/解决什么 → Quick Start+安装 → 10分钟闸门 → 第一个 wow 时刻 → 社会证明 → star。4 个节点不能跳：Demo 让人想试用，Features 让人决定试用，10分钟闸门是流失点，wow 时刻是留存点。
- **30 秒法则 + 10 分钟法则**：首屏 30 秒内传递价值（标题+一句话描述+徽章+视觉冲击）；10 分钟内让访客跑起来看到第一个 wow 时刻。10 分钟是"跑起来看到效果"的最大容忍时间——超过=认知负担=流失。
- **首屏 2 个致命错误**：①一上来讲原理和功能（不是访客决策要素）；②没有视觉冲击（无 logo/GIF/截图，访客大脑判定"信息密度低"→滚走）。
- **Demo 媒体首要目标是"让访客看到"不是"快"**——加载慢→访客等一下；加载失败→访客看到空白→以为没 Demo→流失。.webp 在 GitHub 移动端/部分客户端不渲染=比 gif 慢更糟。更好方案：.mp4（GitHub 原生渲染）或 gif 压缩到 2-5MB，或 .webp + 备用链接。
- **awesome-readme 7 原则**：①第一时间传达价值 ②用视觉替代文字 ③结构化导航 ④降低上手门槛 ⑤保持文档活性（动态元素） ⑥README 驱动开发 ⑦架构文档独立维护。
- **gewu-skill README 现状诊断**：7 徽章+2 Demo 媒体+三语+Quick Start，结构相当完整。4 个卡点：python 误导徽章（`python-3.8+`让访客以为必须装python）、.webp 不兼容、安装章节太重（环境检查+两种方式+10+agent路径表）、首屏标语缺"为谁"。
- **nuwa-skill 是标杆案例**：首屏 hero.gif+slogan+badge 视觉冲击强；Demo 用三段式对话实录（Naval/马斯克/乔布斯）金句密度高，wow 时刻极强；安装<1 分钟（npx skills add）；Feature 放后面用五层表格。首屏 Star Badge 缺失是唯一短板。

**重点知识大纲 / 脑图**：
- README 本质
  - 不是介绍，是转化设计
  - 每个章节=转化漏斗节点
  - 目的=看到→留下→试用→留存
- 7 节点转化漏斗
  - 首屏（30秒：标题+标语+徽章+视觉）
  - 相关性识别（跟我有关吗）
  - Demo/截图（视觉证明价值）
  - Features/解决什么（展开核心卖点）
  - Quick Start+安装（10分钟跑起来）
  - 10分钟闸门（流失点：超时→流失）
  - 第一个wow时刻（留存点：看到效果）
  - 社会证明（star数/贡献者/案例）
  - star+加作者（转化完成）
- 3 个失效边界
  - 首屏无视觉冲击→扫一眼就走
  - 安装超10分钟→耐心耗尽流失
  - 无社会证明→"就我一个人用"→只看不star
- awesome-readme 7 原则
  - 传达价值 / 视觉替代 / 结构导航 / 降低门槛 / 文档活性 / README驱动 / 架构独立
- Demo 媒体取舍
  - 首要目标=让访客看到（不是快）
  - 加载失败比加载慢更糟
  - .mp4 > gif > .webp（兼容性维度）
- gewu-skill 4 卡点与改造
  - python误导徽章→改deps-only或删
  - .webp→转.mp4或加备用链接
  - 安装章节太重→折叠+前置Quick Start
  - 首屏标语缺为谁→补具体人群

## 📝 轻笔记
<details>
<summary>📝 轻笔记（点开看推演摘要与卡壳细节）</summary>

**起点认知**：README=介绍大纲和实现内容，介绍页只讲重点，臃肿没人看。
→ 校准：README ≠ 介绍，是转化设计——每个章节是转化漏斗节点。

**视觉模型（五问 · 用户先讲）**：
- **对象**：README 首段、访客大脑、README 安装步骤、README 解决什么、作者联系方式
- **连接**：访客大脑先看 → README 首段 → 感兴趣 → README 解决什么 → 如何安装 → 实际体验 → 感觉好 + 加作者 V
- **流向**：线性漏斗（首屏→识别→Demo→Features→安装→闸门→wow→社会证明→star）
- **边界**：不会安装 python 的用户；复杂大量训练的学习型用户
- **变化**：首屏效果决定继续或离开

**视觉模型结构（AI 校准后）**：
- **chart_type（AI 自主判定）**：flow（7 节点漏斗 + 3 失效边界）
- **节点 kind**：concept（首屏、Features）、actor（访客）、data（Demo、社会证明）、process（安装、star）、rule（10分钟闸门）、state（wow 时刻）、boundary（3 个失效边界）
- **结构纠偏**：用户初版跳过了 4 个节点（Demo→Features、10分钟闸门→wow时刻）。AI 校准补全为完整 7 节点漏斗。

**类比 1（商店橱窗）**：路人路过橱窗→看到衣服漂亮可能适合自己→进店试穿→看商品标签材质价格→满意结账→排队不超10分钟→试穿 wow→拍照分享好友。橱窗=转化漏斗第一站，10分钟排队=第一个 wow 时刻倒计时。

**类比 2（B 站视频封面）**：封面有冲击力→用户点开看→几分钟满意点赞→继续看有惊喜转发。

**大白话讲解（讲给外行）**：它属于开源运营里的问题，是用来解决"为什么有些项目发出去没人理"的。好比路人路过商店橱窗——橱窗里挂的衣服漂亮（=首屏动画+标语），你觉得可能适合自己就进店试穿（=相关性识别+Demo），看商品标签材质价格（=Features），满意了去结账（=安装），排队不能超过10分钟（=10分钟闸门），穿上身那一刻 wow（=第一个 wow 时刻），看到别人也在穿就放心买了（=社会证明）。README 不是介绍，是转化漏斗——每个章节都是一个转化节点，目的是让你从看到走到 star。

**三重验证**：
1. **正向验证（nuwa-skill）**：首屏 hero.gif+slogan+badge 吸引眼球；Demo 三段式对话（Naval/马斯克/乔布斯）金句密度高 wow 极强；安装<1 分钟；Feature 放后面五层表格。唯一短板=首屏缺 Star Badge。
2. **失效边界补丁**：首屏动画无吸引力 → 重新做一个（B 站封面逻辑：有冲击力才有人点开）。
3. **换类比（B 站视频封面）**：封面=首屏、几分钟满意=Features、点赞=star、继续看有惊喜=wow 时刻、转发=社会证明。

**卡壳点复盘**：
- 卡壳 1：以为 README=介绍 → 补：是转化设计，每个章节是转化节点。
- 卡壳 2：10 分钟法则只抓到"太长没人用" → 补：10 分钟是"跑起来看到第一个 wow 时刻"的最大容忍时间。
- 卡壳 3（.webp 盲区）：只权衡了加载速度和兼容性，漏了"加载失败比慢更糟" → 补：Demo 媒体首要目标是"让访客看到"，.mp4 > gif > .webp。
- 卡壳 4（漏斗跳节点）：验收时跳过 4 个节点 → 补：完整 7 节点不能跳，Demo 让人想试用，Features 让人决定试用，10分钟闸门是流失点，wow 时刻是留存点。

**成长对比**：
- 起点：README=介绍大纲和实现内容，臃肿没人看
- 现在：README 是 7 节点转化漏斗，每章节承担转化任务；Demo 媒体首要目标是让访客看到不是快；gewu-skill 有 4 个卡点待改（python徽章/.webp/安装太重/标语缺为谁）。

</details>

📎 [完整对话记录](_transcript/README工程.jsonl)

## 视觉模型图
- 打开图：[_viz/README工程.svg](_viz/README工程.svg)
- Mermaid 源：[_viz/README工程.mmd](_viz/README工程.mmd)

## 📚 参考资料
<details>
<summary>📚 参考资料（点开查看本轮引用来源）</summary>

- 〔freeCodeCamp · How to Structure Your README File，2026-06-26 抓取〕 链接：https://www.freecodecamp.org/news/how-to-structure-your-readme-file/
  - 原话引述："If someone can clone your repository and get it running in under 10 minutes, your README did its job!"
  - AI 转述（可信度：高）：19 章标准结构，首屏 4 要素（标题+描述/Features/Tech Stack/徽章），Quick Start 四步法（clone→安装依赖→环境配置→启动），核心心法"先写 README 再写代码"。

- 〔awesome-readme · 漂亮 README 核心元素与工程化原则，2026-06-26 抓取〕 链接：https://github.com/matiassingers/awesome-readme
  - AI 转述（可信度：高）：7 大工程化原则——①第一时间传达价值 ②用视觉替代文字 ③结构化导航 ④降低上手门槛 ⑤保持文档活性 ⑥README 驱动开发 ⑦架构文档独立维护。漂亮 README 公式=Logo+一句话描述+Badges→GIF演示→TOC→Features→Installation+Quickstart→Usage→Contributing+License。

- 〔nuwa-skill README · 标杆案例分析，2026-06-26 抓取〕 链接：https://github.com/alchaincyf/nuwa-skill
  - AI 转述（可信度：高）：首屏 hero.gif 炼金术蒸馏动画+slogan"你想蒸馏的下一个员工，何必是同事"+4 badge；Demo 三段式对话实录（Naval/马斯克/乔布斯）金句密度高；安装<1 分钟（npx skills add）；Feature 放后面用五层表格；wow 时刻极强（乔布斯谈 OpenAI 反转"最终赢家可能是 Apple"）。短板=首屏缺 Star Badge。

</details>

## 🔭 视野拓展 · 行业洞见
<details>
<summary>🔭 视野拓展 · 行业洞见（点开看多维度权威参照）</summary>

### 1. Tom Preston-Werner · 「README 驱动开发之父」
- **身份**：GitHub 联合创始人、《Readme Driven Development》作者
- **与本概念的关系**：他提出的"先写 README 再写代码"理念是 awesome-readme 第 6 原则的理论源头——README 不是事后文档，是项目规格说明书，迫使你从用户角度思考。
- **核心洞见**：先写 README 能在写代码前就发现设计问题——"如果你不能在 README 里说清这个项目做什么，那你的代码也说不清"。
- **代表作**：*Readme Driven Development*（2010 博文）
- **扩展阅读**：[Readme Driven Development 原文](https://tom.preston-werner.com/2010/08/23/readme-driven-development.html)

### 2. Richard Littauer · 「standard-readme 规范作者」
- **身份**：开源贡献者、standard-readme 规范发起人
- **与本概念的关系**：他制定了 README 的标准化规范（standard-readme spec），被 awesome-readme 收录为推荐模板——规定了 README 必须包含的章节和顺序。
- **核心洞见**：README 规范化的目的是"让访客在任何开源项目里都能快速找到他们需要的信息"——一致性比创意更重要，首屏结构应遵循行业惯例而非自创。
- **代表作**：standard-readme 规范
- **扩展阅读**：[standard-readme 规范](https://github.com/RichardLitt/standard-readme)

### 3. 花叔（alchaincyf）· 「nuwa-skill README 实战代表」
- **身份**：nuwa-skill 作者、AppStore 付费榜 Top1 开发者
- **与本概念的关系**：nuwa-skill 是 README 工程的中文实战标杆——首屏 hero.gif+slogan 视觉冲击、Demo 三段式对话 wow 时刻、安装<1 分钟、五层 Feature 表格，几乎踩准了 7 节点漏斗每个节点。
- **核心洞见**：Demo 的金句密度比动画精美更重要——nuwa-skill 的 Demo 是纯文本对话实录，但每段都有可截图传播的金句（乔布斯"最终赢家可能是 Apple"），传播性远超精美但无内容的动画。
- **代表作**：nuwa-skill（2026）
- **扩展阅读**：[nuwa-skill 仓库](https://github.com/alchaincyf/nuwa-skill)

**视角对照**：

| 参照 | 一句话 | 关键词 |
|---|---|---|
| Tom Preston-Werner | 先写 README 再写代码，README 是规格不是文档 | README 驱动开发 |
| Richard Littauer | 规范化一致性比创意更重要 | standard-readme |
| 花叔 | Demo 金句密度比动画精美更重要 | 三段式对话 wow |

</details>

## 相关
[[项目定位与价值主张]] · [[Demo与可体验性]] · [[贡献者友好设计]] · [[GitHub发现性优化]]
