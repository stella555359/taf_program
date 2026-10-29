from __future__ import annotations

from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, send_file, url_for

from ..adapters.kpi_traffic_model import get_kpi_traffic_model_adapter
from ..schemas import InputValidationError, TrafficModelPortalInput


kpi_traffic_model_bp = Blueprint('kpi_traffic_model', __name__, url_prefix='/kpi-traffic-model')


def _parse_int(value: str, default: int) -> int:
    cleaned = str(value or '').strip()
    if not cleaned:
        return default
    return int(cleaned)


@kpi_traffic_model_bp.get('/')
def index():
    adapter = get_kpi_traffic_model_adapter()
    env = request.args.get('env', '').strip().upper()
    env_context = None
    env_error = None
    if env:
        try:
            env_context = adapter.inspect_env(env)
        except Exception as exc:
            env_error = str(exc)
    return render_template(
        'modules/kpi_traffic_model.html',
        module=adapter.describe_module(),
        sample_command=adapter.sample_command(),
        jobs=adapter.list_jobs(limit=30),
        env=env,
        env_context=env_context,
        env_error=env_error,
    )


@kpi_traffic_model_bp.get('/api/resolve-env')
def resolve_env_api():
    env = request.args.get('env', '').strip().upper()
    if not env:
        return jsonify({'error': 'env is required.'}), 400
    adapter = get_kpi_traffic_model_adapter()
    try:
        return jsonify(adapter.inspect_env(env))
    except Exception as exc:
        return jsonify({'error': str(exc)}), 400


