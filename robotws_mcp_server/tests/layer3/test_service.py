from __future__ import annotations

from pathlib import Path

from robotws_mcp.layer2.models import GraphNode
from robotws_mcp.layer2.sqlite_store import Layer2SQLiteStore
from robotws_mcp.layer3.service import GovernanceService


def _build_layer2_index(tmp_path: Path) -> Path:
    db_path = tmp_path / "layer2.sqlite3"
    store = Layer2SQLiteStore(db_path)
    store.initialize()
    store.clear()
    store.insert_nodes(
        [
            GraphNode(
                node_id="keyword:allowed",
                node_type="keyword",
                record_id="kw-allowed",
                name="Allowed SG6 Keyword",
                path="testsuite/Hangzhou/resources/RAN_PZ_HAZ_34/lines/SG6/Common.robot",
                domain="Common",
                is_allowed=True,
            ),
            GraphNode(
                node_id="keyword:excluded",
                node_type="keyword",
                record_id="kw-excluded",
                name="Excluded SG1 Keyword",
                path="testsuite/Hangzhou/resources/RAN_PZ_HAZ_34/lines/SG1/Common.robot",
                domain="Common",
                is_allowed=False,
            ),
        ]
    )
    return db_path


def test_filter_generation_context_allows_only_boundary_safe_candidates(tmp_path: Path) -> None:
    service = GovernanceService(layer2_db_path=_build_layer2_index(tmp_path))

    result = service.filter_generation_context(
        ["keyword:allowed", "keyword:excluded", "keyword:missing"],
        profile="Hangzhou_SG6_Common",
    )

    assert [item["candidate"]["node_id"] for item in result["allowed"]] == ["keyword:allowed"]
    assert [item["rule_id"] for item in result["denied"]] == [
        "boundary.excluded",
        "context.candidate_not_found",
    ]


def test_explain_allowed_boundary_accepts_layer2_record_id(tmp_path: Path) -> None:
    service = GovernanceService(layer2_db_path=_build_layer2_index(tmp_path))

    decision = service.explain_allowed_boundary("kw-allowed", profile="Hangzhou_SG6_Common")

    assert decision["decision"] == "allow"
    assert decision["evidence"]["candidate"]["node_id"] == "keyword:allowed"

