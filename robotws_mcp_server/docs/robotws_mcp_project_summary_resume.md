# RobotWS MCP Server 项目框架与实现总结

## 1. 项目定位

`robotws_mcp_server` 是一个面向 `robotws` 自动化测试仓库的只读知识服务项目。它的核心目标不是直接生成或执行测试用例，而是把 Robot Framework / Python 测试资产扫描成结构化知识索引，并通过 MCP Server、HTTP Knowledge API 和本地 CLI 向 Cursor / LLM 提供可解释、可追溯、符合团队风格的生成上下文。

项目可以概括为：

```text
RobotWS Test Knowledge Graph
  + Generation Context
  + Static Validation Engine
  + Execution Feedback Cache
```

它解决的主要问题是：`robotws` 中测试用例、resource、keyword、TAF 调用和团队风格分散在大量 `.robot`、`.resource`、`.py` 文件中，LLM 如果只做文本相似检索，容易引用错误测试线、跨域资源或不符合 SG6 风格的 keyword。本项目通过离线索引、边界治理、知识图谱、模板提取和静态校验，为后续 AI 辅助编写 Robot Framework 测试用例提供可信上下文。

## 2. 技术栈

- 语言与运行时：Python 3.10+
- Web 框架：FastAPI
- MCP 框架：`mcp>=1.0.0`，通过 `FastMCP` 暴露工具
- Robot 解析：Robot Framework 官方 AST parser
- Python 解析：Python AST 静态解析
- 存储：SQLite
- 配置：JSON profile
- 测试：pytest、FastAPI TestClient
- 主要入口：
  - MCP Server：`robotws-mcp`
  - Knowledge API：`robotws-knowledge-api`
  - 索引构建：`robotws-mcp-index`
  - Layer 1 扫描：`robotws-layer1-scan`
  - Layer 2 图构建：`robotws-layer2-build`
  - Layer 7 反馈导入：`robotws-layer7-import`
  - 本地查询：`robotws-mcp-query`

## 3. 整体架构

项目采用“旧版轻量索引能力 + 新版 7 层知识架构”并行演进的方式。

旧版主链路负责快速可用的索引、检索和生成上下文：

```text
robotws
  -> indexer scanner
  -> Robot / Python parser
  -> SQLite index
  -> ContextBuilder
  -> MCP / FastAPI / CLI
```

新版主链路面向长期的知识图谱和可信生成：

```text
Layer 1 Repository Scanner
  -> Layer 2 Keyword Knowledge Graph
  -> Layer 3 Governance Engine
  -> Layer 4 Semantic Retrieval
  -> Layer 5 Template Extraction
  -> Layer 6 Validation Engine
  -> Layer 7 Execution Feedback Cache
```

推荐数据流：

```text
robotws repository
  -> 只读扫描 Robot / Python 源码
  -> 生成结构化 metadata records
  -> 构建 testcase / keyword / step / TAF dependency 图谱
  -> 按 profile、domain、resource boundary 做治理过滤
  -> 检索相似 case、候选 keyword、模板步骤和执行反馈
  -> 输出 generation context 给 Cursor / LLM
  -> 对生成的 Robot testcase 做静态校验
```

## 4. 核心模块说明

### 4.1 Profile 与边界配置

项目通过 `config/profiles/` 维护团队风格与可用边界。当前主要围绕 Hangzhou SG6 场景组织，包括：

- `Hangzhou_SG6_Common`
- `Hangzhou_RRM_SG6_Feature`
- `Hangzhou_RRM_SG6_TMO`
- `Hangzhou_SISO_SG6_Feature`
- `Hangzhou_SISO_SG6_TMO`

Profile 中定义：

- 扫描范围 `path_scopes`
- 确认可生成的 case scope
- 允许复用的 resource scope
- RRM / SISO feature allowlist
- hard exclude patterns
- preferred keywords
- negative patterns
- required fields
- style rules

