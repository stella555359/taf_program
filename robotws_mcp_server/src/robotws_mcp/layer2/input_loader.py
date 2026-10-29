"""Load Layer 1 records for Layer 2 graph construction."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from robotws_mcp.models import normalize_path


@dataclass
class Layer1GraphInput:
    records: list[dict[str, Any]]
    excluded_records: list[dict[str, Any]] = field(default_factory=list)
    by_id: dict[str, dict[str, Any]] = field(default_factory=dict)
    by_type: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    steps_by_owner: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    resource_imports_by_source: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    library_imports_by_source: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    keywords_by_path: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    python_symbols_by_path: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    excluded_keywords_by_name: dict[str, list[dict[str, Any]]] = field(default_factory=dict)

    @classmethod
    def from_records(cls, records: list[dict[str, Any]], excluded_records: list[dict[str, Any]] | None = None) -> "Layer1GraphInput":
        data = cls(records=records, excluded_records=excluded_records or [])
        for record in records:
            record_id = str(record.get("id", ""))
            record_type = str(record.get("record_type", ""))
            if record_id:
                data.by_id[record_id] = record
            data.by_type.setdefault(record_type, []).append(record)
            if record_type == "step":
                data.steps_by_owner.setdefault(str(record.get("owner_id", "")), []).append(record)
            elif record_type == "resource_import":
                data.resource_imports_by_source.setdefault(_source_path(record), []).append(record)
            elif record_type == "library_import":
                data.library_imports_by_source.setdefault(_source_path(record), []).append(record)
            elif record_type == "keyword":
                data.keywords_by_path.setdefault(_record_path(record), []).append(record)
            elif record_type == "python_symbol":
                data.python_symbols_by_path.setdefault(_record_path(record), []).append(record)
        for record in data.excluded_records:
            if record.get("record_type") == "keyword" and record.get("name"):
                data.excluded_keywords_by_name.setdefault(str(record.get("name", "")), []).append(record)
        for steps in data.steps_by_owner.values():
            steps.sort(key=lambda item: int(item.get("ordinal", 0) or 0))
        return data


class Layer1InputLoader:
    """Read Layer 1 SQLite payloads into graph-friendly indexes."""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)

    def load(self, include_excluded: bool = False) -> Layer1GraphInput:
        if not self.db_path.exists():
            raise FileNotFoundError(f"Layer 1 SQLite not found: {self.db_path}")
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            rows = conn.execute("SELECT data FROM layer1_records ORDER BY path, line_no").fetchall()
        finally:
            conn.close()
        all_records = [json.loads(row["data"]) for row in rows]
        excluded_records = [record for record in all_records if not record.get("is_allowed")]
        records = all_records
        if not include_excluded:
            records = [record for record in records if record.get("is_allowed")]
        return Layer1GraphInput.from_records(records, excluded_records=excluded_records)


def _source_path(record: dict[str, Any]) -> str:
    return normalize_path(str(record.get("source_path") or record.get("path") or ""))


def _record_path(record: dict[str, Any]) -> str:
    return normalize_path(str(record.get("path") or record.get("source_path") or record.get("resolved_path") or ""))

