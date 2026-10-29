from __future__ import annotations

from pathlib import Path

from robotws_mcp.layer1.records import CallArgument, StepRecord, stable_record_id
from robotws_mcp.layer1.sqlite_store import Layer1SQLiteStore


def test_layer1_sqlite_store_round_trips_records(tmp_path: Path) -> None:
    db_path = tmp_path / "layer1.sqlite3"
    store = Layer1SQLiteStore(db_path)
    store.initialize()
    store.clear()

    record = StepRecord(
        record_type="step",
        id=stable_record_id("step", "case.robot", "Case:1:Do Something", 10),
        owner_type="testcase",
        owner_name="Case",
        owner_id="testcase:1",
        path="case.robot",
        normalized_type="step",
        keyword="Do Something",
        arguments=[CallArgument(kind="named", name="mode", value="fast")],
        domain="RRM",
        is_allowed=True,
        allowed_source="feature_allowlist",
        line_no=10,
        raw="    Do Something    mode=fast",
    )

    store.insert_records([record])

    assert store.stats() == {"step": 1}
    rows = store.search(record_type="step", domain="RRM", is_allowed=True, query="Do Something")
    assert rows[0]["keyword"] == "Do Something"
    assert rows[0]["arguments"][0]["name"] == "mode"
    assert rows[0]["arguments"][0]["value"] == "fast"
