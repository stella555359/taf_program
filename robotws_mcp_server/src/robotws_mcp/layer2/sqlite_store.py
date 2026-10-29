"""SQLite persistence for Layer 2 keyword graph records."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from robotws_mcp.layer2.models import DependencySummary, GraphEdge, GraphNode, ResolutionResult


class Layer2SQLiteStore:
    """Persist and query the derived Layer 2 graph index."""

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
                CREATE TABLE IF NOT EXISTS layer2_nodes (
                    node_id TEXT PRIMARY KEY,
                    node_type TEXT NOT NULL,
                    record_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    path TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    feature TEXT,
                    is_allowed INTEGER NOT NULL,
                    impl_type TEXT NOT NULL,
                    data TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS layer2_edges (
                    edge_id TEXT PRIMARY KEY,
                    edge_type TEXT NOT NULL,
                    source_node_id TEXT NOT NULL,
                    target_node_id TEXT NOT NULL,
                    source_record_id TEXT NOT NULL,
                    target_record_id TEXT NOT NULL,
                    step_id TEXT NOT NULL,
                    ordinal INTEGER NOT NULL,
                    resolution_status TEXT NOT NULL,
                    data TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS layer2_resolution_results (
                    step_id TEXT PRIMARY KEY,
                    owner_id TEXT NOT NULL,
                    called_name TEXT NOT NULL,
                    normalized_called_name TEXT NOT NULL,
                    resolution_status TEXT NOT NULL,
                    called_target_node_id TEXT NOT NULL,
                    called_target_record_id TEXT NOT NULL,
                    library_kind TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    candidates_json TEXT NOT NULL,
                    import_evidence_json TEXT NOT NULL,
                    data TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS layer2_dependency_summary (
                    record_id TEXT PRIMARY KEY,
                    node_id TEXT NOT NULL,
                    node_type TEXT NOT NULL,
                    impl_type TEXT NOT NULL,
                    has_taf_dependency INTEGER NOT NULL,
                    evidence_paths_json TEXT NOT NULL,
                    unknown_reasons_json TEXT NOT NULL,
                    data TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS layer2_build_info (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_layer2_nodes_type ON layer2_nodes(node_type);
                CREATE INDEX IF NOT EXISTS idx_layer2_nodes_record ON layer2_nodes(record_id);
                CREATE INDEX IF NOT EXISTS idx_layer2_nodes_name ON layer2_nodes(name);
                CREATE INDEX IF NOT EXISTS idx_layer2_edges_source ON layer2_edges(source_node_id);
                CREATE INDEX IF NOT EXISTS idx_layer2_edges_target ON layer2_edges(target_node_id);
                CREATE INDEX IF NOT EXISTS idx_layer2_edges_step ON layer2_edges(step_id);
                CREATE INDEX IF NOT EXISTS idx_layer2_resolution_status ON layer2_resolution_results(resolution_status);
                CREATE INDEX IF NOT EXISTS idx_layer2_dependency_type ON layer2_dependency_summary(impl_type);
                """
            )

    def clear(self) -> None:
        with self.connect() as conn:
            for table in (
                "layer2_nodes",
                "layer2_edges",
                "layer2_resolution_results",
                "layer2_dependency_summary",
                "layer2_build_info",
            ):
                conn.execute(f"DELETE FROM {table}")

    def insert_nodes(self, nodes: list[GraphNode]) -> None:
        with self.connect() as conn:
            for node in nodes:
                data = node.to_dict()
                conn.execute(
                    """
                    INSERT OR REPLACE INTO layer2_nodes(
                        node_id, node_type, record_id, name, path, domain, feature,
                        is_allowed, impl_type, data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        node.node_id,
                        node.node_type,
                        node.record_id,
                        node.name,
                        node.path,
                        node.domain,
                        node.feature,
                        1 if node.is_allowed else 0,
                        node.impl_type,
                        json.dumps(data, ensure_ascii=False),
                    ),
                )

    def insert_edges(self, edges: list[GraphEdge]) -> None:
        with self.connect() as conn:
            for edge in edges:
                data = edge.to_dict()
                conn.execute(
                    """
                    INSERT OR REPLACE INTO layer2_edges(
                        edge_id, edge_type, source_node_id, target_node_id,
                        source_record_id, target_record_id, step_id, ordinal,
                        resolution_status, data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        edge.edge_id,
                        edge.edge_type,
                        edge.source_node_id,
                        edge.target_node_id,
                        edge.source_record_id,
                        edge.target_record_id,
                        edge.step_id,
                        edge.ordinal,
                        edge.resolution_status,
                        json.dumps(data, ensure_ascii=False),
                    ),
                )

    def insert_resolution_results(self, results: list[ResolutionResult]) -> None:
        with self.connect() as conn:
            for result in results:
                data = result.to_dict()
                conn.execute(
                    """
                    INSERT OR REPLACE INTO layer2_resolution_results(
                        step_id, owner_id, called_name, normalized_called_name,
                        resolution_status, called_target_node_id, called_target_record_id,
                        library_kind, reason, candidates_json, import_evidence_json, data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        result.step_id,
                        result.owner_id,
                        result.called_name,
                        result.normalized_called_name,
                        result.resolution_status,
                        result.called_target_node_id,
                        result.called_target_record_id,
                        result.library_kind,
                        result.reason,
                        json.dumps(result.candidates, ensure_ascii=False),
                        json.dumps(result.import_evidence, ensure_ascii=False),
                        json.dumps(data, ensure_ascii=False),
                    ),
                )

    def insert_dependency_summaries(self, summaries: list[DependencySummary]) -> None:
        with self.connect() as conn:
            for summary in summaries:
                data = summary.to_dict()
                conn.execute(
                    """
                    INSERT OR REPLACE INTO layer2_dependency_summary(
                        record_id, node_id, node_type, impl_type, has_taf_dependency,
                        evidence_paths_json, unknown_reasons_json, data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        summary.record_id,
                        summary.node_id,
                        summary.node_type,
                        summary.impl_type,
                        1 if summary.has_taf_dependency else 0,
                        json.dumps(summary.evidence_paths, ensure_ascii=False),
                        json.dumps(summary.unknown_reasons, ensure_ascii=False),
                        json.dumps(data, ensure_ascii=False),
                    ),
                )

    def set_build_info(self, values: dict[str, Any]) -> None:
        with self.connect() as conn:
            for key, value in values.items():
                conn.execute(
                    "INSERT OR REPLACE INTO layer2_build_info(key, value) VALUES (?, ?)",
                    (key, json.dumps(value, ensure_ascii=False)),
                )

    def nodes(self, node_type: str = "", query: str = "", limit: int = 100) -> list[dict[str, Any]]:
        sql = "SELECT data FROM layer2_nodes"
        where: list[str] = []
        params: list[Any] = []
        if node_type:
            where.append("node_type = ?")
            params.append(node_type)
        if query:
            where.append("(name LIKE ? OR path LIKE ?)")
            params.extend([f"%{query}%", f"%{query}%"])
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY path, name LIMIT ?"
        params.append(limit)
        return self._select_json(sql, params)

    def node(self, node_id: str) -> dict[str, Any] | None:
        rows = self._select_json("SELECT data FROM layer2_nodes WHERE node_id = ? OR record_id = ? LIMIT 1", [node_id, node_id])
        return rows[0] if rows else None

    def edges(self, source_node_id: str = "", target_node_id: str = "", edge_type: str = "") -> list[dict[str, Any]]:
        sql = "SELECT data FROM layer2_edges"
        where: list[str] = []
        params: list[Any] = []
        if source_node_id:
            where.append("source_node_id = ?")
            params.append(source_node_id)
        if target_node_id:
            where.append("target_node_id = ?")
            params.append(target_node_id)
        if edge_type:
            where.append("edge_type = ?")
            params.append(edge_type)
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY ordinal, edge_id"
        return self._select_json(sql, params)

    def resolution_for_step(self, step_id: str) -> dict[str, Any] | None:
        rows = self._select_json("SELECT data FROM layer2_resolution_results WHERE step_id = ?", [step_id])
        return rows[0] if rows else None

    def resolutions(self, status: str = "", domain: str = "", feature: str = "", limit: int = 100) -> list[dict[str, Any]]:
        sql = "SELECT data FROM layer2_resolution_results"
        where: list[str] = []
        params: list[Any] = []
        if status:
            where.append("resolution_status = ?")
            params.append(status)
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY called_name LIMIT ?"
        params.append(limit)
        rows = self._select_json(sql, params)
        return [
            row
            for row in rows
            if (not domain or row.get("data", {}).get("domain") == domain)
            and (not feature or row.get("data", {}).get("feature") == feature)
        ]

    def dependency_summary(self, record_id: str) -> dict[str, Any] | None:
        rows = self._select_json("SELECT data FROM layer2_dependency_summary WHERE record_id = ?", [record_id])
        return rows[0] if rows else None

    def stats(self) -> dict[str, int]:
        with self.connect() as conn:
            return {
                table: conn.execute(f"SELECT COUNT(*) AS count FROM {table}").fetchone()["count"]
                for table in (
                    "layer2_nodes",
                    "layer2_edges",
                    "layer2_resolution_results",
                    "layer2_dependency_summary",
                )
            }

    def _select_json(self, sql: str, params: list[Any]) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [json.loads(row["data"]) for row in rows]

