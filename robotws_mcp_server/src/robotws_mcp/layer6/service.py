"""Layer 6 query-facing validation service."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from robotws_mcp.layer6.validator import GeneratedRobotValidator
from robotws_mcp.profiles.store import ProfileStore


class ValidationEngineService:
    """Expose generated Robot validation reports."""

    def __init__(
        self,
        layer2_db_path: str | Path,
        profile_store: ProfileStore | None = None,
        feedback_service: Any | None = None,
    ) -> None:
        self.validator = GeneratedRobotValidator(
            layer2_db_path=layer2_db_path,
            profile_store=profile_store,
            feedback_service=feedback_service,
        )

    def validate_generated_robot(
        self,
        robot_text: str,
        profile: str = "Hangzhou_SG6_Common",
        requirement: str = "",
    ) -> dict[str, Any]:
        return self.validator.validate(robot_text=robot_text, profile=profile, requirement=requirement).to_dict()

    def explain_validation_issue(
        self,
        robot_text: str,
        profile: str = "Hangzhou_SG6_Common",
        requirement: str = "",
    ) -> dict[str, Any]:
        report = self.validate_generated_robot(robot_text=robot_text, profile=profile, requirement=requirement)
        return {
            "decision": report["decision"],
            "errors": report["errors"],
            "warnings": report["warnings"],
            "suggestions": report["suggestions"],
        }

