# Step 09 Windows 本机运行学习记录

## 日期

2026-06-04

## 本步骤解决的问题

tl813-agent 上无法稳定获得 Reporting Portal 的 Microsoft/Nokia SSO session。CLIP Manual Login + `Use Rep-portal` 已验证不能替代 Reporting Portal SSO，但它可能在已有 Microsoft/Nokia SSO 的前提下刷新 Rep Portal 自己的 token/session。

Windows 普通浏览器能进入 Reporting Portal，是因为本机已有有效 SSO session。因此第一版 Agent 的主链路验证调整为 Windows 本机运行：

```text
Windows headed Playwright
-> Microsoft/Nokia SSO in local browser profile
-> optional CLIP Use Rep-portal if Rep Portal token/session is stale
-> Reporting Portal filtered page
-> Test Logs / log.html
-> failed evidence extraction
```

## 修改的文件及原因

```text
config/triage_config.windows.json
```

新增 Windows 专用配置，保留与服务器配置相同的 testline scope 和时间窗口规则，但使用 Windows 本地 browser profile：

```text
C:/TA/cit_crt_morning_triage_agent/browser-profile/reporting-portal
```

该目录属于敏感浏览器状态，已被 `.gitignore` 的 `browser-profile/` 规则排除。

## 核心调用流程

```text
health --config config/triage_config.windows.json --headed --browser-channel chrome
-> if SSO page appears, user completes Microsoft/Nokia login in Playwright browser
-> rerun health
-> if SSO is active but health still fails, run CLIP Use Rep-portal in same profile
-> collect-links --triage-only
-> choose failed/not analyzed log_url
-> extract-log-url
```

## Windows 本机验证命令

在 PowerShell 中执行：

```powershell
cd C:\TA\cit_crt_morning_triage_agent
$env:PYTHONPATH="agent"
C:\Users\stlin\Python313\python -m triage_agent --config config\triage_config.windows.json health --headed --browser-channel chrome
```

这里优先使用本机已安装的 Chrome，避免下载 Playwright 管理的 Chromium。如果要改用 Edge，可将 `chrome` 替换为 `msedge`。

如果弹出 Microsoft/Nokia SSO 页面，在 Playwright 打开的浏览器窗口里完成登录。登录成功后重新执行：

```powershell
C:\Users\stlin\Python313\python -m triage_agent --config config\triage_config.windows.json health --browser-channel chrome
```

预期结果：

```text
"status": "ok"
"reason": "Test Runs page loaded with a non-empty body."
```

已验证结果（2026-06-04）：

```text
Windows 本机使用 --browser-channel chrome 成功。
health --headed --browser-channel chrome: status=ok, body_text_length=22127
health --browser-channel chrome: status=ok, body_text_length=22127
console 显示 Token exchange success。
```

如果确认 Microsoft/Nokia SSO 已经有效，但 Rep Portal health 仍失败，可用同一个 Windows profile 执行 CLIP token refresh：

```powershell
C:\Users\stlin\Python313\python -m triage_agent --config config\triage_config.windows.json relogin-rep-portal --browser-channel chrome --health-browser-channel chrome
```

在打开的 CLIP 页面中选择 `Manual Login`、勾选 `Use Rep-portal` 并完成登录。完成后回到终端按 Enter，再重新执行 `health`。

收集待分析行：

```powershell
C:\Users\stlin\Python313\python -m triage_agent --config config\triage_config.windows.json collect-links --triage-only --max-rows 5 --browser-channel chrome
```

已验证结果（2026-06-04）：

```text
session_status: ok
cit_7_5_UTE5G402T273: raw_row_count=37, row_count=2
crt_7_5_UTE5G402T273: raw_row_count=33, row_count=0
cit_7_5_UTE5G402T272: raw_row_count=37, row_count=4
crt_7_5_UTE5G402T272: raw_row_count=37, row_count=0
cit_7_5_UTE5G402T820: raw_row_count=35, row_count=0
crt_7_5_UTE5G402T820: raw_row_count=34, row_count=0
```

如需指定日期：

```powershell
C:\Users\stlin\Python313\python -m triage_agent --config config\triage_config.windows.json collect-links --triage-only --report-date 2026-06-04 --max-rows 5 --browser-channel chrome
```

从输出中选择一条实际 failed / not analyzed 的 `log_url`：

```powershell
C:\Users\stlin\Python313\python -m triage_agent --config config\triage_config.windows.json extract-log-url --url "<log_url>" --browser-channel chrome
```

预期结果：

```text
"status": "ok"
"body_text_length": 大于 0
"failed_case_count": 大于 0
```

已验证结果（2026-06-04）：

```text
log_url: CB009363_E_cases/log.html
status: ok
response_status: 200
body_text_length: 42600
failed_case_count: 1
full_name: CB009363 E cases.[1]CB009363-SR-F_007_4_UEs_Rank_1_with_non-GBR_high_load_are_paired_with_LOS_and_NLOS_channel
case_message: AVG is 0Mbps, lower than900.0Mbps
```

分类规则修正：

```text
吞吐/KPI 类失败如 "AVG is 0Mbps, lower than..." 应优先匹配 product_bug_candidate。
不要让 raw excerpt 中泛化的 timeout 抢先归到 environment_issue。
```

## 常见失败模式

```text
BrowserType.launch: Executable doesn't exist
```

优先使用系统 Chrome 或 Edge，不需要下载 Playwright Chromium：

```powershell
C:\Users\stlin\Python313\python -m triage_agent --config config\triage_config.windows.json health --headed --browser-channel chrome
```

如果确实要使用 Playwright 管理的 Chromium，再执行：

```powershell
C:\Users\stlin\Python313\python -m playwright install chromium
```

```text
status = expired
```

说明 Windows Playwright profile 还没有有效 Reporting Portal SSO。使用 `health --headed --browser-channel chrome` 完成人工登录后再重试。

```text
collect-links row_count = 0
```

可能是当天时间窗口没有 not analyzed 行。可去掉 `--triage-only` 或指定单个 scope 检查原始 rows：

```powershell
C:\Users\stlin\Python313\python -m triage_agent --config config\triage_config.windows.json collect-links --scope cit_7_5_UTE5G402T820 --max-rows 10 --browser-channel chrome
```

```text
extract-log-url status = navigation_failed
```

优先确认 Windows 浏览器能否直接打开同一个 `log_url`。如果能打开，再贴回 `navigation_errors` 和 `body_text_sample` 用于增强 Playwright 访问参数。

## 安全边界

- 不提交 `browser-profile/`。
- 不保存用户名、密码、token 或 cookie 到配置文件。
- Windows 本机模式用于先跑通 triage 主链路；后续是否回到服务器定时运行，需要另行解决 SSO session 问题。
