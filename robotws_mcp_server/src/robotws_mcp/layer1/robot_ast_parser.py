"""Robot Framework AST adapter for Layer 1 v2."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from robotws_mcp.layer1.boundary import apply_boundary, classify_path
from robotws_mcp.layer1.records import (
    ArgumentSchema,
    CallArgument,
    KeywordRecord,
    LibraryImportRecord,
    ParseIssueRecord,
    ResourceImportRecord,
    RobotFileRecord,
    StepRecord,
    TestCaseRecord,
    VariableRecord,
    stable_record_id,
)
from robotws_mcp.models import StyleProfile, normalize_path

VARIABLE_RE = re.compile(r"[$@&%]\{[^}]+\}")
CONTROL_WRAPPERS = {
    "Run Keywords",
    "Run Keyword",
    "Run Keyword If",
    "Run Keyword Unless",
    "Run Keyword And Ignore Error",
    "Run Keyword And Continue On Failure",
    "Wait Until Keyword Succeeds",
}
VARIABLE_SETTER_KEYWORDS = {"Set Test Variable", "Set Suite Variable", "Set Global Variable", "Set Local Variable"}
ENVIRONMENT_TERMS = {
    "taf",
    "coam",
    "gnb",
    "ue",
    "traffic",
    "capture",
    "wireshark",
    "kpi",
    "ssh",
    "rest",
    "cell",
    "attach",
    "detach",
    "handover",
    "pa",
    "testline",
    "log",
}


@dataclass
class RobotParseResult:
    files: list[RobotFileRecord] = field(default_factory=list)
    testcases: list[TestCaseRecord] = field(default_factory=list)
    keywords: list[KeywordRecord] = field(default_factory=list)
    steps: list[StepRecord] = field(default_factory=list)
    resource_imports: list[ResourceImportRecord] = field(default_factory=list)
    library_imports: list[LibraryImportRecord] = field(default_factory=list)
    variables: list[VariableRecord] = field(default_factory=list)
    parse_issues: list[ParseIssueRecord] = field(default_factory=list)


class RobotAstParser:
    """Parse Robot files through Robot Framework's official AST model."""

    def parse_file(
        self,
        path: str | Path,
        root: str | Path | None = None,
        profile: StyleProfile | None = None,
    ) -> RobotParseResult:
        path_obj = Path(path)
        rel_path = normalize_path(path_obj.relative_to(root) if root else path_obj)
        lines = _read_lines(path_obj)
        result = RobotParseResult()

        try:
            from robot.api.parsing import get_model

            model = get_model(str(path_obj))
        except Exception as exc:  # pragma: no cover - exercised when dependency/source is broken.
            issue = ParseIssueRecord(
                record_type="parse_issue",
                id=stable_record_id("parse_issue", rel_path, "robot_ast", 1),
                path=rel_path,
                severity="error",
                source="robot_ast",
                message=str(exc),
                line_no=1,
                end_line_no=1,
            )
            apply_boundary(issue, classify_path(rel_path, profile, "parse_issue"))
            result.parse_issues.append(issue)
            return result

        file_record = RobotFileRecord(
            record_type="robot_file",
            id=stable_record_id("robot_file", rel_path, rel_path, 1),
            path=rel_path,
            file_kind="resource" if path_obj.suffix.lower() == ".resource" else "robot",
            parse_status="ok",
            line_no=1,
            end_line_no=len(lines) or 1,
            raw="\n".join(lines),
        )
        apply_boundary(file_record, classify_path(rel_path, profile, "robot_file"))
        result.files.append(file_record)

        for section in getattr(model, "sections", getattr(model, "body", [])):
            section_name = section.__class__.__name__.lower()
            body = getattr(section, "body", [])
            if "setting" in section_name:
                self._parse_settings(body, rel_path, lines, profile, file_record, result)
            elif "variable" in section_name:
                self._parse_variables(body, rel_path, lines, profile, result)
            elif "testcase" in section_name or "test case" in section_name:
                self._parse_testcases(body, rel_path, lines, profile, result)
            elif "keyword" in section_name:
                self._parse_keywords(body, rel_path, lines, profile, result)

        return result

    def _parse_settings(
        self,
        statements: Iterable[object],
        path: str,
        lines: list[str],
        profile: StyleProfile | None,
        file_record: RobotFileRecord,
        result: RobotParseResult,
    ) -> None:
        for stmt in statements:
            cells = _cells(stmt)
            if not cells:
                continue
            setting = cells[0].lower()
            start, end = _span(stmt)
            raw = _raw_span(lines, start, end)
            if setting == "documentation":
                file_record.suite_documentation.append(" ".join(cells[1:]))
            elif setting == "force tags":
                file_record.force_tags.extend(cells[1:])
            elif setting == "default tags":
                file_record.default_tags.extend(cells[1:])
            elif setting == "resource" and len(cells) > 1:
                record = ResourceImportRecord(
                    record_type="resource_import",
                    id=stable_record_id("resource_import", path, cells[1], start),
                    source_path=path,
                    resource_path=cells[1],
                    resolved_path=_resolve_robot_import(path, cells[1]),
                    line_no=start,
                    end_line_no=end,
                    raw=raw,
                )
                apply_boundary(record, classify_path(record.resolved_path or path, profile, "resource_import"))
                result.resource_imports.append(record)
            elif setting == "library" and len(cells) > 1:
                alias = _library_alias(cells)
                args = cells[2:]
                record = LibraryImportRecord(
                    record_type="library_import",
                    id=stable_record_id("library_import", path, cells[1], start),
                    source_path=path,
                    library=cells[1],
                    alias=alias,
                    arguments=[_argument(cell) for cell in args if cell != "WITH NAME" and cell != alias],
                    resolved_path=_resolve_robot_import(path, cells[1]),
                    line_no=start,
                    end_line_no=end,
                    raw=raw,
                )
                apply_boundary(record, classify_path(record.resolved_path or path, profile, "library_import"))
                result.library_imports.append(record)

    def _parse_variables(
        self,
        statements: Iterable[object],
        path: str,
        lines: list[str],
        profile: StyleProfile | None,
        result: RobotParseResult,
    ) -> None:
        for stmt in statements:
            cells = _cells(stmt)
            if len(cells) < 2 or not VARIABLE_RE.fullmatch(cells[0].rstrip("=")):
                continue
            start, end = _span(stmt)
            record = VariableRecord(
                record_type="variable",
                id=stable_record_id("variable", path, cells[0], start),
                source_path=path,
                name=cells[0].rstrip("="),
                value="    ".join(cells[1:]),
                line_no=start,
                end_line_no=end,
                raw=_raw_span(lines, start, end),
            )
            apply_boundary(record, classify_path(path, profile, "variable"))
            result.variables.append(record)

    def _parse_testcases(
        self,
        testcases: Iterable[object],
        path: str,
        lines: list[str],
        profile: StyleProfile | None,
        result: RobotParseResult,
    ) -> None:
        for case in testcases:
            name = getattr(case, "name", "") or _node_name(case)
            if not name:
                continue
            start, end = _span(case)
            record = TestCaseRecord(
                record_type="testcase",
                id=stable_record_id("testcase", path, name, start),
                name=name,
                path=path,
                line_no=start,
                end_line_no=end,
                raw=_raw_span(lines, start, end),
            )
            apply_boundary(record, classify_path(path, profile, "testcase"))
            ordinal = 1
            for stmt in getattr(case, "body", []):
                ordinal = self._parse_testcase_statement(stmt, path, lines, profile, record, result, ordinal)
            result.testcases.append(record)

    def _parse_testcase_statement(
        self,
        stmt: object,
        path: str,
        lines: list[str],
        profile: StyleProfile | None,
        case: TestCaseRecord,
        result: RobotParseResult,
        ordinal: int,
    ) -> int:
        cells = _cells(stmt)
        if not cells:
            return ordinal
        first = cells[0].lower()
        if first == "[documentation]":
            case.documentation.append(" ".join(cells[1:]))
            return ordinal
        if first == "[tags]":
            case.tags.extend(cells[1:])
            return ordinal
        normalized_type = "step"
        action_cells = cells
        if first == "[setup]":
            normalized_type = "setup"
            action_cells = cells[1:]
        elif first == "[teardown]":
            normalized_type = "teardown"
            action_cells = cells[1:]
        steps = _logical_steps(action_cells, normalized_type)
        for step_cells, condition, surface_keyword in steps:
            step = self._step_record(
                step_cells,
                path,
                lines,
                profile,
                "testcase",
                case.name,
                case.id,
                normalized_type,
                ordinal,
                stmt,
                condition,
                surface_keyword,
            )
            if not step.keyword:
                continue
            result.steps.append(step)
            case.keyword_sequence.append(step.keyword)
            if normalized_type == "setup":
                case.setup_step_ids.append(step.id)
            elif normalized_type == "teardown":
                case.teardown_step_ids.append(step.id)
            else:
                case.body_step_ids.append(step.id)
            ordinal += 1
        return ordinal

    def _parse_keywords(
        self,
        keywords: Iterable[object],
        path: str,
        lines: list[str],
        profile: StyleProfile | None,
        result: RobotParseResult,
    ) -> None:
        for keyword_node in keywords:
            name = getattr(keyword_node, "name", "") or _node_name(keyword_node)
            if not name:
                continue
            start, end = _span(keyword_node)
            record = KeywordRecord(
                record_type="keyword",
                id=stable_record_id("keyword", path, name, start),
                name=name,
                path=path,
                line_no=start,
                end_line_no=end,
                raw=_raw_span(lines, start, end),
            )
            apply_boundary(record, classify_path(path, profile, "keyword"))
            ordinal = 1
            for stmt in getattr(keyword_node, "body", []):
                cells = _cells(stmt)
                if not cells:
                    continue
                first = cells[0].lower()
                if first == "[documentation]":
                    record.documentation.append(" ".join(cells[1:]))
                    continue
                if first == "[tags]":
                    record.tags.extend(cells[1:])
                    continue
                if first == "[arguments]":
                    record.arguments_schema.extend(_arguments_schema(cells[1:]))
                    continue
                steps = _logical_steps(cells, "keyword_step")
                for step_cells, condition, surface_keyword in steps:
                    step = self._step_record(
                        step_cells,
                        path,
                        lines,
                        profile,
                        "keyword",
                        name,
                        record.id,
                        "keyword_step",
                        ordinal,
                        stmt,
                        condition,
                        surface_keyword,
                    )
                    if not step.keyword:
                        continue
                    result.steps.append(step)
                    record.step_ids.append(step.id)
                    record.keyword_sequence.append(step.keyword)
                    ordinal += 1
            record.robot_impl_type = _robot_impl_type(record.keyword_sequence)
            result.keywords.append(record)

    def _step_record(
        self,
        cells: list[str],
        path: str,
        lines: list[str],
        profile: StyleProfile | None,
        owner_type: str,
        owner_name: str,
        owner_id: str,
        normalized_type: str,
        ordinal: int,
        stmt: object,
        condition: str | None,
        surface_keyword: str | None,
    ) -> StepRecord:
        start, end = _span(stmt)
        keyword, raw_args, assignment_outputs = _call_parts(cells)
        keyword_outputs = _variables_output_from_keyword(keyword, raw_args)
        variables_output = assignment_outputs or keyword_outputs
        step = StepRecord(
            record_type="step",
            id=stable_record_id("step", path, f"{owner_type}:{owner_name}:{ordinal}:{keyword}", start),
            owner_type=owner_type,
            owner_name=owner_name,
            owner_id=owner_id,
            path=path,
            normalized_type=normalized_type,
            ordinal=ordinal,
            keyword=keyword,
            arguments=[_argument(arg) for arg in raw_args],
            condition=condition,
            variables_input=_variables_input(_variables_input_args(keyword, raw_args), condition),
            variables_output=variables_output,
            surface_keyword=surface_keyword,
            line_no=start,
            end_line_no=end,
            raw=_raw_span(lines, start, end),
        )
        apply_boundary(step, classify_path(path, profile, "step"))
        return step


