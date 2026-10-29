from __future__ import annotations

import mimetypes

from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, send_file, url_for

from ..adapters.kpi_detector import get_kpi_detector_adapter
from ..services.job_store import next_queue_order


kpi_detector_bp = Blueprint('kpi_detector', __name__, url_prefix='/kpi-anomaly-detector')


def _index_filters() -> dict:
    try:
        page = int(request.args.get('page', '1'))
    except ValueError:
        page = 1

    return {
        'q': request.args.get('q', '').strip(),
        'status': request.args.get('status', '').strip(),
        'release': request.args.get('release', '').strip(),
        'environment': request.args.get('environment', '').strip(),
        'scenario': request.args.get('scenario', '').strip(),
        'page': max(page, 1),
    }


def _page_numbers(current_page: int, total_pages: int, radius: int = 2) -> list[int]:
    if total_pages <= 0:
        return []

    start_page = max(1, current_page - radius)
    end_page = min(total_pages, current_page + radius)

    if start_page > 1:
        start_page = 1 if current_page <= radius + 2 else start_page
    if end_page < total_pages:
        end_page = total_pages if current_page >= total_pages - (radius + 1) else end_page

    return list(range(start_page, end_page + 1))


def _next_index_args() -> dict:
    try:
        page = max(int(request.form.get('page', '1')), 1)
    except ValueError:
        page = 1
    return {
        'q': request.form.get('q', '').strip(),
        'status': request.form.get('status', '').strip(),
        'release': request.form.get('release', '').strip(),
        'environment': request.form.get('environment', '').strip(),
        'scenario': request.form.get('scenario', '').strip(),
        'page': page,
    }


def _selected_job_ids() -> list[str]:
    seen = set()
    selected = []
    for value in request.form.getlist('job_ids'):
        job_id = value.strip()
        if job_id and job_id not in seen:
            selected.append(job_id)
            seen.add(job_id)
    return selected


@kpi_detector_bp.get('/')
def index():
    adapter = get_kpi_detector_adapter()
    filters = _index_filters()
    job_page = adapter.query_jobs(
        search_query=filters['q'],
        status_query=filters['status'],
        release_query=filters['release'],
        environment_query=filters['environment'],
        scenario_query=filters['scenario'],
        page=filters['page'],
        page_size=10,
    )
    auto_refresh = any(str(job.get('status') or '') in {'queued', 'running'} for job in job_page['jobs'])
    return render_template(
        'modules/kpi_detector.html',
        module=adapter.describe_module(),
        sample_command=adapter.sample_command(),
        filter_options=adapter.filter_options(filters['release'], filters['environment']),
        jobs=job_page['jobs'],
        job_page=job_page,
        page_numbers=_page_numbers(job_page['current_page'], job_page['total_pages']),
        filters=filters,
        auto_refresh=auto_refresh,
    )


@kpi_detector_bp.post('/submit')
def submit():
    adapter = get_kpi_detector_adapter()
    is_base_file = request.form.get('is_base_file', '').strip().lower() in {'1', 'true', 'on', 'yes'}
    override_environment = request.form.get('filename_override_environment', '').strip()
    override_scenario = request.form.get('filename_override_scenario', '').strip()
    uploads = request.files.getlist('files')
    if not uploads:
        single_upload = request.files.get('file')
        if single_upload is not None:
            uploads = [single_upload]

    uploads = [upload for upload in uploads if upload is not None and upload.filename]
    if not uploads:
        flash('Please select one or more .xlsx files before submitting.', 'error')
        return redirect(url_for('kpi_detector.index'))

    queued_jobs = []
    rejected_files = []
    submission_batch_order = next_queue_order()

    for upload_index, upload in enumerate(uploads):
        if not upload.filename.lower().endswith('.xlsx'):
            rejected_files.append(f'{upload.filename}: only .xlsx files are supported for the anomaly detector.')
            continue

        try:
            queued_jobs.append(
                adapter.submit(
                    upload,
                    is_base_file=is_base_file,
                    override_environment=override_environment,
                    override_scenario=override_scenario,
                    submission_batch_order=submission_batch_order,
                    submission_index=upload_index,
                )
            )
        except ValueError as exc:
            rejected_files.append(f'{upload.filename}: {exc}')

    if not queued_jobs and rejected_files:
        for message in rejected_files:
            flash(message, 'error')
        return redirect(url_for('kpi_detector.index'))

    if queued_jobs:
        if len(queued_jobs) == 1:
            uploaded_filename = str(queued_jobs[0].get('uploaded_filename') or queued_jobs[0]['original_filename'])
            override_applied = bool(queued_jobs[0].get('filename_override_applied'))
            if queued_jobs[0].get('reused_existing'):
                if override_applied:
                    flash(f"Replaced the latest detector result for {queued_jobs[0]['original_filename']} and started a fresh run. Uploaded file {uploaded_filename} was renamed automatically.", 'success')
                else:
                    flash(f"Replaced the latest detector result for {queued_jobs[0]['original_filename']} and started a fresh run.", 'success')
            else:
                if override_applied:
                    flash(f"Queued detector job for {queued_jobs[0]['original_filename']}. Uploaded file {uploaded_filename} was renamed automatically.", 'success')
                else:
                    flash(f"Queued detector job for {queued_jobs[0]['original_filename']}.", 'success')
        else:
            flash(f'Queued {len(queued_jobs)} detector jobs.', 'success')

    for message in rejected_files:
        flash(message, 'error')

    if len(queued_jobs) == 1 and not rejected_files:
        return redirect(url_for('kpi_detector.job_detail', job_id=queued_jobs[0]['id']))
    return redirect(url_for('kpi_detector.index'))


