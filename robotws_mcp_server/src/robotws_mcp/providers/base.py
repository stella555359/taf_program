"""Provider interfaces reserved for future AI integration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class CaseSummaryRequest:
    context: dict[str, Any]


@dataclass(frozen=True)
class CaseSummaryResult:
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RobotCaseGenerationRequest:
    context: dict[str, Any]


@dataclass(frozen=True)
class RobotCaseGenerationResult:
    robot_text: str
    generation_basis: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    missing_inputs: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class RobotCaseReviewRequest:
    robot_text: str
    context: dict[str, Any]


@dataclass(frozen=True)
class RobotCaseReviewResult:
    passed: bool
    findings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class FailureClassificationRequest:
    evidence: dict[str, Any]


@dataclass(frozen=True)
class FailureClassificationResult:
    category: str
    confidence: float
    rationale: str


class AiProvider(Protocol):
    """Optional LLM-backed provider interface."""

    def summarize_case(self, request: CaseSummaryRequest) -> CaseSummaryResult:
        raise NotImplementedError

    def generate_robot_case(self, request: RobotCaseGenerationRequest) -> RobotCaseGenerationResult:
        raise NotImplementedError

    def review_robot_case(self, request: RobotCaseReviewRequest) -> RobotCaseReviewResult:
        raise NotImplementedError

    def classify_failure(self, request: FailureClassificationRequest) -> FailureClassificationResult:
        raise NotImplementedError


class EmbeddingProvider(Protocol):
    """Optional embedding provider for future semantic retrieval."""

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError


class RerankerProvider(Protocol):
    """Optional reranker provider for future retrieval improvements."""

    def rerank(self, query: str, documents: list[dict[str, Any]]) -> list[dict[str, Any]]:
        raise NotImplementedError


class WorkflowProvider(Protocol):
    """Optional workflow backend such as Insights Fusion."""

    def run_workflow(self, workflow_name: str, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


class NoopAiProvider:
    """Default provider: AI is intentionally disabled in MVP."""

    def summarize_case(self, request: CaseSummaryRequest) -> CaseSummaryResult:
        return CaseSummaryResult(summary="", metadata={"provider": "noop", "enabled": False})

    def generate_robot_case(self, request: RobotCaseGenerationRequest) -> RobotCaseGenerationResult:
        return RobotCaseGenerationResult(
            robot_text="",
            generation_basis=[],
            assumptions=["AI provider is disabled; use context_only mode."],
            missing_inputs=[],
        )

    def review_robot_case(self, request: RobotCaseReviewRequest) -> RobotCaseReviewResult:
        return RobotCaseReviewResult(passed=False, findings=["AI provider is disabled; use style validation."])

    def classify_failure(self, request: FailureClassificationRequest) -> FailureClassificationResult:
        return FailureClassificationResult(
            category="unknown",
            confidence=0.0,
            rationale="AI provider is disabled.",
        )
