from __future__ import annotations

from typing import Any, Dict

from flask import Flask

from .adapters.kpi_detector import get_kpi_detector_adapter
from .adapters.kpi_generator import get_kpi_generator_adapter
from .blueprints import kpi_detector_bp, kpi_generator_bp, kpi_traffic_model_bp, portal_bp
from .config import build_app_config, configure_logging
from .services.job_store import ensure_runtime_dirs
from .services.repo_registry import get_module_cards


class PrefixMiddleware:
    def __init__(self, app, prefix: str):
        self.app = app
        self.prefix = prefix.rstrip('/') if prefix and prefix != '/' else ''

    def __call__(self, environ, start_response):
        if not self.prefix:
            return self.app(environ, start_response)

        path_info = environ.get('PATH_INFO', '') or ''
        if path_info.startswith(self.prefix):
            environ['SCRIPT_NAME'] = self.prefix
            trimmed = path_info[len(self.prefix):]
            environ['PATH_INFO'] = trimmed or '/'
            return self.app(environ, start_response)

        if environ.get('HTTP_X_SCRIPT_NAME') == self.prefix or environ.get('HTTP_X_FORWARDED_PREFIX') == self.prefix:
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)

        start_response('404 Not Found', [('Content-Type', 'text/plain; charset=utf-8')])
        return [b'Not Found']


def _recover_startup_jobs(app: Flask) -> None:
    try:
        get_kpi_generator_adapter().recover_startup_jobs()
    except Exception:
        app.logger.exception('Generator startup recovery failed.')

    try:
        get_kpi_detector_adapter().recover_startup_jobs()
    except Exception:
        app.logger.exception('Detector startup recovery failed.')


def create_app() -> Flask:
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.update(build_app_config())
    configure_logging(app.config)
    ensure_runtime_dirs()
    url_prefix = str(app.config.get('KPI_DASHBOARD_URL_PREFIX') or '')

    @app.context_processor
    def inject_portal_state() -> Dict[str, Any]:
        return {
            'module_cards': get_module_cards(),
        }

    app.register_blueprint(portal_bp)
    app.register_blueprint(kpi_detector_bp)
    app.register_blueprint(kpi_generator_bp)
    app.register_blueprint(kpi_traffic_model_bp)

    _recover_startup_jobs(app)

    if url_prefix:
        app.wsgi_app = PrefixMiddleware(app.wsgi_app, url_prefix)

    return app