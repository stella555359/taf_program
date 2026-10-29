"""Build Layer 2 graph nodes and edges from Layer 1 records."""

from __future__ import annotations

import hashlib
from collections import Counter
from typing import Any

from robotws_mcp.layer2.input_loader import Layer1GraphInput
from robotws_mcp.layer2.models import GraphEdge, GraphNode, Layer2BuildSummary, ResolutionResult
from robotws_mcp.layer2.resolver import KeywordResolver
from robotws_mcp.models import normalize_path


class Layer2GraphBuilder:
    """Create deterministic graph records and keyword resolution results."""

    def __init__(self, graph_input: Layer1GraphInput) -> None:
        self.graph_input = graph_input

    def build(self) -> tuple[list[GraphNode], list[GraphEdge], list[ResolutionResult], Layer2BuildSummary]:
        nodes = self.build_nodes()
        base_edges = self.build_base_edges(nodes)
        resolutions = KeywordResolver(self.graph_input).resolve_all()
        call_nodes = self.build_synthetic_call_nodes(resolutions)
        all_nodes = _dedupe_nodes([*nodes, *call_nodes])
        call_edges = self.build_call_edges(resolutions)
        all_edges = _dedupe_edges([*base_edges, *call_edges])
        summary = Layer2BuildSummary(
            nodes=len(all_nodes),
            edges=len(all_edges),
            resolution_status_counts=dict(Counter(result.resolution_status for result in resolutions)),
            layer1_record_count=len(self.graph_input.records),
        )
        return all_nodes, all_edges, resolutions, summary

    def build_nodes(self) -> list[GraphNode]:
        nodes: list[GraphNode] = []
        for record in self.graph_input.records:
            record_type = str(record.get("record_type", ""))
            if record_type in {"testcase", "keyword", "step", "python_symbol"}:
                nodes.append(self._record_node(record))
                if record.get("domain"):
                    nodes.append(self._synthetic_node("domain", str(record.get("domain"))))
                if record.get("feature"):
                    nodes.append(self._synthetic_node("feature", str(record.get("feature"))))
            if record_type in {"robot_file", "keyword", "step", "python_symbol"} and _record_path(record):
                nodes.append(self._resource_file_node(_record_path(record), record))
            elif record_type == "resource_import":
                source = normalize_path(str(record.get("source_path") or ""))
                target = normalize_path(str(record.get("resolved_path") or record.get("resource_path") or ""))
                if source:
                    nodes.append(self._resource_file_node(source, record))
                if target:
                    nodes.append(self._resource_file_node(target, record))
        return _dedupe_nodes(nodes)

    def build_synthetic_call_nodes(self, resolutions: list[ResolutionResult]) -> list[GraphNode]:
        nodes: list[GraphNode] = []
        for result in resolutions:
            if result.resolution_status == "taf_library_keyword":
                nodes.append(
                    GraphNode(
                        node_id=result.called_target_node_id,
                        node_type="taf_library_keyword",
                        name=result.called_name,
                        impl_type="taf_dependent",
                        data=result.to_dict(),
                    )
                )
            elif result.resolution_status in {"builtin", "control_keyword"}:
                nodes.append(
                    GraphNode(
                        node_id=result.called_target_node_id,
                        node_type=result.resolution_status,
                        name=result.called_name,
                        impl_type="pure_logic",
                        data=result.to_dict(),
                    )
                )
        return _dedupe_nodes(nodes)

    def build_base_edges(self, nodes: list[GraphNode]) -> list[GraphEdge]:
        node_ids = {node.node_id for node in nodes}
        edges: list[GraphEdge] = []
        for owner_id, steps in self.graph_input.steps_by_owner.items():
            if owner_id not in node_ids:
                continue
            for step in steps:
                step_id = str(step.get("id", ""))
                if step_id in node_ids:
                    edges.append(
                        _edge(
                            "HAS_STEP",
                            owner_id,
                            step_id,
                            source_record_id=owner_id,
                            target_record_id=step_id,
                            step_id=step_id,
                            ordinal=int(step.get("ordinal", 0) or 0),
                        )
                    )
        for keyword in self.graph_input.by_type.get("keyword", []):
            keyword_id = str(keyword.get("id", ""))
            resource_node_id = _resource_node_id(_record_path(keyword))
            if keyword_id in node_ids and resource_node_id in node_ids:
                edges.append(
                    _edge(
                        "DEFINED_IN",
                        keyword_id,
                        resource_node_id,
                        source_record_id=keyword_id,
                        target_record_id=_record_path(keyword),
                    )
                )
        for record in self.graph_input.by_type.get("resource_import", []):
            source_path = normalize_path(str(record.get("source_path") or ""))
            target_path = normalize_path(str(record.get("resolved_path") or record.get("resource_path") or ""))
            if source_path and target_path:
                edges.append(
                    _edge(
                        "IMPORTS_RESOURCE",
                        _resource_node_id(source_path),
                        _resource_node_id(target_path),
                        source_record_id=str(record.get("id", "")),
                        target_record_id=target_path,
                        data={"raw": record.get("raw", "")},
                    )
                )
        for record in self.graph_input.by_type.get("library_import", []):
            source_path = normalize_path(str(record.get("source_path") or ""))
            library = str(record.get("library") or "")
            if source_path and library:
                target_id = f"library:{library}"
                edges.append(
                    _edge(
                        "IMPORTS_LIBRARY",
                        _resource_node_id(source_path),
                        target_id,
                        source_record_id=str(record.get("id", "")),
                        target_record_id=library,
                        data={"alias": record.get("alias")},
                    )
                )
        for record in [*self.graph_input.by_type.get("testcase", []), *self.graph_input.by_type.get("keyword", [])]:
            record_id = str(record.get("id", ""))
            if record_id not in node_ids:
                continue
            if record.get("domain"):
                edges.append(_edge("BELONGS_TO_DOMAIN", record_id, f"domain:{record.get('domain')}", source_record_id=record_id))
            if record.get("feature"):
                edges.append(_edge("BELONGS_TO_FEATURE", record_id, f"feature:{record.get('feature')}", source_record_id=record_id))
        return _dedupe_edges(edges)

    def build_call_edges(self, resolutions: list[ResolutionResult]) -> list[GraphEdge]:
        edges: list[GraphEdge] = []
        for result in resolutions:
            if not result.called_target_node_id:
                continue
            step = self.graph_input.by_id.get(result.step_id, {})
            edges.append(
                _edge(
                    "CALLS",
                    result.step_id,
                    result.called_target_node_id,
                    source_record_id=result.step_id,
                    target_record_id=result.called_target_record_id,
                    step_id=result.step_id,
                    ordinal=int(step.get("ordinal", 0) or 0),
                    resolution_status=result.resolution_status,
                    data=result.to_dict(),
                )
            )
        return _dedupe_edges(edges)

    def _record_node(self, record: dict[str, Any]) -> GraphNode:
        record_type = str(record.get("record_type", ""))
        name = str(record.get("name") or record.get("keyword") or record.get("robot_keyword_name") or record.get("qualified_name") or "")
        impl_type = str(record.get("robot_impl_type") or record.get("python_impl_type") or "unknown")
        if impl_type not in {"taf_dependent", "pure_logic", "unknown"}:
            impl_type = "unknown"
        return GraphNode(
            node_id=str(record.get("id", "")),
            node_type="testcase" if record_type == "testcase" else record_type,
            record_id=str(record.get("id", "")),
            name=name,
            path=_record_path(record),
            domain=str(record.get("domain", "Unknown")),
            feature=record.get("feature"),
            is_allowed=bool(record.get("is_allowed")),
            impl_type=impl_type,
            data=record,
        )

    def _resource_file_node(self, path: str, record: dict[str, Any]) -> GraphNode:
        return GraphNode(
            node_id=_resource_node_id(path),
            node_type="resource_file",
            record_id=path,
            name=path.rsplit("/", 1)[-1],
            path=path,
            domain=str(record.get("domain", "Unknown")),
            feature=record.get("feature"),
            is_allowed=bool(record.get("is_allowed", True)),
            data={"path": path},
        )

    def _synthetic_node(self, node_type: str, name: str) -> GraphNode:
        return GraphNode(
            node_id=f"{node_type}:{name}",
            node_type=node_type,
            name=name,
            data={"name": name},
        )


