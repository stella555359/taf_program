from __future__ import annotations

import uuid

from flask import Blueprint, flash, jsonify, redirect, render_template, request, send_file, url_for

from ..services.kpi_analysis_service import (
    DEFAULT_PAGE_SIZE,
    STATUS_ACTIVE,
    build_kpi_dashboard_context,
    build_stored_filename,
    create_analysis_record,
    delete_analysis_bundle,
    get_analysis_or_404,
    get_request_user_label,
    is_allowed_file,
    parse_page_number,
    queue_analysis_rerun,
    resolve_artifact_path,
    resolve_report_data_path,
    restore_analysis_bundle,
    serialize_analysis,
    soft_delete_analysis_bundle,
    start_analysis_job,
    count_active_analyses,
    UPLOAD_DIR,
    redirect_to_kpi_index,
)


kpi_bp = Blueprint('kpi', __name__, url_prefix='/kpi')


@kpi_bp.get('/')
def index():
    context = build_kpi_dashboard_context(
        search_query=request.args.get('q', '').strip(),
        environment_query=request.args.get('env', '').strip(),
        scenario_query=request.args.get('scenario', '').strip(),
        requested_page=parse_page_number(request.args.get('page', '1')),
        requested_sort=request.args.get('sort', 'created'),
        requested_order=request.args.get('order', 'desc'),
    )
    context['default_page_size'] = DEFAULT_PAGE_SIZE
    return render_template('index.html', **context)


@kpi_bp.post('/upload')
def upload_file():
    uploads = [item for item in request.files.getlist('files') if item and item.filename]
    if not uploads:
        upload = request.files.get('file')
        if upload is not None and upload.filename:
            uploads = [upload]

    if not uploads:
        flash('Please select at least one .xlsx file before submitting.', 'error')
        return redirect(url_for('kpi.index'))

    invalid_filenames = [item.filename for item in uploads if not is_allowed_file(item.filename)]
    if invalid_filenames:
        flash(
            'Only .xlsx files are supported. Invalid files: ' + ', '.join(invalid_filenames),
            'error',
        )
        return redirect(url_for('kpi.index'))

    uploader_username = get_request_user_label()
    created_analysis_ids: list[str] = []
    for upload in uploads:
        analysis_id = uuid.uuid4().hex
        stored_filename = build_stored_filename(upload.filename)
        upload_path = UPLOAD_DIR / stored_filename
        upload.save(upload_path)

        create_analysis_record(
            analysis_id=analysis_id,
            original_filename=upload.filename,
            uploader_username=uploader_username,
            stored_filename=stored_filename,
            upload_path=upload_path,
        )
        start_analysis_job(analysis_id)
        created_analysis_ids.append(analysis_id)

    if len(created_analysis_ids) == 1:
        return redirect(url_for('kpi.analysis_detail', analysis_id=created_analysis_ids[0]))

    flash(f'Started analysis for {len(created_analysis_ids)} files. They are now queued in Latest runs.', 'success')
    return redirect(redirect_to_kpi_index(anchor='page-top'))


@kpi_bp.get('/analysis/<analysis_id>')
def analysis_detail(analysis_id: str):
    analysis = get_analysis_or_404(analysis_id)
    auto_refresh = analysis['status'] in STATUS_ACTIVE
    return render_template('analysis_detail.html', analysis=analysis, auto_refresh=auto_refresh)


@kpi_bp.get('/api/analysis/<analysis_id>')
def analysis_status(analysis_id: str):
    return jsonify(serialize_analysis(get_analysis_or_404(analysis_id)))


@kpi_bp.get('/api/dashboard-status')
def dashboard_status():
    return jsonify({'active_count': count_active_analyses()})


