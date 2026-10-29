"""Explainable hybrid retrieval without runtime embedding dependencies."""

from __future__ import annotations

import re
from typing import Any

from robotws_mcp.layer2.query import Layer2QueryService
from robotws_mcp.layer4.models import RetrievalEvidence
from robotws_mcp.profiles.store import ProfileStore
from robotws_mcp.retrieval.context_builder import ContextBuilder


class HybridRetriever:
    """Rank RobotWS facts using metadata, lexical, graph, and feedback signals."""

    def __init__(
        self,
        context_builder: ContextBuilder,
        layer2_query: Layer2QueryService,
        profile_store: ProfileStore,
        feedback_service: Any | None = None,
    ) -> None:
        self.context_builder = context_builder
        self.layer2_query = layer2_query
        self.profile_store = profile_store
        self.feedback_service = feedback_service

    def search_evidence(
        self,
        query: str,
        profile: str = "",
        evidence_types: list[str] | None = None,
        limit: int = 10,
    ) -> list[RetrievalEvidence]:
        selected_types = evidence_types or ["testcase", "keyword"]
        evidence: list[RetrievalEvidence] = []
        if "testcase" in selected_types:
            cases = self.context_builder.search_cases(query=query, profile=profile, limit=max(limit, 20))
            evidence.extend(self._rank_items(query, "testcase", cases, profile))
        if "keyword" in selected_types:
            keywords = self.context_builder.search_keywords(query=query, profile=profile, limit=max(limit, 20))
            evidence.extend(self._rank_items(query, "keyword", keywords, profile))
        evidence.sort(key=lambda item: (item.score, item.name), reverse=True)
        return evidence[:limit]

    def rank_keyword_candidates(
        self,
        query: str,
        profile: str = "",
        domain: str = "",
        feature: str = "",
        limit: int = 10,
    ) -> list[RetrievalEvidence]:
        nodes_by_id: dict[str, dict[str, Any]] = {}
        for candidate_query in [query, *_tokens(query)]:
            if not candidate_query:
                continue
            for node in self.layer2_query.store.nodes(node_type="keyword", query=candidate_query, limit=max(limit * 10, 50)):
                nodes_by_id[str(node.get("node_id") or node.get("record_id") or node.get("name"))] = node
        nodes = list(nodes_by_id.values())
        filtered = [
            node
            for node in nodes
            if node.get("is_allowed")
            and (not domain or node.get("domain") in {domain, "Common"})
            and (not feature or node.get("feature") in {feature, None})
        ]
        evidence = self._rank_items(query, "keyword", filtered, profile)
        evidence.sort(key=lambda item: (item.score, item.name), reverse=True)
        return evidence[:limit]

    def _rank_items(
        self,
        query: str,
        evidence_type: str,
        items: list[dict[str, Any]],
        profile: str,
    ) -> list[RetrievalEvidence]:
        terms = _tokens(query)
        ranked: list[RetrievalEvidence] = []
        for item in items:
            score, reasons = self._score(item, terms)
            if score <= 0 and terms:
                continue
            record_id = str(item.get("record_id") or item.get("id") or item.get("node_id") or item.get("name", ""))
            taf_dependency = None
            if evidence_type == "keyword":
                taf_dependency = self.layer2_query.store.dependency_summary(record_id)
            feedback = self._feedback_hint(record_id, item.get("name", ""), profile)
            if feedback.get("has_failures"):
                score -= 2
                reasons.append("feedback has previous failures")
            ranked.append(
                RetrievalEvidence(
                    evidence_type=evidence_type,
                    record_id=record_id,
                    name=str(item.get("name", "")),
                    path=str(item.get("path", "")),
                    score=score,
                    match_reasons=reasons,
                    domain=str(item.get("domain", "")),
                    feature=item.get("feature"),
                    taf_dependency=taf_dependency,
                    feedback=feedback or None,
                    data=_compact_item(item),
                )
            )
        return ranked

    def _score(self, item: dict[str, Any], terms: list[str]) -> tuple[int, list[str]]:
        name = str(item.get("name", ""))
        path = str(item.get("path", ""))
        docs = " ".join(str(value) for value in item.get("documentation", []))
        tags = " ".join(str(value) for value in item.get("tags", []))
        called = " ".join(str(value) for value in item.get("called_keywords", item.get("keyword_sequence", [])))
        haystacks = {
            "name": name.lower(),
            "path": path.lower(),
            "documentation": docs.lower(),
            "tags": tags.lower(),
            "called keywords": called.lower(),
        }
        score = int(item.get("_score", 0) or 0)
        reasons: list[str] = []
        for term in terms:
            if term in haystacks["name"]:
                score += 6
                reasons.append(f"name matches '{term}'")
            elif term in haystacks["called keywords"]:
                score += 3
                reasons.append(f"called keyword matches '{term}'")
            elif term in haystacks["documentation"]:
                score += 2
                reasons.append(f"documentation matches '{term}'")
            elif term in haystacks["tags"]:
                score += 2
                reasons.append(f"tag matches '{term}'")
            elif term in haystacks["path"]:
                score += 1
                reasons.append(f"path matches '{term}'")
        if item.get("is_allowed") is True:
            score += 2
            reasons.append("allowed boundary evidence")
        if item.get("impl_type") == "taf_dependent" or item.get("robot_impl_type") == "taf_dependent":
            score += 1
            reasons.append("TAF-dependent reusable wrapper")
        return score, _dedupe(reasons)

    def _feedback_hint(self, record_id: str, name: str, profile: str) -> dict[str, Any]:
        if not self.feedback_service:
            return {}
        try:
            return self.feedback_service.get_feedback_hints(record_id or name, profile=profile)
        except Exception:
            return {}


def _tokens(query: str) -> list[str]:
    return [token for token in re.split(r"[^a-zA-Z0-9_]+", query.lower()) if token]


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


def _compact_item(item: dict[str, Any]) -> dict[str, Any]:
    keys = ("name", "path", "line_no", "documentation", "tags", "keyword_sequence", "called_keywords", "arguments_schema")
    return {key: item.get(key) for key in keys if key in item}

