# 新旧设计与当前实现冲突

> 静态核对：2026-10-07，使用当前工作区（包含原有未提交改动）。本轮只整理文档，未修改这些实现。下文“未见”指本次检索范围和已读入口，不是运行验证。
> [设计正文](../design/current/README.md) · [未决功能](OPEN_QUESTIONS.md) · [实施清单](IMPLEMENTATION.md)

## A. 旧规则退出有效规格

2026-10-11 Q39.3：用户提出二维切片及产业内部抽象位置后，旧“后台算到哪里就在哪里出现”不能解释为产业内也已有精确三维坐标。室外位置与产业内归属须分别恢复；入口来源已按 Q39.3.b 确认（产业区域边界上可达的通行格都算入口），剩余高度口径、失效处置与产业内安全落点待 Q39.3.b 剩余项／Q39.3.c；旧路网与切片关系待 Q39.3.d，不擅自删除既有可达性规则。

2026-10-11 Q39.1.f：此前独立拒绝阈值方案退出，统一使用行动权重。雇员不能拒收上级派发任务，但可以暂不执行；上级派工本身也受员工状态影响。任务延期允许发生，具体恢复和改派尚待讨论。这是新设计确认，不代表代码已完成。

2026-10-11：生理需求不再无条件优先，需求和经历影响行动权重，缺钱可促使带病工作。旧强制觅食和觅食失败自动恢复工作须按 Q39.1.h 衔接；拒绝恢复只暂时搁置。此为设计更新，不是代码修复或运行验证。

| ID | 旧来源／规则 | 当前规则／处理 | 性质 |
|---|---|---|---|
| D01 | SPEC §8：贡献点锚定玩家箱子实物并回流 | MQ 财产挂件数字余额；公共收购／奖励／上贡奖金凭空发放 | 明确替代 |
| D02 | 订单链：个人负债、公共仓库余额与有限透支 | 不负债，个人委托预付；公共买断不扣任何人余额 | 明确替代 |
| D03 | 订单链：制作 1.2M、人工 0.2M | 成品价值 V，售价 10V/9，加工费 V/9 归管理员，工资另算 | 明确替代 |
| D04 | SPEC：6 点起床、两餐制、饿死、工作时禁睡 | 7 点起床，30% 觅食，缓慢分档不致死，生理需求优先 | 明确替代 |
| D05 | 早期世界讨论：外部势力完整模拟、商队连续过路 | 聚落接近生成／假工作，外部队伍距离概率到访 | 明确替代 |
| D06 | 加载草案：工坊能否后台仍待选择；后台不取放居民物品 | 已允许后台并维持同工时与需求消耗；具体交接仍待细化 | 部分被替代，保留技术约束 |
| D07 | 旧四仓分类、矿井独占仓库、27 格缓存 | 所有工程中心统一无限缓存，公共有限；MQ 按单托管单列业务用途 | 明确替代 |
| D08 | 旧讨论：道路重叠阻断、建筑工自行运料、工程损坏即取消 | 自动连接／高等级接管、运送员供料、中心恢复原库存 | 明确替代 |
| D09 | 订单链／模块索引：离职或停止工作就撤材料单 | 居民动作不自动撤已发布单；制作单与材料单独立 | 明确替代 |
| D10 | 旧设计：管理员可常规换绑、居民自己选址 | 管理员是产业出资所有者；玩家划地，资格证招标 | 测试机制不成为正式规则 |
| D11 | 旧 MQ 实施：完成货仍属于交付者，死亡按交付者处置 | 完成未领属于发布者储备私产；发布者死亡应充公 | 业务权属冲突 |
| D12 | SPEC：伴侣优先继承产业，复活可恢复居民 | 当前管理员死亡产业充公；复活／其他私产继承尚未对齐 | 已定产业规则优先，Q32／Q35 保留 |
| D13 | 地皮笔记：7n、7n+k+1、7／14／16／23 同时标确认 | 保留网格框架，冻结尺寸换算公式 | 原记录内部矛盾，Q01 |
| D14 | 接续摘要仍说“其他工种另定中断结算” | 10 月 6 日按招募类／交付类统一处置，不按工种重复定规则 | 同步最新逐次确认 |
| D15 | 矿井记录：任意光源、45 槽控制行、鱼骨矿道待新增 | 火把口径、真 UI 控件、已有分支矿道代码 | 后续修订／代码使旧状态失效 |

