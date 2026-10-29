from __future__ import annotations

import os
import tempfile
import unittest
from unittest.mock import patch

from portal import create_app
from portal.adapters.kpi_generator import KpiGeneratorAdapter


class PortalSmokeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_env = dict(os.environ)
        os.environ['KPI_DASHBOARD_ENV'] = 'test'
        os.environ['KPI_SQLITE_PATH'] = os.path.join(self.temp_dir.name, 'portal-smoke.db')
        self.generator_template_patch = patch.object(KpiGeneratorAdapter, 'template_set_options', return_value={'options': [], 'error': ''})
        self.generator_template_patch.start()

        app = create_app()
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def tearDown(self) -> None:
        self.generator_template_patch.stop()
        os.environ.clear()
        os.environ.update(self.original_env)
        self.temp_dir.cleanup()

    def test_home_page_renders(self) -> None:
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'KPI Portal', response.data)

    def test_healthz_returns_ok(self) -> None:
        response = self.client.get('/healthz')
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload['status'], 'ok')
        self.assertEqual(payload['service'], 'kpi-dashboard')

    def test_detector_page_renders(self) -> None:
        response = self.client.get('/kpi-anomaly-detector/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'KPI Anomaly Detector', response.data)

    def test_generator_page_renders(self) -> None:
        response = self.client.get('/kpi-generator/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'KPI Generator', response.data)

    def test_traffic_model_page_renders(self) -> None:
        response = self.client.get('/kpi-traffic-model/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'KPI Traffic Model', response.data)