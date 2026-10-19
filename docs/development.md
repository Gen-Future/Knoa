# 开发指南

## 本地布局

父目录只是工作区容器，`Knoa/` 与 `Knoa-Parse/` 是两个独立 Git 仓库。所有 Git 命令进入目标仓库执行；不在父目录执行 `git init`。单独克隆任意一个仓库，也应能运行它自己的检查。

本地目录名 `Knoa-Parse` 与 GitHub 仓库路径 `Gen-Future/knoa-Parse` 大小写不同，远端 URL 保持 GitHub 的实际拼写。

## 准备阶段检查

需要 Python 3.11+。它只是仓库工具，不约束未来产品语言。

先运行 `python3 --version`；若解析到 macOS 自带的 Python 3.9，请用已安装的 3.11+ 解释器创建虚拟环境（例如 `python3.11 -m venv .venv`）。后续始终使用 `.venv/bin/python`，避免目录变化导致选错解释器。

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-check.txt
.venv/bin/python scripts/check.py
.venv/bin/python -m unittest discover -s tests -v
git diff --check
```

检查包括：Git 非忽略文件的 UTF-8 文本规范、简单 Markdown 相对文件链接、JSON/YAML 语法、Parse Schema 和合成样例、主仓契约快照摘要。Markdown 检查不验证标题锚点或远端链接可用性；目前也不校验业务实现或运行时依赖边界。

CI 在 push 和 pull_request 时执行同样的命令，权限仅为 contents: read；当前未部署任何服务。Actions 用法参考 [checkout](https://github.com/actions/checkout) 和 [setup-python](https://github.com/actions/setup-python)。

## 分支与提交

默认分支 `main`。任务使用短期分支，如 `docs/architecture`、`feat/first-memory-flow`。提交说明使用中文，例如 `docs: 明确双仓职责与解析契约`。

当前准备文件尚未提交或推送。准备首次发布时先复核待加入文件，运行检查，再提交；有网络访问后先确认远端仍为空，再推送。若远端已经有提交，先获取并协调历史，禁止用强推覆盖。

## 技术栈确认后

补充包管理配置、锁文件、格式化与静态检查、模块依赖检查、产品测试和本地启动方式。未实际选择数据库、端口和模型前，不创建伪配置、空容器服务或含猜测变量的 `.env.example`。
