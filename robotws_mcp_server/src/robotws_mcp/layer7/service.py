"""Layer 7 feedback query and import service."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from robotws_mcp.layer7.importers import import_jenkins_result_json, import_robot_output_xml
from robotws_mcp.layer7.models import ExecutionFeedback, feedback_id
from robotws_mcp.layer7.sqlite_store import FeedbackSQLiteStore


class ExecutionFeedbackService:
    """Record and query execution feedback."""

    def __init__(self, db_path: str | Path) -> None:
        self.store = FeedbackSQLiteStore(db_path)
        self.store.initialize()

    def record_execution_feedback(self, feedback: dict[str, Any]) -> dict[str, Any]:
        record = _feedback_from_dict(feedback)
        self.store.insert_feedback([record])
        return {"record": record.to_dict()}

    def import_robot_output_xml(self, path: str, profile: str = "", testline: str = "") -> dict[str, Any]:
        records = import_robot_output_xml(path, profile=profile, testline=testline)
        self.store.insert_feedback(records)
        return {"imported": len(records), "records": [record.to_dict() for record in records[:20]]}

    def import_jenkins_result_json(self, path: str) -> dict[str, Any]:
        records = import_jenkins_result_json(path)
        self.store.insert_feedback(records)
        return {"imported": len(records), "records": [record.to_dict() for record in records[:20]]}

    def get_execution_feedback(self, query: str = "", profile: str = "", limit: int = 50) -> dict[str, Any]:
        return {"feedback": self.store.search(query=query, profile=profile, limit=limit)}

    def get_feedback_hints(self, record_id_or_name: str, profile: str = "") -> dict[str, Any]:
        return self.store.hints(record_id_or_name, profile=profile)


def _feedback_from_dict(data: dict[str, Any]) -> ExecutionFeedback:
    record_id = str(data.get("id") or "")
    if not record_id:
        record_id = feedback_id(
            str(data.get("source_type", "manual")),
            str(data.get("test_name", "")),
            str(data.get("keyword_name", "")),
            str(data.get("status", "unknown")),
            str(data.get("message", "")),
        )
    return ExecutionFeedback(
        id=record_id,
        source_type=str(data.get("source_type", "manual")),
        source_path=str(data.get("source_path", "")),
        test_name=str(data.get("test_name", "")),
        keyword_name=str(data.get("keyword_name", "")),
        status=str(data.get("status", "unknown")),
        failure_class=str(data.get("failure_class") or _failure_class(str(data.get("message", "")))),
        message=str(data.get("message", "")),
        elapsed_ms=int(data.get("elapsed_ms", 0) or 0),
        profile=str(data.get("profile", "")),
        testline=str(data.get("testline", "")),
        metadata=dict(data.get("metadata", {})),
    )


def _failure_class(message: str) -> str:
    lower = message.lower()
    if not lower:
        return ""
    if "timeout" in lower:
        return "timeout"
    if "unknown keyword" in lower or "no keyword" in lower:
        return "keyword_resolution"
    if "connection" in lower or "ssh" in lower:
        return "environment_connection"
    return "execution_failure"

