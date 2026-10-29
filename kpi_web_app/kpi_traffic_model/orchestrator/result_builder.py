from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import KpiTestModelRequest, OrchestratorState, TestlineContext


class ResultBuilder:
    def build_success(
        self,
        request: KpiTestModelRequest,
        context: TestlineContext,
        state: OrchestratorState,
        *,
        timestamps: dict[str, str | None],
        artifacts: dict[str, Any],
    ) -> dict[str, Any]:
        if not state.kpi_test_starttime or not state.kpi_test_endtime:
            raise ValueError('result.json must include kpi_test_starttime and kpi_test_endtime.')

        return {
            'job_type': 'kpi_test_model',
            'job_version': request.payload.get('job_version', '1.0'),
            'job_id': request.payload.get('job_id'),
            'status': 'completed',
            'error_message': None,
            'env': request.env,
            'request_echo': dict(request.payload),
            'testline_config': self._serialize_resolved_config(context),
            'environment_summary': dict(context.raw_summary),
            'selected_ues': list(request.payload.get('ue_selection', {}).get('selected_ues') or [self._serialize_ue(item) for item in context.ues]),
            'kpi_test_starttime': state.kpi_test_starttime,
            'kpi_test_endtime': state.kpi_test_endtime,
            'precondition_results': [self._serialize_handler_result(item) for item in state.precondition_results],
            'traffic_results': [self._serialize_handler_result(item) for item in state.traffic_results],
            'sidecar_results': [self._serialize_handler_result(item) for item in state.sidecar_results],
            'followup_results': dict(state.followup_results),
            'artifacts': dict(artifacts),
            'summary': {
                'preconditions_total': len(state.precondition_results),
                'preconditions_completed': sum(1 for item in state.precondition_results if item.status == 'completed'),
                'traffic_total': len(state.traffic_results),
                'traffic_completed': sum(1 for item in state.traffic_results if item.status == 'completed'),
                'traffic_failed': sum(1 for item in state.traffic_results if item.status == 'failed'),
                'sidecars_total': len(state.sidecar_results),
                'sidecars_completed': sum(1 for item in state.sidecar_results if item.status == 'completed'),
            },
            'timestamps': dict(timestamps),
        }

    def build_failure(
        self,
        request: KpiTestModelRequest,
        state: OrchestratorState,
        *,
        error_message: str,
        timestamps: dict[str, str | None],
        artifacts: dict[str, Any],
        context: TestlineContext | None = None,
    ) -> dict[str, Any]:
        payload = {
            'job_type': 'kpi_test_model',
            'job_version': request.payload.get('job_version', '1.0'),
            'job_id': request.payload.get('job_id'),
            'status': 'failed',
            'error_message': error_message,
            'env': request.env,
            'request_echo': dict(request.payload),
            'kpi_test_starttime': state.kpi_test_starttime,
            'kpi_test_endtime': state.kpi_test_endtime,
            'precondition_results': [self._serialize_handler_result(item) for item in state.precondition_results],
            'traffic_results': [self._serialize_handler_result(item) for item in state.traffic_results],
            'sidecar_results': [self._serialize_handler_result(item) for item in state.sidecar_results],
            'followup_results': dict(state.followup_results),
            'artifacts': dict(artifacts),
            'timestamps': dict(timestamps),
        }
        if context is not None:
            payload['testline_config'] = self._serialize_resolved_config(context)
            payload['environment_summary'] = dict(context.raw_summary)
            payload['selected_ues'] = list(request.payload.get('ue_selection', {}).get('selected_ues') or [self._serialize_ue(item) for item in context.ues])
        return payload

    def write(self, result: dict[str, Any], path: Path) -> None:
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')

    def _serialize_resolved_config(self, context: TestlineContext) -> dict[str, Any]:
        resolved = context.resolved_config
        return {
            'config_id': resolved.config_id,
            'config_path': str(resolved.config_path),
            'department': resolved.department,
            'site': resolved.site,
            'topology_id': resolved.topology_id,
            'match_type': resolved.match_type,
            'confidence': resolved.confidence,
        }

    def _serialize_ue(self, ue) -> dict[str, Any]:
        return {
            'ue_index': ue.ue_index,
            'ue_type': ue.ue_type,
            'ue_ip': ue.ue_ip,
            'label': ue.label,
            'serial_number': ue.serial_number,
            'capabilities': list(ue.capabilities),
        }

    def _serialize_handler_result(self, result) -> dict[str, Any]:
        return {
            'stage_id': result.stage_id,
            'item_id': result.item_id,
            'model': result.model,
            'status': result.status,
            'started_at': result.started_at,
            'completed_at': result.completed_at,
            'used_ues': list(result.used_ues),
            'params_echo': dict(result.params_echo),
            'summary': dict(result.summary),
            'artifacts': list(result.artifacts),
            'error_message': result.error_message,
        }
