# ADR 0001：Knoa 与 Knoa Parse 双仓边界

- 状态：已确认（仓库与职责划分）
- 日期：2026-10-14
- 依据：用户本次明确指定命名、解析独立仓库、其余部分进入主仓库。

## 决策

主仓 `Gen-Future/Knoa` 采用单仓多模块。解析独立在 `Gen-Future/knoa-Parse`。两个仓库独立版本管理、检查和未来发布；不使用 Git submodule，不在父目录再建立第三个代码仓库。

主仓保留 `apps/api`、`apps/console`、`apps/worker` 和 `packages/core`、`writing`、`retrieval`、`curation`。`packages/ingestion` 收窄为接入协调与解析结果导入。平台适配、系统评测与整套部署配置留在主仓。

## 原因

记忆模型、写入、纠偏与检索需要共同演进，主仓内一次修改可以覆盖这些能力。解析具有独立工具与算力依赖，也具备被其他产品复用的价值。

## 后果

跨仓协作需要版本化证据契约和兼容检查。主仓不能直接引用相邻 Parse 源码；Parse 不能导入主仓内部类型或访问主仓数据库。独立部署与仓库划分分别决策。

解析仓内部目录、契约字段、SDK/HTTP 传输方式和具体技术栈尚未确认，见 [待决事项](../decisions.md)。
