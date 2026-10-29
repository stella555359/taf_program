"""Static Python AST parser for Layer 1 v2."""

from __future__ import annotations

import ast
from pathlib import Path

from robotws_mcp.layer1.boundary import apply_boundary, classify_path
from robotws_mcp.layer1.records import ParseIssueRecord, PythonSymbolRecord, stable_record_id
from robotws_mcp.models import StyleProfile, normalize_path


class PythonAstParser:
    """Parse Python helper/library files without importing or executing them."""

    def parse_file(
        self,
        path: str | Path,
        root: str | Path | None = None,
        profile: StyleProfile | None = None,
    ) -> tuple[list[PythonSymbolRecord], list[ParseIssueRecord]]:
        path_obj = Path(path)
        rel_path = normalize_path(path_obj.relative_to(root) if root else path_obj)

        try:
            source = path_obj.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            source = path_obj.read_text(encoding="latin-1")

        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            issue = ParseIssueRecord(
                record_type="parse_issue",
                id=stable_record_id("parse_issue", rel_path, "python_syntax", exc.lineno),
                path=rel_path,
                severity="error",
                source="python_ast",
                message=str(exc),
                line_no=exc.lineno or 1,
                end_line_no=exc.end_lineno or exc.lineno or 1,
            )
            apply_boundary(issue, classify_path(rel_path, profile, "parse_issue"))
            return [], [issue]

        imports = _collect_imports(tree)
        lines = source.splitlines()
        records: list[PythonSymbolRecord] = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                records.append(self._symbol_record(node, rel_path, "", imports, lines, profile))
            elif isinstance(node, ast.ClassDef):
                records.append(self._class_record(node, rel_path, imports, lines, profile))
                for child in node.body:
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        records.append(self._symbol_record(child, rel_path, node.name, imports, lines, profile))
        return records, []

    def _class_record(
        self,
        node: ast.ClassDef,
        path: str,
        imports: list[str],
        lines: list[str],
        profile: StyleProfile | None,
    ) -> PythonSymbolRecord:
        decorators, robot_keyword_name = _decorators(node.decorator_list)
        record = PythonSymbolRecord(
            record_type="python_symbol",
            id=stable_record_id("python_symbol", path, node.name, node.lineno),
            path=path,
            name=node.name,
            qualified_name=node.name,
            symbol_type="class",
            signature=node.name,
            docstring=ast.get_docstring(node) or "",
            imports=imports,
            decorators=decorators,
            python_impl_type=_impl_type(imports),
            taf_dependencies=_taf_dependencies(imports),
            is_robot_keyword=robot_keyword_name is not None,
            robot_keyword_name=robot_keyword_name,
            line_no=node.lineno,
            end_line_no=getattr(node, "end_lineno", node.lineno) or node.lineno,
            raw=_raw_span(lines, node.lineno, getattr(node, "end_lineno", node.lineno) or node.lineno),
        )
        apply_boundary(record, classify_path(path, profile, "python_symbol"))
        return record

    def _symbol_record(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        path: str,
        class_name: str,
        imports: list[str],
        lines: list[str],
        profile: StyleProfile | None,
    ) -> PythonSymbolRecord:
        name = f"{class_name}.{node.name}" if class_name else node.name
        decorators, robot_keyword_name = _decorators(node.decorator_list)
        signature = f"{name}({_format_args(node.args)})"
        record = PythonSymbolRecord(
            record_type="python_symbol",
            id=stable_record_id("python_symbol", path, name, node.lineno),
            path=path,
            name=name,
            qualified_name=name,
            symbol_type="method" if class_name else "function",
            signature=signature,
            docstring=ast.get_docstring(node) or "",
            imports=imports,
            decorators=decorators,
            python_impl_type=_impl_type(imports),
            taf_dependencies=_taf_dependencies(imports),
            is_robot_keyword=robot_keyword_name is not None,
            robot_keyword_name=robot_keyword_name,
            line_no=node.lineno,
            end_line_no=getattr(node, "end_lineno", node.lineno) or node.lineno,
            raw=_raw_span(lines, node.lineno, getattr(node, "end_lineno", node.lineno) or node.lineno),
        )
        apply_boundary(record, classify_path(path, profile, "python_symbol"))
        return record


def _collect_imports(tree: ast.Module) -> list[str]:
    imports: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            imports.extend(f"{module}.{alias.name}" if module else alias.name for alias in node.names)
    return sorted(set(imports))


def _format_args(args: ast.arguments) -> str:
    names = [arg.arg for arg in args.args]
    if args.vararg:
        names.append(f"*{args.vararg.arg}")
    names.extend(arg.arg for arg in args.kwonlyargs)
    if args.kwarg:
        names.append(f"**{args.kwarg.arg}")
    return ", ".join(names)


def _decorators(nodes: list[ast.expr]) -> tuple[list[str], str | None]:
    values: list[str] = []
    robot_keyword_name: str | None = None
    for node in nodes:
        text = _decorator_text(node)
        values.append(text)
        if text == "keyword":
            robot_keyword_name = ""
        if isinstance(node, ast.Call) and _decorator_text(node.func) == "keyword":
            robot_keyword_name = ""
            if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                robot_keyword_name = node.args[0].value
    return values, robot_keyword_name


def _decorator_text(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _decorator_text(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    if isinstance(node, ast.Call):
        return _decorator_text(node.func)
    return ""


def _taf_dependencies(imports: list[str]) -> list[str]:
    return [item for item in imports if item == "taf" or item.startswith("taf.")]


def _impl_type(imports: list[str]) -> str:
    return "taf_dependent" if _taf_dependencies(imports) else "pure_python"


def _raw_span(lines: list[str], start: int, end: int) -> str:
    return "\n".join(lines[max(start - 1, 0) : max(end, start)])
