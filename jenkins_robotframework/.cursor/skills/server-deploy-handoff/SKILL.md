---
name: server-deploy-handoff
description: Guides safe Debian deployment, release activation, service restart, smoke verification, and deployment troubleshooting for jenkins_robotframework. Use when the user mentions deployment, release, server git pull, making platform-api or Portal changes take effect, systemd, Nginx, Jenkins JCasC or Job DSL activation, AI worker restart, /api/health 502, Portal availability, or Jenkins callback/runtime deployment issues.
---

# Server Deploy Handoff

## Purpose

Convert a known code or configuration change into the smallest safe server-side release procedure.

This skill is a decision and handoff layer. It does not replace executable deployment scripts and does not directly operate the target server.

## Sources Of Truth

Read these project-relative files in order:

1. `deploy/RELEASE_CHECKLIST.md`
   - canonical daily release decision matrix
2. `deploy/SERVER_OPERATIONS.md`
   - individual status, log, restart, build, and troubleshooting commands
3. `deploy/DEPLOYMENT.md`
   - only for greenfield setup, missing infrastructure, or low-frequency configuration details

For Jenkins architecture boundaries, read:

- `docs/modules/jenkins-integration/README.md`
- `docs/modules/jenkins-integration/index.md`

Do not use `issue/` as the primary release source.

## Trigger

Apply this skill when the user asks about:

- deploying or releasing this project
- pulling code on the Debian server
- making local or Git changes take effect
- restarting `platform-api`, `platform-api-ai-worker`, Jenkins, or Nginx
- rebuilding or publishing `automation-portal`
- applying Jenkins pipeline, helper script, Job DSL, or JCasC changes
- applying Nginx, systemd, or server env changes
- troubleshooting Portal unavailable, `/api/health` 502, AI analysis stuck, or Jenkins deployment/callback symptoms

Do not auto-apply this skill when:

- a short prompt such as `continue` or `下一步` asks to resume the project mainline
- the task is feature implementation with no deployment or server handoff
- the user asks only for local unit-test commands

## Required Inputs

Infer inputs from the request and repository when possible:

- changed paths or affected components
- routine update, first deployment, or troubleshooting
- target branch
- whether dependencies, `VITE_*`, systemd units, or server env contracts changed
- whether Jenkins uses SCM Pipeline, Seed Job, JCasC, or manual Job management

Ask one focused question only when a missing value changes the operation materially, especially:

- target branch is unknown and branch switching would be required
- first deployment versus routine update is unclear
- Job DSL/JCasC management mode is unclear
- a destructive or credential-related operation would otherwise be implied

Never ask the user to paste tokens, passwords, private keys, or complete secret-bearing env files.

## Change Classification

Map every changed path to the matching Checklist section:

| Path or component | Release category |
|---|---|
| `platform-api/app/services/ai_analysis_worker.py` or modules used only by that worker | AI worker only |
| AI repository/schema/service/config imported by both API and worker | Platform API and AI worker |
| other `platform-api/app/**` | Platform API |
| `platform-api/requirements.txt` or dependency files | API dependency update |
| `automation-portal/src/**`, `public/**`, Vite config | Portal build |
| `automation-portal/package*.json` | Portal dependency install and build |
| server `automation-portal/.env` `VITE_*` | Portal rebuild |
| `jenkins-integration/pipelines/**`, `scripts/**` | SCM Pipeline activation |
| `jenkins-integration/jobs/**` | Seed Job / Job DSL activation |
| `jenkins-integration/jcasc/**` | JCasC render and reload |
| `deploy/nginx/**` | Nginx sync, syntax check, reload |
| `deploy/systemd/**` | unit sync, daemon reload, service restart |
| `deploy/env/*.example` | manual field merge; never overwrite real env |
| only `docs/**` or `.cursor/**` | normally no server runtime action |

When multiple rows match, combine the rows but deduplicate:

- repository precheck and pull
- service status checks
- Nginx syntax/reload
- final smoke commands

Do not restart unrelated services.

## Workflow

### 1. Establish Scope

State:

- target server role
- target branch if known
- changed components
- whether the procedure is routine update, bootstrap, or troubleshooting

