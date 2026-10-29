#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

APP_USER="${APP_USER:-ute}"
APP_GROUP="${APP_GROUP:-$APP_USER}"
APP_DIR="${APP_DIR:-/home/$APP_USER/kpi-anomaly-detector}"
APP_HOST="${APP_HOST:-10.57.159.149}"
APP_PORT="${APP_PORT:-8088}"
PUBLIC_PORT="${PUBLIC_PORT:-8088}"
SKIP_NGINX="${SKIP_NGINX:-1}"
USE_PROXY="${USE_PROXY:-1}"
PIP_PROXY_URL="${PIP_PROXY_URL:-http://10.158.100.9:8080}"

export APP_USER
export APP_GROUP
export APP_DIR
export APP_HOST
export APP_PORT
export PUBLIC_PORT
export SKIP_NGINX
export USE_PROXY
export PIP_PROXY_URL

exec "$SCRIPT_DIR/deploy_web_dashboard.sh"