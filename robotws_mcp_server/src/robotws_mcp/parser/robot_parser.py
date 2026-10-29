"""Lightweight Robot Framework parser for RobotWS indexing.

The parser intentionally focuses on indexable structure rather than full Robot
Framework execution semantics.
"""

from __future__ import annotations

import re
from pathlib import Path

from robotws_mcp.models import (
    LibraryImport,
    ResourceImport,
    RobotCase,
    RobotFile,
    RobotKeyword,
    RobotStep,
    normalize_path,
)


SECTION_RE = re.compile(r"^\*{3}\s*(?P<section>[^*]+?)\s*\*{3}\s*$")
ASSIGNMENT_RE = re.compile(r"^[$@&%]\{.+\}=?$")
SETTING_NAMES = {
    "documentation",
    "suite setup",
    "suite teardown",
    "test setup",
    "test teardown",
    "force tags",
    "default tags",
    "resource",
    "library",
    "variables",
}
WRAPPER_KEYWORDS = {
    "Run Keyword",
    "Run Keyword If",
    "Run Keyword Unless",
    "Run Keyword And Ignore Error",
    "Run Keyword And Continue On Failure",
    "Wait Until Keyword Succeeds",
}


def split_robot_cells(line: str) -> list[str]:
    """Split one Robot line into cells using Robot's two-space convention."""

    stripped = line.strip()
    if not stripped:
        return []
    return [cell.strip() for cell in re.split(r"\s{2,}|\t+", stripped) if cell.strip()]


def is_comment_or_empty(line: str) -> bool:
    stripped = line.strip()
    return not stripped or stripped.startswith("#")


def is_table_item(line: str) -> bool:
    return bool(line.strip()) and not line.startswith((" ", "\t")) and not line.strip().startswith("#")


def extract_keyword_from_cells(cells: list[str]) -> tuple[str | None, list[str]]:
    """Find the called keyword from a Robot step cell list."""

    if not cells:
        return None, []

    idx = 0
    while idx < len(cells) and (ASSIGNMENT_RE.match(cells[idx]) or cells[idx].endswith("=")):
        idx += 1

    if idx >= len(cells):
        return None, []

    keyword = cells[idx]
    args = cells[idx + 1 :]

    if keyword in WRAPPER_KEYWORDS:
        nested = extract_nested_keyword(keyword, args)
        if nested:
            return nested, args

    return keyword, args


def extract_nested_keyword(wrapper: str, args: list[str]) -> str | None:
    """Best-effort extraction for common Robot wrapper keywords."""

    if wrapper in {"Run Keyword", "Run Keyword And Ignore Error", "Run Keyword And Continue On Failure"}:
        return args[0] if args else None
    if wrapper in {"Run Keyword If", "Run Keyword Unless"}:
        return args[1] if len(args) > 1 else None
    if wrapper == "Wait Until Keyword Succeeds":
        return args[2] if len(args) > 2 else None
    return None