@kpi_bp.post('/analysis/<analysis_id>/rerun')
def analysis_rerun(analysis_id: str):
    analysis = get_analysis_or_404(analysis_id)

    if analysis['status'] in STATUS_ACTIVE:
        flash('Running analyses cannot be queued again yet.', 'error')
    else:
        try:
            queue_analysis_rerun(analysis)
            flash(f"Queued detector rerun for {analysis['original_filename']}.", 'success')
        except FileNotFoundError as exc:
            flash(f"Could not rerun {analysis['original_filename']}: {exc}", 'error')

    if request.form.get('return_to') == 'detail':
        return redirect(url_for('kpi.analysis_detail', analysis_id=analysis_id))

    return redirect(
        redirect_to_kpi_index(
            request.form.get('return_q', '').strip(),
            request.form.get('return_env', '').strip(),
            request.form.get('return_scenario', '').strip(),
            request.form.get('return_sort', 'created'),
            request.form.get('return_order', 'desc'),
            parse_page_number(request.form.get('return_page', '1')),
            request.form.get('return_anchor', f'analysis-{analysis_id}'),
        )
    )


@kpi_bp.post('/analysis/<analysis_id>/delete')
def analysis_delete(analysis_id: str):
    analysis = get_analysis_or_404(analysis_id)

    if analysis['status'] in STATUS_ACTIVE:
        flash('Running analyses cannot be deleted.', 'error')
        return redirect(
            redirect_to_kpi_index(
                request.form.get('return_q', '').strip(),
                request.form.get('return_env', '').strip(),
                request.form.get('return_scenario', '').strip(),
                request.form.get('return_sort', 'created'),
                request.form.get('return_order', 'desc'),
                parse_page_number(request.form.get('return_page', '1')),
            )
        )

    delete_mode = request.form.get('delete_mode', 'hard')
    if delete_mode == 'soft':
        soft_delete_analysis_bundle(analysis)
        flash(f"Hidden {analysis['original_filename']} from Latest 50 runs. Files and JSON history were kept.", 'success')
    else:
        delete_analysis_bundle(analysis)
        flash(f"Deleted {analysis['original_filename']} and removed its generated files and JSON history entry.", 'success')

    return redirect(
        redirect_to_kpi_index(
            request.form.get('return_q', '').strip(),
            request.form.get('return_env', '').strip(),
            request.form.get('return_scenario', '').strip(),
            request.form.get('return_sort', 'created'),
            request.form.get('return_order', 'desc'),
            parse_page_number(request.form.get('return_page', '1')),
        )
    )


@kpi_bp.post('/analysis/<analysis_id>/restore')
def analysis_restore(analysis_id: str):
    analysis = get_analysis_or_404(analysis_id)
    restore_analysis_bundle(analysis)
    flash(f"Restored {analysis['original_filename']} to Latest 50 runs.", 'success')
    return redirect(
        redirect_to_kpi_index(
            request.form.get('return_q', '').strip(),
            request.form.get('return_env', '').strip(),
            request.form.get('return_scenario', '').strip(),
            request.form.get('return_sort', 'created'),
            request.form.get('return_order', 'desc'),
            parse_page_number(request.form.get('return_page', '1')),
        )
    )


@kpi_bp.get('/analysis/<analysis_id>/<artifact_kind>')
def analysis_artifact(analysis_id: str, artifact_kind: str):
    analysis = get_analysis_or_404(analysis_id)

    if artifact_kind == 'data':
        artifact_path = resolve_report_data_path(analysis.get('report_html_path'))
        if artifact_path is None:
            return ('', 404)

        return send_file(
            artifact_path,
            as_attachment=False,
            download_name=artifact_path.name,
            mimetype='application/javascript',
        )

    artifact_column = {
        'html': 'report_html_path',
        'excel': 'report_excel_path',
    }.get(artifact_kind)

    if artifact_column is None:
        return ('', 404)

    artifact_path = resolve_artifact_path(analysis.get(artifact_column))
    if artifact_path is None:
        return ('', 404)

    return send_file(
        artifact_path,
        as_attachment=artifact_kind == 'excel',
        download_name=artifact_path.name,
        mimetype='text/html' if artifact_kind == 'html' else None,
    )