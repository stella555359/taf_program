# Layer 1 仓库扫描器实现

## 目标

将 Layer 1 v2 实现为只读事实采集层：扫描 `robotws`，并把结构化 metadata record 写入 SQLite。

规范设计：[`../architecture/7-layer-architecture-spec.md`](../architecture/7-layer-architecture-spec.md)，章节 `2. Layer 1: Repository Scanner`。

## 最终决策

- 使用 Robot Framework 官方 AST parser 作为唯一的生产级 Robot parser。
- 保留旧 scanner/parser 代码作为参考，但不把它作为新架构主路径。
- 只提取直接逻辑动作；递归图遍历属于 Layer 2。
- 将结构化记录持久化到 SQLite；JSON export 只用于调试和审计。
- 标记边界字段：`record_type`、`domain`、`is_allowed`、`allowed_source`、`exclude_reason`。
- 标记 helper 复用信号：`python_impl_type` 和 `robot_impl_type`。

## 实现步骤

### 步骤 1：模块骨架和依赖

创建新的 Layer 1 v2 路径，不与现有轻量 scanner/parser 路径混在一起。

计划文件：

```text
src/robotws_mcp/layer1/__init__.py
src/robotws_mcp/layer1/records.py
src/robotws_mcp/layer1/robot_ast_parser.py
src/robotws_mcp/layer1/python_ast_parser.py
src/robotws_mcp/layer1/boundary.py
src/robotws_mcp/layer1/sqlite_store.py
src/robotws_mcp/layer1/scanner.py
```

计划依赖：

```text
robotframework
```

原因：Layer 1 v2 使用 `robot.api.parsing.get_model` 作为唯一的生产级 Robot parser。

### 步骤 2：记录模型

定义 dataclass record 和稳定 record ID：

- `RobotFileRecord`
- `TestCaseRecord`
- `KeywordRecord`
- `StepRecord`
- `ResourceImportRecord`
- `LibraryImportRecord`
- `VariableRecord`
- `PythonSymbolRecord`
- `ParseIssueRecord`

必需边界字段：

```text
record_type
domain
is_allowed
allowed_source
exclude_reason
```

稳定 ID 规则：

```text
record_type + path + name/owner + line_no
```

### 步骤 3：Robot AST 适配器

基于以下接口实现 Robot Framework AST 适配器：

```python
from robot.api.parsing import get_model
```

解析器职责：

- 解析 `.robot` 和 `.resource` 文件。
- 提取 settings、resource imports、library imports、variables、test cases、keywords、setup、teardown 和 direct steps。
- 保留源码位置和 `raw` 源码片段。
- 记录 `ParseIssueRecord`，不要回退到文本切分。

### 步骤 4：直接逻辑动作提取

将 Robot statement 转换为直接逻辑 `StepRecord` 条目。

规则：

- 从 setup、teardown、testcase body 和 keyword body 中提取直接逻辑动作。
- 将 `Run Keywords`、`AND` 和 `Run Keyword If` 视为控制包装器，而不是主要学习目标。
- 当 condition 静态可见时保留下来。
- 记录结构化的 `arguments`、`variables_input` 和 `variables_output`。
- 不要递归内联被调用 keyword 的 body；递归展开属于 Layer 2。

### 步骤 5：Python 静态符号解析器

增强对允许范围内 Python helper/library 文件的静态解析。

记录内容：

- class/function/method name
- qualified name
- signature
- docstring
- imports
- decorators
- source location
- `python_impl_type`: `taf_dependent | pure_python | mixed | unknown`
- `taf_dependencies`

不要在运行时 import 模块，也不要执行 Python 代码。

### 步骤 6：边界分类

使用当前 profile 规则对记录分类：

- `feature_allowlist`
- `confirmed_case_scopes`
- `allowed_resource_scopes`

规则：

- Testcase 只在 allowlisted feature path 或 confirmed case scope 下被允许。
- Keyword 在 allowed resource scope、allowlisted feature path 或 confirmed case scope 下被允许。
- 允许的 resource scope 中的 keyword 使用 `domain=Common`。
- 允许的 resource scope 中即使存在 `*** Test Cases ***`，也不作为有效 testcase 放行。
- Feature / `None_Feature_SG6` keyword 继承路径 domain，例如 `RRM` 或 `SISO`。
- Unknown 或 unresolved record 不应进入生成上下文。

### 步骤 7：SQLite V2 存储和调试导出

将 Layer 1 v2 record 持久化到独立的 SQLite 路径和表集合，避免影响旧 index 代码。

建议默认路径：

```text
data/indexes/robotws_layer1_v2.sqlite3
```

将常用查询字段存为列，将完整 normalized record 存为 JSON payload。

可选 JSON 调试导出：

```text
data/indexes/layer1_v2_scan_summary.json
data/indexes/layer1_v2_parse_issues.json
```

### 步骤 8：CLI 入口

新增 v2 scanner 入口，不替换旧 indexer。

建议脚本名：

```text
robotws-layer1-scan
```

建议命令形式：

```powershell
C:\Users\stlin\Python313\python -m robotws_mcp.layer1.scanner --robotws-root C:\TA\robotws --profile Hangzhou_SG6_Common --db-path data\indexes\robotws_layer1_v2.sqlite3 --write-index
```

