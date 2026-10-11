# 文档台账与整理范围

> 2026-10-07。共清点 **53 份自有 Markdown 文档**（含隐藏目录的 .opencode/project.md 和模块 AGENTS.md）；设计文档、索引、待办、交接、测试、API 和技术参考全部分配去向。原混合规格及历史交接、审查、测试、问题记录已集中移入 archive；旧位置不再保留导航页。

## 整理边界

本轮深入对齐的是产品规则、设计记录、重复待办和关键实现入口。API／框架参考按用途分类保留，不宣称已逐签名重新验证所有技术示例。未改模块源码或现有运行资产。

- `refs/` 中第三方源码文档、`.opencode/node_modules/` 的依赖 README／LICENSE 属外部资料，不修改上游内容。
- `run-shared/` 的崩溃报告、调试文本、选项、命令历史、存档说明是运行产物，不混入开发设计，也不清理。
- PNG 封面集中到 `docs/assets/covers/`，旧截图及未识别用途图片集中到 `docs/archive/2026-10-07/assets/`；本轮不对图片内容作新设计解释。
- `docs/scripts/` 与 `docs/templates/` 是辅助程序／模板，本轮不改代码。
- 未发现自有的额外 rst／adoc 设计文档；不递归整理构建输出、Git 内部或依赖目录。

## 全部原文档去向