def _read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1").splitlines()


def _span(node: object) -> tuple[int, int]:
    start = int(getattr(node, "lineno", 1) or 1)
    end = int(getattr(node, "end_lineno", start) or start)
    tokens = list(getattr(node, "tokens", []) or [])
    token_lines = [int(getattr(token, "lineno", 0) or 0) for token in tokens if getattr(token, "lineno", 0)]
    if token_lines:
        start = min(start, min(token_lines))
        end = max(end, max(token_lines))
    return start, end


def _cells(stmt: object) -> list[str]:
    tokens = list(getattr(stmt, "tokens", []) or [])
    values: list[str] = []
    for token in tokens:
        token_type = str(getattr(token, "type", "")).upper()
        value = str(getattr(token, "value", "")).strip()
        if not value or token_type in {"SEPARATOR", "EOL", "COMMENT"}:
            continue
        if value == "...":
            continue
        values.append(value)
    return values


def _node_name(node: object) -> str:
    cells = _cells(node)
    return cells[0] if cells else ""


def _raw_span(lines: list[str], start: int, end: int) -> str:
    return "\n".join(lines[max(start - 1, 0) : max(end, start)])


def _logical_steps(cells: list[str], normalized_type: str) -> list[tuple[list[str], str | None, str | None]]:
    if not cells:
        return []
    keyword, args, _variables_output = _call_parts(cells)
    if keyword == "Run Keywords":
        chunks = _split_run_keywords(args)
        result: list[tuple[list[str], str | None, str | None]] = []
        for chunk in chunks:
            result.extend(_logical_steps(chunk, normalized_type))
        return [(chunk, condition, "Run Keywords") for chunk, condition, _surface in result]
    if keyword == "Run Keyword If" and len(args) >= 2:
        return [(args[1:], args[0], "Run Keyword If")]
    if keyword == "Run Keyword" and args:
        return [(args, None, "Run Keyword")]
    return [(cells, None, None)]


