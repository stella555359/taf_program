from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Mapping

from flask import current_app, has_app_context


PORTAL_ROOT = Path(__file__).resolve().parents[1]
INSTANCE_ROOT = PORTAL_ROOT / 'instance'


def _parse_bool(value: str | None, default: bool) -> bool:
    cleaned = str(value or '').strip().lower()
    if not cleaned:
        return default
    return cleaned in {'1', 'true', 'yes', 'on'}


def _parse_int(value: str | None, default: int, *, minimum: int | None = None) -> int:
    cleaned = str(value or '').strip()
    if not cleaned:
        result = default
    else:
        try:
            result = int(cleaned)
        except ValueError:
            result = default
    if minimum is not None:
        result = max(result, minimum)
    return result


def _normalize_url_prefix(value: str | None) -> str:
    cleaned = str(value or '').strip()
    if not cleaned or cleaned == '/':
        return ''
    return cleaned if cleaned.startswith('/') else f'/{cleaned}'


class BaseConfig:
    dashboard_debug = False
    dashboard_host = '0.0.0.0'
    dashboard_port = 8010
    dashboard_log_level = 'INFO'
    detector_timeout_seconds = 1800
    job_store_backend = 'sqlite'
    sqlite_path = str(INSTANCE_ROOT / 'portal.db')
    compass_login_url = 'http://compass.dyn.nesc.nokia.net:8080/common/login_handle/'
    compass_template_set_url = 'http://compass.dyn.nesc.nokia.net:8080/kpi/kpi_template_set/'
    compass_template_set_timeout_seconds = 60
    compass_template_set_cache_ttl_seconds = 300


class DevConfig(BaseConfig):
    pass


class TestConfig(BaseConfig):
    dashboard_port = 8011
    dashboard_log_level = 'DEBUG'


class ProdConfig(BaseConfig):
    dashboard_log_level = 'WARNING'


CONFIG_CLASS_MAP = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
}


def _environment_name(environ: Mapping[str, str] | None = None) -> str:
    source = environ or os.environ
    cleaned = str(source.get('KPI_DASHBOARD_ENV') or '').strip().lower()
    return cleaned if cleaned in CONFIG_CLASS_MAP else 'dev'


def build_app_config(environ: Mapping[str, str] | None = None) -> dict[str, Any]:
    source = environ or os.environ
    environment_name = _environment_name(source)
    config_class = CONFIG_CLASS_MAP[environment_name]
    secret_key = str(source.get('KPI_DASHBOARD_SECRET_KEY') or '').strip()
    if not secret_key:
        if environment_name == 'prod':
            raise RuntimeError('KPI_DASHBOARD_SECRET_KEY is required when KPI_DASHBOARD_ENV=prod.')
        secret_key = 'kpi-dashboard-test-secret' if environment_name == 'test' else 'kpi-dashboard-dev-secret'

    url_prefix = _normalize_url_prefix(source.get('KPI_DASHBOARD_URL_PREFIX'))

    return {
        'KPI_DASHBOARD_ENV': environment_name,
        'KPI_DASHBOARD_HOST': str(source.get('KPI_DASHBOARD_HOST') or config_class.dashboard_host).strip() or config_class.dashboard_host,
        'KPI_DASHBOARD_PORT': _parse_int(source.get('KPI_DASHBOARD_PORT'), config_class.dashboard_port, minimum=1),
        'KPI_DASHBOARD_DEBUG': _parse_bool(source.get('KPI_DASHBOARD_DEBUG'), config_class.dashboard_debug),
        'KPI_DASHBOARD_URL_PREFIX': url_prefix,
        'KPI_DASHBOARD_LOG_LEVEL': str(source.get('KPI_DASHBOARD_LOG_LEVEL') or config_class.dashboard_log_level).strip().upper() or config_class.dashboard_log_level,
        'KPI_DASHBOARD_SECRET_KEY': secret_key,
        'KPI_JOB_STORE_BACKEND': str(source.get('KPI_JOB_STORE_BACKEND') or config_class.job_store_backend).strip().lower() or config_class.job_store_backend,
        'KPI_SQLITE_PATH': str(source.get('KPI_SQLITE_PATH') or config_class.sqlite_path).strip() or config_class.sqlite_path,
        'KPI_DETECTOR_TIMEOUT_SECONDS': _parse_int(source.get('KPI_DETECTOR_TIMEOUT_SECONDS'), config_class.detector_timeout_seconds, minimum=60),
        'KPI_DETECTOR_PYTHON': str(source.get('KPI_DETECTOR_PYTHON') or '').strip(),
        'KPI_GENERATOR_PYTHON': str(source.get('KPI_GENERATOR_PYTHON') or '').strip(),
        'COMPASS_USERNAME': str(source.get('COMPASS_USERNAME') or '').strip(),
        'COMPASS_PASSWORD': str(source.get('COMPASS_PASSWORD') or '').strip(),
        'COMPASS_LOGIN_URL': str(source.get('COMPASS_LOGIN_URL') or config_class.compass_login_url).strip() or config_class.compass_login_url,
        'COMPASS_TEMPLATE_SET_URL': str(source.get('COMPASS_TEMPLATE_SET_URL') or config_class.compass_template_set_url).strip() or config_class.compass_template_set_url,
        'COMPASS_TEMPLATE_SET_TIMEOUT_SECONDS': _parse_int(source.get('COMPASS_TEMPLATE_SET_TIMEOUT_SECONDS'), config_class.compass_template_set_timeout_seconds, minimum=5),
        'COMPASS_TEMPLATE_SET_CACHE_TTL_SECONDS': _parse_int(source.get('COMPASS_TEMPLATE_SET_CACHE_TTL_SECONDS'), config_class.compass_template_set_cache_ttl_seconds, minimum=0),
        'APPLICATION_ROOT': url_prefix or '/',
        'SECRET_KEY': secret_key,
    }


def get_config_value(name: str, default: Any = None) -> Any:
    if has_app_context():
        return current_app.config.get(name, default)
    return build_app_config().get(name, default)


def configure_logging(config: Mapping[str, Any]) -> None:
    level_name = str(config.get('KPI_DASHBOARD_LOG_LEVEL') or 'INFO').upper()
    level = getattr(logging, level_name, logging.INFO)
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        logging.basicConfig(level=level, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    root_logger.setLevel(level)