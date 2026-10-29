from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config_resolver import EnvConfigResolver
from .models import KpiTestModelRequest, ResolvedConfig, RuntimeOptions, SUPPORTED_TRAFFIC_MODELS


class RequestValidationError(ValueError):
    pass


class RequestLoader:
    def __init__(self, repository_root: Path | None = None):
        self.repository_root = repository_root or Path(__file__).resolve().parents[1]
        self.config_resolver = EnvConfigResolver(self.repository_root)

    def load_json_file(self, path: Path) -> KpiTestModelRequest:
        return self.load_dict(json.loads(path.read_text(encoding='utf-8')))

    def load_dict(self, payload: dict[str, Any]) -> KpiTestModelRequest:
        self.validate_payload(payload)
        request = KpiTestModelRequest.from_dict(payload)
        request.testline_resolution = self._load_resolved_config(payload)
        request.runtime_options = self._load_runtime_options(payload)
        return request

    def validate_payload(self, payload: dict[str, Any]) -> None:
        env = str(payload.get('env') or '').strip().upper()
        if not env:
            raise RequestValidationError('env is required.')

        self.config_resolver.resolve_env(env)

        testline_resolution = payload.get('testline_resolution') or {}
        if testline_resolution and not isinstance(testline_resolution, dict):
            raise RequestValidationError('testline_resolution must be an object.')

        ue_selection = payload.get('ue_selection') or {}
        if not isinstance(ue_selection, dict):
            raise RequestValidationError('ue_selection must be an object.')
        selected_ues = ue_selection.get('selected_ues') or []
        if not isinstance(selected_ues, list) or not selected_ues:
            raise RequestValidationError('selected_ues must contain at least one UE object.')
        seen_ue_indexes: set[int] = set()
        for selected_ue in selected_ues:
            if not isinstance(selected_ue, dict):
                raise RequestValidationError('Each selected UE must be an object, not a label string.')
            missing_keys = [key for key in ('ue_index', 'ue_type', 'label') if key not in selected_ue]
            if missing_keys:
                missing_text = ', '.join(missing_keys)
                raise RequestValidationError(f'Each selected UE object must include: {missing_text}')
            try:
                ue_index = int(selected_ue['ue_index'])
            except (TypeError, ValueError) as exc:
                raise RequestValidationError('selected_ue.ue_index must be an integer.') from exc
            if ue_index in seen_ue_indexes:
                raise RequestValidationError(f'selected_ues contains duplicate ue_index: {ue_index}')
            seen_ue_indexes.add(ue_index)
            if str(selected_ue.get('ue_type') or '').strip() == '':
                raise RequestValidationError('selected_ue.ue_type must not be empty.')
            if str(selected_ue.get('label') or '').strip() == '':
                raise RequestValidationError('selected_ue.label must not be empty.')

        same_type_mode = str(ue_selection.get('same_type_execution_mode') or 'serial')
        cross_type_mode = str(ue_selection.get('cross_type_execution_mode') or 'serial')
        if same_type_mode not in {'serial', 'parallel'}:
            raise RequestValidationError('same_type_execution_mode must be serial or parallel.')
        if cross_type_mode not in {'serial', 'parallel'}:
            raise RequestValidationError('cross_type_execution_mode must be serial or parallel.')

        traffic_plan = payload.get('traffic_plan') or {}
        if not isinstance(traffic_plan, dict):
            raise RequestValidationError('traffic_plan must be an object.')
        stages = traffic_plan.get('stages') or []
        if not stages:
            raise RequestValidationError('traffic_plan.stages is required.')
        seen_stage_ids: set[int] = set()
        for stage in stages:
            if not isinstance(stage, dict):
                raise RequestValidationError('Each stage must be an object.')
            try:
                stage_id = int(stage.get('stage_id'))
            except (TypeError, ValueError) as exc:
                raise RequestValidationError('stage_id must be an integer.') from exc
            if stage_id in seen_stage_ids:
                raise RequestValidationError(f'Duplicate stage_id: {stage_id}')
            seen_stage_ids.add(stage_id)
            stage_mode = str(stage.get('execution_mode') or '').strip()
            if stage_mode not in {'serial', 'parallel'}:
                raise RequestValidationError('stage.execution_mode must be serial or parallel.')
            items = stage.get('items') or []
            if not items:
                raise RequestValidationError(f'stage {stage_id} must contain at least one traffic item.')
            seen_item_ids: set[str] = set()
            for item in items:
                if not isinstance(item, dict):
                    raise RequestValidationError('Each traffic item must be an object.')
                item_id = str(item.get('item_id') or '').strip()
                if not item_id:
                    raise RequestValidationError('Each traffic item must define item_id.')
                if item_id in seen_item_ids:
                    raise RequestValidationError(f'Duplicate item_id within stage {stage_id}: {item_id}')
                seen_item_ids.add(item_id)
                model_name = str(item.get('model') or '').strip()
                if model_name not in SUPPORTED_TRAFFIC_MODELS:
                    supported_text = ', '.join(SUPPORTED_TRAFFIC_MODELS)
                    raise RequestValidationError(f'Only these traffic models are supported in MVP: {supported_text}')
                item_mode = str(item.get('execution_mode') or '').strip()
                if item_mode not in {'serial', 'parallel'}:
                    raise RequestValidationError(f'{item_id}.execution_mode must be serial or parallel.')
                ue_scope = item.get('ue_scope') or {}
                if not isinstance(ue_scope, dict) or str(ue_scope.get('mode') or '').strip() == '':
                    raise RequestValidationError(f'{item_id}.ue_scope.mode is required.')
                if model_name == 'dl_burst_appserver' and bool(item.get('enabled', True)):
                    params = item.get('params') or {}
                    self.config_resolver.validate_script_path(env, str(params.get('script_path') or ''))
                if model_name == 'attach':
                    params = item.get('params') or {}
                    if 'attach_timeout_seconds' in params:
                        try:
                            int(params['attach_timeout_seconds'])
                        except (TypeError, ValueError) as exc:
                            raise RequestValidationError(f'{item_id}.params.attach_timeout_seconds must be an integer.') from exc

        runtime_options = payload.get('runtime_options') or {}
        if not isinstance(runtime_options, dict):
            raise RequestValidationError('runtime_options must be an object.')
        try:
            max_parallel_workers = int(runtime_options.get('max_parallel_workers') or 4)
        except (TypeError, ValueError) as exc:
            raise RequestValidationError('max_parallel_workers must be an integer.') from exc
        if max_parallel_workers <= 0:
            raise RequestValidationError('max_parallel_workers must be greater than 0.')

        portal_followups = payload.get('portal_followups') or {}
        if portal_followups and not isinstance(portal_followups, dict):
            raise RequestValidationError('portal_followups must be an object.')

    def _load_resolved_config(self, payload: dict[str, Any]) -> ResolvedConfig:
        env = str(payload['env']).strip().upper()
        provided = payload.get('testline_resolution') or {}
        resolved = self.config_resolver.resolve_env(env)
        if provided:
            config_id = str(provided.get('config_id') or '')
            if config_id and config_id != resolved.config_id:
                raise RequestValidationError('testline_resolution.config_id must match env_map.json.')
        return resolved

    def _load_runtime_options(self, payload: dict[str, Any]) -> RuntimeOptions:
        options = payload.get('runtime_options') or {}
        return RuntimeOptions(
            dry_run=bool(options.get('dry_run')),
            stop_on_failure=bool(options.get('stop_on_failure', True)),
            max_parallel_workers=int(options.get('max_parallel_workers') or 4),
            log_level=str(options.get('log_level') or 'INFO').upper(),
        )
