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
GUNICORN_WORKERS="${GUNICORN_WORKERS:-2}"
GUNICORN_THREADS="${GUNICORN_THREADS:-4}"
SCOUT_LIB_SOURCE="${SCOUT_LIB_SOURCE:-}"
EXISTING_NGINX_SERVER_CONF="${EXISTING_NGINX_SERVER_CONF:-}"
REUSE_EXISTING_NGINX_SITE="${REUSE_EXISTING_NGINX_SITE:-0}"
PUBLIC_BASE_URL="${PUBLIC_BASE_URL:-}"
VERIFY_URL="${VERIFY_URL:-}"
TLS_CERT_PATH="${TLS_CERT_PATH:-/etc/nginx/ssl/kpi-dashboard.crt}"
TLS_KEY_PATH="${TLS_KEY_PATH:-/etc/nginx/ssl/kpi-dashboard.key}"
TLS_CERT_CN="${TLS_CERT_CN:-${SERVER_IP}}"
ALLOW_SELF_SIGNED_TLS="${ALLOW_SELF_SIGNED_TLS:-1}"
HTTP_PROXY="${HTTP_PROXY:-http://10.158.100.9:8080}"
HTTPS_PROXY="${HTTPS_PROXY:-${HTTP_PROXY}}"
NO_PROXY="${NO_PROXY:-127.0.0.1,localhost,10.57.159.149}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="${WORKSPACE_ROOT:-/home/ute/kpi_web_app}"
PORTAL_ROOT="${WORKSPACE_ROOT}/kpi-dashboard"
DETECTOR_ROOT="${WORKSPACE_ROOT}/kpi-anomaly-detector"
REPORT_ROOT="${WORKSPACE_ROOT}/kpi-generator"
TRAFFIC_MODEL_ROOT="${WORKSPACE_ROOT}/kpi_traffic_model"
ROBOTWS_ROOT="${TRAFFIC_MODEL_ROOT}/robotws"
TESTLINE_ROOT="${TRAFFIC_MODEL_ROOT}/testline_configuration"
TRAFFIC_MODEL_ACTIVATE_COMMAND="${KPI_TRAFFIC_MODEL_ACTIVATE_COMMAND:-source /home/ute/venv/bin/activate}"
VENV_DIR="${WORKSPACE_ROOT}/.venv"
APP_HOME="/var/lib/${APP_USER}"
LOG_DIR="/var/log/kpi-dashboard"
ENV_FILE="/etc/default/kpi-dashboard"
SERVICE_FILE="/etc/systemd/system/kpi-dashboard.service"
NGINX_SITE="/etc/nginx/sites-available/kpi-dashboard"
NGINX_LINK="/etc/nginx/sites-enabled/kpi-dashboard"
NGINX_SNIPPET="/etc/nginx/snippets/kpi-dashboard-location.conf"
NGINX_DEFAULT_LINK="/etc/nginx/sites-enabled/default"

log() {
  printf '[deploy] %s\n' "$*"
}

fail() {
  printf '[deploy] ERROR: %s\n' "$*" >&2
  exit 1
}

warn() {
  printf '[deploy] WARNING: %s\n' "$*" >&2
}

quote_env_value() {
  printf "%q" "$1"
}

require_root() {
  if [[ "$(id -u)" -ne 0 ]]; then
    fail "Please run this script as root or with sudo."
  fi
}

resolve_nginx_mode() {
  if [[ -n "${EXISTING_NGINX_SERVER_CONF}" ]]; then
    log "Using existing nginx server config ${EXISTING_NGINX_SERVER_CONF}"
    return
  fi

  if [[ "${REUSE_EXISTING_NGINX_SITE}" != "1" ]]; then
    return
  fi

  mapfile -t candidates < <(find /etc/nginx/sites-enabled -maxdepth 1 -mindepth 1 \( -type f -o -type l \) ! -name default ! -name kpi-dashboard -print | sort)

  if [[ "${#candidates[@]}" -eq 1 ]]; then
    EXISTING_NGINX_SERVER_CONF="$(readlink -f "${candidates[0]}")"
    log "Auto-detected existing nginx server config ${EXISTING_NGINX_SERVER_CONF}"
    return
  fi

  if [[ "${#candidates[@]}" -gt 1 ]]; then
    warn "Multiple enabled nginx site candidates were found: ${candidates[*]}"
  else
    warn "No enabled nginx site candidate was found under /etc/nginx/sites-enabled/."
  fi

  fail "Set EXISTING_NGINX_SERVER_CONF=/etc/nginx/sites-available/your-existing-site.conf, or rerun without REUSE_EXISTING_NGINX_SITE=1."
}

