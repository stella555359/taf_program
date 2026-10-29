from __future__ import annotations

import json
import os
import sqlite3
import sys
import threading
import traceback
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from flask import abort, request, url_for
from werkzeug.utils import secure_filename

BASE_DIR = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = BASE_DIR / 'scripts'

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from kpi_detector import KPIAnomalyDetector, PATHS  # noqa: E402
from kpi_detector.utils import extract_history_context, extract_history_context_from_record  # noqa: E402


APP_DATA_DIR = BASE_DIR / 'webapp_data'
UPLOAD_DIR = APP_DATA_DIR / 'uploads'
REPORT_DIR = APP_DATA_DIR / 'reports'
DB_PATH = APP_DATA_DIR / 'analysis_history.db'
HISTORY_JSON_PATH = REPORT_DIR / 'kpi_history_records.json'
MAX_UPLOAD_SIZE = 100 * 1024 * 1024
ALLOWED_EXTENSIONS = {'.xlsx'}
STATUS_ACTIVE = {'queued', 'running'}
ANALYSIS_LOCK = threading.Lock()
DEFAULT_PAGE_SIZE = 50


def init_storage() -> None:
    for directory in (APP_DATA_DIR, UPLOAD_DIR, REPORT_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    PATHS['reports'] = REPORT_DIR
    init_db()


def utcnow_text() -> str:
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            '''
            CREATE TABLE IF NOT EXISTS analyses (
                id TEXT PRIMARY KEY,
                original_filename TEXT NOT NULL,
                uploader_username TEXT NOT NULL DEFAULT 'anonymous',
                stored_filename TEXT NOT NULL,
                upload_path TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT,
                report_html_path TEXT,
                report_excel_path TEXT,
                stats_json TEXT,
                record_json TEXT,
                error_message TEXT,
                hidden INTEGER NOT NULL DEFAULT 0
            )
            '''
        )

        columns = {
            row['name']
            for row in connection.execute('PRAGMA table_info(analyses)').fetchall()
        }
        if 'hidden' not in columns:
            connection.execute('ALTER TABLE analyses ADD COLUMN hidden INTEGER NOT NULL DEFAULT 0')
        if 'uploader_username' not in columns:
            connection.execute("ALTER TABLE analyses ADD COLUMN uploader_username TEXT NOT NULL DEFAULT 'anonymous'")


def build_history_context(analysis: Dict[str, Any]) -> Dict[str, Any]:
    context = extract_history_context_from_record(analysis.get('record', {}))
    if context is None:
        context = extract_history_context(analysis.get('original_filename', ''))
    if context is None:
        context = extract_history_context(analysis.get('stored_filename', ''))
    return context or {}


def row_to_analysis(row: Optional[sqlite3.Row]) -> Optional[Dict[str, Any]]:
    if row is None:
        return None

    analysis = dict(row)
    analysis['stats'] = json.loads(analysis['stats_json']) if analysis.get('stats_json') else {}
    analysis['record'] = json.loads(analysis['record_json']) if analysis.get('record_json') else {}
    analysis['history_context'] = build_history_context(analysis)
    analysis['history_context_failed'] = not bool(analysis['history_context'].get('history_key'))
    return analysis


