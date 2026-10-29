from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd


DETECTOR_SCRIPTS_PATH = Path(__file__).resolve().parents[2] / 'kpi-anomaly-detector' / 'scripts'
if str(DETECTOR_SCRIPTS_PATH) not in sys.path:
    sys.path.insert(0, str(DETECTOR_SCRIPTS_PATH))

from kpi_detector.detector import DetectorExecutionError, KPIAnomalyDetector  # noqa: E402


class DetectorValidationFailureTests(unittest.TestCase):
    @staticmethod
    def _valid_report_path(directory: str, filename: str = 'exec20260325T120349_SBTS26R3.ENB.9999.260319.000005_T813.SCF.T813.gNB.25R3.20260224_7UE_DL_Burst_1csv.xlsx') -> Path:
        return Path(directory) / filename

    @staticmethod
    def _stub_load_history(detector: KPIAnomalyDetector) -> None:
        detector.history_records = []
        detector.previous_record = None
        detector._all_history_records = []

    def test_detector_raises_when_input_has_no_valid_t_columns(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = self._valid_report_path(temp_dir)
            pd.DataFrame(
                {
                    'Code': ['DL_Throughput'],
                    'KPI Name': ['DL Throughput'],
                    'Value': [123.4],
                }
            ).to_excel(report_path, index=False)

            with patch.object(KPIAnomalyDetector, 'load_history', self._stub_load_history), patch.object(KPIAnomalyDetector, '_register_unknown_codes', return_value=None):
                detector = KPIAnomalyDetector(str(report_path))
                detector.load_data()

                with self.assertRaisesRegex(DetectorExecutionError, 'No valid KPI data columns found in input report'):
                    detector.analyze_consistency()

    def test_detector_raises_when_history_record_has_no_kpi_data(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = self._valid_report_path(temp_dir)
            pd.DataFrame(
                {
                    'Code': ['DL_Throughput'],
                    'KPI Name': ['DL Throughput'],
                    'T813.20260407_123456': [123.4],
                    'T813.20260407_124456': [125.0],
                }
            ).to_excel(report_path, index=False)

            with patch.object(KPIAnomalyDetector, 'load_history', self._stub_load_history), patch.object(KPIAnomalyDetector, '_register_unknown_codes', return_value=None):
                detector = KPIAnomalyDetector(str(report_path))
                detector.load_data()
                detector.analyze_consistency()
                detector.previous_record = {
                    'filename': 'baseline.xlsx',
                    'timestamp': '2026-04-07 12:34:56',
                    'kpi_data': {},
                }

                with self.assertRaisesRegex(DetectorExecutionError, 'No KPI data in history record: baseline.xlsx'):
                    detector.analyze_ttest_with_history()

    def test_build_current_record_includes_severity_tracking_rows_for_portal(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = self._valid_report_path(temp_dir)
            pd.DataFrame(
                {
                    'Code': ['KPI-001', 'KPI-002'],
                    'KPI Name': ['DL Throughput', 'UL Throughput'],
                    'T813.20260407_123456': [123.4, 88.0],
                    'T813.20260407_124456': [125.0, 88.5],
                }
            ).to_excel(report_path, index=False)

            with patch.object(KPIAnomalyDetector, 'load_history', self._stub_load_history), patch.object(KPIAnomalyDetector, '_register_unknown_codes', return_value=None):
                detector = KPIAnomalyDetector(str(report_path))
                detector.load_data()
                detector.analyze_consistency()
                detector.analysis_results['all_codes'] = pd.DataFrame(
                    [
                        {
                            'Code': 'KPI-001',
                            'KPI Name': 'DL Throughput',
                            'Severity': 'Regression',
                            'Current_Mean': 124.2,
                            'Hist_Mean': 120.0,
                            'Anomaly_Count': 2,
                        },
                        {
                            'Code': 'KPI-002',
                            'KPI Name': 'UL Throughput',
                            'Severity': 'Normal',
                            'Current_Mean': 88.25,
                            'Hist_Mean': 90.0,
                            'Anomaly_Count': 0,
                        },
                    ]
                )
                detector.previous_record = {
                    'code_severity': {
                        'KPI-001': 'Suspicious',
                        'KPI-002': 'Regression',
                    }
                }

                current_record = detector.build_current_record()

        portal_summary = current_record.get('portal_summary', {})
        severity_rows = portal_summary.get('severity_tracking_rows', [])
        self.assertEqual(portal_summary.get('report_mode'), 'single_sheet')
        self.assertEqual(portal_summary.get('severity_tracking_count'), 2)
        self.assertEqual(severity_rows[0]['Code'], 'KPI-001')
        self.assertEqual(severity_rows[0]['Prev Severity'], 'Suspicious')
        self.assertEqual(severity_rows[0]['Change Flag'], 'WORSENED')
        self.assertEqual(severity_rows[1]['Code'], 'KPI-002')
        self.assertEqual(severity_rows[1]['Severity'], 'Normal')
        self.assertEqual(severity_rows[1]['Change Flag'], 'IMPROVED')
