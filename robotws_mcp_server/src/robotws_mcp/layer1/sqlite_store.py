"""SQLite persistence for Layer 1 v2 records."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from robotws_mcp.layer1.records import Layer1Record


class Layer1SQLiteStore:
    """Persist Layer 1 records into an isolated v2 SQLite schema."""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize(self) -> None:
        with self.connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS layer1_records (
                    id TEXT PRIMARY KEY,
                    record_type TEXT NOT NULL,
                    path TEXT NOT NULL,
                    name TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    is_allowed INTEGER NOT NULL,
                    allowed_source TEXT NOT NULL,
                    exclude_reason TEXT NOT NULL,
                    line_no INTEGER NOT NULL,
                    data TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_layer1_type ON layer1_records(record_type);
                CREATE INDEX IF NOT EXISTS idx_layer1_path ON layer1_records(path);
                CREATE INDEX IF NOT EXISTS idx_layer1_name ON layer1_records(name);
                CREATE INDEX IF NOT EXISTS idx_layer1_domain_allowed ON layer1_records(domain, is_allowed);
                """
            )

    def clear(self) -> None:
        with self.connect() as conn:
            conn.execute("DELETE FROM layer1_records")

    def insert_records(self, records: list[Layer1Record]) -> None:
        with self.connect() as conn:
            for record in records:
                data = record.to_dict()
                conn.execute(
                    """
                    INSERT OR REPLACE INTO layer1_records(
                        id, record_type, path, name, domain, is_allowed,
                        allowed_source, exclude_reason, line_no, data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        data.get("id", ""),
                        data.get("record_type", ""),
                        _path(data),
                        _name(data),
                        data.get("domain", "Unknown"),
                        1 if data.get("is_allowed") else 0,
                        data.get("allowed_source", ""),
                        data.get("exclude_reason", ""),
                        int(data.get("line_no", 1) or 1),
                        json.dumps(data, ensure_ascii=False),
                    ),
                )

    def stats(self) -> dict[str, int]:
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT record_type, COUNT(*) AS count FROM layer1_records GROUP BY record_type ORDER BY record_type"
            ).fetchall()
        return {row["record_type"]: row["count"] for row in rows}

    def search(
        self,
        record_type: str = "",
        domain: str = "",
        is_allowed: bool | None = None,
        query: str = "",
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        sql = "SELECT data FROM layer1_records"
        where: list[str] = []
        params: list[Any] = []
        if record_type:
            where.append("record_type = ?")
            params.append(record_type)
        if domain:
            where.append("domain = ?")
            params.append(domain)
        if is_allowed is not None:
            where.append("is_allowed = ?")
            params.append(1 if is_allowed else 0)
        if query:
            where.append("(name LIKE ? OR path LIKE ?)")
            params.extend([f"%{query}%", f"%{query}%"])
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY path, line_no LIMIT ?"
        params.append(limit)
        with self.connect() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [json.loads(row["data"]) for row in rows]


def _path(data: dict[str, Any]) -> str:
    return str(data.get("path") or data.get("source_path") or "")


def _name(data: dict[str, Any]) -> str:
    return str(data.get("name") or data.get("keyword") or data.get("resource_path") or data.get("library") or "")
