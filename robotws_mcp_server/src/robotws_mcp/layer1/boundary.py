"""Boundary classification for Layer 1 v2 records."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath

from robotws_mcp.models import StyleProfile, normalize_path


DOMAINS = {"RRM", "SISO", "OAM"}


@dataclass(frozen=True)
class BoundaryDecision:
    domain: str = "Unknown"
    is_allowed: bool = False
    allowed_source: str = ""
    exclude_reason: str = ""
    site: str = "Unknown"
    case_type: str = "Unknown"
    feature: str | None = None


def classify_path(path: str, profile: StyleProfile | None, record_type: str = "") -> BoundaryDecision:
    """Classify a source path against the active profile boundary."""

    normalized = normalize_path(path)
    lower = normalized.lower()
    site = _site(normalized)
    domain, feature = _domain_feature(normalized)
    case_type = _case_type(feature, record_type)

    if not profile:
        return BoundaryDecision(
            domain=domain,
            is_allowed=False,
            exclude_reason="profile is unavailable",
            site=site,
            case_type=case_type,
            feature=feature,
        )

    if _starts_with_any(lower, profile.allowed_resource_scopes):
        if record_type == "testcase":
            return BoundaryDecision(
                domain="Common",
                is_allowed=False,
                exclude_reason="testcase under allowed resource scope is not a generation testcase",
                site=site,
                case_type="Resource",
                feature=None,
            )
        return BoundaryDecision(
            domain="Common",
            is_allowed=True,
            allowed_source="allowed_resource_scope",
            site=site,
            case_type="Resource",
            feature=None,
        )

    if _starts_with_any(lower, profile.confirmed_case_scopes):
        return BoundaryDecision(
            domain=domain,
            is_allowed=True,
            allowed_source="confirmed_case_scope",
            site=site,
            case_type=case_type,
            feature=feature,
        )

    if domain in profile.feature_allowlist and feature in profile.feature_allowlist.get(domain, []):
        return BoundaryDecision(
            domain=domain,
            is_allowed=True,
            allowed_source="feature_allowlist",
            site=site,
            case_type=case_type,
            feature=feature,
        )

    reason = "path is outside allowed boundary"
    if domain in profile.feature_allowlist and feature:
        reason = "feature is not in active feature_allowlist"
    elif domain == "Unknown":
        reason = "cannot infer domain from path"
    return BoundaryDecision(
        domain=domain,
        is_allowed=False,
        exclude_reason=reason,
        site=site,
        case_type=case_type,
        feature=feature,
    )


def apply_boundary(record: object, decision: BoundaryDecision) -> None:
    """Apply a boundary decision to a mutable record dataclass."""

    for name, value in decision.__dict__.items():
        if hasattr(record, name):
            setattr(record, name, value)


def _starts_with_any(path_lower: str, scopes: list[str]) -> bool:
    return any(path_lower.startswith(normalize_path(scope).lower()) for scope in scopes)


def _site(path: str) -> str:
    parts = PurePosixPath(path).parts
    if "testsuite" in parts:
        idx = parts.index("testsuite")
        if len(parts) > idx + 1:
            return parts[idx + 1]
    return "Unknown"


def _domain_feature(path: str) -> tuple[str, str | None]:
    parts = PurePosixPath(path).parts
    for idx, part in enumerate(parts):
        if part in DOMAINS:
            feature = None
            if "RAN_PZ_HAZ_34" in parts[idx:]:
                marker_idx = parts.index("RAN_PZ_HAZ_34", idx)
                if len(parts) > marker_idx + 1:
                    feature = parts[marker_idx + 1]
            return part, feature
    return "Unknown", None


def _case_type(feature: str | None, record_type: str) -> str:
    if record_type in {"resource_import", "library_import", "variable", "python_symbol"}:
        return "Resource"
    if feature and feature.lower() == "none_feature_sg6":
        return "TMO"
    if feature:
        return "Feature"
    return "Unknown"
