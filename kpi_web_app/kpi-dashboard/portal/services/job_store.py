from __future__ import annotations

import json
import math
import shutil
import sqlite3
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from ..config import get_config_value


PORTAL_ROOT = Path(__file__).resolve().parents[2]
INSTANCE_ROOT = PORTAL_ROOT / 'instance'
JOBS_ROOT = INSTANCE_ROOT / 'jobs'


def utcnow_text() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')


def next_queue_order() -> int:
    return time.time_ns()


def _job_list_sort_key(job: Dict[str, Any]) -> tuple[int, int, str, int, str]:
    batch_order = int(job.get('submission_batch_order') or job.get('queue_order') or 0)
    submission_index = int(job.get('submission_index') or 0)
    queue_order = int(job.get('queue_order') or 0)
    created_at = str(job.get('created_at') or '')
    job_id = str(job.get('id') or '')
    return (batch_order, submission_index, created_at, queue_order, job_id)


def parse_utc_text(value: str | None) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _job_store_backend() -> str:
    return str(get_config_value('KPI_JOB_STORE_BACKEND', 'sqlite') or 'sqlite').strip().lower()


def _using_sqlite_backend() -> bool:
    return _job_store_backend() == 'sqlite'


def _sqlite_db_path() -> Path:
    configured = str(get_config_value('KPI_SQLITE_PATH', str(INSTANCE_ROOT / 'portal.db')) or '').strip()
    return Path(configured) if configured else (INSTANCE_ROOT / 'portal.db')


def _atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f'{path.name}.{uuid.uuid4().hex}.tmp')
    temp_path.write_text(content, encoding='utf-8')
    temp_path.replace(path)


@contextmanager
def _sqlite_connection() -> Iterator[sqlite3.Connection]:
    db_path = _sqlite_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def _ensure_sqlite_schema() -> None:
    with _sqlite_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                module_key TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                queue_order INTEGER NOT NULL,
                job_json TEXT NOT NULL
            )
            """
        )
        connection.execute('CREATE INDEX IF NOT EXISTS idx_jobs_module_created ON jobs(module_key, created_at DESC)')
        connection.execute('CREATE INDEX IF NOT EXISTS idx_jobs_module_status ON jobs(module_key, status)')
        connection.execute('CREATE INDEX IF NOT EXISTS idx_jobs_module_queue_order ON jobs(module_key, queue_order)')
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS job_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_key TEXT NOT NULL,
                job_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                created_at TEXT NOT NULL,
                event_json TEXT NOT NULL
            )
            """
        )
        connection.execute('CREATE INDEX IF NOT EXISTS idx_job_events_lookup ON job_events(module_key, job_id, created_at DESC)')
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS job_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_key TEXT NOT NULL,
                job_id TEXT NOT NULL,
                link_kind TEXT NOT NULL,
                linked_module_key TEXT NOT NULL,
                linked_job_id TEXT NOT NULL,
                link_json TEXT NOT NULL
            )
            """
        )
        connection.execute('CREATE INDEX IF NOT EXISTS idx_job_links_lookup ON job_links(module_key, job_id)')
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS job_artifacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                module_key TEXT NOT NULL,
                job_id TEXT NOT NULL,
                artifact_kind TEXT NOT NULL,
                artifact_path TEXT NOT NULL,
                artifact_json TEXT NOT NULL
            )
            """
        )
        connection.execute('CREATE INDEX IF NOT EXISTS idx_job_artifacts_lookup ON job_artifacts(module_key, job_id)')


def ensure_runtime_dirs() -> None:
    for path in (INSTANCE_ROOT, JOBS_ROOT):
        path.mkdir(parents=True, exist_ok=True)
    if _using_sqlite_backend():
        _ensure_sqlite_schema()


def module_jobs_root(module_key: str) -> Path:
    ensure_runtime_dirs()
    root = JOBS_ROOT / module_key
    root.mkdir(parents=True, exist_ok=True)
    return root


def job_root(module_key: str, job_id: str) -> Path:
    root = module_jobs_root(module_key) / job_id
    root.mkdir(parents=True, exist_ok=True)
    return root


def job_metadata_path(module_key: str, job_id: str) -> Path:
    return job_root(module_key, job_id) / 'job.json'


