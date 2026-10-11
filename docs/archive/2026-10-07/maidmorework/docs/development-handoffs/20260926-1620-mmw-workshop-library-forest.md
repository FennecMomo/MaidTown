> 文档分类（2026-10-07）：历史交接／审查证据。下文方案、命令、缺陷及验收状态仅对应原批次；不构成当前实施授权，未复核条目不自动关闭。 [统一入口](../../../../../INDEX.md).

# MaidMoreWork：工坊、图书馆、林场与制作链交接

项目目录：/mnt/d/ModProduce/MaidTown/maidmorework
交接基线：9d8e0d6
上游项目：/mnt/d/ModProduce/MaidTown/maidquest（本次会话不得修改；先读取其最新 API/JAR）
目标版本：Minecraft 26.1.2，NeoForge 26.1.2.76，Java 25

## 目标与顺序

修复主人发现的制作名称缺翻译、工作站外观与原版工作台相同、绑定不可见、木镐库存目标写死、委托模式下无单自动伐木、工匠接单后停在委托板以及木镐缺料估算错误。加入图书馆共享配方与林场管理，最终使玩家木镐单经制作中心管理员发布缺料单、林场供货、真实制作、交付、首单后有限备货形成闭环。只修改 MMW 仓库；若 MQ API 不足，不修改 MQ，明确报告阻塞。

优先让完整木镐链运作，再实现更宽泛的真实工作台配方；所有产物及需求数据结构必须按物品/配方而非 WOODEN_PICKAXE 字段设计。过程遵守服务端物品守恒；未知配方、缺材料、工作站失效均进入可恢复等待，不凭空产出。矿井现有挖掘算法、MaidTown、货币工资与公共仓库不在本轮；但通用工程中心（含矿井）的管理员绑定与职责接口属于本轮。

## 立即修复的启动与界面问题

- CraftingTask.createBrainTasks 必须返回可修改列表；当前 List.of 会被 TLM MaidBrain.initWorkActivity.add 修改，运行日志明确有 UnsupportedOperationException。加中英文 task.maidmorework.crafting 文案。
- 现有 CraftingBehavior.hasWork 及 QuestExtraMaidBrain 交互要保证已认领制作单在 Home 模式和绑定有效时能离板工作、发布材料单；失效原因在 GUI/聊天可见，不允许静默站立。
- 现有缺木算法为一把木镐只订一根原木；一根原木出 4 木板，做木棍后剩 2 木板，不够木镐的 3 块。按所选配方链及真实库存、已托管、在途量算缺口，不使用原固定估算。
- 工坊外观要明显区别原版工作台；提供独立模型和可辨识的工匠符号/配色，物品图标与方块外观一致；中英文名称均正确。

## 工坊作为工程中心

- 废弃单独的“绑定一名女仆+一张工作台”的管理真相，把工坊方块接入现有 ProjectCenterBlockEntity / ProjectCenterInstance / ProjectCenterManager 身份与生命周期。工坊是一种中心 kind，拥有稳定 UUID、玩家 owner、库存、成员与工作台位置列表。维持当前 54 格物品储存和游戏内可打开的存取界面；本轮容量一名执行制作的女仆、一名管理女仆和一处有效原版工作台，数据与接口预留多工作台/多工匠，后续可按有效工作台数决定工位数。本轮不得同时招入第二工匠。
- 玩家仍能直观绑定管理女仆、执行工匠与工作台；绑定检查所有权、工种、距离和唯一归属，显示目标名称、坐标和失效原因。工坊中心由全局 tick 驱动，工匠或工作台区块卸载时仍可依据持久绑定、已学配方和真实预留材料继续合成；需要实体执行的接单、领取和交货待加载后恢复。测试世界可拆旧工作站重建，不做旧单人站数据迁移。
- 复用现有 ProjectCenterMarkerItem：蹲下右键工坊绑定标记工具。手持该工具（主手或副手）时，在 64 格内绘制工坊到已绑定工作台、工匠的不同颜色连线；目标不在客户端可见范围时显示已绑定但不可见，不强行加载区块。不要常驻显示。
- 当前工坊 Finder 扫描女仆 65×17×65 方块；改为按持久化中心/成员索引查找，避免每次行为检查扫描大范围方块。

