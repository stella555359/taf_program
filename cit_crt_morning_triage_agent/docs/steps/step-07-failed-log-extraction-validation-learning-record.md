# Step 07 failed/not analyzed log 提取验证学习记录

## 日期

2026-05-22

## 本步骤解决的问题

Step 06 已经确认在 `10.57.159.149` / `tl813-agent` 上，Playwright 可以直接打开内部 Robot `log.html`：

```text
status = ok
response_status = 200
body_text_length > 0
```

但已验证样例 `CB010887_cases/log.html` 是 passed log：

```text
Total=1 / Pass=1 / Fail=0
failed_case_count=0
```

因此 Step 07 的目标从“能否打开 `log.html`”切换为：

```text
能否从实际 failed / not analyzed 的 log.html 中提取 failed case evidence
```

重点字段：

```text
case_message
failed_keyword
failure_text
keyword_chain
classification
```

## 修改的文件及原因

```text
docs/steps/step-07-failed-log-extraction-validation-learning-record.md
```

记录 Step 07 的验证目标、服务器命令、预期结果、常见失败模式和复盘问题，便于明天或重启后继续。

## 核心调用流程

```text
tl813-agent
-> health
-> collect-links --triage-only
-> choose failed / not analyzed log_url
-> extract-log-url
-> extract_failed_cases_from_text()
-> classify_failed_case()
-> inspect failed_cases output
```

## 关键字段

```text
session_status
scope
testline
robotcase
result
origin_result
log_url
body_text_length
failed_case_count
failed_cases[].evidence.case_message
failed_cases[].evidence.failed_keyword
failed_cases[].evidence.failure_text
failed_cases[].classification.category
```

## 服务器端验证命令

在 `10.57.159.149` / `tl813-agent` 上执行：

```bash
cd /opt/cit_crt_morning_triage_agent
source .venv/bin/activate
PYTHONPATH=agent python -m triage_agent health
```

预期结果：

```text
status = ok
Test Runs page loaded with a non-empty body
```

然后收集今天早上的待分析行：

```bash
PYTHONPATH=agent python -m triage_agent collect-links \
  --triage-only \
  --report-date 2026-05-22 \
  --max-rows 20
```

预期结果：

```text
session_status = ok
scopes[] 有输出
row_count 显示每个 scope 的 triage 行数量
rows[] 中包含 result / origin_result / log_url
```

从输出中选择一条实际 `failed / not analyzed` 的 `log_url`：

```bash
PYTHONPATH=agent python -m triage_agent extract-log-url \
  --url "<failed_or_not_analyzed_log_url>"
```

预期结果：

```text
status = ok
body_text_length > 0
failed_case_count > 0
failed_cases[].evidence.case_message 不为空
failed_cases[].evidence.failed_keyword 或 failure_text 至少一个不为空
failed_cases[].classification.category 有分类结果
```

如果默认 headless 出现浏览器差异，可临时使用：

```bash
PYTHONPATH=agent python -m triage_agent extract-log-url \
  --browser-channel chromium \
  --url "<failed_or_not_analyzed_log_url>"
```

或：

```bash
PYTHONPATH=agent python -m triage_agent extract-log-url \
  --headed \
  --browser-channel chrome \
  --url "<failed_or_not_analyzed_log_url>"
```

## 常见失败模式

```text
session_status = expired
```

Reporting Portal 登录态过期。需要用同一个 Playwright persistent profile 重新 headed 登录，然后再执行 `health`。

```text
row_count = 0
```

当前 report date / scope 下没有符合 `triage-only` 的行。可先去掉 `--triage-only` 或指定单个 scope 检查原始 rows：

```bash
PYTHONPATH=agent python -m triage_agent collect-links \
  --scope cit_7_5_UTE5G402T820 \
  --report-date 2026-05-22 \
  --max-rows 10
```

```text
status = ok but failed_case_count = 0
```

可能原因：

```text
1. 选到的是 passed log。
2. Robot log 文本结构与当前 log_extractor 规则不匹配。
3. failed 信息没有以 Status: FAIL / Message / KEYWORD / FAIL 这类文本出现。
```

此时把 `body_text_sample`、`failed_case_count`、`failed_cases` 输出贴回，用于增强 `log_extractor.py`。

```text
case_message 有值，但 failed_keyword / failure_text 为空
```

说明 case-level message 已能提取，但失败 step 定位规则还需要根据真实 Robot log 文本增强。

## 给用户的复盘问题

```text
1. collect-links 是否能在 2026-05-22 找到实际 failed / not analyzed 行？
2. 选中的 log_url 是否为真正 failed case，而不是 passed log？
3. extract-log-url 的 failed_case_count 是否大于 0？
4. failed_cases 中 case_message / failed_keyword / failure_text 哪些字段为空？
5. 当前分类结果是否接近人工 triage 判断？
```
