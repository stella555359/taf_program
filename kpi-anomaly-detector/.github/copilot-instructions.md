# KPI Anomaly Detector - Copilot Instructions

## Project Overview
5G NR base station KPI/Counter anomaly detection tool using Statistical Process Control (SPC) and type-based classification. Analyzes Excel data files, compares with historical records, and generates interactive HTML reports.

## Architecture

### Core Package Structure
- **Entry Point**: `scripts/run_detector.py` - Interactive CLI for file selection
- **Core Package**: `scripts/kpi_detector/` - Main detection logic
  - `detector.py` - Orchestrates analysis pipeline (CV → T-Test → SPC → Guard Rails)
  - `shewhart.py` - Shewhart control chart rules (8 SPC rules for X-bar charts)
  - `kpi_types.py` - KPI classification system (10 types with detection strategies)
  - `guard_rails.py` - Hard validation checks (GR-M1 magnitude, GR-S1 overlap, etc.)
  - `html_report.py` - Interactive HTML report generation with keyboard shortcuts

### Data Flow
1. Load Excel from `data/` → Extract KPI/Counter columns (T076 prefixed)
2. Load history from `reports/kpi_history_records.json` (scenario-filtered)
3. Classify KPIs by type → Apply type-specific detection strategy
4. Run Guard Rails → Then SPC analysis → Calculate severity
5. Generate reports to `reports/` (Excel + HTML)

## Key Conventions

### KPI Classification Types (in `kpi_types.py`)
```python
# Each type has forbidden statistical methods
CEILING_SATURATED  # ~100% success rates → NO SPC/T-test (σ=0)
FLOOR_SATURATED    # ~0 counts → NO SPC/T-test (σ=0)
COUNT_TYPE         # Discrete counts → RANGE + CONTEXT
RATIO_TYPE         # 0-100% non-saturated → RELATIVE CHANGE
PHYSICAL_STABLE    # dB/dBm metrics → ABS_DELTA + TREND
THROUGHPUT_TYPE    # MB/bytes → QUANTILES (right-skewed)
```

### Code Patterns (in `utils.py`)
- **KPI codes**: `NR_XXXXx` or `SCOUT_NR_XXXXx` (regex: `NR` keyword)
- **Counter codes**: `MxxxxxCxxxxx` (regex: `^M\d{5}C\d{1,5}$`)

### Scenario Matching (in `config.py`)
Filename pattern: `{version}_{config}_{UEs}_{scenario}_Ncsvrun_...`
Only same-scenario historical data is used for comparison.

## Development Commands

```powershell
# Run detector interactively
cd scripts; python run_detector.py

# Analyze specific file
python run_detector.py data/your_file.xlsx

# Skip HTML generation
python run_detector.py --no-html
```

## Critical Implementation Notes


2. **HTML Report JavaScript**: Avoid duplicate `const` declarations in the same scope (caused critical bug in ivy0128). Variables like `unitEl`, `currentUnitEl` must be unique.

3. **History JSON Format**: Records in `reports/kpi_history_records.json` include:
   - `filename`, `timestamp`, `scenario` (UEs + test type)
   - `kpi_data`: dict with `raw_data` (comma-separated values), `mean`, `cv`, etc.

4. **Shewhart Rules** (see `shewhart.py`):
   - Rule 1: Point > ±3σ (UCL/LCL)
   - Rule 2: 3 consecutive > ±2σ same side
   - Rule 3: 4 consecutive monotonic
   - Rule 4: 3 consecutive same side of CL

## External Dependencies
- `pandas`, `numpy`, `scipy` (stats), `openpyxl` (Excel I/O)
- XML definitions in `lib/kpi_xml/` (`PMKPI_SBTS26R2_5G.xml`, `PMPegs_SBTS26R2_5G.xml`)
- **Unified config file**: `lib/kpi_xml/kpi_config_unified.xlsx` (single source of truth)

## File Naming
- Reports: `{date}_{version}_{config}_{scenario}_trend_viewer.html`
- Changelogs: `docs/changelog_YYYYMMDD.md` (Chinese comments accepted)

## Development Workflow Rules

### Commit Strategy
- **Commit after every code change** - Always commit changes immediately after each modification, in case new code introduces errors and rollback is needed.

### Excel File Maintenance (ivy0205 simplified)
- **Single source of truth**: `lib/kpi_xml/kpi_config_unified.xlsx`
  - Contains 2780 codes with Detection_Strategy, Override_Strategy, Enabled columns
  - Override_Strategy with Enabled=True takes precedence over Detection_Strategy
- **Deprecated files** (moved to `lib/kpi_xml/backup_ivy0205/`):
  - `kpi_classification_v2.xlsx` - merged into unified file
  - `kpi_custom_rules.xlsx` - merged into unified file  
  - `strategy_recommendations.xlsx` - not used by code

- **Valid strategies (6 total)**:
  - `ABS_THRESHOLD`: For saturated data (ceiling/floor)
  - `IQR`: For high-variance/non-normal data
  - `POISSON`: For count/discrete data
  - `RELATIVE`: For ratio/percentage data
  - `STANDARD_SPC`: Default σ-based SPC
  - `Z_SCORE`: For moderate variance

- **Removed strategies**:
  - `KS_TEST`: Only 4 codes used it, migrated to STANDARD_SPC/POISSON

- **Legacy strategies are deprecated**: SKIP, SEMANTIC_RULE, TAIL_AWARE, QUANTILES, RANGE_CONTEXT, RELATIVE_CHANGE, ABS_DELTA_TREND, WINDOW_COUNT
  - These are auto-converted to core strategies via `normalize_strategy()` in code

### Daily Changelog
- **Create markdown notes for each day's work** - File: `docs/changelog_YYYYMMDD.md`
- Include: what was changed, why, and a TODO list for remaining tasks
- Reference the changelog format in `docs/changelog_20260128.md`

### Code Change Checklist
Before modifying any code:
1. **Overall thinking first** - Understand the full impact before making changes
2. **Check related functions** - Verify that changes won't break dependent logic
3. **Trace call chain** - Use `list_code_usages` to find all callers of modified functions
4. **Test critical paths** - Especially for `detector.py` → `shewhart.py` → `html_report.py` pipeline

### Language Rules
| Content Type | Chinese Allowed |
|--------------|-----------------|
| Source code (`.py`) | ❌ NO |
| Comments in code | ✅ Yes |
| Changelogs (`.md`) | ✅ Yes |
| Copilot thinking/reasoning | ✅ Yes |

**Important**: Variable names, function names, strings in code must be ASCII only.