## 图书馆与制作知识

- 新增图书馆方块及界面。玩家用虚拟 3×3 输入格摆放样本，服务端用当前 RecipeManager 校验实际工作台配方，显示产物与所选配方 ID，确认录入不消耗玩家物品；拒绝无效或非工作台配方。支持已加载模组的真实配方，若同一产物有多个录入配方按稳定顺序保存并展示，制作优先使用当前库存可满足的一条。
- 录入配方在世界 SavedData 共享，拆除最后一座图书馆仍保留数据。图书馆是录入和管理女仆亲自学习的入口；没有可达图书馆时单独提示缺图书馆，不能谎称缺配方。数据跨重载保持，配方 ID 在数据包更新后失效时标记不可用并暂停，不使用过时输出。
- 管理女仆接到中心的制作订单即记住该产物有需求；若中心不会做，由管理女仆亲自去可达图书馆学习并登记到中心。图书馆尚未录入时，对该订单向玩家聊天频道发一次本地化缺配方请求，订单保留认领/等待；录入后自动重试并学习。木板、木棍、木镐必须各自录入和学习，不能暗用游戏全量配方。所学配方、已知产品和每产品库存目标由工程中心持久化；更换执行工匠不丢知识，换中心则由新中心独立学习。目标默认 5、可设为 0，首单结束后才自主备货。
- 按已学配方递归制作中间产物，选择可用配方并防环；每步经 RecipeManager 匹配，先检查输出空间、再扣真实输入并入真实产物。精确记录成品预留、玩家订单量、库存量及在途材料；优先履行玩家订单，完成后再补货。非可制作原料通过 MQ 材料子单提出需求；无供应者时等待玩家投料或将来其他工种供货，不伪造资源。木材需求匹配所录木板配方认可的原木，而不是固定橡木。
- 工作站界面显示已知产品列表及各自库存目标，按产品调节，不能再只显示 wood pickaxe target。订单取消时把仍属于该工程的实物成品、半成品和未消耗材料退回工程中心仓库，已消耗原料不得凭空重建；已完成且领取的原木子单归工程中心，不追溯撤销。

## 林场管理和伐木门禁

- 新增林场中心 kind 与管理女仆工种/角色；林场有持久化 owner、管理员、成员、库存、订单和工具借用记录。通过现有工程中心标记与范围系统创建/绑定，树木工程继续复用 ChoppingProject、ProjectCenterInstance 的分配/扫描能力。
- 木匠工程中心的管理女仆代表中心发布原木单。只有已绑定有效林场的管理女仆可接该单；管理员在附近自动招募同主人的空闲伐木工种女仆，须未归属其他中心且委托模式开启。管理员从林场库存发斧；伐木女仆按林场工程砍树，将原木实际送入林场库存。管理员按订单 ID 预留所需木材，从库存实际取出送至委托板交货；超出需求的原木留林场。订单完成后回收借出的工具、释放为此订单招募的成员，不能重复领取、重复存入或跨单混货。本轮无工资账。
- MQ 委托模式开启时，伐木工种女仆没有林场派工就不能在 Home 模式进行个人工程/自动找树；已有自由砍树行为也要在模式切换时安全停下。关闭委托模式时保留 MMW 旧的自主砍树体验；MQ 缺席时也保留 MMW 独立使用的旧逻辑。林场派工量与材料订单剩余量联动，已满足数量即停止继续开新工程。
- 管理员处理斧不足、无树、背包满、区块未加载或委托板暂不可达时进入可见等待状态，物品和订单预留保持，条件恢复后继续。拆林场时安全退回可存物品并解除成员归属。

## 服务端接口与验收

