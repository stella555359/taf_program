from __future__ import annotations

import re
import os
from base64 import b64decode
from hmac import compare_digest
from typing import Any, Dict

from flask import Flask, abort, flash, redirect, request, url_for
from markupsafe import Markup, escape
from werkzeug.exceptions import RequestEntityTooLarge

from .blueprints import kpi_bp, portal_bp
from .services.kpi_analysis_service import MAX_UPLOAD_SIZE, STATUS_ACTIVE, get_allowed_ips, get_request_ip, init_storage


def is_authorized() -> bool:
    username = os.environ.get('KPI_WEB_USERNAME')
    password = os.environ.get('KPI_WEB_PASSWORD')
    if not username or not password:
        return True

    auth = request.authorization
    if auth is None and 'Authorization' in request.headers:
        header_value = request.headers.get('Authorization', '')
        if header_value.startswith('Basic '):
            try:
                decoded = b64decode(header_value.split(' ', 1)[1]).decode('utf-8')
                supplied_username, supplied_password = decoded.split(':', 1)
                return compare_digest(supplied_username, username) and compare_digest(supplied_password, password)
            except Exception:
                return False

    if auth is None:
        return False

    return compare_digest(auth.username or '', username) and compare_digest(auth.password or '', password)


def unauthorized_response():
    return (
        'Authentication required',
        401,
        {'WWW-Authenticate': 'Basic realm="KPI Portal"'},
    )


def create_app() -> Flask:
    init_storage()

    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SECRET_KEY'] = os.environ.get('KPI_WEB_SECRET', 'kpi-web-secret')
    app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_SIZE

    @app.before_request
    def enforce_access_controls():
        if request.endpoint == 'portal.healthz':
            return None

        allowed_ips = get_allowed_ips()
        if allowed_ips and get_request_ip() not in allowed_ips:
            abort(403)

        if not is_authorized():
            return unauthorized_response()

        return None

    @app.errorhandler(RequestEntityTooLarge)
    def handle_request_too_large(_error):
        flash('Upload failed: file is larger than 100 MB.', 'error')
        return redirect(url_for('kpi.index'))

    @app.context_processor
    def inject_state() -> Dict[str, Any]:
        return {
            'active_statuses': STATUS_ACTIVE,
        }

    @app.template_filter('highlight_match')
    def highlight_match(value: Any, search_query: str = ''):
        text = '' if value is None else str(value)
        query = search_query.strip()
        if not query:
            return escape(text)

        pattern = re.compile(re.escape(query), re.IGNORECASE)
        parts: list[Any] = []
        last_index = 0
        for match in pattern.finditer(text):
            parts.append(escape(text[last_index:match.start()]))
            parts.append(Markup(f'<mark class="match-highlight">{escape(match.group(0))}</mark>'))
            last_index = match.end()
        parts.append(escape(text[last_index:]))
        return Markup('').join(parts)

    app.register_blueprint(portal_bp)
    app.register_blueprint(kpi_bp)

    return app