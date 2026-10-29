"""Keyword call resolution for Layer 2 graph construction."""

from __future__ import annotations

import re
from collections import deque
from typing import Any

from robotws_mcp.layer2.input_loader import Layer1GraphInput
from robotws_mcp.layer2.models import ResolutionResult
from robotws_mcp.models import normalize_path

BUILTIN_KEYWORDS = {
    "addtimetodate",
    "appendtofile",
    "appendtolist",
    "callmethod",
    "catenate",
    "clickelement",
    "copylist",
    "copyfile",
    "copyfiles",
    "combinelists",
    "comment",
    "convertdate",
    "converttobinary",
    "converttohex",
    "converttointeger",
    "converttolist",
    "converttolowercase",
    "converttonumber",
    "converttostring",
    "converttime",
    "converttouppercase",
    "createlist",
    "createdictionary",
    "createfile",
    "directoryshouldexist",
    "evaluate",
    "extractzipfile",
    "fail",
    "fetchfromleft",
    "fetchfromright",
    "fileshouldbeempty",
    "fileshouldexist",
    "getfromdictionary",
    "getfromlist",
    "getindexfromlist",
    "getline",
    "getlinescontainingstring",
    "getlinesmatchingregexp",
    "getmatchcount",
    "getmatches",
    "getcurrentdate",
    "getdictionaryitems",
    "getdictionarykeys",
    "getdictionaryvalues",
    "getlength",
    "getregexpmatches",
    "getsubstring",
    "gettext",
    "gettime",
    "getvariablevalue",
    "grepfile",
    "importlibrary",
    "inputtext",
    "joinpath",
    "listfiliesindirectory",
    "listfilesindirectory",
    "listshouldcontainsublist",
    "listshouldcontainvalue",
    "listshouldnotcontainvalue",
    "listsshouldbeequal",
    "log",
    "logmany",
    "logtoconsole",
    "passexecutionif",
    "removefromlist",
    "removedirectory",
    "removefile",
    "removeduplicates",
    "removestring",
    "removestringusingregexp",
    "removevaluesfromlist",
    "reverselist",
    "replacestring",
    "replacestringusingregexp",
    "returnfromkeywordif",
    "run",
    "runandreturnrcandoutput",
    "runkeywordandreturnstatus",
    "runprocess",
    "setglobalvariable",
    "setsuitemetadata",
    "setsuitevariable",
    "settaskvariable",
    "setlibrarysearchorder",
    "settodictionary",
    "returnfromkeyword",
    "settestvariable",
    "setvariable",
    "setvariableif",
    "shouldbeequal",
    "shouldbeequalasintegers",
    "shouldbeequalasnumbers",
    "shouldbeequalasstrings",
    "shouldbeempty",
    "shouldcontainany",
    "shouldcontain",
    "shouldmatchregexp",
    "shouldnotcontain",
    "shouldnotbeempty",
    "shouldnotbeequal",
    "shouldnotbetrue",
    "shouldbetrue",
    "shouldbeuppercase",
    "sleep",
    "sortlist",
    "splitpath",
    "splitextension",
    "splitstring",
    "splitstringtocharacters",
    "splitstringfromright",
    "splittolines",
    "stripstring",
    "subtractdatefromdate",
    "waituntilkeywordsucceeds",
    "waituntilelementisvisible",
}

CONTROL_KEYWORDS = {
    "runkeyword",
    "runkeywordandcontinueonfailure",
    "runkeywordandignoreerror",
    "runkeywordif",
    "runkeywordiftestfailed",
    "runkeywordunless",
    "runkeywords",
}

SETTING_TOKENS = {
    "[arguments]",
    "[documentation]",
    "[return]",
    "[setup]",
    "[tags]",
    "[teardown]",
    "[timeout]",
}