- 使用 MQ 最新 CraftingQuest、MaterialQuest、QuestEligibilityRegistry、QuestService 的正式接口注册资格和处理材料。MQ 不应导入 MMW 类，MMW 单独加载不应因为 MQ 类缺席崩溃；已有矿井与普通工程中心行为保持可用。
- 并行木镐单、并行原木单、根单取消、库存已有原木、成品备货上限、满背包、卸载/重载、图书馆录入后恢复、标记工具绑定和单独安装 MMW 都需保证安全。编码时可做静态推理和编译，禁止本会话运行测试和游戏验证。
- 最终向交接文档补记 OpenCode 会话 ID、准确编译命令与退出码及关键输出，实际人工游戏验证留给用户。

## 唯一允许的开发末尾命令

在项目目录运行：./gradlew jar

已检查 build.gradle 与 gradlew：jar 只执行所需 Java 编译、资源处理、元数据生成和打包，未绑定 test、check、lint、runClient 或截图任务。MMW 通过 build.gradle 读取 ../maidquest/build/libs 中最新 MQ jar；开始前确认上游交接已生成新 jar。编译失败可修改代码并重跑同一命令；完成后不得运行其他验证命令。

禁止运行测试、lint、check、runClient、runServer、游戏、开发服务器、浏览器或截图。不要自行提交、推送或修改关联仓库。

## 用户后续手动测试清单

1. 切换制作工种，确认名称翻译且无大脑初始化异常；绑定工程中心管理员、工匠、工作台并查看标记工具连线。
2. 在图书馆录入木板、木棍、木镐；发布木镐单，确认管理女仆前往学习并把配方登记给中心。不录木镐时先看到缺配方消息，补录后继续。
3. 确认制作中心管理员订足原木；林场管理员招募伐木工并发斧，伐木工砍树入库，林场管理员交原木到委托板，制作中心管理员领取入库；工程预留材料后工匠实际制作、交付。
4. 无原木订单且委托模式开启时伐木工待命；关闭时恢复自主砍树。木镐首单完成后备货到目标 5，设 0 后停产。
5. 重进世界、取消根单、拆工作台/图书馆、塞满背包和库存后检查不丢单、不复制物品、阻塞可恢复。
6. 原木已交至委托板但尚未领取时更换制作中心管理员，确认新管理员可领取入同一中心；制作工程开始后取消订单，确认其未消耗原料与半成品退回中心仓库，工匠不持有跨中心物资。

## 工程中心、管理女仆与制作订单归属修订（主人 2026-09-26 补充，优先于上文旧措辞）

- 每个工程中心都必须绑定一名管理女仆，中心以稳定 UUID 持有人员、工具、资源、产物与工程分配的持久状态。管理女仆负责分派工具、人员、资源，分配全部产物，按缺口代表中心发布和领取材料委托。制作、伐木、挖矿等中心都遵守此职责划分；中心暂时没有可用管理员时工程等待，原有库存、订单和预留不能丢失或转给其他中心。
- 委托板上的玩家制作订单在制作中心内映射为一个持久制作工程。中心而非工匠女仆拥有该工程及其材料、已学配方和备货知识。工匠只是中心调配的执行者；重派、更换或卸载工匠不改变工程所有权和库存。认领委托的女仆与管理女仆可以是不同角色，不以执行女仆 UUID 作为材料单唯一收货身份。
- 管理女仆负责去图书馆学习木板、木棍、木镐等配方，录入中心知识。工匠按中心已学配方执行，不通过自身附件隐式学会。制作订单开始前，按选定配方链和现有库存核算所需材料，原子地从中心仓库移入工程独立预留；材料不足则等待并由管理员发布缺口单，不能先耗用未预留的其他工程材料。材料子单的稳定来源应指向该中心/制作工程，领取后入中心仓库再预留给工程；换管理员仍可继续同一子单，但别的中心不可领取。
- 取消制作订单时，中心把工程仍持有的原料、中间产物和未交付成品退回中心仓库，释放预留、人员及工具；已真实消耗的原料不凭空返还。取消、重载、满仓与区块卸载时保持物品守恒和幂等。订单完成后首单带来的产品备货意向留在中心，并按该产品目标补货；从未接到订单时不主动生产。
- 旧 `CraftingKnowledge` 附在工匠女仆、`WorkshopBlockEntity` 单独持有绑定和仓库、`CraftingBehavior` 让工匠发布/领取原木单的逻辑必须迁移为中心事实，不要仅改 UI 文本。需要时通过 MQ 提供的通用中心受益身份/管理员交接接口衔接；MQ 不导入 MMW。

