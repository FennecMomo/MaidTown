> 文档分类（2026-10-07）：版本相关技术参考，按主题保留；不是产品规格或本轮运行验证结果。公开接口以当前源码／依赖核对。 [统一入口](../../../../INDEX.md).

# 车万女仆 26.1 依赖更新记录（2026-09-26）

- 上游仓库：https://github.com/TouhouLittleMaid/TouhouLittleMaid-26.1.git
- 采用发布：https://github.com/TouhouLittleMaid/TouhouLittleMaid-26.1/releases/tag/snapshot-2026-08-24-14-04-03
- 对应提交：`73673c66db4f43bb8f1e750611e3af3696d20bb5`（2026-08-24）。
- 官方运行 JAR：`touhoulittlemaid-2.0.0-neoforge+mc26.1.2-snapshot.jar`，23,997,413 字节，SHA-256 `b0105bb9b1fd02234024bc9e371a77dfe1631bf795cb98fd7fc7198a52e2fe29`。已核对 ZIP 完整性。
- 生效位置：`libs/`（MQ、MMW 的 `build.gradle` 均从此路径引用）；`refs/` 的同名参考 JAR 也同步。最新源码浅克隆到 `refs/TouhouLittleMaid-26.1/`，`origin` 指向上游仓库。
- 旧运行 JAR 备份：`libs-backup/touhoulittlemaid-2.0.0-neoforge+mc26.1.2-pre-20260926.jar`，SHA-256 `3b1f0c5f0cc62da1ebeecc90e6d723d2df7ee214fe896bcb785656fe2be30599`。旧文件名与新文件名相同，不能仅靠文件名判断是否更新。
- 上游从 2026-07-02 发布标签至此次标签共 13 个提交，涉及任务代码修正、女仆 GUI 资源路径、背包资源空值判断、模型下载、Curios、骑乘放置位置等。上游最新快照依旧面向 Minecraft 26.1.2；其构建 NeoForge 为 26.1.2.87，本地 MQ、MMW 当前为 26.1.2.76。
- 使用新 JAR 后分别在 MQ、MMW 执行 `./gradlew --offline jar`，两者退出码均为 0，Java 编译任务均执行。尚未启动客户端/服务端，也未验证运行时与本地 NeoForge 26.1.2.76 的兼容性。
- 桌面 `女仆模组联调.bat` 会在启动前重新构建 MQ、MMW；TLM 是 `libs/` 的开发运行依赖，`run-shared/mods` 中只保留 MMW JAR，不应额外放入第二份 TLM JAR。