@kpi_detector_bp.post('/validate-upload-filenames')
def validate_upload_filenames():
    adapter = get_kpi_detector_adapter()
    payload = request.get_json(silent=True) or {}
    filenames = payload.get('filenames') if isinstance(payload, dict) else []
    if not isinstance(filenames, list):
        filenames = []

    invalid_filenames = []
    for filename in filenames:
        cleaned_filename = str(filename or '').strip()
        if not cleaned_filename:
            continue
        if adapter.validate_filename(cleaned_filename):
            invalid_filenames.append(cleaned_filename)

    return jsonify(
        {
            'invalid_filenames': invalid_filenames,
            'requires_override': bool(invalid_filenames),
        }
    )


@kpi_detector_bp.get('/jobs/<job_id>')
def job_detail(job_id: str):
    adapter = get_kpi_detector_adapter()
    job = adapter.get_job(job_id)
    if job is None:
        abort(404)
    return render_template(
        'modules/kpi_detector_job.html',
        module=adapter.describe_module(),
        job=job,
        stdout_tail=adapter.read_job_log_tail(job, 'stdout'),
        stderr_tail=adapter.read_job_log_tail(job, 'stderr'),
        auto_refresh=job['status'] in {'queued', 'running'},
    )


@kpi_detector_bp.post('/jobs/<job_id>/rerun')
def rerun(job_id: str):
    adapter = get_kpi_detector_adapter()
    try:
        job = adapter.rerun(job_id)
    except FileNotFoundError:
        abort(404)
    except ValueError as exc:
        flash(str(exc), 'error')
        return redirect(url_for('kpi_detector.job_detail', job_id=job_id))

    flash('Detector job rerun started.', 'success')
    return redirect(url_for('kpi_detector.job_detail', job_id=job['id']))


@kpi_detector_bp.post('/jobs/bulk/rerun')
def bulk_rerun():
    adapter = get_kpi_detector_adapter()
    next_args = _next_index_args()
    job_ids = _selected_job_ids()
    if not job_ids:
        flash('Select at least one job to rerun.', 'error')
        return redirect(url_for('kpi_detector.index', **next_args))

    rerun_count = 0
    failures = []
    for job_id in job_ids:
        try:
            adapter.rerun(job_id)
            rerun_count += 1
        except FileNotFoundError:
            failures.append(f'{job_id}: job not found')
        except ValueError as exc:
            failures.append(f'{job_id}: {exc}')

    if rerun_count:
        flash(f'Rerun started for {rerun_count} selected job(s).', 'success')
    for message in failures:
        flash(message, 'error')
    return redirect(url_for('kpi_detector.index', **next_args))


@kpi_detector_bp.post('/jobs/<job_id>/cancel')
def cancel(job_id: str):
    adapter = get_kpi_detector_adapter()
    next_q = request.form.get('q', '').strip()
    next_status = request.form.get('status', '').strip()
    next_release = request.form.get('release', '').strip()
    next_environment = request.form.get('environment', '').strip()
    next_scenario = request.form.get('scenario', '').strip()
    try:
        next_page = max(int(request.form.get('page', '1')), 1)
    except ValueError:
        next_page = 1

    try:
        job = adapter.cancel(job_id)
    except FileNotFoundError:
        abort(404)
    except ValueError as exc:
        flash(str(exc), 'error')
        return redirect(url_for('kpi_detector.job_detail', job_id=job_id))

    flash(f"Cancelled detector job for {job['original_filename']}.", 'success')
    if request.form.get('from') == 'detail':
        return redirect(url_for('kpi_detector.job_detail', job_id=job_id))
    return redirect(url_for('kpi_detector.index', q=next_q, status=next_status, release=next_release, environment=next_environment, scenario=next_scenario, page=next_page))


