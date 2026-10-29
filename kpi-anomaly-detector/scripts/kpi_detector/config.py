# -*- coding: utf-8 -*-
"""
Configuration module for KPI Anomaly Detector
"""

from pathlib import Path

# ========== Directory Configuration ==========
# Base directory (parent of scripts directory, i.e., project root)
BASE_DIR = Path(__file__).parent.parent.parent

# Subdirectory paths
PATHS = {
    'scripts': BASE_DIR / 'scripts',      # Script files
    'data': BASE_DIR / 'data',            # Raw data files (.xlsx)
    'reports': BASE_DIR / 'reports',      # Report output (Excel, HTML)
    'docs': BASE_DIR / 'docs',            # Documentation files (.md)
}

# Ensure directories exist
for path in PATHS.values():
    path.mkdir(parents=True, exist_ok=True)

# ========== Color Definitions ==========
COLORS = {
    'critical': 'FF0000',      # Red - Critical anomaly
    'warning': 'FFA500',       # Orange - Warning
    'suspicious': '9370DB',    # Purple - Suspicious (CV consistent but T-Test Fail)
    'caution': 'FFFF00',       # Yellow - Caution
    'normal': '90EE90',        # Light green - Normal
    'header': '4472C4',        # Blue - Header
    'light_blue': 'ADD8E6',    # Light blue
    'grey': 'D3D3D3',          # Grey
    'improved': '00FF00',      # Bright green - Improved
    'worsened': 'FF6B6B',      # Light red - Worsened
}

# ========== Analysis Thresholds ==========
DEFAULT_CV_THRESHOLD = 5.0         # CV threshold percentage
DEFAULT_P_VALUE_THRESHOLD = 0.05   # P-value threshold for t-test

# ========== History File ==========
HISTORY_FILENAME = 'kpi_history_records.json'

# ========== Filename Pattern for Scenario Matching ==========
# Group 1: Version (26R2.0115.2)
# Group 2: Test config (T076.SCF.26R1post5)
# Group 3: UE count (32UEs)
# Group 4: Scenario description (httpDL_bigShort)
FILENAME_PATTERN = r'(\d{2}R\d\.\d{4}\.\d{1,3})_(T\d+\.SCF\.\w+)[._](\d+UEs)[._](.+?)_\d+csv'
