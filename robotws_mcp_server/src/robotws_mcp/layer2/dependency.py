"""TAF dependency propagation for Layer 2 graphs."""

from __future__ import annotations

from robotws_mcp.layer2.input_loader import Layer1GraphInput
from robotws_mcp.layer2.models import DependencySummary, ResolutionResult


class TafDependencyPropagator:
    """Classify testcase and keyword nodes using resolved call evidence."""

    def __init__(self, graph_input: Layer1GraphInput, resolutions: list[ResolutionResult]) -> None:
        self.graph_input = graph_input
        self.resolutions = resolutions
        self.results_by_owner: dict[str, list[ResolutionResult]] = {}
        for result in resolutions:
            self.results_by_owner.setdefault(result.owner_id, []).append(result)

    def build_summaries(self) -> list[DependencySummary]:
        summaries: list[DependencySummary] = []
        for record in [*self.graph_input.by_type.get("testcase", []), *self.graph_input.by_type.get("keyword", [])]:
            record_id = str(record.get("id", ""))
            impl_type, evidence_paths, unknown_reasons = self._classify_record(record_id, [])
            summaries.append(
                DependencySummary(
                    record_id=record_id,
                    node_id=record_id,
                    node_type=str(record.get("record_type", "")),
                    impl_type=impl_type,
                    has_taf_dependency=impl_type == "taf_dependent",
                    evidence_paths=evidence_paths[:10],
                    unknown_reasons=unknown_reasons[:10],
                    data={
                        "name": record.get("name", ""),
                        "path": record.get("path", ""),
                        "domain": record.get("domain", "Unknown"),
                        "feature": record.get("feature"),
                    },
                )
            )
        return summaries

    def _classify_record(self, record_id: str, stack: list[str]) -> tuple[str, list[list[str]], list[str]]:
        if record_id in stack:
            return "unknown", [], [f"cycle detected: {' -> '.join([*stack, record_id])}"]
        record = self.graph_input.by_id.get(record_id, {})
        if _record_is_taf(record):
            return "taf_dependent", [[_label(record)]], []
        if record.get("record_type") == "python_symbol":
            if record.get("python_impl_type") == "pure_python":
                return "pure_logic", [], []
            return "unknown", [], [f"python symbol has unknown implementation type: {_label(record)}"]

        evidence_paths: list[list[str]] = []
        unknown_reasons: list[str] = []
        for result in self.results_by_owner.get(record_id, []):
            if result.resolution_status == "taf_library_keyword":
                evidence_paths.append([_label(record), f"taf_library_keyword:{result.called_name}"])
                continue
            if result.resolution_status == "python_symbol":
                target = self.graph_input.by_id.get(result.called_target_record_id, {})
                if target.get("python_impl_type") == "taf_dependent":
                    evidence_paths.append([_label(record), _label(target)])
                elif target.get("python_impl_type") not in {"pure_python", "pure_logic"}:
                    unknown_reasons.append(f"python symbol target is not classified: {result.called_name}")
                continue
            if result.resolution_status == "resolved" and result.called_target_record_id:
                child_type, child_paths, child_unknowns = self._classify_record(result.called_target_record_id, [*stack, record_id])
                if child_type == "taf_dependent":
                    for path in child_paths or [[_label(self.graph_input.by_id.get(result.called_target_record_id, {}))]]:
                        evidence_paths.append([_label(record), *path])
                unknown_reasons.extend(child_unknowns)
                continue
            if result.resolution_status in {"ambiguous", "unresolved", "excluded"}:
                unknown_reasons.append(f"{result.resolution_status}: {result.called_name}")

        if evidence_paths:
            return "taf_dependent", evidence_paths, unknown_reasons
        if unknown_reasons:
            return "unknown", [], unknown_reasons
        return "pure_logic", [], []


def _record_is_taf(record: dict[str, object]) -> bool:
    return record.get("robot_impl_type") == "taf_dependent" or record.get("python_impl_type") == "taf_dependent"


def _label(record: dict[str, object]) -> str:
    record_type = str(record.get("record_type", "record"))
    name = str(record.get("name") or record.get("robot_keyword_name") or record.get("qualified_name") or record.get("id") or "")
    return f"{record_type}:{name}"

