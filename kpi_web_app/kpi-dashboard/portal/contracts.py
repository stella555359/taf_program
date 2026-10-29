from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class ModuleCapabilityContract:
    supports_cancel: bool
    supports_delete: bool
    supports_rerun: bool
    supports_preview: bool
    supports_auto_trigger: bool
    supports_status_api: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class JobContract:
    module_key: str
    statuses: List[str]
    artifact_kinds: List[str]
    progress_fields: List[str]
    linked_job_fields: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SummaryContract:
    result_payload_key: str
    summary_fields: List[str]
    ui_fields: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)