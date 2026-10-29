from __future__ import annotations

from .base import BaseHandler, HandlerContext


class DetachHandler(BaseHandler):
    model_name = 'detach'

    def run(self, context: HandlerContext):
        summary = {
            'implementation_mode': 'skeleton_noop',
            'dry_run': context.request.runtime_options.dry_run,
            'target_ue_labels': [ue.label for ue in context.selected_ues],
            'message': 'Detach handler skeleton executed. Real TAF detach binding is still pending.',
        }
        context.write_stdout(f"[detach] target_ues={len(context.selected_ues)} skeleton_only\n")
        return self.build_success(context, summary=summary)
