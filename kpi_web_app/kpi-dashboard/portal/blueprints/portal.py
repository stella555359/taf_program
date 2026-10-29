from __future__ import annotations

from flask import Blueprint, jsonify, render_template

from ..config import get_config_value
from ..services.job_store import ensure_runtime_dirs
from ..services.repo_registry import get_module_cards


portal_bp = Blueprint('portal', __name__)


@portal_bp.get('/')
def home():
    return render_template('home.html', modules=get_module_cards())


@portal_bp.get('/healthz')
def healthz():
    ensure_runtime_dirs()
    return jsonify(
        {
            'status': 'ok',
            'service': 'kpi-dashboard',
            'job_store_backend': str(get_config_value('KPI_JOB_STORE_BACKEND', 'sqlite') or 'sqlite'),
        }
    )