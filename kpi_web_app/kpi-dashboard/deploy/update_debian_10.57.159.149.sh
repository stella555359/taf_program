#!/usr/bin/env bash

set -euo pipefail

APP_USER="${APP_USER:-kpiapp}"
APP_GROUP="${APP_GROUP:-kpiapp}"
SERVER_IP="${SERVER_IP:-10.57.159.149}"
PORTAL_PORT="${PORTAL_PORT:-8088}"
NGINX_LISTEN_PORT="${NGINX_LISTEN_PORT:-443}"
URL_PREFIX="${URL_PREFIX:-/kpi-dashboard}"
KPI_DASHBOARD_ENV="${KPI_DASHBOARD_ENV:-prod}"
KPI_DASHBOARD_SECRET_KEY="${KPI_DASHBOARD_SECRET_KEY:-}"
KPI_DASHBOARD_LOG_LEVEL="${KPI_DASHBOARD_LOG_LEVEL:-INFO}"
KPI_JOB_STORE_BACKEND="${KPI_JOB_STORE_BACKEND:-sqlite}"
KPI_SQLITE_PATH="${KPI_SQLITE_PATH:-}"
KPI_DETECTOR_PYTHON="${KPI_DETECTOR_PYTHON:-}"
KPI_GENERATOR_PYTHON="${KPI_GENERATOR_PYTHON:-}"
COMPASS_USERNAME="${COMPASS_USERNAME:-}"
COMPASS_PASSWORD="${COMPASS_PASSWORD:-}"
COMPASS_LOGIN_URL="${COMPASS_LOGIN_URL:-http://compass.dyn.nesc.nokia.net:8080/common/login_handle/}"
COMPASS_TEMPLATE_SET_URL="${COMPASS_TEMPLATE_SET_URL:-http://compass.dyn.nesc.nokia.net:8080/kpi/kpi_template_set/}"
COMPASS_TEMPLATE_SET_TIMEOUT_SECONDS="${COMPASS_TEMPLATE_SET_TIMEOUT_SECONDS:-60}"
COMPASS_TEMPLATE_SET_CACHE_TTL_SECONDS="${COMPASS_TEMPLATE_SET_CACHE_TTL_SECONDS:-300}"
HTTP_PROXY="${HTTP_PROXY:-http://10.158.100.9:8080}"
HTTPS_PROXY="${HTTPS_PROXY:-${HTTP_PROXY}}"
NO_PROXY="${NO_PROXY:-127.0.0.1,localhost,10.57.159.149}"
REFRESH_PYTHON_DEPS="${REFRESH_PYTHON_DEPS:-0}"
VERIFY_URL="${VERIFY_URL:-}"
SKIP_HTTP_VERIFY="${SKIP_HTTP_VERIFY:-0}"
TLS_CERT_PATH="${TLS_CERT_PATH:-/etc/nginx/ssl/kpi-dashboard.crt}"
TLS_KEY_PATH="${TLS_KEY_PATH:-/etc/nginx/ssl/kpi-dashboard.key}"
TLS_CERT_CN="${TLS_CERT_CN:-${SERVER_IP}}"
ALLOW_SELF_SIGNED_TLS="${ALLOW_SELF_SIGNED_TLS:-1}"

WORKSPACE_ROOT="${WORKSPACE_ROOT:-/home/ute/kpi_web_app}"
PORTAL_ROOT="${WORKSPACE_ROOT}/kpi-dashboard"
DETECTOR_ROOT="${WORKSPACE_ROOT}/kpi-anomaly-detector"
REPORT_ROOT="${WORKSPACE_ROOT}/kpi-generator"
TRAFFIC_MODEL_ROOT="${WORKSPACE_ROOT}/kpi_traffic_model"
ROBOTWS_ROOT="${TRAFFIC_MODEL_ROOT}/robotws"
TESTLINE_ROOT="${TRAFFIC_MODEL_ROOT}/testline_configuration"
TRAFFIC_MODEL_ACTIVATE_COMMAND="${KPI_TRAFFIC_MODEL_ACTIVATE_COMMAND:-source /home/ute/venv/bin/activate}"
VENV_DIR="${WORKSPACE_ROOT}/.venv"
LOG_DIR="/var/log/kpi-dashboard"
ENV_FILE="/etc/default/kpi-dashboard"
SERVICE_FILE="/etc/systemd/system/kpi-dashboard.service"
NGINX_SITE="/etc/nginx/sites-available/kpi-dashboard"
NGINX_SNIPPET="/etc/nginx/snippets/kpi-dashboard-location.conf"

