"""Layer 1 v2 scanner CLI."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path

from robotws_mcp.layer1.python_ast_parser import PythonAstParser
from robotws_mcp.layer1.records import Layer1Record, ParseIssueRecord
from robotws_mcp.layer1.robot_ast_parser import RobotAstParser
from robotws_mcp.layer1.sqlite_store import Layer1SQLiteStore
from robotws_mcp.profiles.store import ProfileStore

DEFAULT_EXCLUDES = {".git", "__pycache__", ".pytest_cache", ".venv", "venv", "output", "results"}


@dataclass
class Layer1ScanSummary:
    robot_files: int = 0
    testcases: int = 0
    keywords: int = 0
    steps: int = 0
    resource_imports: int = 0
    library_imports: int = 0
    variables: int = 0
    python_symbols: int = 0
    parse_issues: int = 0
    sqlite_path: str = ""
    json_exports: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "robot_files": self.robot_files,
            "testcases": self.testcases,
            "keywords": self.keywords,
            "steps": self.steps,
            "resource_imports": self.resource_imports,
            "library_imports": self.library_imports,
            "variables": self.variables,
            "python_symbols": self.python_symbols,
            "parse_issues": self.parse_issues,
            "sqlite_path": self.sqlite_path,
            "json_exports": self.json_exports,
        }


class Layer1Scanner:
    """Scan RobotWS sources into Layer 1 v2 records."""

    def __init__(
        self,
        robotws_root: str | Path,
        profile_name: str = "Hangzhou_SG6_Common",
        include_paths: list[str] | None = None,
        profile_store: ProfileStore | None = None,
    ) -> None:
        self.robotws_root = Path(robotws_root)
        self.profile_store = profile_store or ProfileStore()
        self.profile = self.profile_store.effective(profile_name) or self.profile_store.get(profile_name)
        self.include_paths = include_paths or (self.profile.path_scopes if self.profile else ["."])
        self.robot_parser = RobotAstParser()
        self.python_parser = PythonAstParser()

    def scan(self) -> tuple[list[Layer1Record], Layer1ScanSummary]:
        if not self.robotws_root.exists():
            raise FileNotFoundError(f"robotws root not found: {self.robotws_root}")

        records: list[Layer1Record] = []
        summary = Layer1ScanSummary()
        for path in self._iter_source_files():
            if path.suffix.lower() in {".robot", ".resource"}:
                parsed = self.robot_parser.parse_file(path, root=self.robotws_root, profile=self.profile)
                records.extend(parsed.files)
                records.extend(parsed.testcases)
                records.extend(parsed.keywords)
                records.extend(parsed.steps)
                records.extend(parsed.resource_imports)
                records.extend(parsed.library_imports)
                records.extend(parsed.variables)
                records.extend(parsed.parse_issues)
                summary.robot_files += len(parsed.files)
                summary.testcases += len(parsed.testcases)
                summary.keywords += len(parsed.keywords)
                summary.steps += len(parsed.steps)
                summary.resource_imports += len(parsed.resource_imports)
                summary.library_imports += len(parsed.library_imports)
                summary.variables += len(parsed.variables)
                summary.parse_issues += len(parsed.parse_issues)
            elif path.suffix.lower() == ".py":
                symbols, issues = self.python_parser.parse_file(path, root=self.robotws_root, profile=self.profile)
                records.extend(symbols)
                records.extend(issues)
                summary.python_symbols += len(symbols)
                summary.parse_issues += len(issues)
        return records, summary

    def _iter_source_files(self) -> list[Path]:
        files: list[Path] = []
        for include_path in self.include_paths:
            root = self.robotws_root / include_path
            if root.is_file() and root.suffix.lower() in {".robot", ".resource", ".py"}:
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Layer 1 v2 RobotWS metadata index.")
    parser.add_argument("--robotws-root", required=True, help="Path to external robotws repository.")
    parser.add_argument("--profile", default="Hangzhou_SG6_Common", help="Profile name.")
    parser.add_argument("--db-path", default="data/indexes/robotws_layer1_v2.sqlite3", help="SQLite v2 index path.")
    parser.add_argument("--write-index", action="store_true", help="Write SQLite v2 index.")
    parser.add_argument("--export-json", action="store_true", help="Export scan summary and parse issues JSON.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scanner = Layer1Scanner(robotws_root=args.robotws_root, profile_name=args.profile)
    records, summary = scanner.scan()
    db_path = Path(args.db_path)
    summary.sqlite_path = str(db_path)

    if args.write_index:
        store = Layer1SQLiteStore(db_path)
        store.initialize()
        store.clear()
        store.insert_records(records)

    if args.export_json:
        summary_path = db_path.with_name("layer1_v2_scan_summary.json")
        issues_path = db_path.with_name("layer1_v2_parse_issues.json")
        summary_path.write_text(json.dumps(summary.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        parse_issues = [record.to_dict() for record in records if isinstance(record, ParseIssueRecord)]
        issues_path.write_text(json.dumps(parse_issues, indent=2, ensure_ascii=False), encoding="utf-8")
        summary.json_exports.extend([str(summary_path), str(issues_path)])

    print(json.dumps(summary.to_dict(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
