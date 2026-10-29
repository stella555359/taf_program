from __future__ import annotations

import json
import math
import os
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
import zipfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import quote

from flask import has_request_context, url_for
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from .base import BaseModuleAdapter
from ..schemas import DetectorPortalInput, InputValidationError
from ..contracts import JobContract, ModuleCapabilityContract, SummaryContract
from ..config import get_config_value
from ..runners import get_unified_runner
from ..services.repo_registry import get_repository
from ..services.job_store import create_job, delete_job, list_jobs, load_job, module_jobs_root, next_queue_order, parse_utc_text, update_job, utcnow_text


class KpiDetectorAdapter(BaseModuleAdapter):
    module_key = 'kpi-anomaly-detector'
    cancel_message = 'Cancelled by user.'
    _release_pattern = re.compile(r'(?<!\d)(\d{2}R\d)(?!\d)', re.IGNORECASE)
    _environment_pattern = re.compile(r'^(T\d{3,4})(?:\b|[._])', re.IGNORECASE)
    _ue_token_pattern = re.compile(r'^\d+UEs?$', re.IGNORECASE)
    _csv_token_pattern = re.compile(r'^\d+csv[\w.-]*$', re.IGNORECASE)
    _html_suffixes = {'.html', '.htm'}
    _excel_suffixes = {'.xlsx', '.xlsm', '.xls'}

    @classmethod
    def _display_environment_code(cls, value: str) -> str:
        cleaned = str(value or '').strip().upper()
        if not cleaned:
            return ''
        match = re.search(r'\b(T\d{3,4})\b', cleaned)
        if match:
            return match.group(1)
        normalized = cleaned.replace('_', '.').strip('.')
        for segment in normalized.split('.'):
            if re.fullmatch(r'T\d{3,4}', segment, flags=re.IGNORECASE):
                return segment.upper()
        environment_match = cls._environment_pattern.match(cleaned)
        if environment_match:
            return environment_match.group(1).upper()
        return cleaned

    def sample_command(self) -> str:
        return 'python scripts/run_detector.py data/sample.xlsx'

    def artifact_endpoint_kind(self, artifact_kind: str) -> Optional[str]:
        mapping = {
            'bundle': 'bundle',
            'report_html': 'html',
            'report_excel': 'excel',
            'report_data': 'data',
            'report_html_detail': None,
            'report_excel_detail': None,
            'stdout': 'stdout',
            'stderr': 'stderr',
            'request': None,
            'result': None,
        }
        return mapping.get(artifact_kind, artifact_kind)

    def capability_contract(self) -> ModuleCapabilityContract:
        return ModuleCapabilityContract(
            supports_cancel=True,
            supports_delete=True,
            supports_rerun=True,
            supports_preview=True,
            supports_auto_trigger=False,
            supports_status_api=True,
        )

    def job_contract(self) -> JobContract:
        return JobContract(
            module_key=self.module_key,
            statuses=['queued', 'running', 'completed', 'failed'],
            artifact_kinds=['report_html', 'report_excel', 'report_data', 'report_html_detail', 'report_excel_detail', 'stdout', 'stderr'],
            progress_fields=['progress_stage', 'progress_message', 'progress_updated_at'],
            linked_job_fields=[],
        )

    def summary_contract(self) -> SummaryContract:
        return SummaryContract(
            result_payload_key='current_record',
            summary_fields=['current_record', 'stats', 'display_release', 'display_environment', 'display_scenario'],
            ui_fields=['status', 'display_release', 'display_environment', 'display_scenario', 'created_at'],
        )

    def timeout_seconds(self) -> int:
        return int(get_config_value('KPI_DETECTOR_TIMEOUT_SECONDS', 1800) or 1800)

    def describe_module(self) -> Dict[str, object]:
        module = super().describe_module()
        module['reports_path'] = str(self.repository.repo_path / 'reports')
        module['job_count'] = len(self.list_jobs(limit=100))
        module['timeout_seconds'] = self.timeout_seconds()
        module['filename_rule_text'] = self.filename_rule_text()
        module['filename_rule_example'] = self.filename_rule_example()
        module['filename_examples'] = self.filename_examples()
        return module

    def filter_options(self, selected_release: str = '', selected_environment: str = '') -> Dict[str, object]:
        jobs = self.list_jobs(limit=1000000)
        releases = sorted({
            str(job.get('display_release')).strip()
            for job in jobs
            if job.get('display_release')
        })
        environments = sorted({
            str(job.get('display_environment')).strip()
            for job in jobs
            if job.get('display_environment')
        })
        scenario_map: Dict[str, set[str]] = {'*::*': set()}
        all_scenarios = set()
        for job in jobs:
            release = str(job.get('display_release') or '').strip()
            environment = str(job.get('display_environment') or '').strip()
            scenario = str(job.get('display_scenario') or '').strip()
            if not scenario:
                continue
            all_scenarios.add(scenario)
            scenario_map['*::*'].add(scenario)
            if release:
                scenario_map.setdefault(f'{release}::*', set()).add(scenario)
            if environment:
                scenario_map.setdefault(f'*::{environment}', set()).add(scenario)
            if release and environment:
                scenario_map.setdefault(f'{release}::{environment}', set()).add(scenario)

        selected_release = selected_release.strip()
        selected_environment = selected_environment.strip()

        scenarios = sorted(self._scenario_values_for_filter(scenario_map, selected_release, selected_environment) or all_scenarios)

        normalized_scenario_map = {
            environment: sorted(list(values))
            for environment, values in scenario_map.items()
        }
        return {
            'releases': releases,
            'environments': environments,
            'scenarios': scenarios,
            'scenario_map': normalized_scenario_map,
        }

    def list_jobs(self, limit: int = 20) -> List[Dict[str, object]]:
        jobs = []
        for job in list_jobs(self.module_key, limit=limit):
            try:
                jobs.append(self._refresh_job_state(job))
            except OSError:
                jobs.append(job)
        return [self._decorate_job(job) for job in jobs]

    def query_jobs(
        self,
        search_query: str = '',
        status_query: str = '',
        release_query: str = '',
        environment_query: str = '',
        scenario_query: str = '',
        page: int = 1,
        page_size: int = 10,
    ) -> Dict[str, object]:
        jobs = self.list_jobs(limit=1000000)

        cleaned_query = search_query.strip().lower()
        cleaned_status = status_query.strip().lower()
        cleaned_release = release_query.strip().lower()
        cleaned_environment = environment_query.strip().lower()
        cleaned_scenario = scenario_query.strip().lower()

        if cleaned_query:
            jobs = [
                job for job in jobs
                if cleaned_query in str(job.get('original_filename', '')).lower()
                or cleaned_query in str(job.get('id', '')).lower()
            ]

        if cleaned_status:
            jobs = [job for job in jobs if str(job.get('status', '')).lower() == cleaned_status]

        if cleaned_release:
            jobs = [
                job for job in jobs
                if cleaned_release in str(job.get('display_release', '')).lower()
            ]

        if cleaned_environment:
            jobs = [
                job for job in jobs
                if cleaned_environment in str(job.get('display_environment', '')).lower()
            ]

        if cleaned_scenario:
            jobs = [
                job for job in jobs
                if cleaned_scenario in str(job.get('display_scenario', '')).lower()
            ]

        total_count = len(jobs)
        total_pages = max(math.ceil(total_count / page_size), 1)
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
        try:
            job = self._refresh_job_state(job)
        except OSError:
            pass
        return self._decorate_job(job)

    def filename_rule_text(self) -> str:
        return (
            'Filename must follow Date_Build_Env_Scenario_otherinfo.xlsx. '
            'Env is taken only from the token after Build that starts with Txxx or Txxxx, and Scenario ends before the first csv token.'
        )

    def filename_rule_example(self) -> str:
        return (
            'Example: exec20260325T120349_SBTS26R3.ENB.9999.260319.000005_T813.SCF.T813.gNB.25R3.20260224_7UE_DL_Burst_1csv.xlsx '
            '-> Date=exec20260325T120349, Build=SBTS26R3.ENB.9999.260319.000005, Env=T813, Scenario=7UE_DL_Burst, otherinfo=1csv.'
        )

    def filename_examples(self) -> List[str]:
        return [
            'exec20260325T120349_SBTS26R3.ENB.9999.260319.000005_T813.SCF.T813.gNB.25R3.20260224_7UE_DL_Burst_1csv.xlsx',
            '0129.1_26R2.0126.7_T076.SCF_7UEs_SFTPDL_1csv8run.xlsx',
            '0324.2_26R2.0182.0_T076.T07.26R2psot2c_CB012971_32UEs_httpDL.SmallShortF15_2csv10_20260324_215532.xlsx',
        ]

    def validate_filename(self, filename: str) -> Optional[str]:
        context = self._extract_filename_context(filename)
        if context['matched']:
            return None
        return f"file name incorrect. {self.filename_rule_text()}"

    def resolve_submission_filename(
        self,
        original_filename: str,
        *,
        override_environment: Optional[str] = None,
        override_scenario: Optional[str] = None,
    ) -> tuple[str, bool]:
        cleaned_filename = Path(str(original_filename or '')).name.strip() or 'upload.xlsx'
        if self.validate_filename(cleaned_filename) is None:
            return cleaned_filename, False

        cleaned_environment = self._sanitize_filename_token(override_environment, fallback='', uppercase=True)
        cleaned_scenario = self._sanitize_filename_token(override_scenario, fallback='')
        if not cleaned_environment or not cleaned_scenario:
            raise ValueError(f'file name incorrect. Please provide Env and Scenario. {self.filename_rule_text()}')

        resolved_filename = self._build_filename_with_override(cleaned_filename, cleaned_environment, cleaned_scenario)
        validation_error = self.validate_filename(resolved_filename)
        if validation_error:
            raise ValueError(validation_error)
        return resolved_filename, True

    def submit(
        self,
        upload: FileStorage,
        *,
        is_base_file: bool = False,
        override_environment: Optional[str] = None,
        override_scenario: Optional[str] = None,
        submission_batch_order: Optional[int] = None,
        submission_index: int = 0,
    ) -> Dict[str, object]:
        uploaded_filename = upload.filename or 'upload.xlsx'
        resolved_filename, override_applied = self.resolve_submission_filename(
            uploaded_filename,
            override_environment=override_environment,
            override_scenario=override_scenario,
        )
        try:
            schema_input = DetectorPortalInput.from_filename(
                original_filename=resolved_filename,
                is_base_file=is_base_file,
                source_generator_job_id=None,
                extract_filename_context=self._extract_filename_context,
                filename_rule_text=self.filename_rule_text(),
            )
        except InputValidationError as exc:
            raise ValueError(str(exc)) from exc

        original_filename = schema_input.original_filename

        safe_name = secure_filename(original_filename) or 'upload.xlsx'
        existing_job = self._latest_job_for_filename(original_filename)
        if existing_job is None:
            job = create_job(self.module_key, original_filename, safe_name, is_base_file=is_base_file)
        else:
            job = self._reset_job_for_reuse(
                str(existing_job['id']),
                original_filename=original_filename,
                stored_filename=safe_name,
                is_base_file=is_base_file,
                refresh_created_at=True,
            )

        input_path = Path(str(job['input_path']))
        input_path.parent.mkdir(parents=True, exist_ok=True)
        upload.save(input_path)
        update_job(
            self.module_key,
            str(job['id']),
            job_mode=schema_input.common.job_mode,
            build=schema_input.common.build,
            environment=schema_input.common.environment,
            scenario=schema_input.common.scenario,
            is_base_file=schema_input.runtime_options.as_base_file,
            uploaded_filename=uploaded_filename,
            filename_override_applied=override_applied,
            submission_batch_order=int(submission_batch_order or job.get('queue_order') or 0),
            submission_index=int(submission_index or 0),
        )

        self._schedule_dispatch()
        job['reused_existing'] = existing_job is not None
        job['uploaded_filename'] = uploaded_filename
        job['filename_override_applied'] = override_applied
        job['submission_batch_order'] = int(submission_batch_order or job.get('queue_order') or 0)
        job['submission_index'] = int(submission_index or 0)
        return job

    def submit_existing_file(
        self,
        *,
        report_file_path: Path,
        original_filename: Optional[str] = None,
        is_base_file: bool = False,
        source_generator_job_id: Optional[str] = None,
    ) -> Dict[str, object]:
        if not report_file_path.exists():
            raise FileNotFoundError(f'Detector input file not found: {report_file_path}')

        try:
            schema_input = DetectorPortalInput.from_filename(
                original_filename=original_filename or report_file_path.name,
                is_base_file=is_base_file,
                source_generator_job_id=source_generator_job_id,
                extract_filename_context=self._extract_filename_context,
                filename_rule_text=self.filename_rule_text(),
            )
        except InputValidationError as exc:
            raise ValueError(str(exc)) from exc

        resolved_original_filename = schema_input.original_filename

        safe_name = secure_filename(resolved_original_filename) or secure_filename(report_file_path.name) or 'upload.xlsx'
        existing_job = self._latest_job_for_filename(resolved_original_filename)
        if existing_job is not None and str(existing_job.get('status') or '') in {'queued', 'running'}:
            existing_job = None

        if existing_job is None:
            job = create_job(self.module_key, resolved_original_filename, safe_name, is_base_file=is_base_file)
        else:
            job = self._reset_job_for_reuse(
                str(existing_job['id']),
                original_filename=resolved_original_filename,
                stored_filename=safe_name,
                is_base_file=is_base_file,
                refresh_created_at=True,
            )

        input_path = Path(str(job['input_path']))
        input_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(report_file_path, input_path)

        updated_job = update_job(
            self.module_key,
            str(job['id']),
            job_mode=schema_input.common.job_mode,
            build=schema_input.common.build,
            environment=schema_input.common.environment,
            scenario=schema_input.common.scenario,
            is_base_file=schema_input.runtime_options.as_base_file,
            source_generator_job_id=schema_input.source_generator_job_id,
            auto_submitted_from_generator=bool(schema_input.source_generator_job_id),
        )
        self._schedule_dispatch()
        final_job = updated_job or job
        final_job['reused_existing'] = existing_job is not None
        return self.get_job(str(final_job['id'])) or final_job

    def rerun(self, source_job_id: str) -> Dict[str, object]:
        source_job = self.get_job(source_job_id)
        if source_job is None:
            raise FileNotFoundError(f'Job not found: {source_job_id}')

        if str(source_job.get('status') or '') in {'queued', 'running'}:
            raise ValueError('Queued or running jobs cannot be rerun.')

        source_input = Path(str(source_job['input_path']))
        if not source_input.exists():
            raise FileNotFoundError(f'Input file not found for job: {source_job_id}')

        original_filename = str(source_job.get('original_filename') or source_input.name)
        validation_error = self.validate_filename(original_filename)
        if validation_error:
            raise ValueError(validation_error)

        job = self._reset_job_for_reuse(source_job_id, refresh_created_at=True)

        self._schedule_dispatch()
        return self.get_job(source_job_id) or job

    def cancel(self, job_id: str) -> Dict[str, object]:
        job = load_job(self.module_key, job_id)
        if job is None:
            raise FileNotFoundError(f'Job not found: {job_id}')

        status = str(job.get('status') or '')
        if status not in {'queued', 'running'}:
            raise ValueError('Only queued or running jobs can be cancelled.')

        try:
            self._terminate_job_process(job)
            if status == 'queued':
                updated_job = update_job(
                    self.module_key,
                    job_id,
                    status='failed',
                    completed_at=utcnow_text(),
                    error_message=self.cancel_message,
                    cancel_requested_at=utcnow_text(),
                    process_pid=None,
                )
            else:
                updated_job = update_job(
                    self.module_key,
                    job_id,
                    cancel_requested_at=utcnow_text(),
                    error_message=self.cancel_message,
                )
        except OSError as exc:
            raise ValueError(f'Unable to cancel job because Portal cannot update its files: {exc}') from exc
        if status == 'queued':
            self._schedule_dispatch()
        return self._decorate_job(updated_job or job)

    def delete(self, job_id: str) -> Dict[str, object]:
        job = self.get_job(job_id)
        if job is None:
            raise FileNotFoundError(f'Job not found: {job_id}')

        if str(job.get('status')) in {'queued', 'running'}:
            raise ValueError('Running or queued jobs cannot be deleted.')

        other_jobs = [item for item in self.list_jobs(limit=1000000) if item.get('id') != job_id]
        tracked_filenames = self._tracked_filenames(job)
        shared_filenames = {
            filename for filename in tracked_filenames
            if any(filename in self._tracked_filenames(other_job) for other_job in other_jobs)
        }

        try:
            removed_history_records = self._delete_history_records(job, tracked_filenames - shared_filenames)
            removed_artifacts = self._delete_artifacts(job, other_jobs)
            removed_job_dir = delete_job(self.module_key, job_id)
        except OSError as exc:
            raise ValueError(f'Unable to delete job because Portal cannot update or remove its files: {exc}') from exc

        return {
            'removed_history_records': removed_history_records,
            'removed_artifacts': removed_artifacts,
            'removed_job_dir': removed_job_dir,
            'kept_shared_filenames': sorted(shared_filenames),
        }

    def _run_job(self, job_id: str) -> None:
        job = load_job(self.module_key, job_id)
        if job is None:
            self._schedule_dispatch()
            return

        if str(job.get('status') or '') not in {'queued', 'running'}:
            self._schedule_dispatch()
            return

        if str(job.get('cancel_requested_at') or '') and str(job.get('error_message') or '') == self.cancel_message:
            update_job(
                self.module_key,
                job_id,
                status='failed',
                completed_at=utcnow_text(),
                process_pid=None,
            )
            self._schedule_dispatch()
            return

        repo_path = self.repository.repo_path.resolve()
        detector_entry = repo_path / 'scripts' / 'run_detector.py'
        if not repo_path.exists() or not detector_entry.exists():
            update_job(
                self.module_key,
                job_id,
                status='failed',
                completed_at=utcnow_text(),
                error_message='Detector repository or entry script is missing.',
            )
            self._schedule_dispatch()
            return

        running_update = {
            'status': 'running',
            'completed_at': None,
        }
        if not job.get('started_at'):
            running_update['started_at'] = utcnow_text()
        update_job(self.module_key, job_id, **running_update)
        job = load_job(self.module_key, job_id)
        if job is None:
            self._schedule_dispatch()
            return

        result_json_path = Path(job['result_json_path'])
        python_executable = str(get_config_value('KPI_DETECTOR_PYTHON', '') or '').strip() or sys.executable
        bridge_code = """
import json
import sys
from pathlib import Path

repo_path = Path(sys.argv[1])
input_path = sys.argv[2]
result_json_path = Path(sys.argv[3])
job_id = sys.argv[4]
is_base_file = sys.argv[5].lower() in {'1', 'true', 'yes', 'on'}
sys.path.insert(0, str(repo_path / 'scripts'))

from kpi_detector import KPIAnomalyDetector

detector = KPIAnomalyDetector(input_path)
detector.source_job_id = job_id
detector.is_base_file = is_base_file
try:
    excel_report_path = detector.run(generate_html=True)
except ValueError as exc:
    print(str(exc), file=sys.stderr, flush=True)
    raise SystemExit(1)
input_stem = Path(input_path).stem
reports_dir = repo_path / 'reports'
html_report_path = reports_dir / f'{input_stem}_trend_viewer.html'
portal_record = detector.build_current_record()
portal_summary_path = result_json_path.parent / 'portal_summary.json'
portal_summary_path.write_text(json.dumps(portal_record, ensure_ascii=False, indent=2), encoding='utf-8')
payload = {
    'report_html_path': str(html_report_path) if html_report_path.exists() else None,
    'report_excel_path': str(excel_report_path) if excel_report_path else None,
    'report_data_path': str(portal_summary_path) if portal_summary_path.exists() else None,
    'current_record': portal_record,
    'detail_html_paths': [str(path) for path in detector.report_outputs.get('detail_html_paths', []) if path],
    'detail_excel_paths': [str(path) for path in detector.report_outputs.get('detail_excel_paths', []) if path],
}
result_json_path.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
"""

        popen_kwargs = {
            'cwd': repo_path,
            'text': True,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
        }
        if os.name == 'nt':
            popen_kwargs['creationflags'] = getattr(subprocess, 'CREATE_NEW_PROCESS_GROUP', 0)
        else:
            popen_kwargs['start_new_session'] = True

        process = subprocess.Popen(
            [python_executable, '-c', bridge_code, str(repo_path), str(job['input_path']), str(result_json_path), str(job_id), '1' if job.get('is_base_file') else '0'],
            **popen_kwargs,
        )
        update_job(self.module_key, job_id, process_pid=process.pid)

        stdout_path = Path(job['stdout_log_path'])
        stderr_path = Path(job['stderr_log_path'])
        stdout_path.parent.mkdir(parents=True, exist_ok=True)
        stdout_path.touch(exist_ok=True)
        stderr_path.touch(exist_ok=True)

        timeout_seconds = self.timeout_seconds()
        timed_out = False
        job_deleted = False
        with stdout_path.open('w', encoding='utf-8') as stdout_file, stderr_path.open('w', encoding='utf-8') as stderr_file:
            stdout_thread = threading.Thread(
                target=self._stream_process_output,
                args=(process.stdout, stdout_file),
                daemon=True,
            )
            stderr_thread = threading.Thread(
                target=self._stream_process_output,
                args=(process.stderr, stderr_file),
                daemon=True,
            )
            stdout_thread.start()
            stderr_thread.start()

            while process.poll() is None:
                current_job = load_job(self.module_key, job_id)
                if current_job is None:
                    job_deleted = True
                    self._terminate_process(process)
                    break

                if str(current_job.get('cancel_requested_at') or '') and str(current_job.get('error_message') or '') == self.cancel_message:
                    self._terminate_process(process)
                    break

                if self._has_job_timed_out(current_job, timeout_seconds):
                    timed_out = True
                    self._terminate_process(process)
                    update_job(
                        self.module_key,
                        job_id,
                        status='failed',
                        completed_at=utcnow_text(),
                        error_message=f'Detector exceeded timeout after {timeout_seconds} seconds.',
                        process_pid=None,
                    )
                    break

                time.sleep(1)

            process.wait()
            stdout_thread.join()
            stderr_thread.join()

        stderr = stderr_path.read_text(encoding='utf-8') if stderr_path.exists() else ''
        stdout = stdout_path.read_text(encoding='utf-8') if stdout_path.exists() else ''

        if job_deleted:
            self._schedule_dispatch()
            return

        current_job = load_job(self.module_key, job_id)
        if current_job is None:
            self._schedule_dispatch()
            return

        if str(current_job.get('cancel_requested_at') or '') and str(current_job.get('error_message') or '') == self.cancel_message:
            self._finalize_job_after_process_exit(job_id, current_job, stdout=stdout, stderr=stderr, process_returncode=process.returncode)
            return

        if timed_out:
            self._schedule_dispatch()
            return

        self._finalize_job_after_process_exit(job_id, current_job, stdout=stdout, stderr=stderr, process_returncode=process.returncode)

    def _refresh_job_state(self, job: Dict[str, object]) -> Dict[str, object]:
        status = str(job.get('status') or '')
        if status != 'running':
            return job

        timeout_seconds = self.timeout_seconds()
        if self._has_job_timed_out(job, timeout_seconds):
            self._terminate_job_process(job)
            refreshed = update_job(
                self.module_key,
                str(job['id']),
                status='failed',
                completed_at=utcnow_text(),
                error_message=f'Detector exceeded timeout after {timeout_seconds} seconds.',
                process_pid=None,
                recovery_owner_pid=None,
            )
            self._schedule_dispatch()
            return refreshed or job

        process_pid = self._job_pid(job)
        if process_pid and not self._is_process_alive(process_pid):
            refreshed = update_job(
                self.module_key,
                str(job['id']),
                status='failed',
                completed_at=utcnow_text(),
                error_message='Detector process exited before the Portal recorded a final status.',
                process_pid=None,
                recovery_owner_pid=None,
            )
            self._schedule_dispatch()
            return refreshed or job

        return job

    def read_job_log_tail(self, job: Dict[str, object], artifact_kind: str, max_bytes: int = 32768) -> str:
        artifact_path = self.artifact_path(job, artifact_kind)
        if artifact_path is None:
            return ''

        try:
            with artifact_path.open('rb') as stream:
                stream.seek(0, os.SEEK_END)
                file_size = stream.tell()
                if file_size <= 0:
                    return ''
                stream.seek(max(file_size - max_bytes, 0), os.SEEK_SET)
                chunk = stream.read()
        except OSError:
            return ''

        text = chunk.decode('utf-8', errors='replace')
        if file_size > max_bytes:
            newline_index = text.find('\n')
            if newline_index >= 0:
                text = text[newline_index + 1:]
        return text

    def _stream_process_output(self, stream, target_file) -> None:
        if stream is None:
            return

        try:
            for line in iter(stream.readline, ''):
                if not line:
                    break
                target_file.write(line)
                target_file.flush()
        finally:
            stream.close()

    def _normalize_result_payload(self, payload: Dict[str, object]) -> Dict[str, object]:
        report_html_path = self._normalize_primary_artifact_path(payload.get('report_html_path'), self._html_suffixes)
        report_excel_path = self._normalize_primary_artifact_path(payload.get('report_excel_path'), self._excel_suffixes)
        report_data_path = self._normalize_primary_artifact_path(payload.get('report_data_path'), {'.json'})
        detail_html_paths = self._normalize_artifact_path_list(payload.get('detail_html_paths'), self._html_suffixes)
        detail_excel_paths = self._normalize_artifact_path_list(payload.get('detail_excel_paths'), self._excel_suffixes)

        if not report_html_path and detail_html_paths:
            report_html_path = detail_html_paths[0]

        if (not report_excel_path or report_excel_path == report_html_path) and detail_excel_paths:
            report_excel_path = detail_excel_paths[0]

        return {
            'report_html_path': report_html_path,
            'report_excel_path': report_excel_path,
            'report_data_path': report_data_path,
            'current_record': payload.get('current_record') or {},
            'detail_html_paths': detail_html_paths,
            'detail_excel_paths': detail_excel_paths,
        }

    def _normalize_primary_artifact_path(self, raw_path: object, expected_suffixes: set[str]) -> Optional[str]:
        normalized = self._normalize_artifact_path(raw_path)
        if not normalized:
            return None
        if Path(normalized).suffix.lower() not in expected_suffixes:
            return None
        return normalized

    def _normalize_artifact_path_list(self, raw_paths: object, expected_suffixes: set[str]) -> List[str]:
        if not isinstance(raw_paths, list):
            return []

        normalized_paths: List[str] = []
        seen: set[str] = set()
        for raw_path in raw_paths:
            normalized = self._normalize_artifact_path(raw_path)
            if not normalized:
                continue
            if Path(normalized).suffix.lower() not in expected_suffixes:
                continue
            normalized_key = normalized.lower()
            if normalized_key in seen:
                continue
            normalized_paths.append(normalized)
            seen.add(normalized_key)
        return normalized_paths

    def _normalize_artifact_path(self, raw_path: object) -> Optional[str]:
        if raw_path in (None, ''):
            return None
        normalized = str(raw_path).strip()
        if not normalized:
            return None
        return normalized

    def _has_job_timed_out(self, job: Dict[str, object], timeout_seconds: int) -> bool:
        started_at = parse_utc_text(str(job.get('started_at') or ''))
        if started_at is None:
            return False
        elapsed_seconds = (datetime.now(timezone.utc) - started_at).total_seconds()
        return elapsed_seconds > timeout_seconds

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
        if pid is None:
            return

        self._terminate_pid(pid)

    def _terminate_pid(self, pid: int) -> None:
        if not self._is_process_alive(pid):
            return

        try:
            if os.name == 'nt':
                os.kill(pid, signal.SIGTERM)
            else:
                os.killpg(pid, signal.SIGTERM)
        except ProcessLookupError:
            return
        except OSError:
            return

        deadline = time.time() + 5
        while time.time() < deadline:
            if not self._is_process_alive(pid):
                return
            time.sleep(0.2)

        try:
            if os.name == 'nt':
                os.kill(pid, signal.SIGKILL)
            else:
                os.killpg(pid, signal.SIGKILL)
        except ProcessLookupError:
            return
        except OSError:
            return

    def _terminate_process(self, process: subprocess.Popen[str]) -> None:
        if process.poll() is not None:
            return

        try:
            if os.name == 'nt':
                process.terminate()
            else:
                os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            return
        except OSError:
            return

    def _clear_job_runtime_files(self, job: Dict[str, object]) -> None:
        job_root = Path(str(job['input_path'])).resolve().parent
        for key in ('stdout_log_path', 'stderr_log_path', 'result_json_path'):
            raw_path = job.get(key)
            if not raw_path:
                continue
            path = Path(str(raw_path)).resolve()
            if path.exists() and path.is_relative_to(job_root):
                path.unlink(missing_ok=True)

    def artifact_path(self, job: Dict[str, object], artifact_kind: str) -> Optional[Path]:
        if artifact_kind == 'bundle':
            return self._history_bundle_path(job)

        artifact_map = {
            'html': job.get('report_html_path'),
            'excel': job.get('report_excel_path'),
            'data': job.get('report_data_path'),
            'stdout': job.get('stdout_log_path'),
            'stderr': job.get('stderr_log_path'),
        }
        raw_path = artifact_map.get(artifact_kind)
        if not raw_path:
            return None

        path = Path(str(raw_path)).resolve()
        job_root = Path(str(job['input_path'])).resolve().parent
        allowed_roots = [self.repository.repo_path.resolve(), job_root]
        if not path.exists() or not any(path.is_relative_to(root) for root in allowed_roots):
            return None
        return path

    def _history_bundle_root(self, job: Dict[str, object]) -> Optional[Path]:
        raw_input_path = str(job.get('input_path') or '').strip()
        if not raw_input_path:
            return None
        return Path(raw_input_path).resolve().parent

    def _history_bundle_path(self, job: Dict[str, object]) -> Optional[Path]:
        bundle_root = self._history_bundle_root(job)
        if bundle_root is None:
            return None

        bundle_path = bundle_root / 'detector_history_bundle.zip'
        source_paths = [
            path
            for path in sorted(bundle_root.rglob('*'))
            if path.is_file() and path.resolve() != bundle_path.resolve()
        ]
        if not source_paths:
            return None

        with zipfile.ZipFile(bundle_path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for source_path in source_paths:
                archive.write(source_path, arcname=source_path.relative_to(bundle_root).as_posix())
        return bundle_path

    def _history_bundle_has_files(self, job: Dict[str, object]) -> bool:
        bundle_root = self._history_bundle_root(job)
        if bundle_root is None:
            return False
        bundle_path = bundle_root / 'detector_history_bundle.zip'
        return any(path.is_file() and path.resolve() != bundle_path.resolve() for path in bundle_root.rglob('*'))

    def detail_artifact_path(self, job: Dict[str, object], artifact_kind: str, item_index: int) -> Optional[Path]:
        if item_index < 0:
            return None

        detail_paths = job.get('detail_html_paths') if artifact_kind == 'html' else job.get('detail_excel_paths') if artifact_kind == 'excel' else None
        if not isinstance(detail_paths, list) or item_index >= len(detail_paths):
            return None

        raw_path = detail_paths[item_index]
        if not raw_path:
            return None

        path = Path(str(raw_path)).resolve()
        job_root = Path(str(job['input_path'])).resolve().parent
        allowed_roots = [self.repository.repo_path.resolve(), job_root]
        if not path.exists() or not any(path.is_relative_to(root) for root in allowed_roots):
            return None
        return path

    def report_asset_path(self, job: Dict[str, object], asset_path: str) -> Optional[Path]:
        report_html_path = job.get('report_html_path')
        if not report_html_path:
            return None

        html_root = Path(str(report_html_path)).resolve().parent
        path = (html_root / asset_path).resolve()
        if not path.exists() or not path.is_relative_to(html_root):
            return None
        return path

    def _tracked_filenames(self, job: Dict[str, object]) -> set[str]:
        names = set()
        for value in (
            job.get('original_filename'),
            job.get('stored_filename'),
            (job.get('current_record') or {}).get('filename') if isinstance(job.get('current_record'), dict) else None,
        ):
            if value:
                names.add(str(value))
                names.add(Path(str(value)).name)
        return {name for name in names if name}

    def _latest_job_for_filename(self, original_filename: str) -> Optional[Dict[str, object]]:
        normalized_name = Path(str(original_filename or '')).name.strip().lower()
        if not normalized_name:
            return None

        for job in self.list_jobs(limit=1000000):
            job_name = Path(str(job.get('original_filename') or '')).name.strip().lower()
            if job_name == normalized_name:
                return job
        return None

    def _reset_job_for_reuse(
        self,
        source_job_id: str,
        *,
        original_filename: Optional[str] = None,
        stored_filename: Optional[str] = None,
        is_base_file: Optional[bool] = None,
        refresh_created_at: bool = False,
    ) -> Dict[str, object]:
        source_job = self.get_job(source_job_id)
        if source_job is None:
            raise FileNotFoundError(f'Job not found: {source_job_id}')

        if str(source_job.get('status') or '') in {'queued', 'running'}:
            raise ValueError('Queued or running jobs cannot be replaced or rerun.')

        other_jobs = [item for item in self.list_jobs(limit=1000000) if item.get('id') != source_job_id]
        tracked_filenames = self._tracked_filenames(source_job)
        shared_filenames = {
            filename for filename in tracked_filenames
            if any(filename in self._tracked_filenames(other_job) for other_job in other_jobs)
        }

        self._delete_history_records(source_job, tracked_filenames - shared_filenames)
        self._delete_artifacts(source_job, other_jobs)

        existing_input_path = Path(str(source_job['input_path']))
        job_root = existing_input_path.resolve().parent
        next_original_filename = original_filename or str(source_job.get('original_filename') or existing_input_path.name)
        next_stored_filename = stored_filename or str(source_job.get('stored_filename') or existing_input_path.name)
        next_input_path = str(job_root / next_stored_filename)

        if str(existing_input_path) != next_input_path and existing_input_path.exists() and existing_input_path.is_relative_to(job_root):
            existing_input_path.unlink(missing_ok=True)

        update_fields = {
            'original_filename': next_original_filename,
            'stored_filename': next_stored_filename,
            'is_base_file': bool(source_job.get('is_base_file')) if is_base_file is None else bool(is_base_file),
            'queue_order': next_queue_order(),
            'input_path': next_input_path,
            'status': 'queued',
            'started_at': None,
            'completed_at': None,
            'error_message': None,
            'process_pid': None,
            'cancel_requested_at': None,
            'report_html_path': None,
            'report_excel_path': None,
            'report_data_path': None,
            'detail_html_paths': [],
            'detail_excel_paths': [],
            'stats': {},
            'current_record': None,
            'rerun_of': None,
        }
        if refresh_created_at:
            update_fields['created_at'] = utcnow_text()

        job = update_job(self.module_key, source_job_id, **update_fields)
        if job is None:
            raise FileNotFoundError(f'Job not found: {source_job_id}')

        self._clear_job_runtime_files(job)
        return job

    def _decorate_job(self, job: Dict[str, object]) -> Dict[str, object]:
        decorated_job = dict(job)
        current_record = decorated_job.get('current_record') if isinstance(decorated_job.get('current_record'), dict) else {}
        decorated_job['current_record'] = current_record
        date = current_record.get('date')
        release = current_record.get('release')
        build = current_record.get('build')
        environment = current_record.get('environment')
        scenario = current_record.get('scenario')
        otherinfo = current_record.get('otherinfo')

        if not date or not build or not environment or not scenario:
            fallback_context = self._extract_filename_context(decorated_job.get('original_filename', ''))
            date = date or fallback_context.get('date')
            release = release or fallback_context.get('release')
            build = build or fallback_context.get('build')
            environment = environment or fallback_context.get('environment')
            scenario = scenario or fallback_context.get('scenario')
            otherinfo = otherinfo or fallback_context.get('otherinfo')

        decorated_job['display_date'] = date
        decorated_job['display_release'] = release
        decorated_job['display_build'] = build
        decorated_job['display_environment'] = self._display_environment_code(str(environment or ''))
        decorated_job['display_scenario'] = scenario
        decorated_job['display_otherinfo'] = otherinfo
        decorated_job['is_base_file'] = bool(decorated_job.get('is_base_file'))
        decorated_job['history_key'] = current_record.get('history_key') or self._extract_filename_context(decorated_job.get('original_filename', '')).get('history_key')
        decorated_job['matched_history_count'] = current_record.get('matched_history_count', 0)
        decorated_job['portal_summary'] = current_record.get('portal_summary') if isinstance(current_record.get('portal_summary'), dict) else {}
        decorated_job['detail_html_paths'] = decorated_job.get('detail_html_paths') if isinstance(decorated_job.get('detail_html_paths'), list) else []
        decorated_job['detail_excel_paths'] = decorated_job.get('detail_excel_paths') if isinstance(decorated_job.get('detail_excel_paths'), list) else []
        decorated_job['sheet_artifacts'] = self._build_sheet_artifacts(decorated_job)
        platform_job = self.enrich_platform_metadata(decorated_job)
        return self._decorate_platform_download_artifacts(platform_job)

    def _build_sheet_artifacts(self, job: Dict[str, object]) -> List[Dict[str, object]]:
        portal_summary = job.get('portal_summary') if isinstance(job.get('portal_summary'), dict) else {}
        sheet_results = portal_summary.get('sheet_results') if isinstance(portal_summary.get('sheet_results'), list) else []
        detail_html_paths = job.get('detail_html_paths') if isinstance(job.get('detail_html_paths'), list) else []
        detail_excel_paths = job.get('detail_excel_paths') if isinstance(job.get('detail_excel_paths'), list) else []

        sheet_artifacts: List[Dict[str, object]] = []
        total_items = max(len(sheet_results), len(detail_html_paths), len(detail_excel_paths))
        for item_index in range(total_items):
            sheet_result = sheet_results[item_index] if item_index < len(sheet_results) and isinstance(sheet_results[item_index], dict) else {}
            html_path = detail_html_paths[item_index] if item_index < len(detail_html_paths) else None
            excel_path = detail_excel_paths[item_index] if item_index < len(detail_excel_paths) else None

            html_available = self.detail_artifact_path(job, 'html', item_index) is not None if html_path else False
            excel_available = self.detail_artifact_path(job, 'excel', item_index) is not None if excel_path else False

            sheet_artifacts.append(
                {
                    'item_index': item_index,
                    'sheet_name': sheet_result.get('sheet_name') or Path(str(excel_path or html_path or '')).stem or f'Sheet {item_index + 1}',
                    'history_key': sheet_result.get('history_key'),
                    'matched_history_count': sheet_result.get('matched_history_count', 0),
                    'stats': sheet_result.get('stats') if isinstance(sheet_result.get('stats'), dict) else {},
                    'html_path': html_path,
                    'excel_path': excel_path,
                    'html_available': html_available,
                    'excel_available': excel_available,
                }
            )
        return sheet_artifacts

    def _decorate_platform_download_artifacts(self, job: Dict[str, object]) -> Dict[str, object]:
        decorated_job = dict(job)
        platform_artifacts = [self._decorate_platform_artifact(decorated_job, artifact) for artifact in decorated_job.get('platform_artifacts', [])]

        platform_artifacts_by_kind = {
            str(artifact.get('artifact_kind') or ''): artifact
            for artifact in platform_artifacts
        }
        platform_artifacts_by_endpoint_kind = {
            str(artifact.get('download_endpoint_kind') or ''): artifact
            for artifact in platform_artifacts
            if artifact.get('download_endpoint_kind')
        }

        artifact_priority = {
            'report_html': 10,
            'report_html_detail': 11,
            'report_excel': 20,
            'report_excel_detail': 21,
            'report_data': 30,
            'stderr': 80,
            'stdout': 90,
        }
        platform_download_artifacts = [
            artifact
            for artifact in platform_artifacts
            if artifact.get('downloadable') and artifact.get('is_available') and artifact.get('download_href')
        ]
        platform_download_artifacts.sort(
            key=lambda artifact: (
                artifact_priority.get(str(artifact.get('artifact_kind') or ''), 999),
                int((artifact.get('payload') or {}).get('item_index') or -1),
                str(artifact.get('artifact_kind') or ''),
            )
        )

        decorated_job['platform_artifacts'] = platform_artifacts
        decorated_job['platform_artifacts_by_kind'] = platform_artifacts_by_kind
        decorated_job['platform_artifacts_by_endpoint_kind'] = platform_artifacts_by_endpoint_kind
        decorated_job['platform_download_artifacts'] = platform_download_artifacts
        decorated_job['history_list_artifacts'] = self._build_history_list_artifacts(decorated_job)
        return decorated_job

    def _build_history_list_artifacts(self, job: Dict[str, object]) -> List[Dict[str, object]]:
        history_artifacts: List[Dict[str, object]] = []
        platform_artifacts_by_kind = job.get('platform_artifacts_by_kind') if isinstance(job.get('platform_artifacts_by_kind'), dict) else {}
        report_html = platform_artifacts_by_kind.get('report_html') if isinstance(platform_artifacts_by_kind, dict) else None
        if isinstance(report_html, dict) and report_html.get('download_href'):
            history_artifacts.append(
                {
                    'artifact_kind': 'report_html',
                    'link_label': 'HTML',
                    'download_href': str(report_html.get('download_href') or ''),
                    'open_in_new_tab': True,
                }
            )

        if self._history_bundle_has_files(job):
            history_artifacts.append(
                {
                    'artifact_kind': 'bundle',
                    'link_label': 'ZIP',
                    'download_href': self._artifact_download_href(job, 'bundle'),
                    'open_in_new_tab': False,
                }
            )
        return history_artifacts

    def _decorate_platform_artifact(self, job: Dict[str, object], artifact: Dict[str, object]) -> Dict[str, object]:
        decorated_artifact = dict(artifact)
        artifact_kind = str(decorated_artifact.get('artifact_kind') or '')
        payload = dict(decorated_artifact.get('payload') or {})
        item_index = payload.get('item_index')

        if artifact_kind in {'report_html_detail', 'report_excel_detail'}:
            endpoint_kind = 'html' if artifact_kind == 'report_html_detail' else 'excel'
            is_available = False
            if isinstance(item_index, int):
                is_available = self.detail_artifact_path(job, endpoint_kind, item_index) is not None
            sheet_artifact = None
            if isinstance(item_index, int):
                sheet_artifacts = job.get('sheet_artifacts') if isinstance(job.get('sheet_artifacts'), list) else []
                if 0 <= item_index < len(sheet_artifacts) and isinstance(sheet_artifacts[item_index], dict):
                    sheet_artifact = sheet_artifacts[item_index]
            sheet_name = (sheet_artifact or {}).get('sheet_name') or f'Sheet {int(item_index) + 1}' if isinstance(item_index, int) else artifact_kind

            decorated_artifact['artifact_endpoint'] = 'kpi_detector.detail_artifact'
            decorated_artifact['download_endpoint_kind'] = endpoint_kind
            decorated_artifact['downloadable'] = True
            decorated_artifact['is_available'] = is_available
            decorated_artifact['link_label'] = f'{sheet_name} {endpoint_kind}'
            decorated_artifact['open_in_new_tab'] = endpoint_kind == 'html'
            decorated_artifact['requires_version_token'] = endpoint_kind == 'html'
            decorated_artifact['display_name'] = sheet_name
            decorated_artifact['download_href'] = self._detail_artifact_download_href(job, endpoint_kind, int(item_index)) if is_available and isinstance(item_index, int) else None
            return decorated_artifact

        endpoint_kind = decorated_artifact.get('download_endpoint_kind')
        if decorated_artifact.get('downloadable') and decorated_artifact.get('is_available') and endpoint_kind:
            decorated_artifact['download_href'] = self._artifact_download_href(job, str(endpoint_kind), bool(decorated_artifact.get('requires_version_token')))
        else:
            decorated_artifact['download_href'] = None
        return decorated_artifact

    def _artifact_download_href(self, job: Dict[str, object], artifact_kind: str, requires_version_token: bool = False) -> str:
        job_id = str(job.get('id') or '').strip()
        if has_request_context():
            href = url_for('kpi_detector.artifact', job_id=job_id, artifact_kind=artifact_kind)
        else:
            href = f'/kpi-anomaly-detector/jobs/{quote(job_id)}/artifacts/{quote(artifact_kind)}'
        if requires_version_token:
            version_value = str(job.get('completed_at') or job.get('started_at') or job.get('created_at') or job_id)
            href += f'?v={quote(version_value)}'
        return href

    def _detail_artifact_download_href(self, job: Dict[str, object], artifact_kind: str, item_index: int) -> str:
        job_id = str(job.get('id') or '').strip()
        if has_request_context():
            href = url_for('kpi_detector.detail_artifact', job_id=job_id, artifact_kind=artifact_kind, item_index=item_index)
        else:
            href = f'/kpi-anomaly-detector/jobs/{quote(job_id)}/detail-artifacts/{quote(artifact_kind)}/{item_index}'
        if artifact_kind == 'html':
            version_value = str(job.get('completed_at') or job.get('started_at') or job.get('created_at') or job_id)
            href += f'?v={quote(version_value)}'
        return href

    def _extract_filename_context(self, filename: str) -> Dict[str, object]:
        raw_name = Path(str(filename or '')).name
        stem = Path(raw_name).stem
        tokens = [token for token in stem.split('_') if token]

        if len(tokens) < 5:
            return {
                'date': None,
                'release': None,
                'build': None,
                'environment': None,
                'scenario': None,
                'otherinfo': None,
                'history_key': None,
                'matched': False,
            }

        date_token = tokens[0]

        environment = None
        env_index = -1
        for index in range(1, len(tokens)):
            environment_match = self._environment_pattern.match(tokens[index])
            if environment_match:
                environment = environment_match.group(1).upper()
                env_index = index
                break

        if env_index <= 1:
            return {
                'date': date_token,
                'release': None,
                'build': None,
                'environment': environment,
                'scenario': None,
                'otherinfo': None,
                'history_key': None,
                'matched': False,
            }

        build = None
        build_tokens = tokens[1:env_index]
        if build_tokens:
            build = '_'.join(build_tokens)

        csv_index = -1
        for index in range(env_index + 1, len(tokens)):
            if self._csv_token_pattern.match(tokens[index]):
                csv_index = index
                break

        if csv_index < 0:
            return {
                'date': date_token,
                'release': None,
                'build': build,
                'environment': environment,
                'scenario': None,
                'otherinfo': None,
                'history_key': None,
                'matched': False,
            }

        scenario_stop = csv_index

        scenario_start = None
        for index in range(env_index + 1, scenario_stop):
            if self._ue_token_pattern.match(tokens[index]):
                scenario_start = index
                break

        if scenario_start is None and env_index + 1 < scenario_stop:
            scenario_start = env_index + 1

        scenario = None
        if scenario_start is not None and scenario_start < scenario_stop:
            scenario_tokens = tokens[scenario_start:scenario_stop]
            if scenario_tokens:
                scenario = '_'.join(scenario_tokens)

        otherinfo = None
        if csv_index >= 0:
            otherinfo_tokens = tokens[csv_index:]
            if otherinfo_tokens:
                otherinfo = '_'.join(otherinfo_tokens)

        release_match = self._release_pattern.search(build or '')
        release = release_match.group(1).upper() if release_match else None
        history_key = f'{environment}::{scenario}' if environment and scenario else None
        return {
            'date': date_token,
            'release': release,
            'build': build,
            'environment': environment,
            'scenario': scenario,
            'otherinfo': otherinfo,
            'history_key': history_key,
            'matched': bool(date_token and build and environment and scenario and otherinfo),
        }

    def _build_filename_with_override(self, original_filename: str, environment: str, scenario: str) -> str:
        raw_name = Path(str(original_filename or '')).name.strip() or 'upload.xlsx'
        stem = Path(raw_name).stem
        suffix = Path(raw_name).suffix or '.xlsx'
        tokens = [token for token in stem.split('_') if token]

        date_token = self._sanitize_filename_token(tokens[0] if tokens else '', fallback=self._default_date_token())

        csv_index = -1
        for index in range(1, len(tokens)):
            if self._csv_token_pattern.match(tokens[index]):
                csv_index = index
                break

        stop_index = len(tokens)
        for index in range(1, len(tokens)):
            if self._environment_pattern.match(tokens[index]) or self._ue_token_pattern.match(tokens[index]) or self._csv_token_pattern.match(tokens[index]):
                stop_index = index
                break

        build_tokens = tokens[1:stop_index] if stop_index > 1 else []
        if not build_tokens and csv_index > 1:
            build_tokens = tokens[1:csv_index]
        build_value = self._sanitize_filename_token('_'.join(build_tokens), fallback='UNKNOWN_BUILD')

        otherinfo_tokens = tokens[csv_index:] if csv_index >= 0 else ['1csv']
        otherinfo_value = self._sanitize_filename_token('_'.join(otherinfo_tokens), fallback='1csv')

        return f'{date_token}_{build_value}_{environment}_{scenario}_{otherinfo_value}{suffix}'

    def _default_date_token(self) -> str:
        return datetime.now(timezone.utc).strftime('exec%Y%m%dT%H%M%S')

    def _sanitize_filename_token(self, value: Optional[str], *, fallback: str, uppercase: bool = False) -> str:
        cleaned = str(value or '').strip()
        cleaned = re.sub(r'\s+', '_', cleaned)
        cleaned = re.sub(r'[\\/]+', '_', cleaned)
        cleaned = re.sub(r'[^A-Za-z0-9._-]+', '_', cleaned)
        cleaned = re.sub(r'_+', '_', cleaned).strip('._-')
        if uppercase:
            cleaned = cleaned.upper()
        return cleaned or fallback

    def _scenario_values_for_filter(
        self,
        scenario_map: Dict[str, set[str]],
        selected_release: str,
        selected_environment: str,
    ) -> set[str]:
        candidates = [
            f'{selected_release}::{selected_environment}' if selected_release or selected_environment else '*::*',
            f'{selected_release}::*' if selected_release else '',
            f'*::{selected_environment}' if selected_environment else '',
            '*::*',
        ]
        for key in candidates:
            if key and key in scenario_map:
                return scenario_map[key]
        return set()

    def _schedule_dispatch(self) -> None:
        get_unified_runner().submit_module_dispatcher(self.module_key, self._dispatch_queued_jobs)

    def _dispatch_queued_jobs(self) -> None:
        self._start_next_queued_job()

    def _job_order_key(self, item: Dict[str, object]) -> tuple[int, str, str]:
        return (
            int(item.get('queue_order') or 0),
            str(item.get('created_at') or ''),
            str(item.get('id') or ''),
        )

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
        selected_job_id = None
        with self._dispatch_lock():
            raw_jobs = list_jobs(self.module_key, limit=1000000)
            for raw_job in raw_jobs:
                if str(raw_job.get('status') or '') == 'running':
                    raw_job = self._refresh_job_state(raw_job)
                if str(raw_job.get('status') or '') == 'running':
                    return

            queued_jobs = [job for job in list_jobs(self.module_key, limit=1000000) if str(job.get('status') or '') == 'queued']
            if not queued_jobs:
                return

            queued_jobs.sort(key=self._job_order_key)
            next_job = queued_jobs[0]
            selected_job_id = str(next_job['id'])

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
            if updated_job is None:
                selected_job_id = None

        if not selected_job_id:
            return

        try:
            get_unified_runner().submit_threaded_job(self.module_key, selected_job_id, lambda: self._run_job(selected_job_id))
        except RuntimeError as exc:
            update_job(
                self.module_key,
                selected_job_id,
                status='failed',
                completed_at=utcnow_text(),
                error_message=f'Unable to start detector worker: {exc}',
                process_pid=None,
            )
            self._schedule_dispatch()

    def recover_startup_jobs(self) -> None:
        should_start_next = False
        adopted_running_job = False
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
                    adopted_running_job = True
                    continue

                process_pid = self._job_pid(refreshed_job)
                if process_pid is None:
                    update_job(
                        self.module_key,
                        str(refreshed_job['id']),
                        status='failed',
                        completed_at=utcnow_text(),
                        error_message='Detector job could not be recovered after Portal restart because no process pid was recorded.',
                        process_pid=None,
                        recovery_owner_pid=None,
                    )
                    continue

                if not self._is_process_alive(process_pid):
                    self._refresh_job_state(refreshed_job)
                    continue

                if adopted_running_job:
                    update_job(
                        self.module_key,
                        str(refreshed_job['id']),
                        status='failed',
                        completed_at=utcnow_text(),
                        error_message='Detector job was left in running state, but another earlier running job was already recovered after Portal restart.',
                        process_pid=None,
                        recovery_owner_pid=None,
                    )
                    continue

                update_job(self.module_key, str(refreshed_job['id']), recovery_owner_pid=os.getpid())

                submitted = get_unified_runner().submit_threaded_job(
                    self.module_key,
                    str(refreshed_job['id']),
                    lambda job_id=str(refreshed_job['id']): self._monitor_running_job(job_id),
                )
                if submitted:
                    adopted_running_job = True
                else:
                    update_job(self.module_key, str(refreshed_job['id']), recovery_owner_pid=None)

            if not adopted_running_job:
                should_start_next = any(str(job.get('status') or '') == 'queued' for job in list_jobs(self.module_key, limit=1000000))

        if should_start_next:
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

        timeout_seconds = self.timeout_seconds()
        while self._is_process_alive(process_pid):
            current_job = load_job(self.module_key, job_id)
            if current_job is None:
                return
            if str(current_job.get('status') or '') != 'running':
                self._schedule_dispatch()
                return
            if self._has_job_timed_out(current_job, timeout_seconds):
                self._terminate_job_process(current_job)
                update_job(
                    self.module_key,
                    job_id,
                    status='failed',
                    completed_at=utcnow_text(),
                    error_message=f'Detector exceeded timeout after {timeout_seconds} seconds.',
                    process_pid=None,
                    recovery_owner_pid=None,
                )
                self._schedule_dispatch()
                return
            if str(current_job.get('cancel_requested_at') or '') and str(current_job.get('error_message') or '') == self.cancel_message:
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
        self._finalize_job_after_process_exit(job_id, current_job, stdout=stdout, stderr=stderr, process_returncode=None)

    def _finalize_job_after_process_exit(
        self,
        job_id: str,
        current_job: Dict[str, object],
        *,
        stdout: str,
        stderr: str,
        process_returncode: Optional[int],
    ) -> None:
        result_json_path = Path(str(current_job['result_json_path']))
        if str(current_job.get('cancel_requested_at') or '') and str(current_job.get('error_message') or '') == self.cancel_message:
            update_job(
                self.module_key,
                job_id,
                status='failed',
                completed_at=utcnow_text(),
                process_pid=None,
                recovery_owner_pid=None,
            )
            self._schedule_dispatch()
            return

        if process_returncode not in (None, 0):
            update_job(
                self.module_key,
                job_id,
                status='failed',
                completed_at=utcnow_text(),
                error_message=(stderr or stdout or 'Detector execution failed.').strip(),
                process_pid=None,
                recovery_owner_pid=None,
            )
            self._schedule_dispatch()
            return

        if not result_json_path.exists():
            update_job(
                self.module_key,
                job_id,
                status='failed',
                completed_at=utcnow_text(),
                error_message='Detector finished without producing result metadata.',
                process_pid=None,
                recovery_owner_pid=None,
            )
            self._schedule_dispatch()
            return

        try:
            payload = json.loads(result_json_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            update_job(
                self.module_key,
                job_id,
                status='failed',
                completed_at=utcnow_text(),
                error_message='Detector produced an unreadable result metadata file.',
                process_pid=None,
                recovery_owner_pid=None,
            )
            self._schedule_dispatch()
            return

        normalized_payload = self._normalize_result_payload(payload)
        report_html_path = normalized_payload['report_html_path']
        report_excel_path = normalized_payload['report_excel_path']
        report_data_path = normalized_payload['report_data_path']
        current_record = normalized_payload['current_record']
        detail_html_paths = normalized_payload['detail_html_paths']
        detail_excel_paths = normalized_payload['detail_excel_paths']

        update_job(
            self.module_key,
            job_id,
            status='completed',
            completed_at=utcnow_text(),
            error_message=None,
            process_pid=None,
            recovery_owner_pid=None,
            report_html_path=report_html_path,
            report_excel_path=report_excel_path,
            report_data_path=report_data_path,
            detail_html_paths=detail_html_paths,
            detail_excel_paths=detail_excel_paths,
            stats=current_record.get('stats', {}),
            current_record=current_record,
        )
        self._schedule_dispatch()

    def _history_file_paths(self) -> list[Path]:
        reports_dir = self.repository.repo_path / 'reports'
        return [
            reports_dir / 'kpi_history_records.json',
            reports_dir / 'kpi_history_records_scout.json',
        ]

    def _delete_history_records(self, job: Dict[str, object], filenames: set[str]) -> int:
        source_job_id = str(job.get('id') or '').strip()
        if not source_job_id and not filenames:
            return 0

        removed_total = 0
        for history_path in self._history_file_paths():
            if not history_path.exists():
                continue

            records = json.loads(history_path.read_text(encoding='utf-8'))
            kept_records = []
            removed_count = 0
            for record in records:
                if source_job_id and str(record.get('source_job_id') or '').strip() == source_job_id:
                    removed_count += 1
                    continue
                record_filename = Path(str(record.get('filename', ''))).name
                if record_filename in filenames:
                    removed_count += 1
                    continue
                kept_records.append(record)

            if removed_count:
                history_path.write_text(json.dumps(kept_records, ensure_ascii=False, indent=2), encoding='utf-8')
                removed_total += removed_count
        return removed_total

    def _delete_artifacts(self, job: Dict[str, object], other_jobs: List[Dict[str, object]]) -> List[str]:
        removable_paths = []
        other_artifact_paths = {
            path
            for other_job in other_jobs
            for path in self._job_artifact_paths(other_job)
        }
        for raw_path_str in self._job_artifact_paths(job):
            if raw_path_str in other_artifact_paths:
                continue

            path = Path(raw_path_str)
            if path.exists() and path.is_relative_to(self.repository.repo_path.resolve()):
                removable_paths.append(path)

        html_path_raw = job.get('report_html_path')
        if html_path_raw:
            html_path = Path(str(html_path_raw))
            assets_dir = html_path.with_name(f'{html_path.stem}_assets')
            if assets_dir.exists() and assets_dir.is_relative_to(self.repository.repo_path.resolve()):
                other_asset_dirs = {
                    str(Path(str(other_job.get('report_html_path'))).with_name(f"{Path(str(other_job.get('report_html_path'))).stem}_assets"))
                    for other_job in other_jobs
                    if other_job.get('report_html_path')
                }
                if str(assets_dir) not in other_asset_dirs:
                    removable_paths.append(assets_dir)

        removed = []
        for path in removable_paths:
            if path.exists():
                if path.is_dir():
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    path.unlink(missing_ok=True)
                removed.append(str(path))
        return removed

    def _job_artifact_paths(self, job: Dict[str, object]) -> List[str]:
        tracked_paths: List[str] = []
        for key in ('report_html_path', 'report_excel_path', 'report_data_path'):
            normalized = self._normalize_artifact_path(job.get(key))
            if normalized:
                tracked_paths.append(normalized)

        for key in ('detail_html_paths', 'detail_excel_paths'):
            tracked_paths.extend(self._normalize_artifact_path_list(job.get(key), self._html_suffixes if key == 'detail_html_paths' else self._excel_suffixes))

        unique_paths: List[str] = []
        seen: set[str] = set()
        for path in tracked_paths:
            normalized_key = path.lower()
            if normalized_key in seen:
                continue
            unique_paths.append(path)
            seen.add(normalized_key)
        return unique_paths


def get_kpi_detector_adapter() -> KpiDetectorAdapter:
    return KpiDetectorAdapter(get_repository('kpi-anomaly-detector'))