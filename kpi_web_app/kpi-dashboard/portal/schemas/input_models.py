from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


class InputValidationError(ValueError):
    pass


@dataclass(frozen=True)
class PortalJobCommonFields:
    job_mode: str
    build: Optional[str] = None
    environment: Optional[str] = None
    scenario: Optional[str] = None


@dataclass(frozen=True)
class PortalRuntimeOptions:
    as_base_file: bool = False
    auto_detector: bool = False
    auto_detector_is_base_file: bool = False
    auto_generator: bool = False
    dry_run: bool = False
    stop_on_failure: bool = True
    max_parallel_workers: Optional[int] = None
    log_level: Optional[str] = None
    timeout_seconds: Optional[int] = None


@dataclass(frozen=True)
class GeneratorPortalInput:
    common: PortalJobCommonFields
    runtime_options: PortalRuntimeOptions
    template_set_name: str
    template_names: List[str] = field(default_factory=list)
    report_timestamps_text: str = ''
    timestamp_delta_minutes: Optional[int] = None

    @classmethod
    def from_submission(
        cls,
        *,
        template_set_name: str,
        template_names: str,
        build: str,
        environment: str,
        scenario: str,
        report_timestamps_text: str,
        timestamp_delta_minutes: Optional[int],
        auto_detector: bool,
        auto_detector_is_base_file: bool,
        normalize_build: Callable[[str], str],
        normalize_environment: Callable[[str], str],
        parse_template_names: Callable[[str], List[str]],
    ) -> 'GeneratorPortalInput':
        cleaned_template_set_name = str(template_set_name or '').strip()
        parsed_template_names = parse_template_names(template_names)
        if not cleaned_template_set_name and not parsed_template_names:
            raise InputValidationError('Please select a template set or input one or more template_names.')

        cleaned_build = str(normalize_build(build) or '').strip()
        if not cleaned_build:
            raise InputValidationError('Build is required.')

        cleaned_environment = str(normalize_environment(environment) or '').strip()
        if not cleaned_environment:
            raise InputValidationError('Env is required.')

        cleaned_scenario = str(scenario or '').strip()
        if not cleaned_scenario:
            raise InputValidationError('Scenario is required.')

        cleaned_timestamps = str(report_timestamps_text or '').strip()
        if not cleaned_timestamps:
            raise InputValidationError('report_timestamps_list is required.')

        if timestamp_delta_minutes is not None and timestamp_delta_minutes <= 0:
            raise InputValidationError('timestamp_delta_minutes must be greater than 0 when provided.')

        return cls(
            common=PortalJobCommonFields(
                job_mode='generator',
                build=cleaned_build,
                environment=cleaned_environment,
                scenario=cleaned_scenario,
            ),
            runtime_options=PortalRuntimeOptions(
                auto_detector=bool(auto_detector),
                auto_detector_is_base_file=bool(auto_detector and auto_detector_is_base_file),
            ),
            template_set_name=cleaned_template_set_name,
            template_names=parsed_template_names,
            report_timestamps_text=cleaned_timestamps,
            timestamp_delta_minutes=timestamp_delta_minutes,
        )


@dataclass(frozen=True)
class GeneratorScoutPortalInput:
    common: PortalJobCommonFields
    runtime_options: PortalRuntimeOptions
    dist_name_filter: str
    dist_name_filters: List[str] = field(default_factory=list)
    scout_report_original_filename: str = 'scout_report.xlsx'

    @classmethod
    def from_submission(
        cls,
        *,
        build: str,
        environment: str,
        scenario: str,
        dist_name_filter: str,
        scout_report_original_filename: str,
        auto_detector: bool,
        auto_detector_is_base_file: bool,
        normalize_build: Callable[[str], str],
        normalize_environment: Callable[[str], str],
        parse_multi_value_text: Callable[[str], List[str]],
    ) -> 'GeneratorScoutPortalInput':
        cleaned_build = str(normalize_build(build) or '').strip()
        if not cleaned_build:
            raise InputValidationError('Build is required.')

        cleaned_environment = str(normalize_environment(environment) or '').strip()
        if not cleaned_environment:
            raise InputValidationError('Env is required.')

        cleaned_scenario = str(scenario or '').strip()
        if not cleaned_scenario:
            raise InputValidationError('Scenario is required.')

        cleaned_filter = str(dist_name_filter or '').strip()
        parsed_filters = parse_multi_value_text(cleaned_filter)
        if not parsed_filters:
            raise InputValidationError('DistName filter is required.')

        normalized_filename = str(scout_report_original_filename or 'scout_report.xlsx').strip() or 'scout_report.xlsx'
        if not normalized_filename.lower().endswith('.xlsx'):
            raise InputValidationError('Scout conversion only supports .xlsx files.')

        return cls(
            common=PortalJobCommonFields(
                job_mode='scout_conversion',
                build=cleaned_build,
                environment=cleaned_environment,
                scenario=cleaned_scenario,
            ),
            runtime_options=PortalRuntimeOptions(
                auto_detector=bool(auto_detector),
                auto_detector_is_base_file=bool(auto_detector and auto_detector_is_base_file),
            ),
            dist_name_filter=cleaned_filter,
            dist_name_filters=parsed_filters,
            scout_report_original_filename=normalized_filename,
        )