portal_public_url() {
  if [[ -n "${PUBLIC_BASE_URL}" ]]; then
    printf '%s%s/' "${PUBLIC_BASE_URL%/}" "${URL_PREFIX}"
    return
  fi

  if [[ -n "${EXISTING_NGINX_SERVER_CONF}" ]]; then
    printf 'existing-nginx-site%s/' "${URL_PREFIX}"
    return
  fi

  if [[ "${NGINX_LISTEN_PORT}" == "443" ]]; then
    printf 'https://%s%s/' "${SERVER_IP}" "${URL_PREFIX}"
    return
  fi

  printf 'https://%s:%s%s/' "${SERVER_IP}" "${NGINX_LISTEN_PORT}" "${URL_PREFIX}"
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
  [[ -d "${TRAFFIC_MODEL_ROOT}" ]] || fail "Missing kpi_traffic_model repo: ${TRAFFIC_MODEL_ROOT}"
  [[ -d "${ROBOTWS_ROOT}" ]] || fail "Missing robotws repo: ${ROBOTWS_ROOT}"
  [[ -d "${TESTLINE_ROOT}" ]] || fail "Missing testline_configuration repo: ${TESTLINE_ROOT}"
}

normalize_runtime_config() {
  if [[ -z "${KPI_DASHBOARD_SECRET_KEY}" ]]; then
    fail "Set KPI_DASHBOARD_SECRET_KEY before deploying to Debian production."
  fi

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

install_system_packages() {
  log "Installing Debian system packages"
  export DEBIAN_FRONTEND=noninteractive
  if ! apt-get update; then
    warn "apt-get update failed. This is often caused by an unrelated third-party apt source with a missing GPG key."
    warn "Current deployment only needs standard Debian/company repositories. Check sources under /etc/apt/sources.list and /etc/apt/sources.list.d/."
    warn "If you see download.docker.com with NO_PUBKEY, disable that source temporarily or install its signing key, then rerun this script."
    fail "Cannot continue until apt repositories are healthy."
  fi
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
    openssl \
    ca-certificates \
    iptables-persistent
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
  chown -R "${APP_USER}:${APP_GROUP}" "${APP_HOME}" "${LOG_DIR}"
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
    "${PORTAL_ROOT}/instance/jobs/kpi-traffic-model" \
    "${DETECTOR_ROOT}/reports" \
    "${DETECTOR_ROOT}/data" \
    "${DETECTOR_ROOT}/docs" \
    "${REPORT_ROOT}/logs"
  chown -R "${APP_USER}:${APP_GROUP}" \
    "${PORTAL_ROOT}/instance" \
    "${DETECTOR_ROOT}/reports" \
    "${DETECTOR_ROOT}/data" \
    "${DETECTOR_ROOT}/docs" \
    "${REPORT_ROOT}/logs"
}

write_env_file() {
  log "Writing environment file ${ENV_FILE}"
  cat > "${ENV_FILE}" <<EOF
PYTHONUNBUFFERED=1
KPI_DASHBOARD_ENV=$(quote_env_value "${KPI_DASHBOARD_ENV}")
KPI_DASHBOARD_SECRET_KEY=$(quote_env_value "${KPI_DASHBOARD_SECRET_KEY}")
KPI_DASHBOARD_PORT=${PORTAL_PORT}
KPI_DASHBOARD_URL_PREFIX=${URL_PREFIX}
KPI_DASHBOARD_LOG_LEVEL=$(quote_env_value "${KPI_DASHBOARD_LOG_LEVEL}")
KPI_JOB_STORE_BACKEND=$(quote_env_value "${KPI_JOB_STORE_BACKEND}")
KPI_SQLITE_PATH=$(quote_env_value "${KPI_SQLITE_PATH}")
KPI_HTML_HISTORY_LIMIT=${KPI_HTML_HISTORY_LIMIT:-20}
KPI_DETECTOR_TIMEOUT_SECONDS=${KPI_DETECTOR_TIMEOUT_SECONDS:-1800}
KPI_DETECTOR_PYTHON=$(quote_env_value "${KPI_DETECTOR_PYTHON}")
KPI_GENERATOR_PYTHON=$(quote_env_value "${KPI_GENERATOR_PYTHON}")
HTTP_PROXY=$(quote_env_value "${HTTP_PROXY}")
HTTPS_PROXY=$(quote_env_value "${HTTPS_PROXY}")
NO_PROXY=$(quote_env_value "${NO_PROXY}")
KPI_DASHBOARD_PUBLIC_SCHEME=https
KPI_TRAFFIC_MODEL_ROBOTWS_PATH=$(quote_env_value "${ROBOTWS_ROOT}")
KPI_TRAFFIC_MODEL_TESTLINE_PATH=$(quote_env_value "${TESTLINE_ROOT}")
KPI_TRAFFIC_MODEL_ACTIVATE_COMMAND=$(quote_env_value "${TRAFFIC_MODEL_ACTIVATE_COMMAND}")
COMPASS_USERNAME=$(quote_env_value "${COMPASS_USERNAME}")
COMPASS_PASSWORD=$(quote_env_value "${COMPASS_PASSWORD}")
COMPASS_LOGIN_URL=$(quote_env_value "${COMPASS_LOGIN_URL}")
COMPASS_TEMPLATE_SET_URL=$(quote_env_value "${COMPASS_TEMPLATE_SET_URL}")
COMPASS_TEMPLATE_SET_TIMEOUT_SECONDS=${COMPASS_TEMPLATE_SET_TIMEOUT_SECONDS}
COMPASS_TEMPLATE_SET_CACHE_TTL_SECONDS=${COMPASS_TEMPLATE_SET_CACHE_TTL_SECONDS}
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
  server_starts = []
  depth = 0
  inside_comment = False
  for index, char in enumerate(text):
    if char == '\n':
      inside_comment = False
      continue
    if inside_comment:
      continue
    if char == '#':
      inside_comment = True
      continue
    if text.startswith('server', index) and depth == 0:
      tail = text[index + len('server'):]
      stripped = tail.lstrip()
      if stripped.startswith('{'):
        server_starts.append(index)
    if char == '{':
      depth += 1
    elif char == '}':
      depth -= 1

  if len(server_starts) != 1:
    raise SystemExit(
      'Refusing to patch nginx config automatically because it does not contain exactly one top-level server block. '
      'Set EXISTING_NGINX_SERVER_CONF to a dedicated single-server file or add the include manually.'
    )

  server_start = server_starts[0]
  brace_start = text.find('{', server_start)
  if brace_start == -1:
    raise SystemExit('No opening brace found for nginx server block')

  depth = 0
  server_end = -1
  for index in range(brace_start, len(text)):
    char = text[index]
    if char == '{':
      depth += 1
    elif char == '}':
      depth -= 1
      if depth == 0:
        server_end = index
        break

  if server_end == -1:
    raise SystemExit('No closing brace found for nginx server block')

  updated = text[:server_end] + include_line + text[server_end:]
config_path.write_text(updated, encoding='utf-8')
PY
}

write_standalone_nginx_site() {
  log "Writing standalone nginx site ${NGINX_SITE}"
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

  if [[ -L "${NGINX_DEFAULT_LINK}" || -f "${NGINX_DEFAULT_LINK}" ]]; then
    log "Disabling default nginx site to avoid port 80 conflicts"
    rm -f "${NGINX_DEFAULT_LINK}"
  fi

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

configure_firewall() {
  log "Configuring iptables rules for nginx and local gunicorn access"
  if [[ -z "${EXISTING_NGINX_SERVER_CONF}" ]]; then
    if ! iptables -C INPUT -p tcp --dport "${NGINX_LISTEN_PORT}" -j ACCEPT >/dev/null 2>&1; then
      iptables -I INPUT -p tcp --dport "${NGINX_LISTEN_PORT}" -j ACCEPT
    fi
  else
    log "Skipping extra nginx port firewall rule because an existing nginx site is being reused"
  fi

  if ! iptables -C INPUT -p tcp -s 127.0.0.1 --dport "${PORTAL_PORT}" -j ACCEPT >/dev/null 2>&1; then
    iptables -I INPUT -p tcp -s 127.0.0.1 --dport "${PORTAL_PORT}" -j ACCEPT
  fi

  if command -v netfilter-persistent >/dev/null 2>&1; then
    netfilter-persistent save
    netfilter-persistent reload
  else
    log "WARNING: netfilter-persistent not found. iptables rules were added but may not survive reboot."
  fi
}

verify_service() {
  if [[ -n "${VERIFY_URL}" ]]; then
    log "Verifying endpoint ${VERIFY_URL}"
    curl -k -I "${VERIFY_URL}"
    return
  fi

  if [[ -n "${EXISTING_NGINX_SERVER_CONF}" ]]; then
    log "Skipping HTTP probe because deployment reuses an existing nginx site. Set VERIFY_URL to enable post-deploy verification."
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

Deployment complete.

Workspace root: ${WORKSPACE_ROOT}
Portal Base URL: $(portal_public_url)
Portal URL Prefix: ${URL_PREFIX}
Portal Login URL: $(portal_public_url)
Gunicorn bind: 127.0.0.1:${PORTAL_PORT}
Nginx mode: $(if [[ -n "${EXISTING_NGINX_SERVER_CONF}" ]]; then printf 'reuse existing site (%s)' "${EXISTING_NGINX_SERVER_CONF}"; else printf 'standalone listen on %s' "${NGINX_LISTEN_PORT}"; fi)

Useful commands:
  systemctl status kpi-dashboard --no-pager
  journalctl -u kpi-dashboard -f
  tail -f ${LOG_DIR}/portal.out.log
  tail -f ${LOG_DIR}/portal.err.log
  nginx -t
  curl -I $(portal_public_url)

Proxy settings:
  HTTP_PROXY=${HTTP_PROXY}
  HTTPS_PROXY=${HTTPS_PROXY}
  NO_PROXY=${NO_PROXY}

Notes:
  - Keep the sibling repo layout unchanged:
    ${WORKSPACE_ROOT}/kpi-dashboard
    ${WORKSPACE_ROOT}/kpi-anomaly-detector
    ${WORKSPACE_ROOT}/kpi-generator
    ${WORKSPACE_ROOT}/kpi_traffic_model
  - kpi-anomaly-detector writes reports into ${DETECTOR_ROOT}/reports
  - kpi-generator still requires Compass network access and may require the Scout library path for future extensions
  - kpi-traffic-model runs attach jobs with:
    robotws=${ROBOTWS_ROOT}
    testline_configuration=${TESTLINE_ROOT}
    activate_command=${TRAFFIC_MODEL_ACTIVATE_COMMAND}
  - HTTPS is terminated by nginx. Gunicorn remains bound to 127.0.0.1:${PORTAL_PORT}
  - If no certificate is provided, the script creates a self-signed certificate at ${TLS_CERT_PATH}
  - For standalone mode on a custom external TLS port, rerun with:
    NGINX_LISTEN_PORT=your_port sudo ./deploy_debian_10.57.159.149.sh
  - To reuse an existing nginx server block, rerun with either:
    REUSE_EXISTING_NGINX_SITE=1 PUBLIC_BASE_URL=https://your-host sudo ./deploy_debian_10.57.159.149.sh
    EXISTING_NGINX_SERVER_CONF=/etc/nginx/sites-available/your-existing-site.conf PUBLIC_BASE_URL=https://your-host sudo ./deploy_debian_10.57.159.149.sh
EOF
}

main() {
  require_root
  resolve_nginx_mode
  check_layout
  normalize_runtime_config
  configure_proxy
  install_system_packages
  ensure_service_user
  setup_python_env
  prepare_runtime_dirs
  write_env_file
  write_systemd_service
  ensure_tls_assets
  write_nginx_site
  setup_scout_path
  enable_services
  configure_firewall
  verify_service
  print_summary
}

main "$@"