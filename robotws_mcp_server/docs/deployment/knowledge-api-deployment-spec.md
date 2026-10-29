# RobotWS Knowledge API Deployment Spec

本文档定义集中式 `RobotWS Knowledge API` 的目标部署方案。

目标是让组内用户不再各自维护本地 `robotws` clone 和 SQLite index，而是统一访问服务器上的 RobotWS Knowledge API。

## 1. 目标架构

本项目选定 **方案 B：本地 MCP client 转发到远端 Knowledge API**。

明确不采用第一版方案：

- 不让 Cursor 直接连接远端 HTTP MCP server。
- Jenkins master 上部署的是普通 HTTPS Knowledge API，不要求实现 MCP streamable HTTP transport。
- Cursor 本地仍启动 stdio MCP server；这个本地 MCP 只负责把 tool request 转发到远端 API。

推荐部署方式：

- Docker Compose 管理常驻 API service。
- Jenkins scheduled job 定时触发 indexer container。
- Nginx 提供现有 HTTPS 入口和反向代理。
- `robotws` 源码和 SQLite index 持久化在 Jenkins master 的独立目录。
- 每个人本地 Cursor MCP 只作为 API client，通过 HTTPS 连接服务器查询。

```text
Cursor
  -> local RobotWS MCP client
  -> Nginx HTTPS reverse proxy
  -> RobotWS Knowledge API
  -> SQLite index
  -> server-side robotws clone
```

对标当前 TAF MCP 使用方式：

```text
TAF MCP:
Cursor -> local test-auto-doc MCP -> official TAF Knowledge API

RobotWS MCP:
Cursor -> local RobotWS MCP client -> Jenkins/Nginx RobotWS Knowledge API
```

服务器侧：

```text
Jenkins master Debian 13
  /opt/robotws-knowledge/
    docker-compose.yml
    .env
    data/
      robotws/
      indexes/
      logs/
```

## 2. 组件职责

### robotws-api

常驻 HTTP API service。

职责：

- 读取 `data/indexes/robotws.sqlite3`。
- 提供 query endpoints。
- 不直接修改 `robotws`。
- 不主动执行 git pull。
- 不主动重建 index。
- 只绑定服务器本机端口，由 Nginx 反向代理对外提供 HTTPS。

建议 endpoints：

```text
GET  /health
GET  /version
GET  /profiles
GET  /discovery/sg6
POST /query/generation-context
POST /query/search-cases
POST /query/search-keywords
POST /query/validate-style
```

### robotws-indexer

一次性 container，由 Jenkins job 定时触发。

职责：

- clone 或 update `robotws`。
- 构建 SQLite index。
- 生成 `sg6_discovery_report.json`。
- 成功后替换当前可用 index。

建议行为：

```text
if data/robotws/.git exists:
  git fetch
  git checkout configured branch
  git pull --ff-only
else:
  git clone configured repository

build index to temporary path
if build succeeds:
  replace active index atomically
```

### local RobotWS MCP client

每个用户本地 Cursor 使用的 MCP。

职责：

- 接收 Cursor MCP tool calls。
- 转发到 RobotWS Knowledge API。
- 返回 API 响应给 Cursor LLM。
- 本地不 clone `robotws`。
- 本地不 build SQLite index。
- 本地不访问 `8051` 端口，只访问 Nginx HTTPS URL。
- 本地通过 stdio 与 Cursor 通信，保持与当前 TAF MCP 类似的使用体验。
- 远端 API 对本地 MCP 来说只是普通 HTTPS REST API。

### Nginx reverse proxy

Jenkins master 上已有 Nginx HTTPS 入口时，RobotWS Knowledge API 不直接暴露给 Windows/Cursor。

职责：

- 统一 TLS/证书入口。
- 将 `/robotws-knowledge/` 转发到 `http://127.0.0.1:8051/`。
- 复用现有 443 端口，避免 Windows/Cursor 访问新端口失败。

推荐外部访问 URL：

