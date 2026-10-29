"""Configuration models for optional provider integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ProviderMode = Literal["context_only", "ai_assisted", "hybrid"]


@dataclass(frozen=True)
class AiSettings:
    enabled: bool = False
    provider: str = "noop"
    mode: ProviderMode = "context_only"
    timeout_seconds: int = 60


@dataclass(frozen=True)
class InsightsFusionSettings:
    base_url: str = ""
    workflow_robot_generation: str = ""
    workflow_case_review: str = ""
    workflow_rca: str = ""
    token_env: str = "INSIGHTS_FUSION_TOKEN"


@dataclass(frozen=True)
class OpenAiCompatibleSettings:
    base_url: str = ""
    model: str = ""
    api_key_env: str = "ROBOTWS_LLM_API_KEY"
