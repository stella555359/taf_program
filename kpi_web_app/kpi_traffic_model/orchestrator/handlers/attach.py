from __future__ import annotations

from .base import BaseHandler, HandlerContext


class AttachHandler(BaseHandler):
    model_name = 'attach'

    def run(self, context: HandlerContext):
        params = dict(context.item.params)
        timeout_seconds = int(params.get('attach_timeout_seconds') or 120)
        summary = {
            'implementation_mode': 'skeleton_noop',
            'dry_run': context.request.runtime_options.dry_run,
            'attach_timeout_seconds': timeout_seconds,
            'target_ue_labels': [ue.label for ue in context.selected_ues],
            'message': 'Attach handler skeleton executed. Real TAF attach binding is still pending.',
        }
        context.write_stdout(f"[attach] target_ues={len(context.selected_ues)} timeout={timeout_seconds}s skeleton_only\n")
        return self.build_success(context, summary=summary)