@kpi_traffic_model_bp.post('/jobs')
def submit():
    adapter = get_kpi_traffic_model_adapter()
    env = request.form.get('env', '').strip().upper()
    if not env:
        flash('Env is required.', 'error')
        return redirect(url_for('kpi_traffic_model.index'))

    try:
        env_context = adapter.inspect_env(env)
    except Exception as exc:
        flash(str(exc), 'error')
        return redirect(url_for('kpi_traffic_model.index', env=env))

    try:
        selected_indexes = [int(value) for value in request.form.getlist('selected_ue_indexes')]
    except ValueError:
        flash('Selected UE indexes must be integers.', 'error')
        return redirect(url_for('kpi_traffic_model.index', env=env))

    try:
        portal_input = TrafficModelPortalInput.from_form(
            environment=env,
            selected_ue_indexes=selected_indexes,
            dry_run=request.form.get('dry_run') == '1',
            stop_on_failure=request.form.get('stop_on_failure') == '1',
            max_parallel_workers=_parse_int(request.form.get('max_parallel_workers', ''), 4),
            log_level=request.form.get('log_level', 'INFO').strip() or 'INFO',
            auto_generator=request.form.get('auto_generator') == '1',
            auto_detector=request.form.get('auto_detector') == '1',
            same_type_execution_mode=request.form.get('same_type_execution_mode', 'serial').strip() or 'serial',
            cross_type_execution_mode=request.form.get('cross_type_execution_mode', 'serial').strip() or 'serial',
            stage_execution_mode=request.form.get('stage_execution_mode', 'serial').strip() or 'serial',
        )
    except InputValidationError as exc:
        flash(str(exc), 'error')
        return redirect(url_for('kpi_traffic_model.index', env=env))

    indexed_ues = {int(item['ue_index']): item for item in env_context['ues']}
    selected_ues = [indexed_ues[index] for index in portal_input.selected_ue_indexes if index in indexed_ues]
    if not selected_ues:
        flash('Select at least one UE.', 'error')
        return redirect(url_for('kpi_traffic_model.index', env=env))

    items = []
    order = 10

    if request.form.get('enable_preconditions') == '1':
        items.append(
            {
                'item_id': 'preconditions-1',
                'model': 'apply_preconditions',
                'enabled': True,
                'order': order,
                'execution_mode': 'serial',
                'continue_on_failure': False,
                'ue_scope': {'mode': 'all_selected_ues'},
                'params': {
                    'cell_barred': request.form.get('cell_barred') == '1',
                    'pa_port_state': request.form.get('pa_port_state', '').strip() or None,
                    'notes': request.form.get('precondition_notes', '').strip() or None,
                },
            }
        )
        order += 10

    if request.form.get('enable_attach') == '1':
        items.append(
            {
                'item_id': 'attach-1',
                'model': 'attach',
                'enabled': True,
                'order': order,
                'execution_mode': request.form.get('attach_execution_mode', 'serial').strip() or 'serial',
                'continue_on_failure': False,
                'ue_scope': {'mode': 'all_selected_ues'},
                'params': {
                    'attach_timeout_seconds': _parse_int(request.form.get('attach_timeout_seconds', ''), 120),
                },
            }
        )
        order += 10

    if request.form.get('enable_dl_burst') == '1':
        script_path = request.form.get('dl_burst_script_path', '').strip()
        if not script_path:
            flash('dl_burst_appserver requires a script_path.', 'error')
            return redirect(url_for('kpi_traffic_model.index', env=env))
        script_args = [line.strip() for line in request.form.get('dl_burst_script_args', '').splitlines() if line.strip()]
        items.append(
            {
                'item_id': 'dl-burst-1',
                'model': 'dl_burst_appserver',
                'enabled': True,
                'order': order,
                'execution_mode': request.form.get('dl_burst_execution_mode', 'serial').strip() or 'serial',
                'continue_on_failure': False,
                'ue_scope': {'mode': 'all_selected_ues'},
                'params': {
                    'script_path': script_path,
                    'script_args': script_args,
                },
            }
        )
        order += 10

    if request.form.get('enable_detach') == '1':
        items.append(
            {
                'item_id': 'detach-1',
                'model': 'detach',
                'enabled': True,
                'order': order,
                'execution_mode': request.form.get('detach_execution_mode', 'serial').strip() or 'serial',
                'continue_on_failure': True,
                'ue_scope': {'mode': 'all_selected_ues'},
                'params': {},
            }
        )

    if not items:
        flash('Enable at least one traffic item.', 'error')
        return redirect(url_for('kpi_traffic_model.index', env=env))

    payload = {
        'job_version': '1.0',
        'job_mode': portal_input.common.job_mode,
        'env': portal_input.common.environment,
        'testline_resolution': env_context['resolved_config'],
        'ue_selection': {
            'selected_ues': selected_ues,
            'same_type_execution_mode': portal_input.same_type_execution_mode,
            'cross_type_execution_mode': portal_input.cross_type_execution_mode,
        },
        'traffic_plan': {
            'stages': [
                {
                    'stage_id': 1,
                    'stage_name': 'default_stage',
                    'execution_mode': portal_input.stage_execution_mode,
                    'items': items,
                }
            ]
        },
        'runtime_options': {
            'dry_run': portal_input.runtime_options.dry_run,
            'stop_on_failure': portal_input.runtime_options.stop_on_failure,
            'max_parallel_workers': portal_input.runtime_options.max_parallel_workers,
            'log_level': portal_input.runtime_options.log_level,
        },
        'portal_followups': {
            'auto_generator': portal_input.runtime_options.auto_generator,
            'auto_detector': portal_input.runtime_options.auto_detector,
        },
    }

    try:
        job = adapter.submit_request(payload)
    except Exception as exc:
        flash(str(exc), 'error')
        return redirect(url_for('kpi_traffic_model.index', env=env))

    flash(f"Queued KPI traffic model job for {job['env']}.", 'success')
    return redirect(url_for('kpi_traffic_model.job_detail', job_id=job['id']))


@kpi_traffic_model_bp.get('/jobs/<job_id>')
def job_detail(job_id: str):
    adapter = get_kpi_traffic_model_adapter()
    job = adapter.get_job(job_id)
    if job is None:
        abort(404)
    return render_template(
        'modules/kpi_traffic_model_job.html',
        module=adapter.describe_module(),
        job=job,
        auto_refresh=job['status'] in {'queued', 'running'},
    )


@kpi_traffic_model_bp.get('/api/jobs/<job_id>')
def job_status(job_id: str):
    adapter = get_kpi_traffic_model_adapter()
    job = adapter.get_job(job_id)
    if job is None:
        abort(404)
    return jsonify(job)


@kpi_traffic_model_bp.get('/jobs/<job_id>/artifacts/<artifact_kind>')
def artifact(job_id: str, artifact_kind: str):
    adapter = get_kpi_traffic_model_adapter()
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
        mimetype='application/json' if artifact_kind in {'request', 'result'} else 'text/plain',
    )


@kpi_traffic_model_bp.post('/jobs/<job_id>/delete')
def delete(job_id: str):
    adapter = get_kpi_traffic_model_adapter()
    try:
        adapter.delete(job_id)
    except FileNotFoundError:
        abort(404)
    flash(f'Deleted KPI traffic model job {job_id}.', 'success')
    return redirect(url_for('kpi_traffic_model.index'))
