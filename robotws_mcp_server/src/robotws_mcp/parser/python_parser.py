"""Basic Python symbol parser for RobotWS helper libraries."""

from __future__ import annotations

import ast
from pathlib import Path

from robotws_mcp.models import PythonSymbol, normalize_path


class PythonParser:
    """Parse Python files at a lightweight symbol level."""

    def parse_file(self, path: str | Path, root: str | Path | None = None) -> list[PythonSymbol]:
        path_obj = Path(path)
        rel_path = normalize_path(path_obj.relative_to(root) if root else path_obj)

        try:
            source = path_obj.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            source = path_obj.read_text(encoding="latin-1")

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return []

        imports = self._collect_imports(tree)
        symbols: list[PythonSymbol] = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                symbols.append(
                    PythonSymbol(
                        path=rel_path,
                        name=node.name,
                        symbol_type="function",
                        line_no=node.lineno,
                        signature=self._format_signature(node),
                        docstring=ast.get_docstring(node) or "",
                        imports=imports,
                    )
                )
            elif isinstance(node, ast.ClassDef):
                symbols.append(
                    PythonSymbol(
                        path=rel_path,
                        name=node.name,
                        symbol_type="class",
                        line_no=node.lineno,
                        signature=node.name,
                        docstring=ast.get_docstring(node) or "",
                        imports=imports,
                    )
                )
                for child in node.body:
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        symbols.append(
                            PythonSymbol(
                                path=rel_path,
                                name=f"{node.name}.{child.name}",
                                symbol_type="method",
                                line_no=child.lineno,
                                signature=f"{node.name}.{self._format_signature(child)}",
                                docstring=ast.get_docstring(child) or "",
                                imports=imports,
                            )
                        )
        return symbols

    def _collect_imports(self, tree: ast.Module) -> list[str]:
        imports: list[str] = []
        for node in tree.body:
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                imports.extend(f"{module}.{alias.name}" if module else alias.name for alias in node.names)
        return imports

    def _format_signature(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        args = [arg.arg for arg in node.args.args]
        if node.args.vararg:
            args.append(f"*{node.args.vararg.arg}")
        if node.args.kwarg:
            args.append(f"**{node.args.kwarg.arg}")
        return f"{node.name}({', '.join(args)})"
