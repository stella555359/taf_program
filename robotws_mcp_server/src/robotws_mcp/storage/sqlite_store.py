"""SQLite storage for RobotWS structured index."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from robotws_mcp.models import CallEdge, PythonSymbol, RobotFile


class SQLiteStore:
    """Persist and query RobotWS index data."""

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
                CREATE TABLE IF NOT EXISTS robot_files (
                    path TEXT PRIMARY KEY,
                    data TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS robot_cases (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    path TEXT NOT NULL,
                    line_no INTEGER NOT NULL,
                    tags TEXT NOT NULL,
                    documentation TEXT NOT NULL,
                    setup TEXT,
                    teardown TEXT,
                    called_keywords TEXT NOT NULL,
                    data TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS robot_keywords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    path TEXT NOT NULL,
                    line_no INTEGER NOT NULL,
                    arguments TEXT NOT NULL,
                    documentation TEXT NOT NULL,
                    called_keywords TEXT NOT NULL,
                    data TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS library_imports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT NOT NULL,
                    library TEXT NOT NULL,
                    alias TEXT,
                    data TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS resource_imports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT NOT NULL,
                    resource TEXT NOT NULL,
                    data TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS call_edges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    caller_type TEXT NOT NULL,
                    caller_name TEXT NOT NULL,
                    callee_name TEXT NOT NULL,
                    path TEXT NOT NULL,
                    line_no INTEGER NOT NULL,
                    raw TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS python_symbols (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT NOT NULL,
                    name TEXT NOT NULL,
                    symbol_type TEXT NOT NULL,
                    line_no INTEGER NOT NULL,
                    signature TEXT NOT NULL,
                    docstring TEXT NOT NULL,
                    imports TEXT NOT NULL,
                    data TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_cases_name ON robot_cases(name);
                CREATE INDEX IF NOT EXISTS idx_cases_path ON robot_cases(path);
                CREATE INDEX IF NOT EXISTS idx_keywords_name ON robot_keywords(name);
                CREATE INDEX IF NOT EXISTS idx_keywords_path ON robot_keywords(path);
                CREATE INDEX IF NOT EXISTS idx_edges_caller ON call_edges(caller_name);
                CREATE INDEX IF NOT EXISTS idx_edges_callee ON call_edges(callee_name);
                CREATE INDEX IF NOT EXISTS idx_libs_library ON library_imports(library);
                """
            )

    def clear(self) -> None:
        with self.connect() as conn:
            for table in (
                "robot_files",
                "robot_cases",
                "robot_keywords",
                "library_imports",
                "resource_imports",
                "call_edges",
                "python_symbols",
            ):
                conn.execute(f"DELETE FROM {table}")

    def insert_robot_file(self, robot_file: RobotFile) -> None:
        with self.connect() as conn:
            data = robot_file.to_dict()
            conn.execute(
                "INSERT OR REPLACE INTO robot_files(path, data) VALUES (?, ?)",
                (robot_file.path, json.dumps(data, ensure_ascii=False)),
            )
            for resource in robot_file.resources:
                conn.execute(
                    "INSERT INTO resource_imports(path, resource, data) VALUES (?, ?, ?)",
                    (resource.path, resource.resource, json.dumps(resource.to_dict(), ensure_ascii=False)),
                )
            for library in robot_file.libraries:
                conn.execute(
                    "INSERT INTO library_imports(path, library, alias, data) VALUES (?, ?, ?, ?)",
                    (
                        library.path,
                        library.library,
                        library.alias,
                        json.dumps(library.to_dict(), ensure_ascii=False),
                    ),
                )
            for case in robot_file.cases:
                case_data = case.to_dict()
                conn.execute(
                    """
                    INSERT INTO robot_cases(
                        name, path, line_no, tags, documentation, setup, teardown,
                        called_keywords, data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        case.name,
                        case.path,
                        case.line_no,
                        json.dumps(case.tags, ensure_ascii=False),
                        json.dumps(case.documentation, ensure_ascii=False),
                        case.setup,
                        case.teardown,
                        json.dumps(case_data["called_keywords"], ensure_ascii=False),
                        json.dumps(case_data, ensure_ascii=False),
                    ),
                )
                for step in case.steps:
                    self._insert_call_edge(
                        conn,
                        CallEdge(
                            caller_type="case",
                            caller_name=case.name,
                            callee_name=step.keyword,
                            path=case.path,
                            line_no=step.line_no,
                            raw=step.raw,
                        ),
                    )
            for keyword in robot_file.keywords:
                keyword_data = keyword.to_dict()
                conn.execute(
                    """
                    INSERT INTO robot_keywords(
                        name, path, line_no, arguments, documentation,
                        called_keywords, data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        keyword.name,
                        keyword.path,
                        keyword.line_no,
                        json.dumps(keyword.arguments, ensure_ascii=False),
                        json.dumps(keyword.documentation, ensure_ascii=False),
                        json.dumps(keyword_data["called_keywords"], ensure_ascii=False),
                        json.dumps(keyword_data, ensure_ascii=False),
                    ),
                )
                for step in keyword.steps:
                    self._insert_call_edge(
                        conn,
                        CallEdge(
                            caller_type="keyword",
                            caller_name=keyword.name,
                            callee_name=step.keyword,
                            path=keyword.path,
                            line_no=step.line_no,
                            raw=step.raw,
                        ),
                    )

    def insert_python_symbols(self, symbols: list[PythonSymbol]) -> None:
        with self.connect() as conn:
            for symbol in symbols:
                data = symbol.to_dict()
                conn.execute(
                    """
                    INSERT INTO python_symbols(
                        path, name, symbol_type, line_no, signature, docstring, imports, data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        symbol.path,
                        symbol.name,
                        symbol.symbol_type,
                        symbol.line_no,
                        symbol.signature,
                        symbol.docstring,
                        json.dumps(symbol.imports, ensure_ascii=False),
                        json.dumps(data, ensure_ascii=False),
                    ),
                )

    def search_cases(self, query: str, profile_paths: list[str] | None = None, limit: int = 10) -> list[dict[str, Any]]:
        return self._search_table("robot_cases", query, profile_paths, limit)

    def search_keywords(self, query: str, profile_paths: list[str] | None = None, limit: int = 10) -> list[dict[str, Any]]:
        return self._search_table("robot_keywords", query, profile_paths, limit)

    def get_case(self, name_or_path: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT data FROM robot_cases WHERE name = ? OR path = ? ORDER BY line_no LIMIT 1",
                (name_or_path, name_or_path),
            ).fetchone()
            return json.loads(row["data"]) if row else None

    def trace_keyword(self, keyword_name: str, depth: int = 2) -> list[dict[str, Any]]:
        edges: list[dict[str, Any]] = []
        seen: set[tuple[str, str]] = set()

        def walk(name: str, remaining: int) -> None:
            if remaining <= 0:
                return
            with self.connect() as conn:
                rows = conn.execute(
                    """
                    SELECT caller_type, caller_name, callee_name, path, line_no, raw
                    FROM call_edges
                    WHERE caller_name = ?
                    ORDER BY path, line_no
                    """,
                    (name,),
                ).fetchall()
            for row in rows:
                key = (row["caller_name"], row["callee_name"])
                if key in seen:
                    continue
                seen.add(key)
                edge = dict(row)
                edges.append(edge)
                walk(row["callee_name"], remaining - 1)

        walk(keyword_name, depth)
        return edges

    def find_library_usage(self, library_name: str, profile_paths: list[str] | None = None) -> list[dict[str, Any]]:
        pattern = f"%{library_name}%"
        query = "SELECT data FROM library_imports WHERE library LIKE ?"
        params: list[Any] = [pattern]
        if profile_paths:
            clauses = " OR ".join("path LIKE ?" for _ in profile_paths)
            query += f" AND ({clauses})"
            params.extend([f"{path}%" for path in profile_paths])
        query += " ORDER BY path LIMIT 100"
        with self.connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [json.loads(row["data"]) for row in rows]

    def stats(self) -> dict[str, int]:
        with self.connect() as conn:
            return {
                table: conn.execute(f"SELECT COUNT(*) AS count FROM {table}").fetchone()["count"]
                for table in (
                    "robot_files",
                    "robot_cases",
                    "robot_keywords",
                    "library_imports",
                    "resource_imports",
                    "call_edges",
                    "python_symbols",
                )
            }

    def _insert_call_edge(self, conn: sqlite3.Connection, edge: CallEdge) -> None:
        conn.execute(
            """
            INSERT INTO call_edges(caller_type, caller_name, callee_name, path, line_no, raw)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (edge.caller_type, edge.caller_name, edge.callee_name, edge.path, edge.line_no, edge.raw),
        )

    def _search_table(
        self,
        table: str,
        query: str,
        profile_paths: list[str] | None,
        limit: int,
    ) -> list[dict[str, Any]]:
        terms = [term for term in query.lower().split() if term]
        sql = f"SELECT data, path, name, documentation FROM {table}"
        params: list[Any] = []
        where: list[str] = []
        if profile_paths:
            where.append("(" + " OR ".join("path LIKE ?" for _ in profile_paths) + ")")
            params.extend([f"{path}%" for path in profile_paths])
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY path, line_no LIMIT 500"

        with self.connect() as conn:
            rows = conn.execute(sql, params).fetchall()

        scored: list[tuple[int, dict[str, Any]]] = []
        for row in rows:
            data = json.loads(row["data"])
            haystack = " ".join(
                [
                    str(data.get("name", "")),
                    str(data.get("path", "")),
                    " ".join(data.get("documentation", [])),
                    " ".join(data.get("tags", [])),
                    " ".join(data.get("called_keywords", [])),
                ]
            ).lower()
            score = sum(3 if term in str(data.get("name", "")).lower() else 1 for term in terms if term in haystack)
            if not terms or score:
                data["_score"] = score
                scored.append((score, data))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [item[1] for item in scored[:limit]]