@dataclass(frozen=True)
class DetectorPortalInput:
    common: PortalJobCommonFields
    runtime_options: PortalRuntimeOptions
    original_filename: str
    source_generator_job_id: Optional[str] = None

    @classmethod
    def from_filename(
        cls,
        *,
        original_filename: str,
        is_base_file: bool,
        source_generator_job_id: Optional[str],
        extract_filename_context: Callable[[str], Dict[str, object]],
        filename_rule_text: str,
    ) -> 'DetectorPortalInput':
        cleaned_filename = str(original_filename or '').strip() or 'upload.xlsx'
        context = extract_filename_context(cleaned_filename)
        if not bool(context.get('matched')):
            raise InputValidationError(f'file name incorrect. {filename_rule_text}')

        return cls(
            common=PortalJobCommonFields(
                job_mode='detector',
                build=str(context.get('build') or '').strip() or None,
                environment=str(context.get('environment') or '').strip() or None,
                scenario=str(context.get('scenario') or '').strip() or None,
            ),
            runtime_options=PortalRuntimeOptions(as_base_file=bool(is_base_file)),
            original_filename=cleaned_filename,
            source_generator_job_id=str(source_generator_job_id or '').strip() or None,
        )


@dataclass(frozen=True)
class TrafficModelPortalInput:
    common: PortalJobCommonFields
    runtime_options: PortalRuntimeOptions
    selected_ue_indexes: List[int] = field(default_factory=list)
    same_type_execution_mode: str = 'serial'
    cross_type_execution_mode: str = 'serial'
    stage_execution_mode: str = 'serial'

    @classmethod
    def from_form(
        cls,
        *,
        environment: str,
        selected_ue_indexes: List[int],
        dry_run: bool,
        stop_on_failure: bool,
        max_parallel_workers: int,
        log_level: str,
        auto_generator: bool,
        auto_detector: bool,
        same_type_execution_mode: str,
        cross_type_execution_mode: str,
        stage_execution_mode: str,
    ) -> 'TrafficModelPortalInput':
        cleaned_environment = str(environment or '').strip().upper()
        if not cleaned_environment:
            raise InputValidationError('Env is required.')
        if not selected_ue_indexes:
            raise InputValidationError('Select at least one UE.')
        if max_parallel_workers <= 0:
            raise InputValidationError('max_parallel_workers must be greater than 0.')

        same_type_mode = str(same_type_execution_mode or 'serial').strip() or 'serial'
        cross_type_mode = str(cross_type_execution_mode or 'serial').strip() or 'serial'
        stage_mode = str(stage_execution_mode or 'serial').strip() or 'serial'
        valid_modes = {'serial', 'parallel'}
        if same_type_mode not in valid_modes:
            raise InputValidationError('same_type_execution_mode must be serial or parallel.')
        if cross_type_mode not in valid_modes:
            raise InputValidationError('cross_type_execution_mode must be serial or parallel.')
        if stage_mode not in valid_modes:
            raise InputValidationError('stage_execution_mode must be serial or parallel.')

        cleaned_log_level = str(log_level or 'INFO').strip().upper() or 'INFO'

        return cls(
            common=PortalJobCommonFields(
                job_mode='traffic_model',
                environment=cleaned_environment,
            ),
            runtime_options=PortalRuntimeOptions(
                auto_generator=bool(auto_generator),
                auto_detector=bool(auto_detector),
                dry_run=bool(dry_run),
                stop_on_failure=bool(stop_on_failure),
                max_parallel_workers=max_parallel_workers,
                log_level=cleaned_log_level,
            ),
            selected_ue_indexes=[int(index) for index in selected_ue_indexes],
            same_type_execution_mode=same_type_mode,
            cross_type_execution_mode=cross_type_mode,
            stage_execution_mode=stage_mode,
        )