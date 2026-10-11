> 文档分类（2026-10-07）：历史交接／审查证据。下文方案、命令、缺陷及验收状态仅对应原批次；不构成当前实施授权，未复核条目不自动关闭。 [统一入口](../../../../../INDEX.md).

# MaidQuest 与 MaidMoreWork 联合静态审查（2026-09-26）

## 当前状态

- MQ 与 MMW 均以 OpenCode Go / DeepSeek V4.1 Flash `max` 实现，最终原样 `./gradlew jar` 编译打包成功；独立 Codex GPT-6 Sol high 审查只读，四份审查 JSONL 均无工具调用。
- 用户决定先完成 MMW、合并两仓库审查，再手动测试，问题在收到手动反馈后的下一轮处理。本轮不继续修复已审查缺陷。
- **木镐订单循环尚不能视为跑通。** 审查发现木板重复预留、非原子扣料、取消后子单继续供货，以及林场交货失败时可能丢失原木等确定代码路径。游戏内尚未验证。
- 桌面 `女仆模组联调.bat` 实际从 MQ 开发类目录加载 MQ、从 `run-shared/mods/maidmorework-0.1.4.jar` 加载 MMW。新 MMW JAR 已复制到该目录，sha256 `ba443853426263162b4bfe94479c316e45fd86520d7af16437327150d2de9b2b`；旧 JAR 备份于 `run-shared/mods-backup/maidmorework-0.1.4-pre-20260926-handoff.jar`。MQ JAR 未复制进 mods，以免重复加载。
- 由于审查已指出物品损耗与中心存档风险，手动验证请使用新的测试世界或可恢复的存档副本。启动游戏、实际 UI 和物品流仍需用户确认。

## 审查结论全文

下列四份结论按仓库与模块排列。MMW 的工作台卸载和过时配方问题在两批中重复出现，属于同一缺陷，不应重复计数。林场审查首次并行进程退出码 143，单独重跑成功后才采用以下结论。

## MaidQuest

主人，小夜只依据提供的代码做了静态审查。**中心单的领取和取消已改为查询当前管理女仆，但材料单的发布与复用仍有缺口**，因此暂不能确认“材料单由当前管理女仆操作”已完整落实。

### 发现的问题

1. **高：中心材料单发布未验证发布者身份。** `src/main/java/com/fennecmomo/maidquest/service/QuestService.java` 的 `requestMaterial(..., beneficiaryId)` 只验证条件和数量，随后用传入的 `requester`、`beneficiaryId` 创建并发布订单；没有调用 `MaterialBeneficiaryRegistry.represents`。当旧管理员、工匠或其他调用方在管理女仆更换后继续传入该中心 UUID 时，MQ 仍会接受其代表中心发布的缺料单。后续领取、取消权限检查不能阻止这笔错误订单产生。

2. **高：会话绑定可让已卸任管理员继续通过权限检查。** `src/main/java/com/fennecmomo/maidquest/api/MaterialBeneficiaryRegistry.java` 的 `represents` 在 `MANAGERS` 中命中便立即返回 `true`，即使注册回调依据持久中心数据已判定该女仆不再管理中心。当管理关系已更换、旧会话绑定尚未覆盖或解除时，旧管理员仍可通过 `QuestService.canClaimMaterial` 和 `cancelMaterial`，领取托管货物或取消未完成单。`bindManager` 的使用说明要求集成方在换人时更新绑定，但当前双通道“任一成立”不足以独立保证“当前”身份。

3. **中：旧材料入口仍可复用另一受益中心的子单。** `src/main/java/com/fennecmomo/maidquest/service/QuestService.java` 的 `materialFor(..., beneficiaryId)` 在参数为 `null` 时跳过归属比较；无中心参数的 `materialFor`、`requestMaterial` 重载均走这条路径。若旧调用方与中心调用方使用相同 `sourceId` 和条件，旧调用方会拿到该中心已有订单，而旧 requester 又无权领取中心单货物。第一轮“复用时检查收货身份”的问题在新五参数入口得到处理，在兼容入口仍存在。

4. **中：去重未比较需求来源类型。** 同文件 `materialFor` 比较了 `parentId`、条件和受益中心，却未比较 `MaterialQuest.source()`。同一中心对相同 `sourceId`、相同材料分别提出 `ORDER` 与 `STOCK` 需求时，第二次请求会复用第一张单，返回的来源和数量仍属第一张单。