def _save_job_file(module_key: str, job: Dict[str, Any]) -> None:
    _atomic_write_text(
        job_metadata_path(module_key, str(job['id'])),
        json.dumps(job, ensure_ascii=False, indent=2),
    )


def _load_job_file(module_key: str, job_id: str) -> Optional[Dict[str, Any]]:
    path = job_metadata_path(module_key, job_id)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding='utf-8'))


def _save_job_sqlite(module_key: str, job: Dict[str, Any]) -> None:
    ensure_runtime_dirs()
    with _sqlite_connection() as connection:
        previous_row = connection.execute(
            'SELECT job_json FROM jobs WHERE module_key = ? AND id = ?',
            (module_key, str(job['id'])),
        ).fetchone()
        previous_job = json.loads(str(previous_row['job_json'])) if previous_row is not None else None
        next_links = _derive_job_links(job)
        next_artifacts = _derive_job_artifacts(job)
        connection.execute(
            """
            INSERT INTO jobs (id, module_key, status, created_at, queue_order, job_json)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                module_key=excluded.module_key,
                status=excluded.status,
                created_at=excluded.created_at,
                queue_order=excluded.queue_order,
                job_json=excluded.job_json
            """,
            (
                str(job['id']),
                module_key,
                str(job.get('status') or 'queued'),
                str(job.get('created_at') or utcnow_text()),
                int(job.get('queue_order') or next_queue_order()),
                json.dumps(job, ensure_ascii=False),
            ),
        )
        _replace_job_links_sqlite(connection, module_key, str(job['id']), next_links)
        _replace_job_artifacts_sqlite(connection, module_key, str(job['id']), next_artifacts)
        for event in _derive_job_events(previous_job, job, next_links, next_artifacts):
            _append_job_event_sqlite(connection, module_key, str(job['id']), str(event['event_type']), dict(event['payload']))


def _load_job_sqlite(module_key: str, job_id: str) -> Optional[Dict[str, Any]]:
    ensure_runtime_dirs()
    with _sqlite_connection() as connection:
        row = connection.execute(
            'SELECT job_json FROM jobs WHERE module_key = ? AND id = ?',
            (module_key, job_id),
        ).fetchone()
    if row is None:
        return None
    return json.loads(str(row['job_json']))


def create_job(module_key: str, original_filename: str, stored_filename: str, *, is_base_file: bool = False) -> Dict[str, Any]:
    job_id = uuid.uuid4().hex
    root = job_root(module_key, job_id)
    job = {
        'id': job_id,
        'module_key': module_key,
        'original_filename': original_filename,
        'stored_filename': stored_filename,
        'is_base_file': bool(is_base_file),
        'queue_order': next_queue_order(),
        'status': 'queued',
        'created_at': utcnow_text(),
        'started_at': None,
        'completed_at': None,
        'error_message': None,
        'process_pid': None,
        'cancel_requested_at': None,
        'input_path': str(root / stored_filename),
        'stdout_log_path': str(root / 'stdout.log'),
        'stderr_log_path': str(root / 'stderr.log'),
        'result_json_path': str(root / 'result.json'),
        'report_html_path': None,
        'report_excel_path': None,
        'report_data_path': None,
        'stats': {},
        'current_record': None,
    }
    save_job(module_key, job)
    return job


def save_job(module_key: str, job: Dict[str, Any]) -> None:
    if _using_sqlite_backend():
        _save_job_sqlite(module_key, job)
        return
    _save_job_file(module_key, job)


def load_job(module_key: str, job_id: str) -> Optional[Dict[str, Any]]:
    if _using_sqlite_backend():
        return _load_job_sqlite(module_key, job_id)
    return _load_job_file(module_key, job_id)


def update_job(module_key: str, job_id: str, **fields: Any) -> Optional[Dict[str, Any]]:
    job = load_job(module_key, job_id)
    if job is None:
        return None
    job.update(fields)
    save_job(module_key, job)
    return job


