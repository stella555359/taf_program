from __future__ import annotations

from .base import BaseHandler, HandlerContext


class AttachHandler(BaseHandler):
    model_name = "attach"

    def run(self, context: HandlerContext):
        params = dict(context.item.params)
        return self.execute_taf_action(
            context,
            "attach",
            {
                "ue_type_map": {ue.ue_index: ue.ue_type for ue in context.selected_ues},
                "ue_family_map": {ue.ue_index: ue.ue_family for ue in context.selected_ues},
                "attach_mode": params.get("attach_mode"),
                "retry": int(params.get("retry") or 0),
                "attach_timeout_seconds": int(params.get("attach_timeout_seconds") or 120),
            },
        )
