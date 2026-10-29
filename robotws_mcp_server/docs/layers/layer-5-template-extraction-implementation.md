# Layer 5 模板提取实现

## 目标

从已验证的 testcase 和 keyword 图模式中提取可复用的 workflow 骨架，避免让 LLM 强行复制特定 case 的包装逻辑。

规范设计：[`../architecture/7-layer-architecture-spec.md`](../architecture/7-layer-architecture-spec.md)，章节 `6. Layer 5: Template Extraction`。

## 草案范围

- 使用 Layer 1 记录和 Layer 2 图事实。
- 区分 TAF 依赖的可信复用与纯逻辑 helper 的重新生成。
- 为 domain workflow 构建候选骨架。
- 包含必需步骤、可选步骤、禁止顺序和参考 case。

## 最终决策

- Layer 5 第一版不做复杂 mining，先实现 deterministic template extraction service。
- 模板来源是 Layer 4 检索证据、Layer 2 keyword graph、Layer 3 boundary，以及少量明确 operation pattern。
- 第一批内置 operation pattern：
  - `l3_call`: attach -> start DL/UL traffic -> check throughput -> stop traffic -> detach -> teardown。
  - `generic_robot_case`: documentation/tags/setup/body/teardown 基础骨架。
- 模板不是最终答案，只输出：
  - required steps。
  - optional steps。
  - forbidden / missing cleanup warnings。
  - reference cases。
  - recommended keyword candidates per step。
- 对 `taf_dependent` keyword 优先推荐复用 existing SG6 wrapper；对 `pure_logic` step 可以建议 LLM 生成。

## 实现步骤

新增：

```text
src/robotws_mcp/layer5/__init__.py
src/robotws_mcp/layer5/models.py
src/robotws_mcp/layer5/templates.py
src/robotws_mcp/layer5/service.py
```

第一版工具：

```text
get_workflow_template(operation, profile, domain)
extract_template_from_requirement(requirement, profile)
recommend_template_steps(requirement, profile)
```

`l3_call` 模板必须覆盖：

```text
setup
attach
start_dl_traffic
start_ul_traffic
check_tput
stop_traffic
detach
teardown
```

## 验证交接

当前验证命令：

```powershell
py -m pytest tests/layer5 -q
py -m pytest -q
```

预期结果：

- L3 call requirement 能识别到 `l3_call` 模板。
- 模板包含 attach / traffic / tput / detach cleanup。
- recommended keywords 来自 allowed evidence。

## 学习记录

- 已解决的问题：
  - 避免 LLM 从零拼接长 testcase。
  - 把 MTK / L3 call 等需求先映射到明确 workflow。
- 变更文件：
  - `src/robotws_mcp/layer5/`
  - `tests/layer5/`
- 核心调用流：
  - requirement -> operation detection -> template -> Layer 4 evidence -> recommended steps。
- 关键字段：
  - `operation`
  - `required_steps`
  - `optional_steps`
  - `forbidden_order`
  - `reference_cases`
  - `recommended_keywords`
- 验证命令：
  - `py -m pytest tests/layer5 -q`
  - `py -m pytest -q`
- 预期结果：
  - L3 call 返回稳定 skeleton。
  - 每个步骤都有 role 和 rationale。
- 常见失败模式：
  - 误把 setup/teardown 从不同 domain 的 case 直接复制。
  - 只推荐 TAF direct API，忽略现有 SG6 wrapper。
- 评审问题：
  - 后续是否增加 handover / PA / KPI 专用模板。
