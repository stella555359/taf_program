"""Query service for Layer 2 graph tools."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from robotws_mcp.layer2.sqlite_store import Layer2SQLiteStore


class Layer2QueryService:
    """Assemble bounded graph responses for MCP/API tools."""

    def __init__(self, db_path: str | Path) -> None:
        self.store = Layer2SQLiteStore(db_path)

    def get_testcase_graph(self, testcase_name_or_id: str, depth: int = 2) -> dict[str, Any]:
        testcase = self._find_node(testcase_name_or_id, "testcase")
        if not testcase:
            return {"testcase": None, "message": f"testcase not found: {testcase_name_or_id}"}
        return {
            "testcase": testcase,
            "setup": self._children_by_type(testcase["node_id"], "setup", depth),
            "body": self._children_by_type(testcase["node_id"], "step", depth),
            "teardown": self._children_by_type(testcase["node_id"], "teardown", depth),
            "taf_dependency": self.store.dependency_summary(testcase["record_id"]),
        }

    def get_keyword_graph(self, keyword_name_or_id: str, direction: str = "downstream", depth: int = 2) -> dict[str, Any]:
        keyword = self._find_node(keyword_name_or_id, "keyword")
        if not keyword:
            return {"keyword": None, "message": f"keyword not found: {keyword_name_or_id}"}
        if direction == "upstream":
            return {"keyword": keyword, "direction": direction, "callers": self._callers(keyword["node_id"])}
        return {
            "keyword": keyword,
            "direction": "downstream",
            "steps": self._children_by_type(keyword["node_id"], "", depth),
            "taf_dependency": self.store.dependency_summary(keyword["record_id"]),
        }

    def resolve_keyword_call(self, owner_id: str, step_id: str) -> dict[str, Any]:
        result = self.store.resolution_for_step(step_id)
        if not result:
            return {"owner_id": owner_id, "step_id": step_id, "message": "resolution result not found"}
        if owner_id and result.get("owner_id") != owner_id:
            return {**result, "warning": f"resolution owner is {result.get('owner_id')}, not {owner_id}"}
        return result

    def explain_taf_dependency(self, record_id: str) -> dict[str, Any]:
        summary = self.store.dependency_summary(record_id)
        if not summary:
            return {"record_id": record_id, "message": "dependency summary not found"}
        return summary

    def find_keyword_callers(
        self,
        keyword_name: str,
        domain: str = "",
        feature: str = "",
        limit: int = 20,
    ) -> dict[str, Any]:
        keyword = self._find_node(keyword_name, "keyword")
        if not keyword:
            return {"keyword": keyword_name, "callers": [], "message": "keyword not found"}
        callers = self._callers(keyword["node_id"])
        filtered = [
            item
            for item in callers
            if (not domain or item.get("domain") == domain) and (not feature or item.get("feature") == feature)
        ][:limit]
        return {"keyword": keyword, "callers": filtered}

    def get_unresolved_calls(
        self,
        domain: str = "",
        feature: str = "",
        status: str = "unresolved",
        limit: int = 50,
    ) -> dict[str, Any]:
        return {"calls": self.store.resolutions(status=status, domain=domain, feature=feature, limit=limit)}

    def _children_by_type(self, owner_node_id: str, normalized_type: str, depth: int) -> list[dict[str, Any]]:
        children: list[dict[str, Any]] = []
        for edge in self.store.edges(source_node_id=owner_node_id, edge_type="HAS_STEP"):
            step = self.store.node(edge["target_node_id"])
            if not step:
                continue
            step_type = step.get("data", {}).get("normalized_type", "")
            if normalized_type and step_type != normalized_type:
                continue
            children.append(self._expand_step(step, depth))
        return children

    def _expand_step(self, step: dict[str, Any], depth: int) -> dict[str, Any]:
        resolution = self.store.resolution_for_step(step["record_id"]) or {}
        item: dict[str, Any] = {
            "step": step.get("name", ""),
            "step_id": step.get("record_id", ""),
            "normalized_type": step.get("data", {}).get("normalized_type", ""),
            "arguments": step.get("data", {}).get("arguments", []),
            "condition": step.get("data", {}).get("condition"),
            "line_no": step.get("data", {}).get("line_no"),
            "resolution_status": resolution.get("resolution_status", ""),
            "called_target": resolution.get("called_target_node_id", ""),
            "reason": resolution.get("reason", ""),
        }
        if depth <= 1:
            return item
        target_id = resolution.get("called_target_node_id", "")
        target = self.store.node(target_id) if target_id else None
        if target and target.get("node_type") == "keyword":
            item["children"] = self._children_by_type(target["node_id"], "", depth - 1)
        return item

    def _callers(self, target_node_id: str) -> list[dict[str, Any]]:
        callers: list[dict[str, Any]] = []
        for call_edge in self.store.edges(target_node_id=target_node_id, edge_type="CALLS"):
            step = self.store.node(call_edge["source_node_id"])
            if not step:
                continue
            for has_step in self.store.edges(target_node_id=step["node_id"], edge_type="HAS_STEP"):
                owner = self.store.node(has_step["source_node_id"])
                if owner:
                    callers.append(
                        {
                            "owner": owner.get("name", ""),
                            "owner_id": owner.get("record_id", ""),
                            "owner_type": owner.get("node_type", ""),
                            "step": step.get("name", ""),
                            "step_id": step.get("record_id", ""),
                            "path": step.get("path", ""),
                            "domain": step.get("domain", ""),
                            "feature": step.get("feature"),
                            "line_no": step.get("data", {}).get("line_no"),
                        }
                    )
        return callers

    def _find_node(self, name_or_id: str, node_type: str) -> dict[str, Any] | None:
        direct = self.store.node(name_or_id)
        if direct and direct.get("node_type") == node_type:
            return direct
        matches = self.store.nodes(node_type=node_type, query=name_or_id, limit=20)
        for match in matches:
            if match.get("name") == name_or_id or match.get("record_id") == name_or_id or match.get("node_id") == name_or_id:
                return match
        return matches[0] if len(matches) == 1 else None

