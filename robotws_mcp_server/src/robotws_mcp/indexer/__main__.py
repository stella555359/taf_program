"""CLI for building the RobotWS index."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any

from robotws_mcp.indexer.scanner import RobotWsIndexer
from robotws_mcp.profiles.store import ProfileStore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build RobotWS MCP index.")
    parser.add_argument("--robotws-root", required=True, help="Path to external robotws repository.")
    parser.add_argument("--profile", default="Hangzhou_SG6_Common", help="Style profile name.")
    parser.add_argument("--db-path", default="data/indexes/robotws.sqlite3", help="SQLite index path.")
    parser.add_argument(
        "--discovery-report-path",
        default="",
        help="Path for SG6 ownership discovery report JSON. Defaults beside the SQLite index.",
    )
    parser.add_argument(
        "--print-discovery",
        action="store_true",
        help="Print concise SG6 discovery details. Kept for compatibility with older commands.",
    )
    parser.add_argument("--discovery-details", action="store_true", help="Print concise SG6 discovery feature details.")
    parser.add_argument(
        "--status",
        choices=["confirmed", "excluded"],
        default="",
        help="Filter discovery details by ownership status.",
    )
    parser.add_argument("--area", choices=["RRM", "SISO"], default="", help="Filter discovery details by area.")
    parser.add_argument(
        "--case-type",
        choices=["Feature", "TMO"],
        default="",
        help="Filter discovery details by feature testcase or TMO/None_Feature_SG6 testcase.",
    )
    parser.add_argument("--top", type=int, default=20, help="Max discovery detail rows to print. Use 0 for all rows.")
    parser.add_argument("--list-paths", action="store_true", help="Print only matched discovery feature paths.")
    parser.add_argument("--dry-run", action="store_true", help="Scan and report without writing index.")
    parser.add_argument("--write-index", action="store_true", help="Write SQLite index.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.dry_run and args.write_index:
        raise SystemExit("--dry-run and --write-index are mutually exclusive")

    profile_store = ProfileStore()
    profile = profile_store.get(args.profile)
    include_paths = profile.path_scopes if profile else ["."]

    indexer = RobotWsIndexer(
        robotws_root=args.robotws_root,
        include_paths=include_paths,
        db_path=Path(args.db_path),
        profile_name=args.profile,
        profile_store=profile_store,
        discovery_report_path=Path(args.discovery_report_path) if args.discovery_report_path else None,
    )
    summary = indexer.build(write_index=args.write_index)
    output = summary.to_dict()
    report = output.get("discovery_report")
    report_saved_path = _save_explicit_report(report, args.discovery_report_path)
    if not report_saved_path and args.write_index and report:
        report_saved_path = str(indexer.discovery_report_path)

    if args.list_paths:
        print(
            _format_discovery_paths(
                report,
                status=args.status,
                area=args.area,
                case_type=args.case_type,
                top=args.top,
            )
        )
        return

    print(_format_summary(output, report_saved_path))
    if args.discovery_details or args.print_discovery or args.status or args.area or args.case_type:
        print()
        print(
            _format_discovery_details(
                report,
                status=args.status,
                area=args.area,
                case_type=args.case_type,
                top=args.top,
            )
        )


def _save_explicit_report(report: object, report_path: str) -> str:
    if not report or not report_path:
        return ""
    path = Path(report_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(path)


def _format_summary(output: dict[str, object], report_saved_path: str = "") -> str:
    report = output.get("discovery_report")
    lines = [
        "RobotWS Index Summary",
        f"- robot files: {output.get('robot_files', 0)}",
        f"- robot cases: {output.get('robot_cases', 0)}",
        f"- robot keywords: {output.get('robot_keywords', 0)}",
        f"- python files: {output.get('python_files', 0)}",
        f"- python symbols: {output.get('python_symbols', 0)}",
        f"- warnings: {len(output.get('warnings', []))}",
    ]
    if isinstance(report, dict):
        features = _features(report)
        status_counts = Counter(str(feature.get("status", "")) for feature in features)
        source_counts = Counter(str(feature.get("source", "")) for feature in features)
        lines.extend(
            [
                "",
                "SG6 Discovery Summary",
                f"- total features: {len(features)}",
                f"- confirmed: {status_counts.get('confirmed', 0)}",
                f"  - by allowlist: {source_counts.get('allowlist', 0)}",
                f"  - by None_Feature_SG6 path: {source_counts.get('none_feature_path', 0)}",
                f"- excluded: {status_counts.get('excluded', 0)}",
                f"  - by hard exclude: {source_counts.get('hard_exclude', 0)}",
                f"  - by not in allowlist: {source_counts.get('not_in_allowlist', 0)}",
            ]
        )
        if report_saved_path:
            lines.append(f"- full report saved to: {report_saved_path}")
        else:
            lines.append("- full report saved to: not saved in dry-run unless --discovery-report-path is provided")
        lines.append("- detail hint: add --status confirmed --top 0 --list-paths or --discovery-details")
    warnings = output.get("warnings", [])
    if isinstance(warnings, list) and warnings:
        lines.extend(["", "Warnings Preview"])
        for warning in warnings[:5]:
            lines.append(f"- {warning}")
        if len(warnings) > 5:
            lines.append(f"- ... {len(warnings) - 5} more warnings")
    return "\n".join(lines)


def _format_discovery_details(
    report: object,
    status: str = "",
    area: str = "",
    case_type: str = "",
    top: int = 20,
) -> str:
    if not isinstance(report, dict):
        return "SG6 Discovery Details\n- no discovery report available"
    filtered = _filtered_features(report, status=status, area=area, case_type=case_type, top=0)
    displayed = filtered if top == 0 else filtered[: max(top, 0)]
    label = f"SG6 Discovery Details (matched={len(filtered)}, shown={len(displayed)})"
    if status:
        label += f", status={status}"
    if area:
        label += f", area={area}"
    if case_type:
        label += f", case_type={case_type}"
    lines = [label]
    if not displayed:
        lines.append("- no matched features")
        return "\n".join(lines)
    for feature in displayed:
        reason = str(feature.get("exclude_reason", "")) or "-"
        lines.append(
            "- "
            f"{feature.get('area')} | {feature.get('feature')} | "
            f"{feature.get('status')} | {feature.get('source')} | "
            f"cases={feature.get('case_count')} | exclude={reason}"
        )
    if top and len(filtered) > len(displayed):
        lines.append(f"- ... {len(filtered) - len(displayed)} more matched features. Use --top 0 to show all.")
    return "\n".join(lines)


def _format_discovery_paths(
    report: object,
    status: str = "",
    area: str = "",
    case_type: str = "",
    top: int = 20,
) -> str:
    if not isinstance(report, dict):
        return ""
    features = _filtered_features(report, status=status, area=area, case_type=case_type, top=top)
    return "\n".join(str(feature.get("path", "")) for feature in features if feature.get("path"))


def _filtered_features(
    report: dict[str, Any],
    status: str = "",
    area: str = "",
    case_type: str = "",
    top: int = 20,
) -> list[dict[str, Any]]:
    features = _features(report)
    filtered = [
        feature
        for feature in features
        if (
            (not status or feature.get("status") == status)
            and (not area or feature.get("area") == area)
            and (not case_type or _case_type(feature) == case_type)
        )
    ]
    filtered = sorted(
        filtered,
        key=lambda feature: (
            str(feature.get("status", "")),
            str(feature.get("area", "")),
            str(feature.get("feature", "")),
        ),
    )
    return filtered if top == 0 else filtered[: max(top, 0)]


def _case_type(feature: dict[str, Any]) -> str:
    return "TMO" if str(feature.get("feature", "")).lower() == "none_feature_sg6" else "Feature"


def _features(report: dict[str, Any]) -> list[dict[str, Any]]:
    features = report.get("features", [])
    if isinstance(features, list):
        return [feature for feature in features if isinstance(feature, dict)]
    return []


if __name__ == "__main__":
    main()