```text
https://<jenkins-master-host>/robotws-knowledge/
```

## 3. 数据目录

推荐服务器目录：

```text
/opt/robotws-knowledge/
  docker-compose.yml
  .env
  data/
    robotws/
    indexes/
      robotws.sqlite3
      robotws.tmp.sqlite3
      sg6_discovery_report.json
    logs/
```

目录说明：

- `data/robotws/`: Git clone 的 `robotws` 源码。
- `data/indexes/robotws.sqlite3`: 当前 API 使用的 SQLite index。
- `data/indexes/robotws.tmp.sqlite3`: indexer 构建中的临时 index。
- `data/indexes/sg6_discovery_report.json`: SG6 allowlist ownership report。
- `data/logs/`: API 和 indexer 日志。

## 4. 配置项

建议 `.env`：

```dotenv
ROBOTWS_GIT_URL=https://wrgitlab.ext.net.nokia.com/RAN/robotws.git
ROBOTWS_BRANCH=master
ROBOTWS_ROOT=/data/robotws
ROBOTWS_DB_PATH=/data/indexes/robotws.sqlite3
ROBOTWS_TMP_DB_PATH=/data/indexes/robotws.tmp.sqlite3
ROBOTWS_DISCOVERY_REPORT=/data/indexes/sg6_discovery_report.json
ROBOTWS_PROFILE=Hangzhou_SG6_Common
ROBOTWS_API_HOST=0.0.0.0
ROBOTWS_API_PORT=8051
ROBOTWS_PUBLIC_BASE_URL=https://<jenkins-master-host>/robotws-knowledge
```

Git 认证建议：

- 优先使用只读 deploy token 或 project access token。
- 不把 token 写入 Git repository。
- Jenkins credential 中保存 token，再注入 Jenkins job。
- 如果使用 SSH key，使用只读 key，并限制权限。

## 5. Docker Compose 目标形态

目标 `docker-compose.yml`：

```yaml
services:
  robotws-api:
    image: robotws-knowledge-api:latest
    container_name: robotws-knowledge-api
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "127.0.0.1:8051:8051"
    volumes:
      - ./data:/data
    command:
      - robotws-knowledge-api
      - --db-path
      - /data/indexes/robotws.sqlite3
      - --host
      - 0.0.0.0
      - --port
      - "8051"

  robotws-indexer:
    image: robotws-knowledge-api:latest
    env_file:
      - .env
    volumes:
      - ./data:/data
    command:
      - python
      - -m
      - robotws_mcp.indexer
      - --robotws-root
      - /data/robotws
      - --profile
      - Hangzhou_SG6_Common
      - --db-path
      - /data/indexes/robotws.sqlite3
      - --discovery-report-path
      - /data/indexes/sg6_discovery_report.json
      - --write-index
```

说明：

- `robotws-api` 常驻运行。
- `robotws-indexer` 不常驻，由 Jenkins job 使用 `docker compose run --rm robotws-indexer` 触发。当前先使用已实现的 `python -m robotws_mcp.indexer`，后续可封装为 `robotws-knowledge-indexer` entrypoint。
- `robotws-indexer` 和 `robotws-api` 共享 `./data` volume。
- `robotws-api` 只暴露给宿主机本机 Nginx，不直接暴露给 Windows/Cursor。
- `robotws-api` 必须显式使用 `/data/indexes/robotws.sqlite3`，确保读取 mounted index。

## 6. Nginx HTTPS 反向代理

推荐在现有 HTTPS server block 中增加：

```nginx
location /robotws-knowledge/ {
    proxy_pass http://127.0.0.1:8051/;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto https;

    proxy_connect_timeout 30s;
    proxy_send_timeout 300s;
    proxy_read_timeout 300s;
}
```

注意：

