"""Import execution feedback from Robot and CI artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

from robotws_mcp.layer7.models import ExecutionFeedback, feedback_id


def import_robot_output_xml(path: str | Path, profile: str = "", testline: str = "") -> list[ExecutionFeedback]:
    source_path = str(path)
    root = ElementTree.parse(path).getroot()
    records: list[ExecutionFeedback] = []
    for test in root.iter("test"):
        test_name = test.attrib.get("name", "")
        status_node = test.find("status")
        status = _status(status_node)
        message = (status_node.text or "").strip() if status_node is not None else ""
        records.append(
            ExecutionFeedback(
                id=feedback_id(source_path, test_name, "test", status),
                source_type="robot_output_xml",
                source_path=source_path,
                test_name=test_name,
                status=status,
                failure_class=_failure_class(message),
                message=message,
                elapsed_ms=_elapsed_ms(status_node),
                profile=profile,
                testline=testline,
            )
        )
        for kw in test.iter("kw"):
            kw_status = _status(kw.find("status"))
            if kw_status.lower() in {"fail", "failed"}:
                kw_name = kw.attrib.get("name", "")
                kw_status_node = kw.find("status")
                kw_message = (kw_status_node.text or "").strip() if kw_status_node is not None else message
                records.append(
                    ExecutionFeedback(
                        id=feedback_id(source_path, test_name, kw_name, kw_status),
                        source_type="robot_output_xml",
                        source_path=source_path,
                        test_name=test_name,
                        keyword_name=kw_name,
                        status=kw_status,
                        failure_class=_failure_class(kw_message),
                        message=kw_message,
                        elapsed_ms=_elapsed_ms(kw_status_node),
                        profile=profile,
                        testline=testline,
                    )
                )
    return records


def import_jenkins_result_json(path: str | Path) -> list[ExecutionFeedback]:
    source_path = str(path)
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    profile = str(data.get("profile", ""))
    testline = str(data.get("testline", ""))
    records: list[ExecutionFeedback] = []
    tests = data.get("tests") or data.get("cases") or []
    if not tests:
        status = str(data.get("status") or data.get("result") or "unknown")
        records.append(
            ExecutionFeedback(
                id=feedback_id(source_path, str(data.get("job", "")), status),
                source_type="jenkins_json",
                source_path=source_path,
                test_name=str(data.get("job", "")),
                status=status,
                failure_class=_failure_class(str(data.get("message", ""))),
                message=str(data.get("message", "")),
                elapsed_ms=int(data.get("elapsed_ms", 0) or 0),
                profile=profile,
                testline=testline,
                metadata=data,
            )
        )
        return records
    for item in tests:
        records.append(_feedback_from_jenkins_item(item, source_path, profile, testline))
    return records


def _feedback_from_jenkins_item(
    item: dict[str, Any],
    source_path: str,
    profile: str,
    testline: str,
) -> ExecutionFeedback:
    status = str(item.get("status") or item.get("result") or "unknown")
    message = str(item.get("message") or item.get("error") or "")
    test_name = str(item.get("test_name") or item.get("name") or "")
    keyword_name = str(item.get("keyword_name") or item.get("failed_keyword") or "")
    return ExecutionFeedback(
        id=feedback_id(source_path, test_name, keyword_name, status, message),
        source_type="jenkins_json",
        source_path=source_path,
        test_name=test_name,
        keyword_name=keyword_name,
        status=status,
        failure_class=str(item.get("failure_class") or _failure_class(message)),
        message=message,
        elapsed_ms=int(item.get("elapsed_ms", 0) or 0),
        profile=str(item.get("profile") or profile),
        testline=str(item.get("testline") or testline),
        metadata=item,
    )


def _status(status_node: ElementTree.Element | None) -> str:
    if status_node is None:
        return "unknown"
    return status_node.attrib.get("status", "unknown").lower()


def _elapsed_ms(status_node: ElementTree.Element | None) -> int:
    if status_node is None:
        return 0
    if "elapsedtime" in status_node.attrib:
        return int(float(status_node.attrib["elapsedtime"]))
    if "elapsed" in status_node.attrib:
        return int(float(status_node.attrib["elapsed"]) * 1000)
    return 0


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

