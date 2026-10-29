from __future__ import annotations

from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, send_file, url_for

from ..adapters.kpi_generator import get_kpi_generator_adapter
from ..adapters.kpi_detector import get_kpi_detector_adapter


kpi_generator_bp = Blueprint('kpi_generator', __name__, url_prefix='/kpi-generator')


def _index_filters() -> dict:
    try:
        page = int(request.args.get('page', '1'))
    except ValueError:
        page = 1
    return {
        'q': request.args.get('q', '').strip(),
        'status': request.args.get('status', '').strip(),
        'environment': request.args.get('environment', '').strip(),
        'scenario': request.args.get('scenario', '').strip(),
        'page': max(page, 1),
    }


def _page_numbers(current_page: int, total_pages: int, radius: int = 2) -> list[int]:
    if total_pages <= 0:
        return []
    start_page = max(1, current_page - radius)
    end_page = min(total_pages, current_page + radius)
    return list(range(start_page, end_page + 1))


@kpi_generator_bp.get('/')
def index():
    adapter = get_kpi_generator_adapter()
    filters = _index_filters()
    job_page = adapter.query_jobs(
        search_query=filters['q'],
        status_query=filters['status'],
        environment_query=filters['environment'],
        scenario_query=filters['scenario'],
        page=filters['page'],
        page_size=10,
    )
    return render_template(
        'modules/kpi_generator.html',
        module=adapter.describe_module(),
        sample_command=adapter.sample_command(),
        filter_options=adapter.filter_options(),
        jobs=job_page['jobs'],
        job_page=job_page,
        page_numbers=_page_numbers(job_page['current_page'], job_page['total_pages']),
        filters=filters,
    )


@kpi_generator_bp.post('/jobs')
def submit():
    adapter = get_kpi_generator_adapter()
    job_mode = request.form.get('job_mode', 'generator').strip()
    auto_detector_is_base_file = request.form.get('auto_detector_is_base_file') == '1'
    auto_detector = request.form.get('auto_detector') == '1' or auto_detector_is_base_file

    if job_mode == 'scout_conversion':
        build = request.form.get('build', '').strip()
        environment = request.form.get('environment', '').strip()
        scenario = request.form.get('scenario', '').strip()
        dist_name_filter = request.form.get('dist_name_filter', '')
        scout_report = request.files.get('scout_report')

        if scout_report is None or not scout_report.filename:
            flash('Please select a scout report .xlsx file.', 'error')
            return redirect(url_for('kpi_generator.index'))
        if not scout_report.filename.lower().endswith('.xlsx'):
            flash('Scout conversion only supports .xlsx files.', 'error')
            return redirect(url_for('kpi_generator.index'))

        try:
            job = adapter.submit_scout_conversion(
                scout_report=scout_report,
                dist_name_filter=dist_name_filter,
                build=build,
                environment=environment,
                scenario=scenario,
                auto_detector=auto_detector,
                auto_detector_is_base_file=auto_detector_is_base_file,
            )
        except ValueError as exc:
            flash(str(exc), 'error')
            return redirect(url_for('kpi_generator.index'))

        flash(f'Queued scout conversion job for {job["scenario"]}.', 'success')
        return redirect(url_for('kpi_generator.job_detail', job_id=job['id']))

    template_set_name = request.form.get('template_set_name', '').strip()
    template_names = request.form.get('template_names', '').strip()
    build = request.form.get('build', '').strip()
    environment = request.form.get('environment', '').strip()
    scenario = request.form.get('scenario', '').strip()
    report_timestamps_text = request.form.get('report_timestamps_list', '').strip()
    raw_delta = request.form.get('timestamp_delta_minutes', '').strip()
    if raw_delta:
        try:
            timestamp_delta_minutes = int(raw_delta)
        except ValueError:
            flash('timestamp_delta_minutes must be an integer.', 'error')
            return redirect(url_for('kpi_generator.index'))
    else:
        timestamp_delta_minutes = None

    try:
        job = adapter.submit(
            report_timestamps_text=report_timestamps_text,
            template_set_name=template_set_name,
            template_names=template_names,
            build=build,
            environment=environment,
            scenario=scenario,
            timestamp_delta_minutes=timestamp_delta_minutes,
            auto_detector=auto_detector,
            auto_detector_is_base_file=auto_detector_is_base_file,
        )
    except ValueError as exc:
        flash(str(exc), 'error')
        return redirect(url_for('kpi_generator.index'))

    flash(f'Queued KPI generator job.', 'success')
    return redirect(url_for('kpi_generator.job_detail', job_id=job['id']))


