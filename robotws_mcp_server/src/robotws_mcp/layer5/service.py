"""Layer 5 template extraction service."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from robotws_mcp.layer4.service import SemanticRetrievalService
from robotws_mcp.layer5.models import TemplateStep, WorkflowTemplate
from robotws_mcp.layer5.templates import GENERIC_ROBOT_STEPS, L3_CALL_STEPS
from robotws_mcp.profiles.store import ProfileStore


class TemplateExtractionService:
    """Build reusable workflow skeletons from retrieval evidence."""

    def __init__(
        self,
        db_path: str | Path,
        layer2_db_path: str | Path,
        profile_store: ProfileStore | None = None,
        retrieval_service: SemanticRetrievalService | None = None,
    ) -> None:
        self.profile_store = profile_store or ProfileStore()
        self.retrieval = retrieval_service or SemanticRetrievalService(
            db_path=db_path,
            layer2_db_path=layer2_db_path,
            profile_store=self.profile_store,
        )

    def extract_template_from_requirement(
        self,
        requirement: str,
        profile: str = "",
        domain: str = "",
        limit: int = 3,
    ) -> dict[str, Any]:
        operation = self._detect_operation(requirement)
        return self.get_workflow_template(operation=operation, profile=profile, domain=domain, requirement=requirement, limit=limit)

    def get_workflow_template(
        self,
        operation: str,
        profile: str = "",
        domain: str = "",
        requirement: str = "",
        limit: int = 3,
    ) -> dict[str, Any]:
        normalized = _normalize_operation(operation)
        base_steps = L3_CALL_STEPS if normalized == "l3_call" else GENERIC_ROBOT_STEPS
        steps = [self._with_recommendations(step, profile, domain, limit) for step in base_steps]
        references = self.retrieval.search_evidence(
            query=requirement or operation,
            profile=profile,
            evidence_types=["testcase"],
            limit=limit,
        ).get("evidence", [])
        template = WorkflowTemplate(
            operation=normalized,
            profile=profile,
            domain=domain,
            required_steps=steps,
            forbidden_order=_forbidden_order(normalized),
            reference_cases=references,
            warnings=_warnings(normalized),
        )
        return template.to_dict()

    def recommend_template_steps(self, requirement: str, profile: str = "", domain: str = "", limit: int = 3) -> dict[str, Any]:
        template = self.extract_template_from_requirement(requirement, profile, domain, limit)
        return {
            "operation": template["operation"],
            "steps": template["required_steps"],
            "warnings": template["warnings"],
        }

    def _with_recommendations(self, step: TemplateStep, profile: str, domain: str, limit: int) -> TemplateStep:
        candidates: list[dict[str, Any]] = []
        for term in step.search_terms:
            result = self.retrieval.rank_keyword_candidates(term, profile=profile, domain=domain, limit=limit)
            for item in result.get("evidence", []):
                if item["name"] not in {candidate["name"] for candidate in candidates}:
                    candidates.append(item)
                if len(candidates) >= limit:
                    break
            if len(candidates) >= limit:
                break
        return TemplateStep(
            role=step.role,
            description=step.description,
            required=step.required,
            search_terms=step.search_terms,
            recommended_keywords=candidates[:limit],
            rationale=step.rationale,
        )

    def _detect_operation(self, requirement: str) -> str:
        lower = requirement.lower()
        if "l3" in lower or {"attach", "traffic", "detach"}.issubset(set(lower.split())):
            return "l3_call"
        return "generic_robot_case"


def _normalize_operation(operation: str) -> str:
    lower = operation.lower().replace("-", "_").replace(" ", "_")
    if "l3" in lower or "traffic" in lower:
        return "l3_call"
    return "generic_robot_case"


def _forbidden_order(operation: str) -> list[str]:
    if operation == "l3_call":
        return [
            "detach before stop_traffic",
            "check_tput before start_dl_traffic/start_ul_traffic",
            "traffic before attach",
        ]
    return []


def _warnings(operation: str) -> list[str]:
    if operation == "l3_call":
        return [
            "Generated case must include cleanup for both traffic and UE attach state.",
            "Setup/teardown must come from the active domain or allowed common resource scope.",
        ]
    return []

