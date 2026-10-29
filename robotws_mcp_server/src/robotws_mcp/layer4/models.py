"""Structured models for Layer 4 retrieval."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class RetrievalEvidence:
    evidence_type: str
    record_id: str
    name: str
    path: str
    score: int
    match_reasons: list[str] = field(default_factory=list)
    domain: str = ""
    feature: str | None = None
    taf_dependency: dict[str, Any] | None = None
    feedback: dict[str, Any] | None = None
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RetrievalResult:
    query: str
    profile: str
    vector_status: str
    evidence: list[RetrievalEvidence]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["evidence"] = [item.to_dict() for item in self.evidence]
        return data

