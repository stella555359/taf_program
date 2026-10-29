"""Static validator for generated Robot Framework snippets."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from robotws_mcp.layer2.query import Layer2QueryService
from robotws_mcp.layer6.models import CheckedKeyword, ValidationReport
from robotws_mcp.profiles.store import ProfileStore
from robotws_mcp.validation.style_validator import StyleValidator


DIRECT_TAF_KEYWORDS = {
    "require ue",
    "attach ue",
    "detach ue",
    "start data transfer",
    "stop data transfer",
    "verify average throughput",
    "verify average throughput with deviation",
}

ROBOT_BUILTINS = {
    "comment",
    "create dictionary",
    "create list",
    "log",
    "log many",
    "log to console",
    "run keyword",
    "run keyword and continue on failure",
    "run keyword and ignore error",
    "run keyword and return status",
    "run keyword if",
    "run keywords",
    "set test variable",
    "set variable",
    "set variable if",
    "should be true",
    "sleep",
}


class GeneratedRobotValidator:
    """Validate generated Robot text against profile, graph, and cleanup rules."""

    def __init__(
        self,
        layer2_db_path: str | Path,
        profile_store: ProfileStore | None = None,
        feedback_service: Any | None = None,
    ) -> None:
        self.layer2_query = Layer2QueryService(layer2_db_path)
        self.profile_store = profile_store or ProfileStore()
        self.style_validator = StyleValidator()
        self.feedback_service = feedback_service

    def validate(self, robot_text: str, profile: str = "Hangzhou_SG6_Common", requirement: str = "") -> ValidationReport:
        style_profile = self.profile_store.effective(profile) or self.profile_store.get(profile)
        style = self.style_validator.validate(robot_text, style_profile).to_dict()
        errors = list(style["errors"])
        warnings = list(style["warnings"])
        suggestions: list[str] = []
        metadata: dict[str, Any] = {"style": style, "profile": profile}

        parse_error = self._parse_error(robot_text)
        if parse_error:
            errors.append(parse_error)

        if style_profile:
            for pattern in style_profile.hard_exclude_patterns:
                if pattern and pattern in robot_text:
                    errors.append(f"Forbidden resource pattern found: {pattern}")
            for item in style_profile.negative_patterns:
                pattern = item.get("pattern", "")
                if pattern and pattern in robot_text:
                    errors.append(item.get("message", f"Forbidden pattern found: {pattern}"))

        checked = self._check_keywords(robot_text, style_profile.area if style_profile else "", profile)
        for item in checked:
            if item.status == "denied":
                errors.append(item.reason)
            elif item.status == "warning":
                warnings.append(item.reason)

        cleanup_warnings = self._cleanup_warnings(robot_text, requirement)
        warnings.extend(cleanup_warnings)
        if cleanup_warnings:
            suggestions.append("Add explicit stop traffic and detach cleanup for L3 call workflows.")

        feedback_warning = self._feedback_warning(checked, profile)
        if feedback_warning:
            warnings.append(feedback_warning)

        decision = "deny" if errors else "warn" if warnings else "allow"
        return ValidationReport(
            passed=not errors and not warnings,
            decision=decision,
            errors=_dedupe(errors),
            warnings=_dedupe(warnings),
            suggestions=_dedupe(suggestions),
            checked_keywords=checked,
            metadata=metadata,
        )

    def _parse_error(self, robot_text: str) -> str:
        try:
            from robot.api.parsing import get_model

            source = robot_text
            if "***" not in robot_text:
                source = "*** Test Cases ***\n" + robot_text
            get_model(source)
        except OSError:
            # Some Robot Framework versions treat a raw source string as a path.
            # Other deterministic validators below still handle snippet checks.
            return ""
        except Exception as error:
            return f"Robot Framework parser error: {error}"
        return ""

    def _check_keywords(self, robot_text: str, expected_domain: str, profile: str) -> list[CheckedKeyword]:
        checked: list[CheckedKeyword] = []
        for keyword in _extract_called_keywords(robot_text):
            normalized = keyword.lower()
            if normalized in ROBOT_BUILTINS:
                checked.append(CheckedKeyword(keyword=keyword, status="allowed", reason="known Robot built-in/control keyword"))
                continue
            if normalized in DIRECT_TAF_KEYWORDS:
                checked.append(CheckedKeyword(keyword=keyword, status="allowed", reason="allowed direct TAF keyword"))
                continue
            node = self._find_keyword_node(keyword)
            if not node:
                checked.append(CheckedKeyword(keyword=keyword, status="warning", reason=f"Unknown keyword: {keyword}"))
                continue
            if not node.get("is_allowed"):
                checked.append(
                    CheckedKeyword(
                        keyword=keyword,
                        status="denied",
                        reason=f"Keyword is outside allowed boundary: {keyword}",
                        evidence=node,
                    )
                )
                continue
            node_domain = str(node.get("domain", ""))
            if expected_domain and node_domain not in {expected_domain, "Common"}:
                checked.append(
                    CheckedKeyword(
                        keyword=keyword,
                        status="denied",
                        reason=f"Keyword domain mismatch for {profile}: {keyword} is {node_domain}",
                        evidence=node,
                    )
                )
                continue
            checked.append(CheckedKeyword(keyword=keyword, status="allowed", reason="matched allowed Layer 2 keyword", evidence=node))
        return checked

    def _find_keyword_node(self, keyword: str) -> dict[str, Any] | None:
        matches = self.layer2_query.store.nodes(node_type="keyword", query=keyword, limit=20)
        for match in matches:
            if str(match.get("name", "")).lower() == keyword.lower():
                return match
        return None

    def _cleanup_warnings(self, robot_text: str, requirement: str) -> list[str]:
        lower = f"{requirement}\n{robot_text}".lower()
        if "l3" not in lower and "traffic" not in lower:
            return []
        warnings: list[str] = []
        if "stop data transfer" not in lower and "stop traffic" not in lower:
            warnings.append("L3/traffic workflow is missing explicit stop traffic cleanup.")
        if "detach ue" not in lower and "ue detach" not in lower and "detach" not in lower:
            warnings.append("L3/traffic workflow is missing explicit UE detach cleanup.")
        return warnings

    def _feedback_warning(self, checked: list[CheckedKeyword], profile: str) -> str:
        if not self.feedback_service:
            return ""
        failing = []
        for item in checked:
            hints = self.feedback_service.get_feedback_hints(item.keyword, profile=profile)
            if hints.get("has_failures"):
                failing.append(item.keyword)
        if failing:
            return "Execution feedback has previous failures for: " + ", ".join(_dedupe(failing))
        return ""


def _extract_called_keywords(robot_text: str) -> list[str]:
    keywords: list[str] = []
    for raw_line in robot_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("..."):
            continue
        if not line.startswith((" ", "\t")):
            continue
        cells = [cell for cell in re.split(r"\s{2,}|\t+", stripped) if cell]
        if not cells:
            continue
        first = cells[0]
        if first.startswith("[") and first.endswith("]"):
            if first.lower() in {"[setup]", "[teardown]"} and len(cells) > 1:
                keywords.append(cells[1])
            continue
        if first.startswith(("${", "@{", "&{")) and len(cells) > 1:
            keywords.append(cells[1])
        else:
            keywords.append(first)
    return _dedupe(keywords)


def _dedupe(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item not in result:
            result.append(item)
    return result

