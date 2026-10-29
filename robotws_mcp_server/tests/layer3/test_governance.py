from __future__ import annotations

from robotws_mcp.layer3.governance import GovernanceEngine
from robotws_mcp.layer3.models import TafUsageEvidence


def test_existing_sg6_wrapper_is_allowed() -> None:
    decision = GovernanceEngine().evaluate_taf_usage(
        TafUsageEvidence(
            operation="capture wireshark",
            requested_call="Start Container Capture Wireshark Log",
            existing_wrapper={
                "name": "Start Container Capture Wireshark Log",
                "path": "testsuite/Hangzhou/resources/RAN_PZ_HAZ_34/lines/SG6/Resources.robot",
            },
        )
    )

    assert decision.decision == "allow"
    assert decision.rule_id == "taf_usage.existing_sg6_wrapper"


def test_new_wrapper_is_allowed_when_grounded_by_sg6_and_taf_docs() -> None:
    decision = GovernanceEngine().evaluate_taf_usage(
        TafUsageEvidence(
            operation="capture wireshark",
            requested_call="Capture Custom Wireshark For New Scenario",
            sg6_evidence=[
                {
                    "keyword": "Start Container Capture Wireshark Log",
                    "path": "testsuite/Hangzhou/resources/RAN_PZ_HAZ_34/lines/SG6/Logs.robot",
                }
            ],
            taf_mcp_docs=[
                {
                    "library": "taf.analyzer.pcap",
                    "function": "start_capture",
                    "url": "taf://docs/pcap/start_capture",
                }
            ],
            has_multiple_taf_candidates=True,
            sg6_selects_candidate=True,
            library_choice_matches_sg6=True,
            parameter_pattern_matches_sg6=True,
            setup_teardown_aligned=True,
            cleanup_aligned=True,
        )
    )

    assert decision.decision == "allow"
    assert decision.rule_id == "taf_usage.grounded_direct_or_new_wrapper"


def test_direct_taf_usage_requires_sg6_evidence() -> None:
    decision = GovernanceEngine().evaluate_taf_usage(
        TafUsageEvidence(
            operation="capture wireshark",
            requested_call="taf.some.capture.Start",
            taf_mcp_docs=[{"library": "taf.some.capture"}],
            library_choice_matches_sg6=True,
            parameter_pattern_matches_sg6=True,
            setup_teardown_aligned=True,
            cleanup_aligned=True,
        )
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "taf_usage.missing_sg6_evidence"


def test_direct_taf_usage_requires_taf_mcp_docs() -> None:
    decision = GovernanceEngine().evaluate_taf_usage(
        TafUsageEvidence(
            operation="capture wireshark",
            requested_call="Capture Custom Wireshark For New Scenario",
            sg6_evidence=[{"keyword": "Start Container Capture Wireshark Log"}],
            library_choice_matches_sg6=True,
            parameter_pattern_matches_sg6=True,
            setup_teardown_aligned=True,
            cleanup_aligned=True,
        )
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "taf_usage.missing_taf_mcp_docs"


def test_multiple_taf_candidates_require_sg6_choice() -> None:
    decision = GovernanceEngine().evaluate_taf_usage(
        TafUsageEvidence(
            operation="capture wireshark",
            requested_call="Capture Custom Wireshark For New Scenario",
            sg6_evidence=[{"keyword": "Start Container Capture Wireshark Log"}],
            taf_mcp_docs=[{"library": "taf.capture.a"}, {"library": "taf.capture.b"}],
            has_multiple_taf_candidates=True,
            sg6_selects_candidate=False,
            library_choice_matches_sg6=True,
            parameter_pattern_matches_sg6=True,
            setup_teardown_aligned=True,
            cleanup_aligned=True,
        )
    )

    assert decision.decision == "deny"
    assert decision.rule_id == "taf_usage.multiple_candidates_without_sg6_choice"


def test_excluded_or_conflicting_evidence_is_denied() -> None:
    excluded_decision = GovernanceEngine().evaluate_taf_usage(
        TafUsageEvidence(
            operation="capture wireshark",
            requested_call="Capture Custom Wireshark For New Scenario",
            uses_excluded_evidence=True,
        )
    )
    conflicting_decision = GovernanceEngine().evaluate_taf_usage(
        TafUsageEvidence(
            operation="capture wireshark",
            requested_call="Capture Custom Wireshark For New Scenario",
            sg6_evidence=[{"keyword": "Start Container Capture Wireshark Log"}],
            taf_mcp_docs=[{"library": "taf.analyzer.pcap"}],
            conflicts_with_sg6=True,
        )
    )

    assert excluded_decision.decision == "deny"
    assert excluded_decision.rule_id == "taf_usage.excluded_evidence"
    assert conflicting_decision.decision == "deny"
    assert conflicting_decision.rule_id == "taf_usage.conflicts_with_sg6"

