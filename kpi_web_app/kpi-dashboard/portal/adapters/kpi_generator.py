from __future__ import annotations

import ast
import json
import os
import re
import signal
import subprocess
import sys
import threading
import time
import zipfile
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import quote

from flask import has_request_context, url_for
import requests
import urllib3
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from .base import BaseModuleAdapter
from ..schemas import GeneratorPortalInput, GeneratorScoutPortalInput, InputValidationError
from ..contracts import JobContract, ModuleCapabilityContract, SummaryContract
from ..config import get_config_value
from ..runners import get_unified_runner
from ..services.job_store import create_job, delete_job, list_jobs, load_job, module_jobs_root, parse_utc_text, update_job, utcnow_text
from ..services.repo_registry import get_repository


PROGRESS_PREFIX = '__KPI_PROGRESS__ '
DEFAULT_TEST_LINE_PREFIX = '7_5_UTE5G402'
ENVIRONMENT_CODE_PATTERN = re.compile(r'(^|[._])(T\d{3,4})(?=$|[._])', re.IGNORECASE)
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
TEMPLATE_NAME_DELIMITER_PATTERN = re.compile(r'[;；,，、|]+')
TEMPLATE_NAME_LINEBREAK_PATTERN = re.compile(r'[\r\n]+')
TEMPLATE_NAME_MULTI_SPACE_PATTERN = re.compile(r'\s{2,}|\t+')
SCOUT_REPORT_SHEET_NAME = 'Chart Data'
FUTURE_REPORT_START_DELAY_MINUTES = 40
COMPASS_LOGIN_URL = 'http://compass.dyn.nesc.nokia.net:8080/common/login_handle/'
COMPASS_TEMPLATE_SET_URL = 'http://compass.dyn.nesc.nokia.net:8080/kpi/kpi_template_set/'
COMPASS_TEMPLATE_SET_TIMEOUT_SECONDS = 60
COMPASS_TEMPLATE_SET_CACHE_TTL_SECONDS = 300
FIXED_TEMPLATE_SET_OPTIONS = [
    {
        'name': 'ivy_26R1_vdt',
        'template_count': 0,
        'template_names': [],
    },
    {
        'name': 'ivy_26R2_vdt',
        'template_count': 0,
        'template_names': [],
    },
]


