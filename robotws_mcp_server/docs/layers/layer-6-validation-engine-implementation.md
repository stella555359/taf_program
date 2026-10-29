# Layer 6 验证引擎实现

## 目标

在生成的 Robot Framework testcase 文本交给用户或测试执行之前，对其进行验证。

规范设计：[`../architecture/7-layer-architecture-spec.md`](../architecture/7-layer-architecture-spec.md)，章节 `7. Layer 6: Validation Engine`。

## 草案范围

- 复用 Robot Framework AST 解析来处理生成的 Robot 文本。
- 检查语法、必需 section、keyword 是否存在、resource import、arguments、variables、domain boundary 和 forbidden pattern。
- 生成结构化验证报告，供 Cursor 用于修正。

## 最终决策

- Layer 6 是 generated Robot static validation engine，不执行 testcase，不连接设备。
- 第一版重点修补 Layer 3 当前只做 style validation 的缺口：
  - Robot text 可解析。
  - required fields 是否存在。
  - keyword 是否能在 Layer 2 / known Robot built-ins / allowed TAF direct keywords 中解释。
  - setup / teardown / body keyword 是否跨 domain 边界。
  - SG1 / SG11 / excluded resource pattern 是否出现。
  - L3 call 类需求是否缺少 stop traffic / detach cleanup。
- 输出结构化 report，保留 `decision=allow|warn|deny` 方便 Layer 3 兼容。

## 实现步骤

新增：

```text
src/robotws_mcp/layer6/__init__.py
src/robotws_mcp/layer6/models.py
src/robotws_mcp/layer6/validator.py
src/robotws_mcp/layer6/service.py
```

第一版工具：

```text
validate_generated_robot(robot_text, profile, requirement)
explain_validation_issue(robot_text, profile)
```

报告结构：

```json
{
  "passed": true,
  "decision": "allow",
  "errors": [],
  "warnings": [],
  "suggestions": [],
  "checked_keywords": []
}
```

## 验证交接

当前验证命令：

```powershell
py -m pytest tests/layer6 -q
py -m pytest tests/layer3 -q
py -m pytest -q
```

预期结果：

- 缺 `[Documentation]`、`[Tags]`、`[Setup]`、`[Teardown]` 至少 warn。
- SG1 / SG11 pattern deny。
- unknown keyword warn 或 deny，取决于是否明显是 direct TAF allowed keyword。
- L3 call 草稿缺 stop traffic / detach 时 warn。

## 学习记录

- 已解决的问题：
  - Layer 3 style validation 不能发现跨 domain setup / teardown。
  - 生成草稿需要可解释 validation report。
- 变更文件：
  - `src/robotws_mcp/layer6/`
  - `src/robotws_mcp/layer3/service.py`
  - `tests/layer6/`
- 核心调用流：
  - robot_text + profile + requirement -> Layer 6 validator -> Layer 2 keyword evidence + profile rules + cleanup checks -> report。
- 关键字段：
  - `passed`
  - `decision`
  - `errors`
  - `warnings`
  - `suggestions`
  - `checked_keywords`
- 验证命令：
  - `py -m pytest tests/layer6 -q`
  - `py -m pytest -q`
- 预期结果：
  - 明显 forbidden pattern 被 deny。
  - 可解释 direct TAF keyword 不被误判为 unknown。
- 常见失败模式：
  - Robot parser 对片段文本过于宽松。
  - setup/teardown 是变量或动态 keyword，无法静态判断。
- 评审问题：
  - unknown keyword 在草稿阶段是否应 deny，还是先 warn。
