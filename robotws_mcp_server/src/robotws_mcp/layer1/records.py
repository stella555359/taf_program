"""Structured record models for Layer 1 v2."""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from typing import Any

from robotws_mcp.models import normalize_path


def stable_record_id(record_type: str, path: str = "", name: str = "", line_no: int | None = None) -> str:
    """Build a stable, readable record id from source identity fields."""

    raw = "|".join([record_type, normalize_path(path), name, str(line_no or 0)])
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]
    return f"{record_type}:{digest}"


@dataclass(frozen=True)
class CallArgument:
    kind: str
    value: str
    name: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ArgumentSchema:
    name: str
    robot_name: str
    default: str | None = None
    required: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class BoundaryFields:
    record_type: str
    domain: str = "Unknown"
    is_allowed: bool = False
    allowed_source: str = ""
    exclude_reason: str = ""
    site: str = "Unknown"
    case_type: str = "Unknown"
    feature: str | None = None


@dataclass
class RobotFileRecord(BoundaryFields):
    id: str = ""
    path: str = ""
    file_kind: str = "robot"
    parse_status: str = "ok"
    suite_documentation: list[str] = field(default_factory=list)
    force_tags: list[str] = field(default_factory=list)
    default_tags: list[str] = field(default_factory=list)
    line_no: int = 1
    end_line_no: int = 1
    raw: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TestCaseRecord(BoundaryFields):
    id: str = ""
    name: str = ""
    path: str = ""
    line_no: int = 1
    end_line_no: int = 1
    documentation: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    setup_step_ids: list[str] = field(default_factory=list)
    teardown_step_ids: list[str] = field(default_factory=list)
    body_step_ids: list[str] = field(default_factory=list)
    keyword_sequence: list[str] = field(default_factory=list)
    raw: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class KeywordRecord(BoundaryFields):
    id: str = ""
    name: str = ""
    path: str = ""
    line_no: int = 1
    end_line_no: int = 1
    documentation: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    arguments_schema: list[ArgumentSchema] = field(default_factory=list)
    step_ids: list[str] = field(default_factory=list)
    keyword_sequence: list[str] = field(default_factory=list)
    robot_impl_type: str = "unknown"
    raw: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["arguments_schema"] = [item.to_dict() for item in self.arguments_schema]
        return data


@dataclass
class StepRecord(BoundaryFields):
    id: str = ""
    owner_type: str = ""
    owner_name: str = ""
    owner_id: str = ""
    path: str = ""
    normalized_type: str = "step"
    ordinal: int = 1
    keyword: str = ""
    arguments: list[CallArgument] = field(default_factory=list)
    condition: str | None = None
    variables_input: list[str] = field(default_factory=list)
    variables_output: list[str] = field(default_factory=list)
    surface_keyword: str | None = None
    line_no: int = 1
    end_line_no: int = 1
    raw: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["arguments"] = [item.to_dict() for item in self.arguments]
        return data


@dataclass
class ResourceImportRecord(BoundaryFields):
    id: str = ""
    source_path: str = ""
    resource_path: str = ""
    resolved_path: str | None = None
    line_no: int = 1
    end_line_no: int = 1
    raw: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class LibraryImportRecord(BoundaryFields):
    id: str = ""
    source_path: str = ""
    library: str = ""
    alias: str | None = None
    arguments: list[CallArgument] = field(default_factory=list)
    resolved_path: str | None = None
    line_no: int = 1
    end_line_no: int = 1
    raw: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["arguments"] = [item.to_dict() for item in self.arguments]
        return data


@dataclass
class VariableRecord(BoundaryFields):
    id: str = ""
    source_path: str = ""
    name: str = ""
    value: str = ""
    scope: str = "file"
    line_no: int = 1
    end_line_no: int = 1
    raw: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PythonSymbolRecord(BoundaryFields):
    id: str = ""
    path: str = ""
    name: str = ""
    qualified_name: str = ""
    symbol_type: str = "function"
    signature: str = ""
    docstring: str = ""
    imports: list[str] = field(default_factory=list)
    decorators: list[str] = field(default_factory=list)
    python_impl_type: str = "unknown"
    taf_dependencies: list[str] = field(default_factory=list)
    is_robot_keyword: bool = False
    robot_keyword_name: str | None = None
    line_no: int = 1
    end_line_no: int = 1
    raw: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ParseIssueRecord(BoundaryFields):
    id: str = ""
    path: str = ""
    severity: str = "warning"
    source: str = "layer1"
    message: str = ""
    line_no: int = 1
    end_line_no: int = 1
    raw: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


Layer1Record = (
    RobotFileRecord
    | TestCaseRecord
    | KeywordRecord
    | StepRecord
    | ResourceImportRecord
    | LibraryImportRecord
    | VariableRecord
    | PythonSymbolRecord
    | ParseIssueRecord
)
