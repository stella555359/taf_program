from __future__ import annotations

from robotws_mcp.layer1.boundary import classify_path
from robotws_mcp.models import StyleProfile


def _profile() -> StyleProfile:
    return StyleProfile(
        name="Hangzhou_SG6_Common",
        description="test",
        path_scopes=[],
        preferred_keywords={},
        negative_patterns=[],
        style_rules=[],
        required_fields=[],
        confirmed_case_scopes=[
            "testsuite/Hangzhou/RRM/RAN_PZ_HAZ_34/None_Feature_SG6",
        ],
        allowed_resource_scopes=[
            "testsuite/Hangzhou/resources/RAN_PZ_HAZ_34/robot",
            "testsuite/Hangzhou/resources/RAN_PZ_HAZ_34/python",
        ],
        feature_allowlist={"RRM": ["CB010767"], "SISO": ["CB009464"]},
    )


def test_allowlisted_feature_path_is_allowed() -> None:
    decision = classify_path(
        "testsuite/Hangzhou/RRM/RAN_PZ_HAZ_34/CB010767/case.robot",
        _profile(),
        "testcase",
    )

    assert decision.is_allowed is True
    assert decision.allowed_source == "feature_allowlist"
    assert decision.domain == "RRM"
    assert decision.case_type == "Feature"
    assert decision.feature == "CB010767"


def test_allowed_resource_scope_is_common() -> None:
    decision = classify_path(
        "testsuite/Hangzhou/resources/RAN_PZ_HAZ_34/robot/Common.resource",
        _profile(),
        "keyword",
    )

    assert decision.is_allowed is True
    assert decision.allowed_source == "allowed_resource_scope"
    assert decision.domain == "Common"
    assert decision.case_type == "Resource"


def test_testcase_under_allowed_resource_scope_is_excluded() -> None:
    decision = classify_path(
        "testsuite/Hangzhou/resources/RAN_PZ_HAZ_34/robot/Common.robot",
        _profile(),
        "testcase",
    )

    assert decision.is_allowed is False
    assert decision.allowed_source == ""
    assert decision.domain == "Common"
    assert decision.case_type == "Resource"
    assert decision.exclude_reason == "testcase under allowed resource scope is not a generation testcase"


def test_unlisted_feature_path_is_excluded() -> None:
    decision = classify_path(
        "testsuite/Hangzhou/RRM/RAN_PZ_HAZ_34/CB999999/case.robot",
        _profile(),
        "testcase",
    )

    assert decision.is_allowed is False
    assert decision.domain == "RRM"
    assert decision.exclude_reason == "feature is not in active feature_allowlist"