这部分是项目的治理基础。它确保生成上下文只来自允许的 SG6 测试资产，避免把 SG1、SG11 或其他不相关测试线的 resource 推荐给 SG6 用例生成。

### 4.2 索引构建与旧版 SQLite Index

旧版索引入口位于 `src/robotws_mcp/indexer/`。

`RobotWsIndexer` 的核心流程：

1. 根据 profile 的 `path_scopes` 遍历外部 `robotws` 仓库。
2. 扫描 `.robot`、`.resource` 和 `.py` 文件。
3. 使用 Robot parser 提取 Robot 文件、用例、keyword、resource import、library import、step 和调用关系。
4. 使用 Python parser 提取 class、function、method、signature、docstring 和 imports。
5. 通过 `FeatureOwnershipDiscoverer` 生成 SG6 discovery report。
6. 在 `--write-index` 时写入 SQLite，默认路径为 `data/indexes/robotws.sqlite3`。

旧版 SQLite 主要表包括：

- `robot_files`
- `robot_cases`
- `robot_keywords`
- `library_imports`
- `resource_imports`
- `call_edges`
- `python_symbols`

这条链路支撑早期的：

- `search_robot_cases`
- `search_robot_keywords`
- `get_case_pattern`
- `trace_keyword_usage`
- `find_taf_library_usage`
- `get_generation_context`
- `validate_generated_case_style`

### 4.3 Layer 1：Repository Scanner

Layer 1 是新版架构中的只读事实采集层。它不做语义推断，也不执行任何 Robot / Python 代码，只负责把源文件转换成结构化 record。

主要实现点：

- 使用 Robot Framework 官方 AST parser 解析 `.robot` / `.resource`。
- 使用 Python AST 做静态符号索引，不 runtime import，不连接设备。
- 提取 `RobotFileRecord`、`TestCaseRecord`、`KeywordRecord`、`StepRecord`、`ResourceImportRecord`、`LibraryImportRecord`、`VariableRecord`、`PythonSymbolRecord`、`ParseIssueRecord`。
- 将 `Run Keywords`、`AND`、`Run Keyword If` 等控制包装器拆成直接逻辑动作。
- 标记 `record_type`、`domain`、`is_allowed`、`allowed_source`、`exclude_reason`。
- 标记 `python_impl_type` 和 `robot_impl_type`，区分 `taf_dependent`、`pure_logic`、`unknown` 等类型。

Layer 1 的边界是事实采集，不负责递归展开调用树，也不负责最终 prompt 组装。

### 4.4 Layer 2：Keyword Knowledge Graph

Layer 2 基于 Layer 1 的 records 构建确定性 keyword dependency graph。

主要实现点：

- 读取 Layer 1 SQLite 中的 allowed records。
- 构建 testcase、keyword、step、resource_file、python_symbol、domain、feature 等图节点。
- 建立 `HAS_STEP`、`DEFINED_IN`、`IMPORTS_RESOURCE`、`IMPORTS_LIBRARY`、`BELONGS_TO_DOMAIN`、`BELONGS_TO_FEATURE` 等确定性边。
- 解析 `StepRecord.keyword`，形成 `CALLS` 边。
- 对无法解析到本地 keyword 但符合 TAF / device 操作模式的调用，生成 synthetic `taf_library_keyword` 节点。
- 沿调用图传播 TAF dependency，形成 dependency summary。
- 使用独立 SQLite 图索引，默认路径类似 `data/indexes/robotws_layer2_graph.sqlite3`。

Layer 2 的价值在于把“文本相似”升级为“可解释调用关系”，让系统能回答某个 case 调用了哪些 keyword、某个 keyword 被谁引用、某个 step 是否可解析、某条链路是否依赖 TAF。

### 4.5 Layer 3：Governance Engine

Layer 3 是确定性治理层，负责在上下文进入检索和生成前执行 profile、domain、resource、keyword 和 TAF 使用规则。

主要能力：

- `evaluate_taf_usage`
- `explain_allowed_boundary`
- `filter_generation_context`
- `validate_generated_robot`

