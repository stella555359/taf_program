from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Sequence

from ..models import HandlerResult, KpiTestModelRequest, NormalizedUe, TestlineContext, TrafficItem


def utcnow_text() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')


@dataclass
class HandlerContext:
    request: KpiTestModelRequest
    testline_context: TestlineContext
    item: TrafficItem
    selected_ues: Sequence[NormalizedUe]
    write_stdout: Callable[[str], None]
    write_stderr: Callable[[str], None]


class BaseHandler:
    model_name = ''

    def run(self, context: HandlerContext) -> HandlerResult:
        raise NotImplementedError

    def build_success(self, context: HandlerContext, *, summary: dict, artifacts: list[str] | None = None) -> HandlerResult:
        started_at = utcnow_text()
        completed_at = utcnow_text()
        return HandlerResult(
            model=self.model_name,
            status='completed',
            started_at=started_at,
            completed_at=completed_at,
            summary=summary,
            artifacts=list(artifacts or []),
            used_ues=[ue.ue_index for ue in context.selected_ues],
            params_echo=dict(context.item.params),
            stage_id=context.item.params.get('_stage_id'),
            item_id=context.item.item_id,
        )

    def build_failure(self, context: HandlerContext, *, error_message: str, summary: dict | None = None) -> HandlerResult:
        started_at = utcnow_text()
        completed_at = utcnow_text()
        return HandlerResult(
            model=self.model_name,
            status='failed',
            started_at=started_at,
            completed_at=completed_at,
            summary=dict(summary or {}),
            artifacts=[],
            error_message=error_message,
            used_ues=[ue.ue_index for ue in context.selected_ues],
            params_echo=dict(context.item.params),
            stage_id=context.item.params.get('_stage_id'),
            item_id=context.item.item_id,
        )