def delete_job(module_key: str, job_id: str) -> bool:
    deleted = False
    if _using_sqlite_backend():
        ensure_runtime_dirs()
        with _sqlite_connection() as connection:
            cursor = connection.execute('DELETE FROM jobs WHERE module_key = ? AND id = ?', (module_key, job_id))
            connection.execute('DELETE FROM job_events WHERE module_key = ? AND job_id = ?', (module_key, job_id))
            connection.execute('DELETE FROM job_links WHERE module_key = ? AND job_id = ?', (module_key, job_id))
            connection.execute('DELETE FROM job_artifacts WHERE module_key = ? AND job_id = ?', (module_key, job_id))
            deleted = cursor.rowcount > 0
    root = module_jobs_root(module_key) / job_id
    if root.exists():
        shutil.rmtree(root, ignore_errors=True)
        deleted = True
    return deleted


def _list_jobs_sqlite(module_key: str, limit: int) -> List[Dict[str, Any]]:
    ensure_runtime_dirs()
    with _sqlite_connection() as connection:
        rows = connection.execute(
            'SELECT job_json FROM jobs WHERE module_key = ?',
            (module_key,),
        ).fetchall()
    jobs = [json.loads(str(row['job_json'])) for row in rows]
    jobs.sort(key=_job_list_sort_key, reverse=True)
    return jobs[:limit]


def _list_jobs_file(module_key: str, limit: int) -> List[Dict[str, Any]]:
    root = module_jobs_root(module_key)
    jobs: List[Dict[str, Any]] = []
    for path in root.glob('*/job.json'):
        try:
            jobs.append(json.loads(path.read_text(encoding='utf-8')))
        except json.JSONDecodeError:
            continue
    jobs.sort(key=_job_list_sort_key, reverse=True)
    return jobs[:limit]


def list_jobs(module_key: str, limit: int = 20) -> List[Dict[str, Any]]:
    if _using_sqlite_backend():
        return _list_jobs_sqlite(module_key, limit)
    return _list_jobs_file(module_key, limit)


def query_jobs(
    module_key: str,
    search_query: str = '',
    status_query: str = '',
    page: int = 1,
    page_size: int = 10,
) -> Dict[str, Any]:
    jobs = list_jobs(module_key, limit=1000000)

    cleaned_query = search_query.strip().lower()
    cleaned_status = status_query.strip().lower()

    if cleaned_query:
        jobs = [
            job for job in jobs
            if cleaned_query in str(job.get('original_filename', '')).lower()
            or cleaned_query in str(job.get('id', '')).lower()
        ]

    if cleaned_status:
        jobs = [
            job for job in jobs
            if str(job.get('status', '')).lower() == cleaned_status
        ]

    total_count = len(jobs)
    total_pages = max(math.ceil(total_count / page_size), 1)
    current_page = min(max(page, 1), total_pages)
    start_index = (current_page - 1) * page_size
    end_index = start_index + page_size

    return {
        'jobs': jobs[start_index:end_index],
        'total_count': total_count,
        'total_pages': total_pages,
        'current_page': current_page,
        'page_size': page_size,
        'page_start': start_index + 1 if total_count else 0,
        'page_end': min(end_index, total_count),
    }


def _derive_job_links(job: Dict[str, Any]) -> List[Dict[str, Any]]:
    links: List[Dict[str, Any]] = []
    detector_job_id = str(job.get('detector_job_id') or '').strip()
    if detector_job_id:
        links.append(
            {
                'link_kind': 'auto_detector',
                'linked_module_key': 'kpi-anomaly-detector',
                'linked_job_id': detector_job_id,
                'payload': {
                    'auto_detector_enabled': bool(job.get('auto_detector_enabled')),
                    'auto_detector_status': str(job.get('auto_detector_status') or ''),
                },
            }
        )
    source_generator_job_id = str(job.get('source_generator_job_id') or '').strip()
    if source_generator_job_id:
        links.append(
            {
                'link_kind': 'source_generator',
                'linked_module_key': 'kpi-generator',
                'linked_job_id': source_generator_job_id,
                'payload': {
                    'auto_submitted_from_generator': bool(job.get('auto_submitted_from_generator')),
                },
            }
        )
    return links


