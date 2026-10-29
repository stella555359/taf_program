# KPI Anomaly Detector

5G NR base station KPI/Counter anomaly detection tool using Statistical Process Control (SPC) and type-based classification. Analyzes Excel data files, compares with historical records, and generates interactive HTML reports.

> **Version**: 2.1.0 (ivy0126)  
> **Repository**: https://wrgitlab.ext.net.nokia.com/w1qin/kpi-anomaly-detector

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Input File Format](#input-file-format)
- [Output Reports](#output-reports)
- [Configuration](#configuration)
- [HTML Report Shortcuts](#html-report-keyboard-shortcuts)
- [Technical Details](#technical-details)
- [Git Workflow](#git-workflow)

---

## Features

- **Consistency Analysis**: CV (Coefficient of Variation) based consistency checking across multiple test runs
- **T-Test Analysis**: Statistical comparison with historical baseline data
- **Shewhart Control Charts**: SPC rules (8 Western Electric rules) for anomaly detection
- **Type-based Detection**: KPI classification (10 types) with tailored detection strategies
- **Guard Rails**: Hard validation checks (GR-M1 magnitude, GR-S1 overlap, etc.)
- **Historical Tracking**: Track changes across multiple test runs with scenario filtering
- **Interactive HTML Reports**: With keyboard shortcuts for filtering and dual chart views

---

## Project Structure

```
kpi-anomaly-detector/
│
├── scripts/                          # Main scripts directory
│   ├── run_detector.py               # 🚀 Main entry point (run this)
│   └── kpi_detector/                 # Core package
│       ├── __init__.py               # Package exports
│       ├── config.py                 # Configuration (paths, thresholds)
│       ├── detector.py               # Main detector class (orchestrates pipeline)
│       ├── shewhart.py               # Shewhart control chart rules (8 SPC rules)
│       ├── kpi_types.py              # KPI classification system (10 types)
│       ├── guard_rails.py            # Hard validation checks
│       ├── utils.py                  # Utility functions
│       ├── excel_report.py           # Excel report generator
│       └── html_report.py            # Interactive HTML report generator
│
├── data/                             # 📂 Input: Put Excel data files here
│   ├── scenario_group_1/             # Organize by test scenario (recommended)
│   ├── scenario_group_2/
│   └── ...
│
├── reports/                          # 📊 Output: Generated reports
│   ├── *_trend_viewer.html           # Interactive HTML reports
│   ├── *_analysis.xlsx               # Excel analysis reports
│   └── kpi_history_records.json      # Historical data (auto-maintained)
│
├── lib/                              # Library files
│   └── kpi_xml/                      # KPI/Counter definitions
│       ├── PMKPI_SBTS26R2_5G.xml     # KPI definitions
│       ├── PMPegs_SBTS26R2_5G.xml    # Counter definitions
│       └── kpi_classification_v2.xlsx # Classification rules
│
├── docs/                             # Documentation and changelogs
│   └── changelog_*.md                # Daily development logs
│
└── README.md                         # This file
```

---

## Installation

### Prerequisites

- **Python**: 3.8 or higher
- **pip**: Python package manager

### Required Python Libraries

```bash
pip install pandas numpy scipy openpyxl
```

| Library | Version | Purpose |
|---------|---------|---------|
| `pandas` | ≥1.3.0 | Data manipulation and analysis |
| `numpy` | ≥1.20.0 | Numerical computations |
| `scipy` | ≥1.7.0 | Statistical tests (t-test, etc.) |
| `openpyxl` | ≥3.0.0 | Excel file I/O |

### Optional: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install pandas numpy scipy openpyxl
```

---

## Quick Start

### 1. Place Input Files

Put your Excel data files in the `data/` directory. You can organize them in subdirectories by test scenario:

```
data/
├── 7UEs_SFTPDL/
│   ├── 0129.1_26R2.0126.7_T076.SCF.T080_7UEs_SFTPDL_1csv8run.xlsx
│   └── 0130.1_26R2.0126.7_T076.SCF.T080_7UEs_SFTPDL_1csv8run.xlsx
└── 32UEs_httpDLUL/
    ├── 0128.1_26R2.0127.2_T076.SCF.26R1psot5_32UEs_httpDLUL.fixed30m_1csv8run.xlsx
    └── 0129.1_26R1.0434.47_T076.SCF.26R1psot5_32UEs_httpDLUL.fixed30m_1csv8run.xlsx
```

### 2. Run the Detector

```bash
cd scripts
python run_detector.py
```

Interactive prompts will guide you to:
1. Select a directory (or root `data/`)
2. Select file(s) to analyze (supports `1`, `1,3,5`, `1-5` syntax)

### 3. View Reports

Reports are saved to `reports/` directory:
- **HTML Report**: `*_trend_viewer.html` - Open in browser for interactive analysis
- **Excel Report**: `*_analysis.xlsx` - Detailed data tables

---

## Input File Format

### Filename Convention

Files should include a detectable test config and scenario segment for proper history matching:

```
{prefix}_{version}_{testconfig}_{UEs}_{scenario}_{runs}.xlsx
```

**Example**:
```
0129.1_26R2.0126.7_T076.SCF.T080_7UEs_SFTPDL_1csv8run.xlsx
│      │           │            │     │       └── Run info
│      │           │            │     └── Test scenario
│      │           │            └── UE count
│      │           └── Test configuration (T076/T080/T073/etc.)
│      └── Software version
└── Date prefix (MMDD.seq)
```

Another supported example:

```
exec20260325T120349_SBTS26R3.ENB.9999.260319.000005_T813.SCF.T813.gNB.25R3.20260224_7UE_DL_Burst_1csv.xlsx
```

**Matching Regex**:
```
(T\d+\.SCF(?:\.[^_]+)*)_(.+?)_(\d+csv(?:\d+run)?)
```

> ⚠️ **Important**: History matching uses the same `environment + scenario` group, derived from the `Txxx.SCF...` segment and the scenario segment before the `csv` suffix. Different environments or scenarios are analyzed independently even when all records share one JSON file.

### Excel Data Format

The input Excel file must contain:

| Column | Required | Description |
|--------|----------|-------------|
| `Code` | ✅ Yes | KPI/Counter code (e.g., `NR_5089e`, `M70017C33007`) |
| `KPI Name` | Optional | Human-readable name |
| `T076.*` / `T080.*` / `T073.*` / `T283.*` / `T813.*` / `T816.*` / `T284.*` | ✅ Yes | Data columns (one per test run) |

**Supported Data Column Prefixes**: `T076`, `T080`, `T073`, `T283`, `T813`, `T816`, `T284`

**Code Patterns**:
- **KPI**: `NR_XXXXx` or `SCOUT_NR_XXXXx` (XXXX = 2-4 digits, x = letter)
- **Counter**: `MxxxxxCxxxxx` (M + 5 digits + C + 1-5 digits)

---

## Output Reports

### HTML Report (`*_trend_viewer.html`)

Interactive report with:
- **Left Panel**: Severity statistics, type filters, searchable KPI list
- **Right Panel**: Dual chart views (Data Detail + SPC Control Chart)
- **Keyboard shortcuts** for quick navigation

### Excel Report (`*_analysis.xlsx`)

Contains multiple sheets:
- `Summary`: Overall statistics
- `All Codes`: Full analysis results
- `Consistency`: CV analysis details
- `T-Test`: Statistical comparison results
- `History Comparison`: Changes from previous run

### History File (`kpi_history_records.json`)

Auto-maintained JSON file storing historical KPI data for trend analysis. **Do not manually edit**.

---

## Configuration

Configuration is in `scripts/kpi_detector/config.py`:

```python
# Analysis Thresholds
DEFAULT_CV_THRESHOLD = 5.0         # CV threshold percentage
DEFAULT_P_VALUE_THRESHOLD = 0.05   # P-value threshold for t-test

# Severity Levels
# - Normal: Within historical mean ±2σ
# - Suspicious: Exceeds ±2σ but not ±3σ
# - Regression: Exceeds ±3σ or trend deviation
# - NoHistory: Insufficient historical data (<2 records)
```

---

## HTML Report Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `/` | Focus search box |
| `K` | Filter KPI codes only |
| `C` | Filter Counter codes only |
| `A` | Show all codes |
| `1` | Switch to Data Detail Chart |
| `2` | Switch to SPC Control Chart |
| `Esc` | Close modal / Clear focus |
| `↑` / `↓` | Navigate KPI list |

---

## Technical Details

### Detection Pipeline

```
Load Excel → CV Analysis → T-Test → Type-based Detection → Guard Rails → SPC Analysis → Generate Reports
```

### KPI Classification Types

| Type | Description | Detection Strategy |
|------|-------------|-------------------|
| `CEILING_SATURATED` | ~100% success rates | NO SPC/T-test (σ=0) |
| `FLOOR_SATURATED` | ~0 counts | NO SPC/T-test (σ=0) |
| `COUNT_TYPE` | Discrete counts | RANGE + CONTEXT |
| `RATIO_TYPE` | 0-100% non-saturated | RELATIVE CHANGE |
| `PHYSICAL_STABLE` | dB/dBm metrics | ABS_DELTA + TREND |
| `THROUGHPUT_TYPE` | MB/bytes | QUANTILES (right-skewed) |

### Shewhart Control Rules

| Rule | Description | Trigger |
|------|-------------|---------|
| Rule 1 | Out of control | Single point exceeds ±3σ (UCL/LCL) |
| Rule 2 | Warning zone | 3 consecutive points exceed ±2σ (same side) |
| Rule 3 | Trend detection | 4 consecutive monotonic points |
| Rule 4 | Centerline shift | 3 consecutive points same side of CL |

### Zone System

| Zone | Range | Status |
|------|-------|--------|
| Zone C | ±1σ | 🟢 Normal |
| Zone B | ±1σ ~ ±2σ | 🟡 Attention |
| Zone A | ±2σ ~ ±3σ | 🟠 Warning |
| OutOfControl | > ±3σ | 🔴 Out of control |

---

## Git Workflow

### Clone Repository

```bash
git clone https://wrgitlab.ext.net.nokia.com/w1qin/kpi-anomaly-detector.git
cd kpi-anomaly-detector
```

### Daily Workflow

```bash
# Pull latest changes
git pull origin main

# Make changes...

# Commit changes
git add .
git commit -m "feat: add new feature description"

# Push to remote
git push origin main
```

### Commit Convention

```
feat: New feature
fix: Bug fix
docs: Documentation update
refactor: Code refactoring
test: Add tests
chore: Maintenance tasks
```

### Rollback to Previous Version

```bash
# View commit history
git log --oneline

# Rollback to specific commit
git checkout <commit-hash>

# Or reset (destructive)
git reset --hard <commit-hash>
```

---

## Command Line Options

```bash
# Interactive mode (default)
python run_detector.py

# Analyze specific file
python run_detector.py path/to/file.xlsx

# Skip HTML report generation
python run_detector.py --no-html

# Combine options
python run_detector.py data/test.xlsx --no-html
```

---

## Flask Portal

This repository now includes a Flask-based portal for browser-based KPI analysis. The KPI detector is the first portal module and lives under a dedicated workspace route instead of being the root app itself.

### Features

- Upload `.xlsx` KPI files from a browser
- Run the existing detector pipeline without rewriting analysis logic
- Persist generated HTML and Excel artifacts on disk
- Keep a searchable run history in SQLite for front-end listing
- Expose a portal landing page at `/` and the KPI workspace at `/kpi/`
- Keep the app ready for additional Flask modules without growing one giant `app.py`

### Files

- `webapp/app.py` - compatibility entry point for local start and WSGI
- `webapp/portal/app_factory.py` - Flask application factory
- `webapp/portal/blueprints/` - portal and KPI workspace blueprints
- `webapp/portal/services/kpi_analysis_service.py` - shared KPI analysis service layer
- `webapp/templates/` - HTML templates
- `webapp/static/styles.css` - Portal and workspace styling
- `requirements-web.txt` - Python dependencies for the dashboard
- `scripts/deploy_web_dashboard.sh` - Debian deployment helper script
- `docs/debian_web_deployment.md` - Debian deployment guide
- `docs/deploy_10_21_41_175_checklist.md` - Copy-paste deployment checklist for server `10.21.41.175`

If the server's default `http://host` address is already occupied, use `http://10.21.41.175:8088` as the deployment target address.

### Local Start

```bash
pip install -r requirements-web.txt
python webapp/app.py
```

Then open `http://127.0.0.1:8000`.

- `http://127.0.0.1:8000/` - Portal home
- `http://127.0.0.1:8000/kpi/` - KPI detector workspace

### Persistence Model

- `webapp_data/reports/` stores generated HTML, Excel, and the detector's JSON history file
- `webapp_data/analysis_history.db` stores run metadata for the front-end

This split is intentional: report artifacts remain files, while queryable history is stored in SQLite.

### Portal Architecture

- `portal.home` serves the landing page and module navigation
- `kpi` blueprint owns upload, analysis, rerun, artifact, and dashboard routes
- Shared request-independent logic lives in `webapp/portal/services/kpi_analysis_service.py`
- `webapp/app.py` remains a thin compatibility wrapper so existing start commands do not change

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `No data columns found` | Ensure Excel has columns starting with T076/T080/T073/T283/T813/T816/T284 |
| `No same-scenario history` | First run for this scenario - baseline will be established |
| `Module not found` | Run `pip install pandas numpy scipy openpyxl` |
| `Permission denied` | Close Excel files before running analysis |

### Debug Mode

For detailed logging, modify `scripts/kpi_detector/config.py`:

```python
DEBUG = True  # Enable verbose output
```

---

## License

Internal use only - Nokia Confidential.

---

## Contact

- **Author**: W1Qin
- **Repository**: https://wrgitlab.ext.net.nokia.com/w1qin/kpi-anomaly-detector
- **Issues**: Submit via GitLab Issues

---

*Last updated: 2026-02-02*