## 本地手动测试交付路径

桌面入口 `C:\Users\32138\Desktop\女仆模组联调.bat` 会依序执行 MQ 与 MMW 的 `gradlew.bat --offline jar`，MQ 从 `maidquest/build/classes/java/main` 和 `build/resources/main` 加载，MMW 从 `D:\ModProduce\MaidTown\run-shared\mods\maidmorework-0.1.4.jar` 加载。OpenCode 的 `./gradlew jar` 只负责编译和打包，不代表用户测试实例已经更新。独立审查闭环后由 Codex 确认 MMW 新 JAR 已复制到该目标、哈希一致且无旧版本重复加载；MQ JAR 不复制到 mods。此流程不运行客户端，游戏内测试由主人执行。

## 本轮先行实施 MMW 的补充指令（主人 2026-09-26）

主人决定先完成 MMW，再把 MQ、MMW 的独立审查结论合并汇报；用户手动测试反馈之后才处理下一轮 MQ/MMW 修复。因此本会话只修改 MMW，不修改 MQ，即使发现上游缺口也如实记录。管理员允许兼任同中心执行人员，但同一 tick 不执行相互冲突的工作；仍要保留管理身份与执行分配的独立字段。

当前 MQ 最新 JAR：`/mnt/d/ModProduce/MaidTown/maidquest/build/libs/maidquest-0.0.1.jar`，MMW 的 Gradle `compileOnly` 自动选用此目录最新 MQ JAR。上游 MQ 未通过最终审查，已知如下限制，MMW 应规避可规避部分并如实报告其余部分：

- `QuestApi.requestMaterial(level, boardPos, managerMaid, sourceId, source, condition, quantity, centerId)` 在 MQ 内不验证 managerMaid 是否真为中心管理员；MMW 调用前必须依据持久中心数据自己核实身份。
- 使用带 `centerId` 的新材料接口，不调用不带受益中心的兼容重载；`MaterialBeneficiaryRegistry.register((centerId, maid, level) -> ...)` 注册基于中心 SavedData 的当前管理员回调。不要调用其会话 `bindManager`，以免旧绑定与持久回调冲突。
- MQ 去重暂不区分 `MaterialSource.ORDER` 与 `STOCK`；MMW 为订单需求和备货需求使用不同、稳定、可持久化的 `sourceId`，并自行核对数量、中心与条件。并行工程各有唯一源 ID。
- MQ 候选目录超过 8192 项时可能漏展示产物；MMW 不要依赖 MQ 客户端候选集作为配方真相，图书馆始终以服务端 RecipeManager 为准。

供本仓库实现使用的 MQ API 精确签名（包名均以 `com.fennecmomo.maidquest` 为根）：

