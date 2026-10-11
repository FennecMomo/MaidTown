# MaidTown

后续以本目录作为单一 MaidTown 模组与 Git 仓库的根目录，不再维护多个子模组仓库。

当前仅完成工作区整理；新的模组源码、Gradle 工程和重构实现尚未建立。

## 旧项目归档

2026-10-11，原 `fenneclib`、`maidmorework`、`maidquest`、`maidtown` 目录及旧启动脚本已迁至：

`D:\ModProduce\MaidTown-legacy-20261011`

归档保留各仓库的 `.git`、未提交修改、未跟踪文件及原有构建目录。迁移前的 HEAD、工作区状态与远端信息记录在归档目录的 `migration-manifest.json`。

根目录 `docs/` 保持原位，内容未因本次迁移修改。文档中的旧模块相对链接可能暂时失效，待文档维护会话统一调整。

`refs/`、本地依赖、运行目录及反编译目录保留在本地，由 `.gitignore` 排除。新仓库用于记录后续单一模组的开发；本次初始化不推送远端，也不覆盖旧远端历史。
