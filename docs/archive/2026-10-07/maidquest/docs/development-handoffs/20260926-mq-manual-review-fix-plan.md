> 文档分类（2026-10-07）：历史交接／审查证据。下文方案、命令、缺陷及验收状态仅对应原批次；不构成当前实施授权，未复核条目不自动关闭。 [统一入口](../../../../../INDEX.md).

# MaidQuest：手测反馈与静态审查修复单（2026-09-26）

交给 OpenCode 的独立问题单。用户将手动安排修改；本文件只整理原因和方案，不表示已修复。依据为用户本次 10 条手测反馈中的第 2、9 条，以及 `/mnt/d/ModProduce/MaidTown/maidmorework/docs/development-handoffs/20260926-mq-mmw-combined-review.md` 的 MQ 静态审查。其余 8 条手测问题属于 MaidMoreWork，见该仓库同日修复单。当前 MQ 工作树仍有上一轮未提交实现；先保留现状并核对差异。不要启动自动 `codex-opencode-handoff` 流程。

## 用户手测：界面问题

### MQ-U01　收起工作列表后“委托模式”按钮盖住女仆背包（用户第 2 条）

- **现象**：展开/收起 TLM 的女仆工作列表后，委托模式按钮与背包 UI 重叠。
- **原因**：`CommissionModeClient.placeButton` 避让的是 TLM `getExclusionArea()`、事件按钮和 `gui.children()` 的**控件矩形**，不一定包含背包面板的整块绘制区域。收起列表后，排斥区与控件位置变化，候选位或网格扫描可能被误判为安全；找不到位置时还直接将按钮放在屏幕左下角，完全没有再做遮挡检查。`onRender` 仅在布局签名变化时重排，面板实际绘制矩形不在签名中的情况也可能漏检。
- **方案**：把背包主面板和展开工作列表实际占用矩形加入禁入区域，重新定义布局签名；在分辨率/GUI 缩放/列表开合变化时复核。首选放在面板外边的固定可见位置；若当前屏幕确实没有空间，隐藏或折叠按钮并给可发现的入口，禁止“无安全位置仍强行绘制”。请在工作列表展开和收起两种状态、不同 GUI 缩放下目视确认不遮挡槽位、标签页与其他按钮。
- **位置**：`src/main/java/com/fennecmomo/maidquest/client/CommissionModeClient.java`，TLM 女仆容器布局 API。

### MQ-U02　委托板物品选择列表不能拖动滚动条，也不能用滚轮滚动（用户第 9 条）

- **拖动原因**：`ItemPickerWidget` 只绘制竖向滑块，没有 `mouseClicked`/`mouseDragged`/`mouseReleased` 的拖动状态与滚动映射，因此该滑块目前是纯视觉元素。`QuestBoardScreen.mouseDragged` 也只主动转发给委托列表、类型列表，没有转发给物品选择器。
- **滚轮原因**：`QuestBoardScreen.mouseScrolled` 先交给 `questList`、`typeButtonList`，最后才调用 `super`；FennecLib `ScrollBar.mouseScrolled` 把滚动条左侧 152 像素也视为自己的列表区域。类型列表的这块命中区与右侧物品选择器重叠，类型列表可先消费滚轮事件，致使 `ItemPickerWidget.mouseScrolled` 得不到调用。当前选择器自身虽实现滚轮逻辑，但事件优先级错误。
- **方案**：仅当物品选择器可见且鼠标在其矩形内时，先把滚轮/按下/拖动/释放事件交给选择器；其余区域再分派给两个 `ContentList`。给选择器绘制真实轨道和滑块，按下滑块/轨道时记录拖动、将 Y 坐标映射到 `[0,maxScroll]`、在释放/失焦时结束拖动；隐藏时不抢事件。不要靠扩大 `ContentList` 的命中区覆盖邻近控件。验证数百种候选物品下滑块拖到底、滚轮逐行滚、搜索过滤后位置归零且可正常选中物品。
- **位置**：`src/main/java/com/fennecmomo/maidquest/client/{QuestBoardScreen,ItemPickerWidget}.java`；FennecLib 的 `template/Bar/ScrollBar.java` 仅作为当前命中区依据。

## 上一轮静态审查：材料单权限与候选目录

下列五项未经此次手测验证，但源码路径清楚。尤其 MQ-S01/S02 会影响 MMW 工坊中心管理员的材料单权限；不要用 MMW 侧自检取代 MQ 服务端授权。

### MQ-S01　中心材料单发布时未验证当前管理员（高）