log() {
  printf '[update] %s\n' "$*"
}

quote_env_value() {
  printf "%q" "$1"
}

fail() {
  printf '[update] ERROR: %s\n' "$*" >&2
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

  export http_proxy="${HTTP_PROXY}"
  export HTTP_PROXY="${HTTP_PROXY}"
  export https_proxy="${HTTPS_PROXY}"
  export HTTPS_PROXY="${HTTPS_PROXY}"
  export no_proxy="${NO_PROXY}"
  export NO_PROXY="${NO_PROXY}"
}

check_layout() {
  [[ -d "${PORTAL_ROOT}" ]] || fail "Missing portal repo: ${PORTAL_ROOT}"
  [[ -f "${PORTAL_ROOT}/app.py" ]] || fail "Missing portal entrypoint: ${PORTAL_ROOT}/app.py"
  [[ -d "${DETECTOR_ROOT}" ]] || fail "Missing detector repo: ${DETECTOR_ROOT}"
  [[ -f "${DETECTOR_ROOT}/scripts/run_detector.py" ]] || fail "Missing detector entrypoint: ${DETECTOR_ROOT}/scripts/run_detector.py"
  [[ -d "${REPORT_ROOT}" ]] || fail "Missing kpi-generator repo: ${REPORT_ROOT}"
  [[ -f "${REPORT_ROOT}/kpi_generator.py" ]] || fail "Missing kpi-generator entrypoint: ${REPORT_ROOT}/kpi_generator.py"
  [[ -d "${TRAFFIC_MODEL_ROOT}" ]] || fail "Missing kpi_traffic_model repo: ${TRAFFIC_MODEL_ROOT}"
  [[ -d "${ROBOTWS_ROOT}" ]] || fail "Missing robotws repo: ${ROBOTWS_ROOT}"
  [[ -d "${TESTLINE_ROOT}" ]] || fail "Missing testline_configuration repo: ${TESTLINE_ROOT}"
  [[ -x "${VENV_DIR}/bin/python" ]] || fail "Missing virtual environment: ${VENV_DIR}"
}

normalize_runtime_config() {
  if [[ -z "${KPI_SQLITE_PATH}" ]]; then
    KPI_SQLITE_PATH="${PORTAL_ROOT}/instance/portal.db"
  fi

  if [[ -z "${KPI_DETECTOR_PYTHON}" ]]; then
    KPI_DETECTOR_PYTHON="${VENV_DIR}/bin/python"
  fi

  if [[ -z "${KPI_GENERATOR_PYTHON}" ]]; then
    KPI_GENERATOR_PYTHON="${VENV_DIR}/bin/python"
  fi
}

