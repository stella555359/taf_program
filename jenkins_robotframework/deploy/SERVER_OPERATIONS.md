# Server Operations Quick Reference

本文件记录服务器侧日常高频操作命令，适合部署后维护、重启服务、切换虚拟环境、查看日志和快速验证。

如果问题是“代码更新后到底需要执行哪些命令”，先看：

- `deploy/RELEASE_CHECKLIST.md`

它负责按改动路径选择最小发布动作；本文件只提供单项运维命令，不负责判断本次应该重启哪些组件。

如果是首次部署或环境尚未安装，回到：

- `deploy/DEPLOYMENT.md`

适用服务器路径：

```text
/opt/jenkins_robotframework
```

## 1. 常用目录

进入项目根目录：

```bash
cd /opt/jenkins_robotframework
```

进入后端：

```bash
cd /opt/jenkins_robotframework/platform-api
```

进入前端：

```bash
cd /opt/jenkins_robotframework/automation-portal
```

进入部署配置：

```bash
cd /opt/jenkins_robotframework/deploy
```

## 2. Platform API 虚拟环境

切到后端虚拟环境：

```bash
cd /opt/jenkins_robotframework/platform-api
source venv/bin/activate
```

确认当前 Python 来自虚拟环境：

```bash
which python
python --version
```

安装或更新后端依赖：

```bash
cd /opt/jenkins_robotframework/platform-api
source venv/bin/activate
python -m pip install -r requirements.txt
```

退出虚拟环境：

```bash
deactivate
```

## 3. Platform API 服务

查看状态：

```bash
sudo systemctl status platform-api --no-pager
```

重启服务：

```bash
sudo systemctl restart platform-api
```

启动 / 停止服务：

```bash
sudo systemctl start platform-api
sudo systemctl stop platform-api
```

设置开机启动：

```bash
sudo systemctl enable platform-api
```

查看最近日志：

```bash
sudo journalctl -u platform-api -n 100 --no-pager
```

实时跟踪日志：

```bash
sudo journalctl -u platform-api -f
```

本机健康检查：

```bash
curl -s http://127.0.0.1:8000/api/health
```

通过 Nginx 入口检查：

```bash
curl -k -s https://10.71.210.104/api/health
```

## 4. AI Analysis Worker 服务

查看状态：

```bash
sudo systemctl status platform-api-ai-worker --no-pager
```

重启服务：

```bash
sudo systemctl restart platform-api-ai-worker
```

启动 / 停止服务：

```bash
sudo systemctl start platform-api-ai-worker
sudo systemctl stop platform-api-ai-worker
```

设置开机启动：

```bash
sudo systemctl enable platform-api-ai-worker
```

查看最近日志：

```bash
sudo journalctl -u platform-api-ai-worker -n 100 --no-pager
```

实时跟踪日志：

```bash
sudo journalctl -u platform-api-ai-worker -f
```

如果 service 文件有更新，重新加载并重启：

```bash
sudo cp /opt/jenkins_robotframework/deploy/systemd/platform-api-ai-worker.service \
  /etc/systemd/system/platform-api-ai-worker.service
sudo systemctl daemon-reload
sudo systemctl restart platform-api-ai-worker
sudo systemctl status platform-api-ai-worker --no-pager
```

## 5. Jenkins 服务

查看状态：

```bash
sudo systemctl status jenkins --no-pager
```

重启服务：

```bash
sudo systemctl restart jenkins
```

启动 / 停止服务：

```bash
sudo systemctl start jenkins
sudo systemctl stop jenkins
```

查看最近日志：

```bash
sudo journalctl -u jenkins -n 100 --no-pager
```

实时跟踪日志：

```bash
sudo journalctl -u jenkins -f
```

检查 Jenkins prefix：

```bash
curl -I http://127.0.0.1:8080/jenkins/
```

## 6. Nginx 服务

检查配置语法：

```bash
sudo nginx -t
```

重新加载配置：

```bash
sudo systemctl reload nginx
```

重启 Nginx：

```bash
sudo systemctl restart nginx
```

查看状态：

```bash
sudo systemctl status nginx --no-pager
```

查看最近日志：

```bash
sudo journalctl -u nginx -n 100 --no-pager
```

检查启用的站点配置：

```bash
sudo ls -l /etc/nginx/sites-enabled/
```

同步仓库里的 Nginx 配置到系统位置：

```bash
sudo cp /opt/jenkins_robotframework/deploy/nginx/jenkins-kpi-platform.conf \
  /etc/nginx/sites-available/jenkins-kpi-platform.conf
sudo ln -sf /etc/nginx/sites-available/jenkins-kpi-platform.conf \
  /etc/nginx/sites-enabled/jenkins-kpi-platform.conf
sudo nginx -t
sudo systemctl reload nginx
```

## 7. Automation Portal 前端

安装依赖：

```bash
cd /opt/jenkins_robotframework/automation-portal
npm install
```

构建前端：

```bash
cd /opt/jenkins_robotframework/automation-portal
npm run build
```