class RobotParser:
    """Parse Robot Framework files into indexable models."""

    def parse_file(self, path: str | Path, root: str | Path | None = None) -> RobotFile:
        path_obj = Path(path)
        rel_path = normalize_path(path_obj.relative_to(root) if root else path_obj)
        robot_file = RobotFile(path=rel_path)

        try:
            lines = path_obj.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines = path_obj.read_text(encoding="latin-1").splitlines()

        section = ""
        current_case: RobotCase | None = None
        current_keyword: RobotKeyword | None = None
        last_step: RobotStep | None = None
        last_setting = ""

        for line_no, line in enumerate(lines, start=1):
            section_match = SECTION_RE.match(line.strip())
            if section_match:
                section = section_match.group("section").strip().lower()
                current_case = None
                current_keyword = None
                last_step = None
                last_setting = ""
                continue

            if is_comment_or_empty(line):
                continue

            cells = split_robot_cells(line)
            if not cells:
                continue

            if section == "settings":
                last_setting = self._parse_setting(robot_file, cells, last_setting)
                continue

            if section == "variables":
                self._parse_variable(robot_file, cells)
                continue

            if section == "test cases":
                if is_table_item(line):
                    current_case = RobotCase(name=cells[0], path=rel_path, line_no=line_no)
                    robot_file.cases.append(current_case)
                    current_keyword = None
                    last_step = None
                    continue
                if current_case is None:
                    robot_file.parse_warnings.append(f"{line_no}: step outside testcase")
                    continue
                last_step = self._parse_case_line(current_case, cells, line, line_no, last_step)
                continue

            if section == "keywords":
                if is_table_item(line):
                    current_keyword = RobotKeyword(name=cells[0], path=rel_path, line_no=line_no)
                    robot_file.keywords.append(current_keyword)
                    current_case = None
                    last_step = None
                    continue
                if current_keyword is None:
                    robot_file.parse_warnings.append(f"{line_no}: step outside keyword")
                    continue
                last_step = self._parse_keyword_line(current_keyword, cells, line, line_no, last_step)
                continue

        return robot_file

    def _parse_setting(self, robot_file: RobotFile, cells: list[str], last_setting: str = "") -> str:
        setting = cells[0].lower()
        if setting == "..." and last_setting == "documentation":
            robot_file.documentation.append(" ".join(cells[1:]))
            return last_setting
        if setting == "documentation":
            robot_file.documentation.append(" ".join(cells[1:]))
            return setting
        elif setting == "resource" and len(cells) > 1:
            robot_file.resources.append(ResourceImport(path=robot_file.path, resource=cells[1]))
            return setting
        elif setting == "library" and len(cells) > 1:
            alias = None
            if "WITH NAME" in cells:
                idx = cells.index("WITH NAME")
                if idx + 1 < len(cells):
                    alias = cells[idx + 1]
            robot_file.libraries.append(LibraryImport(path=robot_file.path, library=cells[1], alias=alias))
            return setting
        elif setting in {"force tags", "default tags"} and len(cells) > 1:
            robot_file.force_tags.extend(cells[1:])
            return setting
        return setting

    def _parse_variable(self, robot_file: RobotFile, cells: list[str]) -> None:
        if len(cells) >= 2:
            robot_file.variables[cells[0]] = "    ".join(cells[1:])

    def _parse_case_line(
        self,
        case: RobotCase,
        cells: list[str],
        raw: str,
        line_no: int,
        last_step: RobotStep | None,
    ) -> RobotStep | None:
        first = cells[0]
        lower = first.lower()

        if first == "..." and last_step is not None:
            last_step.raw = f"{last_step.raw}\n{raw.strip()}"
            last_step.args.extend(cells[1:])
            return last_step

        if lower == "[documentation]":
            case.documentation.append(" ".join(cells[1:]))
            return last_step
        if lower == "...":
            case.documentation.append(" ".join(cells[1:]))
            return last_step
        if lower == "[tags]":
            case.tags.extend(cells[1:])
            return last_step
        if lower == "[setup]":
            case.setup = cells[1] if len(cells) > 1 else ""
            return last_step
        if lower == "[teardown]":
            case.teardown = cells[1] if len(cells) > 1 else ""
            return last_step

        keyword, args = extract_keyword_from_cells(cells)
        if keyword:
            step = RobotStep(keyword=keyword, raw=raw.strip(), line_no=line_no, args=args)
            case.steps.append(step)
            return step
        return last_step

    def _parse_keyword_line(
        self,
        keyword_model: RobotKeyword,
        cells: list[str],
        raw: str,
        line_no: int,
        last_step: RobotStep | None,
    ) -> RobotStep | None:
        first = cells[0]
        lower = first.lower()

        if first == "..." and last_step is not None:
            last_step.raw = f"{last_step.raw}\n{raw.strip()}"
            last_step.args.extend(cells[1:])
            return last_step

        if lower == "[documentation]":
            keyword_model.documentation.append(" ".join(cells[1:]))
            return last_step
        if lower == "[arguments]":
            keyword_model.arguments.extend(cells[1:])
            return last_step

        keyword, args = extract_keyword_from_cells(cells)
        if keyword:
            step = RobotStep(keyword=keyword, raw=raw.strip(), line_no=line_no, args=args)
            keyword_model.steps.append(step)
            return step
        return last_step
