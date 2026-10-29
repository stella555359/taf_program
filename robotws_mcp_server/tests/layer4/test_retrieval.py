from __future__ import annotations

from pathlib import Path

from robotws_mcp.layer2.models import DependencySummary, GraphNode
from robotws_mcp.layer2.sqlite_store import Layer2SQLiteStore
from robotws_mcp.layer4.service import SemanticRetrievalService
from robotws_mcp.models import RobotCase, RobotFile, RobotKeyword, RobotStep
from robotws_mcp.storage.sqlite_store import SQLiteStore


def _build_indexes(tmp_path: Path) -> tuple[Path, Path]:
    db_path = tmp_path / "robotws.sqlite3"
    store = SQLiteStore(db_path)
    store.initialize()
    store.clear()
    store.insert_robot_file(
        RobotFile(
            path="testsuite/Hangzhou/RRM/RAN_PZ_HAZ_34/CB009198/CB009198_cases.robot",
            cases=[
                RobotCase(
                    name="RRM MTK basic L3 call",
                    path="testsuite/Hangzhou/RRM/RAN_PZ_HAZ_34/CB009198/CB009198_cases.robot",
                    line_no=10,
                    documentation=["MTK UE attach and L3 call traffic."],
                    tags=["T813"],
                    setup="9198_Case_Setup",
                    teardown="9198_Case_Teardown",
                    steps=[RobotStep(keyword="Make_L3_Call_With_MTK_UE", raw="Make_L3_Call_With_MTK_UE", line_no=20)],
                )
            ],
            keywords=[
                RobotKeyword(
                    name="Make_L3_Call_With_MTK_UE",
                    path="testsuite/Hangzhou/RRM/RAN_PZ_HAZ_34/CB008247/Resources/CB008247_keywords.robot",
                    line_no=5,
                    documentation=["Attach MTK UE and start L3 traffic."],
                    steps=[RobotStep(keyword="Start Traffic For MTK UE", raw="Start Traffic For MTK UE", line_no=8)],
                )
            ],
        )
    )

    layer2_path = tmp_path / "layer2.sqlite3"
    layer2 = Layer2SQLiteStore(layer2_path)
    layer2.initialize()
    layer2.clear()
    layer2.insert_nodes(
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
    layer2.insert_dependency_summaries(
        [
            DependencySummary(
                record_id="keyword:mtk",
                node_id="keyword:mtk",
                node_type="keyword",
                impl_type="taf_dependent",
                has_taf_dependency=True,
            )
        ]
    )
    return db_path, layer2_path


def test_search_evidence_returns_explainable_ranked_results(tmp_path: Path) -> None:
    db_path, layer2_path = _build_indexes(tmp_path)
    service = SemanticRetrievalService(db_path=db_path, layer2_db_path=layer2_path)

    result = service.search_evidence("MTK L3 call traffic", profile="Hangzhou_SG6_Common", limit=5)

    assert result["vector_status"] == "disabled:no_embedding_provider"
    names = [item["name"] for item in result["evidence"]]
    assert "Make_L3_Call_With_MTK_UE" in names
    assert any(item["match_reasons"] for item in result["evidence"])


def test_rank_keyword_candidates_filters_by_domain(tmp_path: Path) -> None:
    db_path, layer2_path = _build_indexes(tmp_path)
    service = SemanticRetrievalService(db_path=db_path, layer2_db_path=layer2_path)

    result = service.rank_keyword_candidates("MTK L3", domain="RRM", limit=5)

    assert result["evidence"][0]["name"] == "Make_L3_Call_With_MTK_UE"
    assert result["evidence"][0]["taf_dependency"]["has_taf_dependency"] is True

