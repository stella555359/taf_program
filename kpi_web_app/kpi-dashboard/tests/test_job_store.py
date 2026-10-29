from __future__ import annotations

import os
import tempfile
import unittest

from portal.services import job_store


class JobStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_env = dict(os.environ)
        os.environ['KPI_DASHBOARD_ENV'] = 'test'
        os.environ['KPI_JOB_STORE_BACKEND'] = 'sqlite'
        os.environ['KPI_SQLITE_PATH'] = os.path.join(self.temp_dir.name, 'job-store.db')

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self.original_env)
        self.temp_dir.cleanup()

    def test_sqlite_job_metadata_tables_track_links_artifacts_and_events(self) -> None:
        job = job_store.create_job('kpi-generator', 'request.json', 'request.json')
        updated_job = job_store.update_job(
            'kpi-generator',
            job['id'],
            detector_job_id='detector-123',
            auto_detector_enabled=True,
            auto_detector_status='queued',
            report_file_path='C:/tmp/report.xlsx',
            scout_report_path='C:/tmp/source.xlsx',
        )

        self.assertIsNotNone(updated_job)

        job_store.append_job_event('kpi-generator', job['id'], 'submitted', {'status': 'queued'})

        links = job_store.list_job_links('kpi-generator', job['id'])
        artifacts = job_store.list_job_artifacts('kpi-generator', job['id'])
        events = job_store.list_job_events('kpi-generator', job['id'])

        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]['link_kind'], 'auto_detector')
        self.assertEqual(links[0]['linked_module_key'], 'kpi-anomaly-detector')
        self.assertEqual(links[0]['linked_job_id'], 'detector-123')

        artifact_kinds = {artifact['artifact_kind'] for artifact in artifacts}
        self.assertIn('request', artifact_kinds)
        self.assertIn('stdout', artifact_kinds)
        self.assertIn('stderr', artifact_kinds)
        self.assertIn('result', artifact_kinds)
        self.assertIn('report', artifact_kinds)
        self.assertIn('source', artifact_kinds)

        event_types = [event['event_type'] for event in events]
        self.assertIn('job_created', event_types)
        self.assertIn('artifact_registered', event_types)
        self.assertIn('linked_job_added', event_types)
        self.assertIn('submitted', event_types)
        self.assertEqual(events[-1]['event_type'], 'submitted')
        self.assertEqual(events[-1]['payload']['status'], 'queued')

        deleted = job_store.delete_job('kpi-generator', job['id'])
        self.assertTrue(deleted)
        self.assertEqual(job_store.list_job_links('kpi-generator', job['id']), [])
        self.assertEqual(job_store.list_job_artifacts('kpi-generator', job['id']), [])
        self.assertEqual(job_store.list_job_events('kpi-generator', job['id']), [])

    def test_sqlite_job_metadata_tables_track_detail_detector_artifacts(self) -> None:
        job = job_store.create_job('kpi-anomaly-detector', 'report.xlsx', 'report.xlsx')
        updated_job = job_store.update_job(
            'kpi-anomaly-detector',
            job['id'],
            report_html_path='C:/tmp/summary_trend_viewer.html',
            report_excel_path='C:/tmp/NRCELL-101_analysis_report.xlsx',
            detail_html_paths=[
                'C:/tmp/NRCELL-101_trend_viewer.html',
                'C:/tmp/NRCELL-102_trend_viewer.html',
            ],
            detail_excel_paths=[
                'C:/tmp/NRCELL-101_analysis_report.xlsx',
                'C:/tmp/NRCELL-102_analysis_report.xlsx',
            ],
        )

        self.assertIsNotNone(updated_job)

        artifacts = job_store.list_job_artifacts('kpi-anomaly-detector', job['id'])
        detail_html_artifacts = [artifact for artifact in artifacts if artifact['artifact_kind'] == 'report_html_detail']
        detail_excel_artifacts = [artifact for artifact in artifacts if artifact['artifact_kind'] == 'report_excel_detail']

        self.assertEqual(len(detail_html_artifacts), 2)
        self.assertEqual(len(detail_excel_artifacts), 2)
        self.assertEqual(detail_html_artifacts[0]['payload']['field_name'], 'detail_html_paths')
        self.assertEqual(detail_excel_artifacts[1]['payload']['item_index'], 1)

    def test_list_jobs_uses_queue_order_for_same_created_at(self) -> None:
        first_job = job_store.create_job('kpi-anomaly-detector', 'first.xlsx', 'first.xlsx')
        second_job = job_store.create_job('kpi-anomaly-detector', 'second.xlsx', 'second.xlsx')

        same_created_at = '2026-04-06 12:00:00 UTC'
        job_store.update_job(
            'kpi-anomaly-detector',
            first_job['id'],
            created_at=same_created_at,
            queue_order=100,
        )
        job_store.update_job(
            'kpi-anomaly-detector',
            second_job['id'],
            created_at=same_created_at,
            queue_order=200,
        )

        jobs = job_store.list_jobs('kpi-anomaly-detector', limit=10)

        self.assertEqual(jobs[0]['id'], second_job['id'])
        self.assertEqual(jobs[1]['id'], first_job['id'])