def _derive_job_artifacts(job: Dict[str, Any]) -> List[Dict[str, Any]]:
    mapping = {
        'input_path': 'request',
        'stdout_log_path': 'stdout',
        'stderr_log_path': 'stderr',
        'result_json_path': 'result',
        'report_html_path': 'report_html',
        'report_excel_path': 'report_excel',
        'report_data_path': 'report_data',
        'report_file_path': 'report',
        'scout_report_path': 'source',
    }
    artifacts: List[Dict[str, Any]] = []
    for field_name, artifact_kind in mapping.items():
        raw_path = str(job.get(field_name) or '').strip()
        if not raw_path:
            continue
        artifacts.append(
            {
                'artifact_kind': artifact_kind,
                'artifact_path': raw_path,
                'payload': {'field_name': field_name},
            }
        )

    for field_name, artifact_kind in (
        ('detail_html_paths', 'report_html_detail'),
        ('detail_excel_paths', 'report_excel_detail'),
    ):
        raw_paths = job.get(field_name)
        if not isinstance(raw_paths, list):
            continue
        for item_index, raw_path in enumerate(raw_paths):
            normalized_path = str(raw_path or '').strip()
            if not normalized_path:
                continue
            artifacts.append(
                {
                    'artifact_kind': artifact_kind,
                    'artifact_path': normalized_path,
                    'payload': {
                        'field_name': field_name,
                        'item_index': item_index,
                    },
                }
            )
    return artifacts


def _replace_job_links_sqlite(connection: sqlite3.Connection, module_key: str, job_id: str, links: List[Dict[str, Any]]) -> None:
    connection.execute('DELETE FROM job_links WHERE module_key = ? AND job_id = ?', (module_key, job_id))
    for link in links:
        connection.execute(
            'INSERT INTO job_links (module_key, job_id, link_kind, linked_module_key, linked_job_id, link_json) VALUES (?, ?, ?, ?, ?, ?)',
            (
                module_key,
                job_id,
                str(link.get('link_kind') or ''),
                str(link.get('linked_module_key') or ''),
                str(link.get('linked_job_id') or ''),
                json.dumps(link.get('payload') or {}, ensure_ascii=False),
            ),
        )


def _replace_job_artifacts_sqlite(connection: sqlite3.Connection, module_key: str, job_id: str, artifacts: List[Dict[str, Any]]) -> None:
    connection.execute('DELETE FROM job_artifacts WHERE module_key = ? AND job_id = ?', (module_key, job_id))
    for artifact in artifacts:
        connection.execute(
            'INSERT INTO job_artifacts (module_key, job_id, artifact_kind, artifact_path, artifact_json) VALUES (?, ?, ?, ?, ?)',
            (
                module_key,
                job_id,
                str(artifact.get('artifact_kind') or ''),
                str(artifact.get('artifact_path') or ''),
                json.dumps(artifact.get('payload') or {}, ensure_ascii=False),
            ),
        )


def _append_job_event_sqlite(
    connection: sqlite3.Connection,
    module_key: str,
    job_id: str,
    event_type: str,
    payload: Dict[str, Any],
) -> None:
    connection.execute(
        'INSERT INTO job_events (module_key, job_id, event_type, created_at, event_json) VALUES (?, ?, ?, ?, ?)',
        (module_key, job_id, event_type, utcnow_text(), json.dumps(payload, ensure_ascii=False)),
    )


