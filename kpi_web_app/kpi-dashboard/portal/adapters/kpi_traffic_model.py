# pyright: reportMissingImports=false, reportMissingModuleSource=false

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from .base import BaseModuleAdapter, ModuleRepository
from ..contracts import JobContract, ModuleCapabilityContract, SummaryContract
from ..config import get_config_value
from ..runners import get_unified_runner
from ..services.job_store import create_job, delete_job, list_jobs, load_job, update_job, utcnow_text
from ..services.repo_registry import WORKSPACE_ROOT


class KpiTrafficModelAdapter(BaseModuleAdapter):
    module_key = 'kpi-traffic-model'
    cancel_message = 'Cancelled by user.'

    def sample_command(self) -> str:
        return 'python -m orchestrator.runner request.json result.json'

    def capability_contract(self) -> ModuleCapabilityContract:
        return ModuleCapabilityContract(
            supports_cancel=False,
            supports_delete=True,
            supports_rerun=False,
            supports_preview=True,
            supports_auto_trigger=True,
            supports_status_api=True,
        )

    def job_contract(self) -> JobContract:
        return JobContract(
            module_key=self.module_key,
            statuses=['queued', 'running', 'completed', 'failed'],
            artifact_kinds=['request', 'result', 'stdout', 'stderr'],
            progress_fields=['progress_stage', 'progress_message', 'progress_updated_at'],
            linked_job_fields=[],
        )

    def summary_contract(self) -> SummaryContract:
        return SummaryContract(
            result_payload_key='result_payload',
            summary_fields=['summary', 'result_payload', 'kpi_test_starttime', 'kpi_test_endtime'],
            ui_fields=['status', 'env', 'config_id', 'progress_stage', 'progress_message'],
        )

    def env_map_path(self) -> Path:
        return self.repository.repo_path / 'configs' / 'env_map.json'

    def configured_robotws_path(self) -> Path:
        configured = str(get_config_value('KPI_TRAFFIC_MODEL_ROBOTWS_PATH', '') or '').strip()
        return Path(configured) if configured else (self.repository.repo_path / 'robotws')

    def configured_testline_path(self) -> Path:
        configured = str(get_config_value('KPI_TRAFFIC_MODEL_TESTLINE_PATH', '') or '').strip()
        return Path(configured) if configured else (self.repository.repo_path / 'testline_configuration')

    def configured_runner_path(self) -> Optional[Path]:
        configured = str(get_config_value('KPI_TRAFFIC_MODEL_RUNNER_PATH', '') or '').strip()
        return Path(configured) if configured else None

    def configured_activate_command(self) -> str:
        return str(get_config_value('KPI_TRAFFIC_MODEL_ACTIVATE_COMMAND', '') or '').strip()

    def describe_module(self) -> Dict[str, object]:
        module = super().describe_module()
        module['job_count'] = len(self.list_jobs(limit=100))
        module['env_map_path'] = str(self.env_map_path())
        module['supported_models'] = [
            'apply_preconditions',
            'attach',
            'detach',
            'dl_burst_appserver',
        ]
        module['env_map_exists'] = self.env_map_path().exists()
        module['robotws_path'] = str(self.configured_robotws_path())
        module['testline_path'] = str(self.configured_testline_path())
        module['runner_path'] = str(self.configured_runner_path()) if self.configured_runner_path() else ''
        module['activate_command'] = self.configured_activate_command()
        return module

    def list_jobs(self, limit: int = 20) -> List[Dict[str, object]]:
        return [self._decorate_job(job) for job in list_jobs(self.module_key, limit=limit)]

    def get_job(self, job_id: str) -> Optional[Dict[str, object]]:
        job = load_job(self.module_key, job_id)
        if job is None:
            return None
        return self._decorate_job(job)

    def submit_request(self, payload: dict) -> Dict[str, object]:
        request_loader = self._build_request_loader()
        request = request_loader.load_dict(payload)

        job = create_job(self.module_key, f'{request.env} / kpi_traffic_model', 'request.json')
        request_path = Path(job['input_path'])
        request_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')

        update_job(
            self.module_key,
            job['id'],
            job_mode=str(payload.get('job_mode') or 'traffic_model'),
            env=request.env,
            environment=request.env,
            dry_run=request.runtime_options.dry_run,
            stop_on_failure=request.runtime_options.stop_on_failure,
            max_parallel_workers=request.runtime_options.max_parallel_workers,
            log_level=request.runtime_options.log_level,
            config_id=request.testline_resolution.config_id if request.testline_resolution else None,
            progress_stage='queued',
            progress_message='Job queued.',
            progress_updated_at=utcnow_text(),
        )

        get_unified_runner().submit_threaded_job(self.module_key, str(job['id']), lambda: self._run_job(str(job['id'])))
        return self.get_job(job['id']) or job

    def delete(self, job_id: str) -> Dict[str, object]:
        job = self.get_job(job_id)
        if job is None:
            raise FileNotFoundError(f'Job not found: {job_id}')
        delete_job(self.module_key, job_id)
        return {'id': job_id}

    def artifact_path(self, job: Dict[str, object], artifact_kind: str) -> Optional[Path]:
        mapping = {
            'request': 'input_path',
            'stdout': 'stdout_log_path',
            'stderr': 'stderr_log_path',
            'result': 'result_json_path',
        }
        key = mapping.get(artifact_kind)
        if not key:
            return None
        raw_path = job.get(key)
        if not raw_path:
            return None
        path = Path(str(raw_path))
        return path if path.exists() else None

    def resolve_env(self, env: str) -> dict:
        request_loader = self._build_request_loader()
        resolved = request_loader.config_resolver.resolve_env(env)
        return {
            'env': resolved.env,
            'config_id': resolved.config_id,
            'config_path': str(resolved.config_path),
            'department': resolved.department,
            'site': resolved.site,
            'topology_id': resolved.topology_id,
            'allowed_script_roots': list(resolved.allowed_script_roots),
        }

    def inspect_env(self, env: str) -> dict[str, Any]:
        request_loader = self._build_request_loader()
        context = request_loader.config_resolver.load_testline_context(env)
        return {
            'env': context.env,
            'resolved_config': {
                'config_id': context.resolved_config.config_id,
                'config_path': str(context.resolved_config.config_path),
                'department': context.resolved_config.department,
                'site': context.resolved_config.site,
                'topology_id': context.resolved_config.topology_id,
                'match_type': context.resolved_config.match_type,
                'confidence': context.resolved_config.confidence,
                'allowed_script_roots': list(context.resolved_config.allowed_script_roots),
            },
            'ues': [
                {
                    'ue_index': ue.ue_index,
                    'ue_type': ue.ue_type,
                    'ue_ip': ue.ue_ip,
                    'label': ue.label,
                    'serial_number': ue.serial_number,
                    'capabilities': list(ue.capabilities),
                }
                for ue in context.ues
            ],
            'summary': dict(context.raw_summary),
        }

    def _run_job(self, job_id: str) -> None:
        job = load_job(self.module_key, job_id)
        if job is None:
            return

        request_path = Path(str(job['input_path']))
        stdout_path = Path(str(job['stdout_log_path']))
        stderr_path = Path(str(job['stderr_log_path']))
        result_path = Path(str(job['result_json_path']))
        stdout_path.parent.mkdir(parents=True, exist_ok=True)
        stdout_path.touch(exist_ok=True)
        stderr_path.touch(exist_ok=True)

        update_job(
            self.module_key,
            job_id,
            status='running',
            started_at=utcnow_text(),
            completed_at=None,
            error_message=None,
            progress_stage='resolving_env',
            progress_message='Resolving env and loading testline configuration.',
            progress_updated_at=utcnow_text(),
        )

        request_loader = self._build_request_loader()
        result_builder = self._build_result_builder()
        runner = self._build_runner()
        state = self._build_orchestrator_state()
        context = None
        timestamps = {
            'created_at': str(job.get('created_at') or ''),
            'started_at': utcnow_text(),
            'completed_at': None,
        }
        artifacts = {
            'request_json_path': str(request_path),
            'stdout_log_path': str(stdout_path),
            'stderr_log_path': str(stderr_path),
            'result_json_path': str(result_path),
            'extra_artifacts': [],
        }

        def write_stdout(message: str) -> None:
            with stdout_path.open('a', encoding='utf-8') as stdout_handle:
                stdout_handle.write(message)

        def write_stderr(message: str) -> None:
            with stderr_path.open('a', encoding='utf-8') as stderr_handle:
                stderr_handle.write(message)

        def update_progress(stage: str, message: str) -> None:
            update_job(
                self.module_key,
                job_id,
                progress_stage=stage,
                progress_message=message,
                progress_updated_at=utcnow_text(),
            )

        try:
            request = request_loader.load_json_file(request_path)
            context = request_loader.config_resolver.load_testline_context(request.env)
            self._validate_selected_ues_against_context(request.payload, context)
            update_progress('executing', 'Executing orchestrator runner.')
            runner.execute(
                request,
                context,
                state,
                progress_callback=update_progress,
                write_stdout=write_stdout,
                write_stderr=write_stderr,
            )
            completed_at = utcnow_text()
            if state.status == 'failed':
                result = result_builder.build_failure(
                    request,
                    state,
                    error_message=state.error_message or 'Traffic execution failed.',
                    timestamps={**timestamps, 'completed_at': completed_at},
                    artifacts=artifacts,
                    context=context,
                )
            else:
                result = result_builder.build_success(
                    request,
                    context,
                    state,
                    timestamps={**timestamps, 'completed_at': completed_at},
                    artifacts=artifacts,
                )
            result_builder.write(result, result_path)
            update_job(
                self.module_key,
                job_id,
                status=state.status,
                completed_at=completed_at,
                error_message=state.error_message,
                env=request.env,
                config_id=context.resolved_config.config_id,
                summary=result.get('summary') or {},
                result_payload=result,
                kpi_test_starttime=state.kpi_test_starttime,
                kpi_test_endtime=state.kpi_test_endtime,
                progress_stage=state.status,
                progress_message='Orchestrator runner completed.' if state.status == 'completed' else (state.error_message or 'Traffic execution failed.'),
                progress_updated_at=utcnow_text(),
            )
        except Exception as exc:
            message = str(exc)
            write_stderr(f'{message}\n')
            try:
                request = request_loader.load_json_file(request_path)
            except Exception:
                request = self._build_fallback_request(request_path)
            completed_at = utcnow_text()
            result = result_builder.build_failure(
                request,
                state,
                error_message=message,
                timestamps={**timestamps, 'completed_at': completed_at},
                artifacts=artifacts,
                context=context,
            )
            result_builder.write(result, result_path)
            update_job(
                self.module_key,
                job_id,
                status='failed',
                completed_at=completed_at,
                error_message=message,
                result_payload=result,
                progress_stage='failed',
                progress_message=message,
                progress_updated_at=utcnow_text(),
            )

    def _decorate_job(self, job: Dict[str, object]) -> Dict[str, object]:
        decorated = dict(job)
        decorated['artifacts_available'] = {
            'request': self.artifact_path(decorated, 'request') is not None,
            'stdout': self.artifact_path(decorated, 'stdout') is not None,
            'stderr': self.artifact_path(decorated, 'stderr') is not None,
            'result': self.artifact_path(decorated, 'result') is not None,
        }
        return self.enrich_platform_metadata(decorated)

    def _build_request_loader(self):
        if str(self.repository.repo_path) not in sys.path:
            sys.path.insert(0, str(self.repository.repo_path))
        request_loader_module = importlib.import_module('orchestrator.request_loader')

        return request_loader_module.RequestLoader(self.repository.repo_path)

    def _build_result_builder(self):
        if str(self.repository.repo_path) not in sys.path:
            sys.path.insert(0, str(self.repository.repo_path))
        result_builder_module = importlib.import_module('orchestrator.result_builder')

        return result_builder_module.ResultBuilder()

    def _build_orchestrator_state(self):
        if str(self.repository.repo_path) not in sys.path:
            sys.path.insert(0, str(self.repository.repo_path))
        models_module = importlib.import_module('orchestrator.models')

        return models_module.OrchestratorState()

    def _build_runner(self):
        if str(self.repository.repo_path) not in sys.path:
            sys.path.insert(0, str(self.repository.repo_path))
        runner_module = importlib.import_module('orchestrator.runner')

        return runner_module.OrchestratorRunner()

    def _build_fallback_request(self, request_path: Path):
        if str(self.repository.repo_path) not in sys.path:
            sys.path.insert(0, str(self.repository.repo_path))
        models_module = importlib.import_module('orchestrator.models')

        payload = json.loads(request_path.read_text(encoding='utf-8'))
        return models_module.KpiTestModelRequest(
            payload=payload,
            env=str(payload.get('env') or '').strip().upper(),
            runtime_options=models_module.RuntimeOptions(),
            testline_resolution=None,
        )

    def _validate_selected_ues_against_context(self, payload: dict, context) -> None:
        requested_ues = list((payload.get('ue_selection') or {}).get('selected_ues') or [])
        indexed_context_ues = {ue.ue_index: ue for ue in context.ues}
        for requested_ue in requested_ues:
            ue_index = int(requested_ue['ue_index'])
            context_ue = indexed_context_ues.get(ue_index)
            if context_ue is None:
                raise ValueError(f'selected ue_index does not exist in testline configuration: {ue_index}')
            requested_type = str(requested_ue.get('ue_type') or '').strip().lower()
            if requested_type != context_ue.ue_type:
                raise ValueError(f'selected ue_type mismatch for ue_index {ue_index}: request={requested_type} actual={context_ue.ue_type}')


