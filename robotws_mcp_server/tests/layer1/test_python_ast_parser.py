from __future__ import annotations

from pathlib import Path

from robotws_mcp.layer1.python_ast_parser import PythonAstParser


def test_python_parser_marks_pure_python_helper(tmp_path: Path) -> None:
    source = tmp_path / "helper.py"
    source.write_text(
        '"""helpers"""\n'
        "import re\n\n"
        "def normalize_cell_id(cell_id):\n"
        "    return re.sub(r'[^0-9]', '', cell_id)\n",
        encoding="utf-8",
    )

    symbols, issues = PythonAstParser().parse_file(source, root=tmp_path)

    assert issues == []
    function = next(symbol for symbol in symbols if symbol.name == "normalize_cell_id")
    assert function.python_impl_type == "pure_python"
    assert function.signature == "normalize_cell_id(cell_id)"
    assert function.imports == ["re"]


def test_python_parser_marks_taf_dependent_robot_keyword(tmp_path: Path) -> None:
    source = tmp_path / "taf_helper.py"
    source.write_text(
        "from robot.api.deco import keyword\n"
        "from taf.namespaces import cell\n\n"
        "@keyword('Lock Cell')\n"
        "def lock_cell(cell_name):\n"
        "    return cell.lock(cell_name)\n",
        encoding="utf-8",
    )

    symbols, issues = PythonAstParser().parse_file(source, root=tmp_path)

    assert issues == []
    function = next(symbol for symbol in symbols if symbol.name == "lock_cell")
    assert function.python_impl_type == "taf_dependent"
    assert function.taf_dependencies == ["taf.namespaces.cell"]
    assert function.is_robot_keyword is True
    assert function.robot_keyword_name == "Lock Cell"