def _derive_job_events(
    previous_job: Optional[Dict[str, Any]],
    current_job: Dict[str, Any],
    current_links: List[Dict[str, Any]],
    current_artifacts: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []

    if previous_job is None:
        events.append(
            {
                'event_type': 'job_created',
                'payload': {
                    'status': str(current_job.get('status') or ''),
                    'created_at': str(current_job.get('created_at') or ''),
                    'queue_order': int(current_job.get('queue_order') or 0),
                },
            }
        )

    previous_status = str((previous_job or {}).get('status') or '')
    current_status = str(current_job.get('status') or '')
    if current_status and previous_status != current_status:
        events.append(
            {
                'event_type': 'status_changed',
                'payload': {
                    'from_status': previous_status or None,
                    'to_status': current_status,
                    'started_at': current_job.get('started_at'),
                    'completed_at': current_job.get('completed_at'),
                },
            }
        )

    previous_stage = str((previous_job or {}).get('progress_stage') or '')
    previous_message = str((previous_job or {}).get('progress_message') or '')
    current_stage = str(current_job.get('progress_stage') or '')
    current_message = str(current_job.get('progress_message') or '')
    if current_stage or current_message:
        if previous_stage != current_stage or previous_message != current_message:
            events.append(
                {
                    'event_type': 'progress_updated',
                    'payload': {
                        'stage': current_stage or None,
                        'message': current_message or None,
                        'progress_updated_at': current_job.get('progress_updated_at'),
                    },
                }
            )

    previous_error = str((previous_job or {}).get('error_message') or '')
    current_error = str(current_job.get('error_message') or '')
    if current_error and previous_error != current_error:
        events.append(
            {
                'event_type': 'error_recorded',
                'payload': {
                    'message': current_error,
                    'status': current_status or None,
                },
            }
        )

    previous_links = {
        (
            str(link.get('link_kind') or ''),
            str(link.get('linked_module_key') or ''),
            str(link.get('linked_job_id') or ''),
        )
        for link in _derive_job_links(previous_job or {})
    }
    for link in current_links:
        signature = (
            str(link.get('link_kind') or ''),
            str(link.get('linked_module_key') or ''),
            str(link.get('linked_job_id') or ''),
        )
        if signature in previous_links:
            continue
        events.append(
            {
                'event_type': 'linked_job_added',
                'payload': {
                    'link_kind': signature[0],
                    'linked_module_key': signature[1],
                    'linked_job_id': signature[2],
                    'link_payload': dict(link.get('payload') or {}),
                },
            }
        )

    previous_artifacts = {
        (
            str(artifact.get('artifact_kind') or ''),
            str(artifact.get('artifact_path') or ''),
        )
        for artifact in _derive_job_artifacts(previous_job or {})
    }
    for artifact in current_artifacts:
        signature = (
            str(artifact.get('artifact_kind') or ''),
            str(artifact.get('artifact_path') or ''),
        )
        if signature in previous_artifacts:
            continue
        events.append(
            {
                'event_type': 'artifact_registered',
                'payload': {
                    'artifact_kind': signature[0],
                    'artifact_path': signature[1],
                    'artifact_payload': dict(artifact.get('payload') or {}),
                },
            }
        )

    return events


def append_job_event(module_key: str, job_id: str, event_type: str, payload: Dict[str, Any]) -> None:
    if not _using_sqlite_backend():
        return
    ensure_runtime_dirs()
    with _sqlite_connection() as connection:
        _append_job_event_sqlite(connection, module_key, job_id, event_type, payload)


def list_job_events(module_key: str, job_id: str) -> List[Dict[str, Any]]:
    if not _using_sqlite_backend():
        return []
    ensure_runtime_dirs()
    with _sqlite_connection() as connection:
        rows = connection.execute(
            'SELECT event_type, created_at, event_json FROM job_events WHERE module_key = ? AND job_id = ? ORDER BY id ASC',
            (module_key, job_id),
        ).fetchall()
    return [
        {
            'event_type': str(row['event_type']),
            'created_at': str(row['created_at']),
            'payload': json.loads(str(row['event_json'])),
        }
        for row in rows
    ]


def list_job_links(module_key: str, job_id: str) -> List[Dict[str, Any]]:
    if not _using_sqlite_backend():
        job = load_job(module_key, job_id)
        return _derive_job_links(job or {}) if job else []
    ensure_runtime_dirs()
    with _sqlite_connection() as connection:
        rows = connection.execute(
            'SELECT link_kind, linked_module_key, linked_job_id, link_json FROM job_links WHERE module_key = ? AND job_id = ? ORDER BY id ASC',
            (module_key, job_id),
        ).fetchall()
    return [
        {
            'link_kind': str(row['link_kind']),
            'linked_module_key': str(row['linked_module_key']),
            'linked_job_id': str(row['linked_job_id']),
            'payload': json.loads(str(row['link_json'])),
        }
        for row in rows
    ]


def list_job_artifacts(module_key: str, job_id: str) -> List[Dict[str, Any]]:
    if not _using_sqlite_backend():
        job = load_job(module_key, job_id)
        return _derive_job_artifacts(job or {}) if job else []
    ensure_runtime_dirs()
    with _sqlite_connection() as connection:
        rows = connection.execute(
            'SELECT artifact_kind, artifact_path, artifact_json FROM job_artifacts WHERE module_key = ? AND job_id = ? ORDER BY id ASC',
            (module_key, job_id),
        ).fetchall()
    return [
        {
            'artifact_kind': str(row['artifact_kind']),
            'artifact_path': str(row['artifact_path']),
            'payload': json.loads(str(row['artifact_json'])),
        }
        for row in rows
    ]