治理决策统一输出：

```json
{
  "decision": "allow | deny | warn",
  "rule_id": "string",
  "severity": "info | warning | error",
  "reason": "string",
  "evidence": {}
}
```

这里的关键设计是：Direct TAF usage 不默认禁止，但必须同时有 SG6 RobotWS evidence 和权威 TAF 文档证据，且 library choice、参数模式、setup / teardown、cleanup pattern 与 SG6 现有实践对齐。

### 4.6 Layer 4：Semantic Retrieval

Layer 4 当前实现的是 explainable hybrid retrieval，而不是依赖真实 embedding provider 的向量检索。

主要特点：

- `vector_status` 明确返回 `disabled:no_embedding_provider`。
- 结合旧版 `ContextBuilder`、Layer 2 graph facts、Layer 3 boundary 和 Layer 7 feedback hints。
- 为 requirement 检索相似 testcase、候选 keyword 和可解释 evidence。
- 输出 evidence score、profile、TAF dependency、feedback hint 等可解释信息。

这样做的好处是：即使没有接入向量数据库或 LLM provider，系统也能提供可审计、可复现的候选上下文。

### 4.7 Layer 5：Template Extraction

Layer 5 负责从检索证据中提取可复用工作流模板。

当前实现是 deterministic template extraction service：

- 根据 requirement 判断 operation，例如 `l3_call` 或 `generic_robot_case`。
- 使用内置模板步骤作为骨架。
- 结合 Layer 4 检索结果，为每个模板步骤推荐 keyword。
- 输出 required steps、forbidden order、reference cases 和 warnings。

这层不是直接生成最终 Robot 文本，而是向 LLM 提供“应该按什么顺序写、哪些 keyword 值得参考、哪些顺序是禁止的”。

### 4.8 Layer 6：Validation Engine

Layer 6 是生成后静态验证层，不执行 testcase，不连接测试线或设备。

主要目标：

- 检查生成 Robot 文本是否符合 profile 必填字段。
- 检查是否引用 forbidden resource、excluded keyword 或跨 domain setup / teardown。
- 检查 keyword 是否能在 Layer 2、Robot built-ins 或 allowed TAF direct keywords 中解释。
- 输出结构化 report，包括 decision、errors、warnings、suggestions。

这层用于降低 LLM 生成 Robot testcase 时的风险，把“生成后人工肉眼检查”提前变成自动静态校验。

### 4.9 Layer 7：Execution Feedback Cache

Layer 7 用于把真实执行结果变成后续检索和验证的反馈信号。

主要能力：

- 手工记录 execution feedback。
- 导入 Robot `output.xml`。
- 导入 Jenkins result JSON。
- 查询 feedback。
- 根据 record / keyword / case 名称获取 feedback hints。

反馈中会记录：

- source type / source path
- test name / keyword name
- status
- failure class
- message
- elapsed time
- profile
- testline
- metadata

这些信息可以反向提供给 Layer 4 ranking 和 Layer 6 validation，例如降低 flaky keyword 的推荐优先级，或在生成上下文中提示已知失败模式。

## 5. 对外接口

### 5.1 MCP Tools

`src/robotws_mcp/server.py` 中通过 `RobotWsMcpService` 统一封装业务能力，再通过 `FastMCP` 暴露工具。

代表性工具包括：

- `identify_robotws_profile`
- `discover_sg6_features`
- `get_sg6_discovery_report`
- `search_robot_cases`
- `search_robot_keywords`
- `get_case_pattern`
- `trace_keyword_usage`
- `find_taf_library_usage`
- `get_style_profile`
- `get_generation_context`
- `validate_generated_case_style`
- `get_testcase_graph`
- `get_keyword_graph`
- `resolve_keyword_call`
- `explain_taf_dependency`
- `evaluate_taf_usage`
- `explain_allowed_boundary`
- `retrieve_generation_context`
- `get_workflow_template`
- `validate_generated_robot_static`
- `record_execution_feedback`
- `import_robot_output_xml`
- `get_feedback_hints`