def _split_run_keywords(args: list[str]) -> list[list[str]]:
    chunks: list[list[str]] = []
    current: list[str] = []
    for arg in args:
        if arg == "AND":
            if current:
                chunks.append(current)
            current = []
        else:
            current.append(arg)
    if current:
        chunks.append(current)
    return chunks


def _call_parts(cells: list[str]) -> tuple[str, list[str], list[str]]:
    variables_output: list[str] = []
    idx = 0
    while idx < len(cells) and _is_assignment(cells[idx]):
        variables_output.append(_assignment_name(cells[idx]))
        idx += 1
    if idx >= len(cells):
        return "", [], variables_output
    return cells[idx], cells[idx + 1 :], variables_output


def _is_assignment(value: str) -> bool:
    stripped = _assignment_name(value)
    return bool(VARIABLE_RE.fullmatch(stripped)) and (value.endswith("=") or value.startswith(("${", "@{", "&{")))


def _assignment_name(value: str) -> str:
    return value.rstrip("=").strip()


def _argument(value: str) -> CallArgument:
    if "=" in value and not value.startswith(("${", "@{", "&{")):
        name, arg_value = value.split("=", 1)
        if name:
            return CallArgument(kind="named", name=name, value=arg_value)
    return CallArgument(kind="positional", value=value)