构建后重新加载 Nginx：

```bash
sudo nginx -t
sudo systemctl reload nginx
```

浏览器访问：

```text
https://10.71.210.104/
```

## 8. 常用联动重启顺序

本节只给常见组合的快捷命令。先用 `deploy/RELEASE_CHECKLIST.md` 判断本次属于哪一类，不能把本节所有命令连续执行。

只改 Platform API Python 代码，且依赖文件没有变化：

```bash
sudo systemctl restart platform-api
sudo systemctl status platform-api --no-pager
curl -s http://127.0.0.1:8000/api/health
```

只有 `requirements.txt` 或依赖文件变化时，才先更新依赖：

```bash
cd /opt/jenkins_robotframework/platform-api
source venv/bin/activate
python -m pip install -r requirements.txt
deactivate
sudo systemctl restart platform-api
sudo systemctl status platform-api --no-pager
```

只改 AI worker 代码：

```bash
sudo systemctl restart platform-api-ai-worker
sudo systemctl status platform-api-ai-worker --no-pager
```

AI analysis API 和 worker 共享代码都改了：

```bash
sudo systemctl restart platform-api
sudo systemctl restart platform-api-ai-worker
sudo systemctl status platform-api --no-pager
sudo systemctl status platform-api-ai-worker --no-pager
```

只改前端页面，且 `package.json` / lock 文件没有变化：

```bash
cd /opt/jenkins_robotframework/automation-portal
npm run build
ls -la dist/index.html
sudo nginx -t
sudo systemctl reload nginx
```

只有 `package.json`、lock 文件变化或依赖尚未安装时，才在 build 前执行 `npm install`。

Nginx 配置改了：

```bash
sudo cp /opt/jenkins_robotframework/deploy/nginx/jenkins-kpi-platform.conf \
  /etc/nginx/sites-available/jenkins-kpi-platform.conf
sudo ln -sf /etc/nginx/sites-available/jenkins-kpi-platform.conf \
  /etc/nginx/sites-enabled/jenkins-kpi-platform.conf
sudo nginx -t
sudo systemctl reload nginx
```

Jenkins 改动必须先分类：

- `pipelines/**`、`scripts/**`
  - 通常不重启 Jenkins
  - 确认目标 Job 的 SCM ref 后触发最小构建
- `jobs/**`
  - 确认 `t813 && robot` Agent 在线
  - 运行 `seed/jenkins-robotframework-seed`
  - `REPOSITORY_REF` 必须指向包含本次 DSL 提交的分支、tag 或 commit
- `jcasc/**`
  - 先确认 `/etc/default/jenkins-jcasc` 和 launcher key 对 Jenkins 用户可读
  - 再按 `deploy/RELEASE_CHECKLIST.md` 的 JCasC 小节重启 Jenkins

不要把“Jenkins 配置改了”统一处理成无条件重启。

## 9. AI Analysis 快速验证

后端测试：

```bash
cd /opt/jenkins_robotframework/platform-api
source venv/bin/activate
python -m pytest tests/test_ai_analysis.py
```

重启 AI analysis 相关服务：

```bash
sudo systemctl restart platform-api
sudo systemctl restart platform-api-ai-worker
```

查看 worker 是否处理 queued 任务：

```bash
sudo journalctl -u platform-api-ai-worker -n 100 --no-pager
```

常见判断：

```text
analysis_status 一直 queued:
  platform-api-ai-worker 未运行，或 worker 与 platform-api 没连到同一个 RUNS_DB_PATH。

analysis_status=failed 且提示 Cursor / 403:
  请求可能走了 cursor_sdk。当前生产默认应使用 rules_first。

category 仍然 unknown:
  已完成 rules_first 分析，但 artifact 不足或没有命中规则。优先确认 output.xml、debug.log、robot-command.json、callback-payload.json、ute_ue.log 是否可读。
```

## 10. 故障排查优先级

页面打不开：

```bash
sudo systemctl status nginx --no-pager
sudo nginx -t
sudo journalctl -u nginx -n 100 --no-pager
```

`/api/health` 502：

```bash
sudo systemctl status platform-api --no-pager
sudo journalctl -u platform-api -n 100 --no-pager
curl -s http://127.0.0.1:8000/api/health
```

AI analysis 不出结果：

```bash
sudo systemctl status platform-api-ai-worker --no-pager
sudo journalctl -u platform-api-ai-worker -n 100 --no-pager
```

Jenkins 页面或 job 异常：

```bash
sudo systemctl status jenkins --no-pager
sudo journalctl -u jenkins -n 100 --no-pager
curl -I http://127.0.0.1:8080/jenkins/
```

## 11. 操作后确认清单

每次重启或部署后至少确认：

```text
1. sudo systemctl status <service> --no-pager 显示 active/running。
2. sudo journalctl -u <service> -n 100 --no-pager 没有新的明显异常。
3. /api/health 返回正常。
4. Portal 页面能打开。
5. 如果涉及 AI analysis，platform-api-ai-worker 日志中没有循环报错。
```