设计上，MCP tools 按 LLM 的查询和决策动作拆分，而不是按内部 helper 函数拆分，便于 Cursor 在生成用例前按需查询证据。

### 5.2 HTTP Knowledge API

`src/robotws_mcp/api.py` 提供 FastAPI 版本的查询服务，适合集中部署或本地 smoke test。

代表性接口：

- `GET /health`
- `GET /version`
- `GET /profiles`
- `GET /discovery/sg6`
- `POST /query/generation-context`
- `POST /query/search-cases`
- `POST /query/search-keywords`
- `POST /query/validate-style`
- `POST /query/layer2/testcase-graph`
- `POST /query/layer2/keyword-graph`
- `POST /query/layer3/evaluate-taf-usage`
- `POST /query/layer4/retrieve-generation-context`
- `POST /query/layer5/template`
- `POST /query/layer6/validate-generated-robot`
- `POST /query/layer7/import-robot-output`
- `POST /query/layer7/feedback-hints`

API 使用 Pydantic model 限定请求字段和 limit 范围，避免一次查询返回过大结果。

### 5.3 CLI

`src/robotws_mcp/query.py` 提供本地查询 CLI，方便不经过 Cursor 或 HTTP 服务直接调试索引。

常见命令：

```powershell
python -m robotws_mcp.query get-generation-context --requirement "create SG6 TMO DL SFTP KPI testcase" --profile Hangzhou_RRM_SG6_TMO
python -m robotws_mcp.query search-cases --query "handover KPI" --profile Hangzhou_RRM_SG6_Feature
python -m robotws_mcp.query layer4-retrieve --requirement "RRM SG6 handover KPI testcase"
python -m robotws_mcp.query layer6-validate --robot-text "<robot text>" --profile Hangzhou_SG6_Common
```

## 6. 关键实现亮点

### 6.1 只读索引，隔离外部 robotws 仓库

项目明确要求只读取外部 `robotws`，索引写入本项目的 `data/indexes/`，不修改 `robotws` 源仓库。这降低了工具试验对生产测试资产的影响。

### 6.2 使用 AST 而不是简单文本匹配

Robot 文件使用官方 AST parser，Python 文件使用 AST 静态解析。相比基于正则的文本切分，AST 方案更容易保留 source location、setup / teardown、keyword、arguments、library import 和 resource import 等结构化信息。

### 6.3 Profile 驱动的团队风格和边界治理

系统把 SG6 的 feature allowlist、allowed resource scope、negative pattern 和 preferred keyword 写入 profile。检索和生成不是从全量 robotws 中盲目找相似文本，而是在明确边界内选择证据。

### 6.4 知识图谱补足调用关系

Layer 2 把 testcase、keyword、step、resource、library、Python symbol 和 TAF dependency 建成图，支撑调用追踪、依赖解释和 unresolved call 排查。

### 6.5 不依赖 LLM 的可解释检索

MVP 不直接调用 LLM，也不强依赖 embedding provider。Layer 4 通过 hybrid retrieval 和可解释 evidence 输出，让结果在没有向量服务的情况下也能工作。

### 6.6 静态验证降低生成风险

Layer 6 在生成 Robot 文本后做静态校验，提前发现缺字段、跨边界 resource、无法解释 keyword、cleanup 不足等问题。

### 6.7 执行反馈形成闭环

Layer 7 把 Robot / Jenkins 执行结果转成 feedback cache，后续可影响检索排序和验证提示，让系统从“只看历史源码”逐步演进到“结合真实执行质量”的知识服务。

## 7. 测试与工程化

项目测试覆盖了主要层次：

- API 健康检查、版本信息、profile 查询。
- generation context 构建。
- case / keyword 搜索。
- style validation。
- Layer 2 graph 查询。
- Layer 3 governance 决策。
- Layer 4 retrieval。
- Layer 5 template extraction。
- Layer 6 generated Robot validation。
- Layer 7 feedback import / query。