5. **中：候选目录可能漏掉服务端认可的产物。** `src/main/java/com/fennecmomo/maidquest/service/CraftingCatalog.java` 的 `compute` 将展示候选截为排序后的前 8192 项，而 `isProduct` 用未截断的全集校验。当前配方产物超过该数时，余下物品可通过服务端校验，却永远不会出现在委托板选择器中。分页限制应限制每包大小，不能悄悄缩小可选全集。

### 六项复审与局限

第 2 项伐木回退核对条件、第 3 项完成单剩余量固定为 0、第 6 项材料条件拒绝空集及超界候选，代码中已有对应处理。第 4 项已增加依赖配方重载的缓存清理；第 5 项已增加渲染时重查布局，但 `CommissionModeClient.placeButton` 找不到安全位置时仍直接放到屏幕角落，**无遮挡效果需要主人画面确认**。第 1 项的领取入口已统一检查中心管理身份，发布、兼容复用和会话绑定仍有上述问题。

资料包含 MQ 代码及 MMW 旧实现，未包含 MMW 后续中心绑定与调用代码；因此无法确认实际集成是否会触发这些条件，也不能据交接记录中的 `./gradlew jar` 成功推断游戏内行为。小夜遵照要求未调用工具、运行验证或修改文件。

## MaidMoreWork：工程中心与制作物品流

主人，小夜只依据所给代码做了静态审查。**这批工程中心与制作流尚未落实木镐闭环**；其中有确定会造成材料损耗、订单卡住或取消后物品归属错误的路径。

### 高风险

1. **一把木镐仍只会预留一根原木，并可能在制作时损耗木板。** [WorkshopInstance.java](/mnt/d/ModProduce/MaidTown/maidmorework/src/main/java/com/fennecmomo/maidmorework/crafting/WorkshopInstance.java) 的 `collectDemand` 将木镐所需的 3 块木板、木棍所需的 2 块木板分别展开为一根原木；`refreshReservations` / `pendingMaterialNeeds` 却让第二项需求重复计算第一项已预留的同一根原木。做出 4 块木板、再消耗 2 块制作木棍后，仅剩 2 块。`plan` 可将这同一堆 2 块木板选给木镐的 3 个输入格；`executeCraftStep` 逐项扣料，扣掉前 2 块后第三次失败，且不回滚。触发条件正是交接要求的木镐配方链；影响是原木低订、木板实物损失、订单无法完成。

2. **执行工匠可以在没有可用管理员时继续制作。** [CraftingBehavior.java](/mnt/d/ModProduce/MaidTown/maidmorework/src/main/java/com/fennecmomo/maidmorework/crafting/CraftingBehavior.java) 的 `hasDuty` 和 `tickCraft` 只检查工匠身份、订单与工作台，没有检查中心管理员是否在线；[WorkshopInstance.java](/mnt/d/ModProduce/MaidTown/maidmorework/src/main/java/com/fennecmomo/maidmorework/crafting/WorkshopInstance.java) 的 `tick` 也照常预留材料。管理员卸载或缺席而工匠仍在时，工程继续消耗中心资源，违反“无可用管理员则工程等待”的新设计。

3. **工作台区块卸载会永久清除绑定。** `WorkshopInstance.hasValidTable` 用 `tables.removeIf(pos -> !level.isLoaded(pos) || ...)` 同时删除卸载和失效的工作台。绑定工作台所在区块暂时卸载后，只要资格检查或制作行为调用该方法，位置便从持久列表移除；区块重载也无法自动恢复工作。这与“卸载只暂停”相冲突。

4. **配方 ID 保持不变但产物变化时，会消耗原料并制作错误物品。** `WorkshopInstance.hasUsableRecipe` 仅确认 ID 仍指向某条工作台配方；`executeCraftStep` 仅核对配方 ID 和非空输出，均未核对当前输出是否仍为 `WorkOrder.product`。数据包更新改变该 ID 的产物后，中心仍把旧知识视为可用，真实扣料后将错误产物存入工程预留，订单无法交付。