def _edge(
    edge_type: str,
    source_node_id: str,
    target_node_id: str,
    source_record_id: str = "",
    target_record_id: str = "",
    step_id: str = "",
    ordinal: int = 0,
    resolution_status: str = "",
    data: dict[str, Any] | None = None,
) -> GraphEdge:
    raw = "|".join([edge_type, source_node_id, target_node_id, step_id, str(ordinal)])
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]
    return GraphEdge(
        edge_id=f"edge:{digest}",
        edge_type=edge_type,
        source_node_id=source_node_id,
        target_node_id=target_node_id,
        source_record_id=source_record_id,
        target_record_id=target_record_id,
        step_id=step_id,
        ordinal=ordinal,
        resolution_status=resolution_status,
        data=data or {},
    )


def _record_path(record: dict[str, Any]) -> str:
    return normalize_path(str(record.get("path") or record.get("source_path") or record.get("resolved_path") or ""))


def _resource_node_id(path: str) -> str:
    return f"resource_file:{normalize_path(path)}"


def _dedupe_nodes(nodes: list[GraphNode]) -> list[GraphNode]:
    deduped: dict[str, GraphNode] = {}
    for node in nodes:
        if node.node_id and node.node_id not in deduped:
            deduped[node.node_id] = node
    return list(deduped.values())


def _dedupe_edges(edges: list[GraphEdge]) -> list[GraphEdge]:
    deduped: dict[str, GraphEdge] = {}
    for edge in edges:
        deduped[edge.edge_id] = edge
    return list(deduped.values())