refresh_python_deps() {
  if [[ "${REFRESH_PYTHON_DEPS}" != "1" ]]; then
    log "Skipping Python dependency refresh"
    return
  fi

  log "Refreshing Python dependencies in ${VENV_DIR}"
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

upsert_env_var() {
  local key="$1"
  local value="$2"

  if grep -q "^${key}=" "${ENV_FILE}"; then
    sed -i "s|^${key}=.*|${key}=${value}|" "${ENV_FILE}"
  else
    printf '%s=%s\n' "${key}" "${value}" >> "${ENV_FILE}"
  fi
}

has_env_var() {
  local key="$1"
  [[ -f "${ENV_FILE}" ]] || return 1
  grep -q "^${key}=" "${ENV_FILE}"
}

ensure_runtime_dirs() {
  mkdir -p \
    "${PORTAL_ROOT}/instance" \
    "${PORTAL_ROOT}/instance/jobs/kpi-traffic-model" \
    "${DETECTOR_ROOT}/reports" \
    "${DETECTOR_ROOT}/data" \
    "${DETECTOR_ROOT}/docs" \
    "${REPORT_ROOT}/logs" \
    "${LOG_DIR}"

  chown -R "${APP_USER}:${APP_GROUP}" \
    "${PORTAL_ROOT}/instance" \
    "${DETECTOR_ROOT}/reports" \
    "${DETECTOR_ROOT}/data" \
    "${DETECTOR_ROOT}/docs" \
    "${REPORT_ROOT}/logs" \
    "${LOG_DIR}"
}

ensure_env_file() {
  if [[ ! -f "${ENV_FILE}" ]]; then
    cat > "${ENV_FILE}" <<EOF
PYTHONUNBUFFERED=1
KPI_DASHBOARD_PORT=${PORTAL_PORT}
KPI_DASHBOARD_URL_PREFIX=${URL_PREFIX}
KPI_HTML_HISTORY_LIMIT=${KPI_HTML_HISTORY_LIMIT:-20}
KPI_DETECTOR_TIMEOUT_SECONDS=${KPI_DETECTOR_TIMEOUT_SECONDS:-1800}
HTTP_PROXY=${HTTP_PROXY}
HTTPS_PROXY=${HTTPS_PROXY}
NO_PROXY=${NO_PROXY}
EOF
  fi

  upsert_env_var "PYTHONUNBUFFERED" "1"
  upsert_env_var "KPI_DASHBOARD_ENV" "$(quote_env_value "${KPI_DASHBOARD_ENV}")"
  if [[ -n "${KPI_DASHBOARD_SECRET_KEY}" ]]; then
    upsert_env_var "KPI_DASHBOARD_SECRET_KEY" "$(quote_env_value "${KPI_DASHBOARD_SECRET_KEY}")"
  fi
  upsert_env_var "KPI_DASHBOARD_PORT" "${PORTAL_PORT}"
  upsert_env_var "KPI_DASHBOARD_URL_PREFIX" "${URL_PREFIX}"
  upsert_env_var "KPI_DASHBOARD_LOG_LEVEL" "$(quote_env_value "${KPI_DASHBOARD_LOG_LEVEL}")"
  upsert_env_var "KPI_JOB_STORE_BACKEND" "$(quote_env_value "${KPI_JOB_STORE_BACKEND}")"
  upsert_env_var "KPI_SQLITE_PATH" "$(quote_env_value "${KPI_SQLITE_PATH}")"
  upsert_env_var "KPI_HTML_HISTORY_LIMIT" "${KPI_HTML_HISTORY_LIMIT:-20}"
  upsert_env_var "KPI_DETECTOR_TIMEOUT_SECONDS" "${KPI_DETECTOR_TIMEOUT_SECONDS:-1800}"
  upsert_env_var "KPI_DETECTOR_PYTHON" "$(quote_env_value "${KPI_DETECTOR_PYTHON}")"
  upsert_env_var "KPI_GENERATOR_PYTHON" "$(quote_env_value "${KPI_GENERATOR_PYTHON}")"
  upsert_env_var "HTTP_PROXY" "$(quote_env_value "${HTTP_PROXY}")"
  upsert_env_var "HTTPS_PROXY" "$(quote_env_value "${HTTPS_PROXY}")"
  upsert_env_var "NO_PROXY" "$(quote_env_value "${NO_PROXY}")"
  upsert_env_var "KPI_DASHBOARD_PUBLIC_SCHEME" "https"
  upsert_env_var "KPI_TRAFFIC_MODEL_ROBOTWS_PATH" "$(quote_env_value "${ROBOTWS_ROOT}")"
  upsert_env_var "KPI_TRAFFIC_MODEL_TESTLINE_PATH" "$(quote_env_value "${TESTLINE_ROOT}")"
  upsert_env_var "KPI_TRAFFIC_MODEL_ACTIVATE_COMMAND" "$(quote_env_value "${TRAFFIC_MODEL_ACTIVATE_COMMAND}")"
  if [[ -n "${COMPASS_USERNAME}" ]] || ! has_env_var "COMPASS_USERNAME"; then
    upsert_env_var "COMPASS_USERNAME" "$(quote_env_value "${COMPASS_USERNAME}")"
  fi
  if [[ -n "${COMPASS_PASSWORD}" ]] || ! has_env_var "COMPASS_PASSWORD"; then
    upsert_env_var "COMPASS_PASSWORD" "$(quote_env_value "${COMPASS_PASSWORD}")"
  fi
  upsert_env_var "COMPASS_LOGIN_URL" "$(quote_env_value "${COMPASS_LOGIN_URL}")"
  upsert_env_var "COMPASS_TEMPLATE_SET_URL" "$(quote_env_value "${COMPASS_TEMPLATE_SET_URL}")"
  upsert_env_var "COMPASS_TEMPLATE_SET_TIMEOUT_SECONDS" "${COMPASS_TEMPLATE_SET_TIMEOUT_SECONDS}"
  upsert_env_var "COMPASS_TEMPLATE_SET_CACHE_TTL_SECONDS" "${COMPASS_TEMPLATE_SET_CACHE_TTL_SECONDS}"
}

write_systemd_service() {
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
ExecStart=${VENV_DIR}/bin/gunicorn --workers 2 --threads 4 --timeout 600 --bind 127.0.0.1:${PORTAL_PORT} wsgi:app
Restart=always
RestartSec=5
StandardOutput=append:${LOG_DIR}/portal.out.log
StandardError=append:${LOG_DIR}/portal.err.log

[Install]
WantedBy=multi-user.target
EOF
}

ensure_tls_assets() {
  local cert_dir
  cert_dir="$(dirname "${TLS_CERT_PATH}")"
  mkdir -p "${cert_dir}"

  if [[ -f "${TLS_CERT_PATH}" && -f "${TLS_KEY_PATH}" ]]; then
    log "Using existing TLS certificate ${TLS_CERT_PATH}"
    return
  fi

  if [[ "${ALLOW_SELF_SIGNED_TLS}" != "1" ]]; then
    fail "TLS certificate/key not found. Provide TLS_CERT_PATH and TLS_KEY_PATH or rerun with ALLOW_SELF_SIGNED_TLS=1."
  fi

  log "Generating self-signed TLS certificate for ${TLS_CERT_CN}"
  openssl req -x509 -nodes -newkey rsa:2048 \
    -keyout "${TLS_KEY_PATH}" \
    -out "${TLS_CERT_PATH}" \
    -days 825 \
    -subj "/CN=${TLS_CERT_CN}"
  chmod 600 "${TLS_KEY_PATH}"
}

write_nginx_location_snippet() {
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

write_nginx_site() {
  cat > "${NGINX_SITE}" <<EOF
server {
    listen ${NGINX_LISTEN_PORT} ssl;
    server_name ${SERVER_IP};

    ssl_certificate ${TLS_CERT_PATH};
    ssl_certificate_key ${TLS_KEY_PATH};
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_protocols TLSv1.2 TLSv1.3;

    client_max_body_size 100m;

    include ${NGINX_SNIPPET};
}
EOF
}

restart_services() {
  log "Restarting kpi-dashboard"
  systemctl daemon-reload
  systemctl restart kpi-dashboard.service
  nginx -t
  systemctl reload nginx
}

verify_service() {
  if [[ "${SKIP_HTTP_VERIFY}" == "1" ]]; then
    log "Skipping HTTP verification"
    return
  fi

  if [[ -n "${VERIFY_URL}" ]]; then
    log "Verifying endpoint ${VERIFY_URL}"
    curl -k -I "${VERIFY_URL}"
    return
  fi

  if [[ "${NGINX_LISTEN_PORT}" == "443" ]]; then
    log "Verifying endpoint https://${SERVER_IP}${URL_PREFIX}/healthz"
    curl -k -I "https://${SERVER_IP}${URL_PREFIX}/healthz"
    return
  fi

  log "Verifying endpoint https://${SERVER_IP}:${NGINX_LISTEN_PORT}${URL_PREFIX}/healthz"
  curl -k -I "https://${SERVER_IP}:${NGINX_LISTEN_PORT}${URL_PREFIX}/healthz"
}

print_summary() {
  cat <<EOF

Update complete.

Useful commands:
  systemctl status kpi-dashboard --no-pager
  journalctl -u kpi-dashboard -f
  tail -f ${LOG_DIR}/portal.out.log
  tail -f ${LOG_DIR}/portal.err.log

If package versions changed, rerun with:
  REFRESH_PYTHON_DEPS=1 sudo ./update_debian_10.57.159.149.sh

If Portal is exposed through an existing nginx site instead of external port ${NGINX_LISTEN_PORT}, rerun update with:
  VERIFY_URL=https://your-host${URL_PREFIX}/ sudo ./update_debian_10.57.159.149.sh
  or SKIP_HTTP_VERIFY=1 sudo ./update_debian_10.57.159.149.sh

Traffic model paths:
  robotws=${ROBOTWS_ROOT}
  testline_configuration=${TESTLINE_ROOT}
EOF
}

main() {
  require_root
  configure_proxy
  check_layout
  normalize_runtime_config
  refresh_python_deps
  ensure_runtime_dirs
  ensure_env_file
  write_systemd_service
  ensure_tls_assets
  write_nginx_location_snippet
  write_nginx_site
  restart_services
  verify_service
  print_summary
}

main "$@"