5. **取消制作单不会取消该工程的材料子单。** `WorkshopInstance.sourceId` 为玩家单使用 `WorkOrder.id()` 生成 `mmw:craft:order:…`；[CraftingQuestIntegration.java](/mnt/d/ModProduce/MaidTown/maidmorework/src/main/java/com/fennecmomo/maidmorework/crafting/CraftingQuestIntegration.java) 的 `onCancelled` 却用 `CraftingQuest.id()` 生成查询 ID，两者不同，因此找不到相应子单。此外它向 `QuestApi.cancelMaterial` 传的是中心 UUID，而所给 MQ API 说明中心单须由当前管理女仆取消。根单取消后，材料单仍可能继续被供货。

6. **取消时可能漏收工匠携带的订单成品。** `CraftingBehavior.tickCraft` 将带订单标记的成品放入执行工匠背包；`CraftingQuestIntegration.onCancelled` 只对 `order.claimedBy()` 指向的女仆调用 `recoverMarked`。当管理女仆认领、另一名工匠制作时，取消只检查管理员背包，工匠身上的成品不会退回中心，之后换中心仍可能携带旧订单物资。

7. **背包满一次后，已制作的成品可能永久滞留在预留中。** `tickCraft` 插入女仆背包失败时用 `addToReserved` 放回成品；但下一次只在 `executeCraftStep` 成功之后才调用 `extractOutput`。如果此时已无原料可做下一步，即使背包腾空，`nextCraftStep` 返回空，既有成品也不会再次取出交付。

### 中风险

8. **设库存目标为 0 后，既有备货工程仍会继续生产。** `WorkshopInstance.tickStock` 对 `target <= 0` 直接 `continue`，没有移除已有的 `stock` 订单；`firstActiveOrder` 仍选取它，`refreshReservations` 仍为它预留材料。触发条件是在备货工程创建后把目标改为 0；影响是不能按界面设置停产。

9. **缺料单的在途量未按物品条件分别核对。** `WorkshopInstance.sourceId` 对同一制作工程的不同原料使用同一个 ID；`CraftingQuestIntegration.inTransit` 只核对 `receiverId`，将该来源的所有未取消子单数量相加。一个需要两种非可制作原料的配方，第一种材料的在途量会抵扣第二种材料的缺口，导致第二种材料单不发布。木镐的两项原木需求也受这一重复抵扣影响。

10. **管理女仆领取材料后可能把其他订单的同类物品一并转入工坊。** `CraftingBehavior.tickCollectMaterials` 只在 `claimMaterial` 返回正数后调用 `depositCarried`；后者按 `acceptedItems` 的物品 ID 扫描并取出背包里所有匹配堆，没有限定本次领取数量或检查订单标记。若管理员原已携带另一订单的同类材料，这些实物也会进入当前中心仓库，造成跨单混货。

本轮未调用工具，也未运行任何验证。以上结论限于提供的代码与 MQ API 资料；不把尚未进行的游戏验证列为缺陷。

## MaidMoreWork：林场、矿井与管理员绑定

主人，小夜只依据给定代码做了静态审查，没有调用工具。**本批存在会影响物品守恒、林场派工和管理员归属的高风险缺陷。**以下按触发条件列出确切证据；没有把游戏内未验证或上游 MQ 的已知问题算作 MMW 缺陷。

### 高风险

1. **交货失败时可能丢失原木。** `ForestManagerBehavior.tickDeliver` 先用 `forest.takeFromWarehouse(...)` 一次取出多个堆；逐堆插入管理员背包时，若某堆插入失败，只把该堆退库并 `break`。触发条件是订单需从多个仓库堆取货，且插入中途失败；列表中尚未处理的堆已离开仓库，也没有退回路径。

2. **委托模式下仍可无单砍树。** `ChopBehavior.commissionBlocksFreeChopping` 只判断归属中心是否为 `ForestInstance`，不检查成员是否有派工或林场是否有有效订单。`checkExtraStartConditions` 随后可走 `ensureCenter` 和 `assignOrResume`。触发条件是女仆仍归属林场但没有派工；影响是继续创建或执行砍树工程，违反无单待命要求。

3. **借出的斧子装备后无法按记录回收。** `ChopBehavior.equipAxe` 会把背包斧子移到主手或副手；`ForestInstance.recoverTools` 的 `takeFromMaid` 只搜索 `getAvailableInv(false)` 的槽位。订单结束时若斧子已装备，工具记录保留、斧子留在女仆身上，林场库存无法收回。

