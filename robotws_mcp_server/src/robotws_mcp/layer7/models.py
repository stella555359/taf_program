"""Models for execution feedback records."""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class ExecutionFeedback:
    id: str
    source_type: str
    source_path: str = ""
    test_name: str = ""
    keyword_name: str = ""
    status: str = "unknown"
    failure_class: str = ""
    message: str = ""
    elapsed_ms: int = 0
    profile: str = ""
    testline: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def feedback_id(*parts: str) -> str:
    raw = "|".join(parts)
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]
    return f"feedback:{digest}"