- `location /robotws-knowledge/` 和 `proxy_pass http://127.0.0.1:8051/;` 末尾都带 `/`。
- 这样 `/robotws-knowledge/health` 会转发为后端 `/health`。
- Windows/Cursor 不需要访问 `10.71.210.104:8051`。
- 后端 API 可以继续监听 container 内 `0.0.0.0:8051`，但宿主机只绑定 `127.0.0.1:8051`。

## 7. Index 更新策略

推荐不要直接覆盖正在使用的 SQLite index。

安全流程：

```text
1. git pull robotws
2. build index -> robotws.tmp.sqlite3
3. build discovery report -> sg6_discovery_report.tmp.json
4. smoke check tmp index
5. atomically replace:
   robotws.tmp.sqlite3 -> robotws.sqlite3
   sg6_discovery_report.tmp.json -> sg6_discovery_report.json
```

这样 API 不会读到半成品 index。

## 8. Jenkins Job 策略

推荐 Jenkins job：

```text
robotws-knowledge-index-refresh
```

触发方式：

- 手动触发。
- 每天低峰定时触发。
- 需要时可以增加 webhook，但第一版不需要。

建议 cron：

```text
H 2 * * *
```

Jenkins job shell：

```bash
set -euo pipefail
cd /opt/robotws-knowledge
docker compose run --rm robotws-indexer
curl --fail http://127.0.0.1:8051/health
curl --fail https://<jenkins-master-host>/robotws-knowledge/health
```

## 9. 安全要求

- API container 只绑定宿主机 `127.0.0.1:8051`。
- 对 Windows/Cursor 只开放现有 Nginx HTTPS 入口。
- 不对公网暴露。
- Git token 不提交到 repository。
- Jenkins credentials 管理 Git token。
- API container 不需要写 `robotws`，只需要读 index。
- indexer container 需要写 `data/robotws` 和 `data/indexes`。
- 如果使用自签或内网证书，pilot 阶段本地 MCP 可配置临时跳过证书校验；长期应修正证书信任链。

## 10. 生成质量持续优化闭环

RobotWS MCP / Knowledge API 不会因为用户在 Cursor 中生成过一个 case 就自动训练模型。生成质量提升主要来自更好的索引数据、更准确的 style profile、更完整的 allowlist、更明确的失败经验和验证反馈。

推荐闭环：

```text
Cursor 生成 Robot case
  -> SG6 用户 review / 修改
  -> 在目标环境验证
  -> 高质量 case 合入 robotws
  -> Jenkins master git pull robotws
  -> 重建 SQLite index 和 discovery report
  -> Knowledge API 返回更好的 similar cases / keyword examples / guidance
  -> 下一次 Cursor 生成更贴近 SG6 风格和真实需求
```

需要沉淀的内容：

- 通过 review 的高质量 Robot case，应合入 `robotws`，成为后续 similar case pool 的一部分。
- 新增或变更 SG6 feature 后，应同步维护 `feature_allowlist`，否则不会进入 SG6 testcase 检索池。
- 发现 Cursor 常犯的错误，应补充到 profile 的 `negative_patterns` 或 `style_rules`。
- 常见 TL、UE、PA、KPI、setup/teardown 经验，应逐步进入 Robot case、resource keyword、profile guidance 或后续扩展知识库。
- 服务器定时 index refresh 是闭环生效的关键；只在本地临时修改、不合入 `robotws` 的 case 不会长期提升检索质量。

本闭环的边界：

- MCP 第一版仍是 `context_only`，不直接训练或微调 LLM。
- Cursor/LLM 负责根据上下文生成最终 case；Knowledge API 负责提供已验证知识、候选模式和约束。
- 如果未来接入 Insights Fusion / OpenAI-compatible provider，也应继续保留“review -> 验证 -> 合入 -> 重建 index”的知识闭环。

验证命令：

```bash
cd /opt/robotws-knowledge
docker compose run --rm robotws-indexer
curl --fail http://127.0.0.1:8051/health
curl --fail -X POST http://127.0.0.1:8051/query/generation-context \
  -H "Content-Type: application/json" \
  -d '{"requirement":"RRM SG6 handover KPI testcase","profile":"Hangzhou_RRM_SG6_Feature","limit":3}'
```

