# Layer 4 语义检索实现

## 目标

结合 metadata filter、图事实以及后续的语义向量，检索相关 testcase、keyword、setup/teardown 和 workflow 上下文。

规范设计：[`../architecture/7-layer-architecture-spec.md`](../architecture/7-layer-architecture-spec.md)，章节 `5. Layer 4: Semantic Retrieval`。

## 草案范围

- 从 metadata 和 governance filter 开始。
- 将 Layer 2 图遍历结果作为检索信号。
- 仅在结构化事实稳定后加入语义检索。
- 将 vector search 作为补充手段，而不是唯一检索方法。

## 最终决策

- Layer 4 第一版实现 explainable hybrid retrieval，不依赖真实 embedding provider。
- 当前环境只有 Cursor Chat，没有 MCP server 可直接调用的 embedding API / 本地模型，所以 vector search 先预留接口，不作为运行时依赖。
- Retrieval 必须先经过 profile / domain / allowed boundary 过滤，再进行 ranking。
- Ranking 信号包括：
  - metadata / path / domain / feature match。
  - testcase / keyword lexical score。
  - Layer 2 `taf_dependency`、resolution 和 graph facts。
  - Layer 7 execution feedback hints。
- 每条结果必须返回 `match_reasons`，避免只给黑盒相似度。
- 默认返回 bounded summary，避免深度 graph expansion 卡住 Cursor。

## 实现步骤

新增：

```text
src/robotws_mcp/layer4/__init__.py
src/robotws_mcp/layer4/models.py
src/robotws_mcp/layer4/retriever.py
src/robotws_mcp/layer4/service.py
```

第一版工具：

```text
retrieve_generation_context(requirement, profile, limit)
search_evidence(query, profile, evidence_types, limit)
rank_keyword_candidates(query, profile, domain, feature, limit)
```

输出原则：

- `evidence_type`: `testcase | keyword`
- `score`: deterministic score。
- `match_reasons`: 可解释匹配原因。
- `feedback`: Layer 7 的 flaky / success rate / known failure hint。
- `taf_dependency`: Layer 2 的依赖摘要。

## 验证交接

当前验证命令：

```powershell
py -m pytest tests/layer4 -q
py -m pytest tests/test_api.py -q
py -m pytest -q
```

预期结果：

- 相同输入返回稳定排序。
- excluded / out-of-profile context 不进入结果。
- 每条 evidence 都包含 `match_reasons`。
- 没有 embedding provider 时不报错，返回 `vector_status=disabled`。

## 学习记录

- 已解决的问题：
  - 当前不强依赖 vector DB / embedding model。
  - 避免深度 graph expansion 导致查询卡住。
- 变更文件：
  - `src/robotws_mcp/layer4/`
  - `src/robotws_mcp/server.py`
  - `src/robotws_mcp/api.py`
  - `tests/layer4/`
- 核心调用流：
  - requirement + profile -> Layer 4 service -> Layer 1/legacy metadata + Layer 2 graph facts + Layer 3 boundary + Layer 7 feedback -> ranked evidence。
- 关键字段：
  - `query`
  - `profile`
  - `evidence_type`
  - `score`
  - `match_reasons`
  - `taf_dependency`
  - `feedback`
  - `vector_status`
- 验证命令：
  - `py -m pytest tests/layer4 -q`
  - `py -m pytest -q`
- 预期结果：
  - allowed evidence 可被检索。
  - out-of-profile / excluded evidence 被过滤。
  - 返回结果可解释且 bounded。
- 常见失败模式：
  - query 太宽导致结果噪声大。
  - 直接展开大 graph 导致慢查询。
  - 把 vector search 误认为已启用。
- 评审问题：
  - 后续 embedding provider 使用公司内网 API 还是本地模型。
