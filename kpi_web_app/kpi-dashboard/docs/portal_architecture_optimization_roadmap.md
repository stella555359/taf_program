# Portal 架构优化真实状态与后续计划

本文替代旧版“理想目标型”路线图，面向 `kpi-dashboard` 的开发、测试和运维同学，记录截至当前代码状态的真实进展、未完成项和下一步动作，避免把历史 roadmap 误读为“已经全部完成”。

适用范围:

- 已接入模块: `kpi-anomaly-detector`、`kpi-generator`、`kpi-traffic-model`
- 部署目标: Debian Portal 服务，当前入口为 `https://10.57.159.149/kpi-dashboard/`

## 1. 结论摘要

截至当前版本，Portal 已完成从“单模块页面壳”向“多模块任务入口”的第一阶段平台化改造，但没有完成旧 roadmap 中第一、第二、第三优先级的全部目标。

当前更准确的状态判断是:

- 第一优先级: 部分完成，核心骨架已落地，但 runner / 运维闭环未完成
- 第二优先级: 部分完成，contract / schema 已有基础实现，但未完全平台化
- 第三优先级: 大部分未完成，目前仅有零散能力，不可视为已交付

如果只保留一句话:

- Portal 现在已经能稳定承载 detector、generator、traffic model 的统一入口和作业视图
- 但还不能宣称“多模块任务控制平面已全面完成”

## 2. 当前已完成

### 2.1 平台配置基础收口已落地

已完成:

- `portal/config.py` 提供统一配置解析入口
- 已区分 `dev / test / prod`
- `SECRET_KEY` 已环境化，`prod` 环境要求必须显式提供
- 已统一读取 Portal 关键配置:
  - `KPI_DASHBOARD_ENV`
  - `KPI_DASHBOARD_SECRET_KEY`
  - `KPI_DASHBOARD_PORT`
  - `KPI_DASHBOARD_URL_PREFIX`
  - `KPI_DASHBOARD_LOG_LEVEL`
  - `KPI_JOB_STORE_BACKEND`
  - `KPI_SQLITE_PATH`
  - `KPI_DETECTOR_PYTHON`
  - `KPI_GENERATOR_PYTHON`
  - `COMPASS_*`

现状评价:

- 已从“散落读取环境变量”进入“集中配置入口”阶段
- 但模块级并发、统一 retry、cleanup 策略等平台执行配置仍未统一定义

### 2.2 Job Store 已升级到 SQLite 主路径

已完成:

- `portal/services/job_store.py` 已支持 SQLite backend
- 已有表:
  - `jobs`
  - `job_events`
  - `job_links`
  - `job_artifacts`
- 已支持:
  - 作业主记录持久化
  - artifact 注册
  - linked job 注册
  - event 时间线查询

现状评价:

- 这部分已经明显超出旧的 `job.json` 目录扫描模式
- 但还没有 retention 元数据、cleanup 元数据、历史归档策略

### 2.3 统一 runner 骨架已存在

已完成:

- `portal/runners/unified_runner.py` 已提供统一线程运行器
- 已支持:
  - 同一 job 防重复提交
  - 同模块 dispatcher 防重复启动
  - 统一的线程生命周期清理

现状评价:

- 这是 runner 抽离的起点，不是最终形态
- 目前仍属于进程内线程模型，不是完整的恢复型后台执行平台

### 2.4 模块 contract / schema 基础版已落地

已完成:

- `portal/contracts.py` 定义了:
  - `ModuleCapabilityContract`
  - `JobContract`
  - `SummaryContract`
- `portal/schemas/input_models.py` 定义了:
  - `GeneratorPortalInput`
  - `GeneratorScoutPortalInput`
  - `DetectorPortalInput`
  - `TrafficModelPortalInput`
- `portal/adapters/base.py` 已把 contract 暴露给 UI 层

现状评价:

- Portal 已不再完全依赖模块内部脚本字段做页面渲染
- 但 failure payload、artifact lifecycle、跨模块统一 linked job 语义还没有完全制度化

### 2.5 基础测试体系已经建立

已完成:

- `tests/test_job_store.py`
- `tests/test_unified_runner.py`
- `tests/test_portal_contracts.py`
- `tests/test_portal_input_schemas.py`
- `tests/test_portal_smoke.py`
- `tests/test_portal_submissions.py`

覆盖范围:

- 配置与 schema 基础校验
- SQLite job store 元数据
- runner 去重行为
- Portal 页面 smoke
- detector / generator 提交与 artifact 行为

现状评价:

- 已达到“关键链路可以回归”的最低可用水平
- 但还没有更系统的端到端恢复测试、运维健康测试、压力与并发测试

### 2.6 多模块接入与 Portal UI 已可用

已完成:

- detector、generator、traffic model 均有独立模块入口
- Portal 支持统一首页入口、job 列表、job detail、artifact 下载
- generator 与 detector 的联动链路已可用
- detector 多 sheet artifact 展示已修复
- detector 文件名不合规时，Portal 已支持补填 `Env` / `Scenario` 后自动重命名并提交

### 2.7 部署脚本已进入“正式部署脚本”阶段

已完成:

- Debian 部署脚本已支持:
  - systemd
  - gunicorn
  - nginx reverse proxy
  - HTTPS
  - URL prefix `/kpi-dashboard`
