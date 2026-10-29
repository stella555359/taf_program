# KPI Dashboard Portal

Flask Portal repository hosted in `kpi-dashboard`.

## User Guide

- Portal + standalone guide for `kpi-anomaly-detector` and `kpi-generator`: `docs/portal_kpi_generator_detector_user_guide.md`
- One-page quick start for end users: `docs/portal_kpi_generator_detector_quick_start.md`
- FAQ + troubleshooting checklist for frontline users: `docs/portal_kpi_generator_detector_faq_checklist.md`
- Developer / operations guide: `docs/portal_kpi_generator_detector_devops_guide.md`
- Architecture optimization roadmap: `docs/portal_architecture_optimization_roadmap.md`

## Purpose

This repository is the web portal shell for multiple KPI-related capabilities.

- `kpi-anomaly-detector` is treated as the anomaly detection capability repository
- `kpi-generator` is treated as the KPI report generation capability repository
- `kpi-dashboard` contains only the Portal UI, navigation, adapters, and future orchestration logic

## Current Scope

This first version provides:

- A Portal landing page
- A `KPI Anomaly Detector` module page
- A `KPI Generator` module page
- Config-driven adapters that point to sibling repositories
- Repository health and entrypoint visibility in the UI
- Working upload and background execution flow for `kpi-anomaly-detector`
- Portal-side job records with stdout and stderr logs for detector runs
- Scout conversion with multi-DistName input, multi-sheet Excel output, and scout-specific detector summary HTML flow

## Repository Layout

```text
kpi-dashboard/
  app.py
  requirements.txt
  portal/
    app_factory.py
    blueprints/
    adapters/
    services/
    templates/
    static/
```

## Sibling Repository Assumptions

The Portal assumes this folder layout:

```text
kpi_web_app/
  kpi-dashboard/
  kpi-anomaly-detector/
  kpi-generator/
  kpi_traffic_model/
```

## Local Start

```powershell
cd kpi-dashboard
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:8010`.

## Debian Deployment

The repository includes deployment scripts under `deploy/` for Debian hosts.

- `deploy/deploy_debian_10.21.41.175.sh` deploys the Portal to `10.21.41.175`
- `deploy/deploy_debian_10.57.159.149.sh` deploys the Portal to `10.57.159.149`

The `10.57.159.149` deployment script assumes:

- workspace root is `/home/ute/kpi_web_app`
- sibling repositories exist under that root
- `kpi_traffic_model/robotws` and `kpi_traffic_model/testline_configuration` are present
- attach jobs run through the external Robot environment activation command `source /home/ute/venv/bin/activate` unless overridden with `KPI_TRAFFIC_MODEL_ACTIVATE_COMMAND`
- by default, external access goes through nginx on port `443`
- it can also reuse an existing nginx site by injecting the Portal location snippet into an existing `server {}` block
- local gunicorn binds to `127.0.0.1:8088`
- firewall rules are managed with `iptables`
- if no certificate is provided, the deploy script generates a self-signed TLS certificate for nginx

After the initial deployment, use `deploy/update_debian_10.57.159.149.sh` to validate the layout and restart the running service after code updates. If Python packages changed, rerun it with `REFRESH_PYTHON_DEPS=1`.

### Reuse Existing Nginx Site

If `443` is already terminated by another reverse proxy, prefer reusing that existing nginx site and expose the Portal at `${URL_PREFIX}` under that site.

- Automatic mode: `REUSE_EXISTING_NGINX_SITE=1` tells the deploy script to auto-detect a single enabled nginx site other than `default` and `kpi-dashboard`
- Explicit mode: `EXISTING_NGINX_SERVER_CONF=/etc/nginx/sites-available/your-site.conf` tells the deploy script exactly which nginx server config to patch
- `PUBLIC_BASE_URL=https://your-host` makes deployment output and verification URLs human-usable
- `VERIFY_URL=https://your-host${URL_PREFIX}/` lets the deploy or update script verify the final externally exposed URL

Example:

```text
cd /home/ute/kpi_web_app/kpi-dashboard/deploy
sudo REUSE_EXISTING_NGINX_SITE=1 PUBLIC_BASE_URL=https://10.57.159.149 VERIFY_URL=https://10.57.159.149/kpi-dashboard/ ./deploy_debian_10.57.159.149.sh
```

### Deployment Path Table