4. **卸载的成员会失去释放路径。** `ForestManagerBehavior.tickRecruit` 在 `level.getEntity(memberId)` 查不到女仆时直接 `forest.removeMember(memberId)`；但 `ForestInstance` 基类的中心归属还保存在 `savedHomes`，女仆附件也未清除。触发条件是成员区块暂时卸载；重新加载后，该女仆仍归属原林场，却不在招募成员列表中，`tickRelease` 也不会为她执行 `leaveCenter`，可能长期无法被重新招募或归属别的中心。

5. **标记绑定可改动其他玩家的中心。** `ProjectCenterMarkerEventHandler.handleCenterBind` 不核对中心 owner；`onEntityInteract` 只检查女仆归玩家所有，不检查 `center.getOwner()`；登记工作台的分支也不检查 owner。玩家可先把标记绑定到别人的中心，再把自己的女仆设为其管理员或工匠、修改其工作台列表。

6. **管理员和工匠的唯一归属检查不完整。** `ProjectCenterMarkerEventHandler.isOperativeElsewhere` 只搜索其他 `WorkshopInstance`；林场、矿井绑定分支完全没有跨中心归属检查。同一女仆可被绑定到多个林场、矿井，或同时绑定工坊与其他中心。`ForestManagerBehavior.resolveForest` 在这种状态下会按当前归属或中心遍历结果选林场，派工与库存可能落到错误中心。

### 中风险

7. **缺斧后补货不会重试发斧。** `ForestManagerBehavior.tickRecruit` 先 `joinCenter`、`addMember`，然后才调用 `lendAxe`。发斧失败后，女仆仍是成员；后续招募条件排除已有成员，代码没有对其再次调用 `lendAxe`。仓库后来补斧也不能让该成员恢复正常领工具流程。

8. **工坊管理员无法通过该绑定入口更换。** `ProjectCenterMarkerEventHandler.onEntityInteract` 对工坊只在 `getManagerId() == null` 时设置管理员；此后所有绑定都调用 `setCraftsmanId`。原管理员离开或失效后，用标记绑定新管理员会覆盖工匠字段，不能完成交接，中心材料单的当前管理员身份也无法由此更新。

9. **矿井及普通中心尚未落实管理员门禁。** `MineInstance` 新增了持久化 `managerId`，但 `requestWork` 和 `tick` 没有检查管理员是否可用，仍可派发和推进工作。普通 `ProjectCenterInstance.getManagerId` 恒返回 `null`、`setManagerId` 为空实现，标记事件也没有普通中心的绑定分支。触发条件是这些中心无管理员或管理员失联；工程不会按修订设计等待。

10. **林场失效检查没有进入接单和派工路径。** `ForestInstance.isStructurallyValid` 会核对中心方块已加载且仍为林场方块，但 `ForestManagerBehavior.resolveForest`、`checkExtraStartConditions`、`tickClaim` 均未调用它。中心实例仍可解析而方块暂不可用时，管理员仍可能接单、招募和移动库存，未进入要求的可恢复等待。

11. **砍树入库会收走女仆身上所有原木。** `ChopBehavior.tickForestDeposit` 按 `ItemTags.LOGS` 从全部可用库存提取，不核对原木是否来自当前林场工程或是否已供订单携带。触发条件是林场成员原本带有私人原木，或兼任角色携带待交货原木；这些物品会被并入林场仓库，失去原有归属。

这份结论限于提供的源码和调用关系。MQ 的具体认领、提交实现及游戏内行为未在本批完整展开，因此小夜没有据此推断额外缺陷。

## MaidMoreWork：图书馆、界面与资源

主人，小夜仅依据提供的代码静态审查，发现以下有明确触发路径的高、中风险缺陷：

### 高风险

1. **图书馆重载后追加同产物配方可能抛异常。** [LibraryData.java](/mnt/d/ModProduce/MaidTown/maidmorework/src/main/java/com/fennecmomo/maidmorework/library/LibraryData.java) 的 `Recording.CODEC` 用 `Codec.STRING.listOf()` 解码配方列表；`LibraryData(List<Recording>, …)` 只复制外层列表，`record()` 却直接对 `recording.recipes()` 调用 `add()`。世界重载后，给已有产物录入第二条配方时，解码所得列表可能不可修改，导致 `UnsupportedOperationException`，多配方录入无法完成。

