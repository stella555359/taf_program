from __future__ import annotations

import unittest

from portal.schemas import DetectorPortalInput, GeneratorPortalInput, GeneratorScoutPortalInput, TrafficModelPortalInput


class PortalInputSchemaTests(unittest.TestCase):
    def test_generator_input_normalizes_common_fields(self) -> None:
        schema_input = GeneratorPortalInput.from_submission(
            template_set_name=' DemoSet ',
            template_names='Template A; Template B',
            build=' 24A ',
            environment=' t813 ',
            scenario=' Throughput ',
            report_timestamps_text=' [["2024-01-01 00:00:00", "2024-01-01 01:00:00"]] ',
            timestamp_delta_minutes=None,
            auto_detector=True,
            auto_detector_is_base_file=True,
            normalize_build=lambda value: value.strip().upper(),
            normalize_environment=lambda value: value.strip().upper(),
            parse_template_names=lambda value: [item.strip() for item in value.split(';') if item.strip()],
        )

        self.assertEqual(schema_input.common.job_mode, 'generator')
        self.assertEqual(schema_input.common.build, '24A')
        self.assertEqual(schema_input.common.environment, 'T813')
        self.assertEqual(schema_input.common.scenario, 'Throughput')
        self.assertTrue(schema_input.runtime_options.auto_detector)
        self.assertTrue(schema_input.runtime_options.auto_detector_is_base_file)

    def test_detector_input_derives_common_fields_from_filename_context(self) -> None:
        schema_input = DetectorPortalInput.from_filename(
            original_filename='exec20260325_SBTS26R3_T813_7UE_DL_Burst_1csv.xlsx',
            is_base_file=True,
            source_generator_job_id='generator-1',
            extract_filename_context=lambda _: {
                'matched': True,
                'build': 'SBTS26R3',
                'environment': 'T813',
                'scenario': '7UE_DL_Burst',
            },
            filename_rule_text='rule',
        )

        self.assertEqual(schema_input.common.job_mode, 'detector')
        self.assertEqual(schema_input.common.build, 'SBTS26R3')
        self.assertEqual(schema_input.common.environment, 'T813')
        self.assertEqual(schema_input.common.scenario, '7UE_DL_Burst')
        self.assertTrue(schema_input.runtime_options.as_base_file)
        self.assertEqual(schema_input.source_generator_job_id, 'generator-1')

    def test_traffic_model_input_uses_shared_runtime_fields(self) -> None:
        schema_input = TrafficModelPortalInput.from_form(
            environment='t282',
            selected_ue_indexes=[1, 2],
            dry_run=True,
            stop_on_failure=False,
            max_parallel_workers=6,
            log_level='debug',
            auto_generator=True,
            auto_detector=False,
            same_type_execution_mode='parallel',
            cross_type_execution_mode='serial',
            stage_execution_mode='parallel',
        )

        self.assertEqual(schema_input.common.job_mode, 'traffic_model')
        self.assertEqual(schema_input.common.environment, 'T282')
        self.assertTrue(schema_input.runtime_options.dry_run)
        self.assertFalse(schema_input.runtime_options.stop_on_failure)
        self.assertEqual(schema_input.runtime_options.max_parallel_workers, 6)
        self.assertEqual(schema_input.runtime_options.log_level, 'DEBUG')
        self.assertTrue(schema_input.runtime_options.auto_generator)