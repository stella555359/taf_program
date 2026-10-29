from __future__ import annotations

from .base import BaseHandler, HandlerContext


class DlBurstAppserverHandler(BaseHandler):
    model_name = 'dl_burst_appserver'

    def run(self, context: HandlerContext):
        params = dict(context.item.params)
        script_path = str(params.get('script_path') or '').strip()
        if not script_path:
            return self.build_failure(
                context,
                error_message='dl_burst_appserver requires params.script_path.',
                summary={'implementation_mode': 'skeleton_noop'},
            )
        summary = {
            'implementation_mode': 'skeleton_noop',
            'dry_run': context.request.runtime_options.dry_run,
            'script_path': script_path,
            'script_args': list(params.get('script_args') or []),
            'target_ue_labels': [ue.label for ue in context.selected_ues],
            'message': 'DL burst handler skeleton executed. Script path was validated, but no external launcher is bound yet.',
        }
        context.write_stdout(f"[dl_burst_appserver] script_path={script_path} target_ues={len(context.selected_ues)} skeleton_only\n")
        return self.build_success(context, summary=summary)