- **原因**：`QuestService.requestMaterial(..., beneficiaryId)` 检查条件和数量后接受传入的 requester/受益中心，并未调用 `MaterialBeneficiaryRegistry.represents`；旧管理员、工匠或其他调用方可尝试代表中心发布。
- **方案**：中心单创建入口、以及复用现有单的入口，都验证发布女仆当下确实代表受益中心；非中心单维持明确的独立规则。服务端不得信任调用方提供的 UUID。更换管理员后，旧管理员发布应拒绝，新管理员可继续同一中心业务。
- **位置**：`src/main/java/com/fennecmomo/maidquest/service/QuestService.java`、`api/MaterialBeneficiaryRegistry.java`。

### MQ-S02　会话绑定能让卸任管理员继续领取/取消（高）

- **原因**：`MaterialBeneficiaryRegistry.represents` 命中内存 `MANAGERS` 时直接返回 true，即使持久中心回调已经判定她不是当前管理员。`QuestService.canClaimMaterial/cancelMaterial` 因而可能接受过时身份。
- **方案**：以中心持久数据/当前回调为授权真值；会话绑定只可作缓存且有生命周期/代数校验，换人时立即失效，不允许“旧会话或当前回调任一为真”放行。覆盖旧管理员、新管理员、中心卸载重载和存档恢复路径。
- **位置**：`src/main/java/com/fennecmomo/maidquest/api/MaterialBeneficiaryRegistry.java`、`service/QuestService.java`。

### MQ-S03　旧兼容入口可能复用别的中心的子单（中）

- **原因**：`QuestService.materialFor(..., beneficiaryId=null)` 跳过受益中心比较；旧的无中心参数 `materialFor/requestMaterial` 重载沿这一路径。相同 `sourceId` 与条件可匹配到中心单，旧 requester 随后无法正常领取。
- **方案**：复用判定时把“无受益中心”作为一个**明确且必须相等**的归属值，不能当通配符；中心与旧入口互不复用。保持兼容入口能正常服务非中心旧存档。
- **位置**：`src/main/java/com/fennecmomo/maidquest/service/QuestService.java`。

### MQ-S04　材料单去重未区分 ORDER 与 STOCK（中）

- **原因**：`QuestService.materialFor` 对同源、同条件和受益中心比较，却不比较 `MaterialQuest.source()`；订单材料和备货材料可能互相复用，数量与业务归属错误。
- **方案**：将 `MaterialSource` 纳入请求键及现有订单复用条件，或显式存储唯一子单 ID；完成、取消、重载后保持区分。与 MMW 的每材料在途量修复联合验收。
- **位置**：`src/main/java/com/fennecmomo/maidquest/service/QuestService.java`、`quest/type/MaterialQuest.java`。

### MQ-S05　候选目录前 8192 项以外的产物不可选（中）

- **原因**：`CraftingCatalog.compute` 对展示候选排序后截断到 8192，但 `isProduct` 对完整全集校验；服务端允许而客户端永远看不到后面的产物。
- **方案**：按页/搜索查询传输完整候选全集，限制每包大小与查询成本，而不是截断总目录；显示总数/页码或继续加载状态。搜索稀有产物时应能选择并由服务端一致校验。
- **位置**：`src/main/java/com/fennecmomo/maidquest/service/CraftingCatalog.java`、候选查询/响应载荷、`client/CraftingCandidatesClient.java`。

## 建议修复顺序与验收

1. 先修 MQ-U01/U02，使手测可继续选择物品且 UI 无遮挡；同时处理 MQ-S01/S02 权限高风险。
2. 再修 S03/S04 去重归属、S05 候选分页；与 MMW 的工坊/林场材料单联测。
3. 用新测试世界或备份档验证：按钮在任务列表开合时不盖背包；选择器鼠标滚轮与拖动均能到底并选中；旧管理员不能发布、领走或取消中心材料单，新管理员可以；ORDER/STOCK 与不同受益中心子单不互相复用；大量候选时可搜索尾部产物。
4. 编译后确认桌面联调入口实际加载的是**新 MQ 开发类**，不要把 MQ JAR 再放进 `run-shared/mods` 造成重复加载。用户会自行手动运行，不由本文件触发 OpenCode。

## 证据边界

MQ-U01 的确切遮挡矩形需要截图或游戏内目视确认，源码已经表明兜底布局无安全性保障。MQ-U02 的拖动缺实现与滚轮区域相互覆盖可直接从当前代码确认。本文件没有修改源码、运行 OpenCode、编译或启动游戏。
