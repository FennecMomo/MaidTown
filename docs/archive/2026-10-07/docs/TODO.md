> 历史归档（2026-10-07）：保留整理前正文，仅重定位相对链接。旧确认、旧待办和旧实现状态不代表当前状态；当前规则见 [统一设计](../../../design/current/README.md)。

# MaidTown TODO 总览

> 最后更新：2026-09-28
> 各模块详细清单见「来源文档」；本页为全项目待办唯一总入口，条目变更时同步维护。

---

## 一、待游戏内验证（v0.1.3 发布后）

| # | 项目 | 说明 | 来源 |
|---|------|------|------|
| V1 | 矿井仓库 UI 本轮待测 6 项 | <1000 精确角标、k/M/B 缩写、悬停精确总计、无黑罩、>32767、翻页与存取回归 | TEST_LOGGING「矿井仓库 UI 测试」 |
| V2 | 仓库角标/同步截断修复（W1/W2） | 角标改原版 countText 渲染、计数数据槽 lo/hi 拆分的验证 | TEST_LOGGING 上轮反馈 |
| V3 | TODO_V1 #6-UI 640 堆叠显示 | 与 V1 同批验证，通过后勾掉 | TODO_V1 |
| V4 | 矿井重构解决项 #2 / #6 / #8 / #20 / #22 | 就近派发、光源位、重力方块重扫、矿石 REPLACE、替换列表 | TODO_V1「待验证」 |
| V5 | maidquest 统一身份改造后测试 | 双端发布与校验、按身份撤销/领取、女仆接单链路、材料单链路（含批量撤单）、委托模式配置，清单见 `maidquest/docs/TEST_LOGGING.md` | maidquest TEST_LOGGING |

## 二、待实现

### MaidMoreWork

| # | 项目 | 说明 | 来源 |
|---|------|------|------|
| I1 | 鱼骨矿道 | 主通道 + 两侧分支，需新增 FishboneMinePlanner；几何已在矿井重构中预留 | TODO_V1 #7 |
| I2 | 跟随采矿（跟随模式） | 跟随玩家沿途采表面矿；范围/判定见 C1、流程/背包满策略见 C2 | MINE_REDESIGN §12 |
| I3 | 困难表红点渲染 | 手持标记工具时，矿井困难表坐标画红框（矿井ID+坐标列表定向推送 + 复用 WireframeBoxRenderer） | MINE_REDESIGN §11 / D3 |
| I4 | 挂顶灯笼 | 灯笼无法贴墙，需加栅栏挂到下一层；当前光源只认火把 | MINE_REDESIGN §6 |

### MaidQuest

| # | 项目 | 说明 | 来源 |
|---|------|------|------|
| I7 | TLM 原生任务兼容 | 增加通用「交付型」委托（`preferredTaskUid` 指向 TLM 原生任务），女仆用自己的 TLM 任务产出物品后到板交付，maidquest 不做执行逻辑 | maidquest/docs/INDEX.md |
| I8 | MQ×MMW 订单链（设计待定稿） | 委托倾向、制作／管理、父子订单、有界备货、制作价 `1.2M`、采矿交货按固定原价计分且目标 `10R`；公共仓库先供缺料、矿场缺钱再出售余货，固定报价与有限透支；价目及结算边界待讨论，尚未实现（订单归属已定为"发布女仆"、受益中心机制已随统一身份改造删除） | [订单生产链设计](design/MAIDQUEST_MMW_ORDER_CHAIN.md) |

### FennecLib

| # | 项目 | 说明 | 来源 |
|---|------|------|------|
| I5 | 加权算法框架解耦 | 从 Behavior 中剥离加权轮盘赌核心，提供可选 Behavior 外壳 | fenneclib/docs/TODO.md |

### 模块同步

| # | 项目 | 说明 | 来源 |
|---|------|------|------|
| I6 | maidtown 跟进 maidmorework 现 API | maidquest 已完成重构（独立模组、去除 maidmorework 依赖，待游戏内验证）；maidtown 仍引用 `entity.ai.SearchBehavior` / `ISearchAction` / `IMaidmoreHost` 等旧 API，且代注册了 maidquest 的方块/BE/网络/命令，需按 maidquest 新 API 重做适配 | project-status.md |

## 三、待修复 / 待解决

