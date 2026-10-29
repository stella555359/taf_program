"""Layer 4 service methods exposed to MCP/API."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from robotws_mcp.layer2.query import Layer2QueryService
from robotws_mcp.layer4.models import RetrievalResult
from robotws_mcp.layer4.retriever import HybridRetriever
from robotws_mcp.profiles.store import ProfileStore
from robotws_mcp.retrieval.context_builder import ContextBuilder, GenerationContextRequest


class SemanticRetrievalService:
    """Explainable retrieval facade for generation context."""

    def __init__(
        self,
        db_path: str | Path,
        layer2_db_path: str | Path,
        profile_store: ProfileStore | None = None,
        feedback_service: Any | None = None,
    ) -> None:
        self.profile_store = profile_store or ProfileStore()
        self.context_builder = ContextBuilder(db_path=db_path, profile_store=self.profile_store)
        self.layer2_query = Layer2QueryService(layer2_db_path)
        self.retriever = HybridRetriever(
            context_builder=self.context_builder,
            layer2_query=self.layer2_query,
            profile_store=self.profile_store,
            feedback_service=feedback_service,
        )

    def retrieve_generation_context(
        self,
        requirement: str,
        profile: str = "",
        path_hint: str = "",
        limit: int = 5,
    ) -> dict[str, Any]:
        base_context = self.context_builder.build_generation_context(
            GenerationContextRequest(
                requirement=requirement,
                profile_hint=profile,
                path_hint=path_hint,
                limit=limit,
            )
        )
        evidence = self.retriever.search_evidence(
            query=requirement,
            profile=profile or str((base_context.get("profile") or {}).get("name", "")),
            limit=limit,
        )
        result = RetrievalResult(
            query=requirement,
            profile=profile or str((base_context.get("profile") or {}).get("name", "")),
            vector_status="disabled:no_embedding_provider",
            evidence=evidence,
            metadata={
                "mode": "hybrid_without_vectors",
                "base_context": base_context,
            },
        )
        return result.to_dict()

    def search_evidence(
        self,
        query: str,
        profile: str = "",
        evidence_types: list[str] | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        result = RetrievalResult(
            query=query,
            profile=profile,
            vector_status="disabled:no_embedding_provider",
            evidence=self.retriever.search_evidence(query, profile, evidence_types, limit),
            metadata={"evidence_types": evidence_types or ["testcase", "keyword"]},
        )
        return result.to_dict()

    def rank_keyword_candidates(
        self,
        query: str,
        profile: str = "",
        domain: str = "",
        feature: str = "",
        limit: int = 10,
    ) -> dict[str, Any]:
        result = RetrievalResult(
            query=query,
            profile=profile,
            vector_status="disabled:no_embedding_provider",
            evidence=self.retriever.rank_keyword_candidates(query, profile, domain, feature, limit),
            metadata={"domain": domain, "feature": feature},
        )
        return result.to_dict()

