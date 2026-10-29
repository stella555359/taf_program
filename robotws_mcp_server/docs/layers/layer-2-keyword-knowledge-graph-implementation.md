# Layer 2 关键字知识图谱实现

## 目标

基于 Layer 1 记录构建图视图，使 testcase、keyword、resource、variable 以及 TAF 依赖关系可以被遍历和解释。

规范设计：[`../architecture/7-layer-architecture-spec.md`](../architecture/7-layer-architecture-spec.md)，章节 `3. Layer 2: Keyword Knowledge Graph`。

## 草案范围

- 将 Layer 1 记录作为事实来源。
- 基于 `StepRecord` 构建 keyword 直接调用图。
- 解析 testcase -> setup/teardown/body -> keyword 关系。
- 在适当位置沿 keyword 图传播 `taf_dependent`。
- 保持图遍历逻辑与 Layer 1 扫描逻辑分离。

## 最终决策

- Layer 2 是 deterministic keyword dependency graph layer，不重新扫描 `robotws`，不重新 parse Robot source，不做 semantic retrieval。
- Layer 2 MVP 不自动推断完整测试状态机。`PRODUCES_STATE`、`CONSUMES_STATE`、`NEXT_POSSIBLE`、`FORBIDDEN_BEFORE`、`FORBIDDEN_AFTER` 放到 Layer 2.5。
- `step` 是独立 graph node，因为一次调用本身包含 `ordinal`、`normalized_type`、`arguments`、`condition`、`variables_input`、`variables_output`、`line_no` 和 `raw`。
- `impl_type` 只使用 `taf_dependent | pure_logic | unknown`，不持久化 `mixed`。
- 在 allowed RobotWS boundary 内，namespace-style、plain-name TAF/device 操作或明显底层执行调用如果无法解析到 Robot keyword / local Python symbol，应归类为 `taf_library_keyword`，并作为 TAF dependency evidence。
- Layer 2 使用独立 SQLite graph index，例如 `data/indexes/robotws_layer2_graph.sqlite3`。

## 实现步骤

### 步骤 1：模块骨架和数据模型

创建独立 Layer 2 模块，不混入 Layer 1：

```text
src/robotws_mcp/layer2/__init__.py
src/robotws_mcp/layer2/models.py
src/robotws_mcp/layer2/sqlite_store.py
src/robotws_mcp/layer2/input_loader.py
src/robotws_mcp/layer2/graph_builder.py
src/robotws_mcp/layer2/resolver.py
src/robotws_mcp/layer2/dependency.py
src/robotws_mcp/layer2/query.py
src/robotws_mcp/layer2/build_graph.py
```

核心数据模型：

```text
GraphNode
GraphEdge
ResolutionResult
DependencySummary
Layer2BuildSummary
```

### 步骤 2：SQLite Store

实现 Layer 2 独立 SQLite schema：

```text
layer2_nodes
layer2_edges
layer2_resolution_results
layer2_dependency_summary
layer2_build_info
```

先写 store round-trip tests，确保常用列和 JSON payload 一致。

### 步骤 3：Layer 1 Input Loader

从 Layer 1 SQLite 读取 records：

- 按 `record_type` 读取 Layer 1 payload。
- 默认过滤 `is_allowed=true`。
- 支持 debug mode 读取 excluded records。
- 按 `id`、`path`、`name` 建索引，供 resolver 使用。

Input loader 不做 parse，不做 graph decision。

### 步骤 4：Node Builder

把 Layer 1 records 转成 graph nodes：

- testcase -> `testcase`
- keyword -> `keyword`
- step -> `step`
- resource path -> `resource_file`
- Python symbol -> `python_symbol`
- domain / feature -> synthetic `domain` / `feature`
- namespace-style 和 plain-name TAF/device fallback calls 后续可生成 synthetic `taf_library_keyword:*`

### 步骤 5：Base Edge Builder

建立确定性边：

```text
HAS_STEP
DEFINED_IN
IMPORTS_RESOURCE
IMPORTS_LIBRARY
BELONGS_TO_DOMAIN
BELONGS_TO_FEATURE
```

这一步不猜 keyword call，只连接 Layer 1 已经明确的结构关系。

### 步骤 6：Keyword Resolver

实现 `StepRecord.keyword` resolution。

优先级：

1. 显式 namespace 调用。
2. 当前文件内 keyword。
3. 当前文件 direct resource imports。
4. 当前文件 resource import closure。
5. allowed resource scope 内唯一匹配 keyword。
6. imported library / local Python symbol。
7. Robot Framework built-in / known control keyword。
8. excluded。

关键规则：

- 多候选标记为 `excluded`，保留候选列表用于 debug。
- 候选存在但不在 allowed boundary，标记为 `excluded`。
- namespace-style 或 plain-name TAF/device 操作找不到本地定义，标记为 `taf_library_keyword`。
- 普通 unknown call 如果不命中 TAF/device fallback pattern，标记为 `excluded`，不进入 generation context，也不递归展开。
- 每条 resolution 保留 `reason`、`candidates` 和 `import_evidence`。

### 步骤 7：CALLS Edge Builder

根据 resolution results 建立：

```text
step -> CALLS -> called_target
```

如果 target 是真实 keyword / python symbol，指向真实 node。

如果 target 是 TAF library call，生成 synthetic node，例如：

```text
taf_library_keyword:csn.execute
```

### 步骤 8：TAF Dependency Propagation