旧源文均见 [归档及文档台账](../archive/DOCUMENT_REGISTER.md)，当前入口不再并列展示这些规则。

## B. 目标设计与实现差距

源码链接用于定位文件，方法名作为稳定检索锚；行号不复制进易漂移的正文。每条给触发、差异和后续去向。

| ID | 目标／触发 | 当前代码证据与差异 | 后续 |
|---|---|---|---|
| C01 | 完成委托未领取时取消或拆板；发布者死亡 | [QuestService](../../maidquest/src/main/java/com/fennecmomo/maidquest/service/QuestService.java) 的 `cancelInternal→returnEscrow` 以 claimant 找返货者；`onMaidDeath` 按 claimant 遍历并可重开带托管完成单，不是按发布者产业充公链 | I02；部分中断返货口径受 Q12／Q13 约束 |
| C02 | 执行中禁止收起；外部中断超 3000 tick 才自动放弃 | [MaidQuest](../../maidquest/src/main/java/com/fennecmomo/maidquest/MaidQuest.java) 的 ToItem 监听调用 `onMaidStored`；[QuestService](../../maidquest/src/main/java/com/fennecmomo/maidquest/service/QuestService.java) 立即 abandon/reopen，死亡也有立即重开路径；未见通用 3000 tick 分类计时 | I02；Q14 先澄清语义 |
| C03 | 产业仓库玩家只能看 | [WarehouseMenu](../../maidmorework/src/main/java/com/fennecmomo/maidmorework/project/center/WarehouseMenu.java) 的 `clicked`／`quickMoveStack` 允许存取；[WorkshopMenu](../../maidmorework/src/main/java/com/fennecmomo/maidmorework/crafting/WorkshopMenu.java)、[ForestMenu](../../maidmorework/src/main/java/com/fennecmomo/maidmorework/forest/ForestMenu.java) 也含可操作视图 | I03；独立 MMW 模式适用范围 Q28 |
| C04 | 管理员是产业所有者，普通换岗不自动撤单 | [WorkshopMenu](../../maidmorework/src/main/java/com/fennecmomo/maidmorework/crafting/WorkshopMenu.java) 换绑定调用 `cancelManagerMaterials`；[ProjectCenterManager](../../maidmorework/src/main/java/com/fennecmomo/maidmorework/project/center/ProjectCenterManager.java) 也有批量撤材料单调用；现有绑定尚属测试机制 | I04；正式产权／招标替换，非本轮改代码 |
| C05 | 工坊前后台相同工时、作息、生理暂停 | [WorkshopInstance](../../maidmorework/src/main/java/com/fennecmomo/maidmorework/crafting/WorkshopInstance.java) 每 10 tick `tickBackgroundCraft` 直接推进一步；[CraftingBehavior](../../maidmorework/src/main/java/com/fennecmomo/maidmorework/crafting/CraftingBehavior.java) `tickCraft` 到工作台后执行一步；这两个入口未见共享工时预算与 7／18／20 点作息控制 | I05；后台分支存在不等于统一模拟完成 |
| C06 | MQ 财产挂件、预付、数字工资 | [ModAttachments](../../maidquest/src/main/java/com/fennecmomo/maidquest/ModAttachments.java) 只注册 `QUEST_ASSIGNMENT`；已读发布／交付流程未包含新财产账。现有实物托管不是金额代管 | I01；金额退出受 Q12／Q15／Q16 约束 |
| C07 | 公共仓库有限容量、专用箱、收售和运送员 | 本次三业务模块类名检索仅发现现有中心 Warehouse 系列；[ProjectCenterInstance](../../maidmorework/src/main/java/com/fennecmomo/maidmorework/project/center/ProjectCenterInstance.java) 是中心无限缓存，不能冒充公共仓库 | I03／I06；新系统缺口 |
| C08 | 新剧本、资格证招标、网格地皮 | [Territory](../../maidtown/src/main/java/com/fennecmomo/maidtown/territory/Territory.java) 半径 50；[TerritoryManager](../../maidtown/src/main/java/com/fennecmomo/maidtown/territory/TerritoryManager.java) 运行时 Map，以篝火为基础；不是新网格地皮系统 | I07；Q01–Q11，MaidTown 暂缓开发 |
| C09 | 真实路网、后台居民沿路线运输和道路施工 | 已读生产行为仍调用实体导航；未检索到独立 Road 路网系统。矿井 `checkSealsOneLayer` 只是可参考的复核，不是道路实现 | I06；Q20–Q22 |
| C10 | 商铺按 10%／60% 补货、结算时库存核验 | [WorkshopInstance](../../maidmorework/src/main/java/com/fennecmomo/maidmorework/crafting/WorkshopInstance.java) `tickStock` 按 target 补差额，是旧有限备货基础；未见完整新双阈值商铺交易链 | I04；与售货员等系统一起对齐 |
| C11 | 维度卸载不能影响其他维度正常拆除 | [ProjectCenterManager](../../maidmorework/src/main/java/com/fennecmomo/maidmorework/project/center/ProjectCenterManager.java) `onLevelUnload` 仍设置全局 `shuttingDown=true`，`clearAll` 才复位；[ProjectCenterBlockEntity](../../maidmorework/src/main/java/com/fennecmomo/maidmorework/project/center/ProjectCenterBlockEntity.java) 拆除读该标志 | 静态风险仍在，I11；未运行复现 |
| C12 | 饥饿、作息、休息在玩家居民前后台一致 | 现有 MQ／MMW 行为入口未见新需求调度；旧 MaidTown 需求代码不能直接当新模型验收 | I05；Q23／Q31 |
| C13 | 未加载不能直接清除个人工程 | [ProjectCenterManager](../../maidmorework/src/main/java/com/fennecmomo/maidmorework/project/center/ProjectCenterManager.java) 的 `sweepOrphanProjects` 对 `owner == null` 仍加入删除列表并注销工程；当前查不到实体不证明工程结束 | I11；与林场已改路径分开处理 |

