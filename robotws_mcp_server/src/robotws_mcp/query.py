"""Small CLI for querying the RobotWS index without Cursor."""

from __future__ import annotations

import argparse
import json

from robotws_mcp.server import DEFAULT_DB_PATH, DEFAULT_LAYER2_DB_PATH, DEFAULT_LAYER7_DB_PATH, RobotWsMcpService


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Query RobotWS MCP index.")
    parser.add_argument("--db-path", default=DEFAULT_DB_PATH)
    parser.add_argument("--layer2-db-path", default=DEFAULT_LAYER2_DB_PATH)
    parser.add_argument("--layer7-db-path", default=DEFAULT_LAYER7_DB_PATH)
    subparsers = parser.add_subparsers(dest="command", required=True)

    context = subparsers.add_parser("get-generation-context")
    context.add_argument("--requirement", required=True)
    context.add_argument("--profile", default="")
    context.add_argument("--path-hint", default="")
    context.add_argument("--limit", type=int, default=5)

    cases = subparsers.add_parser("search-cases")
    cases.add_argument("--query", required=True)
    cases.add_argument("--profile", default="")
    cases.add_argument("--limit", type=int, default=10)

    keywords = subparsers.add_parser("search-keywords")
    keywords.add_argument("--query", required=True)
    keywords.add_argument("--profile", default="")
    keywords.add_argument("--limit", type=int, default=10)

    validate = subparsers.add_parser("validate-style")
    validate.add_argument("--robot-text", required=True)
    validate.add_argument("--profile", default="")

    layer4 = subparsers.add_parser("layer4-retrieve")
    layer4.add_argument("--requirement", required=True)
    layer4.add_argument("--profile", default="")
    layer4.add_argument("--path-hint", default="")
    layer4.add_argument("--limit", type=int, default=5)

    layer5 = subparsers.add_parser("layer5-template")
    layer5.add_argument("--requirement", required=True)
    layer5.add_argument("--profile", default="")
    layer5.add_argument("--domain", default="")
    layer5.add_argument("--limit", type=int, default=3)

    layer6 = subparsers.add_parser("layer6-validate")
    layer6.add_argument("--robot-text", required=True)
    layer6.add_argument("--profile", default="")
    layer6.add_argument("--requirement", default="")

    layer7 = subparsers.add_parser("layer7-feedback")
    layer7.add_argument("--query", default="")
    layer7.add_argument("--profile", default="")
    layer7.add_argument("--limit", type=int, default=50)

    subparsers.add_parser("get-sg6-discovery-report")
    discovery = subparsers.add_parser("discover-sg6-features")
    discovery.add_argument("--area", default="")
    discovery.add_argument("--summary-only", action="store_true")

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    service = RobotWsMcpService(db_path=args.db_path, layer2_db_path=args.layer2_db_path, layer7_db_path=args.layer7_db_path)
    if args.command == "get-generation-context":
        result = service.get_generation_context(
            requirement=args.requirement,
            profile_hint=args.profile,
            path_hint=args.path_hint,
            limit=args.limit,
        )
    elif args.command == "search-cases":
        result = service.search_robot_cases(query=args.query, profile=args.profile, limit=args.limit)
    elif args.command == "search-keywords":
        result = service.search_robot_keywords(query=args.query, profile=args.profile, limit=args.limit)
    elif args.command == "validate-style":
        result = service.validate_generated_case_style(robot_text=args.robot_text, profile=args.profile)
    elif args.command == "layer4-retrieve":
        result = service.retrieve_generation_context(
            requirement=args.requirement,
            profile=args.profile,
            path_hint=args.path_hint,
            limit=args.limit,
        )
    elif args.command == "layer5-template":
        result = service.extract_template_from_requirement(
            requirement=args.requirement,
            profile=args.profile,
            domain=args.domain,
            limit=args.limit,
        )
    elif args.command == "layer6-validate":
        result = service.validate_generated_robot_static(
            robot_text=args.robot_text,
            profile=args.profile,
            requirement=args.requirement,
        )
    elif args.command == "layer7-feedback":
        result = service.get_execution_feedback(query=args.query, profile=args.profile, limit=args.limit)
    elif args.command == "get-sg6-discovery-report":
        result = service.get_sg6_discovery_report()
    elif args.command == "discover-sg6-features":
        result = service.discover_sg6_features(area=args.area, print_detail=not args.summary_only)
    else:
        raise SystemExit(f"Unsupported command: {args.command}")

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
