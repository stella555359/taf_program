import ast
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

BTSID_CLASSES: Set[str] = {
    "Cloud4gBts",
    "Enb",
    "SimEnb",
    "RealEnb",
    "LTEEmuEnb",
    "PrismaEnb",
    "DocomoEnb",
    "CloudBts",
    "ClassicalBts",
    "gNB",
    "DU",
    "VDU",
    "CU",
}


def get_callee_name(call_node: ast.Call) -> Optional[str]:
    func = call_node.func

    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr

    return None


def extract_bts_ids_from_source(source: str) -> List[int]:
    bts_ids: List[int] = []

    # Skip files that aren't valid Python
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return bts_ids

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        callee_name = get_callee_name(node)
        if callee_name is None or callee_name not in BTSID_CLASSES:
            continue

        # Look through keyword arguments for instance_id
        for kw in node.keywords:
            if kw.arg != "instance_id":
                continue

            value = kw.value
            if isinstance(value, ast.Constant) and isinstance(value.value, int):
                bts_ids.append(value.value)

    return bts_ids


def process_init_files(root: Path) -> Tuple[int, Dict[str, List[int]]]:
    result: Dict[str, List[int]] = {}

    file_no = 0
    for path in root.rglob("__init__.py"):
        if not path.is_file():
            continue
        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        file_no += 1

        relpath = path.relative_to(root)

        print(f"Reading {relpath}... ", end="")

        bts_ids = extract_bts_ids_from_source(source)
        if bts_ids:
            result[str(relpath)] = bts_ids

        print(f"found {len(bts_ids)} ids")

    return file_no, result


def report_duplicates(mapping: dict[str, list[int]]) -> dict:
    reverse: dict[int, list[str]] = {}
    for filename, btsids in mapping.items():
        for btsid in btsids:
            reverse.setdefault(btsid, []).append(filename)

    duplicates = {btsid: files for btsid, files in reverse.items() if len(files) > 1}

    if not duplicates:
        return {}

    print("Duplicate BTS ID values detected:")
    for btsid, files in duplicates.items():
        print(f"  BTS ID {btsid} occurs in:")
        for f in files:
            print(f"    - {f}")

    return duplicates


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    file_no, mapping = process_init_files(root)
    bts_ids_no = sum(len(btsids) for btsids in mapping.values())
    duplicates = report_duplicates(mapping)

    print()
    print(
        f"Parsed {file_no} files; "
        f"found {bts_ids_no} BTS IDs with {len(duplicates)} duplicates"
    )
    if duplicates:
        sys.exit(1)


if __name__ == "__main__":
    main()