## C. 旧问题单的状态校正

| 原项目 | 本次静态事实 | 新状态 |
|---|---|---|
| 总 TODO F5：工程基类没仓库 | `ProjectCenterInstance` 已有 `warehouse` Codec、deposit／take 方法 | 旧描述过时；权限和公共仓库仍未完成 |
| 总 TODO F8：林场批量取出后未退余货 | `ForestManagerBehavior.tickDeliver` 现逐堆 `takeFirstFromWarehouse`，插不完的余量回库 | 原特定丢物路径已改；未做游戏回归，不能保留“确定仍存在” |
| 总 TODO F9：林场查不到成员就删除 | 当前 `tickRelease` 对查得到实体才 remove，旧描述至少部分过时；个人工程仍有 C13 | 不能一笔判全修好；普通中心其他分支仍需分别查 |
| 总 TODO I1：需新增 FishboneMinePlanner | `MineInstance.buildTunnelPlan`／`MineTunnelProject` 已有主道与分支 | 改为几何覆盖核对，非从零开发 |
| MQ 索引：全局化／安全拆板“待实施” | `QuestBoardData`、`QuestLostItems`、拆板 payload 已有代码 | 有实现待验证，新规则另需改造 |
| 旧订单链：没有制作、接单资格、全局配置、按单托管 | 现有 crafting、eligibility、COMMON 配置及每单库存已有代码 | 旧 9 月 25 日实现表停用 |
| 旧矿井 TODO：工具等级／效率全未做 | 矿井行为和工具选择已有对应路径；完整适配仍需专项核对 | 不再当整项从零待做 |

## 审查范围与限制

本次逐项核对新设计涉及的关键入口和旧待办高风险状态；没有对所有 Java 文件做完整逻辑审计。历史 F／L／U／S 问题单保留为证据，未逐条复查的不能自动关闭。接口参考、第三方源码说明和日志仅分类，不宣称已逐行验证全部 API。实际构建、游戏联调、旧存档恢复和 UI 行为均未在本轮验证。