def get_kpi_traffic_model_adapter() -> KpiTrafficModelAdapter:
    configured_robotws = str(get_config_value('KPI_TRAFFIC_MODEL_ROBOTWS_PATH', '') or '').strip()
    configured_testline = str(get_config_value('KPI_TRAFFIC_MODEL_TESTLINE_PATH', '') or '').strip()
    robotws_root = Path(configured_robotws) if configured_robotws else (WORKSPACE_ROOT / 'kpi_traffic_model' / 'robotws')
    testline_root = Path(configured_testline) if configured_testline else (WORKSPACE_ROOT / 'kpi_traffic_model' / 'testline_configuration')
    repository = ModuleRepository(
        key='kpi-traffic-model',
        title='KPI Traffic Model',
        summary='Schema-first orchestrator for testline-driven KPI traffic workflows without Robot execution.',
        route_name='kpi_traffic_model.index',
        repo_path=WORKSPACE_ROOT / 'kpi_traffic_model',
        readme_path=(testline_root / 'README.md'),
        entry_candidates=[
            WORKSPACE_ROOT / 'kpi_traffic_model' / 'orchestrator' / 'request_loader.py',
            WORKSPACE_ROOT / 'kpi_traffic_model' / 'orchestrator' / 'config_resolver.py',
            WORKSPACE_ROOT / 'kpi_traffic_model' / 'orchestrator' / 'result_builder.py',
            WORKSPACE_ROOT / 'kpi_traffic_model' / 'orchestrator' / 'runner.py',
            robotws_root / 'bootstrap',
        ],
    )
    return KpiTrafficModelAdapter(repository)
