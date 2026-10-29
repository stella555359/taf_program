from __future__ import annotations

import io
import os
import tempfile
import unittest
import zipfile
from datetime import datetime, timedelta
from unittest.mock import patch

from portal import create_app
from portal.adapters.kpi_detector import KpiDetectorAdapter, get_kpi_detector_adapter
from portal.adapters.kpi_generator import KpiGeneratorAdapter, get_kpi_generator_adapter
from flask import url_for
from portal.services.job_store import create_job, delete_job, list_job_artifacts, list_job_links, list_jobs, load_job, update_job


class PortalSubmissionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_env = dict(os.environ)
        os.environ['KPI_DASHBOARD_ENV'] = 'test'
        os.environ['KPI_JOB_STORE_BACKEND'] = 'sqlite'
        os.environ['KPI_SQLITE_PATH'] = os.path.join(self.temp_dir.name, 'portal-submissions.db')
        self.generator_template_patch = patch.object(KpiGeneratorAdapter, 'template_set_options', return_value={'options': [], 'error': ''})
        self.generator_schedule_patch = patch.object(KpiGeneratorAdapter, '_schedule_dispatch', return_value=None)
        self.detector_schedule_patch = patch.object(KpiDetectorAdapter, '_schedule_dispatch', return_value=None)
        self.generator_template_patch.start()
        self.generator_schedule_patch.start()
        self.detector_schedule_patch.start()

        app = create_app()
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def tearDown(self) -> None:
        self.generator_template_patch.stop()
        self.generator_schedule_patch.stop()
        self.detector_schedule_patch.stop()
        os.environ.clear()
        os.environ.update(self.original_env)
        self.temp_dir.cleanup()

    def test_generator_submit_creates_queued_job_and_platform_metadata(self) -> None:
        response = self.client.post(
            '/kpi-generator/jobs',
            data={
                'job_mode': 'generator',
                'template_set_name': 'DemoTemplateSet',
                'template_names': 'TemplateA;TemplateB',
                'build': '24A',
                'environment': 'T813.SCF.T813.demo',
                'scenario': 'Throughput',
                'report_timestamps_list': '[["2024-01-01 00:00:00", "2024-01-01 01:00:00"]]',
                'auto_detector': '1',
            },
        )

        self.assertEqual(response.status_code, 302)

        jobs = list_jobs('kpi-generator', limit=10)
        self.assertEqual(len(jobs), 1)
        job_id = str(jobs[0]['id'])
        saved_job = load_job('kpi-generator', job_id)

        self.assertIsNotNone(saved_job)
        self.assertEqual(saved_job['status'], 'queued')
        self.assertEqual(saved_job['job_mode'], 'generator')
        self.assertEqual(saved_job['template_set_name'], 'DemoTemplateSet')
        self.assertEqual(saved_job['build'], '24A')
        self.assertEqual(saved_job['environment'], 'T813.SCF.T813.demo')
        self.assertEqual(saved_job['scenario'], 'Throughput')
        self.assertEqual(saved_job['auto_detector_status'], 'waiting_for_generator')

        artifact_kinds = {artifact['artifact_kind'] for artifact in list_job_artifacts('kpi-generator', job_id)}
        self.assertIn('request', artifact_kinds)
        self.assertIn('stdout', artifact_kinds)
        self.assertIn('stderr', artifact_kinds)
        self.assertIn('result', artifact_kinds)

        self.assertEqual(list_job_links('kpi-generator', job_id), [])

        api_response = self.client.get(f'/kpi-generator/api/jobs/{job_id}')
        self.assertEqual(api_response.status_code, 200)
        payload = api_response.get_json()
        self.assertIsNotNone(payload)
        self.assertIn('platform_artifacts', payload)
        self.assertIn('platform_events', payload)
        self.assertIn('platform_display_events', payload)
        self.assertIn('platform_timeline_events', payload)
        self.assertIn('platform_recent_stage', payload)
        self.assertIn('platform_recent_message', payload)
        self.assertIn('platform_download_artifacts', payload)
        self.assertIn('platform_artifacts_by_kind', payload)
        self.assertTrue(any(event['event_type'] == 'job_created' for event in payload['platform_events']))
        self.assertTrue(any(event['event_type'] == 'progress_updated' for event in payload['platform_display_events']))
        self.assertTrue(any(event['event_type'] == 'progress_updated' for event in payload['platform_timeline_events']))
        self.assertEqual(payload['platform_recent_stage'], 'queued')
        self.assertTrue(any(artifact['artifact_kind'] == 'request' for artifact in payload['platform_artifacts']))
        self.assertTrue(any(artifact['artifact_kind'] == 'request' for artifact in payload['platform_download_artifacts']))
        self.assertIn('request', payload['platform_artifacts_by_kind'])

    def test_detector_display_environment_normalizes_to_standard_code(self) -> None:
        job = create_job('kpi-anomaly-detector', 'report.xlsx', 'report.xlsx')
        update_job(
            'kpi-anomaly-detector',
            job['id'],
            status='completed',
            current_record={
                'build': 'SBTS26R3.ENB.9999.260331.000003',
                'environment': 'T282.AP',
                'scenario': '60UE_UL_1530_1600',
            },
        )

        list_response = self.client.get('/kpi-anomaly-detector/')
        detail_response = self.client.get(f'/kpi-anomaly-detector/jobs/{job["id"]}')
        try:
            self.assertEqual(list_response.status_code, 200)
            self.assertEqual(detail_response.status_code, 200)
            self.assertIn(b'T282', list_response.data)
            self.assertNotIn(b'T282.AP</span>', list_response.data)
            self.assertIn(b'<dt>Environment</dt><dd>T282</dd>', detail_response.data)
            self.assertNotIn(b'<dt>Environment</dt><dd>T282.AP</dd>', detail_response.data)
        finally:
            list_response.close()
            detail_response.close()
            delete_job('kpi-anomaly-detector', job['id'])

    def test_generator_index_shows_fixed_template_set_options(self) -> None:
        self.generator_template_patch.stop()
        fixed_patch = patch.object(
            KpiGeneratorAdapter,
            'template_set_options',
            return_value={
                'options': [
                    {'name': 'ivy_26R1_vdt', 'template_count': 0, 'template_names': []},
                    {'name': 'ivy_26R2_vdt', 'template_count': 0, 'template_names': []},
                ],
                'error': '',
            },
        )
        fixed_patch.start()

        try:
            response = self.client.get('/kpi-generator/')
        finally:
            fixed_patch.stop()
            self.generator_template_patch.start()

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'name="template_set_name"', response.data)
        self.assertIn(b'kpi-generator-template-set-options', response.data)
        self.assertIn(b'Leave empty, choose a preset, or type a custom template set', response.data)
        self.assertIn(b'ivy_26R1_vdt', response.data)
        self.assertIn(b'ivy_26R2_vdt', response.data)

    def test_detector_detail_artifact_route_serves_per_sheet_files(self) -> None:
        job = create_job('kpi-anomaly-detector', 'report.xlsx', 'report.xlsx')
        job_root = os.path.dirname(job['input_path'])
        html_path = os.path.join(job_root, 'NRCELL-101_trend_viewer.html')
        excel_path = os.path.join(job_root, 'NRCELL-101_analysis_report.xlsx')

        with open(html_path, 'w', encoding='utf-8') as stream:
            stream.write('<html><body>sheet html</body></html>')
        with open(excel_path, 'wb') as stream:
            stream.write(b'sheet excel')

        update_job(
            'kpi-anomaly-detector',
            job['id'],
            detail_html_paths=[html_path],
            detail_excel_paths=[excel_path],
            current_record={'portal_summary': {'sheet_results': [{'sheet_name': 'NRCELL-101'}]}},
        )

        html_response = None
        excel_response = None
        try:
            html_response = self.client.get(f'/kpi-anomaly-detector/jobs/{job["id"]}/detail-artifacts/html/0')
            excel_response = self.client.get(f'/kpi-anomaly-detector/jobs/{job["id"]}/detail-artifacts/excel/0')

            self.assertEqual(html_response.status_code, 200)
            self.assertIn(b'sheet html', html_response.data)
            self.assertEqual(excel_response.status_code, 200)
            self.assertEqual(excel_response.data, b'sheet excel')
        finally:
            if html_response is not None:
                html_response.close()
            if excel_response is not None:
                excel_response.close()
            delete_job('kpi-anomaly-detector', job['id'])

    def test_detector_api_and_list_page_include_per_sheet_download_artifacts(self) -> None:
        job = create_job('kpi-anomaly-detector', 'report.xlsx', 'report.xlsx')
        job_root = os.path.dirname(job['input_path'])
        html_path = os.path.join(job_root, 'NRCELL-101_trend_viewer.html')
        excel_path = os.path.join(job_root, 'NRCELL-101_analysis_report.xlsx')
        summary_html_path = os.path.join(job_root, 'summary_trend_viewer.html')
        portal_summary_path = os.path.join(job_root, 'portal_summary.json')

        with open(html_path, 'w', encoding='utf-8') as stream:
            stream.write('<html><body>sheet html</body></html>')
        with open(excel_path, 'wb') as stream:
            stream.write(b'sheet excel')
        with open(summary_html_path, 'w', encoding='utf-8') as stream:
            stream.write('<html><body>summary html</body></html>')
        with open(portal_summary_path, 'w', encoding='utf-8') as stream:
            stream.write('{}')

        update_job(
            'kpi-anomaly-detector',
            job['id'],
            status='completed',
            report_html_path=summary_html_path,
            report_excel_path=excel_path,
            report_data_path=portal_summary_path,
            detail_html_paths=[html_path],
            detail_excel_paths=[excel_path],
            current_record={
                'portal_summary': {
                    'sheet_results': [
                        {
                            'sheet_name': 'NRCELL-101',
                            'history_key': 'T080::demo::NRCELL-101',
                            'matched_history_count': 1,
                            'stats': {'severity_nohistory': 0},
                        }
                    ]
                }
            },
        )

        try:
            api_response = self.client.get(f'/kpi-anomaly-detector/api/jobs/{job["id"]}')
            list_response = self.client.get('/kpi-anomaly-detector/')
            detail_response = self.client.get(f'/kpi-anomaly-detector/jobs/{job["id"]}')
        finally:
            delete_job('kpi-anomaly-detector', job['id'])

        self.assertEqual(api_response.status_code, 200)
        self.assertEqual(detail_response.status_code, 200)
        payload = api_response.get_json()
        self.assertIsNotNone(payload)
        detail_artifacts = [
            item for item in payload['platform_download_artifacts']
            if item['artifact_kind'] in {'report_html_detail', 'report_excel_detail'}
        ]
        self.assertEqual(len(detail_artifacts), 2)
        self.assertTrue(any(item['download_href'].endswith('/detail-artifacts/html/0?v=' + item['download_href'].split('?v=')[-1]) for item in detail_artifacts if item['artifact_kind'] == 'report_html_detail'))
        self.assertTrue(any(item['download_href'].endswith('/detail-artifacts/excel/0') for item in detail_artifacts if item['artifact_kind'] == 'report_excel_detail'))
        self.assertIn(b'HTML', list_response.data)
        self.assertIn(b'ZIP', list_response.data)
        self.assertIn(f'/kpi-anomaly-detector/jobs/{job["id"]}/artifacts/html'.encode('utf-8'), list_response.data)
        self.assertIn(f'/kpi-anomaly-detector/jobs/{job["id"]}/artifacts/bundle'.encode('utf-8'), list_response.data)
        self.assertIn(f'/kpi-anomaly-detector/jobs/{job["id"]}/detail-artifacts/html/0'.encode('utf-8'), detail_response.data)
        self.assertIn(f'/kpi-anomaly-detector/jobs/{job["id"]}/detail-artifacts/excel/0'.encode('utf-8'), detail_response.data)

    def test_detector_detail_page_shows_previous_record_comparison_summary(self) -> None:
        job = create_job('kpi-anomaly-detector', 'report.xlsx', 'report.xlsx')
        job_root = os.path.dirname(job['input_path'])
        summary_html_path = os.path.join(job_root, 'summary_trend_viewer.html')

        with open(summary_html_path, 'w', encoding='utf-8') as stream:
            stream.write('<html><body>summary html</body></html>')

        update_job(
            'kpi-anomaly-detector',
            job['id'],
            status='completed',
            report_html_path=summary_html_path,
            stats={'inconsistent': 3},
            current_record={
                'comparison': {
                    'previous_file': 'baseline.xlsx',
                    'previous_time': '2026-04-01 01:00:00',
                    'delta_inconsistent': 1,
                    'new_inconsistent': ['KPI-003', 'KPI-001'],
                    'fixed': ['KPI-009'],
                    'persistent': ['KPI-002'],
                    'prev_stats': {'inconsistent': 2},
                }
            },
        )

        try:
            detail_response = self.client.get(f'/kpi-anomaly-detector/jobs/{job["id"]}')
        finally:
            delete_job('kpi-anomaly-detector', job['id'])

        self.assertEqual(detail_response.status_code, 200)
        self.assertIn(b'History comparison', detail_response.data)
        self.assertIn(b'baseline.xlsx', detail_response.data)
        self.assertIn(b'Previous inconsistent</dt><dd>2</dd>', detail_response.data)
        self.assertIn(b'Current inconsistent</dt><dd>3</dd>', detail_response.data)
        self.assertIn(b'Delta inconsistent</dt><dd>+1</dd>', detail_response.data)
        self.assertIn(b'KPI-001, KPI-003', detail_response.data)
        self.assertIn(b'KPI-009', detail_response.data)
        self.assertIn(b'KPI-002', detail_response.data)

    def test_detector_detail_page_shows_filterable_severity_tracking_table(self) -> None:
        job = create_job('kpi-anomaly-detector', 'report.xlsx', 'report.xlsx')
        job_root = os.path.dirname(job['input_path'])
        summary_html_path = os.path.join(job_root, 'summary_trend_viewer.html')

        with open(summary_html_path, 'w', encoding='utf-8') as stream:
            stream.write('<html><body>summary html</body></html>')

        update_job(
            'kpi-anomaly-detector',
            job['id'],
            status='completed',
            report_html_path=summary_html_path,
            current_record={
                'portal_summary': {
                    'severity_tracking_rows': [
                        {
                            'Code': 'KPI-001',
                            'KPI Name': 'DL Throughput',
                            'Severity': 'Regression',
                            'Relative Change(%)': 3.5,
                            'Anomaly Count': 2,
                            'Prev Severity': 'Suspicious',
                            'Change Flag': 'WORSENED',
                        },
                        {
                            'Code': 'KPI-002',
                            'KPI Name': 'UL Throughput',
                            'Severity': 'Normal',
                            'Relative Change(%)': '',
                            'Anomaly Count': 0,
                            'Prev Severity': 'Regression',
                            'Change Flag': 'IMPROVED',
                        },
                    ]
                }
            },
        )

        try:
            detail_response = self.client.get(f'/kpi-anomaly-detector/jobs/{job["id"]}')
        finally:
            delete_job('kpi-anomaly-detector', job['id'])

        self.assertEqual(detail_response.status_code, 200)
        self.assertIn(b'Severity tracking', detail_response.data)
        self.assertIn(b'id="severity-tracking-table"', detail_response.data)
        self.assertIn(b'id="reset-severity-tracking-filters"', detail_response.data)
        self.assertIn(b'data-filter-label="Code"', detail_response.data)
        self.assertIn(b'data-filter-label="Change Flag"', detail_response.data)
        self.assertIn(b'KPI-001', detail_response.data)
        self.assertIn(b'DL Throughput', detail_response.data)
        self.assertIn(b'WORSENED', detail_response.data)
        self.assertIn(b'IMPROVED', detail_response.data)

    def test_detector_bundle_artifact_download_contains_job_outputs(self) -> None:
        job = create_job('kpi-anomaly-detector', 'report.xlsx', 'report.xlsx')
        job_root = os.path.dirname(job['input_path'])
        summary_html_path = os.path.join(job_root, 'summary_trend_viewer.html')
        stdout_path = os.path.join(job_root, 'stdout.log')

        with open(summary_html_path, 'w', encoding='utf-8') as stream:
            stream.write('<html><body>summary html</body></html>')
        with open(stdout_path, 'w', encoding='utf-8') as stream:
            stream.write('detector stdout')

        update_job(
            'kpi-anomaly-detector',
            job['id'],
            status='completed',
            report_html_path=summary_html_path,
            stdout_log_path=stdout_path,
        )

        response = self.client.get(f'/kpi-anomaly-detector/jobs/{job["id"]}/artifacts/bundle')
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, 'application/zip')
            archive = zipfile.ZipFile(io.BytesIO(response.data))
            names = archive.namelist()
            self.assertIn('summary_trend_viewer.html', names)
            self.assertIn('stdout.log', names)
        finally:
            response.close()
            delete_job('kpi-anomaly-detector', job['id'])

    def test_history_artifact_links_include_script_root_prefix(self) -> None:
        detector_job = create_job('kpi-anomaly-detector', 'report.xlsx', 'report.xlsx')
        detector_root = os.path.dirname(detector_job['input_path'])
        detector_html_path = os.path.join(detector_root, 'summary_trend_viewer.html')
        with open(detector_html_path, 'w', encoding='utf-8') as stream:
            stream.write('<html><body>summary html</body></html>')
        update_job(
            'kpi-anomaly-detector',
            detector_job['id'],
            status='completed',
            report_html_path=detector_html_path,
        )

        generator_job = create_job('kpi-generator', 'request.json', 'request.json')
        generator_root = os.path.dirname(generator_job['input_path'])
        generator_report_path = os.path.join(generator_root, 'outputs', 'generated_report.xlsx')
        os.makedirs(os.path.dirname(generator_report_path), exist_ok=True)
        with open(generator_report_path, 'wb') as stream:
            stream.write(b'xlsx-data')
        update_job(
            'kpi-generator',
            generator_job['id'],
            status='completed',
            report_file_path=generator_report_path,
        )

        try:
            with self.client.application.test_request_context('/', environ_overrides={'SCRIPT_NAME': '/kpi-dashboard'}):
                detector_payload = get_kpi_detector_adapter().get_job(str(detector_job['id']))
                generator_payload = get_kpi_generator_adapter().get_job(str(generator_job['id']))

                self.assertIsNotNone(detector_payload)
                self.assertIsNotNone(generator_payload)
                self.assertTrue(
                    detector_payload['history_list_artifacts'][0]['download_href'].startswith(
                        url_for('kpi_detector.artifact', job_id=str(detector_job['id']), artifact_kind='html')
                    )
                )
                self.assertEqual(
                    generator_payload['history_list_artifacts'][0]['download_href'],
                    url_for('kpi_generator.artifact', job_id=str(generator_job['id']), artifact_kind='report'),
                )
        finally:
            delete_job('kpi-anomaly-detector', detector_job['id'])
            delete_job('kpi-generator', generator_job['id'])

    def test_detector_summary_html_relative_detail_link_resolves_as_report_asset(self) -> None:
        job = create_job('kpi-anomaly-detector', 'report.xlsx', 'report.xlsx')
        job_root = os.path.dirname(job['input_path'])
        detail_html_name = 'NRCELL-101_trend_viewer.html'
        detail_html_path = os.path.join(job_root, detail_html_name)
        summary_html_path = os.path.join(job_root, 'summary_trend_viewer.html')

        with open(detail_html_path, 'w', encoding='utf-8') as stream:
            stream.write('<html><body>sheet html</body></html>')
        with open(summary_html_path, 'w', encoding='utf-8') as stream:
            stream.write(f'<html><body><a href="{detail_html_name}">Open</a></body></html>')

        update_job(
            'kpi-anomaly-detector',
            job['id'],
            status='completed',
            report_html_path=summary_html_path,
        )

        summary_response = None
        relative_detail_response = None
        try:
            summary_response = self.client.get(f'/kpi-anomaly-detector/jobs/{job["id"]}/artifacts/html')
            relative_detail_response = self.client.get(f'/kpi-anomaly-detector/jobs/{job["id"]}/artifacts/{detail_html_name}')

            self.assertEqual(summary_response.status_code, 200)
            self.assertEqual(relative_detail_response.status_code, 200)
            self.assertIn(b'sheet html', relative_detail_response.data)
        finally:
            if summary_response is not None:
                summary_response.close()
            if relative_detail_response is not None:
                relative_detail_response.close()
            delete_job('kpi-anomaly-detector', job['id'])

    def test_detector_submit_rebuilds_invalid_filename_with_override_fields(self) -> None:
        response = self.client.post(
            '/kpi-anomaly-detector/submit',
            data={
                'filename_override_environment': 'T813.SCF.T813.demo',
                'filename_override_scenario': '7UE_DL_Burst',
                'files': (io.BytesIO(b'test workbook'), '0129.1_26R2.0126.7_1csv.xlsx'),
            },
            content_type='multipart/form-data',
        )

        self.assertEqual(response.status_code, 302)

        jobs = list_jobs('kpi-anomaly-detector', limit=10)
        self.assertEqual(len(jobs), 1)
        saved_job = load_job('kpi-anomaly-detector', str(jobs[0]['id']))

        self.assertIsNotNone(saved_job)
        self.assertEqual(saved_job['original_filename'], '0129.1_26R2.0126.7_T813.SCF.T813.DEMO_7UE_DL_Burst_1csv.xlsx')
        self.assertEqual(saved_job['uploaded_filename'], '0129.1_26R2.0126.7_1csv.xlsx')
        self.assertTrue(saved_job['filename_override_applied'])
        self.assertEqual(saved_job['environment'], 'T813')
        self.assertEqual(saved_job['scenario'], '7UE_DL_Burst')

    def test_detector_validate_upload_filenames_endpoint_reports_only_invalid_names(self) -> None:
        response = self.client.post(
            '/kpi-anomaly-detector/validate-upload-filenames',
            json={
                'filenames': [
                    'exec20260325T120349_SBTS26R3.ENB.9999.260319.000005_T813.SCF_7UE_DL_Burst_1csv.xlsx',
                    '0129.1_26R2.0126.7_1csv.xlsx',
                ]
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload['invalid_filenames'], ['0129.1_26R2.0126.7_1csv.xlsx'])
        self.assertTrue(payload['requires_override'])

    def test_detector_multi_file_batch_shows_latest_selected_file_first_in_job_list(self) -> None:
        response = self.client.post(
            '/kpi-anomaly-detector/submit',
            data={
                'files': [
                    (io.BytesIO(b'first workbook'), 'exec20260325T120349_SBTS26R3.ENB.9999.260319.000005_T813.SCF_7UE_DL_Burst_1csv.xlsx'),
                    (io.BytesIO(b'second workbook'), 'exec20260325T120349_SBTS26R3.ENB.9999.260319.000006_T813.SCF_8UE_Burst_1csv.xlsx'),
                ],
            },
            content_type='multipart/form-data',
        )

        self.assertEqual(response.status_code, 302)

        jobs = list_jobs('kpi-anomaly-detector', limit=10)
        self.assertEqual(len(jobs), 2)
        self.assertEqual(
            [job['original_filename'] for job in jobs],
            [
                'exec20260325T120349_SBTS26R3.ENB.9999.260319.000006_T813.SCF_8UE_Burst_1csv.xlsx',
                'exec20260325T120349_SBTS26R3.ENB.9999.260319.000005_T813.SCF_7UE_DL_Burst_1csv.xlsx',
            ],
        )
        self.assertEqual(jobs[0]['submission_index'], 1)
        self.assertEqual(jobs[1]['submission_index'], 0)
        self.assertEqual(jobs[0]['submission_batch_order'], jobs[1]['submission_batch_order'])

    def test_generator_recovery_adopts_running_process_and_dispatches_queued_jobs(self) -> None:
        running_job = create_job('kpi-generator', 'running.json', 'running.json')
        queued_job = create_job('kpi-generator', 'queued.json', 'queued.json')
        update_job(
            'kpi-generator',
            running_job['id'],
            status='running',
            process_pid=4242,
            queue_order=1,
        )
        update_job(
            'kpi-generator',
            queued_job['id'],
            status='queued',
            queue_order=2,
        )

        adapter = get_kpi_generator_adapter()
        with patch('portal.adapters.kpi_generator.get_unified_runner') as runner_factory, patch.object(adapter, '_is_process_alive', return_value=True):
            runner_factory.return_value.submit_threaded_job.return_value = True
            adapter.recover_startup_jobs()

        recovered_running_job = load_job('kpi-generator', str(running_job['id']))
        recovered_queued_job = load_job('kpi-generator', str(queued_job['id']))
        self.assertIsNotNone(recovered_running_job)
        self.assertIsNotNone(recovered_queued_job)
        self.assertEqual(recovered_running_job['status'], 'running')
        self.assertEqual(recovered_running_job['recovery_owner_pid'], os.getpid())
        self.assertEqual(recovered_queued_job['status'], 'running')
        self.assertEqual(recovered_queued_job['recovery_owner_pid'], os.getpid())
        self.assertEqual(runner_factory.return_value.submit_threaded_job.call_count, 2)
        self.assertEqual(
            [call.args[1] for call in runner_factory.return_value.submit_threaded_job.call_args_list],
            [str(running_job['id']), str(queued_job['id'])],
        )

    def test_generator_dispatch_starts_all_queued_jobs_in_parallel(self) -> None:
        first_job = create_job('kpi-generator', 'first.json', 'first.json')
        second_job = create_job('kpi-generator', 'second.json', 'second.json')
        update_job('kpi-generator', first_job['id'], status='queued', queue_order=1)
        update_job('kpi-generator', second_job['id'], status='queued', queue_order=2)

        adapter = get_kpi_generator_adapter()
        with patch('portal.adapters.kpi_generator.get_unified_runner') as runner_factory:
            runner_factory.return_value.submit_threaded_job.return_value = True
            runner_factory.return_value.submit_module_dispatcher.return_value = False
            adapter._start_next_queued_job()

        refreshed_first_job = load_job('kpi-generator', str(first_job['id']))
        refreshed_second_job = load_job('kpi-generator', str(second_job['id']))
        self.assertIsNotNone(refreshed_first_job)
        self.assertIsNotNone(refreshed_second_job)
        self.assertEqual(refreshed_first_job['status'], 'running')
        self.assertEqual(refreshed_second_job['status'], 'running')
        self.assertEqual(runner_factory.return_value.submit_threaded_job.call_count, 2)
        self.assertEqual(
            [call.args[1] for call in runner_factory.return_value.submit_threaded_job.call_args_list],
            [str(first_job['id']), str(second_job['id'])],
        )

    def test_detector_recovery_keeps_only_one_running_job(self) -> None:
        first_job = create_job('kpi-anomaly-detector', 'first.xlsx', 'first.xlsx')
        second_job = create_job('kpi-anomaly-detector', 'second.xlsx', 'second.xlsx')
        update_job(
            'kpi-anomaly-detector',
            first_job['id'],
            status='running',
            process_pid=5001,
            queue_order=1,
        )
        update_job(
            'kpi-anomaly-detector',
            second_job['id'],
            status='running',
            process_pid=5002,
            queue_order=2,
        )

        adapter = get_kpi_detector_adapter()
        with patch('portal.adapters.kpi_detector.get_unified_runner') as runner_factory, patch.object(adapter, '_is_process_alive', return_value=True):
            runner_factory.return_value.submit_threaded_job.return_value = True
            adapter.recover_startup_jobs()

        recovered_first_job = load_job('kpi-anomaly-detector', str(first_job['id']))
        recovered_second_job = load_job('kpi-anomaly-detector', str(second_job['id']))
        self.assertIsNotNone(recovered_first_job)
        self.assertIsNotNone(recovered_second_job)
        self.assertEqual(recovered_first_job['status'], 'running')
        self.assertEqual(recovered_first_job['recovery_owner_pid'], os.getpid())
        self.assertEqual(recovered_second_job['status'], 'failed')
        self.assertIn('already recovered after Portal restart', str(recovered_second_job.get('error_message') or ''))
        runner_factory.return_value.submit_threaded_job.assert_called_once()
        self.assertEqual(runner_factory.return_value.submit_threaded_job.call_args.args[1], str(first_job['id']))

    def test_create_app_triggers_startup_recovery(self) -> None:
        with patch('portal.app_factory.get_kpi_generator_adapter') as generator_factory, patch('portal.app_factory.get_kpi_detector_adapter') as detector_factory:
            generator_factory.return_value.recover_startup_jobs.return_value = None
            detector_factory.return_value.recover_startup_jobs.return_value = None

            app = create_app()

        self.assertIsNotNone(app)
        generator_factory.return_value.recover_startup_jobs.assert_called_once_with()
        detector_factory.return_value.recover_startup_jobs.assert_called_once_with()

    def test_generator_history_list_shows_report_and_zip_bundle(self) -> None:
        job = create_job('kpi-generator', 'request.json', 'request.json')
        job_root = os.path.dirname(job['input_path'])
        report_path = os.path.join(job_root, 'outputs', 'generated_report.xlsx')
        stdout_path = os.path.join(job_root, 'stdout.log')
        os.makedirs(os.path.dirname(report_path), exist_ok=True)

        with open(report_path, 'wb') as stream:
            stream.write(b'xlsx-data')
        with open(stdout_path, 'w', encoding='utf-8') as stream:
            stream.write('generator stdout')

        update_job(
            'kpi-generator',
            job['id'],
            status='completed',
            report_file_path=report_path,
            stdout_log_path=stdout_path,
            request_mode='generator',
            build='24A',
            environment='T813',
            scenario='Burst',
        )

        list_response = self.client.get('/kpi-generator/')
        bundle_response = self.client.get(f'/kpi-generator/jobs/{job["id"]}/artifacts/bundle')
        try:
            self.assertEqual(list_response.status_code, 200)
            self.assertIn(f'/kpi-generator/jobs/{job["id"]}/artifacts/report'.encode('utf-8'), list_response.data)
            self.assertIn(f'/kpi-generator/jobs/{job["id"]}/artifacts/bundle'.encode('utf-8'), list_response.data)
            self.assertEqual(bundle_response.status_code, 200)
            self.assertEqual(bundle_response.mimetype, 'application/zip')
            archive = zipfile.ZipFile(io.BytesIO(bundle_response.data))
            names = archive.namelist()
            self.assertIn('stdout.log', names)
            self.assertIn('outputs/generated_report.xlsx', names)
        finally:
            list_response.close()
            bundle_response.close()
            delete_job('kpi-generator', job['id'])

    def test_generator_history_list_normalizes_environment_display_code(self) -> None:
        job = create_job('kpi-generator', 'request.json', 'request.json')
        job_root = os.path.dirname(job['input_path'])
        report_path = os.path.join(job_root, 'outputs', 'generated_report.xlsx')
        os.makedirs(os.path.dirname(report_path), exist_ok=True)

        with open(report_path, 'wb') as stream:
            stream.write(b'xlsx-data')

        update_job(
            'kpi-generator',
            job['id'],
            status='completed',
            request_mode='scout_conversion',
            report_file_path=report_path,
            generated_filename='exec20260406T144606_SBTS26R3.ENB.9999.260331.000003_T282.AP_60UE_UL_1530_1600_0csv_nosplit_scout.xlsx',
            build='SBTS26R3.ENB.9999.260331.000003',
            environment='T282.AP',
            scenario='60UE_UL_1530_1600',
        )

        list_response = self.client.get('/kpi-generator/')
        try:
            self.assertEqual(list_response.status_code, 200)
            self.assertIn(b'Env', list_response.data)
            self.assertIn(b'T282', list_response.data)
            self.assertNotIn(b'T282.AP</span>', list_response.data)
        finally:
            list_response.close()
            delete_job('kpi-generator', job['id'])

    def test_generator_environment_filter_options_show_normalized_codes(self) -> None:
        job = create_job('kpi-generator', 'request.json', 'request.json')
        update_job(
            'kpi-generator',
            job['id'],
            status='completed',
            request_mode='scout_conversion',
            build='SBTS26R3.ENB.9999.260331.000003',
            environment='T282.AP',
            scenario='60UE_UL_1530_1600',
        )

        response = self.client.get('/kpi-generator/')
        try:
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'value="T282"', response.data)
            self.assertNotIn(b'T282.AP</option>', response.data)
        finally:
            response.close()
            delete_job('kpi-generator', job['id'])

    def test_generator_detail_page_shows_normalized_environment_code(self) -> None:
        job = create_job('kpi-generator', 'request.json', 'request.json')
        update_job(
            'kpi-generator',
            job['id'],
            status='completed',
            request_mode='scout_conversion',
            build='SBTS26R3.ENB.9999.260331.000003',
            environment='T282.AP',
            scenario='60UE_UL_1530_1600',
        )

        response = self.client.get(f'/kpi-generator/jobs/{job["id"]}')
        try:
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<dt>Env</dt><dd>T282</dd>', response.data)
            self.assertNotIn(b'<dt>Env</dt><dd>T282.AP</dd>', response.data)
        finally:
            response.close()
            delete_job('kpi-generator', job['id'])

    def test_generator_report_timestamps_use_server_time_labels_and_schedule(self) -> None:
        future_start = (datetime.now().astimezone() + timedelta(minutes=5)).replace(microsecond=0)
        future_end = future_start + timedelta(minutes=30)

        response = self.client.post(
            '/kpi-generator/jobs',
            data={
                'job_mode': 'generator',
                'template_set_name': 'DemoTemplateSet',
                'template_names': 'TemplateA',
                'build': '24A',
                'environment': 'T813.SCF.T813.demo',
                'scenario': 'Throughput',
                'report_timestamps_list': (
                    f'[["{future_start.strftime("%Y-%m-%d %H:%M:%S")}", '
                    f'"{future_end.strftime("%Y-%m-%d %H:%M:%S")}"]]'
                ),
            },
        )

        self.assertEqual(response.status_code, 302)

        jobs = list_jobs('kpi-generator', limit=10)
        self.assertEqual(len(jobs), 1)
        job_id = str(jobs[0]['id'])
        saved_job = load_job('kpi-generator', job_id)

        self.assertIsNotNone(saved_job)
        self.assertIsInstance(saved_job.get('latest_interval_end_at'), str)
        self.assertIn('T', str(saved_job.get('latest_interval_end_at') or ''))
        self.assertIsInstance(saved_job.get('scheduled_generate_start_at'), str)
        self.assertIn('T', str(saved_job.get('scheduled_generate_start_at') or ''))
        self.assertIn('Latest report end time is in the future.', str(saved_job.get('progress_message') or ''))
        self.assertNotIn('UTC', str(saved_job.get('progress_message') or ''))

        detail_response = self.client.get(f'/kpi-generator/jobs/{job_id}')
        list_response = self.client.get('/kpi-generator/')
        try:
            self.assertEqual(detail_response.status_code, 200)
            self.assertEqual(list_response.status_code, 200)
            self.assertIn(b'Latest end', detail_response.data)
            self.assertNotIn(b'Latest UTC end', detail_response.data)
            self.assertIn(b'Portal merged server-time ranges', detail_response.data)
            self.assertNotIn(b'Portal merged UTC ranges', detail_response.data)
            self.assertIn(b'Scheduled start', list_response.data)
            self.assertNotIn(b'Scheduled UTC start', list_response.data)
        finally:
            detail_response.close()
            list_response.close()
            delete_job('kpi-generator', job_id)

    def test_generator_detail_progress_updated_displays_server_time_text(self) -> None:
        job = create_job('kpi-generator', 'request.json', 'request.json')
        update_job(
            'kpi-generator',
            job['id'],
            status='running',
            request_mode='generator',
            progress_stage='template_request_started',
            progress_message='Requesting template report.',
            progress_updated_at='2026-04-07 03:41:09 UTC',
        )

        response = self.client.get(f'/kpi-generator/jobs/{job["id"]}')
        try:
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'template_request_started', response.data)
            self.assertIn(b'CST', response.data)
            self.assertNotIn(b'2026-04-07 03:41:09 UTC', response.data)
        finally:
            response.close()
            delete_job('kpi-generator', job['id'])

    def test_generator_visible_timestamps_do_not_show_utc(self) -> None:
        job = create_job('kpi-generator', 'request.json', 'request.json')
        update_job(
            'kpi-generator',
            job['id'],
            status='running',
            request_mode='generator',
            build='24A',
            environment='T813',
            scenario='Burst',
            progress_stage='template_request_started',
            progress_message='Requesting template report.',
            progress_updated_at='2026-04-07 03:41:09 UTC',
        )

        detail_response = self.client.get(f'/kpi-generator/jobs/{job["id"]}')
        list_response = self.client.get('/kpi-generator/')
        try:
            self.assertEqual(detail_response.status_code, 200)
            self.assertEqual(list_response.status_code, 200)
            self.assertIn(b'CST', detail_response.data)
            self.assertNotIn(b' UTC', detail_response.data)
            self.assertIn(b'CST', list_response.data)
            self.assertNotIn(b' UTC', list_response.data)
        finally:
            detail_response.close()
            list_response.close()
            delete_job('kpi-generator', job['id'])

    def test_detector_visible_timestamps_show_cst_without_utc(self) -> None:
        job = create_job('kpi-anomaly-detector', 'report.xlsx', 'report.xlsx')
        update_job(
            'kpi-anomaly-detector',
            job['id'],
            status='completed',
            started_at='2026-04-07 03:41:09 UTC',
            completed_at='2026-04-07 03:45:53 UTC',
            current_record={
                'build': 'SBTS26R3.ENB.9999.260331.000003',
                'environment': 'T282.AP',
                'scenario': '60UE_UL_1530_1600',
            },
        )

        detail_response = self.client.get(f'/kpi-anomaly-detector/jobs/{job["id"]}')
        list_response = self.client.get('/kpi-anomaly-detector/')
        try:
            self.assertEqual(detail_response.status_code, 200)
            self.assertEqual(list_response.status_code, 200)
            self.assertIn(b'CST', detail_response.data)
            self.assertNotIn(b' UTC', detail_response.data)
            self.assertIn(b'CST', list_response.data)
            self.assertNotIn(b' UTC', list_response.data)
        finally:
            detail_response.close()
            list_response.close()
            delete_job('kpi-anomaly-detector', job['id'])

    def test_generator_detail_shows_final_failure_request_data(self) -> None:
        job = create_job('kpi-generator', 'request.json', 'request.json')
        update_job(
            'kpi-generator',
            job['id'],
            status='failed',
            request_mode='generator',
            generation_result={
                'final_failure': {
                    'operation': 'compare',
                    'http_status': 200,
                    'attempt': 1,
                    'report_ids': ['1534183306'],
                    'request_data': {'reports': '1534183306'},
                    'response_body': '{"success": false, "error": "bad id", "data": null}',
                }
            },
        )

        response = self.client.get(f'/kpi-generator/jobs/{job["id"]}')
        try:
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'1534183306', response.data)
            self.assertIn(b'reports', response.data)
            self.assertIn(b'bad id', response.data)
        finally:
            response.close()
            delete_job('kpi-generator', job['id'])