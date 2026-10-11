> 历史归档（2026-10-07）：保留整理前正文，仅重定位相对链接。旧确认、旧待办和旧实现状态不代表当前状态；当前规则见 [统一设计](../../../design/current/README.md)。

# MaidTown 项目状态

> 最后更新：2026-09-26

## 项目架构

```
fenneclib（基础库）→ TLM
maidmorework → TLM + fenneclib
maidquest → TLM + fenneclib
maidtown → TLM + fenneclib + maidmorework + maidquest
```

## 模块现状

| 模块 | mod_id | 包名 | Git | Java 文件 | 状态 |
|------|--------|------|-----|----------|------|
| fenneclib | fenneclib | com.fennecmomo.fenneclib | FennecLib 已同步 | 17 | v0.0.2 开发中（ButtonListItem 修复，待发布） |
| maidmorework | maidmorework | com.fennecmomo.maidmorework | MaidMoreWork 已同步（分支 1.26.1） | 63 | v0.1.3 已发布（Pre-release） |
| maidquest | maidquest | com.fennecmomo.maidquest | MaidQuest 已同步（main） | 68 | 统一身份改造完成（待游戏内验证）；订单链未实现 |
| maidtown | maidtown | com.fennecmomo.maidtown | MaidTown 原始快照已同步（main） | 38 | 旧版本，暂缓开发，当前无法编译 |

模块职责：

- **fenneclib** — 加权行为框架 + UI 模板组件
- **maidmorework** — TLM 行为包（砍树 / 矿井挖矿 / 工程中心 / 仓库）
- **maidquest** — 委托系统（独立模组：任务板发布 / 普通女仆默认接单执行交付 / 对外扩展 API），仅依赖 TLM + fenneclib
- **maidtown** — 主模组（居民/领地/身份/需求/记忆/GUI）

> maidquest 已完成统一身份改造：发布者/接取者统一身份（女仆 / 玩家），玩家与女仆发布走同一套链路，判权按身份编号；订单归属 = 发布者本人，受益中心机制已删除，接取只开放女仆（玩家供货走供货模组公共仓库渠道）。行为经 TLM `IExtraMaidBrain` 注入所有女仆；技能加权预留 `IQuestWeightProvider` 扩展点。
> maidtown 仍基于 maidmorework 早期 API 开发（`SearchBehavior` / `ISearchAction` / `IMaidmoreHost` 已随重构移除），且原代注册了 maidquest 的方块/BE/网络/命令，需重做适配（见 `docs/TODO.md` I6）。
> 规划中的 MQ×MMW 订单驱动生产链见 [design/MAIDQUEST_MMW_ORDER_CHAIN.md](design/MAIDQUEST_MMW_ORDER_CHAIN.md)；这是设计讨论记录，不代表现有模块已实现订单模式、制作／管理工种或经济规则（其中"受益中心持有订单"部分已被统一身份改造取代）。

## 共享资源

- `libs/` — 共享 TLM jar 依赖
- `refs/` — 参考模组 jar（TLM / 百年战争 / 殖民地）
- `run-shared/` — 共享运行目录（`mods/`：fenneclib-0.0.1 + maidmorework-0.1.4；maidquest 经 gradle runClient 以开发态加载）
- `.opencode/` — AI 项目记忆（`project.md`）+ 发布工具（`tools/gh-release.ps1`）
- `docs/` — 项目文档（规范/参考/设计，待办总览见 `docs/TODO.md`）
- `temp_decompile/` — TLM 反编译参考源码
- `net/` — MC 源码参考片段（RenderType）
- `Blocks/` — SPBlock 废弃方案的模型资产（保留备查，见 `maidmorework/docs/deprecated/spblock.md`）

## 技术栈

- Minecraft 26.1.2 / NeoForge 26.1.2.76
- JDK 25 (Temurin) / Gradle 9.2.1
- NeoGradle ModDev 2.0.141

## 关键架构决策

- 所有 Behavior 泛型使用 TLM 的 `EntityMaid`，行为不依赖自定义实体
- 模块接口（历史设计，待 maidquest/maidtown 跟进时重建）：`IMaidmoreHost` → `IMaidquestHost` → `ColonistEntity`
- 任务所有权通过 Attachment 持久化
- SPBlock 方案已废弃，改为懒 BFS 验证
- 工程系统从 CompoundTag 手动序列化升级为 Codec + SavedData 方案
- 矿井 = 工程中心子类（多态 Codec 分派），复用同一套实例管理器 + 通用仓库/困难表
- 版本号按变更级别递增（系统级 / 模块级 / 修改级）；发布走 GitHub Release（alpha / beta → Pre-release）
