from __future__ import annotations

from .base import BaseHandler, HandlerContext


class ApplyPreconditionsHandler(BaseHandler):
    model_name = 'apply_preconditions'

    def run(self, context: HandlerContext):
        params = dict(context.item.params)
        summary = {
            'implementation_mode': 'skeleton_noop',
            'dry_run': context.request.runtime_options.dry_run,
            'requested_preconditions': {
                'cell_barred': params.get('cell_barred'),
                'pa_port_state': params.get('pa_port_state'),
                'notes': params.get('notes'),
            },
            'target_ue_count': len(context.selected_ues),
            'message': 'Preconditions handler is wired into the orchestrator, but external TAF actions are not bound yet.',
        }
        context.write_stdout(f"[apply_preconditions] {summary['message']}\n")
        return self.build_success(context, summary=summary)
