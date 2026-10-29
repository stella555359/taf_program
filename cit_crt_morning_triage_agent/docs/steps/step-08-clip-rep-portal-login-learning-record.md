# Step 08 CLIP Rep Portal 登录接入学习记录

## 日期

2026-06-04

## 本步骤解决的问题

旧方案依赖 Reporting Portal 的 SSO/MSAL session。该 session 过期后，页面可能停留在：

```text
Loading...
SSO LOG IN
No active accounts found. Trying to login silently...
```

用户最初在 Windows 普通浏览器中验证发现，打开 CLIP 登录页后选择 `Manual Login`，勾选 `Use Rep-portal` 并登录成功，再访问 Reporting Portal 可以直接进入。

后续 Windows InPrivate 验证显示，干净浏览器中完成同样 CLIP 登录后，Reporting Portal 仍会跳转到 Microsoft SSO。因此 CLIP 不能替代 Reporting Portal SSO。普通浏览器能直接进入，是因为该浏览器已经存在有效 Microsoft/Nokia SSO session。

更准确的模型是两层登录态：

```text
Microsoft/Nokia SSO active account
+
Rep Portal 自己的 token/session
```

CLIP `Use Rep-portal` 可能刷新第二层 Rep Portal token/session，但不能从零创建第一层 Microsoft SSO。

因此本步骤的结论调整为：

```text
CLIP Manual Login
-> cannot replace Reporting Portal Microsoft SSO
-> can refresh Rep Portal token/session if Microsoft SSO is already active
-> prefer Windows local headed Playwright for first MVP validation
```

## 修改的文件及原因

```text
config/triage_config.json
```

新增 `portal.clip_login_url`，默认指向 CLIP 登录页：

```text
https://10.182.68.169/login
```

```text
agent/triage_agent/models.py
agent/triage_agent/config.py
```

让 `PortalConfig` 支持读取 `clip_login_url`。

```text
agent/triage_agent/cli.py
```

新增 CLI：

```bash
PYTHONPATH=agent python -m triage_agent relogin-rep-portal
```

该命令使用同一个 `profile_dir` 打开 CLIP 登录页，等待用户手工完成登录，然后自动执行 Reporting Portal health check。当前验证结果显示，它不能在 tl813-agent 上刷新 Reporting Portal MSAL active account，但可以保留为 Rep Portal token refresh 辅助入口。

## 核心调用流程

```text
relogin-rep-portal
-> launch_persistent_context(profile_dir)
-> open portal.clip_login_url
-> user completes Manual Login with Use Rep-portal checked
-> close browser context so profile state is flushed
-> check_portal_session() opens Reporting Portal with same profile
-> output JSON status, expected to remain expired if no Microsoft SSO session exists
```

## 关键字段

```text
portal.clip_login_url
portal.profile_dir
status
health.status
health.reason
health.body_text_length
```

## 服务器端验证命令

在 `10.57.159.149` / `tl813-agent` 上执行：

```bash
cd /opt/cit_crt_morning_triage_agent
source .venv/bin/activate
NO_PROXY=10.182.68.169 no_proxy=10.182.68.169 \
PYTHONPATH=agent python -m triage_agent relogin-rep-portal
```

浏览器打开后：

```text
1. 选择 Manual Login。
2. 勾选 Use Rep-portal。
3. 输入 Nokia intranet username 和 password。
4. 点击 Sign In with Credentials。
5. 登录完成后回到终端按 Enter。
```

预期输出：

```text
"status": "ok"
"health": {
  "status": "ok",
  "reason": "Test Runs page loaded with a non-empty body."
}
```

随后执行：

```bash
PYTHONPATH=agent python -m triage_agent health
PYTHONPATH=agent python -m triage_agent collect-links --triage-only --max-rows 5
```

已验证结果（2026-06-04）：

```text
tl813-agent 上直接访问 https://10.182.68.169/login 会经过 Fortinet proxy 并失败：
curl -k -I https://10.182.68.169/login
-> HTTP/1.1 200 Connection established
-> Proxy-Agent: Fortinet-Proxy/1.0
-> SSL_ERROR_SYSCALL

加 NO_PROXY/no_proxy 绕过 proxy 后，relogin-rep-portal 可以打开 CLIP 登录页。
用户已完成 Manual Login + Use Rep-portal，并确认 CLIP 登录成功。
但同一 Playwright profile 再访问 Reporting Portal 仍跳转到 login.microsoftonline.com。
Windows InPrivate 中复现同样现象：CLIP 登录不能绕过 Reporting Portal SSO。
```

## 安全边界

- 默认不保存用户名、密码、token 或 cookie 到配置文件。
- 默认不支持命令行传入密码，避免进入 shell history。
- `profile_dir` 属于敏感浏览器会话状态，不能提交到 Git。
- 自动填表只能作为后续可选增强，并且应优先从交互式输入或受保护的 secret store 读取凭据。
- CLIP 登录和 Reporting Portal health check 必须使用同一个 `profile_dir`，否则 Rep Portal 登录态不会共享。

## 常见失败模式

```text
status = expired
```

当前结论：如果没有有效 Microsoft/Nokia SSO session，CLIP 登录后仍然会出现该结果。这不是用户操作失败，而是 CLIP 不能替代 Reporting Portal SSO。若 Microsoft/Nokia SSO 已经有效但 Rep Portal token 失效，再使用 CLIP `Use Rep-portal` 刷新第二层 token。

```text
status = unknown
```

页面打开了，但没有检测到 `Test Runs` 内容。检查是否登录到了其他页面，或 CLIP 是否没有写入 Rep Portal token。

```text
headed browser cannot open
```

当前 shell 没有图形界面。需要使用 X11 forwarding、VNC、服务器桌面会话，或后续实现安全的非交互式登录方式。

```text
Page.goto: net::ERR_CONNECTION_CLOSED at https://10.182.68.169/login
curl shows Proxy-Agent: Fortinet-Proxy/1.0
```

说明 tl813-agent 把 CLIP 内网 IP 的 HTTPS 请求送进了 proxy，proxy 会关闭 TLS 连接。使用：

```bash
NO_PROXY=10.182.68.169 no_proxy=10.182.68.169 \
PYTHONPATH=agent python -m triage_agent relogin-rep-portal
```

## 后续可选增强

在确认安全允许后，可以评估：

```text
relogin-rep-portal --auto
```

但自动化版本必须满足：

- 不在命令行明文传密码。
- 不把凭据写入仓库或普通配置文件。
- 明确记录凭据来源和过期处理。
- 登录失败时仍回退到手工模式。