| 原路径／当前入口 | 分类 | 处理 |
|---|---|---|
| [.opencode/project.md](../../.opencode/project.md) | 工具／工作约定 | 保留工作约定；校正旧模块快照，设计入口指向统一设计；不是额外产品规格。 |
| [docs/INDEX.md](../INDEX.md) | 已归并／归档 | 当前索引／状态保留在链接位置，整理前版本另存归档。 |
| [docs/TODO.md](2026-10-07/docs/TODO.md) | 已归并／归档 | 原文已集中归档，原位置的冗余导航页已移出。 |
| [docs/conventions/DEV_CONVENTIONS.md](../conventions/DEV_CONVENTIONS.md) | 开发规范 | 保留规范；修正文中可直接确认的不合法 Java import 别名示例。 |
| [docs/conventions/GIT_COMMIT_CONVENTIONS.md](../conventions/GIT_COMMIT_CONVENTIONS.md) | 开发规范 | 保留规范；修正文中可直接确认的不合法 Java import 别名示例。 |
| [docs/conventions/TEST_CONVENTIONS.md](../conventions/TEST_CONVENTIONS.md) | 协作规范 | 保留，澄清代码修复不等于游戏验证通过。 |
| [docs/design/DESIGN_REVIEW_20260928.md](2026-10-07/docs/design/DESIGN_REVIEW_20260928.md) | 已归并／归档 | 原文已集中归档，原位置的冗余导航页已移出。 |
| [docs/design/LOADING_AND_SIMULATION.md](2026-10-07/docs/design/LOADING_AND_SIMULATION.md) | 已归并／归档 | 原文已集中归档，原位置的冗余导航页已移出。 |
| [docs/design/MAIDQUEST_MMW_ORDER_CHAIN.md](2026-10-07/docs/design/MAIDQUEST_MMW_ORDER_CHAIN.md) | 已归并／归档 | 原文已集中归档，原位置的冗余导航页已移出。 |
| [docs/design/MQ_MMW_WOODEN_PICKAXE_PHASE1.md](2026-10-07/docs/design/MQ_MMW_WOODEN_PICKAXE_PHASE1.md) | 已归并／归档 | 原文已集中归档，原位置的冗余导航页已移出。 |
| [docs/design/SPEC.md](2026-10-07/docs/design/SPEC.md) | 已归并／归档 | 原文已集中归档，原位置的冗余导航页已移出。 |
| [docs/design/WORLD_SIMULATION_DISCUSSION.md](2026-10-07/docs/design/WORLD_SIMULATION_DISCUSSION.md) | 已归并／归档 | 原文已集中归档，原位置的冗余导航页已移出。 |
| [docs/design/WORLD_SIMULATION_HANDOFF_20261001.md](2026-10-07/docs/design/WORLD_SIMULATION_HANDOFF_20261001.md) | 已归并／归档 | 原文已集中归档，原位置的冗余导航页已移出。 |
| [docs/project-status.md](../planning/STATUS.md) | 已归并／归档 | 当前索引／状态保留在链接位置，整理前版本另存归档。 |
| [docs/references/mc-neoforge/api-pitfalls.md](../references/mc-neoforge/api-pitfalls.md) | 技术参考 | 按 API／框架专题保留；不是业务设计，具体 API 随本地依赖核对。 |
| [docs/references/mc-neoforge/attachment-codec.md](../references/mc-neoforge/attachment-codec.md) | 技术参考 | 按 API／框架专题保留；不是业务设计，具体 API 随本地依赖核对。 |
| [docs/references/mc-neoforge/brain-behavior.md](../references/mc-neoforge/brain-behavior.md) | 技术参考 | 按 API／框架专题保留；不是业务设计，具体 API 随本地依赖核对。 |
| [docs/references/mc-neoforge/gui-system.md](../references/mc-neoforge/gui-system.md) | 技术参考 | 按 API／框架专题保留；不是业务设计，具体 API 随本地依赖核对。 |
| [docs/references/mc-neoforge/registration.md](../references/mc-neoforge/registration.md) | 技术参考 | 按 API／框架专题保留；不是业务设计，具体 API 随本地依赖核对。 |
| [docs/references/mc-neoforge/task-system.md](../references/mc-neoforge/task-system.md) | 技术参考 | 按 API／框架专题保留；不是业务设计，具体 API 随本地依赖核对。 |
| [docs/references/mc-neoforge/tlm-integration.md](../references/mc-neoforge/tlm-integration.md) | 技术参考 | 按 API／框架专题保留；不是业务设计，具体 API 随本地依赖核对。 |
| [docs/references/patterns.md](../references/patterns.md) | 技术参考 | 按 API／框架专题保留；不是业务设计，具体 API 随本地依赖核对。 |
| [docs/references/template-library.md](../references/template-library.md) | 技术参考 | 公开签名以 FennecLib API／源码为准；模板／旧名映射保留。 |
| [docs/references/touhoulittlemaid-26.1-update-20260926.md](2026-10-07/docs/references/touhoulittlemaid-26.1-update-20260926.md) | 依赖历史证据 | 保留当时版本／哈希／构建记录，不升级为当前构建或兼容通过。 |
| [fenneclib/README.md](../../fenneclib/README.md) | 模块介绍 | 保留安装／介绍；补统一开发文档入口，避免当完整开发状态。 |
| [fenneclib/docs/API.md](../../fenneclib/docs/API.md) | 公开接口参考 | 保留现有签名；标明实现契约与目标设计区别，本轮不宣称逐方法重新验收。 |
| [fenneclib/docs/CHANGELOG.md](../../fenneclib/docs/CHANGELOG.md) | 版本历史 | 原样保留；不改版本，不虚构发布记录。 |
| [fenneclib/docs/INDEX.md](../../fenneclib/docs/INDEX.md) | 已归并／归档 | 当前索引／状态保留在链接位置，整理前版本另存归档。 |
| [fenneclib/docs/TODO.md](../../fenneclib/docs/design/WEIGHTED_BEHAVIOR.md) | 专项技术设计 | 保留算法解耦的具体目标；总跟踪 I10，不复制另一份状态。 |
| [maidmorework/AGENTS.md](../../maidmorework/AGENTS.md) | 执行约束 | 原样保留；禁止主动游戏／自动化测试要求仍有效。 |
| [maidmorework/README.md](../../maidmorework/README.md) | 模块介绍 | 保留安装／介绍；补统一开发文档入口，避免当完整开发状态。 |
| [maidmorework/docs/API.md](../../maidmorework/docs/API.md) | 公开接口参考 | 保留现有签名；标明实现契约与目标设计区别，本轮不宣称逐方法重新验收。 |
| [maidmorework/docs/CHANGELOG.md](../../maidmorework/docs/CHANGELOG.md) | 版本历史 | 原样保留；不改版本，不虚构发布记录。 |
| [maidmorework/docs/INDEX.md](../../maidmorework/docs/INDEX.md) | 已归并／归档 | 当前索引／状态保留在链接位置，整理前版本另存归档。 |
| [maidmorework/docs/bugs/BUG-016.md](2026-10-07/maidmorework/docs/bugs/BUG-016.md) | 历史修复证据 | 保留旧类名、当时 API 与根因；不当作当前已复测结论。 |
| [maidmorework/docs/deprecated/spblock.md](2026-10-07/maidmorework/docs/deprecated/spblock.md) | 废弃方案 | 保持已废弃状态，不进入开发清单。 |
| [maidmorework/docs/design/MINE_REDESIGN.md](2026-10-07/maidmorework/docs/design/MINE_REDESIGN.md) | 已归并／归档 | 原文已集中归档，原位置的冗余导航页已移出。 |
| [maidmorework/docs/design/MINE_SPIRAL_ALGORITHM.md](../../maidmorework/docs/design/MINE_SPIRAL_ALGORITHM.md) | 算法参考 | 保留坐标公式；不是新地皮网格或运行验收证据。 |
| [maidmorework/docs/development-handoffs/20260926-1620-mmw-workshop-library-forest.md](2026-10-07/maidmorework/docs/development-handoffs/20260926-1620-mmw-workshop-library-forest.md) | 历史交接／审查 | 保留正文与原有修改，增加历史边界；设计看专题，缺陷当前状态看 C／I／V。 |
| [maidmorework/docs/development-handoffs/20260926-mmw-manual-review-fix-plan.md](2026-10-07/maidmorework/docs/development-handoffs/20260926-mmw-manual-review-fix-plan.md) | 历史交接／审查 | 保留正文与原有修改，增加历史边界；设计看专题，缺陷当前状态看 C／I／V。 |
| [maidmorework/docs/development-handoffs/20260926-mq-mmw-combined-review.md](2026-10-07/maidmorework/docs/development-handoffs/20260926-mq-mmw-combined-review.md) | 历史交接／审查 | 保留正文与原有修改，增加历史边界；设计看专题，缺陷当前状态看 C／I／V。 |
| [maidmorework/docs/development-handoffs/20260927-mmw-mq-unification-batch-purchasing.md](2026-10-07/maidmorework/docs/development-handoffs/20260927-mmw-mq-unification-batch-purchasing.md) | 历史交接／审查 | 保留正文与原有修改，增加历史边界；设计看专题，缺陷当前状态看 C／I／V。 |
| [maidmorework/docs/issues/KNOWN_ISSUES.md](2026-10-07/maidmorework/docs/issues/KNOWN_ISSUES.md) | 关闭记录 | “当前无未解决”仅限原文件当时列出的条目，不代表全项目无问题。 |
| [maidmorework/docs/issues/TEST_LOGGING.md](2026-10-07/maidmorework/docs/issues/TEST_LOGGING.md) | 测试证据 | 保留按轮记录，当前汇总见 V 清单；不把旧反馈冒充本轮复现。 |
| [maidmorework/docs/issues/TEST_NOTES.md](2026-10-07/maidmorework/docs/issues/TEST_NOTES.md) | 测试证据 | 保留按轮记录，当前汇总见 V 清单；不把旧反馈冒充本轮复现。 |
| [maidmorework/docs/issues/TODO_V1.md](2026-10-07/maidmorework/docs/issues/TODO_V1.md) | 已归并／归档 | 原文已集中归档，原位置的冗余导航页已移出。 |
| [maidquest/docs/API.md](../../maidquest/docs/API.md) | 公开接口参考 | 保留现有签名；标明实现契约与目标设计区别，本轮不宣称逐方法重新验收。 |
| [maidquest/docs/CHANGELOG.md](../../maidquest/docs/CHANGELOG.md) | 版本历史 | 原样保留；不改版本，不虚构发布记录。 |
| [maidquest/docs/INDEX.md](../../maidquest/docs/INDEX.md) | 已归并／归档 | 当前索引／状态保留在链接位置，整理前版本另存归档。 |
| [maidquest/docs/TEST_LOGGING.md](2026-10-07/maidquest/docs/TEST_LOGGING.md) | 测试证据 | 保留按轮记录，当前汇总见 V 清单；不把旧反馈冒充本轮复现。 |
| [maidquest/docs/design/QUEST_WORLD_DATA_AND_DISMANTLE.md](2026-10-07/maidquest/docs/design/QUEST_WORLD_DATA_AND_DISMANTLE.md) | 已归并／归档 | 原文已集中归档，原位置的冗余导航页已移出。 |
| [maidquest/docs/development-handoffs/20260926-1620-mq-order-product.md](2026-10-07/maidquest/docs/development-handoffs/20260926-1620-mq-order-product.md) | 历史交接／审查 | 保留正文与原有修改，增加历史边界；设计看专题，缺陷当前状态看 C／I／V。 |
| [maidquest/docs/development-handoffs/20260926-mq-manual-review-fix-plan.md](2026-10-07/maidquest/docs/development-handoffs/20260926-mq-manual-review-fix-plan.md) | 历史交接／审查 | 保留正文与原有修改，增加历史边界；设计看专题，缺陷当前状态看 C／I／V。 |

