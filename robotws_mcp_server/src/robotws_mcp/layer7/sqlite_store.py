"""SQLite store for Layer 7 execution feedback."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from robotws_mcp.layer7.models import ExecutionFeedback


class FeedbackSQLiteStore:
    """Persist execution feedback and provide lightweight hints."""

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
                CREATE TABLE IF NOT EXISTS layer7_execution_feedback (
                    id TEXT PRIMARY KEY,
                    source_type TEXT NOT NULL,
                    source_path TEXT NOT NULL,
                    test_name TEXT NOT NULL,
                    keyword_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    failure_class TEXT NOT NULL,
                    message TEXT NOT NULL,
                    elapsed_ms INTEGER NOT NULL,
                    profile TEXT NOT NULL,
                    testline TEXT NOT NULL,
                    data TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS layer7_keyword_feedback_summary (
                    keyword_name TEXT PRIMARY KEY,
                    pass_count INTEGER NOT NULL,
                    fail_count INTEGER NOT NULL,
                    data TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_layer7_test_name ON layer7_execution_feedback(test_name);
                CREATE INDEX IF NOT EXISTS idx_layer7_keyword_name ON layer7_execution_feedback(keyword_name);
                CREATE INDEX IF NOT EXISTS idx_layer7_status ON layer7_execution_feedback(status);
                CREATE INDEX IF NOT EXISTS idx_layer7_profile ON layer7_execution_feedback(profile);
                """
            )

    def clear(self) -> None:
        with self.connect() as conn:
            conn.execute("DELETE FROM layer7_execution_feedback")
            conn.execute("DELETE FROM layer7_keyword_feedback_summary")

    def insert_feedback(self, records: list[ExecutionFeedback]) -> None:
        with self.connect() as conn:
            for record in records:
                data = record.to_dict()
                conn.execute(
                    """
                    INSERT OR REPLACE INTO layer7_execution_feedback(
                        id, source_type, source_path, test_name, keyword_name,
                        status, failure_class, message, elapsed_ms, profile, testline, data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        record.id,
                        record.source_type,
                        record.source_path,
                        record.test_name,
                        record.keyword_name,
                        record.status,
                        record.failure_class,
                        record.message,
                        record.elapsed_ms,
                        record.profile,
                        record.testline,
                        json.dumps(data, ensure_ascii=False),
                    ),
                )
            self._refresh_summary(conn)

    def search(self, query: str = "", profile: str = "", limit: int = 50) -> list[dict[str, Any]]:
        sql = "SELECT data FROM layer7_execution_feedback"
        where: list[str] = []
        params: list[Any] = []
        if query:
            where.append("(test_name LIKE ? OR keyword_name LIKE ? OR message LIKE ?)")
            params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])
        if profile:
            where.append("(profile = ? OR profile = '')")
            params.append(profile)
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY status, test_name, keyword_name LIMIT ?"
        params.append(limit)
        with self.connect() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [json.loads(row["data"]) for row in rows]

    def hints(self, record_id_or_name: str, profile: str = "") -> dict[str, Any]:
        rows = self.search(record_id_or_name, profile=profile, limit=100)
        failures = [row for row in rows if str(row.get("status", "")).lower() in {"fail", "failed"}]
        passes = [row for row in rows if str(row.get("status", "")).lower() in {"pass", "passed"}]
        return {
            "record_id_or_name": record_id_or_name,
            "has_failures": bool(failures),
            "failure_count": len(failures),
            "pass_count": len(passes),
            "recent_failures": failures[:5],
        }

    def _refresh_summary(self, conn: sqlite3.Connection) -> None:
        conn.execute("DELETE FROM layer7_keyword_feedback_summary")
        rows = conn.execute(
            """
            SELECT keyword_name,
                   SUM(CASE WHEN lower(status) IN ('pass', 'passed') THEN 1 ELSE 0 END) AS pass_count,
                   SUM(CASE WHEN lower(status) IN ('fail', 'failed') THEN 1 ELSE 0 END) AS fail_count
            FROM layer7_execution_feedback
            WHERE keyword_name != ''
            GROUP BY keyword_name
            """
        ).fetchall()
        for row in rows:
            data = {"keyword_name": row["keyword_name"], "pass_count": row["pass_count"], "fail_count": row["fail_count"]}
            conn.execute(
                """
                INSERT OR REPLACE INTO layer7_keyword_feedback_summary(keyword_name, pass_count, fail_count, data)
                VALUES (?, ?, ?, ?)
                """,
                (row["keyword_name"], row["pass_count"], row["fail_count"], json.dumps(data, ensure_ascii=False)),
            )

