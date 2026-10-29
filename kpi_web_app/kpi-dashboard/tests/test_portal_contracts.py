from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import portal.adapters.kpi_generator as kpi_generator_module
from portal.adapters.kpi_detector import get_kpi_detector_adapter
from portal.adapters.kpi_generator import KpiGeneratorAdapter, get_kpi_generator_adapter
from portal.adapters.kpi_traffic_model import get_kpi_traffic_model_adapter
from portal.services.job_store import create_job, load_job


class PortalContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_env = dict(os.environ)
        os.environ['KPI_DASHBOARD_ENV'] = 'test'
        os.environ['KPI_SQLITE_PATH'] = os.path.join(self.temp_dir.name, 'portal-test.db')

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self.original_env)
        self.temp_dir.cleanup()

    def test_detector_module_contract_is_exposed(self) -> None:
        module = get_kpi_detector_adapter().describe_module()
        self.assertEqual(module['key'], 'kpi-anomaly-detector')
        self.assertTrue(module['capabilities']['supports_cancel'])
        self.assertIn('report_html', module['job_contract']['artifact_kinds'])
        self.assertEqual(module['summary_contract']['result_payload_key'], 'current_record')

    def test_generator_module_contract_is_exposed(self) -> None:
        with patch.object(KpiGeneratorAdapter, 'template_set_options', return_value={'options': [], 'error': ''}):
            module = get_kpi_generator_adapter().describe_module()
        self.assertEqual(module['key'], 'kpi-generator')
        self.assertTrue(module['capabilities']['supports_auto_trigger'])
        self.assertIn('detector_job_id', module['job_contract']['linked_job_fields'])
        self.assertEqual(module['summary_contract']['result_payload_key'], 'generation_result')

    def test_traffic_model_contract_is_exposed(self) -> None:
        module = get_kpi_traffic_model_adapter().describe_module()
        self.assertEqual(module['key'], 'kpi-traffic-model')
        self.assertTrue(module['capabilities']['supports_status_api'])
        self.assertIn('result', module['job_contract']['artifact_kinds'])
        self.assertEqual(module['summary_contract']['result_payload_key'], 'result_payload')

    def test_generator_cancel_uses_taskkill_fallback_on_windows(self) -> None:
        adapter = get_kpi_generator_adapter()
        completed = subprocess.CompletedProcess(args=['taskkill'], returncode=0)

        with patch.object(kpi_generator_module.os, 'name', 'nt'), \
             patch.object(adapter, '_is_process_alive', return_value=True), \
             patch.object(kpi_generator_module.os, 'kill', side_effect=OSError('no direct kill')), \
             patch.object(kpi_generator_module.time, 'time', side_effect=[0.0, 6.0]), \
             patch.object(kpi_generator_module.time, 'sleep', return_value=None), \
             patch.object(kpi_generator_module.subprocess, 'run', return_value=completed) as mocked_run:
            adapter._terminate_job_process({'process_pid': 4321})

        mocked_run.assert_called_once_with(
            ['taskkill', '/PID', '4321', '/T', '/F'],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10,
        )

    def test_detector_normalizes_multi_sheet_scout_artifacts(self) -> None:
        adapter = get_kpi_detector_adapter()

        normalized = adapter._normalize_result_payload(
            {
                'report_html_path': 'C:/tmp/summary_trend_viewer.html',
                'report_excel_path': 'C:/tmp/summary_trend_viewer.html',
                'report_data_path': 'C:/tmp/portal_summary.json',
                'detail_html_paths': [
                    'C:/tmp/NRCELL-101_trend_viewer.html',
                    'C:/tmp/NRCELL-102_trend_viewer.html',
                ],
                'detail_excel_paths': [
                    'C:/tmp/NRCELL-101_analysis_report.xlsx',
                    'C:/tmp/NRCELL-102_analysis_report.xlsx',
                ],
                'current_record': {'stats': {'severity_regression': 1}},
            }
        )

        self.assertEqual(normalized['report_html_path'], 'C:/tmp/summary_trend_viewer.html')
        self.assertEqual(normalized['report_excel_path'], 'C:/tmp/NRCELL-101_analysis_report.xlsx')
        self.assertEqual(normalized['detail_html_paths'][1], 'C:/tmp/NRCELL-102_trend_viewer.html')
        self.assertEqual(normalized['detail_excel_paths'][1], 'C:/tmp/NRCELL-102_analysis_report.xlsx')
        self.assertEqual(normalized['report_data_path'], 'C:/tmp/portal_summary.json')

    def test_detector_builds_sheet_artifacts_with_direct_download_metadata(self) -> None:
        adapter = get_kpi_detector_adapter()

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = os.path.join(temp_dir, 'job')
            os.makedirs(temp_root, exist_ok=True)
            input_path = os.path.join(temp_root, 'input.xlsx')
            html_path = os.path.join(temp_root, 'sheet1.html')
            excel_path = os.path.join(temp_root, 'sheet1.xlsx')
            with open(input_path, 'w', encoding='utf-8') as stream:
                stream.write('input')
            with open(html_path, 'w', encoding='utf-8') as stream:
                stream.write('<html></html>')
            with open(excel_path, 'w', encoding='utf-8') as stream:
                stream.write('excel')

            job = {
                'input_path': input_path,
                'portal_summary': {
                    'sheet_results': [
                        {
                            'sheet_name': 'NRCELL-101',
                            'history_key': 'T080::demo::NRCELL-101',
                            'matched_history_count': 2,
                            'stats': {'severity_nohistory': 0},
                        }
                    ]
                },
                'detail_html_paths': [html_path],
                'detail_excel_paths': [excel_path],
            }

            sheet_artifacts = adapter._build_sheet_artifacts(job)

        self.assertEqual(len(sheet_artifacts), 1)
        self.assertEqual(sheet_artifacts[0]['sheet_name'], 'NRCELL-101')
        self.assertTrue(sheet_artifacts[0]['html_available'])
        self.assertTrue(sheet_artifacts[0]['excel_available'])

    def test_detector_can_rebuild_invalid_filename_with_env_and_scenario(self) -> None:
        adapter = get_kpi_detector_adapter()

        resolved_filename, override_applied = adapter.resolve_submission_filename(
            '0129.1_26R2.0126.7_1csv.xlsx',
            override_environment='t813',
            override_scenario='7UE_DL_Burst',
        )

        self.assertTrue(override_applied)
        self.assertEqual(resolved_filename, '0129.1_26R2.0126.7_T813_7UE_DL_Burst_1csv.xlsx')
        self.assertIsNone(adapter.validate_filename(resolved_filename))

    def test_detector_finalize_failure_uses_stderr_as_error_message(self) -> None:
        adapter = get_kpi_detector_adapter()
        job = create_job('kpi-anomaly-detector', 'report.xlsx', 'report.xlsx')
        current_job = load_job('kpi-anomaly-detector', str(job['id']))

        self.assertIsNotNone(current_job)

        with patch.object(adapter, '_schedule_dispatch', return_value=None):
            adapter._finalize_job_after_process_exit(
                str(job['id']),
                current_job,
                stdout='',
                stderr='No KPI data in history record: baseline.xlsx',
                process_returncode=1,
            )

        refreshed_job = load_job('kpi-anomaly-detector', str(job['id']))
        self.assertIsNotNone(refreshed_job)
        self.assertEqual(refreshed_job['status'], 'failed')
        self.assertEqual(refreshed_job['error_message'], 'No KPI data in history record: baseline.xlsx')