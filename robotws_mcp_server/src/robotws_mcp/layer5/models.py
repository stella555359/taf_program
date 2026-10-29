"""Structured models for Layer 5 workflow templates."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class TemplateStep:
    role: str
    description: str
    required: bool = True
    search_terms: list[str] = field(default_factory=list)
    recommended_keywords: list[dict[str, Any]] = field(default_factory=list)
    rationale: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class WorkflowTemplate:
    operation: str
    profile: str
    domain: str
    required_steps: list[TemplateStep]
    optional_steps: list[TemplateStep] = field(default_factory=list)
    forbidden_order: list[str] = field(default_factory=list)
    reference_cases: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["required_steps"] = [item.to_dict() for item in self.required_steps]
        data["optional_steps"] = [item.to_dict() for item in self.optional_steps]
        return data

