# Portal Module Extension SOP

## 1. Purpose

This document defines the standard operating procedure for adding a fourth module into the Portal.

The goal is to keep new module integration consistent with the current architecture.

## 2. Preconditions

Before integration, the new module owner must provide:

- module name and key
- repository path
- readme path
- entry candidates
- execution model
- input contract
- output artifacts
- supported lifecycle actions
- status model

## 3. Integration Checklist

The fourth module must be wired into these layers:

1. repository registry
2. adapter layer
3. contracts and schemas
4. blueprint layer
5. templates
6. optional startup recovery
7. artifact mapping and links
8. documentation and tests

## 4. Step-By-Step SOP

### Step 1: define module key and repository metadata

Update `portal/services/repo_registry.py` with:

- `key`
- `title`
- `summary`
- `route_name`
- `repo_path`
- `readme_path`
- `entry_candidates`

Requirement:

- key naming should match current style, for example `kpi-anomaly-detector`

### Step 2: define input schema

If the module has structured input, add a dataclass in `portal/schemas/input_models.py`.

Best practice:

- reuse `PortalJobCommonFields`
- reuse `PortalRuntimeOptions`
- add `from_form()` or similar constructor
- raise `InputValidationError` for user-facing validation failures

### Step 3: implement adapter

Create a new adapter file in `portal/adapters/`, for example `kpi_new_module.py`.

Minimum adapter responsibilities:

- `describe_module()`
- `sample_command()`
- `list_jobs()`
- `get_job()`
- `submit(...)` or `submit_request(...)`
- `artifact_path()`
- `delete()`

Add these when supported:

- `query_jobs()`
- `filter_options()`
- `rerun()`
- `cancel()`
- `recover_startup_jobs()`

### Step 4: define job fields and artifacts

Use `job_store.create_job()` as the common baseline.

Adapter must populate module-specific fields such as:

- business context
- progress fields
- result payload path
- report artifact paths
- linked downstream job IDs

Ensure artifact kinds can be exposed through `platform_artifacts` and `platform_download_artifacts`.

### Step 5: implement blueprint

Create a new blueprint file in `portal/blueprints/`, for example `kpi_new_module.py`.

Minimum routes:

- module index page
- submit endpoint
- job detail page
- job status API if auto-refresh is needed
- artifact download endpoint
- delete endpoint

Optional routes:

- rerun
- cancel
- filter APIs
- preview APIs

### Step 6: register blueprint

Update `portal/app_factory.py` so the app registers the new blueprint during startup.

Also ensure URL prefix handling remains correct.

### Step 7: add templates

Create templates under `portal/templates/modules/`:

- `<module>.html`
- `<module>_job.html`

Best practice:

- follow current module page layout
- keep index page for submit and history
- keep detail page for status, artifacts, events, links, and logs

### Step 8: update navigation

Update `portal/templates/base.html` to add the new module link to the top navigation.

Update `home.html` only if extra presentation logic is needed. In most cases the registry-driven cards will appear automatically.

### Step 9: define capability and job contracts

If the UI needs explicit normalization, extend usage of:

- `ModuleCapabilityContract`
- `JobContract`
- `SummaryContract`

This keeps the new module aligned with current Portal behavior.

### Step 10: add startup recovery if needed

If the module launches background work, implement `recover_startup_jobs()` and call it from startup recovery flow.

### Step 11: add tests

Minimum recommended tests:

- schema validation tests
- adapter submit tests
- blueprint route tests
- artifact endpoint tests
- delete and rerun behavior tests

### Step 12: add documentation

Update these docs when a new module is added:

- Portal architecture details
- Portal API contract
- page-to-template mapping
- module user guide if needed

## 5. Reference Implementation Pattern

Use current modules as reference by complexity:

- simplest reference: `kpi_traffic_model`
- medium reference: `kpi_generator`
- most feature-rich reference: `kpi_detector`

## 6. Common Pitfalls

Avoid these mistakes:

- putting execution logic inside blueprint handlers
- skipping schema validation and using raw `request.form` everywhere
- returning artifacts without job-store registration
- adding template logic that depends on non-normalized adapter fields
- forgetting startup recovery for long-running jobs
- forgetting route registration in app factory

## 7. Definition Of Done

The new module integration is complete when:

- module card appears on home page
- nav link is visible in `base.html`
- user can submit a job from module index page
- job record is persisted in SQLite
- detail page renders correctly
- artifacts can be downloaded
- lifecycle actions behave as declared
- documentation and tests are updated

## 8. Core Conclusion

The safest extension path is always the same: register module metadata, normalize input with schemas, isolate module logic in an adapter, keep blueprints thin, and expose artifacts through the existing job-store model.