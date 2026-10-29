#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/home/ute/kpi-anomaly-detector}"
APP_USER="${APP_USER:-ute}"
APP_GROUP="${APP_GROUP:-$APP_USER}"
APP_HOST="${APP_HOST:-10.21.41.175}"
APP_PORT="${APP_PORT:-8000}"
PUBLIC_PORT="${PUBLIC_PORT:-80}"
APP_SECRET="${APP_SECRET:-change-this-secret}"
APP_USERNAME="${APP_USERNAME:-}"
APP_PASSWORD="${APP_PASSWORD:-}"
APP_ALLOWED_IPS="${APP_ALLOWED_IPS:-}"
SKIP_NGINX="${SKIP_NGINX:-0}"
USE_PROXY="${USE_PROXY:-0}"
PIP_PROXY_URL="${PIP_PROXY_URL:-http://10.158.100.9:8080}"

if [[ ! -d "$APP_DIR" ]]; then
    echo "Application directory not found: $APP_DIR" >&2
    exit 1
fi

export DEBIAN_FRONTEND=noninteractive

sudo apt update
if [[ "$SKIP_NGINX" == "1" ]]; then
    sudo apt install -y python3 python3-venv python3-pip apache2-utils
else
    sudo apt install -y python3 python3-venv python3-pip nginx apache2-utils
fi

cd "$APP_DIR"

if [[ ! -d .venv ]]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip

if [[ "$USE_PROXY" == "1" ]]; then
    pip install --proxy "$PIP_PROXY_URL" -r requirements-web.txt
else
    pip install -r requirements-web.txt
fi

cat > /tmp/kpi-web.service <<EOF
[Unit]
Description=KPI Detector Web Dashboard
After=network.target

[Service]
User=$APP_USER
Group=$APP_GROUP
WorkingDirectory=$APP_DIR
Environment=KPI_WEB_HOST=0.0.0.0
Environment=KPI_WEB_PORT=$APP_PORT
Environment=KPI_WEB_SECRET=$APP_SECRET
EOF

if [[ -n "$APP_USERNAME" ]]; then
    printf 'Environment=KPI_WEB_USERNAME=%s\n' "$APP_USERNAME" >> /tmp/kpi-web.service
fi

if [[ -n "$APP_PASSWORD" ]]; then
    printf 'Environment=KPI_WEB_PASSWORD=%s\n' "$APP_PASSWORD" >> /tmp/kpi-web.service
fi

if [[ -n "$APP_ALLOWED_IPS" ]]; then
    printf 'Environment=KPI_WEB_ALLOWED_IPS=%s\n' "$APP_ALLOWED_IPS" >> /tmp/kpi-web.service
fi

cat >> /tmp/kpi-web.service <<EOF
ExecStart=$APP_DIR/.venv/bin/gunicorn -w 2 -b 0.0.0.0:$APP_PORT webapp.wsgi:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo mv /tmp/kpi-web.service /etc/systemd/system/kpi-web.service

if [[ "$SKIP_NGINX" != "1" ]]; then
    cat > /tmp/kpi-web-nginx <<EOF
server {
    listen $PUBLIC_PORT;
    server_name $APP_HOST;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:$APP_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

    sudo mv /tmp/kpi-web-nginx /etc/nginx/sites-available/kpi-web
    sudo ln -sf /etc/nginx/sites-available/kpi-web /etc/nginx/sites-enabled/kpi-web
    sudo nginx -t
fi

sudo systemctl daemon-reload
sudo systemctl enable --now kpi-web

if [[ "$SKIP_NGINX" != "1" ]]; then
    sudo systemctl reload nginx
fi

echo "Deployment complete"
if [[ "$SKIP_NGINX" == "1" ]]; then
    echo "App URL: http://$APP_HOST:$APP_PORT"
else
    echo "App URL: http://$APP_HOST:$PUBLIC_PORT"
fi
echo "Service status command: sudo systemctl status kpi-web"