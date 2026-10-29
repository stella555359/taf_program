"""CLI for importing Layer 7 execution feedback."""

from __future__ import annotations

import argparse
import json

from robotws_mcp.layer7.service import ExecutionFeedbackService


DEFAULT_FEEDBACK_DB_PATH = "data/indexes/robotws_feedback.sqlite3"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import RobotWS execution feedback.")
    parser.add_argument("--db-path", default=DEFAULT_FEEDBACK_DB_PATH, help="Layer 7 feedback SQLite path.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    robot = subparsers.add_parser("robot-output")
    robot.add_argument("--path", required=True)
    robot.add_argument("--profile", default="")
    robot.add_argument("--testline", default="")

    jenkins = subparsers.add_parser("jenkins-json")
    jenkins.add_argument("--path", required=True)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    service = ExecutionFeedbackService(args.db_path)
    if args.command == "robot-output":
        result = service.import_robot_output_xml(args.path, profile=args.profile, testline=args.testline)
    elif args.command == "jenkins-json":
        result = service.import_jenkins_result_json(args.path)
    else:
        raise SystemExit(f"Unsupported command: {args.command}")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

