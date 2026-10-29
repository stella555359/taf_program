"""Profile-aware style validation for generated Robot text."""

from __future__ import annotations

from dataclasses import dataclass, field

from robotws_mcp.models import StyleProfile


@dataclass
class StyleValidationResult:
    passed: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "warnings": self.warnings,
            "errors": self.errors,
        }


class StyleValidator:
    """Validate generated Robot Framework text against a style profile."""

    def validate(self, robot_text: str, profile: StyleProfile | None) -> StyleValidationResult:
        warnings: list[str] = []
        errors: list[str] = []

        if not robot_text.strip():
            errors.append("Generated Robot text is empty.")
            return StyleValidationResult(passed=False, warnings=warnings, errors=errors)

        lines = [line.rstrip() for line in robot_text.splitlines()]
        joined = "\n".join(lines)

        if "[Documentation]" not in joined:
            warnings.append("Missing [Documentation].")
        if "[Tags]" not in joined:
            warnings.append("Missing [Tags].")
        if "[Setup]" not in joined:
            warnings.append("Missing [Setup].")
        if "[Teardown]" not in joined:
            warnings.append("Missing [Teardown].")

        if profile:
            self._validate_profile_patterns(joined, profile, warnings)

        for idx, line in enumerate(lines, start=1):
            if line.startswith(" ") and not line.startswith("    "):
                warnings.append(f"Line {idx}: indentation is not a multiple of four spaces.")
            if "\t" in line:
                warnings.append(f"Line {idx}: tab indentation found.")

        return StyleValidationResult(passed=not errors and not warnings, warnings=warnings, errors=errors)

    def _validate_profile_patterns(self, joined: str, profile: StyleProfile, warnings: list[str]) -> None:
        setup_keywords = profile.preferred_keywords.get("setup", [])
        if setup_keywords and "[Setup]" in joined and not any(keyword in joined for keyword in setup_keywords):
            warnings.append(f"Setup does not use preferred profile keywords: {setup_keywords}")

        teardown_keywords = profile.preferred_keywords.get("teardown", [])
        if teardown_keywords and "[Teardown]" in joined and not any(keyword in joined for keyword in teardown_keywords):
            warnings.append(f"Teardown does not use preferred profile keywords: {teardown_keywords}")

        for item in profile.negative_patterns:
            pattern = item.get("pattern", "")
            if pattern and pattern in joined:
                warnings.append(item.get("message", f"Negative pattern found: {pattern}"))