```java
// api.QuestApi
static MaterialQuest requestMaterial(ServerLevel level, BlockPos boardPos, EntityMaid requester,
    UUID sourceId, quest.MaterialSource source, quest.MaterialCondition condition,
    int quantity, UUID beneficiaryId);
static List<api.MaterialOrderInfo> materialOrdersFor(ServerLevel level, BlockPos boardPos, UUID beneficiaryId);
static Optional<api.MaterialOrderInfo> materialOrder(ServerLevel level, BlockPos boardPos, UUID orderId);
static int claimMaterial(ServerLevel level, EntityMaid maid, BlockPos boardPos, UUID orderId, UUID beneficiaryId);
static List<BlockPos> boardsNear(ServerLevel level, BlockPos pos, double radius);
static Optional<quest.Quest> currentQuest(EntityMaid maid);
static void markWaiting(EntityMaid maid, String reasonKey);
static void resume(EntityMaid maid);
// api.MaterialBeneficiaryRegistry
static void register(api.MaterialBeneficiary beneficiary);
// api.MaterialSupplyRegistry
static void register(api.MaterialSupplyQualifier qualifier);
// api.QuestEligibilityRegistry
static void register(api.QuestEligibilityRegistry.Provider provider);
// quest.MaterialCondition
static Optional<quest.MaterialCondition> tryOf(Collection<Identifier> ids);
static Optional<quest.MaterialCondition> tryFromIngredient(Ingredient ingredient);
static quest.MaterialCondition exact(Identifier id);
// quest.MaterialSource: ORDER, STOCK
// api.MaterialOrderInfo: orderId(), parentId(), receiverId(), source(), beneficiaryId(),
//   acceptedItems(), quantity(), remaining(), escrow(), status().
```

完成 `./gradlew jar` 后只由 Codex 独立审查并核对本地打包/联调 JAR，不由 OpenCode 运行游戏。桌面 BAT 已能按 MQ→MMW 顺序构建，但 MMW 旧 JAR 仍在 `run-shared/mods`；新版本必须在审查后由 Codex 复制并核对哈希，才能交给主人手动测试。

## OpenCode 本轮实施记录（2026-09-26，仅 MMW 仓库）

- 会话来源：OpenCode（本仓库工作区），未修改 MaidQuest / MaidTown / FennecLib。
- 编译命令：在 `/mnt/d/ModProduce/MaidTown/maidmorework` 运行 `./gradlew jar`
- 编译结果：`BUILD SUCCESSFUL`（退出码 0），关键输出 `BUILD SUCCESSFUL in 5s`，产物 `build/libs/maidmorework-0.1.4.jar`
  （最终构建 sha256 `ba443853426263162b4bfe94479c316e45fd86520d7af16437327150d2de9b2b`，以 Codex 复核时重新计算的哈希为准）。
- 禁止项遵守：未运行测试、lint、check、runClient、runServer、游戏、浏览器或截图；未提交、未推送；未使用 `--auto`。

### 实现内容

