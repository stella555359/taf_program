"""Governance rules for generation and validation."""

from __future__ import annotations

from robotws_mcp.layer3.models import GovernanceDecision, TafUsageEvidence


class GovernanceEngine:
    """Evaluate deterministic governance decisions from Layer 1/2 evidence."""

    def evaluate_taf_usage(self, evidence: TafUsageEvidence) -> GovernanceDecision:
        """Allow direct/new TAF usage only when grounded in SG6 and TAF MCP evidence."""

        base_evidence = evidence.to_dict()
        if evidence.uses_excluded_evidence:
            return _deny(
                "taf_usage.excluded_evidence",
                "TAF usage is based on excluded RobotWS evidence and cannot enter generation context.",
                base_evidence,
            )
        if evidence.conflicts_with_sg6:
            return _deny(
                "taf_usage.conflicts_with_sg6",
                "TAF usage conflicts with SG6-proven library choice or parameter conventions.",
                base_evidence,
            )
        if evidence.existing_wrapper:
            return GovernanceDecision(
                decision="allow",
                rule_id="taf_usage.existing_sg6_wrapper",
                severity="info",
                reason="Existing SG6 Robot keyword wrapper is available and preferred.",
                evidence=base_evidence,
            )
        if not evidence.sg6_evidence:
            return _deny(
                "taf_usage.missing_sg6_evidence",
                "Direct or newly wrapped TAF usage requires SG6 RobotWS evidence.",
                base_evidence,
            )
        if not evidence.taf_mcp_docs:
            return _deny(
                "taf_usage.missing_taf_mcp_docs",
                "Direct or newly wrapped TAF usage requires authoritative TAF MCP documentation.",
                base_evidence,
            )
        if evidence.has_multiple_taf_candidates and not evidence.sg6_selects_candidate:
            return _deny(
                "taf_usage.multiple_candidates_without_sg6_choice",
                "Multiple TAF APIs are available, but SG6 evidence does not identify the correct choice.",
                base_evidence,
            )

        missing_alignment = []
        if not evidence.library_choice_matches_sg6:
            missing_alignment.append("library choice")
        if not evidence.parameter_pattern_matches_sg6:
            missing_alignment.append("parameter pattern")
        if not evidence.setup_teardown_aligned:
            missing_alignment.append("setup/teardown expectation")
        if not evidence.cleanup_aligned:
            missing_alignment.append("cleanup pattern")
        if missing_alignment:
            return _deny(
                "taf_usage.not_aligned_with_sg6_pattern",
                "TAF usage is not aligned with SG6-proven " + ", ".join(missing_alignment) + ".",
                base_evidence,
            )

        return GovernanceDecision(
            decision="allow",
            rule_id="taf_usage.grounded_direct_or_new_wrapper",
            severity="info",
            reason=(
                "Direct TAF usage or a new Robot Framework wrapper is allowed because it is grounded by "
                "SG6 RobotWS evidence and authoritative TAF MCP documentation."
            ),
            evidence=base_evidence,
        )


def _deny(rule_id: str, reason: str, evidence: dict[str, object]) -> GovernanceDecision:
    return GovernanceDecision(
        decision="deny",
        rule_id=rule_id,
        severity="error",
        reason=reason,
        evidence=evidence,
    )