## 新增的有效文档

| 目录 | 职责 |
|---|---|
| [design/current/README.md](../design/current/README.md) 及其九个专题 | 系统化设计正文；明确已确认、推导、未决、旧设计保留 |
| [design/current/DECISIONS.md](../design/current/DECISIONS.md) | 新确认与替代依据 |
| [planning/OPEN_QUESTIONS.md](../planning/OPEN_QUESTIONS.md) | Q01–Q38，尚未讨论完的功能 |
| [planning/CONFLICTS.md](../planning/CONFLICTS.md) | D：旧规则替代；C：当前代码差距；旧问题状态校正 |
| [planning/IMPLEMENTATION.md](../planning/IMPLEMENTATION.md) | I：实施和风险；V：运行验收 |
| [archive/2026-10-07/README.md](2026-10-07/README.md) | 归档说明和历史入口 |

## 不丢失、不重复维护

归档保留整理前正文，只加历史说明和重定位相对链接。开发交接与历史测试／问题记录已实际集中归档；模块 CHANGELOG 仍留在各模块 docs。当前状态不再从历史记录重复维护。旧标题中的“已确认／待实现／已修复”均受日期和对应批次限制。

本次未解决的设计冲突继续保留 Q 编号；已经确认的公共买断资金来源、二维独立计算等从旧未决清单移出。阅读当前规则不需要再逐份拼接历史文档。

