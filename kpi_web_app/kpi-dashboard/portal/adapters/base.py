from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..contracts import JobContract, ModuleCapabilityContract, SummaryContract


@dataclass(frozen=True)
class ModuleRepository:
    key: str
    title: str
    summary: str
    route_name: str
    repo_path: Path
    readme_path: Path
    entry_candidates: List[Path]


class BaseModuleAdapter:
    display_timezone = timezone(timedelta(hours=8), name='CST')

    def __init__(self, repository: ModuleRepository):
        self.repository = repository

    def _parse_display_timestamp(self, value: object) -> Optional[datetime]:
        from ..services.job_store import parse_utc_text

        text = str(value or '').strip()
        if not text:
            return None

        parsed_utc = parse_utc_text(text)
        if parsed_utc is not None:
            return parsed_utc.astimezone(self.display_timezone)

        try:
            parsed = datetime.fromisoformat(text)
        except ValueError:
            return None

        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=self.display_timezone)
        return parsed.astimezone(self.display_timezone)

    def _format_display_timestamp_text(self, value: object) -> Optional[str]:
        parsed = self._parse_display_timestamp(value)
        if parsed is None:
            return str(value or '').strip() or None
        return parsed.strftime('%Y-%m-%d %H:%M:%S CST')

    def _format_timestamp_payload(self, value: object) -> object:
        if isinstance(value, dict):
            formatted: Dict[str, object] = {}
            for key, item in value.items():
                if key in {
                    'created_at',
                    'updated_at',
                    'started_at',
                    'completed_at',
                    'first_created_at',
                    'last_created_at',
                    'progress_updated_at',
                }:
                    formatted[key] = self._format_display_timestamp_text(item) or item
                else:
                    formatted[key] = self._format_timestamp_payload(item)
            return formatted
        if isinstance(value, list):
            return [self._format_timestamp_payload(item) for item in value]
        return value

    def _format_platform_events(self, events: object) -> object:
        if not isinstance(events, list):
            return events
        formatted_events: List[Dict[str, object]] = []
        for event in events:
            if not isinstance(event, dict):
                formatted_events.append(event)
                continue
            formatted_event = dict(event)
            formatted_event['created_at'] = self._format_display_timestamp_text(event.get('created_at')) or event.get('created_at')
            formatted_event['payload'] = self._format_timestamp_payload(event.get('payload') or {})
            formatted_events.append(formatted_event)
        return formatted_events

    def _format_platform_artifacts(self, artifacts: object) -> object:
        if not isinstance(artifacts, list):
            return artifacts
        formatted_artifacts: List[Dict[str, object]] = []
        for artifact in artifacts:
            if not isinstance(artifact, dict):
                formatted_artifacts.append(artifact)
                continue
            formatted_artifact = dict(artifact)
            if 'created_at' in formatted_artifact:
                formatted_artifact['created_at'] = self._format_display_timestamp_text(artifact.get('created_at')) or artifact.get('created_at')
            formatted_artifact['payload'] = self._format_timestamp_payload(artifact.get('payload') or {})
            formatted_artifacts.append(formatted_artifact)
        return formatted_artifacts

    def capability_contract(self) -> ModuleCapabilityContract:
        return ModuleCapabilityContract(
            supports_cancel=False,
            supports_delete=True,
            supports_rerun=False,
            supports_preview=False,
            supports_auto_trigger=False,
            supports_status_api=True,
        )

    def job_contract(self) -> JobContract:
        return JobContract(
            module_key=self.repository.key,
            statuses=['queued', 'running', 'completed', 'failed'],
            artifact_kinds=[],
            progress_fields=['progress_stage', 'progress_message', 'progress_updated_at'],
            linked_job_fields=[],
        )

    def summary_contract(self) -> SummaryContract:
        return SummaryContract(
            result_payload_key='summary',
            summary_fields=['summary'],
            ui_fields=['status', 'created_at', 'completed_at'],
        )

    def describe_module(self) -> Dict[str, object]:
        available_entries = []
        for path in self.repository.entry_candidates:
            if not path.exists():
                continue
            try:
                entry_text = str(path.relative_to(self.repository.repo_path)).replace('\\', '/')
            except ValueError:
                entry_text = str(path)
            available_entries.append(entry_text)
        return {
            'key': self.repository.key,
            'title': self.repository.title,
            'summary': self.repository.summary,
            'repo_path': str(self.repository.repo_path),
            'readme_exists': self.repository.readme_path.exists(),
            'repo_exists': self.repository.repo_path.exists(),
            'available_entries': available_entries,
            'integration_mode': 'local-cli-adapter',
            'capabilities': self.capability_contract().to_dict(),
            'job_contract': self.job_contract().to_dict(),
            'summary_contract': self.summary_contract().to_dict(),
        }

    def sample_command(self) -> str:
        raise NotImplementedError

    def artifact_endpoint_kind(self, artifact_kind: str) -> Optional[str]:
        return artifact_kind

    def should_display_platform_event(self, event_type: str) -> bool:
        return event_type in {'status_changed', 'progress_updated', 'linked_job_added', 'error_recorded'}

    def artifact_link_label(self, artifact_kind: str) -> str:
        labels = {
            'request': 'request',
            'result': 'result',
            'stdout': 'stdout',
            'stderr': 'stderr',
            'report': 'report',
            'report_html': 'html',
            'report_excel': 'excel',
            'report_data': 'json',
            'source': 'source',
        }
        return labels.get(artifact_kind, artifact_kind)

    def summarize_platform_events(self, events: List[Dict[str, object]]) -> List[Dict[str, object]]:
        timeline: List[Dict[str, object]] = []
        progress_run: List[Dict[str, object]] = []

        def flush_progress_run() -> None:
            nonlocal progress_run
            if not progress_run:
                return
            first_event = progress_run[0]
            last_event = progress_run[-1]
            first_payload = dict(first_event.get('payload') or {})
            last_payload = dict(last_event.get('payload') or {})
            stage = str(last_payload.get('stage') or first_payload.get('stage') or '').strip() or 'progress'
            first_message = str(first_payload.get('message') or '').strip()
            last_message = str(last_payload.get('message') or '').strip()
            summary_text = last_message or first_message or '-'
            if len(progress_run) > 1 and first_message and first_message != last_message:
                summary_text = f'{first_message} -> {last_message}'
            timeline.append(
                {
                    'event_type': 'progress_updated',
                    'created_at': str(last_event.get('created_at') or ''),
                    'payload': {
                        'stage': stage,
                        'first_message': first_message or None,
                        'last_message': last_message or None,
                        'update_count': len(progress_run),
                        'first_created_at': str(first_event.get('created_at') or ''),
                        'last_created_at': str(last_event.get('created_at') or ''),
                    },
                    'summary_label': stage,
                    'summary_text': summary_text,
                }
            )
            progress_run = []

        for event in events:
            event_type = str(event.get('event_type') or '')
            payload = dict(event.get('payload') or {})
            if event_type == 'progress_updated':
                stage = str(payload.get('stage') or '').strip()
                if progress_run:
                    last_stage = str((progress_run[-1].get('payload') or {}).get('stage') or '').strip()
                    if stage != last_stage:
                        flush_progress_run()
                progress_run.append(event)
                continue

            flush_progress_run()
            summary_label = event_type
            summary_text = '-'
            if event_type == 'status_changed':
                summary_label = str(payload.get('to_status') or payload.get('from_status') or event_type)
                from_status = str(payload.get('from_status') or '').strip()
                to_status = str(payload.get('to_status') or '').strip()
                summary_text = f'{from_status or "-"} -> {to_status or "-"}'
            elif event_type == 'linked_job_added':
                summary_label = str(payload.get('link_kind') or event_type)
                summary_text = f"{payload.get('linked_module_key') or '-'} / {payload.get('linked_job_id') or '-'}"
            elif event_type == 'error_recorded':
                summary_label = 'error'
                summary_text = str(payload.get('message') or '-').strip() or '-'

            timeline.append(
                {
                    **event,
                    'summary_label': summary_label,
                    'summary_text': summary_text,
                }
            )

        flush_progress_run()
        return timeline[-12:]

    def enrich_platform_metadata(self, job: Dict[str, object]) -> Dict[str, object]:
        from ..services.job_store import list_job_artifacts, list_job_events, list_job_links
        from ..services.repo_registry import REPOSITORIES

        job_id = str(job.get('id') or '').strip()
        if not job_id:
            return dict(job)

        decorated = dict(job)
        artifact_endpoint = self.repository.route_name.rsplit('.', 1)[0] + '.artifact'
        platform_artifacts = []
        for artifact in list_job_artifacts(self.repository.key, job_id):
            artifact_kind = str(artifact.get('artifact_kind') or '')
            endpoint_kind = self.artifact_endpoint_kind(artifact_kind)
            is_available = False
            artifact_path = str(artifact.get('artifact_path') or '')
            artifact_path_resolver = getattr(self, 'artifact_path', None)
            if callable(artifact_path_resolver):
                try:
                    is_available = artifact_path_resolver(decorated, endpoint_kind or artifact_kind) is not None
                except Exception:
                    is_available = False
            platform_artifacts.append(
                {
                    **artifact,
                    'artifact_endpoint': artifact_endpoint,
                    'download_endpoint_kind': endpoint_kind,
                    'downloadable': bool(endpoint_kind),
                    'is_available': is_available,
                    'link_label': self.artifact_link_label(artifact_kind),
                    'open_in_new_tab': endpoint_kind == 'html',
                    'requires_version_token': endpoint_kind == 'html',
                    'display_name': str((artifact.get('payload') or {}).get('field_name') or artifact_kind or artifact_path),
                }
            )

        platform_artifacts_by_kind = {
            str(artifact.get('artifact_kind') or ''): artifact
            for artifact in platform_artifacts
        }
        platform_artifacts_by_endpoint_kind = {
            str(artifact.get('download_endpoint_kind') or ''): artifact
            for artifact in platform_artifacts
            if artifact.get('download_endpoint_kind')
        }

        platform_links = []
        for link in list_job_links(self.repository.key, job_id):
            linked_module_key = str(link.get('linked_module_key') or '')
            repository = REPOSITORIES.get(linked_module_key)
            detail_endpoint = None
            if repository is not None:
                detail_endpoint = repository.route_name.rsplit('.', 1)[0] + '.job_detail'
            platform_links.append(
                {
                    **link,
                    'linked_module_title': repository.title if repository is not None else linked_module_key,
                    'detail_endpoint': detail_endpoint,
                }
            )

        platform_events = list_job_events(self.repository.key, job_id)
        display_events = [event for event in platform_events if self.should_display_platform_event(str(event.get('event_type') or ''))]
        recent_event = display_events[-1] if display_events else None

        recent_stage = str(decorated.get('progress_stage') or '').strip()
        recent_message = str(decorated.get('progress_message') or '').strip()
        if recent_event is not None:
            payload = recent_event.get('payload') or {}
            if str(recent_event.get('event_type') or '') == 'progress_updated':
                recent_stage = str(payload.get('stage') or recent_stage or '').strip()
                recent_message = str(payload.get('message') or recent_message or '').strip()
            elif str(recent_event.get('event_type') or '') == 'status_changed':
                recent_stage = str(payload.get('to_status') or recent_stage or decorated.get('status') or '').strip()
                if not recent_message:
                    recent_message = f"Status changed to {recent_stage}." if recent_stage else ''
            elif str(recent_event.get('event_type') or '') == 'linked_job_added' and not recent_message:
                recent_stage = recent_stage or 'linked'
                recent_message = f"Linked {payload.get('linked_module_key') or 'job'} {payload.get('linked_job_id') or ''}.".strip()
            elif str(recent_event.get('event_type') or '') == 'error_recorded' and not recent_message:
                recent_stage = recent_stage or 'failed'
                recent_message = str(payload.get('message') or '').strip()

        artifact_priority = {
            'report_html': 10,
            'report_excel': 20,
            'report_data': 30,
            'report': 40,
            'source': 50,
            'result': 60,
            'request': 70,
            'stderr': 80,
            'stdout': 90,
        }
        platform_download_artifacts = [
            artifact
            for artifact in platform_artifacts
            if artifact.get('downloadable') and artifact.get('is_available')
        ]
        platform_download_artifacts.sort(
            key=lambda artifact: (
                artifact_priority.get(str(artifact.get('artifact_kind') or ''), 999),
                str(artifact.get('artifact_kind') or ''),
            )
        )

        platform_timeline_events = self.summarize_platform_events(display_events)

        decorated['platform_events'] = platform_events
        decorated['platform_links'] = platform_links
        decorated['platform_artifacts'] = platform_artifacts
        decorated['platform_artifacts_by_kind'] = platform_artifacts_by_kind
        decorated['platform_artifacts_by_endpoint_kind'] = platform_artifacts_by_endpoint_kind
        decorated['platform_display_events'] = display_events[-12:]
        decorated['platform_timeline_events'] = platform_timeline_events
        decorated['platform_recent_event'] = recent_event
        decorated['platform_recent_stage'] = recent_stage or str(decorated.get('status') or '').strip() or '-'
        decorated['platform_recent_message'] = recent_message or '-'
        decorated['platform_download_artifacts'] = platform_download_artifacts[:5]
        decorated['platform_metadata_counts'] = {
            'events': len(platform_events),
            'display_events': len(decorated['platform_display_events']),
            'timeline_events': len(platform_timeline_events),
            'links': len(platform_links),
            'artifacts': len(platform_artifacts),
        }
        for key in ('created_at', 'started_at', 'completed_at', 'progress_updated_at'):
            if key in decorated:
                decorated[key] = self._format_display_timestamp_text(decorated.get(key)) or decorated.get(key)
        decorated['platform_events'] = self._format_platform_events(decorated.get('platform_events'))
        decorated['platform_display_events'] = self._format_platform_events(decorated.get('platform_display_events'))
        decorated['platform_timeline_events'] = self._format_platform_events(decorated.get('platform_timeline_events'))
        decorated['platform_artifacts'] = self._format_platform_artifacts(decorated.get('platform_artifacts'))
        decorated['platform_artifacts_by_kind'] = self._format_timestamp_payload(decorated.get('platform_artifacts_by_kind') or {})
        decorated['platform_artifacts_by_endpoint_kind'] = self._format_timestamp_payload(decorated.get('platform_artifacts_by_endpoint_kind') or {})
        return decorated