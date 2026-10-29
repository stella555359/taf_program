"""SG6 feature ownership discovery."""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import PurePosixPath

from robotws_mcp.models import DiscoveryReport, FeatureOwnership, RobotFile, StyleProfile, normalize_path

SG_TOKEN_RE = re.compile(r"(^|[^A-Za-z0-9])(?:MMW_)?SG_?0*(?P<number>\d+)(?=$|[^A-Za-z0-9])", re.IGNORECASE)


@dataclass
class FeatureBucket:
    area: str
    feature: str
    path: str
    files: list[RobotFile] = field(default_factory=list)


class FeatureOwnershipDiscoverer:
    """Classify RobotWS feature folders for SG6 indexing."""

    def __init__(self, profile: StyleProfile) -> None:
        self.profile = profile

    def discover(self, robot_files: list[RobotFile]) -> DiscoveryReport:
        buckets = self._group_feature_files(robot_files)
        features = [self._classify_bucket(bucket) for bucket in sorted(buckets.values(), key=lambda item: item.path)]
        summary: dict[str, int] = defaultdict(int)
        for feature in features:
            if feature.status == "confirmed" and feature.source == "allowlist":
                summary["confirmed_by_allowlist"] += 1
            elif feature.status == "confirmed" and feature.source == "none_feature_path":
                summary["confirmed_by_none_feature_path"] += 1
            elif feature.status == "excluded":
                if feature.source == "hard_exclude":
                    summary["excluded_by_hard_exclude"] += 1
                elif feature.source == "not_in_allowlist":
                    summary["excluded_by_not_in_allowlist"] += 1
                else:
                    summary["excluded"] += 1
        return DiscoveryReport(summary=dict(summary), features=features)

    def is_indexable_path(self, path: str, report: DiscoveryReport | None = None) -> bool:
        normalized = normalize_path(path).lower()
        if any(normalized.startswith(normalize_path(scope).lower()) for scope in self.profile.allowed_resource_scopes):
            return True
        if not report:
            return True
        for feature in report.features:
            feature_path = normalize_path(feature.path).lower()
            if normalized.startswith(feature_path):
                return feature.status == "confirmed"
        return False

    def _group_feature_files(self, robot_files: list[RobotFile]) -> dict[tuple[str, str], FeatureBucket]:
        buckets: dict[tuple[str, str], FeatureBucket] = {}
        for robot_file in robot_files:
            area_feature = self._extract_area_feature(robot_file.path)
            if not area_feature:
                continue
            area, feature, feature_path = area_feature
            key = (area, feature)
            if key not in buckets:
                buckets[key] = FeatureBucket(area=area, feature=feature, path=feature_path)
            buckets[key].files.append(robot_file)
        return buckets

    def _extract_area_feature(self, path: str) -> tuple[str, str, str] | None:
        parts = PurePosixPath(normalize_path(path)).parts
        for area in ("RRM", "SISO"):
            marker = ("testsuite", "Hangzhou", area, "RAN_PZ_HAZ_34")
            marker_len = len(marker)
            for idx in range(0, len(parts) - marker_len):
                if parts[idx : idx + marker_len] == marker and len(parts) > idx + marker_len:
                    feature = parts[idx + marker_len]
                    feature_path = "/".join(parts[: idx + marker_len + 1])
                    return area, feature, feature_path
        return None

    def _classify_bucket(self, bucket: FeatureBucket) -> FeatureOwnership:
        resource_imports = self._resource_imports(bucket)
        tags = self._tags(bucket)
        case_count = sum(len(robot_file.cases) for robot_file in bucket.files)

        if self._is_allowlisted(bucket):
            source = "none_feature_path" if self._is_none_feature(bucket) else "allowlist"
            return FeatureOwnership(
                area=bucket.area,
                feature=bucket.feature,
                path=bucket.path,
                status="confirmed",
                source=source,
                case_count=case_count,
                resource_imports=resource_imports,
            )

        exclude_reason = self._hard_exclude_reason(bucket, tags, resource_imports)
        source = "hard_exclude" if exclude_reason else "not_in_allowlist"
        reason = exclude_reason or "feature is not in SG6 allowlist"

        return FeatureOwnership(
            area=bucket.area,
            feature=bucket.feature,
            path=bucket.path,
            status="excluded",
            source=source,
            case_count=case_count,
            resource_imports=resource_imports,
            exclude_reason=reason,
        )

    def _is_allowlisted(self, bucket: FeatureBucket) -> bool:
        return bucket.feature in self.profile.feature_allowlist.get(bucket.area, [])

    def _is_none_feature(self, bucket: FeatureBucket) -> bool:
        return bucket.feature.lower() == "none_feature_sg6"

    def _resource_imports(self, bucket: FeatureBucket) -> list[str]:
        imports: set[str] = set()
        for robot_file in bucket.files:
            for resource in robot_file.resources:
                imports.add(normalize_path(resource.resource))
        return sorted(imports)

    def _tags(self, bucket: FeatureBucket) -> list[str]:
        tags: set[str] = set()
        for robot_file in bucket.files:
            tags.update(robot_file.force_tags)
            for case in robot_file.cases:
                tags.update(case.tags)
        return sorted(tags)

    def _hard_exclude_reason(self, bucket: FeatureBucket, tags: list[str], resource_imports: list[str]) -> str:
        feature_reason = self._other_sg_token_reason(bucket.feature, "feature path")
        if feature_reason:
            return feature_reason
        path_reason = self._other_sg_token_reason(bucket.path, "feature path")
        if path_reason:
            return path_reason
        for tag in tags:
            tag_reason = self._other_sg_token_reason(tag, "tag")
            if tag_reason:
                return tag_reason
        for resource in resource_imports:
            resource_reason = self._other_sg_token_reason(resource, "resource import")
            if resource_reason:
                return resource_reason
        return ""

    def _other_sg_token_reason(self, text: str, source: str) -> str:
        normalized = normalize_path(text)
        for match in SG_TOKEN_RE.finditer(normalized):
            number = int(match.group("number"))
            if number != 6:
                token = match.group(0).strip("/\\_- ")
                return f"{source} matches other SG token: {token or match.group(0)}"
        return ""
