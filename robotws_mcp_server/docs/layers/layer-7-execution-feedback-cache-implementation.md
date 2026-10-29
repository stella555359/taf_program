# Layer 7 执行反馈缓存实现

## 目标

记录真实执行反馈，使后续检索、治理、验证和模板选择能够从稳定模式与不稳定模式中学习。

规范设计：[`../architecture/7-layer-architecture-spec.md`](../architecture/7-layer-architecture-spec.md)，章节 `8. Layer 7: Execution Feedback Cache`。

## 草案范围

- 等核心 scanner、graph、governance、retrieval、template 和 validation 层稳定后再推进。
- 后续来源可以包括 Jenkins log、Robot output、Allure report、CI result、failure classification 和 testline metadata。
- 使用反馈进行排序、告警、规避 flaky keyword，以及提出自愈建议。

## 最终决策

- Layer 7 第一版现在实现，但保持轻量、可导入、可查询。
- 支持三类输入：
  - Robot Framework `output.xml`。
  - Jenkins build result / log summary JSON。
  - 手工提交 execution feedback。
- 不直接连接 Jenkins API，不拉远端日志；先支持本地文件导入和 API/MCP 手工提交。
- 缓存用于：
  - Layer 4 ranking hints。
  - Layer 6 validation warnings。
  - 查询某个 keyword / testcase 的历史失败摘要。

## 实现步骤

新增：

```text
src/robotws_mcp/layer7/__init__.py
src/robotws_mcp/layer7/models.py
src/robotws_mcp/layer7/sqlite_store.py
src/robotws_mcp/layer7/importers.py
src/robotws_mcp/layer7/service.py
src/robotws_mcp/layer7/import_feedback.py
```

SQLite 表：

```text
layer7_execution_feedback
layer7_keyword_feedback_summary
```

第一版工具：

```text
record_execution_feedback(feedback)
import_robot_output_xml(path, profile, testline)
import_jenkins_result_json(path)
get_execution_feedback(query, profile, limit)
get_feedback_hints(record_id_or_name, profile)
```

关键字段：

```text
source_type
source_path
test_name
keyword_name
status
failure_class
message
elapsed_ms
profile
testline
metadata
```

## 验证交接

当前验证命令：

```powershell
py -m pytest tests/layer7 -q
py -m pytest -q
```

预期结果：

- 可导入最小 Robot `output.xml`。
- 可导入 Jenkins JSON。
- 可手工记录 feedback。
- 查询同名 keyword / testcase 时返回 failure hints。

## 学习记录

- 已解决的问题：
  - 先不依赖 Jenkins API，降低部署复杂度。
  - 将真实执行反馈以 SQLite cache 形式提供给 Layer 4/6。
- 变更文件：
  - `src/robotws_mcp/layer7/`
  - `tests/layer7/`
- 核心调用流：
  - execution result file / manual feedback -> importer/service -> SQLite feedback cache -> retrieval / validation hints。
- 关键字段：
  - `source_type`
  - `test_name`
  - `keyword_name`
  - `status`
  - `failure_class`
  - `message`
  - `profile`
  - `testline`
- 验证命令：
  - `py -m pytest tests/layer7 -q`
  - `py -m pytest -q`
- 预期结果：
  - feedback record 可写入、可查询。
  - failed keyword 会产生 warning hint。
- 常见失败模式：
  - Robot output.xml 格式版本差异。
  - Jenkins JSON 字段不统一。
- 评审问题：
  - 后续是否接 Jenkins API 和 Allure report。