| Purpose | Variable | Path |
| --- | --- | --- |
| Workspace root | `WORKSPACE_ROOT` | `/home/ute/kpi_web_app` |
| Portal repo | `PORTAL_ROOT` | `/home/ute/kpi_web_app/kpi-dashboard` |
| Detector repo | `DETECTOR_ROOT` | `/home/ute/kpi_web_app/kpi-anomaly-detector` |
| Report repo | `REPORT_ROOT` | `/home/ute/kpi_web_app/kpi-generator` |
| Traffic model repo | `TRAFFIC_MODEL_ROOT` | `/home/ute/kpi_web_app/kpi_traffic_model` |
| robotws repo | `ROBOTWS_ROOT` | `/home/ute/kpi_web_app/kpi_traffic_model/robotws` |
| testline repo | `TESTLINE_ROOT` | `/home/ute/kpi_web_app/kpi_traffic_model/testline_configuration` |
| Python virtual environment | `VENV_DIR` | `/home/ute/kpi_web_app/.venv` |
| Gunicorn executable | `VENV_DIR/bin/gunicorn` | `/home/ute/kpi_web_app/.venv/bin/gunicorn` |
| Python executable | `VENV_DIR/bin/python` | `/home/ute/kpi_web_app/.venv/bin/python` |
| Portal runtime directory | `PORTAL_ROOT/instance` | `/home/ute/kpi_web_app/kpi-dashboard/instance` |
| Traffic model job directory | `PORTAL_ROOT/instance/jobs/kpi-traffic-model` | `/home/ute/kpi_web_app/kpi-dashboard/instance/jobs/kpi-traffic-model` |
| Traffic model activate command | `KPI_TRAFFIC_MODEL_ACTIVATE_COMMAND` | `source /home/ute/venv/bin/activate` |
| Detector reports | `DETECTOR_ROOT/reports` | `/home/ute/kpi_web_app/kpi-anomaly-detector/reports` |
| Detector data | `DETECTOR_ROOT/data` | `/home/ute/kpi_web_app/kpi-anomaly-detector/data` |
| Generator entrypoint | `REPORT_ROOT/kpi_generator.py` | `/home/ute/kpi_web_app/kpi-generator/kpi_generator.py` |
| Service user home | `APP_HOME` | `/var/lib/kpiapp` |
| Portal logs | `LOG_DIR` | `/var/log/kpi-dashboard` |
| Environment file | `ENV_FILE` | `/etc/default/kpi-dashboard` |
| Systemd service file | `SERVICE_FILE` | `/etc/systemd/system/kpi-dashboard.service` |
| Nginx site config | `NGINX_SITE` | `/etc/nginx/sites-available/kpi-dashboard` |
| Nginx enabled symlink | `NGINX_LINK` | `/etc/nginx/sites-enabled/kpi-dashboard` |
| Nginx location snippet | `NGINX_SNIPPET` | `/etc/nginx/snippets/kpi-dashboard-location.conf` |

## Detector Upload Naming Rule

The Portal validates KPI detector uploads before a job is queued.

- The filename must contain an environment code such as `T076` or `T813`
- The filename must contain a scenario segment after that environment
- The scenario segment must end before a csv marker such as `_1csv`, `_2csv10`, or `_1csv8run`

Examples:

```text
exec20260325T120349_SBTS26R3.ENB.9999.260319.000005_T813.SCF.T813.gNB.25R3.20260224_7UE_DL_Burst_1csv.xlsx
0129.1_26R2.0126.7_T076.SCF_7UEs_SFTPDL_1csv8run.xlsx
0324.2_26R2.0182.0_T076.T07.26R2psot2c_CB012971_32UEs_httpDL.SmallShortF15_2csv10_20260324_215532.xlsx
```

If the filename cannot be parsed, the UI shows `file name incorrect` and the upload is rejected.

## Detector Performance Tuning

The detector HTML report history depth can be tuned by environment variable:

```text
KPI_HTML_HISTORY_LIMIT=20
```

This controls how many recent history batches are embedded into generated report assets for charting. Lower values reduce report payload size and improve page load time.

The Portal can also auto-fail detector jobs that remain running too long:

```text
KPI_DETECTOR_TIMEOUT_SECONDS=1800
```

This timeout is enforced by the Portal job runner. Users can also cancel queued or running detector jobs from the Portal UI.

## Next Step

This Portal is prepared for the next integration stage:

1. Expand `kpi-generator` with more Compass-side generation options and richer validation
2. Persist richer job metadata and structured result summaries in the Portal repository
3. Add queue control, retries, and cleanup policies for detector jobs
4. Upgrade adapters from local CLI invocation to HTTP services later