1. 启动与界面修复：`CraftingTask.createBrainTasks` 返回可变 `ArrayList`（修复 TLM `add` 抛 `UnsupportedOperationException`）；补 `task.maidmorework.crafting` 中英文；工坊换用自绘纹理与独立模型（工匠交叉工具符号 + 胡桃木/铜色配色），物品模型继承方块外观；名称改为工坊 / Artisan Workshop。
2. 工坊接入工程中心：新增 `WorkshopInstance`（kind=workshop）持久化管理女仆、执行工匠、工作台列表、已学配方、已知产品、每产品库存目标、制作工程与工程预留；新增/改造 `WorkshopBlock`、`WorkshopBlockEntity`、`WorkshopMenu`（54 格中心仓库视图 + 绑定/目标调节）、`WorkshopStatusPayload`；拆除旧 `WorkshopFinder` 方块扫描，改为按持久化中心/成员索引查找。
3. 中心化知识：删除女仆侧 `CraftingKnowledge` 附件；新增 `LibraryData`（世界 SavedData，录入共享、拆最后一座图书馆仍保留）、`LibraryBlock/BlockEntity/Menu/Screen`、`LibraryPreviewPayload`；3×3 幽灵格不消耗玩家物品，服务端 RecipeManager 校验并显示产物/配方 ID；管理女仆亲自到 64 格内可达图书馆按依赖闭包学习，无图书馆/未录入分别提示。
4. 缺料与制作：按已学配方递归核算缺口（木板/木棍/木镐各自录入；木材需求用所录木板配方认可的 Ingredient 转 MQ 条件，不写死橡木）；工程预留原子移动、优先玩家订单、首单后按目标（默认 5，可设 0）有限备货；每步经 RecipeManager 校验并核对配方 ID，扣真实输入、入真实产物；订单取消退回预留与工匠身上带标记成品、并取消未领取材料子单。
5. MQ 接口：`MaterialBeneficiaryRegistry` 按持久中心数据核实当前管理员；`MaterialSupplyRegistry` 限定制作中心缺料单只允许有效林场管理员（或 MQ 默认原木单+伐木工种）；订单/备货使用不同稳定 sourceId 并经 `MaterialOrderInfo.receiverId()` 核实在途；使用带 `beneficiary` 的材料接口，未调用旧兼容重载或 `bindManager`。
6. 林场：新增 `ForestInstance`（kind=forest，持久化管理员/成员/库存/订单预留/工具借用）、`ForestBlock/BlockEntity`、`ForestManagerBehavior`（认领制作中心缺料单、招募同主人委托模式空闲伐木女仆并发斧、按订单预留交货、完成回收工具释放成员）、`MqBridge`（MMW 单独加载不触达 MQ 类）；伐木女仆砍下原木实际送入林场库存；MQ 委托模式开启且无林场派工时禁止自由砍树，关闭/MQ 缺席保留旧自主砍树；模式切换安全停止。
7. 通用中心管理员：`ProjectCenterInstance` 增加 `getManagerId/isManager/hasOnlineManager` 接口；工坊/林场/矿井均持久化管理员；标记工具支持蹲下右键绑定中心、右键工作台登记、蹲下右键女仆绑定管理员/工匠，并显示所有权、工种、距离、唯一归属检查与原因；新增绑定连线渲染（主/副手标记 64 格内，管理/工匠/工作台不同颜色，不常驻、不强加载区块）。
8. 资源与注册：图书馆/林场/工坊的方块状态、模型、物品、掉落表、配方、中英文文案；网络包与客户端注册；创建标签页条目；拆中心时工坊预留退回仓库、林场回收工具并释放成员。

### 未完成项与已知限制（未完成，需后续处理）

- 矿井：仅补了中心管理员持久化字段与标记绑定入口；矿井派活/挖矿算法本轮未接入管理员职责（仍按原逻辑运行），无矿井管理员 GUI。
- 林场派工量只与"是否有未完成订单"联动，未按订单剩余数量精确开工程；订单交货完成前可能继续砍伐，超出部分留在林场。
- 缺料核算为保守估算：已预留的半成品不会抵扣上层原料需求，个别情况会多订原木（不会丢物，剩余留中心仓库）。
- 工作台界面只展示/操作前 54 个仓库堆；中心仓库列表本身不限制 54 格，超出部分仍由制作引擎使用。
- 标记连线只画管理女仆、执行工匠与第一处工作台；多工作台连线未画。
- 图书馆同一产物的多配方仅按"先录入先保存"追加，录入界面不提供从多配方中选择；制作时按库存可满足度选配方。
- 管理女仆的"可见等待"以聊天提示（10 秒节流）为主，未做常驻 GUI 状态面板。
- 所有闭环仅通过静态推理与编译验证；游戏内验证按交接要求留给用户/后续 Codex。

### 交叉报告的上游限制（MQ 未通过审查，如实记录）

- MQ 不验证 `managerMaid` 是否真为中心管理员：MMW 已在调用前按持久中心数据自核身份。
- MQ 去重不区分 ORDER/STOCK：MMW 已为订单与备货使用不同且稳定可持久化的 sourceId，并自行核对数量/中心/条件。
- MQ 客户端候选目录 8192 限制：图书馆与服务端核算不依赖客户端候选集。
- 换管理员继续同一材料子单依赖 `MaterialBeneficiaryRegistry` 回调指向当前中心管理员，MMW 已按此注册；未使用会话 `bindManager`。