@kpi_generator_bp.get('/jobs/<job_id>')
def job_detail(job_id: str):
    adapter = get_kpi_generator_adapter()
    job = adapter.get_job(job_id)
    if job is None:
        abort(404)
    linked_detector_job = None
    if job.get('detector_job_id'):
        linked_detector_job = get_kpi_detector_adapter().get_job(str(job['detector_job_id']))
    return render_template(
        'modules/kpi_generator_job.html',
        module=adapter.describe_module(),
        job=job,
        linked_detector_job=linked_detector_job,
        auto_refresh=job['status'] in {'queued', 'running'},
    )


@kpi_generator_bp.post('/jobs/<job_id>/rerun')
def rerun(job_id: str):
    adapter = get_kpi_generator_adapter()
    try:
        job = adapter.rerun(job_id)
    except FileNotFoundError:
        abort(404)
    except ValueError as exc:
        flash(str(exc), 'error')
        return redirect(url_for('kpi_generator.job_detail', job_id=job_id))
    flash('KPI generator job queued again.', 'success')
    return redirect(url_for('kpi_generator.job_detail', job_id=job['id']))


@kpi_generator_bp.post('/jobs/<job_id>/cancel')
def cancel(job_id: str):
    adapter = get_kpi_generator_adapter()
    try:
        job = adapter.cancel(job_id)
    except FileNotFoundError:
        abort(404)
    except ValueError as exc:
        flash(str(exc), 'error')
        return redirect(url_for('kpi_generator.job_detail', job_id=job_id))
    job_label = job.get('job_label') or job.get('generated_filename') or job.get('template_set_name') or job.get('release') or job.get('scenario') or job_id
    flash(f'Cancelled KPI generator job {job_label}.', 'success')
    return redirect(url_for('kpi_generator.job_detail', job_id=job_id))


@kpi_generator_bp.post('/jobs/<job_id>/delete')
def delete(job_id: str):
    adapter = get_kpi_generator_adapter()
    try:
        adapter.delete(job_id)
    except FileNotFoundError:
        abort(404)
    except ValueError as exc:
        flash(str(exc), 'error')
        return redirect(url_for('kpi_generator.job_detail', job_id=job_id))
    flash(f'Deleted KPI generator job {job_id}.', 'success')
    return redirect(url_for('kpi_generator.index'))


@kpi_generator_bp.get('/api/jobs/<job_id>')
def job_status(job_id: str):
    adapter = get_kpi_generator_adapter()
    job = adapter.get_job(job_id)
    if job is None:
        abort(404)
    return jsonify(job)


@kpi_generator_bp.get('/jobs/<job_id>/artifacts/<artifact_kind>')
def artifact(job_id: str, artifact_kind: str):
    adapter = get_kpi_generator_adapter()
    job = adapter.get_job(job_id)
    if job is None:
        abort(404)
    artifact_path = adapter.artifact_path(job, artifact_kind)
    if artifact_path is None:
        abort(404)
    return send_file(
        artifact_path,
        as_attachment=artifact_kind not in {'result'},
        download_name=artifact_path.name,
        mimetype='application/json' if artifact_kind == 'result' else ('application/zip' if artifact_kind == 'bundle' else None),
    )