PLAIN_TAF_KEYWORD_PATTERNS = (
    "702 case setup for ute",
    "702 case teardown for ute",
    "at operation",
    "coam navigate to login page via webui",
    "coam update several parameters via webui",
    "coam save snapshot via webui",
    "collect interface mirroring bip collector from webui",
    "common case testline setup",
    "connect to capacity unit master",
    "connect to capacity unit slave",
    "connect to common unit master",
    "get rmod id list by restapi",
    "get ue info",
    "get gnb cu type value",
    "log collection",
    "prepare multiue with client",
    "power ue start dl traffic",
    "start mue dltraffic with appserver",
    "start capture cp-if logs from container",
    "start trace in dcap",
    "start l3 call and verify throughput",
    "stop cp-if log collection",
    "stop trace in dcap",
    "stop traffic with appserver",
    "vdu get cell list from webem",
)


class KeywordResolver:
    """Resolve Layer 1 step calls to graph targets conservatively."""

    def __init__(self, graph_input: Layer1GraphInput) -> None:
        self.graph_input = graph_input
        self.keywords = graph_input.by_type.get("keyword", [])
        self.python_symbols = graph_input.by_type.get("python_symbol", [])
        self._keywords_by_norm: dict[str, list[dict[str, Any]]] = {}
        self._python_symbols_by_norm: dict[str, list[dict[str, Any]]] = {}
        self._excluded_keywords_by_norm: dict[str, list[dict[str, Any]]] = {}
        self._import_graph = self._build_import_graph()
        for keyword in self.keywords:
            self._keywords_by_norm.setdefault(normalize_keyword(str(keyword.get("name", ""))), []).append(keyword)
        for keywords in graph_input.excluded_keywords_by_name.values():
            for keyword in keywords:
                self._excluded_keywords_by_norm.setdefault(normalize_keyword(str(keyword.get("name", ""))), []).append(keyword)
        for symbol in self.python_symbols:
            names = {str(symbol.get("name", "")), str(symbol.get("robot_keyword_name", "") or "")}
            for name in names:
                if name:
                    self._python_symbols_by_norm.setdefault(normalize_keyword(name), []).append(symbol)

    def resolve_all(self) -> list[ResolutionResult]:
        return [self.resolve_step(step) for step in self.graph_input.by_type.get("step", [])]

    def resolve_step(self, step: dict[str, Any]) -> ResolutionResult:
        called_name = str(step.get("keyword", ""))
        normalized = normalize_keyword(called_name)
        owner_id = str(step.get("owner_id", ""))
        owner = self.graph_input.by_id.get(owner_id, {})
        current_path = normalize_path(str(step.get("path") or owner.get("path") or ""))

        current_file_matches = self._matching_keywords_in_paths(normalized, [current_path])
        if len(current_file_matches) == 1:
            return self._resolved(step, current_file_matches[0], normalized, "matched keyword in current file")
        if len(current_file_matches) > 1:
            return self._ambiguous(step, normalized, current_file_matches, "multiple current-file keyword matches")

        direct_paths = self._direct_import_paths(current_path)
        direct_matches = self._matching_keywords_in_paths(normalized, direct_paths)
        if len(direct_matches) == 1:
            return self._resolved(
                step,
                direct_matches[0],
                normalized,
                "matched keyword from direct resource import",
                self._direct_import_evidence(current_path, direct_matches[0]),
            )
        if len(direct_matches) > 1:
            return self._ambiguous(step, normalized, direct_matches, "same keyword found in multiple direct resources")

        closure_paths, closure_evidence = self._resource_closure(current_path)
        closure_matches = self._matching_keywords_in_paths(normalized, closure_paths)
        if len(closure_matches) == 1:
            return self._resolved(
                step,
                closure_matches[0],
                normalized,
                "matched keyword from resource import closure",
                closure_evidence.get(normalize_path(str(closure_matches[0].get("path", ""))), []),
            )
        if len(closure_matches) > 1:
            return self._ambiguous(step, normalized, closure_matches, "same keyword found in resource import closure")

        allowed_matches = self._keywords_by_norm.get(normalized, [])
        if len(allowed_matches) == 1:
            return self._resolved(step, allowed_matches[0], normalized, "unique keyword match in allowed resource scope")
        if len(allowed_matches) > 1:
            return self._ambiguous(step, normalized, allowed_matches, "same keyword found in multiple allowed records")

        python_matches = self._python_symbols_by_norm.get(normalized, [])
        if len(python_matches) == 1:
            return self._python_symbol(step, normalized, python_matches[0])
        if len(python_matches) > 1:
            return self._ambiguous(step, normalized, python_matches, "same Python symbol exposed by multiple records")

        if called_name.strip().lower() in SETTING_TOKENS:
            return self._synthetic(step, normalized, "control_keyword", f"control_keyword:{normalized}", "Robot setting token")
        if normalized in CONTROL_KEYWORDS:
            return self._synthetic(step, normalized, "control_keyword", f"control_keyword:{normalized}", "known Robot control keyword")
        if normalized in BUILTIN_KEYWORDS:
            return self._synthetic(step, normalized, "builtin", f"builtin:{normalized}", "known Robot Framework built-in keyword")
        if _looks_like_namespace_call(called_name):
            return self._taf_library_keyword(step, normalized)
        if _looks_like_plain_taf_call(called_name):
            return self._taf_library_keyword(
                step,
                normalized,
                "plain device/TAF-like call not resolved to local Robot/Python definition; treated as TAF library keyword",
            )

        excluded_matches = self._excluded_keywords_by_norm.get(normalized, [])
        if excluded_matches:
            return self._excluded(step, normalized, excluded_matches)

        return ResolutionResult(
            step_id=str(step.get("id", "")),
            owner_id=owner_id,
            called_name=called_name,
            normalized_called_name=normalized,
            resolution_status="excluded",
            reason="no visible Robot keyword, Python symbol, built-in, or TAF fallback match; excluded from generation context",
            data=_step_context(step),
        )

    def _resolved(
        self,
        step: dict[str, Any],
        keyword: dict[str, Any],
        normalized: str,
        reason: str,
        evidence: list[str] | None = None,
    ) -> ResolutionResult:
        return ResolutionResult(
            step_id=str(step.get("id", "")),
            owner_id=str(step.get("owner_id", "")),
            called_name=str(step.get("keyword", "")),
            normalized_called_name=normalized,
            resolution_status="resolved",
            called_target_node_id=str(keyword.get("id", "")),
            called_target_record_id=str(keyword.get("id", "")),
            reason=reason,
            import_evidence=evidence or [],
            data=_step_context(step),
        )

    def _python_symbol(self, step: dict[str, Any], normalized: str, symbol: dict[str, Any]) -> ResolutionResult:
        return ResolutionResult(
            step_id=str(step.get("id", "")),
            owner_id=str(step.get("owner_id", "")),
            called_name=str(step.get("keyword", "")),
            normalized_called_name=normalized,
            resolution_status="python_symbol",
            called_target_node_id=str(symbol.get("id", "")),
            called_target_record_id=str(symbol.get("id", "")),
            library_kind="taf" if symbol.get("python_impl_type") == "taf_dependent" else "local_python",
            reason="matched local Python symbol or exposed robot keyword",
            data=_step_context(step),
        )

    def _taf_library_keyword(
        self,
        step: dict[str, Any],
        normalized: str,
        reason: str = "namespace-style call not resolved to local Robot/Python definition; treated as TAF library keyword",
    ) -> ResolutionResult:
        called_name = str(step.get("keyword", ""))
        return ResolutionResult(
            step_id=str(step.get("id", "")),
            owner_id=str(step.get("owner_id", "")),
            called_name=called_name,
            normalized_called_name=normalized,
            resolution_status="taf_library_keyword",
            called_target_node_id=f"taf_library_keyword:{called_name}",
            library_kind="taf",
            reason=reason,
            data=_step_context(step),
        )

    def _synthetic(
        self,
        step: dict[str, Any],
        normalized: str,
        status: str,
        target_node_id: str,
        reason: str,
    ) -> ResolutionResult:
        return ResolutionResult(
            step_id=str(step.get("id", "")),
            owner_id=str(step.get("owner_id", "")),
            called_name=str(step.get("keyword", "")),
            normalized_called_name=normalized,
            resolution_status=status,
            called_target_node_id=target_node_id,
            reason=reason,
            data=_step_context(step),
        )

    def _ambiguous(
        self,
        step: dict[str, Any],
        normalized: str,
        candidates: list[dict[str, Any]],
        reason: str,
    ) -> ResolutionResult:
        return ResolutionResult(
            step_id=str(step.get("id", "")),
            owner_id=str(step.get("owner_id", "")),
            called_name=str(step.get("keyword", "")),
            normalized_called_name=normalized,
            resolution_status="excluded",
            reason=f"{reason}; excluded because multiple candidates would require guessing",
            candidates=[_candidate(item) for item in candidates],
            data=_step_context(step),
        )

    def _excluded(self, step: dict[str, Any], normalized: str, candidates: list[dict[str, Any]]) -> ResolutionResult:
        return ResolutionResult(
            step_id=str(step.get("id", "")),
            owner_id=str(step.get("owner_id", "")),
            called_name=str(step.get("keyword", "")),
            normalized_called_name=normalized,
            resolution_status="excluded",
            reason="matching keyword exists only outside the active allowed boundary",
            candidates=[_candidate(item) for item in candidates],
            data=_step_context(step),
        )

    def _matching_keywords_in_paths(self, normalized: str, paths: list[str]) -> list[dict[str, Any]]:
        path_set = {normalize_path(path) for path in paths if path}
        return [
            keyword
            for keyword in self._keywords_by_norm.get(normalized, [])
            if normalize_path(str(keyword.get("path", ""))) in path_set
        ]

    def _build_import_graph(self) -> dict[str, list[str]]:
        graph: dict[str, list[str]] = {}
        for record in self.graph_input.by_type.get("resource_import", []):
            source_path = normalize_path(str(record.get("source_path") or ""))
            target_path = normalize_path(str(record.get("resolved_path") or record.get("resource_path") or ""))
            if source_path and target_path:
                graph.setdefault(source_path, []).append(target_path)
        return graph

    def _direct_import_paths(self, source_path: str) -> list[str]:
        return self._import_graph.get(normalize_path(source_path), [])

    def _direct_import_evidence(self, source_path: str, keyword: dict[str, Any]) -> list[str]:
        target_path = normalize_path(str(keyword.get("path", "")))
        if target_path in self._direct_import_paths(source_path):
            return [f"{normalize_path(source_path)} -> {target_path}"]
        return []

    def _resource_closure(self, source_path: str) -> tuple[list[str], dict[str, list[str]]]:
        start = normalize_path(source_path)
        queue: deque[tuple[str, list[str]]] = deque((target, [start, target]) for target in self._import_graph.get(start, []))
        visited: set[str] = set()
        paths: list[str] = []
        evidence: dict[str, list[str]] = {}
        while queue:
            path, trail = queue.popleft()
            if path in visited:
                continue
            visited.add(path)
            paths.append(path)
            evidence[path] = [" -> ".join(trail)]
            for child in self._import_graph.get(path, []):
                if child not in visited:
                    queue.append((child, [*trail, child]))
        return paths, evidence


def normalize_keyword(name: str) -> str:
    """Approximate Robot Framework keyword matching semantics."""

    return re.sub(r"[\s_]+", "", name).lower()


def _looks_like_namespace_call(name: str) -> bool:
    prefix, separator, suffix = name.partition(".")
    return bool(separator and prefix.strip() and suffix.strip() and " " not in prefix.strip())


def _looks_like_plain_taf_call(name: str) -> bool:
    normalized = " ".join(name.strip().lower().split())
    return any(normalized.startswith(pattern) for pattern in PLAIN_TAF_KEYWORD_PATTERNS)


def _candidate(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_id": record.get("id", ""),
        "record_type": record.get("record_type", ""),
        "name": record.get("name") or record.get("robot_keyword_name") or record.get("qualified_name") or "",
        "path": record.get("path", ""),
        "line_no": record.get("line_no", 1),
    }


def _step_context(step: dict[str, Any]) -> dict[str, Any]:
    return {
        "domain": step.get("domain", "Unknown"),
        "feature": step.get("feature"),
        "path": step.get("path", ""),
        "line_no": step.get("line_no", 1),
        "ordinal": step.get("ordinal", 0),
        "normalized_type": step.get("normalized_type", ""),
    }

