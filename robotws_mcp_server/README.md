# RobotWS MCP Server

Standalone read-only MCP server for indexing `robotws` and building generation context for Cursor.

The first version does not call an LLM. It scans Robot Framework and Python files, stores structured metadata in SQLite, identifies team style profiles, and returns context that Cursor's LLM can use to explain or draft Robot Framework testcases in the correct team style.

## Scope

- Index `robotws` as an external source.
- Keep generated indexes under `data/indexes/`.
- Never write into `robotws`.
- Keep AI provider interfaces disabled by default for future Insights Fusion/OpenAI/internal LLM integration.

## Quick Start

```powershell
cd C:\TA\robotws_mcp_server
python -m pip install -e .
python -m robotws_mcp.indexer --robotws-root C:\TA\robotws --profile Hangzhou_SG6_Common --dry-run
python -m robotws_mcp.indexer --robotws-root C:\TA\robotws --profile Hangzhou_SG6_Common --dry-run --status confirmed --top 0 --list-paths
python -m robotws_mcp.indexer --robotws-root C:\TA\robotws --profile Hangzhou_SG6_Common --dry-run --case-type TMO --top 0 --list-paths
python -m robotws_mcp.indexer --robotws-root C:\TA\robotws --profile Hangzhou_SG6_Common --write-index
python -m robotws_mcp.query get-generation-context --requirement "create SG6 TMO DL SFTP KPI testcase" --profile Hangzhou_RRM_SG6_TMO
python -m robotws_mcp.api --db-path data\indexes\robotws.sqlite3 --host 127.0.0.1 --port 8051
```

Local API smoke test:

```powershell
Invoke-WebRequest http://127.0.0.1:8051/health
Invoke-WebRequest http://127.0.0.1:8051/version
```

## MCP Tools

- `identify_robotws_profile`
- `discover_sg6_features`
- `get_sg6_discovery_report`
- `search_robot_cases`
- `search_robot_keywords`
- `get_case_pattern`
- `trace_keyword_usage`
- `find_taf_library_usage`
- `get_style_profile`
- `get_generation_context`
- `validate_generated_case_style`

## HTTP API Endpoints

- `GET /health`
- `GET /version`
- `GET /profiles`
- `GET /discovery/sg6`
- `POST /query/generation-context`
- `POST /query/search-cases`
- `POST /query/search-keywords`
- `POST /query/validate-style`

## Configuration

The SG6 profile set is stored under `config/profiles/`:

- `Hangzhou_SG6_Common`: common SG6 ownership and resource boundary.
- `Hangzhou_RRM_SG6_Feature`: RRM feature testcase style profile.
- `Hangzhou_RRM_SG6_TMO`: RRM `None_Feature_SG6` testcase style profile.
- `Hangzhou_SISO_SG6_Feature`: SISO feature testcase style profile.
- `Hangzhou_SISO_SG6_TMO`: SISO `None_Feature_SG6` testcase style profile.

`Hangzhou_SG6_Common` is the indexer entry profile for SG6 discovery. Its `feature_allowlist` is the only SG6 testcase pool source. The area/type profiles are used for generation context and style validation.

Generated SQLite index defaults to:

`data/indexes/robotws.sqlite3`

## Non-Goals For MVP

- No direct LLM call.
- No execution on testlines.
- No modification of `robotws`.
- No automatic commit or publishing to GitHub.
