"""Generation context assembly for Cursor."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from robotws_mcp.models import StyleProfile
from robotws_mcp.profiles.store import ProfileStore
from robotws_mcp.storage.sqlite_store import SQLiteStore


@dataclass
class GenerationContextRequest:
    requirement: str
    path_hint: str = ""
    profile_hint: str = ""
    limit: int = 5


class ContextBuilder:
    """Build structured context that Cursor LLM can use for generation."""

    def __init__(
        self,
        db_path: str | Path = "data/indexes/robotws.sqlite3",
        profile_store: ProfileStore | None = None,
    ) -> None:
        self.db_path = Path(db_path)
        self.discovery_report_path = self.db_path.with_name("sg6_discovery_report.json")
        self.store = SQLiteStore(self.db_path)
        self.profile_store = profile_store or ProfileStore()

    def identify_profile(self, path_hint: str = "", requirement: str = "", profile_hint: str = "") -> StyleProfile | None:
        if profile_hint:
            profile = self.profile_store.get(profile_hint)
            if profile:
                return profile
        return self.profile_store.identify(path_hint=path_hint, requirement=requirement)

    def build_generation_context(self, request: GenerationContextRequest) -> dict[str, Any]:
        profile = self.identify_profile(
            path_hint=request.path_hint,
            requirement=request.requirement,
            profile_hint=request.profile_hint,
        )
        case_paths = self._case_search_paths(profile)
        keyword_paths = self._keyword_search_paths(profile)
        generation_profile = self._generation_profile(profile)

        similar_cases = self.store.search_cases(request.requirement, profile_paths=case_paths, limit=request.limit)
        recommended_keywords = self._recommended_keywords(generation_profile, request.requirement)
        keyword_examples = self._keyword_examples(recommended_keywords, keyword_paths, limit=3)
        setup_teardown = self._setup_teardown(generation_profile, similar_cases)
        skeleton = self._build_skeleton(generation_profile, recommended_keywords, setup_teardown)
        discovery_report = self.get_sg6_discovery_report()

        return {
            "mode": "context_only",
            "profile": profile.to_dict() if profile else None,
            "requirement": request.requirement,
            "sg6_ownership": self._ownership_summary(discovery_report, request.limit),
            "similar_cases": similar_cases,
            "recommended_keywords": recommended_keywords,
            "keyword_examples": keyword_examples,
            "setup_teardown_pattern": setup_teardown,
            "style_rules": self._merged_style_rules(profile, generation_profile),
            "negative_patterns": self._merged_negative_patterns(profile, generation_profile),
            "required_user_inputs": self._required_user_inputs(request.requirement, generation_profile),
            "generation_skeleton": skeleton,
            "unresolved_assumptions": [
                "Confirm target testline tags.",
                "Confirm UE mapping variable or UE index.",
                "Confirm KPI/traffic model and duration.",
            ],
        }

    def search_cases(self, query: str, profile: str = "", limit: int = 10) -> list[dict[str, Any]]:
        style_profile = self.profile_store.get(profile) if profile else None
        return self.store.search_cases(query, self._case_search_paths(style_profile), limit)

    def search_keywords(self, query: str, profile: str = "", limit: int = 10) -> list[dict[str, Any]]:
        style_profile = self.profile_store.get(profile) if profile else None
        return self.store.search_keywords(query, self._keyword_search_paths(style_profile), limit)

    def get_case_pattern(self, case_name_or_path: str) -> dict[str, Any] | None:
        return self.store.get_case(case_name_or_path)

    def trace_keyword_usage(self, keyword_name: str, depth: int = 2) -> list[dict[str, Any]]:
        return self.store.trace_keyword(keyword_name, depth=depth)

    def find_taf_library_usage(self, library_name: str, profile: str = "") -> list[dict[str, Any]]:
        style_profile = self.profile_store.get(profile) if profile else None
        return self.store.find_library_usage(library_name, style_profile.path_scopes if style_profile else None)

    def get_style_profile(self, profile: str) -> dict[str, Any] | None:
        style_profile = self.profile_store.effective(profile)
        return style_profile.to_dict() if style_profile else None

    def get_sg6_discovery_report(self) -> dict[str, Any]:
        if not self.discovery_report_path.exists():
            return {
                "summary": {},
                "features": [],
                "message": f"Discovery report not found: {self.discovery_report_path}",
            }
        return json.loads(self.discovery_report_path.read_text(encoding="utf-8"))

    def _generation_profile(self, profile: StyleProfile | None) -> StyleProfile | None:
        if profile:
            return self.profile_store.effective(profile.name) or profile
        return self.profile_store.get("Hangzhou_SG6_Common") or profile

    def _case_search_paths(self, profile: StyleProfile | None) -> list[str] | None:
        common = self.profile_store.get("Hangzhou_SG6_Common")
        if not common:
            return profile.path_scopes if profile else None
        paths = self._allowlist_paths(common)
        if not profile:
            return paths
        if profile.area:
            paths = [path for path in paths if f"/{profile.area}/" in f"/{path}/"]
        if profile.case_type == "TMO":
            paths = [path for path in paths if path.lower().endswith("/none_feature_sg6")]
        elif profile.case_type == "Feature":
            paths = [path for path in paths if not path.lower().endswith("/none_feature_sg6")]
        return paths

    def _keyword_search_paths(self, profile: StyleProfile | None) -> list[str] | None:
        common = self.profile_store.get("Hangzhou_SG6_Common")
        if not common:
            return profile.path_scopes if profile else None
        case_paths = self._case_search_paths(profile) or []
        return [*case_paths, *common.allowed_resource_scopes]

    def _allowlist_paths(self, profile: StyleProfile) -> list[str]:
        paths: list[str] = []
        for area, features in profile.feature_allowlist.items():
            for feature in features:
                paths.append(f"testsuite/Hangzhou/{area}/RAN_PZ_HAZ_34/{feature}")
        return paths

    def _merged_style_rules(
        self,
        profile: StyleProfile | None,
        generation_profile: StyleProfile | None,
    ) -> list[str]:
        rules: list[str] = []
        for item in (generation_profile, profile):
            if item:
                rules.extend(rule for rule in item.style_rules if rule not in rules)
        return rules

    def _merged_negative_patterns(
        self,
        profile: StyleProfile | None,
        generation_profile: StyleProfile | None,
    ) -> list[dict[str, str]]:
        patterns: list[dict[str, str]] = []
        seen: set[tuple[str, str]] = set()
        for item in (generation_profile, profile):
            if not item:
                continue
            for pattern in item.negative_patterns:
                key = (pattern.get("pattern", ""), pattern.get("message", ""))
                if key not in seen:
                    seen.add(key)
                    patterns.append(pattern)
        return patterns

    def _ownership_summary(self, report: dict[str, Any], limit: int) -> dict[str, Any]:
        features = report.get("features", [])
        return {
            "summary": report.get("summary", {}),
            "confirmed_features": [
                item for item in features if item.get("status") == "confirmed"
            ][:limit],
            "excluded_features": [
                item for item in features if item.get("status") == "excluded"
            ][:limit],
        }

    def _recommended_keywords(self, profile: StyleProfile | None, requirement: str) -> dict[str, list[str]]:
        if not profile:
            return {}
        requirement_lower = requirement.lower()
        selected: dict[str, list[str]] = {}
        for category, keywords in profile.preferred_keywords.items():
            if category in requirement_lower or any(token in requirement_lower for token in self._category_tokens(category)):
                selected[category] = keywords
        if not selected:
            selected = {
                "setup": profile.preferred_keywords.get("setup", []),
                "teardown": profile.preferred_keywords.get("teardown", []),
            }
        return selected

    def _keyword_examples(
        self,
        recommended_keywords: dict[str, list[str]],
        profile_paths: list[str] | None,
        limit: int,
    ) -> dict[str, list[dict[str, Any]]]:
        examples: dict[str, list[dict[str, Any]]] = {}
        for keywords in recommended_keywords.values():
            for keyword in keywords:
                matches = self.store.search_keywords(keyword, profile_paths=profile_paths, limit=limit)
                if matches:
                    examples[keyword] = matches
        return examples

    def _setup_teardown(
        self,
        profile: StyleProfile | None,
        similar_cases: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        if not profile:
            return {}
        if profile.case_type == "Feature":
            reference_cases = self._case_setup_teardown_references(similar_cases or [])
            return {
                "setup": ["TODO_SELECT_FEATURE_LOCAL_SETUP"],
                "teardown": ["TODO_SELECT_FEATURE_LOCAL_TEARDOWN"],
                "reference_cases": reference_cases,
                "strategy": [
                    "Feature skeleton keeps setup/teardown as TODO placeholders.",
                    "Cursor should choose or compose feature-local setup/teardown from reference_cases and retrieved Resources.",
                    "Do not copy setup from one case and teardown from another case unless the user explicitly confirms it.",
                ],
            }
        return {
            "setup": profile.preferred_keywords.get("setup", []),
            "teardown": profile.preferred_keywords.get("teardown", []),
        }

    def _case_setup_teardown_references(self, cases: list[dict[str, Any]]) -> list[dict[str, str]]:
        references: list[dict[str, str]] = []
        seen: set[tuple[str, str, str]] = set()
        for case in cases:
            setup = case.get("setup")
            teardown = case.get("teardown")
            if setup and teardown:
                reference = {
                    "name": str(case.get("name", "")),
                    "path": str(case.get("path", "")),
                    "setup": str(setup),
                    "teardown": str(teardown),
                }
                key = (reference["name"], reference["setup"], reference["teardown"])
                if key not in seen:
                    seen.add(key)
                    references.append(reference)
            if len(references) >= 3:
                break
        return references

    def _build_skeleton(
        self,
        profile: StyleProfile | None,
        recommended_keywords: dict[str, list[str]],
        setup_teardown: dict[str, Any],
    ) -> str:
        setup = ""
        teardown = ""
        if profile:
            setup = next(iter(setup_teardown.get("setup", [])), "")
            teardown = next(iter(setup_teardown.get("teardown", [])), "")
        lines = [
            "New_Testcase_Name",
            "    [Documentation]    TODO: add author and testcase purpose.",
            "    [Tags]    TODO_TESTLINE",
        ]
        if setup:
            lines.append(f"    [Setup]    {setup}")
        for category, keywords in recommended_keywords.items():
            if category in {"setup", "teardown"}:
                continue
            lines.append(f"    # {category}")
            for keyword in keywords[:3]:
                lines.append(f"    {keyword}    TODO")
        if teardown:
            if teardown.startswith("TODO_"):
                lines.append(f"    [Teardown]    {teardown}")
            else:
                lines.append(f"    [Teardown]    Run Keyword And Continue On Failure    {teardown}")
        return "\n".join(lines)

    def _required_user_inputs(self, requirement: str, profile: StyleProfile | None) -> list[str]:
        required = ["testcase id/name", "target testline"]
        requirement_lower = requirement.lower()
        if any(token in requirement_lower for token in ("ue", "attach", "traffic", "sftp", "burst")):
            required.append("UE index or group mapping variable")
        if any(token in requirement_lower for token in ("pa", "attenuator", "ru")):
            required.append("PA/RU mapping or existing profile mapping variable")
        if "kpi" in requirement_lower:
            required.append("KPI report model description and expected duration")
        if profile:
            required.extend(f"profile required field: {item}" for item in profile.required_fields)
        return required

    def _category_tokens(self, category: str) -> list[str]:
        return {
            "coam": ["cellbarred", "gnb", "oam", "cell"],
            "pa": ["attenuator", "ru", "power", "rsrp"],
            "kpi": ["report", "compass", "scout"],
            "evidence": ["pcap", "wireshark", "syslog", "snapshot", "log"],
            "ue": ["attach", "detach", "sftp", "burst", "dingli", "spark"],
        }.get(category, [])
