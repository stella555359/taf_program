from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from robotws_mcp.api import create_api_app
from robotws_mcp.layer2.models import GraphNode
from robotws_mcp.layer2.sqlite_store import Layer2SQLiteStore
from robotws_mcp.models import RobotCase, RobotFile, RobotKeyword, RobotStep
from robotws_mcp.storage.sqlite_store import SQLiteStore


def _build_test_index(tmp_path: Path) -> Path:
    db_path = tmp_path / "robotws.sqlite3"
    store = SQLiteStore(db_path)
    store.initialize()
    store.clear()
    robot_file = RobotFile(
        path="testsuite/Hangzhou/RRM/RAN_PZ_HAZ_34/CB009363/CB009363_cases.robot",
        cases=[
            RobotCase(
                name="CB009363 handover KPI case",
                path="testsuite/Hangzhou/RRM/RAN_PZ_HAZ_34/CB009363/CB009363_cases.robot",
                line_no=10,
                documentation=["Handover KPI validation."],
                tags=["CRT"],
                setup="SG6 Setup",
                teardown="SG6 Teardown",
                steps=[
                    RobotStep(
                        keyword="Compass.KPI Generate And Upload To Remote Server",
                        raw="Compass.KPI Generate And Upload To Remote Server",
                        line_no=20,
                    )
                ],
            )
        ],
        keywords=[
            RobotKeyword(
                name="Compass.KPI Generate And Upload To Remote Server",
                path="testsuite/Hangzhou/resources/RAN_PZ_HAZ_34/lines/SG6/KPI.robot",
                line_no=5,
                documentation=["Generate KPI report."],
            )
        ],
    )
    store.insert_robot_file(robot_file)
    report = {
        "summary": {"confirmed_by_allowlist": 1},
        "features": [
            {
                "area": "RRM",
                "feature": "CB009363",
                "path": "testsuite/Hangzhou/RRM/RAN_PZ_HAZ_34/CB009363",
                "status": "confirmed",
                "source": "allowlist",
                "case_count": 1,
                "resource_imports": [],
                "exclude_reason": "",
            }
        ],
    }
    db_path.with_name("sg6_discovery_report.json").write_text(json.dumps(report), encoding="utf-8")
    return db_path


def _build_layer2_index(tmp_path: Path) -> Path:
    db_path = tmp_path / "layer2.sqlite3"
    store = Layer2SQLiteStore(db_path)
    store.initialize()
    store.clear()
    store.insert_nodes(
        [
            GraphNode(
                node_id="keyword:mtk",
                node_type="keyword",
                record_id="keyword:mtk",
                name="Make_L3_Call_With_MTK_UE",
                path="testsuite/Hangzhou/RRM/RAN_PZ_HAZ_34/CB008247/Resources/CB008247_keywords.robot",
                domain="RRM",
                feature="CB008247",
                is_allowed=True,
                impl_type="taf_dependent",
            )
        ]
    )
    return db_path


def test_health_and_version(tmp_path: Path) -> None:
    db_path = _build_test_index(tmp_path)
    client = TestClient(create_api_app(db_path=db_path, layer7_db_path=tmp_path / "feedback.sqlite3"))

    assert client.get("/health").json() == {"status": "ok"}
    version = client.get("/version").json()
    assert version["name"] == "robotws-knowledge-api"
    assert version["db_path"] == str(db_path)


