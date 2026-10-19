# 契约

`knoa-parse/v0.1.0-draft.1/` 是 Parse 仓库契约的只读消费快照；不是第二份独立设计。字段和语义的权威说明位于 [Knoa Parse](https://github.com/Gen-Future/knoa-Parse)。本版本尚未发布，也未承诺兼容。

当前只定义解析结果，不定义 HTTP 路由、认证、上传、轮询、分页或记忆模型。见 [ParseResult Schema](knoa-parse/v0.1.0-draft.1/parse-result.schema.json) 和 [成功示例](knoa-parse/v0.1.0-draft.1/examples/success.json)。

## 同步流程

1. 先在 Parse 仓库修改 Schema、语义说明和用例，运行生产侧检查。
2. 字段变更增加草案版本；正式发布后再明确稳定版本兼容策略。
3. 在主仓导入选定版本的 Schema、协议说明与合成样例，更新 [UPSTREAM.json](knoa-parse/UPSTREAM.json) 中的文件摘要。
4. 上游有真实提交或发布后填写对应 `source_commit`；当前为 `null`，表示共同初始化的未发布草案，不能用作发布溯源。
5. 运行主仓检查与消费者回归，评审通过后再升级运行时适配器。

摘要用于检测意外漂移，不证明来源可信或运行时兼容。两仓的契约回归当前只验证草案格式与部分结构约束，尚不代表真实解析器和导入器已经互通。

主仓 HTTP/MCP 契约与记忆写入契约将在使用场景、授权模型和技术栈确定后另行设计。