| # | 项目 | 说明 | 来源 |
|---|------|------|------|
| F1 | 砍树女仆找不到新树后原地不动 | 搜索机制已重写为个人搜索（含 Home 半径），需复测确认 | TODO_V1 #15 |
| F2 | 砍树旧测试遗留（#5 收起女仆 HUD 残留 / #10 耗尽气泡不显示） | 2026-07-25 轮次遗留，相关机制已重写（ProjectManager→ProjectCenterManager、SearchBehavior 移除），需复测 | TEST_LOGGING「历史轮次」 |
| F3 | 挖矿道时墙上矿未替换成垫脚方块 | 2026-09-22 反馈 N1：矿道工程挖格/保留位扫描是否覆盖墙面矿待查 | TEST_LOGGING N1 |
| F4 | 绑定矿井中心后不显示矿井范围 | 2026-09-22 反馈 N2：绑定未同步边界显隐/客户端边界数据（矿井 BE 默认 boundaryVisible=false） | TEST_LOGGING N2 |
| F5 | 工程中心无储物空间、伐木女仆不放产物 | 2026-09-22 反馈 N3：仓库目前为矿井专属，中心基类无仓库与存放流程 | TEST_LOGGING N3 |
| F6 | 远距离时中心区块卸载重载把女仆踢出 | 2026-09-22 反馈 N4：疑似参与者清理的"实体在场"判定在区块卸载期间误判 | TEST_LOGGING N4 |
| F7 | 排水生成的流体瓶是空瓶（应为水瓶） | 2026-09-22 反馈 N5：创建时已 setFluid，疑似入库/背包路径丢数据组件（FLUID_TYPE） | TEST_LOGGING N5 |
| F8 | 林场交货取货失败时可能丢未处理原木 | `tickDeliver` 批量从仓库取出后，背包插入失败只退还当前堆；其余已取堆没有回库 | [设计审查 §3](design/DESIGN_REVIEW_20260928.md#3-审查时发现的直接实现风险) |
| F9 | 区块卸载被误判为女仆离职或工程失效 | 林场清成员、个人工程清扫和普通中心释放席位仅凭当前查不到实体 | [设计审查 §2B](design/DESIGN_REVIEW_20260928.md#b-未加载和已离职死亡需要独立状态) |
| F10 | 单个维度卸载设置全局关服标志 | `onLevelUnload` 把全局 `shuttingDown` 置真，可能影响其他维度的拆除清理 | [设计审查 §2G](design/DESIGN_REVIEW_20260928.md#g-维度卸载与服务器停止被共用标志混淆) |

## 四、暂缓 / 未来

| # | 项目 | 说明 | 来源 |
|---|------|------|------|
| P1 | 液体瓶右键交互 | 暂缓，后续改为直接对接流体容器 | TODO_V1 #13 |
| P2 | 漏斗/管道对接 | 低优先级，NeoForge 26.x capability API | TODO_V1 #19 |
| P3 | 挖掘/移动速度与工具效率适配 | 未来（石镐 vs 钻石镐） | TODO_V1 #5 |
| P4 | 工具等级要求与自动更换 | 未来 | TODO_V1 #10 |
| P5 | 深矿井滑索/扫帚飞行 | 未来；矿道控制器传送已覆盖主要场景 | TODO_V1 #21 |
| P6 | 测试期诊断日志清理 | `[MineDebug]` 全阶段日志、水中抖动诊断等临时日志，测试完成后清理 | MINE_REDESIGN §6 |

## 五、设计未决（SPEC）

- MQ × MMW 加载边界尚待讨论：工坊卸载制作是否保留、工时如何一致计算、实体缺席与死亡/收起如何区分、管理员更换时的材料单归属、跨模组物品交割和全局 tick 预算；见 [加载边界草案](design/LOADING_AND_SIMULATION.md) 与 [2026-09-28 设计审查](design/DESIGN_REVIEW_20260928.md)。
- 工资系统（§8.2）、事件池扩展（§12.7.7）等为设计占位；SPEC 内大量 `[PLACEHOLDER]` 数值待实现阶段定
- 详见 [design/SPEC.md](design/SPEC.md)

---

## 来源文档

| 文档 | 内容 |
|------|------|
| [../maidmorework/docs/issues/TODO_V1.md](../maidmorework/docs/issues/TODO_V1.md) | MaidMoreWork V1 待解决问题清单 |
| [../maidmorework/docs/issues/KNOWN_ISSUES.md](../maidmorework/docs/issues/KNOWN_ISSUES.md) | 长期技术难题（含已关闭记录） |
| [../maidmorework/docs/design/MINE_REDESIGN.md](../maidmorework/docs/design/MINE_REDESIGN.md) | 矿井重构设计（拍板记录 + 未实现项） |
| [../maidmorework/docs/issues/TEST_LOGGING.md](../maidmorework/docs/issues/TEST_LOGGING.md) | 当前测试清单 |
| [../fenneclib/docs/TODO.md](../../../../fenneclib/docs/design/WEIGHTED_BEHAVIOR.md) | FennecLib 待办 |
| [design/SPEC.md](design/SPEC.md) | 游戏设计文档（含占位项） |
