"""Shared data models for RobotWS indexing and retrieval."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


def normalize_path(path: str | Path) -> str:
    """Return a stable path string for indexes and API responses."""

    return str(Path(path)).replace("\\", "/")


@dataclass(frozen=True)
class LibraryImport:
    path: str
    library: str
    alias: str | None = None
    section: str = "Settings"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ResourceImport:
    path: str
    resource: str
    section: str = "Settings"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RobotStep:
    keyword: str
    raw: str
    line_no: int
    args: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RobotCase:
    name: str
    path: str
    line_no: int
    documentation: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    setup: str | None = None
    teardown: str | None = None
    steps: list[RobotStep] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["called_keywords"] = [step.keyword for step in self.steps]
        return data


@dataclass
class RobotKeyword:
    name: str
    path: str
    line_no: int
    arguments: list[str] = field(default_factory=list)
    documentation: list[str] = field(default_factory=list)
    steps: list[RobotStep] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["called_keywords"] = [step.keyword for step in self.steps]
        return data


@dataclass
class RobotFile:
    path: str
    resources: list[ResourceImport] = field(default_factory=list)
    libraries: list[LibraryImport] = field(default_factory=list)
    documentation: list[str] = field(default_factory=list)
    variables: dict[str, str] = field(default_factory=dict)
    force_tags: list[str] = field(default_factory=list)
    cases: list[RobotCase] = field(default_factory=list)
    keywords: list[RobotKeyword] = field(default_factory=list)
    parse_warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "resources": [item.to_dict() for item in self.resources],
            "libraries": [item.to_dict() for item in self.libraries],
            "documentation": self.documentation,
            "variables": self.variables,
            "force_tags": self.force_tags,
            "cases": [item.to_dict() for item in self.cases],
            "keywords": [item.to_dict() for item in self.keywords],
            "parse_warnings": self.parse_warnings,
        }


@dataclass(frozen=True)
class PythonSymbol:
    path: str
    name: str
    symbol_type: str
    line_no: int
    signature: str = ""
    docstring: str = ""
    imports: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CallEdge:
    caller_type: str
    caller_name: str
    callee_name: str
    path: str
    line_no: int
    raw: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class StyleProfile:
    name: str
    description: str
    path_scopes: list[str]
    preferred_keywords: dict[str, list[str]]
    negative_patterns: list[dict[str, str]]
    style_rules: list[str]
    required_fields: list[str]
    profile_type: str = "style"
    area: str | None = None
    case_type: str | None = None
    case_candidate_scopes: list[str] = field(default_factory=list)
    confirmed_case_scopes: list[str] = field(default_factory=list)
    allowed_resource_scopes: list[str] = field(default_factory=list)
    feature_allowlist: dict[str, list[str]] = field(default_factory=dict)
    hard_exclude_patterns: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FeatureOwnership:
    area: str
    feature: str
    path: str
    status: str
    source: str
    case_count: int = 0
    resource_imports: list[str] = field(default_factory=list)
    exclude_reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DiscoveryReport:
    summary: dict[str, int]
    features: list[FeatureOwnership]

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary,
            "features": [feature.to_dict() for feature in self.features],
        }
