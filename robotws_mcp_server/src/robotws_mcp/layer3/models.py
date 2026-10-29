"""Structured models for Layer 3 governance decisions."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class GovernanceDecision:
    decision: str
    rule_id: str
    severity: str
    reason: str
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TafUsageEvidence:
    """Evidence bundle for evaluating direct or newly wrapped TAF usage."""

    operation: str
    requested_call: str = ""
    sg6_evidence: list[dict[str, Any]] = field(default_factory=list)
    taf_mcp_docs: list[dict[str, Any]] = field(default_factory=list)
    existing_wrapper: dict[str, Any] | None = None
    uses_excluded_evidence: bool = False
    has_multiple_taf_candidates: bool = False
    sg6_selects_candidate: bool = False
    library_choice_matches_sg6: bool = False
    parameter_pattern_matches_sg6: bool = False
    setup_teardown_aligned: bool = False
    cleanup_aligned: bool = False
    conflicts_with_sg6: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

