# Knoa

面向个人、团队与组织的记忆基础设施，让不同 Agent 能够持续使用可追溯、可修正的记忆。

**当前阶段：项目准备。** 本仓库包含架构、目录边界、契约草案与检查工具，尚未实现可运行产品。语言、框架、数据库和模型供应商均待选型。

## 两个仓库

| 仓库 | 职责 |
| --- | --- |
| [Knoa](https://github.com/Gen-Future/Knoa) | 记忆模型、形成与纠偏、检索、长期整理、HTTP/MCP 接入、后台任务、管理工作台与平台适配 |
| [Knoa Parse](https://github.com/Gen-Future/knoa-Parse) | 独立解析资料，输出带来源版本和位置的标准化证据；不决定长期记忆 |

## 目录

```text
apps/                 可运行入口：api、console、worker
packages/             core、ingestion、writing、retrieval、curation
integrations/         外部 Agent 平台适配
contracts/            对外契约及 Knoa Parse 契约快照
evals/                质量评测设计与未来评测集
deploy/               未来的本地启动与部署配置
docs/                 架构、设计决策与开发指南
scripts/              仓库检查工具
tests/                契约回归检查
```

`ingestion` 只负责接入协调和解析结果导入，具体解析实现归 Knoa Parse。主仓内部优先通过模块公开接口协作，模块划分不意味着必须拆成网络服务。

## 从这里开始

1. 阅读 [项目定义](docs/vision.md) 和 [架构与依赖边界](docs/architecture.md)。
2. 阅读 [决策记录](docs/adr/0001-repository-boundaries.md) 与 [待决事项](docs/decisions.md)，区分已确认方向和实现建议。
3. 按 [开发指南](docs/development.md) 运行准备阶段检查。
4. 从 [路线图](docs/roadmap.md) 的 M0 选型任务开始，再进入第一条垂直链路。

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-check.txt
.venv/bin/python scripts/check.py
.venv/bin/python -m unittest discover -s tests -v
```

Python 3.11+ 仅用于检查文档与契约，不代表产品后端已选择 Python。当前没有产品启动命令。

许可证尚未确定，仓库暂不附加许可证文本。参与开发前请阅读 [贡献约定](CONTRIBUTING.md)。
