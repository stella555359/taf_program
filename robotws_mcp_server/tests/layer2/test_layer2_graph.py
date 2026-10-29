from __future__ import annotations

from pathlib import Path

from robotws_mcp.layer1.records import KeywordRecord, ResourceImportRecord, StepRecord, TestCaseRecord as Layer1TestCaseRecord
from robotws_mcp.layer1.sqlite_store import Layer1SQLiteStore
from robotws_mcp.layer2.build_graph import build_layer2_graph
from robotws_mcp.layer2.input_loader import Layer1InputLoader
from robotws_mcp.layer2.query import Layer2QueryService
from robotws_mcp.layer2.resolver import KeywordResolver


CASE_PATH = "testsuite/Hangzhou/SISO/RAN_PZ_HAZ_34/CB009275_AEHC/CB009275_case.robot"
FEATURE_RESOURCE = "testsuite/Hangzhou/SISO/RAN_PZ_HAZ_34/CB009275_AEHC/Resources/CB009275_common.robot"
SG6_RESOURCES = "testsuite/Hangzhou/resources/RAN_PZ_HAZ_34/lines/SG6/Resources.robot"
COAM_RESOURCE = "testsuite/Hangzhou/resources/RAN_PZ_HAZ_34/robot/coam_siso_common.robot"


def _build_layer1_fixture(tmp_path: Path) -> Path:
    db_path = tmp_path / "layer1.sqlite3"
    store = Layer1SQLiteStore(db_path)
    store.initialize()
    store.clear()
    records = [
        Layer1TestCaseRecord(
            record_type="testcase",
            id="testcase:cb009275",
            name="[1]02_CB009275_Feature_Enable_with_Fault_1932_actived",
            path=CASE_PATH,
            domain="SISO",
            feature="CB009275_AEHC",
            is_allowed=True,
            allowed_source="feature_allowlist",
            body_step_ids=["step:case:feature"],
        ),
        StepRecord(
            record_type="step",
            id="step:case:feature",
            owner_type="testcase",
            owner_name="[1]02_CB009275_Feature_Enable_with_Fault_1932_actived",
            owner_id="testcase:cb009275",
            path=CASE_PATH,
            normalized_type="step",
            ordinal=1,
            keyword="02_CB009275_Feature_Enable_with_Fault_1932_actived",
            domain="SISO",
            feature="CB009275_AEHC",
            is_allowed=True,
            allowed_source="feature_allowlist",
        ),
        ResourceImportRecord(
            record_type="resource_import",
            id="resource_import:case:feature",
            source_path=CASE_PATH,
            resource_path="Resources/CB009275_common.robot",
            resolved_path=FEATURE_RESOURCE,
            domain="SISO",
            feature="CB009275_AEHC",
            is_allowed=True,
            allowed_source="feature_allowlist",
        ),
        KeywordRecord(
            record_type="keyword",
            id="keyword:feature",
            name="02_CB009275_Feature_Enable_with_Fault_1932_actived",
            path=FEATURE_RESOURCE,
            domain="SISO",
            feature="CB009275_AEHC",
            is_allowed=True,
            allowed_source="feature_allowlist",
            step_ids=["step:feature:connect", "step:feature:common_unit", "step:feature:csn"],
        ),
        StepRecord(
            record_type="step",
            id="step:feature:connect",
            owner_type="keyword",
            owner_name="02_CB009275_Feature_Enable_with_Fault_1932_actived",
            owner_id="keyword:feature",
            path=FEATURE_RESOURCE,
            normalized_type="keyword_step",
            ordinal=1,
            keyword="Connect to RU With Allocated IP",
            domain="SISO",
            feature="CB009275_AEHC",
            is_allowed=True,
            allowed_source="feature_allowlist",
        ),
        StepRecord(
            record_type="step",
            id="step:feature:common_unit",
            owner_type="keyword",
            owner_name="02_CB009275_Feature_Enable_with_Fault_1932_actived",
            owner_id="keyword:feature",
            path=FEATURE_RESOURCE,
            normalized_type="keyword_step",
            ordinal=2,
            keyword="Connect to Common Unit Master",
            domain="SISO",
            feature="CB009275_AEHC",
            is_allowed=True,
            allowed_source="feature_allowlist",
        ),
        StepRecord(
            record_type="step",
            id="step:feature:csn",
            owner_type="keyword",
            owner_name="02_CB009275_Feature_Enable_with_Fault_1932_actived",
            owner_id="keyword:feature",
            path=FEATURE_RESOURCE,
            normalized_type="keyword_step",
            ordinal=3,
            keyword="csn.execute",
            domain="SISO",
            feature="CB009275_AEHC",
            is_allowed=True,
            allowed_source="feature_allowlist",
        ),
        ResourceImportRecord(
            record_type="resource_import",
            id="resource_import:feature:sg6",
            source_path=FEATURE_RESOURCE,
            resource_path=SG6_RESOURCES,
            resolved_path=SG6_RESOURCES,
            domain="SISO",
            feature="CB009275_AEHC",
            is_allowed=True,
            allowed_source="feature_allowlist",
        ),
        ResourceImportRecord(
            record_type="resource_import",
            id="resource_import:sg6:coam",
            source_path=SG6_RESOURCES,
            resource_path=COAM_RESOURCE,
            resolved_path=COAM_RESOURCE,
            domain="Common",
            is_allowed=True,
            allowed_source="allowed_resource_scope",
        ),
        KeywordRecord(
            record_type="keyword",
            id="keyword:connect_ru",
            name="Connect to RU With Allocated IP",
            path=COAM_RESOURCE,
            domain="Common",
            is_allowed=True,
            allowed_source="allowed_resource_scope",
            step_ids=["step:connect:csn"],
        ),
        KeywordRecord(
            record_type="keyword",
            id="keyword:excluded",
            name="Excluded Feature Helper",
            path="testsuite/Hangzhou/SISO/RAN_PZ_HAZ_34/CB000000/Resources/helper.robot",
            domain="SISO",
            feature="CB000000",
            is_allowed=False,
            exclude_reason="feature is not in active feature_allowlist",
        ),
        StepRecord(
            record_type="step",
            id="step:connect:csn",
            owner_type="keyword",
            owner_name="Connect to RU With Allocated IP",
            owner_id="keyword:connect_ru",
            path=COAM_RESOURCE,
            normalized_type="keyword_step",
            ordinal=1,
            keyword="csn.execute",
            domain="Common",
            is_allowed=True,
            allowed_source="allowed_resource_scope",
        ),
    ]
    store.insert_records(records)
    return db_path


