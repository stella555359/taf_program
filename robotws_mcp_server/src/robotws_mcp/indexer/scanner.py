"""Filesystem scanner and index builder for RobotWS."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from robotws_mcp.models import DiscoveryReport, PythonSymbol, RobotFile
from robotws_mcp.parser.python_parser import PythonParser
from robotws_mcp.parser.robot_parser import RobotParser
from robotws_mcp.profiles.ownership import FeatureOwnershipDiscoverer
from robotws_mcp.profiles.store import ProfileStore
from robotws_mcp.storage.sqlite_store import SQLiteStore


DEFAULT_EXCLUDES = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "output",
    "results",
}


@dataclass
class IndexSummary:
    robot_files: int = 0
    robot_cases: int = 0
    robot_keywords: int = 0
    python_files: int = 0
    python_symbols: int = 0
    discovery_report: dict[str, object] | None = None
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "robot_files": self.robot_files,
            "robot_cases": self.robot_cases,
            "robot_keywords": self.robot_keywords,
            "python_files": self.python_files,
            "python_symbols": self.python_symbols,
            "discovery_report": self.discovery_report,
            "warnings": self.warnings,
        }


class RobotWsIndexer:
    """Scan RobotWS and optionally persist a SQLite index."""

    def __init__(
        self,
        robotws_root: str | Path,
        include_paths: list[str] | None = None,
        db_path: str | Path | None = None,
        profile_name: str = "Hangzhou_SG6_Common",
        profile_store: ProfileStore | None = None,
        discovery_report_path: str | Path | None = None,
    ) -> None:
        self.robotws_root = Path(robotws_root)
        self.include_paths = include_paths or ["."]
        self.db_path = Path(db_path) if db_path else Path("data/indexes/robotws.sqlite3")
        self.profile_store = profile_store or ProfileStore()
        self.profile = self.profile_store.get(profile_name)
        self.discovery_report_path = (
            Path(discovery_report_path) if discovery_report_path else self.db_path.with_name("sg6_discovery_report.json")
        )
        self.robot_parser = RobotParser()
        self.python_parser = PythonParser()

    def build(self, write_index: bool = False) -> IndexSummary:
        if not self.robotws_root.exists():
            raise FileNotFoundError(f"robotws root not found: {self.robotws_root}")

        summary = IndexSummary()
        store = SQLiteStore(self.db_path)
        if write_index:
            store.initialize()
            store.clear()

        robot_files: list[RobotFile] = []
        python_symbols_by_path: list[list[PythonSymbol]] = []
        for file_path in self._iter_source_files():
            if file_path.suffix.lower() in {".robot", ".resource"}:
                robot_file = self.robot_parser.parse_file(file_path, root=self.robotws_root)
                robot_files.append(robot_file)
                summary.robot_files += 1
                summary.robot_cases += len(robot_file.cases)
                summary.robot_keywords += len(robot_file.keywords)
                summary.warnings.extend(f"{robot_file.path}: {warning}" for warning in robot_file.parse_warnings)
            elif file_path.suffix.lower() == ".py":
                symbols = self.python_parser.parse_file(file_path, root=self.robotws_root)
                python_symbols_by_path.append(symbols)
                summary.python_files += 1
                summary.python_symbols += len(symbols)

        discovery_report = self._discover_ownership(robot_files)
        if discovery_report:
            summary.discovery_report = discovery_report.to_dict()
            if write_index:
                self.discovery_report_path.parent.mkdir(parents=True, exist_ok=True)
                self.discovery_report_path.write_text(
                    json.dumps(discovery_report.to_dict(), indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )

        if write_index:
            for robot_file in robot_files:
                if self._should_index_robot_file(robot_file, discovery_report):
                    store.insert_robot_file(robot_file)
            for symbols in python_symbols_by_path:
                if self._should_index_python_symbols(symbols):
                    store.insert_python_symbols(symbols)

        return summary

    def _discover_ownership(self, robot_files: list[RobotFile]) -> DiscoveryReport | None:
        if not self.profile or self.profile.name != "Hangzhou_SG6_Common":
            return None
        return FeatureOwnershipDiscoverer(self.profile).discover(robot_files)

    def _should_index_robot_file(self, robot_file: RobotFile, report: DiscoveryReport | None) -> bool:
        if not self.profile or self.profile.name != "Hangzhou_SG6_Common":
            return True
        return FeatureOwnershipDiscoverer(self.profile).is_indexable_path(robot_file.path, report)

    def _should_index_python_symbols(self, symbols: list[PythonSymbol]) -> bool:
        if not self.profile or self.profile.name != "Hangzhou_SG6_Common":
            return True
        for symbol in symbols:
            normalized = symbol.path.lower().replace("\\", "/")
            if any(normalized.startswith(scope.lower().replace("\\", "/")) for scope in self.profile.allowed_resource_scopes):
                return True
        return False

    def _iter_source_files(self) -> list[Path]:
        files: list[Path] = []
        for include_path in self.include_paths:
            root = self.robotws_root / include_path
            if root.is_file():
                files.append(root)
                continue
            if not root.exists():
                continue
            for path in root.rglob("*"):
                if any(part in DEFAULT_EXCLUDES for part in path.parts):
                    continue
                if path.suffix.lower() in {".robot", ".resource", ".py"}:
                    files.append(path)
        return sorted(set(files))