def _server_timezone():
    return datetime.now().astimezone().tzinfo or timezone.utc


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class KpiGeneratorAdapter(BaseModuleAdapter):
    module_key = 'kpi-generator'
    cancel_message = 'Cancelled by user.'
    _template_set_cache: Dict[str, object] = {
        'expires_at': 0.0,
        'options': [],
        'error': '',
    }
    environment_test_line_map = {
        'T284': '7_5_UTE402T284',
        'T080': '7_5_UTE5G402T080',
        'T073': '7_5_CLOUD402T073',
        'T283': '7_5_UTE5G402T283',
        'T813': '7_5_UTE5G402T813',
        'T816': '7_5_UTE5G402T816',
    }
    operation_display_map = {
        'analysis': 'singe_report',
        'compare': 'compare_merge',
        'horizontal_merge': 'horizontal_merge',
        'scout_conversion': 'scout_to_compass',
    }

    @classmethod
    def normalize_dot_joined_token(cls, value: str) -> str:
        parts = [re.sub(r'[^A-Za-z0-9-]+', '', part) for part in re.split(r'[._]+', str(value or '').strip())]
        normalized_parts = [part for part in parts if part]
        return '.'.join(normalized_parts)

    @classmethod
    def normalize_build(cls, value: str) -> str:
        return cls.normalize_dot_joined_token(value)

    @classmethod
    def normalize_environment(cls, value: str) -> str:
        return cls.normalize_dot_joined_token(value)

    @classmethod
    def extract_environment_code(cls, value: str) -> str:
        normalized_environment = cls.normalize_environment(value)
        for segment in normalized_environment.split('.'):
            if re.fullmatch(r'T\d{3,4}', segment, flags=re.IGNORECASE):
                return segment.upper()
        match = ENVIRONMENT_CODE_PATTERN.search(normalized_environment)
        if match:
            return match.group(2).upper()
        raise ValueError('Env must contain a Txxx or Txxxx code, for example T813 or T1234.CB0099.xxxx.')

    @classmethod
    def resolve_test_line(cls, environment: str) -> str:
        environment_code = cls.extract_environment_code(environment)
        if environment_code in cls.environment_test_line_map:
            return cls.environment_test_line_map[environment_code]
        if re.fullmatch(r'T\d{3,4}', environment_code):
            return f'{DEFAULT_TEST_LINE_PREFIX}{environment_code}'
        raise ValueError('Env must match Txxx or Txxxx format, for example T812 or T1234.')

    def _build_job_label(self, template_set_name: str, build: str, environment: str, scenario: str, report_timestamps_text: str) -> str:
        summary = self._summarize_time_ranges(report_timestamps_text)
        return f'{template_set_name} / {self._display_environment_code(environment) or environment} / {build} / {scenario} / {summary}'

    def _build_history_title(self, build: str, environment: str) -> str:
        try:
            cleaned_environment = self.extract_environment_code(environment)
        except ValueError:
            cleaned_environment = str(environment or '').strip() or '-'
        cleaned_build = str(build or '').strip() or '-'
        return f'{cleaned_environment}_{cleaned_build}'

    @classmethod
    def _display_environment_code(cls, value: str) -> str:
        try:
            return cls.extract_environment_code(value)
        except ValueError:
            return str(value or '').strip()

    def _summarize_time_ranges(self, report_timestamps_text: str) -> str:
        try:
            parsed = ast.literal_eval(report_timestamps_text)
        except (SyntaxError, ValueError):
            return 'time ranges'
        if not isinstance(parsed, list) or not parsed:
            return 'time ranges'
        first_item = parsed[0] if isinstance(parsed[0], list) and len(parsed[0]) == 2 else None
        if first_item is None:
            return 'time ranges'
        more_count = max(len(parsed) - 1, 0)
        base = f'{first_item[0]} -> {first_item[1]}'
        if more_count:
            return f'{base} (+{more_count} more)'
        return base

    def _parse_timestamp_ranges(self, value: str) -> List[tuple[datetime, datetime]]:
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise ValueError('report_timestamps_list format is invalid.') from exc
        if not isinstance(parsed, list) or not parsed:
            raise ValueError('report_timestamps_list must contain at least one [start, end] pair.')

        intervals: List[tuple[datetime, datetime]] = []
        for item in parsed:
            if not isinstance(item, (list, tuple)) or len(item) != 2:
                raise ValueError('Each timestamp range must be [start_time, end_time].')
            try:
                start_time = self._parse_server_time_text(str(item[0]).strip())
                end_time = self._parse_server_time_text(str(item[1]).strip())
            except ValueError as exc:
                raise ValueError('Each timestamp must use server time format YYYY-MM-DD HH:MM:SS.') from exc
            if end_time <= start_time:
                raise ValueError('Each timestamp range must have end_time later than start_time.')
            intervals.append((start_time, end_time))
        return intervals

    def _parse_server_time_text(self, value: str) -> datetime:
        return datetime.strptime(value, TIMESTAMP_FORMAT).replace(tzinfo=_server_timezone())

    def _parse_schedule_time_text(self, value: str) -> Optional[datetime]:
        parsed_utc = parse_utc_text(value)
        if parsed_utc is not None:
            return parsed_utc.astimezone(_server_timezone())
        try:
            parsed = datetime.fromisoformat(str(value or '').strip())
        except ValueError:
            return None
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=_server_timezone())
        return parsed.astimezone(_server_timezone())

    def _format_server_time_text(self, value: datetime) -> str:
        return self._format_display_timestamp_text(value) or value.strftime('%Y-%m-%d %H:%M:%S CST')

    def _format_portal_timestamp_text(self, value: object) -> Optional[str]:
        return self._format_display_timestamp_text(value)

    def _format_timestamp_payload(self, value: object) -> object:
        return super()._format_timestamp_payload(value)

    def _decorate_platform_event_times(self, events: object) -> object:
        return super()._format_platform_events(events)

    def _decorate_platform_artifact_times(self, artifacts: object) -> object:
        return super()._format_platform_artifacts(artifacts)

    def _derive_schedule_fields(self, report_timestamps_text: str) -> Dict[str, Optional[str]]:
        intervals = self._parse_timestamp_ranges(report_timestamps_text)
        latest_end_time = max(end_time for _, end_time in intervals)
        scheduled_generate_start_at = None
        if latest_end_time > datetime.now(_server_timezone()):
            scheduled_generate_start_at = (
                latest_end_time + timedelta(minutes=FUTURE_REPORT_START_DELAY_MINUTES)
            ).isoformat()
        return {
            'latest_interval_end_at': latest_end_time.isoformat(),
            'scheduled_generate_start_at': scheduled_generate_start_at,
        }

    def _format_remaining_duration(self, total_seconds: int) -> str:
        remaining = max(int(total_seconds), 0)
        hours, remainder = divmod(remaining, 3600)
        minutes, seconds = divmod(remainder, 60)
        parts: List[str] = []
        if hours:
            parts.append(f'{hours}h')
        if minutes or hours:
            parts.append(f'{minutes}m')
        parts.append(f'{seconds}s')
        return ' '.join(parts)

    def _parse_template_names_text(self, value: str) -> List[str]:
        return self._parse_multi_value_text(value)

    def _parse_multi_value_text(self, value: str) -> List[str]:
        text = str(value or '').strip()
        if not text:
            return []

        if TEMPLATE_NAME_DELIMITER_PATTERN.search(text):
            raw_items = TEMPLATE_NAME_DELIMITER_PATTERN.split(text)
        elif TEMPLATE_NAME_LINEBREAK_PATTERN.search(text):
            raw_items = TEMPLATE_NAME_LINEBREAK_PATTERN.split(text)
        elif TEMPLATE_NAME_MULTI_SPACE_PATTERN.search(text):
            raw_items = TEMPLATE_NAME_MULTI_SPACE_PATTERN.split(text)
        else:
            raw_items = [text]

        normalized_items: List[str] = []
        seen: set[str] = set()
        for item in raw_items:
            normalized = str(item).strip()
            lowered = normalized.lower()
            if not normalized or lowered in seen:
                continue
            seen.add(lowered)
            normalized_items.append(normalized)
        return normalized_items

    def _summarize_dist_name_filters(self, filters: List[str]) -> str:
        if not filters:
            return '-'
        if len(filters) == 1:
            return filters[0]
        return f'{filters[0]} (+{len(filters) - 1} more)'

    def sample_command(self) -> str:
        return 'python kpi_generator.py --request-json request.json --output-dir outputs --result-json result.json'

    def capability_contract(self) -> ModuleCapabilityContract:
        return ModuleCapabilityContract(
            supports_cancel=True,
            supports_delete=True,
            supports_rerun=True,
            supports_preview=True,
            supports_auto_trigger=True,
            supports_status_api=True,
        )

    def job_contract(self) -> JobContract:
        return JobContract(
            module_key=self.module_key,
            statuses=['queued', 'running', 'completed', 'failed'],
            artifact_kinds=['request', 'result', 'report', 'source', 'stdout', 'stderr'],
            progress_fields=['progress_stage', 'progress_message', 'progress_updated_at'],
            linked_job_fields=['detector_job_id'],
        )

    def summary_contract(self) -> SummaryContract:
        return SummaryContract(
            result_payload_key='generation_result',
            summary_fields=['summary', 'generation_result', 'sheet_results', 'matched_dist_names'],
            ui_fields=['status', 'build', 'environment', 'scenario', 'generated_filename', 'auto_detector_status'],
        )

    def entrypoint_path(self) -> Path:
        return self.repository.repo_path / 'kpi_generator.py'

    def describe_module(self) -> Dict[str, object]:
        module = super().describe_module()
        template_set_payload = self.template_set_options()
        module['job_count'] = len(self.list_jobs(limit=100))
        module['environment_test_line_map'] = dict(self.environment_test_line_map)
        module['environment_fallback_prefix'] = DEFAULT_TEST_LINE_PREFIX
        module['filename_rule_text'] = 'Generated file names follow Date_Build_Env_Scenario_otherinfo.xlsx. Build comes from the form, Env comes from the selected environment, and Scenario comes from the form.'
        module['template_set_options'] = template_set_payload['options']
        module['template_set_error'] = template_set_payload['error']
        return module

    def template_set_options(self, force_refresh: bool = False) -> Dict[str, object]:
        return {
            'options': [dict(option) for option in FIXED_TEMPLATE_SET_OPTIONS],
            'error': '',
        }

    def filter_options(self) -> Dict[str, object]:
        jobs = self.list_jobs(limit=1000000)
        environments = sorted({
            self._display_environment_code(str(job.get('environment') or ''))
            for job in jobs
            if job.get('environment')
        })
        scenarios = sorted({
            str(job.get('scenario')).strip()
            for job in jobs
            if job.get('scenario')
        })
        return {
            'environments': environments,
            'scenarios': scenarios,
        }

    def list_jobs(self, limit: int = 20) -> List[Dict[str, object]]:
        jobs = []
        for job in list_jobs(self.module_key, limit=limit):
            jobs.append(self._refresh_job_state(job))
        return [self._decorate_job(job) for job in jobs]

    def query_jobs(
        self,
        search_query: str = '',
        status_query: str = '',
        environment_query: str = '',
        scenario_query: str = '',
        page: int = 1,
        page_size: int = 10,
    ) -> Dict[str, object]:
        jobs = self.list_jobs(limit=1000000)
        cleaned_query = search_query.strip().lower()
        cleaned_status = status_query.strip().lower()
        cleaned_environment = environment_query.strip().lower()
        cleaned_scenario = scenario_query.strip().lower()

        if cleaned_query:
            jobs = [
                job for job in jobs
                if cleaned_query in str(job.get('template_set_name', '')).lower()
                or cleaned_query in str(job.get('release', '')).lower()
                or cleaned_query in str(job.get('build', '')).lower()
                or cleaned_query in str(job.get('environment', '')).lower()
                or cleaned_query in str(job.get('scenario', '')).lower()
                or cleaned_query in str(job.get('dist_name_filter', '')).lower()
                or cleaned_query in str(job.get('scout_report_original_filename', '')).lower()
                or cleaned_query in str(job.get('generated_filename', '')).lower()
                or cleaned_query in str(job.get('id', '')).lower()
            ]

        if cleaned_status:
            jobs = [job for job in jobs if str(job.get('status', '')).lower() == cleaned_status]

        if cleaned_environment:
            jobs = [
                job for job in jobs
                if cleaned_environment in str(job.get('environment', '')).lower()
            ]

        if cleaned_scenario:
            jobs = [
                job for job in jobs
                if cleaned_scenario in str(job.get('scenario', '')).lower()
            ]

        total_count = len(jobs)
        total_pages = max((total_count + page_size - 1) // page_size, 1)
        current_page = min(max(page, 1), total_pages)
        start_index = (current_page - 1) * page_size
        end_index = start_index + page_size
        return {
            'jobs': jobs[start_index:end_index],
            'total_count': total_count,
            'total_pages': total_pages,
            'current_page': current_page,
            'page_size': page_size,
            'page_start': start_index + 1 if total_count else 0,
            'page_end': min(end_index, total_count),
        }

    def get_job(self, job_id: str) -> Optional[Dict[str, object]]:
        job = load_job(self.module_key, job_id)
        if job is None:
            return None
        job = self._refresh_job_state(job)
        return self._decorate_job(job)

    def submit(
        self,
        *,
        report_timestamps_text: str,
        template_set_name: str,
        template_names: str,
        build: str,
        environment: str,
        scenario: str,
        timestamp_delta_minutes: Optional[int],
        auto_detector: bool = False,
        auto_detector_is_base_file: bool = False,
    ) -> Dict[str, object]:
        try:
            schema_input = GeneratorPortalInput.from_submission(
                template_set_name=template_set_name,
                template_names=template_names,
                build=build,
                environment=environment,
                scenario=scenario,
                report_timestamps_text=report_timestamps_text,
                timestamp_delta_minutes=timestamp_delta_minutes,
                auto_detector=auto_detector,
                auto_detector_is_base_file=auto_detector_is_base_file,
                normalize_build=self.normalize_build,
                normalize_environment=self.normalize_environment,
                parse_template_names=self._parse_template_names_text,
            )
        except InputValidationError as exc:
            raise ValueError(str(exc)) from exc

        cleaned_template_set_name = schema_input.template_set_name
        parsed_template_names = list(schema_input.template_names)
        cleaned_build = str(schema_input.common.build or '')
        cleaned_environment = str(schema_input.common.environment or '')
        resolved_test_line = self.resolve_test_line(cleaned_environment)
        cleaned_scenario = str(schema_input.common.scenario or '')
        cleaned_text = schema_input.report_timestamps_text

        self._validate_timestamps_text(cleaned_text)
        schedule_fields = self._derive_schedule_fields(cleaned_text)
        timestamp_delta_minutes = schema_input.timestamp_delta_minutes
        if not self.entrypoint_path().exists():
            raise ValueError(f'kpi_generator entrypoint not found: {self.entrypoint_path()}')

        job_template_label = cleaned_template_set_name or '; '.join(parsed_template_names[:2])
        if len(parsed_template_names) > 2 and not cleaned_template_set_name:
            job_template_label = f'{job_template_label} (+{len(parsed_template_names) - 2} more)'
        job_label = self._build_job_label(job_template_label or 'manual templates', cleaned_build, cleaned_environment, cleaned_scenario, cleaned_text)
        job = create_job(self.module_key, job_label, 'request.json')
        request_path = Path(job['input_path'])
        output_dir = request_path.parent / 'outputs'
        request_payload = {
            'template_set_name': cleaned_template_set_name,
            'template_names': ';'.join(parsed_template_names),
            'build': cleaned_build,
            'environment': cleaned_environment,
            'scenario': cleaned_scenario,
            'report_timestamps_list': cleaned_text,
            'timestamp_delta_minutes': timestamp_delta_minutes,
            'job_mode': schema_input.common.job_mode,
            'auto_detector': schema_input.runtime_options.auto_detector,
            'auto_detector_is_base_file': schema_input.runtime_options.auto_detector_is_base_file,
        }
        request_path.write_text(json.dumps(request_payload, ensure_ascii=False, indent=2), encoding='utf-8')
        output_dir.mkdir(parents=True, exist_ok=True)

        update_job(
            self.module_key,
            job['id'],
            job_label=job_label,
            template_set_name=cleaned_template_set_name,
            manual_template_names=parsed_template_names,
            template_names_input=';'.join(parsed_template_names),
            build=cleaned_build,
            environment=cleaned_environment,
            scenario=cleaned_scenario,
            job_mode=schema_input.common.job_mode,
            test_line=resolved_test_line,
            report_timestamps_text=cleaned_text,
            timestamp_delta_minutes=timestamp_delta_minutes,
            output_dir=str(output_dir),
            command_preview=self._command_preview(request_path, output_dir, Path(job['result_json_path'])),
            generated_filename=None,
            final_operation=None,
            report_file_path=None,
            auto_detector_enabled=schema_input.runtime_options.auto_detector,
            auto_detector_is_base_file=schema_input.runtime_options.auto_detector_is_base_file,
            auto_detector_status='waiting_for_generator' if schema_input.runtime_options.auto_detector else 'disabled',
            auto_detector_message='Detector will be queued automatically after report generation succeeds.' if schema_input.runtime_options.auto_detector else 'Auto detector disabled.',
            detector_job_id=None,
            detector_reused_existing=False,
            progress_stage='queued',
            progress_message=(
                f"Latest report end time is in the future. Generator will start at {self._format_server_time_text(self._parse_schedule_time_text(schedule_fields['scheduled_generate_start_at']) or datetime.now(_server_timezone()))} "
                f'after waiting {FUTURE_REPORT_START_DELAY_MINUTES} minutes past the latest end time.'
                if schedule_fields['scheduled_generate_start_at']
                else 'Job queued.'
            ),
            progress_updated_at=utcnow_text(),
            latest_interval_end_at=schedule_fields['latest_interval_end_at'],
            scheduled_generate_start_at=schedule_fields['scheduled_generate_start_at'],
        )

        self._schedule_dispatch()
        return self.get_job(job['id']) or job

    def submit_scout_conversion(
        self,
        *,
        scout_report: FileStorage,
        dist_name_filter: str,
        build: str,
        environment: str,
        scenario: str,
        auto_detector: bool = False,
        auto_detector_is_base_file: bool = False,
    ) -> Dict[str, object]:
        try:
            schema_input = GeneratorScoutPortalInput.from_submission(
                build=build,
                environment=environment,
                scenario=scenario,
                dist_name_filter=dist_name_filter,
                scout_report_original_filename=scout_report.filename or 'scout_report.xlsx',
                auto_detector=auto_detector,
                auto_detector_is_base_file=auto_detector_is_base_file,
                normalize_build=self.normalize_build,
                normalize_environment=self.normalize_environment,
                parse_multi_value_text=self._parse_multi_value_text,
            )
        except InputValidationError as exc:
            raise ValueError(str(exc)) from exc

        cleaned_build = str(schema_input.common.build or '')
        cleaned_environment = str(schema_input.common.environment or '')
        resolved_test_line = self.resolve_test_line(cleaned_environment)
        cleaned_scenario = str(schema_input.common.scenario or '')
        cleaned_filter = schema_input.dist_name_filter
        parsed_filters = list(schema_input.dist_name_filters)
        original_filename = schema_input.scout_report_original_filename
        if not self.entrypoint_path().exists():
            raise ValueError(f'kpi_generator entrypoint not found: {self.entrypoint_path()}')

        job_label = f'SCOUT / {cleaned_environment} / {cleaned_build} / {cleaned_scenario} / {self._summarize_dist_name_filters(parsed_filters)}'
        job = create_job(self.module_key, job_label, 'request.json')
        request_path = Path(job['input_path'])
        output_dir = request_path.parent / 'outputs'
        output_dir.mkdir(parents=True, exist_ok=True)

        safe_name = secure_filename(original_filename) or 'scout_report.xlsx'
        scout_report_path = request_path.parent / safe_name
        scout_report.save(scout_report_path)

        request_payload = {
            'job_mode': 'scout_conversion',
            'build': cleaned_build,
            'environment': cleaned_environment,
            'scenario': cleaned_scenario,
            'job_mode': schema_input.common.job_mode,
            'dist_name_filter': cleaned_filter,
            'dist_name_filters': parsed_filters,
            'scout_report_original_filename': original_filename,
            'scout_report_path': str(scout_report_path),
            'auto_detector': schema_input.runtime_options.auto_detector,
            'auto_detector_is_base_file': schema_input.runtime_options.auto_detector_is_base_file,
        }
        request_path.write_text(json.dumps(request_payload, ensure_ascii=False, indent=2), encoding='utf-8')

        update_job(
            self.module_key,
            job['id'],
            job_label=job_label,
            request_mode='scout_conversion',
            build=cleaned_build,
            environment=cleaned_environment,
            scenario=cleaned_scenario,
            job_mode=schema_input.common.job_mode,
            test_line=resolved_test_line,
            dist_name_filter=cleaned_filter,
            dist_name_filters=parsed_filters,
            scout_report_path=str(scout_report_path),
            scout_report_original_filename=original_filename,
            output_dir=str(output_dir),
            command_preview=self._scout_command_preview(
                scout_report_path=scout_report_path,
                result_path=Path(job['result_json_path']),
                build=cleaned_build,
                environment=cleaned_environment,
                scenario=cleaned_scenario,
                dist_name_filter=cleaned_filter,
            ),
            generated_filename=None,
            final_operation='scout_conversion',
            report_file_path=None,
            auto_detector_enabled=schema_input.runtime_options.auto_detector,
            auto_detector_is_base_file=schema_input.runtime_options.auto_detector_is_base_file,
            auto_detector_status='waiting_for_generator' if schema_input.runtime_options.auto_detector else 'disabled',
            auto_detector_message='Detector will be queued automatically after conversion succeeds.' if schema_input.runtime_options.auto_detector else 'Auto detector disabled.',
            detector_job_id=None,
            detector_reused_existing=False,
            progress_stage='queued',
            progress_message='Scout conversion job queued.',
            progress_updated_at=utcnow_text(),
        )

        self._schedule_dispatch()
        return self.get_job(job['id']) or job

    def rerun(self, source_job_id: str) -> Dict[str, object]:
        source_job = self.get_job(source_job_id)
        if source_job is None:
            raise FileNotFoundError(f'Job not found: {source_job_id}')
        request_mode = str(source_job.get('request_mode') or 'generator')
        request_path = Path(str(source_job['input_path']))
        if not request_path.exists():
            raise FileNotFoundError(f'Request file not found for job: {source_job_id}')
        payload = json.loads(request_path.read_text(encoding='utf-8'))

        if request_mode == 'scout_conversion':
            scout_report_path = Path(str(payload.get('scout_report_path') or source_job.get('scout_report_path') or ''))
            if not scout_report_path.exists():
                raise FileNotFoundError(f'Scout report file not found for job: {source_job_id}')
            job = self.submit_scout_conversion_from_path(
                scout_report_path=scout_report_path,
                scout_report_original_filename=str(payload.get('scout_report_original_filename') or source_job.get('scout_report_original_filename') or scout_report_path.name),
                dist_name_filter=str(payload.get('dist_name_filter') or source_job.get('dist_name_filter') or ''),
                build=str(payload.get('build') or source_job.get('build') or ''),
                environment=str(payload.get('environment') or source_job.get('environment') or ''),
                scenario=str(payload.get('scenario') or source_job.get('scenario') or ''),
                auto_detector=bool(payload.get('auto_detector') if payload.get('auto_detector') is not None else source_job.get('auto_detector_enabled')),
                auto_detector_is_base_file=bool(payload.get('auto_detector_is_base_file') if payload.get('auto_detector_is_base_file') is not None else source_job.get('auto_detector_is_base_file')),
            )
            return job

        raw_delta = payload.get('timestamp_delta_minutes')
        delta = int(raw_delta) if raw_delta not in (None, '') else None
        return self.submit(
            report_timestamps_text=str(payload.get('report_timestamps_list') or ''),
            template_set_name=str(payload.get('template_set_name') or source_job.get('template_set_name') or payload.get('release') or source_job.get('release') or ''),
            template_names=str(payload.get('template_names') or source_job.get('template_names_input') or ''),
            build=str(payload.get('build') or ''),
            environment=str(payload.get('environment') or ''),
            scenario=str(payload.get('scenario') or ''),
            timestamp_delta_minutes=delta,
            auto_detector=bool(payload.get('auto_detector') if payload.get('auto_detector') is not None else source_job.get('auto_detector_enabled')),
            auto_detector_is_base_file=bool(payload.get('auto_detector_is_base_file') if payload.get('auto_detector_is_base_file') is not None else source_job.get('auto_detector_is_base_file')),
        )

    def submit_scout_conversion_from_path(
        self,
        *,
        scout_report_path: Path,
        scout_report_original_filename: str,
        dist_name_filter: str,
        build: str,
        environment: str,
        scenario: str,
        auto_detector: bool = False,
        auto_detector_is_base_file: bool = False,
    ) -> Dict[str, object]:
        try:
            schema_input = GeneratorScoutPortalInput.from_submission(
                build=build,
                environment=environment,
                scenario=scenario,
                dist_name_filter=dist_name_filter,
                scout_report_original_filename=scout_report_original_filename,
                auto_detector=auto_detector,
                auto_detector_is_base_file=auto_detector_is_base_file,
                normalize_build=self.normalize_build,
                normalize_environment=self.normalize_environment,
                parse_multi_value_text=self._parse_multi_value_text,
            )
        except InputValidationError as exc:
            raise ValueError(str(exc)) from exc

        cleaned_build = str(schema_input.common.build or '')
        cleaned_environment = str(schema_input.common.environment or '')
        resolved_test_line = self.resolve_test_line(cleaned_environment)
        cleaned_scenario = str(schema_input.common.scenario or '')
        cleaned_filter = schema_input.dist_name_filter
        parsed_filters = list(schema_input.dist_name_filters)
        if not scout_report_path.exists():
            raise FileNotFoundError(f'Scout report not found: {scout_report_path}')

        job_label = f'SCOUT / {cleaned_environment} / {cleaned_build} / {cleaned_scenario} / {self._summarize_dist_name_filters(parsed_filters)}'
        job = create_job(self.module_key, job_label, 'request.json')
        request_path = Path(job['input_path'])
        output_dir = request_path.parent / 'outputs'
        output_dir.mkdir(parents=True, exist_ok=True)

        copied_report_path = request_path.parent / scout_report_path.name
        copied_report_path.write_bytes(scout_report_path.read_bytes())
        request_payload = {
            'job_mode': 'scout_conversion',
            'build': cleaned_build,
            'environment': cleaned_environment,
            'scenario': cleaned_scenario,
            'job_mode': schema_input.common.job_mode,
            'dist_name_filter': cleaned_filter,
            'dist_name_filters': parsed_filters,
            'scout_report_original_filename': schema_input.scout_report_original_filename,
            'scout_report_path': str(copied_report_path),
            'auto_detector': schema_input.runtime_options.auto_detector,
            'auto_detector_is_base_file': schema_input.runtime_options.auto_detector_is_base_file,
        }
        request_path.write_text(json.dumps(request_payload, ensure_ascii=False, indent=2), encoding='utf-8')

        update_job(
            self.module_key,
            job['id'],
            job_label=job_label,
            request_mode='scout_conversion',
            build=cleaned_build,
            environment=cleaned_environment,
            scenario=cleaned_scenario,
            job_mode=schema_input.common.job_mode,
            test_line=resolved_test_line,
            dist_name_filter=cleaned_filter,
            dist_name_filters=parsed_filters,
            scout_report_path=str(copied_report_path),
            scout_report_original_filename=schema_input.scout_report_original_filename,
            output_dir=str(output_dir),
            command_preview=self._scout_command_preview(
                scout_report_path=copied_report_path,
                result_path=Path(job['result_json_path']),
                build=cleaned_build,
                environment=cleaned_environment,
                scenario=cleaned_scenario,
                dist_name_filter=cleaned_filter,
            ),
            generated_filename=None,
            final_operation='scout_conversion',
            report_file_path=None,
            auto_detector_enabled=schema_input.runtime_options.auto_detector,
            auto_detector_is_base_file=schema_input.runtime_options.auto_detector_is_base_file,
            auto_detector_status='waiting_for_generator' if schema_input.runtime_options.auto_detector else 'disabled',
            auto_detector_message='Detector will be queued automatically after conversion succeeds.' if schema_input.runtime_options.auto_detector else 'Auto detector disabled.',
            detector_job_id=None,
            detector_reused_existing=False,
            progress_stage='queued',
            progress_message='Scout conversion job queued.',
            progress_updated_at=utcnow_text(),
        )

        self._schedule_dispatch()
        return self.get_job(job['id']) or job

    def _schedule_dispatch(self) -> None:
        get_unified_runner().submit_module_dispatcher(self.module_key, self._dispatch_queued_jobs)

    def _dispatch_queued_jobs(self) -> None:
        self._start_next_queued_job()

    @contextmanager
    def _dispatch_lock(self):
        lock_path = module_jobs_root(self.module_key) / '.dispatch.lock'
        lock_path.touch(exist_ok=True)
        with lock_path.open('r+', encoding='utf-8') as handle:
            if os.name == 'nt':
                import msvcrt

                if handle.read(1) == '':
                    handle.seek(0)
                    handle.write('0')
                    handle.flush()
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
                try:
                    yield
                finally:
                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
                try:
                    yield
                finally:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def _start_next_queued_job(self) -> None:
        selected_job_ids: List[str] = []
        with self._dispatch_lock():
            raw_jobs = list_jobs(self.module_key, limit=1000000)
            for raw_job in raw_jobs:
                if str(raw_job.get('status') or '') == 'running':
                    self._refresh_job_state(raw_job)

            queued_jobs = [job for job in list_jobs(self.module_key, limit=1000000) if str(job.get('status') or '') == 'queued']
            if not queued_jobs:
                return

            queued_jobs.sort(key=self._job_order_key)
            for queued_job in queued_jobs:
                selected_job_id = str(queued_job['id'])
                updated_job = update_job(
                    self.module_key,
                    selected_job_id,
                    status='running',
                    started_at=utcnow_text(),
                    completed_at=None,
                    error_message=None,
                    cancel_requested_at=None,
                    process_pid=None,
                    recovery_owner_pid=os.getpid(),
                )
                if updated_job is not None:
                    selected_job_ids.append(selected_job_id)

        if not selected_job_ids:
            return

        for selected_job_id in selected_job_ids:
            try:
                submitted = get_unified_runner().submit_threaded_job(self.module_key, selected_job_id, lambda job_id=selected_job_id: self._run_job(job_id))
                if not submitted:
                    continue
            except RuntimeError as exc:
                update_job(
                    self.module_key,
                    selected_job_id,
                    status='failed',
                    completed_at=utcnow_text(),
                    error_message=f'Unable to start generator worker: {exc}',
                    process_pid=None,
                    recovery_owner_pid=None,
                )
        self._schedule_dispatch()

    def _job_order_key(self, item: Dict[str, object]) -> tuple[int, str, str]:
        return (
            int(item.get('queue_order') or 0),
            str(item.get('created_at') or ''),
            str(item.get('id') or ''),
        )

    def recover_startup_jobs(self) -> None:
        with self._dispatch_lock():
            raw_jobs = list_jobs(self.module_key, limit=1000000)
            running_jobs = [job for job in raw_jobs if str(job.get('status') or '') == 'running']
            running_jobs.sort(key=self._job_order_key)

            for raw_job in running_jobs:
                refreshed_job = self._refresh_job_state(raw_job)
                if str(refreshed_job.get('status') or '') != 'running':
                    continue

                owner_pid = refreshed_job.get('recovery_owner_pid')
                try:
                    owner_pid = int(owner_pid) if owner_pid not in (None, '') else None
                except (TypeError, ValueError):
                    owner_pid = None
                if owner_pid and owner_pid != os.getpid() and self._is_process_alive(owner_pid):
                    continue

                process_pid = self._job_pid(refreshed_job)
                if process_pid is None:
                    update_job(
                        self.module_key,
                        str(refreshed_job['id']),
                        status='failed',
                        completed_at=utcnow_text(),
                        error_message='kpi_generator job could not be recovered after Portal restart because no process pid was recorded.',
                        process_pid=None,
                        recovery_owner_pid=None,
                    )
                    continue

                if not self._is_process_alive(process_pid):
                    self._refresh_job_state(refreshed_job)
                    continue

                update_job(self.module_key, str(refreshed_job['id']), recovery_owner_pid=os.getpid())

                submitted = get_unified_runner().submit_threaded_job(
                    self.module_key,
                    str(refreshed_job['id']),
                    lambda job_id=str(refreshed_job['id']): self._monitor_running_job(job_id),
                )
                if not submitted:
                    update_job(self.module_key, str(refreshed_job['id']), recovery_owner_pid=None)

        self._start_next_queued_job()

    def _monitor_running_job(self, job_id: str) -> None:
        job = load_job(self.module_key, job_id)
        if job is None:
            self._schedule_dispatch()
            return

        if str(job.get('status') or '') != 'running':
            self._schedule_dispatch()
            return

        process_pid = self._job_pid(job)
        if process_pid is None or not self._is_process_alive(process_pid):
            self._refresh_job_state(job)
            self._schedule_dispatch()
            return

        while self._is_process_alive(process_pid):
            current_job = load_job(self.module_key, job_id)
            if current_job is None:
                return
            if str(current_job.get('status') or '') != 'running':
                self._schedule_dispatch()
                return
            if str(current_job.get('error_message') or '') == self.cancel_message:
                self._terminate_job_process(current_job)
            time.sleep(1)

        current_job = load_job(self.module_key, job_id)
        if current_job is None:
            self._schedule_dispatch()
            return

        stdout_path = Path(str(current_job['stdout_log_path']))
        stderr_path = Path(str(current_job['stderr_log_path']))
        stdout = stdout_path.read_text(encoding='utf-8') if stdout_path.exists() else ''
        stderr = stderr_path.read_text(encoding='utf-8') if stderr_path.exists() else ''
        request_mode = str(current_job.get('request_mode') or 'generator')
        self._finalize_job_after_process_exit(
            job_id,
            current_job,
            request_mode=request_mode,
            stdout=stdout,
            stderr=stderr,
            process_returncode=None,
        )

    def _finalize_job_after_process_exit(
        self,
        job_id: str,
        current_job: Dict[str, object],
        *,
        request_mode: str,
        stdout: str,
        stderr: str,
        process_returncode: Optional[int],
    ) -> None:
        result_path = Path(str(current_job['result_json_path']))
        if str(current_job.get('status') or '') == 'failed' and str(current_job.get('error_message') or '') == self.cancel_message:
            update_job(self.module_key, job_id, process_pid=None, recovery_owner_pid=None)
            self._schedule_dispatch()
            return

        failure_payload = None
        if result_path.exists():
            try:
                failure_payload = json.loads(result_path.read_text(encoding='utf-8'))
            except json.JSONDecodeError:
                failure_payload = None

        final_failure = failure_payload.get('final_failure') if isinstance(failure_payload, dict) and isinstance(failure_payload.get('final_failure'), dict) else {}
        final_failure_message = str(final_failure.get('exception') or final_failure.get('response_body') or '').strip()

        if process_returncode not in (None, 0) or final_failure:
            update_job(
                self.module_key,
                job_id,
                status='failed',
                completed_at=utcnow_text(),
                error_message=(final_failure_message or stderr or stdout or 'kpi_generator execution failed.').strip(),
                process_pid=None,
                recovery_owner_pid=None,
                report_file_path=(failure_payload.get('report_file_path') or failure_payload.get('output_path')) if failure_payload else None,
                generated_filename=failure_payload.get('final_filename') if failure_payload else None,
                final_operation=(failure_payload.get('final_operation') if failure_payload else None) or ('scout_conversion' if request_mode == 'scout_conversion' else None),
                build=failure_payload.get('build') if failure_payload else current_job.get('build'),
                environment=self.normalize_environment(str(failure_payload.get('environment') if failure_payload else current_job.get('environment') or '')),
                scenario=failure_payload.get('scenario') if failure_payload else current_job.get('scenario'),
                test_line=failure_payload.get('test_line') if failure_payload else current_job.get('test_line'),
                dist_name_filter=(failure_payload.get('dist_name_filter') if failure_payload else None) or current_job.get('dist_name_filter'),
                dist_name_filters=(failure_payload.get('dist_name_filters') if failure_payload else None) or current_job.get('dist_name_filters') or [],
                summary=(failure_payload or {}).get('summary') or current_job.get('summary') or {},
                generation_result=failure_payload,
                auto_detector_status='skipped' if current_job.get('auto_detector_enabled') else 'disabled',
                auto_detector_message='Generator did not complete, detector was not started.' if current_job.get('auto_detector_enabled') else 'Auto detector disabled.',
                auto_detector_is_base_file=bool(current_job.get('auto_detector_is_base_file')),
                detector_job_id=None,
                detector_reused_existing=False,
                progress_stage='failed',
                progress_message='kpi_generator execution failed.',
                progress_updated_at=utcnow_text(),
            )
            self._schedule_dispatch()
            return

        if not result_path.exists():
            update_job(
                self.module_key,
                job_id,
                status='failed',
                completed_at=utcnow_text(),
                error_message='kpi_generator finished without producing result metadata.',
                process_pid=None,
                recovery_owner_pid=None,
                auto_detector_status='skipped' if current_job.get('auto_detector_enabled') else 'disabled',
                auto_detector_message='Generator finished without result metadata, detector was not started.' if current_job.get('auto_detector_enabled') else 'Auto detector disabled.',
                auto_detector_is_base_file=bool(current_job.get('auto_detector_is_base_file')),
                detector_job_id=None,
                detector_reused_existing=False,
                progress_stage='failed',
                progress_message='kpi_generator finished without producing result metadata.',
                progress_updated_at=utcnow_text(),
            )
            self._schedule_dispatch()
            return

        try:
            payload = json.loads(result_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            update_job(
                self.module_key,
                job_id,
                status='failed',
                completed_at=utcnow_text(),
                error_message='kpi_generator produced an unreadable result metadata file.',
                process_pid=None,
                recovery_owner_pid=None,
                auto_detector_status='skipped' if current_job.get('auto_detector_enabled') else 'disabled',
                auto_detector_message='Generator produced unreadable result metadata, detector was not started.' if current_job.get('auto_detector_enabled') else 'Auto detector disabled.',
                auto_detector_is_base_file=bool(current_job.get('auto_detector_is_base_file')),
                detector_job_id=None,
                detector_reused_existing=False,
                progress_stage='failed',
                progress_message='kpi_generator produced an unreadable result metadata file.',
                progress_updated_at=utcnow_text(),
            )
            self._schedule_dispatch()
            return

        summary = payload.get('summary') or {}
        if request_mode == 'scout_conversion':
            summary = {
                **summary,
                'dist_name_filter_count': len(payload.get('dist_name_filters') or []),
                'matched_dist_name_count': len(payload.get('matched_dist_names') or []),
                'sheet_count': len(payload.get('sheet_results') or []),
                'timestamp_count': len(payload.get('timestamp_headers') or []),
                'group_row_count': payload.get('group_row_count'),
            }
        auto_detector_fields = self._prepare_auto_detector_fields(current_job, payload)
        update_job(
            self.module_key,
            job_id,
            status='completed',
            completed_at=utcnow_text(),
            error_message=None,
            process_pid=None,
            recovery_owner_pid=None,
            report_file_path=payload.get('report_file_path') or payload.get('output_path'),
            generated_filename=payload.get('final_filename'),
            final_operation=payload.get('final_operation') or ('scout_conversion' if request_mode == 'scout_conversion' else None),
            build=payload.get('build'),
            environment=self.normalize_environment(str(payload.get('environment') or '')),
            scenario=payload.get('scenario'),
            test_line=payload.get('test_line'),
            dist_name_filter=payload.get('dist_name_filter') or current_job.get('dist_name_filter'),
            dist_name_filters=payload.get('dist_name_filters') or current_job.get('dist_name_filters') or [],
            summary=summary,
            generation_result=payload,
            **auto_detector_fields,
            progress_stage='completed',
            progress_message='KPI generator job completed.',
            progress_updated_at=utcnow_text(),
        )
        self._schedule_dispatch()

    def cancel(self, job_id: str) -> Dict[str, object]:
        job = load_job(self.module_key, job_id)
        if job is None:
            raise FileNotFoundError(f'Job not found: {job_id}')
        status = str(job.get('status') or '')
        if status not in {'queued', 'running'}:
            raise ValueError('Only queued or running jobs can be cancelled.')

        self._terminate_job_process(job)
        updated_job = update_job(
            self.module_key,
            job_id,
            status='failed',
            completed_at=utcnow_text(),
            error_message=self.cancel_message,
            process_pid=None,
            progress_stage='failed',
            progress_message=self.cancel_message,
            progress_updated_at=utcnow_text(),
        )
        return self._decorate_job(updated_job or job)

    def delete(self, job_id: str) -> Dict[str, object]:
        job = self.get_job(job_id)
        if job is None:
            raise FileNotFoundError(f'Job not found: {job_id}')
        if str(job.get('status')) in {'queued', 'running'}:
            raise ValueError('Running or queued jobs cannot be deleted.')
        delete_job(self.module_key, job_id)
        return {'id': job_id}

    def artifact_path(self, job: Dict[str, object], artifact_kind: str) -> Optional[Path]:
        if artifact_kind == 'bundle':
            return self._history_bundle_path(job)

        mapping = {
            'request': 'input_path',
            'source': 'scout_report_path',
            'stdout': 'stdout_log_path',
            'stderr': 'stderr_log_path',
            'result': 'result_json_path',
            'report': 'report_file_path',
        }
        key = mapping.get(artifact_kind)
        if not key:
            return None
        raw_path = job.get(key)
        if not raw_path:
            return None
        path = Path(str(raw_path))
        return path if path.exists() else None

    def _validate_timestamps_text(self, value: str) -> None:
        self._parse_timestamp_ranges(value)

    def _command_preview(self, request_path: Path, output_dir: Path, result_path: Path) -> str:
        return f'{sys.executable} {self.entrypoint_path()} --request-json {request_path} --output-dir {output_dir} --result-json {result_path}'

    def _scout_command_preview(
        self,
        *,
        scout_report_path: Path,
        result_path: Path,
        build: str,
        environment: str,
        scenario: str,
        dist_name_filter: str,
    ) -> str:
        return (
            f'{sys.executable} {self.entrypoint_path()} --scout-report {scout_report_path} '
            f'--dist-name "{dist_name_filter}" --build {build} --environment {environment} '
            f'--scenario {scenario} --sheet-name {SCOUT_REPORT_SHEET_NAME} --result-json {result_path}'
        )

    def _run_job(self, job_id: str) -> None:
        job = self._wait_for_scheduled_start(job_id)
        if job is None:
            return

        request_path = Path(job['input_path'])
        result_path = Path(job['result_json_path'])
        output_dir = Path(str(job.get('output_dir') or request_path.parent / 'outputs'))
        output_dir.mkdir(parents=True, exist_ok=True)
        request_mode = str(job.get('request_mode') or 'generator')

        update_job(
            self.module_key,
            job_id,
            status='running',
            started_at=utcnow_text(),
            completed_at=None,
            error_message=None,
            recovery_owner_pid=os.getpid(),
            progress_stage='starting',
            progress_message='Starting kpi_generator process.',
            progress_updated_at=utcnow_text(),
        )

        popen_kwargs = {
            'cwd': str(self.repository.repo_path),
            'text': True,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
        }
        if os.name == 'nt':
            popen_kwargs['creationflags'] = getattr(subprocess, 'CREATE_NEW_PROCESS_GROUP', 0)
        else:
            popen_kwargs['start_new_session'] = True

        generator_python = str(get_config_value('KPI_GENERATOR_PYTHON', '') or '').strip() or sys.executable
        command = [generator_python, str(self.entrypoint_path())]
        if request_mode == 'scout_conversion':
            scout_report_path = Path(str(job.get('scout_report_path') or ''))
            command.extend([
                '--scout-report', str(scout_report_path),
                '--dist-name', str(job.get('dist_name_filter') or ''),
                '--build', str(job.get('build') or ''),
                '--environment', str(job.get('environment') or ''),
                '--scenario', str(job.get('scenario') or ''),
                '--sheet-name', SCOUT_REPORT_SHEET_NAME,
                '--result-json', str(result_path),
            ])
        else:
            command.extend([
                '--request-json', str(request_path),
                '--output-dir', str(output_dir),
                '--result-json', str(result_path),
            ])

        process = subprocess.Popen(command, **popen_kwargs)
        update_job(self.module_key, job_id, process_pid=process.pid)
        stdout_path = Path(job['stdout_log_path'])
        stderr_path = Path(job['stderr_log_path'])
        stdout_path.parent.mkdir(parents=True, exist_ok=True)
        stdout_path.touch(exist_ok=True)
        stderr_path.touch(exist_ok=True)

        with stdout_path.open('w', encoding='utf-8') as stdout_file, stderr_path.open('w', encoding='utf-8') as stderr_file:
            stdout_thread = threading.Thread(
                target=self._stream_process_output,
                args=(job_id, process.stdout, stdout_file, True),
                daemon=True,
            )
            stderr_thread = threading.Thread(
                target=self._stream_process_output,
                args=(job_id, process.stderr, stderr_file, False),
                daemon=True,
            )
            stdout_thread.start()
            stderr_thread.start()
            process.wait()
            stdout_thread.join()
            stderr_thread.join()

        stderr = stderr_path.read_text(encoding='utf-8') if stderr_path.exists() else ''
        stdout = stdout_path.read_text(encoding='utf-8') if stdout_path.exists() else ''

        current_job = load_job(self.module_key, job_id)
        if current_job is None:
            self._schedule_dispatch()
            return
        self._finalize_job_after_process_exit(
            job_id,
            current_job,
            request_mode=request_mode,
            stdout=stdout,
            stderr=stderr,
            process_returncode=process.returncode,
        )

    def _prepare_auto_detector_fields(self, job: Dict[str, object], payload: Dict[str, object]) -> Dict[str, object]:
        if not bool(job.get('auto_detector_enabled')):
            return {
                'auto_detector_enabled': False,
                'auto_detector_is_base_file': False,
                'auto_detector_status': 'disabled',
                'auto_detector_message': 'Auto detector disabled.',
                'detector_job_id': None,
                'detector_reused_existing': False,
            }

        report_file_value = payload.get('report_file_path') or payload.get('output_path')
        if not report_file_value:
            return {
                'auto_detector_enabled': True,
                'auto_detector_is_base_file': bool(job.get('auto_detector_is_base_file')),
                'auto_detector_status': 'failed',
                'auto_detector_message': 'Generator completed but did not return a detector input file.',
                'detector_job_id': None,
                'detector_reused_existing': False,
            }

        report_file_path = Path(str(report_file_value))
        if not report_file_path.exists():
            return {
                'auto_detector_enabled': True,
                'auto_detector_is_base_file': bool(job.get('auto_detector_is_base_file')),
                'auto_detector_status': 'failed',
                'auto_detector_message': f'Generator completed but report file is missing: {report_file_path}',
                'detector_job_id': None,
                'detector_reused_existing': False,
            }

        generated_filename = str(payload.get('final_filename') or report_file_path.name)
        try:
            from .kpi_detector import get_kpi_detector_adapter

            detector_job = get_kpi_detector_adapter().submit_existing_file(
                report_file_path=report_file_path,
                original_filename=generated_filename,
                is_base_file=bool(job.get('auto_detector_is_base_file')),
                source_generator_job_id=str(job['id']),
            )
        except Exception as exc:
            return {
                'auto_detector_enabled': True,
                'auto_detector_is_base_file': bool(job.get('auto_detector_is_base_file')),
                'auto_detector_status': 'failed',
                'auto_detector_message': f'Auto detector enqueue failed: {exc}',
                'detector_job_id': None,
                'detector_reused_existing': False,
            }

        reused_existing = bool(detector_job.get('reused_existing'))
        detector_status = str(detector_job.get('status') or 'queued')
        detector_job_id = str(detector_job.get('id') or '') or None
        message = 'Detector job queued automatically.'
        if reused_existing:
            message = 'Detector job queued automatically by reusing the latest matching detector job.'
        return {
            'auto_detector_enabled': True,
            'auto_detector_is_base_file': bool(job.get('auto_detector_is_base_file')),
            'auto_detector_status': detector_status,
            'auto_detector_message': message,
            'detector_job_id': detector_job_id,
            'detector_reused_existing': reused_existing,
        }

    def _stream_process_output(
        self,
        job_id: str,
        stream,
        target_file,
        parse_progress: bool,
    ) -> None:
        if stream is None:
            return

        try:
            for line in iter(stream.readline, ''):
                if not line:
                    break
                if parse_progress and line.startswith(PROGRESS_PREFIX):
                    self._apply_progress_event(job_id, line[len(PROGRESS_PREFIX):].strip())
                    continue
                target_file.write(line)
                target_file.flush()
        finally:
            stream.close()

    def _apply_progress_event(self, job_id: str, event_text: str) -> None:
        try:
            event = json.loads(event_text)
        except json.JSONDecodeError:
            return

        update_fields: Dict[str, object] = {
            'progress_stage': event.get('stage') or 'running',
            'progress_message': event.get('message') or 'Running kpi_generator job.',
            'progress_updated_at': utcnow_text(),
        }

        mapping = {
            'template_count': 'template_count',
            'original_interval_count': 'original_interval_count',
            'expanded_interval_count': 'expanded_interval_count',
            'successful_template_count': 'successful_template_count',
            'failed_template_count': 'failed_template_count',
            'interval_index': 'current_interval_index',
            'interval_start': 'current_interval_start',
            'interval_end': 'current_interval_end',
            'template_index': 'current_template_index',
            'template_total': 'current_template_total',
            'template_name': 'current_template_name',
            'template_attempt': 'current_template_attempt',
            'template_attempt_total': 'current_template_attempt_total',
            'report_id': 'current_report_id',
            'combined_report_id': 'current_combined_report_id',
            'generated_report_count': 'generated_report_count',
            'combined_report_count': 'combined_report_count',
            'final_operation': 'final_operation',
            'final_filename': 'generated_filename',
            'report_file_path': 'report_file_path',
            'request_timeout_seconds': 'current_request_timeout_seconds',
            'retry_delay_seconds': 'current_retry_delay_seconds',
            'error': 'current_template_error',
            'matched_dist_name_count': 'matched_dist_name_count',
            'timestamp_count': 'timestamp_count',
            'row_count': 'group_row_count',
        }
        for event_key, job_key in mapping.items():
            if event_key in event and event[event_key] not in (None, ''):
                update_fields[job_key] = event[event_key]

        update_job(self.module_key, job_id, **update_fields)

    def _wait_for_scheduled_start(self, job_id: str) -> Optional[Dict[str, object]]:
        job = load_job(self.module_key, job_id)
        if job is None:
            return None

        scheduled_start_at = parse_utc_text(str(job.get('scheduled_generate_start_at') or ''))
        if scheduled_start_at is None:
            return job

        latest_interval_end_at = str(job.get('latest_interval_end_at') or '')
        update_job(
            self.module_key,
            job_id,
            progress_stage='waiting_for_future_server_window',
            progress_message=(
                f'Latest report end time is {self._format_server_time_text(self._parse_schedule_time_text(latest_interval_end_at) or datetime.now(_server_timezone()))}. '
                f'Generator will start at {self._format_server_time_text(scheduled_start_at)} '
                f'after waiting {FUTURE_REPORT_START_DELAY_MINUTES} minutes past that server time.'
            ),
            progress_updated_at=utcnow_text(),
        )

        while True:
            current_job = load_job(self.module_key, job_id)
            if current_job is None:
                return None
            if str(current_job.get('status') or '') == 'failed' and str(current_job.get('error_message') or '') == self.cancel_message:
                return None

            remaining_seconds = (scheduled_start_at - datetime.now(_server_timezone())).total_seconds()
            if remaining_seconds <= 0:
                break
            time.sleep(min(max(remaining_seconds, 0.0), 2.0))

        refreshed_job = update_job(
            self.module_key,
            job_id,
            progress_stage='starting',
            progress_message='Scheduled server-time start reached. Starting kpi_generator process.',
            progress_updated_at=utcnow_text(),
        )
        return refreshed_job or load_job(self.module_key, job_id)

    def _refresh_job_state(self, job: Dict[str, object]) -> Dict[str, object]:
        status = str(job.get('status') or '')
        if status != 'running':
            return job
        process_pid = self._job_pid(job)
        if process_pid and not self._is_process_alive(process_pid):
            refreshed = update_job(
                self.module_key,
                str(job['id']),
                status='failed',
                completed_at=utcnow_text(),
                error_message='kpi_generator process exited before the Portal recorded a final status.',
                process_pid=None,
                recovery_owner_pid=None,
            )
            return refreshed or job
        return job

    def _decorate_job(self, job: Dict[str, object]) -> Dict[str, object]:
        decorated = dict(job)
        result_payload = decorated.get('generation_result') if isinstance(decorated.get('generation_result'), dict) else {}
        decorated['generation_result'] = result_payload
        decorated['request_mode'] = decorated.get('request_mode') or result_payload.get('request_mode') or 'generator'
        decorated['request_mode_display'] = 'scout_conversion' if decorated['request_mode'] == 'scout_conversion' else 'compass_generator'
        decorated['template_set_name'] = decorated.get('template_set_name') or result_payload.get('template_set_name') or decorated.get('release') or result_payload.get('release')
        decorated['manual_template_names'] = decorated.get('manual_template_names') if isinstance(decorated.get('manual_template_names'), list) else (result_payload.get('manual_template_names') or self._parse_template_names_text(str(decorated.get('template_names_input') or '')))
        decorated['template_names_input'] = decorated.get('template_names_input') or ';'.join(decorated['manual_template_names'])
        decorated['build'] = decorated.get('build') or result_payload.get('build')
        decorated['environment'] = decorated.get('environment') or result_payload.get('environment')
        decorated['scenario'] = decorated.get('scenario') or result_payload.get('scenario')
        try:
            decorated['display_environment'] = self.extract_environment_code(str(decorated.get('environment') or ''))
        except ValueError:
            decorated['display_environment'] = str(decorated.get('environment') or '')
        decorated['test_line'] = decorated.get('test_line') or result_payload.get('test_line')
        decorated['dist_name_filter'] = decorated.get('dist_name_filter') or result_payload.get('dist_name_filter')
        decorated['scout_report_original_filename'] = decorated.get('scout_report_original_filename') or result_payload.get('scout_report_original_filename')
        decorated['generated_filename'] = decorated.get('generated_filename') or result_payload.get('final_filename')
        decorated['created_at'] = self._format_portal_timestamp_text(decorated.get('created_at')) or decorated.get('created_at')
        decorated['started_at'] = self._format_portal_timestamp_text(decorated.get('started_at')) or decorated.get('started_at')
        decorated['completed_at'] = self._format_portal_timestamp_text(decorated.get('completed_at')) or decorated.get('completed_at')
        decorated['progress_updated_at'] = self._format_portal_timestamp_text(decorated.get('progress_updated_at')) or decorated.get('progress_updated_at')
        decorated['auto_detector_enabled'] = bool(decorated.get('auto_detector_enabled'))
        decorated['auto_detector_is_base_file'] = bool(decorated.get('auto_detector_is_base_file')) if decorated['auto_detector_enabled'] else False
        if decorated['auto_detector_enabled']:
            decorated['auto_detector_status'] = decorated.get('auto_detector_status') or 'waiting_for_generator'
            decorated['auto_detector_message'] = decorated.get('auto_detector_message') or 'Detector will be queued automatically after report generation succeeds.'
        else:
            decorated['auto_detector_status'] = decorated.get('auto_detector_status') or 'disabled'
            decorated['auto_detector_message'] = decorated.get('auto_detector_message') or 'Auto detector disabled.'
        decorated['detector_job_id'] = decorated.get('detector_job_id') or None
        decorated['detector_reused_existing'] = bool(decorated.get('detector_reused_existing'))
        if decorated['detector_job_id']:
            try:
                from .kpi_detector import get_kpi_detector_adapter

                linked_detector_job = get_kpi_detector_adapter().get_job(str(decorated['detector_job_id']))
            except Exception:
                linked_detector_job = None
            if linked_detector_job is not None:
                decorated['linked_detector_job'] = linked_detector_job
                decorated['auto_detector_status'] = str(linked_detector_job.get('status') or decorated['auto_detector_status'])
                if linked_detector_job.get('is_base_file') is not None:
                    decorated['auto_detector_is_base_file'] = bool(linked_detector_job.get('is_base_file'))
        else:
            decorated['linked_detector_job'] = None
        decorated['history_title'] = self._build_history_title(str(decorated.get('build') or ''), str(decorated.get('environment') or ''))
        decorated['history_time_summary'] = self._summarize_time_ranges(str(decorated.get('report_timestamps_text') or ''))
        latest_interval_end_at = str(decorated.get('latest_interval_end_at') or '')
        scheduled_generate_start_at = str(decorated.get('scheduled_generate_start_at') or '')
        latest_interval_end_dt = self._parse_schedule_time_text(latest_interval_end_at)
        scheduled_generate_start_dt = self._parse_schedule_time_text(scheduled_generate_start_at)
        remaining_seconds = 0
        if scheduled_generate_start_dt is not None:
            remaining_seconds = max(int((scheduled_generate_start_dt - datetime.now(_server_timezone())).total_seconds()), 0)
        decorated['latest_interval_end_at'] = self._format_server_time_text(latest_interval_end_dt) if latest_interval_end_dt else None
        decorated['scheduled_generate_start_at'] = self._format_server_time_text(scheduled_generate_start_dt) if scheduled_generate_start_dt else None
        decorated['latest_interval_end_at_iso'] = latest_interval_end_dt.isoformat() if latest_interval_end_dt else ''
        decorated['scheduled_generate_start_at_iso'] = scheduled_generate_start_dt.isoformat() if scheduled_generate_start_dt else ''
        decorated['generate_start_remaining_seconds'] = remaining_seconds
        decorated['generate_start_remaining_text'] = self._format_remaining_duration(remaining_seconds) if scheduled_generate_start_dt else ''
        decorated['waiting_to_start_generate'] = bool(
            scheduled_generate_start_dt is not None
            and str(decorated.get('status') or '') == 'queued'
            and remaining_seconds > 0
        )
        decorated['final_operation'] = decorated.get('final_operation') or result_payload.get('final_operation')
        if decorated['request_mode'] == 'scout_conversion':
            decorated['final_operation'] = decorated.get('final_operation') or 'scout_conversion'
        decorated['final_operation_display'] = self.operation_display_map.get(str(decorated.get('final_operation') or ''), decorated.get('final_operation') or '-')
        decorated['matched_dist_names'] = result_payload.get('matched_dist_names') or []
        decorated['dist_name_filters'] = decorated.get('dist_name_filters') if isinstance(decorated.get('dist_name_filters'), list) else (result_payload.get('dist_name_filters') or self._parse_multi_value_text(str(decorated.get('dist_name_filter') or '')))
        decorated['sheet_results'] = result_payload.get('sheet_results') or []
        decorated['timestamp_headers'] = result_payload.get('timestamp_headers') or []
        decorated['group_row_count'] = result_payload.get('group_row_count')
        decorated['original_intervals'] = result_payload.get('original_intervals') or []
        decorated['expanded_intervals'] = result_payload.get('expanded_intervals') or []
        decorated['summary'] = decorated.get('summary') if isinstance(decorated.get('summary'), dict) else (result_payload.get('summary') or {})
        if decorated.get('template_count') in (None, '') and decorated['summary'].get('template_count') is not None:
            decorated['template_count'] = decorated['summary'].get('template_count')
        if decorated.get('original_interval_count') in (None, '') and decorated['summary'].get('original_interval_count') is not None:
            decorated['original_interval_count'] = decorated['summary'].get('original_interval_count')
        if decorated.get('expanded_interval_count') in (None, '') and decorated['summary'].get('expanded_interval_count') is not None:
            decorated['expanded_interval_count'] = decorated['summary'].get('expanded_interval_count')
        decorated['artifacts_available'] = {
            'request': self.artifact_path(decorated, 'request') is not None,
            'stdout': self.artifact_path(decorated, 'stdout') is not None,
            'stderr': self.artifact_path(decorated, 'stderr') is not None,
            'result': self.artifact_path(decorated, 'result') is not None,
            'report': self.artifact_path(decorated, 'report') is not None,
            'source': self.artifact_path(decorated, 'source') is not None,
        }
        decorated = self.enrich_platform_metadata(decorated)
        decorated['platform_events'] = self._decorate_platform_event_times(decorated.get('platform_events'))
        decorated['platform_display_events'] = self._decorate_platform_event_times(decorated.get('platform_display_events'))
        decorated['platform_timeline_events'] = self._decorate_platform_event_times(decorated.get('platform_timeline_events'))
        decorated['platform_artifacts'] = self._decorate_platform_artifact_times(decorated.get('platform_artifacts'))
        decorated['platform_artifacts_by_kind'] = self._format_timestamp_payload(decorated.get('platform_artifacts_by_kind') or {})
        decorated['platform_artifacts_by_endpoint_kind'] = self._format_timestamp_payload(decorated.get('platform_artifacts_by_endpoint_kind') or {})
        return self._decorate_history_list_artifacts(decorated)

    def _decorate_history_list_artifacts(self, job: Dict[str, object]) -> Dict[str, object]:
        decorated_job = dict(job)
        history_artifacts: List[Dict[str, object]] = []
        if self.artifact_path(decorated_job, 'report') is not None:
            history_artifacts.append(
                {
                    'artifact_kind': 'report',
                    'link_label': 'Report',
                    'download_href': self._artifact_download_href(decorated_job, 'report'),
                    'open_in_new_tab': False,
                }
            )
        if self._history_bundle_has_files(decorated_job):
            history_artifacts.append(
                {
                    'artifact_kind': 'bundle',
                    'link_label': 'ZIP',
                    'download_href': self._artifact_download_href(decorated_job, 'bundle'),
                    'open_in_new_tab': False,
                }
            )
        decorated_job['history_list_artifacts'] = history_artifacts
        return decorated_job

    def _artifact_download_href(self, job: Dict[str, object], artifact_kind: str) -> str:
        job_id = str(job.get('id') or '').strip()
        if has_request_context():
            return url_for('kpi_generator.artifact', job_id=job_id, artifact_kind=artifact_kind)
        return f'/kpi-generator/jobs/{quote(job_id)}/artifacts/{quote(artifact_kind)}'

    def _history_bundle_root(self, job: Dict[str, object]) -> Optional[Path]:
        raw_input_path = str(job.get('input_path') or '').strip()
        if not raw_input_path:
            return None
        return Path(raw_input_path).resolve().parent

    def _history_bundle_path(self, job: Dict[str, object]) -> Optional[Path]:
        bundle_root = self._history_bundle_root(job)
        if bundle_root is None:
            return None

        bundle_path = bundle_root / 'generator_history_bundle.zip'
        source_paths = [
            path
            for path in sorted(bundle_root.rglob('*'))
            if path.is_file() and path.resolve() != bundle_path.resolve()
        ]
        report_path = self.artifact_path(job, 'report') if str(job.get('report_file_path') or '').strip() else None
        source_path = self.artifact_path(job, 'source') if str(job.get('scout_report_path') or '').strip() else None
        extra_paths = [
            path
            for path in [report_path, source_path]
            if path is not None and path.exists() and not str(path.resolve()).startswith(str(bundle_root))
        ]
        if not source_paths and not extra_paths:
            return None

        with zipfile.ZipFile(bundle_path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for source_path_item in source_paths:
                archive.write(source_path_item, arcname=source_path_item.relative_to(bundle_root).as_posix())
            for extra_path in extra_paths:
                archive.write(extra_path, arcname=(Path('external') / extra_path.name).as_posix())
        return bundle_path

    def _history_bundle_has_files(self, job: Dict[str, object]) -> bool:
        bundle_root = self._history_bundle_root(job)
        if bundle_root is None:
            return False
        bundle_path = bundle_root / 'generator_history_bundle.zip'
        if any(path.is_file() and path.resolve() != bundle_path.resolve() for path in bundle_root.rglob('*')):
            return True
        return any(path is not None and path.exists() for path in [self.artifact_path(job, 'report'), self.artifact_path(job, 'source')])

    def _job_pid(self, job: Dict[str, object]) -> Optional[int]:
        raw_pid = job.get('process_pid')
        if raw_pid in (None, ''):
            return None
        try:
            return int(raw_pid)
        except (TypeError, ValueError):
            return None

    def _is_process_alive(self, pid: int) -> bool:
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        return True

    def _terminate_job_process(self, job: Dict[str, object]) -> None:
        pid = self._job_pid(job)
        if pid is None or not self._is_process_alive(pid):
            return

        if os.name == 'nt':
            self._terminate_pid_windows(pid)
            return

        try:
            os.killpg(pid, signal.SIGTERM)
        except OSError:
            return
        deadline = time.time() + 5
        while time.time() < deadline:
            if not self._is_process_alive(pid):
                return
            time.sleep(0.2)
        try:
            os.killpg(pid, signal.SIGKILL)
        except OSError:
            return

    def _terminate_pid_windows(self, pid: int) -> None:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            pass

        deadline = time.time() + 5
        while time.time() < deadline:
            if not self._is_process_alive(pid):
                return
            time.sleep(0.2)

        try:
            subprocess.run(
                ['taskkill', '/PID', str(pid), '/T', '/F'],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=10,
            )
        except (OSError, subprocess.TimeoutExpired):
            return


def get_kpi_generator_adapter() -> KpiGeneratorAdapter:
    return KpiGeneratorAdapter(get_repository('kpi-generator'))