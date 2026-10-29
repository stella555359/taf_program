#!/usr/bin/env bash

set -euo pipefail

APP_USER="${APP_USER:-kpiapp}"
APP_GROUP="${APP_GROUP:-kpiapp}"
SERVER_IP="${SERVER_IP:-10.21.41.175}"
PORTAL_PORT="${PORTAL_PORT:-8010}"
NGINX_LISTEN_PORT="${NGINX_LISTEN_PORT:-8081}"
URL_PREFIX="${URL_PREFIX:-/kpi-dashboard}"
GUNICORN_WORKERS="${GUNICORN_WORKERS:-2}"
GUNICORN_THREADS="${GUNICORN_THREADS:-4}"
SCOUT_LIB_SOURCE="${SCOUT_LIB_SOURCE:-}"
EXISTING_NGINX_SERVER_CONF="${EXISTING_NGINX_SERVER_CONF:-}"
HTTP_PROXY="${HTTP_PROXY:-http://10.158.100.9:8080}"
HTTPS_PROXY="${HTTPS_PROXY:-${HTTP_PROXY}}"
NO_PROXY="${NO_PROXY:-127.0.0.1,localhost,10.21.41.175}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
PORTAL_ROOT="${WORKSPACE_ROOT}/kpi-dashboard"
DETECTOR_ROOT="${WORKSPACE_ROOT}/kpi-anomaly-detector"
REPORT_ROOT="${WORKSPACE_ROOT}/kpi-generator"
VENV_DIR="${WORKSPACE_ROOT}/.venv"
ECHARTS_VENDOR_DIR="${PORTAL_ROOT}/portal/static/vendor/echarts"
ECHARTS_VENDOR_FILE="${ECHARTS_VENDOR_DIR}/echarts.min.js"
APP_HOME="/var/lib/${APP_USER}"
LOG_DIR="/var/log/kpi-dashboard"
ENV_FILE="/etc/default/kpi-dashboard"
SERVICE_FILE="/etc/systemd/system/kpi-dashboard.service"
NGINX_SITE="/etc/nginx/sites-available/kpi-dashboard"
NGINX_LINK="/etc/nginx/sites-enabled/kpi-dashboard"
NGINX_SNIPPET="/etc/nginx/snippets/kpi-dashboard-location.conf"

log() {
  printf '[deploy] %s\n' "$*"
}

fail() {
  printf '[deploy] ERROR: %s\n' "$*" >&2
  exit 1
}

require_root() {
  if [[ "$(id -u)" -ne 0 ]]; then
    fail "Please run this script as root or with sudo."
  fi
}

configure_proxy() {
  if [[ -z "${HTTP_PROXY}" ]]; then
    return
  fi

  log "Using HTTP proxy ${HTTP_PROXY}"
  export http_proxy="${HTTP_PROXY}"
  export HTTP_PROXY="${HTTP_PROXY}"
  export https_proxy="${HTTPS_PROXY}"
  export HTTPS_PROXY="${HTTPS_PROXY}"
  export no_proxy="${NO_PROXY}"
  export NO_PROXY="${NO_PROXY}"

  mkdir -p /etc/apt/apt.conf.d
  cat > /etc/apt/apt.conf.d/99kpi-dashboard-proxy <<EOF
Acquire::http::Proxy "${HTTP_PROXY}";
Acquire::https::Proxy "${HTTPS_PROXY}";
EOF
}

check_layout() {
  [[ -d "${PORTAL_ROOT}" ]] || fail "Missing portal repo: ${PORTAL_ROOT}"
  [[ -f "${PORTAL_ROOT}/app.py" ]] || fail "Missing portal entrypoint: ${PORTAL_ROOT}/app.py"
  [[ -d "${DETECTOR_ROOT}" ]] || fail "Missing detector repo: ${DETECTOR_ROOT}"
  [[ -f "${DETECTOR_ROOT}/scripts/run_detector.py" ]] || fail "Missing detector entrypoint: ${DETECTOR_ROOT}/scripts/run_detector.py"
  [[ -d "${REPORT_ROOT}" ]] || fail "Missing kpi-generator repo: ${REPORT_ROOT}"
  [[ -f "${REPORT_ROOT}/kpi_generator.py" ]] || fail "Missing kpi-generator entrypoint: ${REPORT_ROOT}/kpi_generator.py"
}

install_system_packages() {
  log "Installing Debian system packages"
  export DEBIAN_FRONTEND=noninteractive
  apt-get update
  apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    python3-dev \
    build-essential \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    nginx \
    curl \
    ca-certificates
}

