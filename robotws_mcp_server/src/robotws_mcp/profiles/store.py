"""Profile loading and identification."""

from __future__ import annotations

import json
from pathlib import Path

from robotws_mcp.models import StyleProfile, normalize_path


DEFAULT_PROFILE_DIR = Path(__file__).resolve().parents[3] / "config" / "profiles"


class ProfileStore:
    """Load and identify RobotWS style profiles."""

    def __init__(self, profile_dir: str | Path | None = None) -> None:
        self.profile_dir = Path(profile_dir) if profile_dir else DEFAULT_PROFILE_DIR
        self._profiles: dict[str, StyleProfile] | None = None

    def all(self) -> list[StyleProfile]:
        if self._profiles is None:
            self._profiles = self._load_profiles()
        return list(self._profiles.values())

    def get(self, name: str) -> StyleProfile | None:
        if self._profiles is None:
            self._profiles = self._load_profiles()
        return self._profiles.get(name)

    def effective(self, name: str) -> StyleProfile | None:
        profile = self.get(name)
        if not profile or profile.name == "Hangzhou_SG6_Common":
            return profile
        common = self.get("Hangzhou_SG6_Common")
        if not common:
            return profile
        return StyleProfile(
            name=profile.name,
            description=profile.description,
            path_scopes=profile.path_scopes,
            preferred_keywords=self._merge_keyword_groups(common.preferred_keywords, profile.preferred_keywords),
            negative_patterns=self._merge_patterns(common.negative_patterns, profile.negative_patterns),
            style_rules=self._merge_strings(common.style_rules, profile.style_rules),
            required_fields=self._merge_strings(common.required_fields, profile.required_fields),
            profile_type=profile.profile_type,
            area=profile.area,
            case_type=profile.case_type,
            case_candidate_scopes=profile.case_candidate_scopes or common.case_candidate_scopes,
            confirmed_case_scopes=profile.confirmed_case_scopes or common.confirmed_case_scopes,
            allowed_resource_scopes=profile.allowed_resource_scopes or common.allowed_resource_scopes,
            feature_allowlist=profile.feature_allowlist or common.feature_allowlist,
            hard_exclude_patterns=profile.hard_exclude_patterns or common.hard_exclude_patterns,
        )

    def identify(self, path_hint: str = "", requirement: str = "") -> StyleProfile | None:
        path = normalize_path(path_hint).lower() if path_hint else ""
        requirement_lower = requirement.lower()
        best: tuple[int, StyleProfile] | None = None
        for profile in self.all():
            score = 0
            for scope in profile.path_scopes:
                normalized_scope = normalize_path(scope).lower()
                if path and normalized_scope in path:
                    score += 10
                for part in normalized_scope.split("/"):
                    if part and part.lower() in requirement_lower:
                        score += 1
            for token in profile.name.lower().split("_"):
                if token and token in requirement_lower:
                    score += 2
            if best is None or score > best[0]:
                best = (score, profile)
        return best[1] if best and best[0] > 0 else None

    def _merge_strings(self, first: list[str], second: list[str]) -> list[str]:
        merged: list[str] = []
        for item in [*first, *second]:
            if item not in merged:
                merged.append(item)
        return merged

    def _merge_patterns(self, first: list[dict[str, str]], second: list[dict[str, str]]) -> list[dict[str, str]]:
        merged: list[dict[str, str]] = []
        seen: set[tuple[str, str]] = set()
        for item in [*first, *second]:
            key = (item.get("pattern", ""), item.get("message", ""))
            if key not in seen:
                seen.add(key)
                merged.append(item)
        return merged

    def _load_profiles(self) -> dict[str, StyleProfile]:
        profiles: dict[str, StyleProfile] = {}
        if not self.profile_dir.exists():
            return profiles
        for path in sorted(self.profile_dir.glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            profile = StyleProfile(
                name=data["name"],
                description=data.get("description", ""),
                path_scopes=data.get("path_scopes", []),
                preferred_keywords=data.get("preferred_keywords", {}),
                negative_patterns=data.get("negative_patterns", []),
                style_rules=data.get("style_rules", []),
                required_fields=data.get("required_fields", []),
                profile_type=data.get("profile_type", "style"),
                area=data.get("area"),
                case_type=data.get("case_type"),
                case_candidate_scopes=data.get("case_candidate_scopes", []),
                confirmed_case_scopes=data.get("confirmed_case_scopes", []),
                allowed_resource_scopes=data.get("allowed_resource_scopes", []),
                feature_allowlist=data.get("feature_allowlist", {}),
                hard_exclude_patterns=data.get("hard_exclude_patterns", []),
            )
            profiles[profile.name] = profile
        return profiles

    def _merge_keyword_groups(
        self,
        common_keywords: dict[str, list[str]],
        profile_keywords: dict[str, list[str]],
    ) -> dict[str, list[str]]:
        merged = dict(common_keywords)
        for category, keywords in profile_keywords.items():
            merged[category] = keywords
        return merged
