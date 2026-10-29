# Portal Page To Template Mapping

## 1. Purpose

This document maps each Portal page to its template file, route, user actions, and frontend callback chain.

## 2. Global Layout

### Shared shell

- template: `portal/templates/base.html`
- responsibility:
  - shared HTML shell
  - global stylesheet include
  - top navigation
  - flash message stack
- main navigation targets:
  - `portal.home`
  - `kpi_detector.index`
  - `kpi_generator.index`
  - `kpi_traffic_model.index`

## 3. Home Page

### Page mapping

- route: `GET /`
- blueprint handler: `portal.home`
- template: `portal/templates/home.html`
- backend data source: `repo_registry.get_module_cards()`

### Main UI actions

- `Open module` button
  - action: `url_for(module.route_name)`
  - effect: jumps into module index page

## 4. Detector Pages

### Detector index page

- route: `GET /kpi-anomaly-detector/`
- handler: `kpi_detector.index`
- template: `portal/templates/modules/kpi_detector.html`

### Main forms and buttons

- upload form
  - action: `POST /kpi-anomaly-detector/submit`
  - fields: `files`, `is_base_file`, filename override hidden fields
- filter form
  - action: `GET /kpi-anomaly-detector/`
  - fields: `q`, `status`, `release`, `environment`, `scenario`, `page`
- bulk rerun button
  - form action: `POST /kpi-anomaly-detector/jobs/bulk/rerun`
- bulk delete button
  - form action: `POST /kpi-anomaly-detector/jobs/bulk/delete`
- row filename link
  - target: `GET /kpi-anomaly-detector/jobs/<job_id>`
- row rerun button
  - action: `POST /kpi-anomaly-detector/jobs/<job_id>/rerun`
- row cancel button
  - action: `POST /kpi-anomaly-detector/jobs/<job_id>/cancel`
- row delete button
  - action: `POST /kpi-anomaly-detector/jobs/<job_id>/delete`

### Frontend callback chain

- filename validation callback
  - JS uses `fetch()` to call `POST /kpi-anomaly-detector/validate-upload-filenames`
  - invalid filenames open override dialog
  - user provides Env and Scenario
  - script fills hidden override fields
  - form submit continues
- filter-dependent scenario list callback
  - template uses `scenario_map` JSON to rebuild scenario options when release or environment changes
- visible job auto-refresh callback
  - JS polls `GET /kpi-anomaly-detector/api/jobs/<job_id>` for visible queued or running jobs
  - job row status, artifact area, and buttons are refreshed in place
  - polling interval is driven by `window.setTimeout()`

### Detector detail page

- route: `GET /kpi-anomaly-detector/jobs/<job_id>`
- handler: `kpi_detector.job_detail`
- template: `portal/templates/modules/kpi_detector_job.html`

### Main actions

- back button to module index
- run again button
  - action: `POST /kpi-anomaly-detector/jobs/<job_id>/rerun`
- cancel button
  - action: `POST /kpi-anomaly-detector/jobs/<job_id>/cancel`
- delete button
  - action: `POST /kpi-anomaly-detector/jobs/<job_id>/delete`
- artifact buttons
  - stdout and stderr downloads
  - main report HTML, Excel, JSON
  - per-sheet detail HTML and Excel
  - linked job jump links

### Frontend callback chain

- detail auto-refresh callback
  - JS polls `GET /kpi-anomaly-detector/api/jobs/<job_id>`
  - page reload occurs when data indicates terminal state or changed rendering is needed
  - polling loop uses `window.setTimeout()`

## 5. Generator Pages

### Generator index page

- route: `GET /kpi-generator/`
- handler: `kpi_generator.index`
- template: `portal/templates/modules/kpi_generator.html`

### Main forms and buttons

- generator submit form
  - action: `POST /kpi-generator/jobs`
  - purpose: template-set or template-name based generation
- scout conversion form
  - action: `POST /kpi-generator/jobs`
  - purpose: convert scout workbook into Compass-style output
- filter form
  - action: `GET /kpi-generator/`
  - fields: `q`, `status`, `environment`, `scenario`, `page`
- row filename link
  - target: `GET /kpi-generator/jobs/<job_id>`
- row run again button
  - action: `POST /kpi-generator/jobs/<job_id>/rerun`
- row cancel button
  - action: `POST /kpi-generator/jobs/<job_id>/cancel`
- row delete button
  - action: `POST /kpi-generator/jobs/<job_id>/delete`

### Frontend callback chain

- template preview callback
  - selected template set and manual `template_names` are merged in browser preview areas
- timestamp builder callback
  - user creates one or more time ranges
  - script expands and merges intervals
  - hidden `report_timestamps_list` field is updated before submit

### Generator detail page

- route: `GET /kpi-generator/jobs/<job_id>`
- handler: `kpi_generator.job_detail`
- template: `portal/templates/modules/kpi_generator_job.html`

### Main actions

- back button to module index
- linked detector job button when available
- run again button
- cancel button
- delete button
- artifact downloads for source and final report
- links to request, result, stdout, stderr, and final report artifacts inside the page body

### Frontend callback chain

- detail auto-refresh callback
  - JS polls `GET /kpi-generator/api/jobs/<job_id>`
  - page reload occurs during queued or running status updates
  - countdown blocks are updated by client-side timer logic

## 6. Traffic Model Pages

### Traffic model index page

- route: `GET /kpi-traffic-model/`
- handler: `kpi_traffic_model.index`
- template: `portal/templates/modules/kpi_traffic_model.html`

### Main forms and buttons

- env resolve form
  - action: `GET /kpi-traffic-model/`
  - field: `env`
- workflow submit form
  - action: `POST /kpi-traffic-model/jobs`
  - fields include env, selected UEs, runtime flags, stage options, traffic item options
- history row link
  - target: `GET /kpi-traffic-model/jobs/<job_id>`
- preview artifact links
  - action: `GET /kpi-traffic-model/jobs/<job_id>/artifacts/<artifact_kind>`

### Frontend callback chain

- this page is mainly server-rendered
- no significant client-side polling was observed on index page
- env resolution data is returned server-side through page re-render

### Traffic model detail page

- route: `GET /kpi-traffic-model/jobs/<job_id>`
- handler: `kpi_traffic_model.job_detail`
- template: `portal/templates/modules/kpi_traffic_model_job.html`

### Main actions

- back button to module page
- delete button
- artifact download buttons
- linked job jump links

### Frontend callback chain

- auto-refresh callback
  - for queued or running jobs the page executes `window.setTimeout()` then `window.location.reload()`
  - refresh interval is 4 seconds in current template

## 7. Mapping Summary

The Portal is server-rendered first and script-enhanced second.

The main callback patterns are:

- form submit to blueprint routes
- AJAX validation or status polling via `fetch()`
- timed refresh via `window.setTimeout()`
- full-page reload on job detail pages when live state changes