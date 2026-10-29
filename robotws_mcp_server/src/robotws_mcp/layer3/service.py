"""Layer 3 query-facing governance service."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from robotws_mcp.layer1.boundary import classify_path
from robotws_mcp.layer2.query import Layer2QueryService
from robotws_mcp.layer3.governance import GovernanceEngine
from robotws_mcp.layer3.models import GovernanceDecision, TafUsageEvidence
from robotws_mcp.models import normalize_path
from robotws_mcp.profiles.store import ProfileStore
from robotws_mcp.validation.style_validator import StyleValidator


class GovernanceService:
    """Tool-oriented wrapper around Layer 3 governance rules."""

    def __init__(
        self,
        layer2_db_path: str | Path,
        profile_store: ProfileStore | None = None,
    ) -> None:
        self.profile_store = profile_store or ProfileStore()
        self.layer2_query = Layer2QueryService(layer2_db_path)
        self.engine = GovernanceEngine()
        self.style_validator = StyleValidator()

    def evaluate_taf_usage(self, evidence: dict[str, Any]) -> dict[str, Any]:
        return self.engine.evaluate_taf_usage(TafUsageEvidence(**evidence)).to_dict()

    def explain_allowed_boundary(self, record_id_or_path: str, profile: str = "Hangzhou_SG6_Common") -> dict[str, Any]:
        style_profile = self.profile_store.effective(profile) or self.profile_store.get(profile)
        candidate = self._find_layer2_node(record_id_or_path)
        path = normalize_path(candidate.get("path", "")) if candidate else normalize_path(record_id_or_path)
        decision = classify_path(path, style_profile, str(candidate.get("node_type", "") if candidate else ""))
        if decision.is_allowed:
            governance = GovernanceDecision(
                decision="allow",
                rule_id="boundary.allowed",
                severity="info",
                reason=f"Path is allowed by {decision.allowed_source}.",
                evidence={**decision.__dict__, "path": path, "candidate": candidate},
            )
        else:
            governance = GovernanceDecision(
                decision="deny",
                rule_id="boundary.excluded",
                severity="error",
                reason=decision.exclude_reason or "Path is outside allowed boundary.",
                evidence={**decision.__dict__, "path": path, "candidate": candidate},
            )
        return governance.to_dict()

    def filter_generation_context(
        self,
        candidate_ids: list[str],
        profile: str = "Hangzhou_SG6_Common",
    ) -> dict[str, Any]:
        allowed: list[dict[str, Any]] = []
        denied: list[dict[str, Any]] = []
        for candidate_id in candidate_ids:
            candidate = self._find_layer2_node(candidate_id)
            if not candidate:
                denied.append(
                    GovernanceDecision(
                        decision="deny",
                        rule_id="context.candidate_not_found",
                        severity="error",
                        reason="Candidate was not found in Layer 2 graph.",
                        evidence={"candidate_id": candidate_id},
                    ).to_dict()
                )
                continue
            boundary = self.explain_allowed_boundary(str(candidate.get("node_id") or candidate.get("record_id")), profile)
            if boundary["decision"] == "allow" and candidate.get("is_allowed", False):
                allowed.append({"candidate": candidate, "decision": boundary})
            else:
                denied.append(
                    boundary
                    if boundary["decision"] == "deny"
                    else GovernanceDecision(
                        decision="deny",
                        rule_id="context.excluded_candidate",
                        severity="error",
                        reason="Candidate is marked as excluded by Layer 1/2 boundary facts.",
                        evidence={"candidate": candidate, "boundary": boundary},
                    ).to_dict()
                )
        return {"allowed": allowed, "denied": denied}

    def validate_generated_robot(self, robot_text: str, profile: str = "Hangzhou_SG6_Common") -> dict[str, Any]:
        style_profile = self.profile_store.effective(profile) or self.profile_store.get(profile)
        style_result = self.style_validator.validate(robot_text, style_profile).to_dict()
        if style_result["errors"]:
            decision = GovernanceDecision(
                decision="deny",
                rule_id="generated_robot.style_errors",
                severity="error",
                reason="Generated Robot text has blocking style errors.",
                evidence={"style": style_result},
            )
        elif style_result["warnings"]:
            decision = GovernanceDecision(
                decision="warn",
                rule_id="generated_robot.style_warnings",
                severity="warning",
                reason="Generated Robot text has style warnings.",
                evidence={"style": style_result},
            )
        else:
            decision = GovernanceDecision(
                decision="allow",
                rule_id="generated_robot.style_passed",
                severity="info",
                reason="Generated Robot text passed current governance style checks.",
                evidence={"style": style_result},
            )
        return decision.to_dict()

    def _find_layer2_node(self, record_id_or_path: str) -> dict[str, Any] | None:
        direct = self.layer2_query.store.node(record_id_or_path)
        if direct:
            return direct
        matches = self.layer2_query.store.nodes(query=record_id_or_path, limit=20)
        for item in matches:
            if record_id_or_path in {item.get("record_id"), item.get("node_id"), item.get("path"), item.get("name")}:
                return item
        return matches[0] if len(matches) == 1 else None