- 本次进一步补齐了环境文件写入能力:
  - `KPI_DASHBOARD_ENV`
  - `KPI_DASHBOARD_SECRET_KEY`
  - `KPI_DASHBOARD_LOG_LEVEL`
  - `KPI_JOB_STORE_BACKEND`
  - `KPI_SQLITE_PATH`
  - `KPI_DETECTOR_PYTHON`
  - `KPI_GENERATOR_PYTHON`
  - `COMPASS_*`
  - `KPI_TRAFFIC_MODEL_*`
- 部署后的默认探活已切换到 `/healthz`

## 3. 当前未完成

### 3.1 第一优先级未完成项

未完成:

- 统一 runner 仍不是恢复型后台执行平台
- 未形成统一模块并发数配置
- 未形成统一 retry / backoff / orphan process 回收策略
- 未形成统一任务清理策略

影响:

- 现在可以跑，但还不适合宣称“平台执行层已完全成型”

### 3.2 第二优先级未完成项

未完成:

- adapter contract 还没有覆盖完整 failure payload 契约
- summary schema 仍带有模块私有结构残留
- capability 驱动渲染还不彻底，部分页面仍带模块特例
- traffic model 虽已接入 Portal，但业务边界和平台边界还没有彻底收口

影响:

- 新模块继续接入时，仍有复制已有模块特例的风险

### 3.3 第三优先级未完成项

未完成:

- 没有统一 metrics 出口
- 没有失败率、排队时长、模块耗时统计
- 没有 artifact retention policy
- 没有 cleanup scheduler
- 没有审计日志能力
- 没有更完整的 health / ready / dependency health 体系

说明:

- 本次新增了最小健康检查 `/healthz`
- 这只是第三优先级的一小步，不代表 observability 已完成

## 4. 当前真实优先级判断

### 第一优先级状态

状态: 部分完成

已完成:

- 配置基础收口
- SQLite job store 主路径
- runner 骨架
- 首批测试体系

未完成:

- runner 恢复能力
- 平台统一并发 / retry / cleanup

### 第二优先级状态

状态: 部分完成

已完成:

- contract 基础类
- input schema 基础类
- summary contract 基础类

未完成:

- failure payload 正式化
- linked job / artifact contract 进一步统一
- traffic model 平台边界彻底收口

### 第三优先级状态

状态: 大部分未完成

已完成:

- 最小健康检查 `/healthz`

未完成:

- 指标体系
- retention / cleanup
- 审计与告警
- 更完整的可观测性平台能力

## 5. Debian 10.57.159.149 现状与要求

当前入口:

- `https://10.57.159.149/kpi-dashboard/`

当前推荐的生产环境配置:

- `KPI_DASHBOARD_ENV=prod`
- `KPI_DASHBOARD_SECRET_KEY=<strong-random-secret>`
- `KPI_DASHBOARD_PORT=8088`
- `KPI_DASHBOARD_URL_PREFIX=/kpi-dashboard`
- `KPI_DASHBOARD_LOG_LEVEL=INFO`
- `KPI_JOB_STORE_BACKEND=sqlite`
- `KPI_SQLITE_PATH=/home/ute/kpi_web_app/kpi-dashboard/instance/portal.db`
- `KPI_DETECTOR_TIMEOUT_SECONDS=1800`
- `KPI_DETECTOR_PYTHON=/home/ute/kpi_web_app/.venv/bin/python`
- `KPI_GENERATOR_PYTHON=/home/ute/kpi_web_app/.venv/bin/python`
- `KPI_TRAFFIC_MODEL_ROBOTWS_PATH=/home/ute/kpi_web_app/kpi_traffic_model/robotws`
- `KPI_TRAFFIC_MODEL_TESTLINE_PATH=/home/ute/kpi_web_app/kpi_traffic_model/testline_configuration`
- `KPI_TRAFFIC_MODEL_ACTIVATE_COMMAND=source /home/ute/venv/bin/activate`
- `COMPASS_USERNAME=<optional but required for generator standard mode>`
- `COMPASS_PASSWORD=<optional but required for generator standard mode>`
- `COMPASS_LOGIN_URL=http://compass.dyn.nesc.nokia.net:8080/common/login_handle/`
- `COMPASS_TEMPLATE_SET_URL=http://compass.dyn.nesc.nokia.net:8080/kpi/kpi_template_set/`
- `COMPASS_TEMPLATE_SET_TIMEOUT_SECONDS=60`
- `COMPASS_TEMPLATE_SET_CACHE_TTL_SECONDS=300`

## 6. 下一步

建议按这个顺序继续推进:

1. 把 traffic model 对 `KPI_TRAFFIC_MODEL_*` 的运行时消费补全到 orchestrator 边界
2. 给 job store 增加 retention / cleanup 元数据与定时清理策略
3. 在 runner 层补模块级并发限制与统一 retry 策略
4. 增加更完整的 health / readiness / dependency health 检查
5. 增加结构化指标与运维统计视图

## 7. 文档使用说明

从现在开始，这份文档应被视为“Portal 当前真实状态说明”，而不是“历史理想路线图”。

如果后续新增功能或完成度发生变化，应直接更新“已完成 / 未完成 / 下一步”，不要再保留模糊的“建议中”状态。