沿 `CALLS` 图传播 TAF dependency：

- `taf_library_keyword` 是 TAF evidence。
- `PythonSymbolRecord.python_impl_type=taf_dependent` 是 TAF evidence。
- 任何直接或间接有 TAF evidence 的 testcase / keyword 标记为 `taf_dependent`。
- 无 TAF evidence 且 resolved graph 清楚，标记为 `pure_logic`。
- 有 excluded 影响判断，标记为 `unknown`。

Propagation 必须防 cycle，并保存 evidence paths。

### 步骤 9：Query Service

先实现 Python query service，对应 6 个工具：

```text
get_testcase_graph
get_keyword_graph
resolve_keyword_call
explain_taf_dependency
find_keyword_callers
get_unresolved_calls
```

查询时从 SQLite 拉相关子图，在 Python 内存里做 depth traversal、cycle detection 和 result assembly。

### 步骤 10：MCP / HTTP 暴露

把 query service 接到现有 MCP / API 层。

工具按 LLM query action 设计，不暴露 `get_node`、`get_edge`、`get_resolution_row`、`get_import_closure` 这类内部函数。

### 步骤 11：CLI Build Entry

新增 Layer 2 build 入口：

```text
python -m robotws_mcp.layer2.build_graph --layer1-db data/indexes/robotws_layer1_v2.sqlite3 --db-path data/indexes/robotws_layer2_graph.sqlite3 --profile Hangzhou_SG6_Common
```

输出 build summary：

```json
{
  "nodes": 123,
  "edges": 456,
  "resolution_status_counts": {
    "resolved": 100,
    "taf_library_keyword": 20,
    "excluded": 8
  },
  "dependency_summary_counts": {
    "taf_dependent": 80,
    "pure_logic": 30,
    "unknown": 10
  }
}
```

### 步骤 12：测试策略

测试分三层：

- Unit tests：models、store、resolver normalization、dependency propagation cycle handling。
- Fixture tests：小型 Robot fixture 覆盖 resource import closure、多候选 excluded、taf namespace fallback。
- Integration tests：用 Layer 1 SQLite fixture build Layer 2 graph，并验证 6 个 query API 输出。

## 验证交接

Layer 2 最小闭环：

```text
models -> sqlite_store -> input_loader -> node_builder -> base_edges -> resolver -> calls_edges -> dependency -> query
```

调试验收命令：

```powershell
py -m pytest tests/layer2 -q
py -m pytest -q
py -m robotws_mcp.layer2.build_graph --layer1-db data/indexes/robotws_layer1_v2.sqlite3 --db-path data/indexes/robotws_layer2_graph.sqlite3 --profile Hangzhou_SG6_Common
```

预期结果：

- `tests/layer2` 通过，覆盖 resource import closure、`taf_library_keyword` fallback、TAF dependency propagation 和 query service。
- 全量 pytest 通过，证明 Layer 2 接入没有破坏既有 API / Layer 1 行为。
- build graph CLI 输出 `nodes`、`edges`、`resolution_status_counts`、`dependency_summary_counts`。
- `resolution_status_counts` 中应能看到 `resolved` 和 `taf_library_keyword`；如果 `excluded` 很多，应优先用 `get_unresolved_calls` 调试。

## 学习记录

- 已解决的问题：
  - Layer 2 / Layer 2.5 边界已明确：状态机语义后置到 Layer 2.5。
  - Keyword Resolution 明确保守原则：多候选和 unknown call 都归为 `excluded`，不硬猜。
  - Namespace-style 和 plain-name TAF/device 未解析调用在 RobotWS allowed boundary 内默认视为 `taf_library_keyword`。
  - TAF propagation 不持久化 `mixed`，只使用 `taf_dependent | pure_logic | unknown`。
- 变更文件：
  - `docs/architecture/7-layer-architecture-spec.md`
  - `docs/layers/layer-2-keyword-knowledge-graph-implementation.md`
  - `src/robotws_mcp/layer2/`
  - `src/robotws_mcp/server.py`
  - `src/robotws_mcp/api.py`
  - `pyproject.toml`
  - `tests/layer2/test_layer2_graph.py`
- 核心调用流：
  - Layer 1 records -> Layer 2 nodes -> base edges -> keyword resolution -> `CALLS` edges -> TAF dependency summary -> query tools。
- 关键字段：
  - `node_id`
  - `edge_type`
  - `step_id`
  - `resolution_status`
  - `called_target`
  - `impl_type`
  - `evidence_paths`
- 验证命令：
  - `py -m pytest tests/layer2 -q`
  - `py -m pytest -q`
  - `py -m robotws_mcp.layer2.build_graph --layer1-db data/indexes/robotws_layer1_v2.sqlite3 --db-path data/indexes/robotws_layer2_graph.sqlite3 --profile Hangzhou_SG6_Common`
- 预期结果：
  - 可解释 testcase / keyword 调用图。
  - 可解释每个 step call 的 resolution reason。
  - 可解释 testcase / keyword 为什么是 `taf_dependent`。
- 常见失败模式：
  - import closure 缺失导致 false excluded。
  - 同名 keyword 未标 `excluded` 而误解析。
  - TAF namespace call 被误标为普通 excluded。
  - dependency propagation 遇到 cycle 未停止。
- 评审问题：
  - 第一版 built-in / control keyword 列表需要随实现补充。
  - Layer 2 build summary 的质量阈值后续需要定义。