@kpi_detector_bp.post('/jobs/<job_id>/delete')
def delete(job_id: str):
    adapter = get_kpi_detector_adapter()
    next_args = _next_index_args()

    try:
        result = adapter.delete(job_id)
    except FileNotFoundError:
        abort(404)
    except ValueError as exc:
        flash(str(exc), 'error')
        return redirect(url_for('kpi_detector.job_detail', job_id=job_id))

    removed_history = result.get('removed_history_records', 0)
    kept_shared = result.get('kept_shared_filenames') or []
    message = f'Deleted job {job_id}.'
    if removed_history:
        message += f' Removed {removed_history} history record(s).'
    if kept_shared:
        message += ' Kept shared history for duplicated filenames.'
    flash(message, 'success')
    return redirect(url_for('kpi_detector.index', **next_args))


@kpi_detector_bp.post('/jobs/bulk/delete')
def bulk_delete():
    adapter = get_kpi_detector_adapter()
    next_args = _next_index_args()
    job_ids = _selected_job_ids()
    if not job_ids:
        flash('Select at least one job to delete.', 'error')
        return redirect(url_for('kpi_detector.index', **next_args))

    deleted_count = 0
    removed_history = 0
    failures = []
    for job_id in job_ids:
        try:
            result = adapter.delete(job_id)
            deleted_count += 1
            removed_history += int(result.get('removed_history_records', 0) or 0)
        except FileNotFoundError:
            failures.append(f'{job_id}: job not found')
        except ValueError as exc:
            failures.append(f'{job_id}: {exc}')

    if deleted_count:
        message = f'Deleted {deleted_count} selected job(s).'
        if removed_history:
            message += f' Removed {removed_history} history record(s).'
        flash(message, 'success')
    for message in failures:
        flash(message, 'error')
    return redirect(url_for('kpi_detector.index', **next_args))


@kpi_detector_bp.get('/api/jobs/<job_id>')
def job_status(job_id: str):
    adapter = get_kpi_detector_adapter()
    job = adapter.get_job(job_id)
    if job is None:
        abort(404)
    payload = dict(job)
    payload['stdout_tail'] = adapter.read_job_log_tail(job, 'stdout')
    payload['stderr_tail'] = adapter.read_job_log_tail(job, 'stderr')
    return jsonify(payload)


@kpi_detector_bp.get('/jobs/<job_id>/artifacts/<artifact_kind>')
def artifact(job_id: str, artifact_kind: str):
    adapter = get_kpi_detector_adapter()
    job = adapter.get_job(job_id)
    if job is None:
        abort(404)

    artifact_path = adapter.artifact_path(job, artifact_kind)
    as_attachment = artifact_kind in {'excel', 'stdout', 'stderr', 'bundle'}
    guessed_type = 'application/json' if artifact_kind == 'data' else ('application/zip' if artifact_kind == 'bundle' else None)

    if artifact_path is None:
        artifact_path = adapter.report_asset_path(job, artifact_kind)
        if artifact_path is None:
            abort(404)
        as_attachment = False
        guessed_type, _ = mimetypes.guess_type(str(artifact_path))

    response = send_file(
        artifact_path,
        as_attachment=as_attachment,
        download_name=artifact_path.name,
        mimetype='application/json' if guessed_type == 'application/json' and artifact_path.suffix.lower() == '.json' else guessed_type,
    )
    response.cache_control.no_store = True
    response.cache_control.no_cache = True
    response.cache_control.must_revalidate = True
    response.expires = 0
    return response


@kpi_detector_bp.get('/jobs/<job_id>/detail-artifacts/<artifact_kind>/<int:item_index>')
def detail_artifact(job_id: str, artifact_kind: str, item_index: int):
    adapter = get_kpi_detector_adapter()
    job = adapter.get_job(job_id)
    if job is None:
        abort(404)

    artifact_path = adapter.detail_artifact_path(job, artifact_kind, item_index)
    if artifact_path is None:
        abort(404)

    guessed_type = None
    if artifact_kind == 'html':
        guessed_type = 'text/html'
    elif artifact_kind == 'excel':
        guessed_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    response = send_file(
        artifact_path,
        as_attachment=artifact_kind == 'excel',
        download_name=artifact_path.name,
        mimetype=guessed_type,
    )
    response.cache_control.no_store = True
    response.cache_control.no_cache = True
    response.cache_control.must_revalidate = True
    response.expires = 0
    return response


@kpi_detector_bp.get('/jobs/<job_id>/artifacts/<path:asset_path>')
def artifact_asset(job_id: str, asset_path: str):
    adapter = get_kpi_detector_adapter()
    job = adapter.get_job(job_id)
    if job is None:
        abort(404)

    artifact_path = adapter.report_asset_path(job, asset_path)
    if artifact_path is None:
        abort(404)

    guessed_type, _ = mimetypes.guess_type(str(artifact_path))
    response = send_file(
        artifact_path,
        as_attachment=False,
        download_name=artifact_path.name,
        mimetype=guessed_type,
    )
    response.cache_control.no_store = True
    response.cache_control.no_cache = True
    response.cache_control.must_revalidate = True
    response.expires = 0
    return response