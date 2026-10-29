"""CLI entry point for building the Layer 2 graph index."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from robotws_mcp.layer2.dependency import TafDependencyPropagator
from robotws_mcp.layer2.graph_builder import Layer2GraphBuilder
from robotws_mcp.layer2.input_loader import Layer1InputLoader
from robotws_mcp.layer2.sqlite_store import Layer2SQLiteStore


def build_layer2_graph(
    layer1_db: str | Path,
    db_path: str | Path = "data/indexes/robotws_layer2_graph.sqlite3",
    include_excluded: bool = False,
    profile: str = "Hangzhou_SG6_Common",
) -> dict[str, object]:
    graph_input = Layer1InputLoader(layer1_db).load(include_excluded=include_excluded)
    nodes, edges, resolutions, summary = Layer2GraphBuilder(graph_input).build()
    dependency_summaries = TafDependencyPropagator(graph_input, resolutions).build_summaries()
    for item in dependency_summaries:
        summary.dependency_summary_counts[item.impl_type] = summary.dependency_summary_counts.get(item.impl_type, 0) + 1
    summary.sqlite_path = str(db_path)

    store = Layer2SQLiteStore(db_path)
    store.initialize()
    store.clear()
    store.insert_nodes(nodes)
    store.insert_edges(edges)
    store.insert_resolution_results(resolutions)
    store.insert_dependency_summaries(dependency_summaries)
    store.set_build_info(
        {
            "source_layer1_db_path": str(layer1_db),
            "profile": profile,
            "layer2_schema_version": 1,
            "layer1_record_count": len(graph_input.records),
            "node_count": len(nodes),
            "edge_count": len(edges),
            "resolution_status_counts": dict(Counter(result.resolution_status for result in resolutions)),
            "dependency_summary_counts": summary.dependency_summary_counts,
        }
    )
    return summary.to_dict()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Layer 2 keyword graph from Layer 1 SQLite records.")
    parser.add_argument("--layer1-db", default="data/indexes/robotws_layer1_v2.sqlite3", help="Layer 1 SQLite path.")
    parser.add_argument("--db-path", default="data/indexes/robotws_layer2_graph.sqlite3", help="Layer 2 SQLite path.")
    parser.add_argument("--profile", default="Hangzhou_SG6_Common", help="Profile label stored in build metadata.")
    parser.add_argument("--include-excluded", action="store_true", help="Include Layer 1 records outside generation boundary.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = build_layer2_graph(
        layer1_db=args.layer1_db,
        db_path=args.db_path,
        include_excluded=args.include_excluded,
        profile=args.profile,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