def test_discovery_and_generation_context(tmp_path: Path) -> None:
    db_path = _build_test_index(tmp_path)
    client = TestClient(create_api_app(db_path=db_path, layer7_db_path=tmp_path / "feedback.sqlite3"))

    discovery = client.get("/discovery/sg6").json()
    assert discovery["summary"]["confirmed_by_allowlist"] == 1

    response = client.post(
        "/query/generation-context",
        json={
            "requirement": "RRM SG6 handover KPI testcase",
            "profile": "Hangzhou_RRM_SG6_Feature",
            "limit": 3,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "context_only"
    assert body["similar_cases"][0]["name"] == "CB009363 handover KPI case"
    assert body["sg6_ownership"]["confirmed_features"][0]["feature"] == "CB009363"
    assert body["setup_teardown_pattern"]["setup"] == ["TODO_SELECT_FEATURE_LOCAL_SETUP"]
    assert body["setup_teardown_pattern"]["teardown"] == ["TODO_SELECT_FEATURE_LOCAL_TEARDOWN"]
    assert body["setup_teardown_pattern"]["reference_cases"] == [
        {
            "name": "CB009363 handover KPI case",
            "path": "testsuite/Hangzhou/RRM/RAN_PZ_HAZ_34/CB009363/CB009363_cases.robot",
            "setup": "SG6 Setup",
            "teardown": "SG6 Teardown",
        }
    ]
    assert "    [Setup]    TODO_SELECT_FEATURE_LOCAL_SETUP" in body["generation_skeleton"]
    assert "    [Teardown]    TODO_SELECT_FEATURE_LOCAL_TEARDOWN" in body["generation_skeleton"]
    assert "SG6 Setup" not in body["generation_skeleton"]
    assert "SetUp.TMO Case Common SetUp" not in body["generation_skeleton"]

    tmo_response = client.post(
        "/query/generation-context",
        json={
            "requirement": "RRM SG6 TMO KPI testcase",
            "profile": "Hangzhou_RRM_SG6_TMO",
            "limit": 3,
        },
    )
    tmo_body = tmo_response.json()
    assert tmo_body["setup_teardown_pattern"]["setup"] == ["SetUp.TMO Case Common SetUp"]
    assert tmo_body["setup_teardown_pattern"]["teardown"] == ["TMO_Common_Case_Teardown"]


def test_search_and_validate_endpoints(tmp_path: Path) -> None:
    db_path = _build_test_index(tmp_path)
    client = TestClient(create_api_app(db_path=db_path, layer7_db_path=tmp_path / "feedback.sqlite3"))

    cases = client.post(
        "/query/search-cases",
        json={"query": "handover KPI", "profile": "Hangzhou_RRM_SG6_Feature", "limit": 5},
    ).json()
    assert cases["cases"][0]["name"] == "CB009363 handover KPI case"

    keywords = client.post(
        "/query/search-keywords",
        json={"query": "KPI", "profile": "Hangzhou_RRM_SG6_Feature", "limit": 5},
    ).json()
    assert keywords["keywords"][0]["name"] == "Compass.KPI Generate And Upload To Remote Server"

    validation = client.post(
        "/query/validate-style",
        json={
            "profile": "Hangzhou_RRM_SG6_Feature",
            "robot_text": (
                "Case\n"
                "    [Documentation]    demo\n"
                "    [Tags]    T001\n"
                "    [Setup]    SG6 Setup\n"
                "    [Teardown]    SG6 Teardown"
            ),
        },
    ).json()
    assert validation["passed"] is True


def test_layer3_governance_endpoints(tmp_path: Path) -> None:
    db_path = _build_test_index(tmp_path)
    layer2_path = _build_layer2_index(tmp_path)
    client = TestClient(create_api_app(db_path=db_path, layer2_db_path=layer2_path, layer7_db_path=tmp_path / "feedback.sqlite3"))

    taf_decision = client.post(
        "/query/layer3/evaluate-taf-usage",
        json={
            "evidence": {
                "operation": "capture wireshark",
                "requested_call": "Capture Custom Wireshark For New Scenario",
                "sg6_evidence": [{"keyword": "Start Container Capture Wireshark Log"}],
                "taf_mcp_docs": [{"library": "taf.analyzer.pcap"}],
                "library_choice_matches_sg6": True,
                "parameter_pattern_matches_sg6": True,
                "setup_teardown_aligned": True,
                "cleanup_aligned": True,
            }
        },
    ).json()
    assert taf_decision["decision"] == "allow"
    assert taf_decision["rule_id"] == "taf_usage.grounded_direct_or_new_wrapper"

    boundary = client.post(
        "/query/layer3/explain-allowed-boundary",
        json={
            "record_id_or_path": "testsuite/Hangzhou/resources/RAN_PZ_HAZ_34/lines/SG6/Common.robot",
            "profile": "Hangzhou_SG6_Common",
        },
    ).json()
    assert boundary["decision"] == "allow"

    validation = client.post(
        "/query/layer3/validate-generated-robot",
        json={
            "profile": "Hangzhou_SG6_Common",
            "robot_text": (
                "Case\n"
                "    [Documentation]    demo\n"
                "    [Tags]    T001\n"
                "    [Setup]    SG6 Setup\n"
                "    [Teardown]    SG6 Teardown"
            ),
        },
    ).json()
    assert validation["decision"] == "allow"
    assert validation["rule_id"] == "generated_robot.style_passed"


def test_layer4_to_layer7_endpoints(tmp_path: Path) -> None:
    db_path = _build_test_index(tmp_path)
    layer2_path = _build_layer2_index(tmp_path)
    feedback_path = tmp_path / "feedback.sqlite3"
    client = TestClient(create_api_app(db_path=db_path, layer2_db_path=layer2_path, layer7_db_path=feedback_path))

    evidence = client.post(
        "/query/layer4/search-evidence",
        json={"query": "MTK L3 call", "profile": "Hangzhou_RRM_SG6_Feature", "limit": 5},
    ).json()
    assert evidence["vector_status"] == "disabled:no_embedding_provider"

    template = client.post(
        "/query/layer5/extract-template",
        json={
            "requirement": "RRM MTK L3 call attach traffic tput detach",
            "profile": "Hangzhou_RRM_SG6_Feature",
            "domain": "RRM",
        },
    ).json()
    assert template["operation"] == "l3_call"

    validation = client.post(
        "/query/layer6/validate-generated-robot",
        json={
            "profile": "Hangzhou_RRM_SG6_Feature",
            "requirement": "L3 traffic",
            "robot_text": (
                "BASIC_L3_Call\n"
                "    [Documentation]    demo\n"
                "    [Tags]    T813\n"
                "    [Setup]    Make_L3_Call_With_MTK_UE\n"
                "    [Teardown]    Detach Ue    ue_alias=UE_1\n"
                "    Attach Ue    ue_alias=UE_1\n"
                "    Stop Data Transfer    DL_TRAFFIC\n"
                "    Detach Ue    ue_alias=UE_1\n"
            ),
        },
    ).json()
    assert validation["decision"] == "allow"

    recorded = client.post(
        "/query/layer7/record-execution-feedback",
        json={
            "feedback": {
                "source_type": "manual",
                "test_name": "BASIC_L3_Call",
                "keyword_name": "Make_L3_Call_With_MTK_UE",
                "status": "FAIL",
                "message": "timeout",
                "profile": "Hangzhou_RRM_SG6_Feature",
            }
        },
    ).json()
    assert recorded["record"]["failure_class"] == "timeout"
    hints = client.post(
        "/query/layer7/feedback-hints",
        json={"record_id_or_name": "Make_L3_Call_With_MTK_UE", "profile": "Hangzhou_RRM_SG6_Feature"},
    ).json()
    assert hints["has_failures"] is True
