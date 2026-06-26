# RELEASES

格物 · Gewu 的发布记录与待办。

> 链接：[全部 Release](https://github.com/YuhangZho/gewu-skill/releases) · [全部 PR](https://github.com/YuhangZho/gewu-skill/pulls) · [提交历史](https://github.com/YuhangZho/gewu-skill/commits)

---

## [0.1.0] - 2026-06-26

首个内测版本。把"有问题问 AI"沉淀为可复习的本地知识地图。

### Added
- **学习路线规划**：围绕目标拆解"先学什么 / 为什么先学它 / 下一步学什么"。
- **费曼式学习闭环**：设问 → 讲解 → 复述 → 追问卡壳点 → 通过验证再收尾。
- **概念笔记沉淀**：一句话定位、核心收获、卡壳点与修正、边界与易错点。
- **本地知识站**：学习路线图、知识图谱、目标规划、概念文档四类可打开页面。
- **断点续学**：记录学习状态，下次从卡住位置继续。
- **零散知识融合**：临时小概念可先记下，攒多后归入对应领域。
- **多主题外观**：浅色、深色、宣纸、夜墨四种风格，配置见 `templates/config.example.json`。
- **指定知识库路径**：首次使用询问，路径存于 `~/.gewu/glb_vault_path.json`。

### Changed
- README 与多语言文档（EN / ES）初版定稿。

### Fixed
- 切换主题后未持久化保存的问题。([#12](https://github.com/YuhangZho/gewu-skill/pull/12))
- GitHub 主页 README 无法内联 `<video>` 的问题，改用 WebP/GIF 格式。([#14](https://github.com/YuhangZho/gewu-skill/pull/14))
- 资源体积过大导致首页加载缓慢的问题。([#15](https://github.com/YuhangZho/gewu-skill/pull/15))

### Removed
- 导师子系统：保持单一学习主线，避免认知负担。([#7](https://github.com/YuhangZho/gewu-skill/pull/7))
- Step 4 的冗余细节描述：轻量化学习过程。([#8](https://github.com/YuhangZho/gewu-skill/pull/8)、[#11](https://github.com/YuhangZho/gewu-skill/pull/11))

### Verification
- 通过：Cursor(auto) / Codex(5.5) / Claude(opus4.8) / Kimi(K2.6)。
- 一般：Marvis / Trae / Qoder（疑似模型注意力漂移，2026.6.26）。

---

## TODO

按优先级与状态分组。状态标记：`待办` / `进行中` / `探索中` / `阻塞`。

### 进行中
- [ ] **零散知识融合效果进一步测试**：领域归属判定不够稳定，需要更多场景样本验证。

### 待办
- [ ] **多 agent 的稳定性**：调研 Marvis / Trae / Qoder 上注意力漂移的根因，必要时给出 prompt 层面的兜底。

### 探索中

- [ ] **复习机制**：基于艾宾浩斯曲线的提醒，而非完整题库。
- [ ] **抽卡复习**：学完知识提供抽卡复习的小游戏；
- [ ] **导师系统**：不同导师风格口吻、思维不同(严格遵循教学流程框架)
- [ ] **导入与导出**：支持从 Obsidian / Anki 导入，导出为 Markdown 包。

---

## 维护说明

**如何新增一次发布？**

1. 在 `[Unreleased]` 节累积改动，归类到 `Added` / `Changed` / `Fixed` / `Removed`。
2. 发布时把 `[Unreleased]` 改写为 `[x.y.z] - YYYY-MM-DD`，并在顶部新建空的 `[Unreleased]`。
3. 打 git tag：`git tag v0.x.y && git push origin v0.x.y`。
4. 在 GitHub 创建对应 Release，正文可粘贴本文件该版本节内容。

**版本号怎么定？**

- 主版本（MAJOR）：架构级重构或不兼容变更。
- 次版本（MINOR）：新增能力，向后兼容。
- 修订号（PATCH）：bug 修复与文案调整。
- 0.x.x 阶段：一切皆可变，次版本号即可视为"破坏性变更"。

**链接约定**

[Unreleased]: https://github.com/YuhangZho/gewu-skill/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/YuhangZho/gewu-skill/releases/tag/v0.1.0
