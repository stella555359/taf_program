from __future__ import annotations

from pathlib import Path

from robotws_mcp.layer2.models import GraphNode
from robotws_mcp.layer2.sqlite_store import Layer2SQLiteStore
from robotws_mcp.layer5.service import TemplateExtractionService
from robotws_mcp.storage.sqlite_store import SQLiteStore


def _build_indexes(tmp_path: Path) -> tuple[Path, Path]:
    db_path = tmp_path / "robotws.sqlite3"
    store = SQLiteStore(db_path)
    store.initialize()
    store.clear()
    layer2_path = tmp_path / "layer2.sqlite3"
    layer2 = Layer2SQLiteStore(layer2_path)
    layer2.initialize()
    layer2.clear()
    layer2.insert_nodes(
        [
            GraphNode(
                node_id="keyword:attach",
                node_type="keyword",
                record_id="keyword:attach",
                name="Make_L3_Call_With_MTK_UE",
                path="testsuite/Hangzhou/RRM/RAN_PZ_HAZ_34/CB008247/Resources/CB008247_keywords.robot",
                domain="RRM",
                feature="CB008247",
                is_allowed=True,
                impl_type="taf_dependent",
            ),
            GraphNode(
                node_id="keyword:tput",
                node_type="keyword",
                record_id="keyword:tput",
                name="Check L3 Call Tput",
                path="testsuite/Hangzhou/resources/RAN_PZ_HAZ_34/lines/SG6/L3call.robot",
                domain="Common",
                is_allowed=True,
                impl_type="taf_dependent",
            ),
        ]
    )
    return db_path, layer2_path


def test_l3_call_template_contains_required_cleanup_steps(tmp_path: Path) -> None:
    db_path, layer2_path = _build_indexes(tmp_path)
    service = TemplateExtractionService(db_path=db_path, layer2_db_path=layer2_path)

    template = service.extract_template_from_requirement(
        "RRM MTK basic L3 call attach dl ul traffic check tput detach",
        profile="Hangzhou_RRM_SG6_Feature",
        domain="RRM",
    )

    roles = [step["role"] for step in template["required_steps"]]
    assert roles == [
        "setup",
        "attach",
        "start_dl_traffic",
        "start_ul_traffic",
        "check_tput",
        "stop_traffic",
        "detach",
        "teardown",
    ]
    assert "traffic before attach" in template["forbidden_order"]
    assert any(step["recommended_keywords"] for step in template["required_steps"])