ensure_service_user() {
  if ! getent group "${APP_GROUP}" >/dev/null; then
    log "Creating group ${APP_GROUP}"
    groupadd --system "${APP_GROUP}"
  fi

  if ! id -u "${APP_USER}" >/dev/null 2>&1; then
    log "Creating user ${APP_USER}"
    useradd --system --gid "${APP_GROUP}" --create-home --home-dir "${APP_HOME}" --shell /usr/sbin/nologin "${APP_USER}"
  fi

  mkdir -p "${APP_HOME}" "${LOG_DIR}"
  chown -R "${APP_USER}:${APP_GROUP}" "${APP_HOME}" "${LOG_DIR}" "${WORKSPACE_ROOT}"
}

setup_python_env() {
  log "Creating Python virtual environment at ${VENV_DIR}"
  python3 -m venv "${VENV_DIR}"
  "${VENV_DIR}/bin/pip" install --proxy "${HTTP_PROXY}" --upgrade pip setuptools wheel
  "${VENV_DIR}/bin/pip" install --proxy "${HTTP_PROXY}" \
    "Flask>=3.0,<4.0" \
    gunicorn \
    pandas \
    numpy \
    scipy \
    openpyxl \
    requests \
    urllib3
}

prepare_runtime_dirs() {
  log "Preparing runtime directories"
  mkdir -p \
    "${PORTAL_ROOT}/instance" \
    "${ECHARTS_VENDOR_DIR}" \
    "${DETECTOR_ROOT}/reports" \
    "${DETECTOR_ROOT}/data" \
    "${REPORT_ROOT}/logs"
  chown -R "${APP_USER}:${APP_GROUP}" "${PORTAL_ROOT}/instance" "${ECHARTS_VENDOR_DIR}" "${DETECTOR_ROOT}/reports" "${DETECTOR_ROOT}/data" "${REPORT_ROOT}/logs"
}

install_frontend_assets() {
  log "Installing local ECharts asset"
  mkdir -p "${ECHARTS_VENDOR_DIR}"
  curl -fsSL --proxy "${HTTP_PROXY}" "https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js" -o "${ECHARTS_VENDOR_FILE}"
  chown "${APP_USER}:${APP_GROUP}" "${ECHARTS_VENDOR_FILE}"
}

write_env_file() {
  log "Writing environment file ${ENV_FILE}"
  cat > "${ENV_FILE}" <<EOF
PYTHONUNBUFFERED=1
KPI_DASHBOARD_PORT=${PORTAL_PORT}
KPI_DASHBOARD_URL_PREFIX=${URL_PREFIX}
KPI_HTML_HISTORY_LIMIT=${KPI_HTML_HISTORY_LIMIT:-20}
KPI_DETECTOR_TIMEOUT_SECONDS=${KPI_DETECTOR_TIMEOUT_SECONDS:-1800}
HTTP_PROXY=${HTTP_PROXY}
HTTPS_PROXY=${HTTPS_PROXY}
NO_PROXY=${NO_PROXY}

# Optional for kpi-generator future integration:
# COMPASS_USERNAME=your_username
# COMPASS_PASSWORD=your_password
EOF
}

write_systemd_service() {
  log "Writing systemd service ${SERVICE_FILE}"
  cat > "${SERVICE_FILE}" <<EOF
[Unit]
Description=KPI Dashboard Portal
After=network.target

[Service]
Type=simple
User=${APP_USER}
Group=${APP_GROUP}
WorkingDirectory=${PORTAL_ROOT}
EnvironmentFile=${ENV_FILE}
ExecStart=${VENV_DIR}/bin/gunicorn --workers ${GUNICORN_WORKERS} --threads ${GUNICORN_THREADS} --timeout 600 --bind 127.0.0.1:${PORTAL_PORT} wsgi:app
Restart=always
RestartSec=5
StandardOutput=append:${LOG_DIR}/portal.out.log
StandardError=append:${LOG_DIR}/portal.err.log

[Install]
WantedBy=multi-user.target
EOF
}

write_nginx_location_snippet() {
  log "Writing nginx location snippet ${NGINX_SNIPPET}"
  mkdir -p /etc/nginx/snippets
  cat > "${NGINX_SNIPPET}" <<EOF
location = ${URL_PREFIX} {
    return 301 ${URL_PREFIX}/;
}

location ${URL_PREFIX}/ {
  gzip on;
  gzip_min_length 1024;
  gzip_comp_level 5;
  gzip_vary on;
  gzip_proxied any;
  gzip_types text/plain text/css text/xml text/javascript application/javascript application/x-javascript application/json application/xml+rss image/svg+xml;

    proxy_pass http://127.0.0.1:${PORTAL_PORT}/;
    proxy_http_version 1.1;
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
    proxy_set_header X-Script-Name ${URL_PREFIX};
    proxy_set_header X-Forwarded-Prefix ${URL_PREFIX};
    proxy_set_header Connection "";
    proxy_read_timeout 600s;
    proxy_send_timeout 600s;
}
EOF
}

