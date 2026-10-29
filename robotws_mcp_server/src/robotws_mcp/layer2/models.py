"""Structured models for Layer 2 keyword graph records."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class GraphNode:
    node_id: str
    node_type: str
    record_id: str = ""
    name: str = ""
    path: str = ""
    domain: str = "Unknown"
    feature: str | None = None
    is_allowed: bool = True
    impl_type: str = "unknown"
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GraphEdge:
    edge_id: str
    edge_type: str
    source_node_id: str
    target_node_id: str
    source_record_id: str = ""
    target_record_id: str = ""
    step_id: str = ""
    ordinal: int = 0
    resolution_status: str = ""
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ResolutionResult:
    step_id: str
    owner_id: str
    called_name: str
    normalized_called_name: str
    resolution_status: str
    called_target_node_id: str = ""
    called_target_record_id: str = ""
    library_kind: str = ""
    reason: str = ""
    candidates: list[dict[str, Any]] = field(default_factory=list)
    import_evidence: list[str] = field(default_factory=list)
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DependencySummary:
    record_id: str
    node_id: str
    node_type: str
    impl_type: str
    has_taf_dependency: bool = False
    evidence_paths: list[list[str]] = field(default_factory=list)
    unknown_reasons: list[str] = field(default_factory=list)
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Layer2BuildSummary:
    nodes: int = 0
    edges: int = 0
    resolution_status_counts: dict[str, int] = field(default_factory=dict)
    dependency_summary_counts: dict[str, int] = field(default_factory=dict)
    layer1_record_count: int = 0
    sqlite_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

