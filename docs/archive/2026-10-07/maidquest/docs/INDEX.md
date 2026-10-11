> 历史索引快照，2026-10-07 已被新入口替代。

# MaidQuest 文档

> 版本：0.1.0（统一身份改造完成，待游戏内验证） | MC 26.1.2 / NeoForge | JDK 25
> 全项目待办总览：[../../docs/TODO.md](../../docs/TODO.md)

女仆委托模组：任务板发布委托，普通 TLM 女仆在移动范围内有委托板时默认接单、执行并交付。

## 文档列表

| 文档 | 说明 |
|------|------|
| [API.md](../../../../../maidquest/docs/API.md) | 公开 API 参考：QuestApi / QuestActor / IQuestType / 注册表 / 事件 / 材料单接口 |
| [design/QUEST_WORLD_DATA_AND_DISMANTLE.md](design/QUEST_WORLD_DATA_AND_DISMANTLE.md) | 委托数据全局化（B 方案）与安全拆除流程实施计划（已拍板，待实施） |
| [订单生产链设计](../../docs/design/MAIDQUEST_MMW_ORDER_CHAIN.md) | 与 MaidMoreWork 的委托倾向、工分工资和公共仓库交易设计（讨论中，非当前功能；其中"受益中心持有订单"部分已被统一身份改造取代） |
| [TEST_LOGGING.md](TEST_LOGGING.md) | 当前测试清单（操作人用） |
| [CHANGELOG.md](../../../../../maidquest/docs/CHANGELOG.md) | 版本更新记录（仅作者明确要求时记录） |

## 包结构

```
com.fennecmomo.maidquest/
  MaidQuest.java                        # @Mod 入口（自注册全部内容）
  MaidQuestExtension.java               # TLM 扩展入口（注入全女仆接单行为）
  MaidQuestConfig.java                  # 行为常量
  MaidQuestCommonConfig.java            # 玩家配置（委托模式开关，COMMON）
  ModAttachments.java                   # 认领委托 Attachment（执行缓存）
  api/
    QuestApi.java                       # 对外静态入口
    QuestPublishArgs.java               # 发布表单参数（产物 / 材料）
    IQuestType.java                     # 委托类型接口
    IQuestExecutor.java                 # 执行器接口
    QuestTypeRegistry.java              # 类型注册表（+ @RegQuestType 发现）
    IQuestWeightProvider.java           # 匹配度加权接口
    QuestWeightRegistry.java            # 加权注册表
    WorkTypeWeightProvider.java         # 默认加权（当前工作类型匹配）
    QuestEligibilityRegistry.java       # 外部接单资格回调
    MaterialSupplyQualifier.java        # 供货资格接口（供货模组实现）
    MaterialSupplyRegistry.java         # 供货资格注册表
    MaterialOrderInfo.java              # 材料单对外最小视图
    event/                              # 发布/认领/完成/取消 + 类型注册事件
  quest/
    Quest.java / QuestCore.java / QuestStatus.java / QuestAssignment.java
    QuestActor.java                     # 统一参与者身份（女仆 / 玩家 / 无身份）
    MaterialCondition.java / MaterialSource.java
    type/                               # 内置类型：制作（交付型）；材料（供货型）；建造为未开放占位
                                        # 兼容型委托（矿井挖矿等）由任务定义方注册
  service/
    QuestService.java                   # 统一发布/认领/进度/提交/放弃/领取/取消/材料单
    QuestBoardRegistry.java / QuestBoardData.java   # 任务板登记（SavedData）
    QuestMatcher.java                   # 可接委托筛选与加权抽取
    QuestInventoryHelper.java           # TLM 背包读写工具（与掉落同 handler）
    QuestItemMarker.java                # 订单物品标记（防串单）
    QuestFeedback.java                  # TLM 女仆音效 + 聊天气泡
    CraftingCatalog.java                # 工作台配方产物目录（分页同步）
  ai/
    QuestExtraMaidBrain.java            # IExtraMaidBrain 注入 WORK 活动
    QuestClaimBehavior.java / QuestExecuteBehavior.java / QuestSubmitBehavior.java
  compat/
    ClothConfigCompat.java              # TLM 配置界面扩展（委托模式开关）
  block/ + menu/ + client/ + network/ + command/ + registry/
```

## 设计要点

- **统一身份**：发布者与接取者共用同一身份模型（女仆 / 玩家 / 无身份）；发布链路不分渠道，玩家界面、命令与女仆/模组调用汇聚到同一个发布服务；判权一律按身份编号，名字只作显示。
- **接取只开放女仆**：玩家可发布、撤销自己的委托、领取完成品，但当前不接单。
- **去中心化**：订单归属 = 发布者本人，没有受益中心概念；管理女仆离开工程中心时由供货模组（MMW）调用「按发布者批量撤单」清理她派发的材料单。
- **普通女仆标准**：行为通过 TLM `IExtraMaidBrain.getWorkBehaviors()` 注入所有女仆，无需指派任务；背包读写走 TLM `MaidItemManager`。
- **不依赖 maidmorework/maidtown**：只依赖 TLM + FennecLib；与 MMW 通过 QuestApi 事件与材料单接口对接。
- **委托模式**：全局配置项（默认开启），在 TLM 配置界面（Cloth Config）或 `config/maidquest-common.toml` 修改。
- **持久化**：委托本体、每单托管和找回中心在每维度 `QuestBoardData` 中；任务板方块实体只负责交互。认领关系的权威记录在订单上，女仆 Attachment 是执行缓存；执行器运行时状态可重建。
- **匹配度加权**：默认按女仆当前 TLM 任务名匹配；第三方可注册 `IQuestWeightProvider` 叠加技能等影响。
