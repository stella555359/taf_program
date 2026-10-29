# Portal API 契约文档

## 1. 范围

本文档描述 `kpi-dashboard/portal` 当前实现的 Portal 对外契约，覆盖：

- 页面职责
- HTTP 路由
- adapter 职责
- 输入 schema
- job 持久化结构

## 2. 页面契约

### Portal 首页

- 路由：`GET /`
- 模板：`portal/templates/home.html`
- 目的：模块导航入口
- 数据源：`repo_registry.get_module_cards()`

### Detector 页面

- 模块页：`GET /kpi-anomaly-detector/`
- 详情页：`GET /kpi-anomaly-detector/jobs/<job_id>`
- 模板：
  - `portal/templates/modules/kpi_detector.html`
  - `portal/templates/modules/kpi_detector_job.html`

### Generator 页面

- 模块页：`GET /kpi-generator/`
- 详情页：`GET /kpi-generator/jobs/<job_id>`
- 模板：
  - `portal/templates/modules/kpi_generator.html`
  - `portal/templates/modules/kpi_generator_job.html`

### Traffic Model 页面

- 模块页：`GET /kpi-traffic-model/`
- 详情页：`GET /kpi-traffic-model/jobs/<job_id>`
- 模板：
  - `portal/templates/modules/kpi_traffic_model.html`
  - `portal/templates/modules/kpi_traffic_model_job.html`

## 3. 路由契约

### Portal blueprint

- `GET /`
- `GET /healthz`

### Detector blueprint

- `GET /`
- `POST /submit`
- `POST /validate-upload-filenames`
- `GET /jobs/<job_id>`
- `POST /jobs/<job_id>/rerun`
- `POST /jobs/bulk/rerun`
- `POST /jobs/<job_id>/cancel`
- `POST /jobs/<job_id>/delete`
- `POST /jobs/bulk/delete`
- `GET /api/jobs/<job_id>`
- `GET /jobs/<job_id>/artifacts/<artifact_kind>`
- `GET /jobs/<job_id>/detail-artifacts/<artifact_kind>/<item_index>`
- `GET /jobs/<job_id>/artifacts/<path:asset_path>`

### Generator blueprint

- `GET /`
- `POST /jobs`
- `GET /jobs/<job_id>`
- `POST /jobs/<job_id>/rerun`
- `POST /jobs/<job_id>/cancel`
- `POST /jobs/<job_id>/delete`
- `GET /api/jobs/<job_id>`
- `GET /jobs/<job_id>/artifacts/<artifact_kind>`

### Traffic Model blueprint

- `GET /`
- `GET /api/resolve-env`
- `POST /jobs`
- `GET /jobs/<job_id>`
- `GET /api/jobs/<job_id>`
- `GET /jobs/<job_id>/artifacts/<artifact_kind>`
- `POST /jobs/<job_id>/delete`

## 4. Adapter 契约

### 共同职责

所有 adapter 都应负责：

- 返回模块元数据
- 提供示例执行命令
- 标准化 Portal 输入
- 创建和持久化 job
- 把输出映射成 artifact 和页面摘要

### Detector adapter

关键方法：

- `describe_module()`
- `sample_command()`
- `filter_options()`
- `query_jobs()`
- `validate_filename()`
- `submit()`
- `rerun()`
- `cancel()`
- `delete()`
- `read_job_log_tail()`
- `artifact_path()`

### Generator adapter

关键方法：

- `describe_module()`
- `sample_command()`
- `filter_options()`
- `query_jobs()`
- `submit()`
- `submit_scout_conversion()`
- `rerun()`
- `cancel()`
- `delete()`
- `artifact_path()`

### Traffic Model adapter

关键方法：

- `describe_module()`
- `sample_command()`
- `inspect_env()`
- `submit_request()`
- `get_job()`
- `list_jobs()`
- `delete()`
- `artifact_path()`

## 5. 输入 Schema 契约

定义于 `portal/schemas/input_models.py`。

### 公共模型

- `PortalJobCommonFields`
- `PortalRuntimeOptions`

### 模块模型

- `DetectorPortalInput`
- `GeneratorPortalInput`
- `GeneratorScoutPortalInput`
- `TrafficModelPortalInput`
- `InputValidationError`

## 6. Job 持久化契约

job 由 `portal/services/job_store.py` 的基础逻辑创建，再由 adapter 追加业务字段。

关键存储字段包括：

- `id`
- `module_key`
- `original_filename`
- `stored_filename`
- `status`
- `created_at`
- `started_at`
- `completed_at`
- `error_message`
- `process_pid`
- `input_path`
- `stdout_log_path`
- `stderr_log_path`
- `result_json_path`
- `report_html_path`
- `report_excel_path`
- `report_data_path`
- `stats`
- `current_record`

SQLite 表包括：

- `jobs`
- `job_events`
- `job_links`
- `job_artifacts`

## 7. 结论

Portal 的稳定契约可以概括为：页面和路由保持稳定，adapter 吸收兄弟仓库差异，job store 负责保存统一的运行态数据。