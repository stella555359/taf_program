from __future__ import annotations

from pathlib import Path

from robotws_mcp.layer2.models import GraphNode
from robotws_mcp.layer2.sqlite_store import Layer2SQLiteStore
from robotws_mcp.layer6.service import ValidationEngineService


def _build_layer2(tmp_path: Path) -> Path:
    db_path = tmp_path / "layer2.sqlite3"
    store = Layer2SQLiteStore(db_path)
    store.initialize()
    store.clear()
    store.insert_nodes(
        [
            GraphNode(
                node_id="keyword:rrm",
                node_type="keyword",
                record_id="keyword:rrm",
                name="9198_Case_Setup",
                path="testsuite/Hangzhou/RRM/RAN_PZ_HAZ_34/CB009198/Resources/CB009198_common_keywords.robot",
                domain="RRM",
                feature="CB009198",
                is_allowed=True,
            ),
            GraphNode(
                node_id="keyword:siso",
                node_type="keyword",
                record_id="keyword:siso",
                name="9331 Coam Test Setup",
                path="testsuite/Hangzhou/SISO/RAN_PZ_HAZ_34/5GC002510/Resources/keywords.robot",
                domain="SISO",
                feature="5GC002510",
                is_allowed=True,
            ),
        ]
    )
    return db_path


def test_validate_generated_robot_allows_direct_taf_with_cleanup(tmp_path: Path) -> None:
    service = ValidationEngineService(layer2_db_path=_build_layer2(tmp_path))
    robot_text = """BASIC_L3_Call
    [Documentation]    demo
    [Tags]    T813
    [Setup]    9198_Case_Setup
    [Teardown]    Detach Ue    ue_alias=UE_1
    Attach Ue    ue_alias=UE_1
    Start Data Transfer    DL_TRAFFIC    UE_1    DL    throughput=1800Mbits/sec
    Verify Average Throughput    DL_TRAFFIC    tput_min=1800Mbits/sec
    Stop Data Transfer    DL_TRAFFIC
    Detach Ue    ue_alias=UE_1
"""

    report = service.validate_generated_robot(robot_text, profile="Hangzhou_RRM_SG6_Feature", requirement="L3 traffic")

    assert report["decision"] == "allow"
    assert report["errors"] == []


def test_validate_generated_robot_denies_cross_domain_setup(tmp_path: Path) -> None:
    service = ValidationEngineService(layer2_db_path=_build_layer2(tmp_path))
    robot_text = """BASIC_L3_Call
    [Documentation]    demo
    [Tags]    T813
    [Setup]    9331 Coam Test Setup
    [Teardown]    Detach Ue    ue_alias=UE_1
    Attach Ue    ue_alias=UE_1
    Stop Data Transfer    DL_TRAFFIC
    Detach Ue    ue_alias=UE_1
"""

    report = service.validate_generated_robot(robot_text, profile="Hangzhou_RRM_SG6_Feature", requirement="L3 traffic")

    assert report["decision"] == "deny"
    assert any("domain mismatch" in error for error in report["errors"])


def test_validate_generated_robot_warns_when_cleanup_missing(tmp_path: Path) -> None:
    service = ValidationEngineService(layer2_db_path=_build_layer2(tmp_path))
    robot_text = """BASIC_L3_Call
    [Documentation]    demo
    [Tags]    T813
    [Setup]    9198_Case_Setup
    [Teardown]    9198_Case_Setup
    Attach Ue    ue_alias=UE_1
    Start Data Transfer    DL_TRAFFIC    UE_1    DL    throughput=1800Mbits/sec
"""

    report = service.validate_generated_robot(robot_text, profile="Hangzhou_RRM_SG6_Feature", requirement="L3 traffic")

    assert report["decision"] == "warn"
    assert any("stop traffic" in warning.lower() for warning in report["warnings"])

