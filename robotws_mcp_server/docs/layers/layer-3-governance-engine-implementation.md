# Layer 3 治理引擎实现

## 目标

在上下文进入检索、生成之前，以及验证过程中，应用确定性的 profile、domain、resource、keyword 和 sequence 规则。

规范设计：[`../architecture/7-layer-architecture-spec.md`](../architecture/7-layer-architecture-spec.md)，章节 `4. Layer 3: Governance Engine`。

## 草案范围

- 消费 Layer 1 边界字段和 Layer 2 图事实。
- 过滤 `is_allowed=false` 的记录。
- 强制执行 domain 边界和 allowed resource 边界。
- 解释上下文为什么被允许或被过滤。
- 将策略决策保持在 scanner 之外。

## 最终决策

- Layer 3 是 deterministic governance layer，不发现事实，不重新 parse source，不重新构图。
- Layer 3 只把 Layer 1 / Layer 2 facts 放到当前 profile 下评估，并输出可解释的 `allow | deny | warn` 决策。
- 每个 deny / warn 必须包含 `rule_id`、`severity`、`reason` 和 `evidence`。
- `needs_user_confirmation` 不进入 MVP。
- `excluded` context 不进入 generation context，也不递归展开。
- Direct TAF usage 不默认禁止；只要有 SG6 RobotWS evidence 和权威 TAF MCP documentation 支撑，就可以 allow。

Direct TAF usage 原则：

```text
Direct TAF usage is allowed when grounded by SG6 RobotWS evidence and authoritative TAF MCP documentation. Existing SG6 wrappers are preferred, but new Robot Framework wrappers are allowed when they follow SG6-proven TAF library choice, parameter conventions, setup/teardown expectations, and cleanup patterns.
```

Layer 3 要判断：

- 这个 TAF 用法有没有 SG6 RobotWS 证据。
- 这个 API 有没有 TAF MCP 权威文档。
- 这个新 wrapper 是否沿用了 SG6 的底层库选择和参数模式。
- setup / teardown / cleanup 是否符合 SG6 日常模式。

## 实现步骤

### 步骤 1：模块骨架和决策模型

新增：

```text
src/robotws_mcp/layer3/__init__.py
src/robotws_mcp/layer3/models.py
src/robotws_mcp/layer3/governance.py
```

核心模型：

```text
GovernanceDecision
TafUsageEvidence
GovernanceEngine
```

决策结构：

```json
{
  "decision": "allow | deny | warn",
  "rule_id": "taf_usage.grounded_direct_or_new_wrapper",
  "severity": "info | warning | error",
  "reason": "string",
  "evidence": {}
}
```

### 步骤 2：Direct TAF Usage Rule

已有 SG6 wrapper 时：

```text
decision=allow
rule_id=taf_usage.existing_sg6_wrapper
```

没有完全现成 wrapper 时，如果同时满足以下条件，也允许生成新的 RF wrapper：

- 有 SG6 RobotWS evidence。
- 有 TAF MCP documentation。
- TAF library choice 符合 SG6 evidence。
- 参数模式符合 SG6 evidence。
- setup / teardown expectation 符合 SG6 evidence。
- cleanup pattern 符合 SG6 evidence。

拒绝场景：

- 使用 excluded evidence。
- 与 SG6 evidence 冲突。
- 缺少 SG6 evidence。
- 缺少 TAF MCP documentation。
- TAF MCP 有多个候选，但 SG6 evidence 不能判断该选哪个。
- library choice / parameter pattern / setup-teardown / cleanup 任一项无法对齐 SG6。

### 步骤 3：Context Filter

后续实现：

- Layer 1 `is_allowed=false` deny。
- Layer 2 `resolution_status=excluded` deny。
- `domain=Unknown` deny。
- profile 不匹配的 domain / feature deny。
- allowed `taf_dependent` keyword 可以进入 context，但必须带 evidence path。

### 步骤 4：Generated Robot Validator

后续实现：

- 引用 `excluded` keyword / resource 时 deny。
- 使用 forbidden SG/site resource 时 deny。
- 缺少 required profile fields 时按策略 warn 或 deny。
- 命中 negative patterns 时按 pattern severity 决策。
- TAF usage 必须通过 Direct TAF Usage Rule。

### 步骤 5：Query Tools

第一版已接入 MCP/API：

```text
filter_generation_context(candidate_ids, profile)
validate_generated_robot(robot_text, profile)
explain_allowed_boundary(record_id_or_path, profile)
evaluate_taf_usage(operation, evidence)
```

对应 HTTP API：

```text
POST /query/layer3/filter-generation-context
POST /query/layer3/validate-generated-robot
POST /query/layer3/explain-allowed-boundary
POST /query/layer3/evaluate-taf-usage
```

MVP 行为：

