# Portal API Contract

## 1. Scope

This document describes the Portal-facing contract implemented by `kpi-dashboard/portal`.

It covers:

- page responsibilities
- HTTP routes
- adapter responsibilities
- input schemas
- persisted job structure

## 2. Page Contract

### Portal home

- route: `GET /`
- template: `portal/templates/home.html`
- purpose: module navigation entry
- data source: `repo_registry.get_module_cards()`

### Detector pages

- module page: `GET /kpi-anomaly-detector/`
- detail page: `GET /kpi-anomaly-detector/jobs/<job_id>`
- templates:
  - `portal/templates/modules/kpi_detector.html`
  - `portal/templates/modules/kpi_detector_job.html`

### Generator pages

- module page: `GET /kpi-generator/`
- detail page: `GET /kpi-generator/jobs/<job_id>`
- templates:
  - `portal/templates/modules/kpi_generator.html`
  - `portal/templates/modules/kpi_generator_job.html`

### Traffic model pages

- module page: `GET /kpi-traffic-model/`
- detail page: `GET /kpi-traffic-model/jobs/<job_id>`
- templates:
  - `portal/templates/modules/kpi_traffic_model.html`
  - `portal/templates/modules/kpi_traffic_model_job.html`

## 3. Route Contract

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

### Traffic model blueprint

- `GET /`
- `GET /api/resolve-env`
- `POST /jobs`
- `GET /jobs/<job_id>`
- `GET /api/jobs/<job_id>`
- `GET /jobs/<job_id>/artifacts/<artifact_kind>`
- `POST /jobs/<job_id>/delete`

## 4. Adapter Contract

### Shared responsibilities

All adapters must:

- describe module metadata
- provide sample execution command
- normalize Portal input
- create and persist Portal jobs
- map outputs to artifacts and job summaries

### Detector adapter

Important methods:

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

Important methods:

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

### Traffic model adapter

Important methods:

- `describe_module()`
- `sample_command()`
- `inspect_env()`
- `submit_request()`
- `get_job()`
- `list_jobs()`
- `delete()`
- `artifact_path()`

## 5. Input Schema Contract

Defined in `portal/schemas/input_models.py`.

### Common models

- `PortalJobCommonFields`
- `PortalRuntimeOptions`

### Module models

- `DetectorPortalInput`
- `GeneratorPortalInput`
- `GeneratorScoutPortalInput`
- `TrafficModelPortalInput`
- `InputValidationError`

## 6. Job Persistence Contract

Jobs are created in `portal/services/job_store.py` and enriched by adapters.

Important stored fields include:

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

SQLite tables:

- `jobs`
- `job_events`
- `job_links`
- `job_artifacts`

## 7. Core Conclusion

The stable Portal contract is: routes and templates remain consistent while adapters absorb the differences of sibling repositories and the job store persists normalized operational state.