def serialize_analysis(analysis: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if analysis is None:
        return None

    return {
        'id': analysis['id'],
        'original_filename': analysis['original_filename'],
        'uploader_username': analysis.get('uploader_username', 'anonymous'),
        'history_context': analysis.get('history_context', {}),
        'status': analysis['status'],
        'created_at': analysis['created_at'],
        'started_at': analysis.get('started_at'),
        'completed_at': analysis.get('completed_at'),
        'error_message': analysis.get('error_message'),
        'hidden': bool(analysis.get('hidden', 0)),
        'stats': analysis.get('stats', {}),
        'has_html_report': bool(analysis.get('report_html_path')),
        'has_excel_report': bool(analysis.get('report_excel_path')),
        'html_url': url_for('kpi.analysis_artifact', analysis_id=analysis['id'], artifact_kind='html') if analysis.get('report_html_path') else None,
        'excel_url': url_for('kpi.analysis_artifact', analysis_id=analysis['id'], artifact_kind='excel') if analysis.get('report_excel_path') else None,
    }


def get_allowed_ips() -> set[str]:
    raw_value = os.environ.get('KPI_WEB_ALLOWED_IPS', '')
    return {item.strip() for item in raw_value.split(',') if item.strip()}


def get_request_ip() -> str:
    forwarded_for = request.headers.get('X-Forwarded-For', '')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.remote_addr or ''


def get_request_user_label() -> str:
    auth = request.authorization
    if auth and auth.username:
        return auth.username

    forwarded_user = request.headers.get('X-Forwarded-User', '').strip()
    if forwarded_user:
        return forwarded_user

    request_ip = get_request_ip()
    if request_ip:
        return request_ip

    return 'anonymous'


def build_search_pattern(search_query: str) -> Optional[str]:
    cleaned = search_query.strip()
    if not cleaned:
        return None
    return f'%{cleaned}%'


def normalize_filter_text(raw_value: str) -> str:
    return (raw_value or '').strip().lower()


def matches_history_filters(
    analysis: Dict[str, Any],
    environment_query: str = '',
    scenario_query: str = '',
) -> bool:
    history_context = analysis.get('history_context', {})
    environment_text = str(history_context.get('environment') or '').lower()
    scenario_text = str(history_context.get('scenario') or '').lower()
    history_key_text = str(history_context.get('history_key') or '').lower()

    normalized_environment = normalize_filter_text(environment_query)
    normalized_scenario = normalize_filter_text(scenario_query)

    if normalized_environment and normalized_environment not in environment_text:
        return False
    if normalized_scenario:
        if normalized_scenario not in scenario_text and normalized_scenario not in history_key_text:
            return False
    return True


def parse_page_number(raw_value: str) -> int:
    try:
        page_number = int(raw_value)
    except (TypeError, ValueError):
        return 1
    return max(page_number, 1)


def get_sort_config(sort_key: str, sort_order: str) -> tuple[str, str, str]:
    normalized_key = 'created'
    normalized_order = sort_order if sort_order in {'asc', 'desc'} else 'desc'

    sort_columns = {
        'created': 'datetime(created_at)',
    }
    sort_expression = (
        f"{sort_columns[normalized_key]} {'ASC' if normalized_order == 'asc' else 'DESC'}, "
        'datetime(created_at) DESC'
    )
    return normalized_key, normalized_order, sort_expression


def build_index_params(
    search_query: str = '',
    environment_query: str = '',
    scenario_query: str = '',
    sort_key: str = 'created',
    sort_order: str = 'desc',
    page: int = 1,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {
        'sort': sort_key,
        'order': sort_order,
    }
    if search_query:
        params['q'] = search_query
    if environment_query:
        params['env'] = environment_query
    if scenario_query:
        params['scenario'] = scenario_query
    if page > 1:
        params['page'] = page
    return params


def query_analyses(
    hidden: bool,
    search_query: str = '',
    sort_key: str = 'created',
    sort_order: str = 'desc',
) -> list[Dict[str, Any]]:
    search_pattern = build_search_pattern(search_query)
    _, _, sort_expression = get_sort_config(sort_key, sort_order)
    hidden_value = 1 if hidden else 0

    with get_connection() as connection:
        if search_pattern:
            rows = connection.execute(
                f'''
                SELECT *
                FROM analyses
                WHERE hidden = ?
                  AND original_filename LIKE ?
                ORDER BY {sort_expression}, rowid DESC
                ''',
                (hidden_value, search_pattern),
            ).fetchall()
        else:
            rows = connection.execute(
                f'''
                SELECT *
                FROM analyses
                WHERE hidden = ?
                ORDER BY {sort_expression}, rowid DESC
                ''',
                (hidden_value,),
            ).fetchall()

    return [row_to_analysis(row) for row in rows]


def query_filtered_visible_analyses(
    search_query: str = '',
    environment_query: str = '',
    scenario_query: str = '',
    sort_key: str = 'created',
    sort_order: str = 'desc',
) -> list[Dict[str, Any]]:
    analyses = query_analyses(
        hidden=False,
        search_query=search_query,
        sort_key=sort_key,
        sort_order=sort_order,
    )
    return [
        item for item in analyses
        if matches_history_filters(item, environment_query, scenario_query)
    ]


def list_analyses(
    limit: int = 50,
    offset: int = 0,
    search_query: str = '',
    environment_query: str = '',
    scenario_query: str = '',
    sort_key: str = 'created',
    sort_order: str = 'desc',
) -> list[Dict[str, Any]]:
    analyses = query_filtered_visible_analyses(
        search_query=search_query,
        environment_query=environment_query,
        scenario_query=scenario_query,
        sort_key=sort_key,
        sort_order=sort_order,
    )
    return analyses[offset:offset + limit]


def list_hidden_analyses(
    limit: int = 50,
    search_query: str = '',
    environment_query: str = '',
    scenario_query: str = '',
    sort_key: str = 'created',
    sort_order: str = 'desc',
) -> list[Dict[str, Any]]:
    analyses = query_analyses(
        hidden=True,
        search_query=search_query,
        sort_key=sort_key,
        sort_order=sort_order,
    )
    filtered = [
        item for item in analyses
        if matches_history_filters(item, environment_query, scenario_query)
    ]
    return filtered[:limit]


def count_hidden_analyses(
    search_query: str = '',
    environment_query: str = '',
    scenario_query: str = '',
) -> int:
    return len(list_hidden_analyses(
        limit=1000000,
        search_query=search_query,
        environment_query=environment_query,
        scenario_query=scenario_query,
    ))


def count_visible_analyses(
    search_query: str = '',
    environment_query: str = '',
    scenario_query: str = '',
) -> int:
    return len(query_filtered_visible_analyses(search_query, environment_query, scenario_query))


def count_all_analyses() -> int:
    with get_connection() as connection:
        row = connection.execute('SELECT COUNT(*) AS total_count FROM analyses').fetchone()
    return int(row['total_count']) if row else 0


def count_active_analyses() -> int:
    with get_connection() as connection:
        row = connection.execute(
            f"SELECT COUNT(*) AS active_count FROM analyses WHERE hidden = 0 AND status IN ({','.join('?' for _ in STATUS_ACTIVE)})",
            tuple(STATUS_ACTIVE),
        ).fetchone()
    return int(row['active_count']) if row else 0


def get_history_filter_options() -> Dict[str, list[str]]:
    analyses = query_analyses(hidden=False) + query_analyses(hidden=True)
    environments = sorted({
        str(item.get('history_context', {}).get('environment')).strip()
        for item in analyses
        if item.get('history_context', {}).get('environment')
    })
    scenarios = sorted({
        str(item.get('history_context', {}).get('scenario')).strip()
        for item in analyses
        if item.get('history_context', {}).get('scenario')
    })
    return {
        'environments': environments,
        'scenarios': scenarios,
    }


def get_analysis(analysis_id: str) -> Optional[Dict[str, Any]]:
    with get_connection() as connection:
        row = connection.execute(
            'SELECT * FROM analyses WHERE id = ?',
            (analysis_id,),
        ).fetchone()

    return row_to_analysis(row)


def create_analysis_record(
    analysis_id: str,
    original_filename: str,
    uploader_username: str,
    stored_filename: str,
    upload_path: Path,
) -> None:
    with get_connection() as connection:
        connection.execute(
            '''
            INSERT INTO analyses (
                id, original_filename, uploader_username, stored_filename, upload_path, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                analysis_id,
                original_filename,
                uploader_username,
                stored_filename,
                str(upload_path),
                'queued',
                utcnow_text(),
            ),
        )


def update_analysis(analysis_id: str, **fields: Any) -> None:
    if not fields:
        return

    columns = ', '.join(f'{key} = ?' for key in fields)
    values = list(fields.values())
    values.append(analysis_id)

    with get_connection() as connection:
        connection.execute(
            f'UPDATE analyses SET {columns} WHERE id = ?',
            values,
        )


def delete_analysis_row(analysis_id: str) -> None:
    with get_connection() as connection:
        connection.execute('DELETE FROM analyses WHERE id = ?', (analysis_id,))


def set_hidden_state(analysis_id: str, hidden: bool) -> None:
    with get_connection() as connection:
        connection.execute(
            'UPDATE analyses SET hidden = ? WHERE id = ?',
            (1 if hidden else 0, analysis_id),
        )


def is_allowed_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def build_stored_filename(original_filename: str) -> str:
    safe_name = secure_filename(original_filename) or 'upload.xlsx'
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    return f'{timestamp}_{uuid.uuid4().hex[:8]}_{safe_name}'


def resolve_artifact_path(raw_path: Optional[str]) -> Optional[Path]:
    if not raw_path:
        return None

    resolved = Path(raw_path).resolve()
    reports_root = REPORT_DIR.resolve()
    if not resolved.is_file() or not resolved.is_relative_to(reports_root):
        return None
    return resolved


def resolve_report_data_path(raw_path: Optional[str]) -> Optional[Path]:
    html_path = resolve_artifact_path(raw_path)
    if html_path is None:
        return None

    candidate = html_path.with_name(f'{html_path.stem}_data.js').resolve()
    reports_root = REPORT_DIR.resolve()
    if not candidate.is_file() or not candidate.is_relative_to(reports_root):
        return None
    return candidate


def resolve_upload_path(raw_path: Optional[str]) -> Optional[Path]:
    if not raw_path:
        return None

    resolved = Path(raw_path).resolve()
    uploads_root = UPLOAD_DIR.resolve()
    if not resolved.exists() or not resolved.is_relative_to(uploads_root):
        return None
    return resolved


def safe_unlink(path: Optional[Path]) -> None:
    if path is None:
        return
    try:
        if path.exists() and path.is_file():
            path.unlink()
    except OSError:
        pass


def delete_history_record(stored_filename: Optional[str]) -> None:
    if not stored_filename or not HISTORY_JSON_PATH.exists():
        return

    try:
        with HISTORY_JSON_PATH.open('r', encoding='utf-8') as handle:
            records = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return

    filtered_records = [row for row in records if row.get('filename') != stored_filename]
    if len(filtered_records) == len(records):
        return

    try:
        with HISTORY_JSON_PATH.open('w', encoding='utf-8') as handle:
            json.dump(filtered_records, handle, ensure_ascii=False, indent=2)
    except OSError:
        return


def delete_analysis_bundle(analysis: Dict[str, Any]) -> None:
    safe_unlink(resolve_upload_path(analysis.get('upload_path')))
    safe_unlink(resolve_artifact_path(analysis.get('report_html_path')))
    safe_unlink(resolve_artifact_path(analysis.get('report_excel_path')))
    delete_history_record(analysis.get('stored_filename'))
    delete_analysis_row(analysis['id'])


def soft_delete_analysis_bundle(analysis: Dict[str, Any]) -> None:
    set_hidden_state(analysis['id'], True)


def restore_analysis_bundle(analysis: Dict[str, Any]) -> None:
    set_hidden_state(analysis['id'], False)


def clear_analysis_artifacts(analysis: Dict[str, Any]) -> None:
    safe_unlink(resolve_artifact_path(analysis.get('report_html_path')))
    safe_unlink(resolve_report_data_path(analysis.get('report_html_path')))
    safe_unlink(resolve_artifact_path(analysis.get('report_excel_path')))


def queue_analysis_rerun(analysis: Dict[str, Any]) -> None:
    upload_path = resolve_upload_path(analysis.get('upload_path'))
    if upload_path is None:
        raise FileNotFoundError('Original uploaded file is missing.')

    clear_analysis_artifacts(analysis)
    update_analysis(
        analysis['id'],
        status='queued',
        started_at=None,
        completed_at=None,
        report_html_path=None,
        report_excel_path=None,
        stats_json=None,
        record_json=None,
        error_message=None,
    )
    start_analysis_job(analysis['id'])


def build_kpi_dashboard_context(
    search_query: str = '',
    environment_query: str = '',
    scenario_query: str = '',
    requested_page: int = 1,
    requested_sort: str = 'created',
    requested_order: str = 'desc',
) -> Dict[str, Any]:
    page = parse_page_number(str(requested_page))
    sort_key, sort_order, _ = get_sort_config(requested_sort, requested_order)
    total_visible = count_visible_analyses(
        search_query=search_query,
        environment_query=environment_query,
        scenario_query=scenario_query,
    )
    total_pages = max((total_visible + DEFAULT_PAGE_SIZE - 1) // DEFAULT_PAGE_SIZE, 1)
    current_page = min(page, total_pages)
    offset = (current_page - 1) * DEFAULT_PAGE_SIZE

    analyses = list_analyses(
        limit=DEFAULT_PAGE_SIZE,
        offset=offset,
        search_query=search_query,
        environment_query=environment_query,
        scenario_query=scenario_query,
        sort_key=sort_key,
        sort_order=sort_order,
    )
    hidden_analyses = list_hidden_analyses(
        limit=20,
        search_query=search_query,
        environment_query=environment_query,
        scenario_query=scenario_query,
        sort_key=sort_key,
        sort_order=sort_order,
    )
    hidden_count = count_hidden_analyses(
        search_query=search_query,
        environment_query=environment_query,
        scenario_query=scenario_query,
    )
    active_analysis_count = count_active_analyses()
    filter_options = get_history_filter_options()

    return {
        'analyses': analyses,
        'hidden_analyses': hidden_analyses,
        'hidden_count': hidden_count,
        'search_query': search_query,
        'environment_query': environment_query,
        'scenario_query': scenario_query,
        'environment_options': filter_options['environments'],
        'scenario_options': filter_options['scenarios'],
        'sort_key': sort_key,
        'sort_order': sort_order,
        'current_page': current_page,
        'total_pages': total_pages,
        'total_visible': total_visible,
        'page_start': offset + 1 if total_visible else 0,
        'page_end': offset + len(analyses),
        'has_active_jobs': active_analysis_count > 0,
        'active_analysis_count': active_analysis_count,
    }


def build_portal_overview() -> Dict[str, Any]:
    visible_count = count_visible_analyses()
    hidden_count = count_hidden_analyses()
    active_count = count_active_analyses()
    total_count = count_all_analyses()
    recent_runs = list_analyses(limit=6, offset=0)
    return {
        'visible_count': visible_count,
        'hidden_count': hidden_count,
        'active_count': active_count,
        'total_count': total_count,
        'recent_runs': recent_runs,
    }


def redirect_to_kpi_index(
    search_query: str = '',
    environment_query: str = '',
    scenario_query: str = '',
    sort_key: str = 'created',
    sort_order: str = 'desc',
    page: int = 1,
    anchor: str = 'page-top',
):
    target_anchor = anchor.strip() or 'page-top'
    return url_for(
        'kpi.index',
        **build_index_params(search_query, environment_query, scenario_query, sort_key, sort_order, page),
    ) + f'#{target_anchor}'


def get_analysis_or_404(analysis_id: str) -> Dict[str, Any]:
    analysis = get_analysis(analysis_id)
    if analysis is None:
        abort(404)
    return analysis


def run_analysis_job(analysis_id: str) -> None:
    analysis = get_analysis(analysis_id)
    if analysis is None:
        return

    update_analysis(analysis_id, status='running', started_at=utcnow_text(), error_message=None)

    try:
        upload_path = Path(analysis['upload_path'])

        with ANALYSIS_LOCK:
            detector = KPIAnomalyDetector(str(upload_path))
            excel_report_path = detector.run(generate_html=True)
            report_files = detector.last_report_files
            current_record = detector.last_current_record or detector.build_current_record()

        stats = current_record.get('stats', {})
        html_report_path = report_files.get('html')
        excel_report_path = report_files.get('excel') or excel_report_path

        update_analysis(
            analysis_id,
            status='completed',
            completed_at=utcnow_text(),
            report_html_path=str(html_report_path) if html_report_path else None,
            report_excel_path=str(excel_report_path) if excel_report_path else None,
            stats_json=json.dumps(stats, ensure_ascii=False),
            record_json=json.dumps(current_record, ensure_ascii=False),
            error_message=None,
        )
    except Exception as exc:
        traceback.print_exc()
        update_analysis(
            analysis_id,
            status='failed',
            completed_at=utcnow_text(),
            error_message=f'{type(exc).__name__}: {exc}',
        )


def start_analysis_job(analysis_id: str) -> None:
    worker = threading.Thread(target=run_analysis_job, args=(analysis_id,), daemon=True)
    worker.start()