def test_keyword_resolver_uses_resource_closure_and_taf_fallback(tmp_path: Path) -> None:
    layer1_db = _build_layer1_fixture(tmp_path)
    graph_input = Layer1InputLoader(layer1_db).load()

    results = {result.step_id: result for result in KeywordResolver(graph_input).resolve_all()}

    assert results["step:feature:connect"].resolution_status == "resolved"
    assert results["step:feature:connect"].called_target_record_id == "keyword:connect_ru"
    assert "resource import closure" in results["step:feature:connect"].reason
    assert results["step:feature:common_unit"].resolution_status == "taf_library_keyword"
    assert "plain device/TAF-like call" in results["step:feature:common_unit"].reason
    assert results["step:feature:csn"].resolution_status == "taf_library_keyword"
    assert results["step:feature:csn"].library_kind == "taf"


def test_keyword_resolver_classifies_robot_standard_library_keyword(tmp_path: Path) -> None:
    layer1_db = _build_layer1_fixture(tmp_path)
    graph_input = Layer1InputLoader(layer1_db).load()
    step = {
        "id": "step:std:join_path",
        "owner_id": "keyword:feature",
        "keyword": "Join Path",
        "path": FEATURE_RESOURCE,
        "domain": "SISO",
        "feature": "CB009275_AEHC",
    }

    result = KeywordResolver(graph_input).resolve_step(step)

    assert result.resolution_status == "builtin"
    assert result.called_target_node_id == "builtin:joinpath"


def test_keyword_resolver_classifies_excluded_candidates(tmp_path: Path) -> None:
    layer1_db = _build_layer1_fixture(tmp_path)
    graph_input = Layer1InputLoader(layer1_db).load()
    step = {
        "id": "step:excluded",
        "owner_id": "keyword:feature",
        "keyword": "Excluded Feature Helper",
        "path": FEATURE_RESOURCE,
        "domain": "SISO",
        "feature": "CB009275_AEHC",
    }

    result = KeywordResolver(graph_input).resolve_step(step)

    assert result.resolution_status == "excluded"
    assert result.candidates[0]["record_id"] == "keyword:excluded"


def test_layer2_builds_queryable_graph_and_taf_summary(tmp_path: Path) -> None:
    layer1_db = _build_layer1_fixture(tmp_path)
    layer2_db = tmp_path / "layer2.sqlite3"

    summary = build_layer2_graph(layer1_db=layer1_db, db_path=layer2_db)

    assert summary["resolution_status_counts"]["resolved"] == 2
    assert summary["resolution_status_counts"]["taf_library_keyword"] == 3
    assert summary["dependency_summary_counts"]["taf_dependent"] == 3

    query = Layer2QueryService(layer2_db)
    graph = query.get_testcase_graph("[1]02_CB009275_Feature_Enable_with_Fault_1932_actived", depth=3)
    feature_step = graph["body"][0]
    assert feature_step["resolution_status"] == "resolved"
    assert feature_step["children"][0]["step"] == "Connect to RU With Allocated IP"
    assert feature_step["children"][1]["step"] == "Connect to Common Unit Master"
    assert feature_step["children"][1]["resolution_status"] == "taf_library_keyword"
    assert feature_step["children"][2]["resolution_status"] == "taf_library_keyword"

    dependency = query.explain_taf_dependency("keyword:feature")
    assert dependency["impl_type"] == "taf_dependent"
    assert any("csn.execute" in " -> ".join(path) for path in dependency["evidence_paths"])

    callers = query.find_keyword_callers("Connect to RU With Allocated IP")
    assert callers["callers"][0]["owner_id"] == "keyword:feature"