期望结果：

- 新合入 `robotws` 且属于 allowlist path 的 case 能在后续 `similar_cases` 中被检索到。
- 如果 case 不在 allowlist path 内，不应进入 SG6 testcase pool。

常见失败：

- 新 case 已合入但检索不到：检查 Jenkins index refresh 是否成功、API 是否读取最新 `/data/indexes/robotws.sqlite3`。
- 新 feature case 检索不到：检查 `feature_allowlist` 是否漏配。
- 生成结果仍重复旧错误：检查错误是否已沉淀到 `negative_patterns`、`style_rules` 或可检索的高质量参考 case。

学习记录：

- 解决的问题：明确 RobotWS MCP 的质量提升来自“高质量 case 和规则进入索引”的知识闭环，而不是 Cursor 自动训练。
- 影响文件：`robotws` 中已合入的 Robot cases、`config/profiles/*.json`、SQLite index、SG6 discovery report。
- 核心调用流：reviewed case -> merge to `robotws` -> server git pull -> rebuild index -> Knowledge API query -> Cursor generation。
- 关键字段：`feature_allowlist`、`similar_cases`、`keyword_examples`、`style_rules`、`negative_patterns`。
- 验证方式：重建 index 后查询 generation context，确认新 case 或新规则能影响返回上下文。

## 11. 当前项目需要新增的代码能力

当前本地 MVP 已具备：

- RobotWS parser。
- SQLite indexer。
- allowlist-only SG6 ownership。
- local query CLI。
- local MCP service。
- local RobotWS Knowledge API 最小版。

为了支持集中式部署，后续需要新增：

- API client mode MCP。
- Dockerfile。
- Docker Compose deployment files。
- Git clone/update source sync command。
- temporary index build and atomic replace。
- API root path / reverse proxy 支持验证。
- local MCP client 的 HTTPS API base URL 配置。
- 每个实现 step 必须同步添加 pytest 单元测试或集成测试，并同步更新验收命令。

本地 API 最小版验收：

```powershell
cd C:\TA\robotws_mcp_server
C:\Users\stlin\Python313\python -m pip install -e ".[dev]"
C:\Users\stlin\Python313\python -m pytest tests\test_api.py
C:\Users\stlin\Python313\python -m robotws_mcp.api --db-path data\indexes\robotws.sqlite3 --host 127.0.0.1 --port 8051
```

## 12. 验收标准

服务器本机验收：

```bash
curl http://127.0.0.1:8051/health
curl http://127.0.0.1:8051/version
```

Windows/Cursor 网络验收：

```powershell
curl.exe -k https://<jenkins-master-host>/robotws-knowledge/health
curl.exe -k https://<jenkins-master-host>/robotws-knowledge/version
```

期望：

- `/health` 返回 `ok`。
- `/version` 返回 API 名称、版本和当前 SQLite index path。后续 Docker/index metadata step 再补充 index build time、robotws branch、robotws commit。

查询验收：

```bash
curl -k -X POST https://<jenkins-master-host>/robotws-knowledge/query/generation-context \
  -H "Content-Type: application/json" \
  -d '{"requirement":"RRM SG6 handover KPI testcase","profile":"Hangzhou_RRM_SG6_Feature"}'
```

期望：

- 返回 `mode=context_only`。
- `similar_cases` 只来自 SG6 allowlist paths。
- 不返回 allowlist 外 feature testcase。

常见失败：

- API 启动失败：检查 container logs 和 env。
- Nginx 404：检查 `location /robotws-knowledge/` 和 `proxy_pass` 末尾 `/`。
- HTTPS 证书失败：pilot 用 `curl -k` 验证；长期修复证书信任。
- Git clone 失败：检查 GitLab token/SSH key。
- Index 为空：检查 `robotws` path 和 allowlist paths。
- 查询结果含 allowlist 外 case：检查 search path filter。
