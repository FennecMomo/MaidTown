# MaidTown 文档总入口

> 2026-10-07 统一整理。以后从本页进入；当前规则不再分散在旧 SPEC、交接摘要和问题单里。

| 要做什么 | 唯一入口 |
|---|---|
| 理解当前完整设计 | [统一开发设计](design/current/README.md) |
| 继续讨论未定功能 | [待讨论功能清单](planning/OPEN_QUESTIONS.md)，以该页顶部暂停点为准 |
| 看新旧设计及实现冲突 | [冲突与源码证据](planning/CONFLICTS.md) |
| 看开发、风险和验收状态 | [实施与验证清单](planning/IMPLEMENTATION.md) |
| 看模块当前快照 | [项目状态](planning/STATUS.md) |
| 找原文、旧报告和整理去向 | [53 份文档台账](archive/DOCUMENT_REGISTER.md) |
| 记录新确认 | [决策日志](design/current/DECISIONS.md)，同时更新对应专题 |

## AI 继续设计讨论：读取与修改规则

### 开始时读取

1. 先读本页，确认当前文档分工，不从归档里的旧接续摘要恢复状态。
2. 读 [统一设计总览](design/current/README.md)，掌握模块边界、规则优先级和工作范围。
3. 读 [待讨论功能清单](planning/OPEN_QUESTIONS.md) 顶部的当前暂停点与对应 Q 条目，再读该功能的设计专题；暂停点只在 Q 清单维护。
4. 查 [决策日志](design/current/DECISIONS.md) 最近的相关确认，避免把已回答的问题重新提出。
5. 涉及实现冲突时才按需读 [冲突表](planning/CONFLICTS.md)、[实施清单](planning/IMPLEMENTATION.md) 和对应源码／模块 API。只有当前文档缺少确认依据或用户要求追溯时才查 archive；无需每轮重读全部历史记录或重做代码审查。

### 每次用户确认后修改

| 文件 | 必须更新什么 |
|---|---|
| 对应的 design/current 专题 | 将新确认写入有效正文，替换被推翻的规则；建议与推导保持明确标注 |
| [DECISIONS.md](design/current/DECISIONS.md) | 追加日期、Q 编号、用户确认、替代了什么、影响哪些专题；保留决策过程 |
| [OPEN_QUESTIONS.md](planning/OPEN_QUESTIONS.md) | 更新本项状态；只有全部未决点解决才关闭，部分确认保留剩余问题；更新顶部暂停点与下一条具体问题，编号不重用 |
| [CONFLICTS.md](planning/CONFLICTS.md) | 仅当确认解决／新增设计冲突，或有新的源码证据时同步；设计定案不等于代码已修 |
| [IMPLEMENTATION.md](planning/IMPLEMENTATION.md) | 仅当实施范围、依赖或验证状态变化时同步；已定未实现的工作仍保持待做 |

归档正文不追加新讨论，也不重新创建旧 SPEC、旧 HANDOFF 或分散的讨论笔记。目录结构不变时，无需每次改本页、模块 INDEX 或 API 文档；设计设想不能写成已存在的 API。

### 讨论方式与权限

一次只提出一个真正未定的问题，连同一议题的多个分叉也逐次讨论。用户确认后先落盘，再进入下一项；不重复询问已确认规则。用户指定新议题时以用户指示为先，保留尚未解决的旧项。

提问方式（2026-10-11 用户明确要求）：每次提出决策前，先用具体场景说明问题背景、可行方案与各自代价，再只问一个决策；不得把问题单独抛出、只给一句标题让用户猜。选项中的推荐只作助手建议，不构成定案。

继续设计讨论只授权读资料、按需静态核对和同步 Markdown；未经用户明确授权，不改源码、不启动开发、不委派开发、不编译或运行游戏。新确认优先于当前正文，当前正文优先于归档旧方案；无法判定时保留争议，不替用户拍板。

## 按系统阅读

[开局与地皮](design/current/SETTLEMENT_AND_LAND.md) · [世界与物流](design/current/WORLD_AND_LOGISTICS.md) · [道路施工](design/current/ROADS_AND_CONSTRUCTION.md) · [委托产业](design/current/QUESTS_AND_INDUSTRIES.md) · [仓库](design/current/STORAGE.md) · [经济商业](design/current/ECONOMY_AND_COMMERCE.md) · [居民生活](design/current/RESIDENTS.md) · [工程技术](design/current/ENGINEERING.md) · [长期保留项](design/current/LEGACY_FEATURES.md)

## 模块与技术资料

| 类别 | 入口 | 使用边界 |
|---|---|---|
| MaidQuest | [模块索引](../maidquest/docs/INDEX.md) · [公开 API](../maidquest/docs/API.md) | 现有委托能力，不等于新经济已实现 |
| MaidMoreWork | [模块索引](../maidmorework/docs/INDEX.md) · [公开 API](../maidmorework/docs/API.md) | 现有生产能力与测试记录 |
| FennecLib | [模块索引](../fenneclib/docs/INDEX.md) · [公开 API](../fenneclib/docs/API.md) | 行为和 UI 基础库 |
| 开发规范 | [代码规范](conventions/DEV_CONVENTIONS.md) · [提交规范](conventions/GIT_COMMIT_CONVENTIONS.md) · [测试协作](conventions/TEST_CONVENTIONS.md) | 规范不构成本轮代码／运行授权 |
| NeoForge／TLM | [注册](references/mc-neoforge/registration.md) · [Brain](references/mc-neoforge/brain-behavior.md) · [任务](references/mc-neoforge/task-system.md) · [TLM](references/mc-neoforge/tlm-integration.md) · [持久化](references/mc-neoforge/attachment-codec.md) · [GUI](references/mc-neoforge/gui-system.md) · [API 陷阱](references/mc-neoforge/api-pitfalls.md) | 特定版本技术参考，不是产品规格 |
| 模式与模板 | [代码模式](references/patterns.md) · [UI 模板参考](references/template-library.md) · [Java 模板](templates/CustomPayload.java) | 以实际依赖与源码为准 |
| 工具及依赖记录 | [文档脚本](scripts/) · [依赖更新记录](archive/2026-10-07/docs/references/touhoulittlemaid-26.1-update-20260926.md) | 历史构建记录不证明当前运行已验证 |

## 文档维护

只在当前专题维护有效规则；Q 清单维护未定事项；I／V 清单维护实现与验证。历史报告集中移入 archive，原目录不再保留旧文档或跳转页；子模组仅保留专属 API、版本记录、索引和仍有效的专项技术文档。

归档见 [2026-10-07 归档说明](archive/2026-10-07/README.md)。运行日志、截图素材、第三方依赖说明分类保留，不混入产品规格。

## 目录分工

| 目录 | 只放什么 |
|---|---|
| docs 根目录 | 本页 INDEX.md |
| design/current | 当前统一设计与决策日志 |
| planning | 待讨论、实现清单、冲突表和项目状态 |
| conventions、references | 跨模块规范和仍有效的技术参考 |
| assets/covers | 模组封面素材 |
| scripts、templates | 文档辅助工具和代码模板 |
| archive | 历史设计、交接、审查、测试、问题记录与旧截图；台账也在此 |
