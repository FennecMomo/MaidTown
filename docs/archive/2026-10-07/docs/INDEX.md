> 历史索引快照，2026-10-07 已被新入口替代。

# MaidTown 文档总目录

> 最后更新：2026-10-01

---

## 一、项目文档

| 文档 | 说明 |
|------|------|
| [TODO.md](TODO.md) | 全项目待办总览（唯一总入口） |
| [project-status.md](project-status.md) | 模块现状、Git状态、技术栈、架构决策 |
| [conventions/DEV_CONVENTIONS.md](../../../conventions/DEV_CONVENTIONS.md) | 代码风格（//注释、Allman括号、禁用长限定类名） |
| [conventions/GIT_COMMIT_CONVENTIONS.md](../../../conventions/GIT_COMMIT_CONVENTIONS.md) | 提交格式（中文摘要+新增/修改/删除） |
| [conventions/TEST_CONVENTIONS.md](../../../conventions/TEST_CONVENTIONS.md) | 测试协作规范（操作人与 AI 的分工流程） |
| [design/SPEC.md](design/SPEC.md) | 游戏设计文档（GDD v2.4-review，新增加载边界草案） |
| [design/WORLD_SIMULATION_HANDOFF_20261001.md](design/WORLD_SIMULATION_HANDOFF_20261001.md) | 世界模拟重设计接续摘要：当前确认规则、已撤销设想、暂停点与讨论边界；新会话先读 |
| [design/WORLD_SIMULATION_DISCUSSION.md](design/WORLD_SIMULATION_DISCUSSION.md) | 世界模拟逐次讨论记录：前后台、居民、仓库、商铺、路网与工地；较新确认覆盖早期设想 |
| [design/LOADING_AND_SIMULATION.md](design/LOADING_AND_SIMULATION.md) | MQ × MMW 区块卸载、持久账本、现场动作与抽象加工的修订草案（待讨论） |
| [design/DESIGN_REVIEW_20260928.md](design/DESIGN_REVIEW_20260928.md) | 现有代码与设计文档审查；列出冲突、实现风险和待拍板问题 |
| [design/MAIDQUEST_MMW_ORDER_CHAIN.md](design/MAIDQUEST_MMW_ORDER_CHAIN.md) | 历史订单链讨论记录；铁镐经济、矿场工分与公共仓库仍待实现 |
| [design/MQ_MMW_WOODEN_PICKAXE_PHASE1.md](design/MQ_MMW_WOODEN_PICKAXE_PHASE1.md) | 历史木镐第一阶段计划；部分规则已被工程中心设计替代 |

## 二、子模组文档

### FennecLib
[../fenneclib/docs/](../../../../fenneclib/docs/) — API参考 / CHANGELOG / TODO / 包结构

### MaidMoreWork
[../maidmorework/docs/](../../../../maidmorework/docs/) — INDEX / API / CHANGELOG / V1待办 / 已知问题 / Bug记录 / 矿井设计 / 测试清单 / 废弃方案

### MaidQuest
[../maidquest/docs/](../../../../maidquest/docs/) — INDEX / API / TEST_LOGGING / CHANGELOG

## 三、开发参考（`docs/references/`）

### MC/NeoForge 核心

| 文档 | 内容 |
|------|------|
| [mc-neoforge/registration.md](../../../references/mc-neoforge/registration.md) | 注册系统（方块/物品/实体/事件/资源） |
| [mc-neoforge/brain-behavior.md](../../../references/mc-neoforge/brain-behavior.md) | Brain行为系统（生命周期/Picker/Activity/Search） |
| [mc-neoforge/task-system.md](../../../references/mc-neoforge/task-system.md) | 任务系统（Claim/Execute/Submit/伐木流程） |
| [mc-neoforge/tlm-integration.md](../../../references/mc-neoforge/tlm-integration.md) | TLM集成（EntityMaid/IMaidTask/Brain/拾取） |
| [mc-neoforge/attachment-codec.md](../../../references/mc-neoforge/attachment-codec.md) | 持久化（Attachment/多态Codec/序列化陷阱） |
| [mc-neoforge/gui-system.md](../../../references/mc-neoforge/gui-system.md) | GUI系统（Screen/Container/布局/滚动/渲染） |
| [mc-neoforge/api-pitfalls.md](../../../references/mc-neoforge/api-pitfalls.md) | MC 26.x API陷阱速查表 |

### 通用开发

| 文档 | 内容 |
|------|------|
| [template-library.md](../../../references/template-library.md) | FennecLib UI模板库（API+旧名→新名映射） |
| [patterns.md](../../../references/patterns.md) | 通用模式（背包/捡东西/进食） |

## 四、工具

| 目录 | 内容 |
|------|------|
| [scripts/](../../../scripts/) | 文档格式化脚本（Markdown 代码块 K&R→Allman 花括号转换） |
| [templates/](../../../templates/) | 代码模板（CustomPayload.java） |

## 五、AI 工作记忆

| 文件 | 内容 |
|------|------|
| [.opencode/project.md](../../../../.opencode/project.md) | 项目记忆：架构速记、开发规范、发布流程（更新版本/发布新版本） |
| [.opencode/tools/gh-release.ps1](../../../../.opencode/tools/gh-release.ps1) | GitHub Release 发布脚本（自动读取本机凭据，不落盘） |

---

### 从哪里开始？

- **新手上路** → [design/SPEC.md](design/SPEC.md) → [project-status.md](project-status.md)
- **开发新功能** → [conventions/DEV_CONVENTIONS.md](../../../conventions/DEV_CONVENTIONS.md) → 对应参考文档
- **查 API/模式** → 上方参考文档按需查阅
- **查陷阱** → [api-pitfalls.md](../../../references/mc-neoforge/api-pitfalls.md)
- **看进度/待办** → [TODO.md](TODO.md)