def _variables_input(args: list[str], condition: str | None) -> list[str]:
    variables: list[str] = []
    for text in [*(args or []), condition or ""]:
        variables.extend(VARIABLE_RE.findall(text))
    return sorted(set(variables))


def _variables_input_args(keyword: str, args: list[str]) -> list[str]:
    if keyword in VARIABLE_SETTER_KEYWORDS and args:
        return args[1:]
    return args


def _variables_output_from_keyword(keyword: str, args: list[str]) -> list[str]:
    if keyword in VARIABLE_SETTER_KEYWORDS and args:
        first = args[0]
        if VARIABLE_RE.fullmatch(first):
            return [first]
    return []


def _arguments_schema(cells: list[str]) -> list[ArgumentSchema]:
    schema: list[ArgumentSchema] = []
    for cell in cells:
        if not VARIABLE_RE.match(cell):
            continue
        default = None
        robot_name = cell
        required = True
        if "=" in cell:
            robot_name, default = cell.split("=", 1)
            required = False
        schema.append(ArgumentSchema(name=robot_name.strip("${@&%}"), robot_name=robot_name, default=default, required=required))
    return schema


def _library_alias(cells: list[str]) -> str | None:
    if "WITH NAME" in cells:
        idx = cells.index("WITH NAME")
        if len(cells) > idx + 1:
            return cells[idx + 1]
    return None


def _resolve_robot_import(source_path: str, import_path: str) -> str | None:
    if VARIABLE_RE.search(import_path):
        return None
    if import_path.startswith("testsuite/"):
        return normalize_path(import_path)
    source_parts = Path(source_path).parent
    return normalize_path(source_parts / import_path)


def _robot_impl_type(keyword_sequence: list[str]) -> str:
    if not keyword_sequence:
        return "unknown"
    joined = " ".join(keyword_sequence).lower()
    return "taf_dependent" if any(term in joined for term in ENVIRONMENT_TERMS) else "pure_logic"
