from __future__ import annotations

from flask import Blueprint, redirect, render_template, url_for

from ..services.kpi_analysis_service import APP_DATA_DIR, DB_PATH, REPORT_DIR, build_portal_overview


portal_bp = Blueprint('portal', __name__)


@portal_bp.get('/')
def home():
    return render_template('portal_home.html', overview=build_portal_overview())


@portal_bp.get('/dashboard')
def dashboard_redirect():
    return redirect(url_for('kpi.index'))


@portal_bp.get('/healthz')
def healthz():
    return {'status': 'ok', 'reports_dir': str(REPORT_DIR), 'db_path': str(DB_PATH), 'app_data_dir': str(APP_DATA_DIR)}