2. **数据包更新后，同一配方 ID 改了产物仍会被当作旧知识使用。** [WorkshopInstance.java](/mnt/d/ModProduce/MaidTown/maidmorework/src/main/java/com/fennecmomo/maidmorework/crafting/WorkshopInstance.java) 的 `hasUsableRecipe()` 和 `chooseRecipe()` 只核实 ID 对应的是 `CraftingRecipe`；`executeCraftStep()` 只核实配方 ID，未核实实际产物仍是登记的产品。配方 ID 保留但输出改变时，中心不会标记旧知识不可用，还会消耗工程预留并存入错误产物，违反“过时配方暂停”的要求。

3. **先学最终产物、后补录中间配方时，依赖知识无法自动补齐。** [WorkshopInstance.java](/mnt/d/ModProduce/MaidTown/maidmorework/src/main/java/com/fennecmomo/maidmorework/crafting/WorkshopInstance.java) 的 `learnFromLibrary()` 遇到已学的配方 ID 就 `continue`，依赖遍历也因此跳过。若先录入并学会木镐，之后才录入木棍、木板，再次从木镐学习不会访问这些新录入的依赖；中心仍缺中间配方，木镐链无法按要求自动恢复。

4. **工坊界面可把空堆写入持久仓库。** [WorkshopMenu.java](/mnt/d/ModProduce/MaidTown/maidmorework/src/main/java/com/fennecmomo/maidmorework/crafting/WorkshopMenu.java) 的 `WarehouseView.setItem()` 在向当前列表末尾之外的槽位放物品时，先补足 54 个 `ItemStack.EMPTY`。例如空仓库向第 1 格放物品，也会留下其余空堆；[ProjectCenterInstance.java](/mnt/d/ModProduce/MaidTown/maidmorework/src/main/java/com/fennecmomo/maidmorework/project/center/ProjectCenterInstance.java) 的 `MAP_CODEC` 又直接编码仓库列表。它破坏了基类明确要求的“仓库过滤空堆”约束，使中心存档序列化存在失败风险。

### 中风险

5. **工作台区块卸载会永久丢失绑定。** [WorkshopInstance.java](/mnt/d/ModProduce/MaidTown/maidmorework/src/main/java/com/fennecmomo/maidmorework/crafting/WorkshopInstance.java) 的 `hasValidTable()` 用 `removeIf(pos -> !level.isLoaded(pos) || …)` 删除登记位置。调用该方法时，只要工作台区块暂时卸载，位置就从持久列表移除；重新加载后不会自动恢复，制作不能仅靠区块恢复继续。

6. **界面绑定未完整执行中心归属规则。** [WorkshopMenu.java](/mnt/d/ModProduce/MaidTown/maidmorework/src/main/java/com/fennecmomo/maidmorework/crafting/WorkshopMenu.java) 的 `clickMenuButton()` 未核实玩家是 `workshop.getOwner()`；`unboundElsewhere()` 也只检查其他 `WorkshopInstance`，不检查林场、矿井等中心。触发条件是非中心 owner 已打开菜单，或女仆已属其他种类中心：前者仍可修改绑定和库存目标，后者可被重复绑定，造成中心人员归属冲突。

7. **工坊界面不能让管理员兼任工匠。** [WorkshopMenu.java](/mnt/d/ModProduce/MaidTown/maidmorework/src/main/java/com/fennecmomo/maidmorework/crafting/WorkshopMenu.java) 的 `bindMaid()` 在绑定管理员时清掉同一人的工匠字段，在绑定工匠时又拒绝当前管理员。通过这两个界面按钮，单名女仆始终无法同时占有两个独立字段，与主人补充的兼任设计不符。

8. **超出 54 堆的中心物资在界面中不可见、不可取。** [WorkshopMenu.java](/mnt/d/ModProduce/MaidTown/maidmorework/src/main/java/com/fennecmomo/maidmorework/crafting/WorkshopMenu.java) 的 `WarehouseView` 固定只暴露前 54 个索引，而 [ProjectCenterInstance.java](/mnt/d/ModProduce/MaidTown/maidmorework/src/main/java/com/fennecmomo/maidmorework/project/center/ProjectCenterInstance.java) 的 `depositToWarehouse()` 可继续追加堆。材料或退回物资使仓库超过 54 堆时，后续堆仍被中心持有，却无法通过承诺的玩家存取界面取出。

本轮没有调用工具、运行验证或修改文件。以上结论是代码路径审查；未把尚未进行的游戏验证列为缺陷。