- `evaluate_taf_usage` 使用 Direct TAF Usage Rule 输出 `allow | deny`。
- `explain_allowed_boundary` 根据 profile + Layer 1/2 boundary facts 解释 path / record 是否可进入上下文。
- `filter_generation_context` 过滤候选 Layer 2 node，只允许 boundary safe 且 `is_allowed=true` 的候选进入 generation context。
- `validate_generated_robot` 先复用当前 style validator，后续再叠加 generated Robot governance rules。

## 本地 MCP Smoke Test 路线

短期先不部署服务器，先在本地把 RobotWS MCP server 接到 Cursor 做一次真实 SG6 smoke test。

### 步骤 1：准备索引

```powershell
py -m robotws_mcp.layer2.build_graph --layer1-db data/indexes/robotws_layer1_v2.sqlite3 --db-path data/indexes/robotws_layer2_graph.sqlite3 --profile Hangzhou_SG6_Common
```

如果 Layer 1 index 还在重新生成，以最新 `robotws_layer1_v2.sqlite3` 为准；Layer 2 graph 每次可重建。

### 步骤 2：本地启动 HTTP API

```powershell
py -m robotws_mcp.api --db-path data/indexes/robotws.sqlite3 --layer2-db-path data/indexes/robotws_layer2_graph.sqlite3 --host 127.0.0.1 --port 8051
```

基础检查：

```powershell
Invoke-RestMethod http://127.0.0.1:8051/health
Invoke-RestMethod http://127.0.0.1:8051/version
```

### 步骤 3：本地启动 MCP Server

```powershell
py -m robotws_mcp.server --db-path data/indexes/robotws.sqlite3 --layer2-db-path data/indexes/robotws_layer2_graph.sqlite3
```

Cursor MCP 本地配置使用同一条命令和参数。先保持 stdio 本地连接，不上远端服务器。

### 步骤 4：Cursor Smoke Test 问题

用真实 SG6 问题验证 tools 是否返回稳定证据：

```text
1. identify_robotws_profile: 询问一个 Hangzhou SG6 RRM / SISO 需求，看是否识别到正确 profile。
2. get_generation_context: 给一个 CB009363 / CB009275 类似需求，确认 similar cases 和 setup/teardown skeleton 只来自 SG6 allowed context。
3. get_keyword_graph / explain_taf_dependency: 查询 Connect to RU With Allocated IP、Connect to Common Unit Master、csn.execute 相关调用链。
4. evaluate_taf_usage: 给一个新 RF wrapper 的 TAF 调用证据，确认 SG6 evidence + TAF MCP docs 齐全时 allow，缺任一项时 deny。
5. filter_generation_context: 用 allowed SG6 keyword 和 excluded SG1/SG11 keyword 混合候选，确认 excluded 不进入 context。
```

Smoke test 通过后，再继续进入 Layer 4 semantic retrieval；如果工具返回太大、证据不足或决策原因不清楚，先调整 Layer 2/3 tool 输出。

## 验证交接

当前验证命令：

```powershell
py -m pytest tests/layer3 -q
py -m pytest tests/test_api.py -q
py -m pytest -q
```

预期结果：

- 有现成 SG6 wrapper 时，TAF usage allow。
- 没有现成 wrapper，但 SG6 evidence + TAF MCP docs + SG6 对齐项齐全时，allow。
- 缺 SG6 evidence / 缺 TAF MCP docs / 多候选无法由 SG6 证据选择 / 使用 excluded evidence / 与 SG6 冲突时，deny。

## 学习记录

- 已解决的问题：
  - Direct TAF usage 不默认禁止。
  - 新 RF wrapper 允许生成，但底层 TAF API 选择和参数模式必须有 SG6 evidence + TAF MCP docs 支撑。
- 变更文件：
  - `docs/architecture/7-layer-architecture-spec.md`
  - `docs/layers/layer-3-governance-engine-implementation.md`
  - `src/robotws_mcp/layer3/`
  - `src/robotws_mcp/server.py`
  - `src/robotws_mcp/api.py`
  - `tests/layer3/`
  - `tests/test_api.py`
- 核心调用流：
  - SG6 RobotWS evidence + TAF MCP docs + alignment checks -> `GovernanceEngine.evaluate_taf_usage()` -> `GovernanceDecision`
- 关键字段：
  - `decision`
  - `rule_id`
  - `severity`
  - `reason`
  - `evidence`
  - `sg6_evidence`
  - `taf_mcp_docs`
- 验证命令：
  - `py -m pytest tests/layer3 -q`
  - `py -m pytest tests/test_api.py -q`
  - `py -m pytest -q`
- 预期结果：
  - grounded direct TAF usage allow。
  - ungrounded or conflicting direct TAF usage deny。
- 常见失败模式：
  - 只有 TAF MCP docs，没有 SG6 evidence。
  - SG6 有相似场景，但参数模式未对齐。
  - 候选 API 多个，但 SG6 evidence 没有指明选择。
  - 使用 excluded feature/resource 作为依据。
- 评审问题：
  - required profile fields 在 Layer 3 中应该 warn 还是 deny，后续继续定。