patch_existing_nginx_server() {
  [[ -f "${EXISTING_NGINX_SERVER_CONF}" ]] || fail "Existing nginx server config not found: ${EXISTING_NGINX_SERVER_CONF}"

  if grep -Fq "include ${NGINX_SNIPPET};" "${EXISTING_NGINX_SERVER_CONF}"; then
    log "Existing nginx server config already includes ${NGINX_SNIPPET}"
    return
  fi

  log "Patching existing nginx server config ${EXISTING_NGINX_SERVER_CONF}"
  python3 - <<PY
from pathlib import Path

config_path = Path(${EXISTING_NGINX_SERVER_CONF@Q})
include_line = f"    include ${NGINX_SNIPPET};\n"
text = config_path.read_text(encoding='utf-8')
marker = text.rfind('}')
if marker == -1:
    raise SystemExit('No closing brace found in nginx config')
updated = text[:marker] + include_line + text[marker:]
config_path.write_text(updated, encoding='utf-8')
PY
}

write_standalone_nginx_site() {
  log "Writing standalone nginx site ${NGINX_SITE}"
  cat > "${NGINX_SITE}" <<EOF
server {
    listen ${NGINX_LISTEN_PORT};
    server_name ${SERVER_IP};

    client_max_body_size 100m;

    include ${NGINX_SNIPPET};
}
EOF

  ln -sfn "${NGINX_SITE}" "${NGINX_LINK}"
}

write_nginx_site() {
  write_nginx_location_snippet

  if [[ -n "${EXISTING_NGINX_SERVER_CONF}" ]]; then
    patch_existing_nginx_server
  else
    write_standalone_nginx_site
  fi
}

setup_scout_path() {
  if [[ -n "${SCOUT_LIB_SOURCE}" && -d "${SCOUT_LIB_SOURCE}" ]]; then
    log "Creating Scout compatibility symlink from ${SCOUT_LIB_SOURCE}"
    mkdir -p /home/ute/cli/taf
    ln -sfn "${SCOUT_LIB_SOURCE}" /home/ute/cli/taf/taf.sw.scout
  fi

  if [[ ! -d /home/ute/cli/taf/taf.sw.scout ]]; then
    log "WARNING: /home/ute/cli/taf/taf.sw.scout not found. kpi-generator may not run until this dependency is provided when Compass-side extensions require Scout."
  fi
}

enable_services() {
  log "Reloading systemd and enabling services"
  systemctl daemon-reload
  systemctl enable --now kpi-dashboard.service
  nginx -t
  systemctl enable nginx
  systemctl restart nginx
}

print_summary() {
  cat <<EOF

Deployment complete.

Workspace root: ${WORKSPACE_ROOT}
Portal Base URL: http://${SERVER_IP}:${NGINX_LISTEN_PORT}/
Portal URL Prefix: ${URL_PREFIX}
Portal Login URL: http://${SERVER_IP}:${NGINX_LISTEN_PORT}${URL_PREFIX}
Gunicorn bind: 127.0.0.1:${PORTAL_PORT}
Nginx listen port: ${NGINX_LISTEN_PORT}

Useful commands:
  systemctl status kpi-dashboard --no-pager
  journalctl -u kpi-dashboard -f
  tail -f ${LOG_DIR}/portal.out.log
  tail -f ${LOG_DIR}/portal.err.log
  nginx -t
  curl -I http://${SERVER_IP}:${NGINX_LISTEN_PORT}${URL_PREFIX}

Proxy settings:
  HTTP_PROXY=${HTTP_PROXY}
  HTTPS_PROXY=${HTTPS_PROXY}
  NO_PROXY=${NO_PROXY}

Notes:
  - Keep the sibling repo layout unchanged:
    ${WORKSPACE_ROOT}/kpi-dashboard
    ${WORKSPACE_ROOT}/kpi-anomaly-detector
    ${WORKSPACE_ROOT}/kpi-generator
  - kpi-anomaly-detector writes reports into ${DETECTOR_ROOT}/reports
  - kpi-generator still requires Compass network access and may require the Scout library path for future extensions
  - If port 80 is already serving another site, rerun with:
    EXISTING_NGINX_SERVER_CONF=/etc/nginx/sites-available/your-existing-site.conf sudo ./deploy_debian_10.21.41.175.sh
EOF
}

main() {
  require_root
  check_layout
  configure_proxy
  install_system_packages
  ensure_service_user
  setup_python_env
  prepare_runtime_dirs
  install_frontend_assets
  write_env_file
  write_systemd_service
  write_nginx_site
  setup_scout_path
  enable_services
  print_summary
}

main "$@"