### 步骤 9：聚焦单元测试

在以下目录添加测试：

```text
tests/layer1/
```

最小测试范围：

- Robot AST parser 能从 `Run Keywords ... AND ...` 中提取 setup 逻辑动作。
- Named arguments 会以结构化 `arguments` 存储。
- 对 assignment 和 `Set Test Variable` 提取 `variables_input` 与 `variables_output`。
- Keyword `[Arguments]` 会转换为 `arguments_schema`。
- Boundary classifier 能正确标记 allowlisted feature path 和 allowed resource scope。
- Python parser 将简单 pure Python helper 标记为 `pure_python`。
- Python parser 将 `taf.*` import 标记为 `taf_dependent`。
- SQLite store 能持久化并读回代表性记录。

## 验证交接

在目标环境 scan 执行并完成评审之前，不要将该层标记为已验证。

代码准备好后，用户侧可运行的开发者单元测试命令：

```powershell
cd C:\TA\robotws_mcp_server
C:\Users\stlin\Python313\python -m pytest tests\layer1
```

预期结果：

```text
所有 Layer 1 单元测试通过。
```

单元测试通过后，用户侧可运行的目标仓库扫描命令：

```powershell
cd C:\TA\robotws_mcp_server
C:\Users\stlin\Python313\python -m robotws_mcp.layer1.scanner --robotws-root C:\TA\robotws --profile Hangzhou_SG6_Common --db-path data\indexes\robotws_layer1_v2.sqlite3 --write-index
```

预期结果：

```text
Scan 完成且没有崩溃。
SQLite 文件存在于 data\indexes\robotws_layer1_v2.sqlite3。
Scan summary 会报告 robot files、testcases、keywords、steps、Python symbols 和 parse issues。
Parse issues 会作为记录报告，而不是未处理异常。
```

实际验收结果：

```text
已在 C:\TA\robotws 上完成目标仓库扫描。
以下计数是 Hangzhou_SG6_Common 的 path_scopes 扫描范围内的总解析量，不是 feature_allowlist 过滤后的允许数量。
robot_files: 3499
testcases: 4402
keywords: 43123
steps: 293209
resource_imports: 9668
library_imports: 5884
variables: 31251
python_symbols: 9569
parse_issues: 0
sqlite_path: data\indexes\robotws_layer1_v2.sqlite3
empty_name_testcases: 0
```

testcase 边界分布：

```text
feature_allowlist: 110
  RRM: 69
  SISO: 41
confirmed_case_scope: 119
  RRM: 65
  SISO: 54
allowed_resource_scope: 0
excluded_feature_not_in_allowlist: 4116
excluded_resource_scope_testcases: 57
```

常见失败模式：

- `ModuleNotFoundError: robot`：添加 `robotframework` 后安装项目依赖。
- AST node 形状不匹配：根据已安装的 Robot Framework 版本更新 adapter 测试。
- Dynamic resource path 无法解析：应生成 `ParseIssueRecord`，而不是让 scan 失败。
- Boundary 计数看起来过宽：修改生成过滤器之前，先检查 `is_allowed=false` 和 `exclude_reason` 记录。

## 学习记录

- 已解决的问题：用基于 AST 的结构化事实替换轻量解析，作为 Layer 1 主路径。
- 变更文件：
  - `pyproject.toml`：添加 `robotframework` 依赖和 `robotws-layer1-scan` 入口。
  - `src/robotws_mcp/layer1/__init__.py`：创建独立的 Layer 1 v2 package。
  - `src/robotws_mcp/layer1/records.py`：定义结构化 Layer 1 record 和稳定 record ID。
  - `src/robotws_mcp/layer1/boundary.py`：根据当前 profile 分类 path/domain/allowed boundary。
  - `src/robotws_mcp/layer1/robot_ast_parser.py`：使用官方 AST 解析 Robot 源码，并提取直接逻辑动作。
  - `src/robotws_mcp/layer1/python_ast_parser.py`：将 Python helper 解析为静态符号，并分类 `python_impl_type`。
  - `src/robotws_mcp/layer1/sqlite_store.py`：将 Layer 1 record 持久化到独立 SQLite v2 schema。
  - `src/robotws_mcp/layer1/scanner.py`：添加 Layer 1 v2 scanner 和 CLI。
  - `tests/layer1/`：添加 boundary、Robot AST parsing、Python AST parsing 和 SQLite persistence 的聚焦测试。
- 核心调用流：`scanner -> Robot AST / Python AST parser -> boundary classifier -> SQLite v2 store -> JSON debug summary`。
- 关键字段：`record_type`、`domain`、`is_allowed`、`allowed_source`、`exclude_reason`、`arguments`、`variables_input`、`variables_output`、`python_impl_type`、`robot_impl_type`。
- 验证命令：见 `验证交接`。
- 预期结果：见 `验证交接`。
- 常见失败模式：见 `验证交接`。
- 评审问题：
  - Allowlisted feature testcase 和 allowed common resource 是否都有 `is_allowed=true`？
  - Feature-local keyword 是否按 domain 分域，而允许的 resource keyword 是否为 `domain=Common`？
  - 是否能识别 TAF 依赖动作，同时不强制复用 pure helper？
  - Parse 问题是否能通过 `ParseIssueRecord` 检查，而不是被隐藏为失败？