If the request is routine release, use `RELEASE_CHECKLIST.md`.

If the repository or required service does not yet exist on the server, switch to the relevant `DEPLOYMENT.md` section and clearly label it as first deployment.

### 2. Generate Safe Precheck

Always start routine updates with commands that show:

- server working tree status
- active branch
- current commit

If output shows an unexpected dirty tree, instruct the user to stop and paste the result. Never propose automatic cleanup, hard reset, file deletion, or force checkout.

Use `git pull --ff-only`. Do not generate branch-switch commands unless the target branch is confirmed.

### 3. Select Minimal Activation Steps

Use only the matching sections from `deploy/RELEASE_CHECKLIST.md`.

Important rules:

- API source change: restart API; install dependencies only if dependency files changed.
- Worker-only change: restart worker; restart API only when shared API code/config also changed.
- Portal source or `VITE_*` change: rebuild Portal; `VITE_*` is build-time configuration.
- Jenkinsfile/helper change: normally no Jenkins restart; verify SCM branch and run a minimal build.
- Job DSL change: confirm the commit is pushed, the Seed Job `REPOSITORY_REF` contains it, and the `t813 && robot` Agent is online before running Seed Job. Master `/opt` pull does not apply DSL.
- JCasC change: verify environment and private-key readability before Jenkins restart. The current canonical restart path triggers `render_jcasc.py`; UI reload alone may reuse stale rendered YAML.
- Job DSL and JCasC together: apply and verify JCasC first, then run Seed Job with the confirmed repository ref.
- Nginx change: run `nginx -t` before reload; if syntax check fails, do not reload.
- systemd change: copy only a repository-backed unit, run `daemon-reload`, restart only that service.
- env example change: merge field names manually into the real server env; never overwrite it.

### 4. Produce Verification Handoff

Do not execute verification commands.

Provide:

1. server commands for the user
2. expected results
3. common failure modes and the stop point
4. exact output to paste back

Wait for the user to execute them on the target server.

Do not mark the release or project step verified until the user pastes sufficient evidence.

### 5. Interpret Returned Output

When the user pastes output:

1. identify the first failing layer
2. distinguish deployment failure from application/test failure
3. provide the smallest next diagnostic command set
4. update the relevant learning record only after evidence is available

Do not expand a focused deployment problem into a full regression campaign.

## Output Format

Use this structure:

```markdown
## 本次发布范围

- 目标分支：
- 变更组件：
- 需要生效的服务：
- 不需要执行的动作：

## 请在目标服务器执行

### 1. 安全预检
<commands>

### 2. 拉取代码
<commands>

### 3. 组件生效
<only relevant commands>

### 4. 最小 Smoke
<only relevant commands>

## 预期结果

- ...

## 常见失败和停止点

- ...

## 请贴回

- branch / before commit / after commit
- service status
- health or HTTP result
- relevant error log
```

Keep command blocks directly executable except for clearly marked placeholders.

## Guardrails

- Do not proactively run `pytest`, Allure, Postman/Newman, JMeter, frontend test runners, or long server validation.
- Do not SSH to the target server or restart services from the agent.
- Do not claim successful verification before user evidence.
- Do not delete files, directories, Nginx sites, units, Jenkins jobs, or runtime data without current-conversation approval.
- Do not use `git reset --hard`, force push, destructive checkout, or history rewriting.
- Do not write business source code directly on the server.
- Do not expose `:5173`, `:8000`, or raw `:8080` as the product access path; Nginx HTTPS is the external entry.
- Do not put real credentials in repository files, commands, learning notes, or chat summaries.
- Do not recommend `VITE_JENKINS_BASE_URL=http://127.0.0.1:8080/jenkins`; browser-facing configuration must use the external Jenkins URL.
- Do not turn Jenkins test-execution pipelines into platform-release pipelines.

## Learning Record

For a completed implementation step, record:

- problem solved
- files changed and why
- release decision flow
- key paths, services, and configuration fields
- user-run validation commands and expected results
- common failures
- review questions

Use the relevant module guide or step document. Keep the active project status in `docs/overview/8-day-full-project-execution-plan.md`.