测试中大量使用临时 SQLite index 和 FastAPI `TestClient`，避免依赖真实 `robotws` 或真实测试环境，符合项目“只读、可本地验证、可快速回归”的定位。

## 8. 当前项目价值

从业务角度看，本项目把部门已有的 Robot Framework 测试资产转化为可检索、可治理、可验证的知识底座，为 AI 辅助编写测试用例提供上下文。

从架构角度看，它把传统“文件级搜索”拆成：

- 源码事实采集
- 结构化索引
- 关键字依赖图谱
- 生成边界治理
- 可解释检索
- 测试模板抽取
- 生成后静态校验
- 执行反馈闭环

从工程角度看，它支持 MCP、HTTP API 和 CLI 三种访问方式，便于 Cursor、自动化脚本、服务器部署和本地调试复用同一套核心服务。

## 9. 可放入简历的项目经验描述

### 项目名称

RobotWS MCP Knowledge Server：面向 Robot Framework 自动化测试资产的知识图谱与 AI 生成上下文服务

### 简历版描述

负责设计并实现一个面向 5G Robot Framework 自动化测试仓库的只读 MCP / Knowledge API 服务，将分散在 `robotws` 中的 `.robot`、`.resource` 和 Python helper 静态解析为结构化 SQLite 索引，并基于团队 profile 构建 SG6 测试资产边界、keyword 调用图谱、TAF 依赖解释、生成模板和静态校验能力。项目通过 MCP Server、FastAPI 和 CLI 三种入口向 Cursor / LLM 提供可追溯的相似用例、候选关键字、setup / teardown 模式和生成校验报告，避免 AI 生成用例时跨测试线引用错误资源或使用不符合团队风格的 keyword。

### 工作内容

- 搭建 Python + FastAPI + MCP 的知识服务框架，封装统一 `RobotWsMcpService`，同时支持 Cursor MCP tools、HTTP API 和本地 CLI 查询。
- 实现 Robot Framework / Python 源码只读扫描链路，基于 Robot 官方 AST parser 和 Python AST 提取 testcase、keyword、step、resource import、library import、Python symbol 等结构化元数据，并持久化到 SQLite。
- 设计 SG6 profile 配置体系，沉淀 RRM / SISO feature allowlist、allowed resource scope、preferred keyword、negative pattern 和 required fields，实现生成上下文的边界治理。
- 参与实现 7 层知识架构，包括 Repository Scanner、Keyword Knowledge Graph、Governance Engine、Hybrid Retrieval、Template Extraction、Validation Engine 和 Execution Feedback Cache。
- 构建 keyword 调用图谱和 TAF dependency 解释能力，支持 testcase graph、keyword graph、keyword caller、unresolved call 和 allowed boundary 查询。
- 实现生成后静态校验与执行反馈缓存，支持导入 Robot output.xml / Jenkins result JSON，并将真实执行结果作为后续检索和校验提示。
- 编写 pytest / FastAPI TestClient 自动化测试，覆盖 API、检索、治理、模板、校验和反馈导入等核心链路。

### 技术关键词

Python、FastAPI、MCP、Robot Framework AST、Python AST、SQLite、Knowledge Graph、Static Analysis、Prompt Context、pytest、Cursor AI

### 简历压缩版

设计并实现 `RobotWS MCP Knowledge Server`，面向 5G Robot Framework 自动化测试仓库提供只读知识索引和 AI 生成上下文服务。基于 Robot Framework AST / Python AST 扫描 `.robot`、`.resource`、Python helper，构建 SQLite 元数据索引、SG6 profile 边界治理、keyword 调用图谱、TAF 依赖解释、模板抽取和生成后静态校验能力；通过 MCP Server、FastAPI 和 CLI 向 Cursor / LLM 提供可追溯的相似用例、候选 keyword、setup / teardown 模式和 validation report，提升 AI 辅助编写测试用例的准确性和可控性。
