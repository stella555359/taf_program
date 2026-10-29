#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unified Strategy Configuration Cleanup (ivy0205)

Goals:
1. Consolidate all strategy configuration into kpi_classification_v2.xlsx
2. Remove legacy strategies (SEMANTIC_RULE, TAIL_AWARE, QUANTILES, etc.)
3. Map all strategies to the 7 valid core strategies
4. Delete strategy_recommendations.xlsx (not used by code)

Valid strategies (7 total):
- ABS_THRESHOLD: For saturated data (ceiling/floor)
- IQR: For high-variance/non-normal data
- POISSON: For count/discrete data
- RELATIVE: For ratio/percentage data
- STANDARD_SPC: Default σ-based SPC
- Z_SCORE: For moderate variance
- KS_TEST: For distribution comparison

Legacy strategy mapping:
- SEMANTIC_RULE → POISSON (for count data) or STANDARD_SPC
- TAIL_AWARE → IQR
- QUANTILES → IQR
- RANGE_CONTEXT → IQR
- RELATIVE_CHANGE → RELATIVE
- ABS_DELTA_TREND → Z_SCORE
- WINDOW_COUNT → POISSON
"""

import pandas as pd
from pathlib import Path
import shutil

# Paths
LIB_DIR = Path(__file__).parent.parent / 'lib' / 'kpi_xml'
CLASSIFICATION_FILE = LIB_DIR / 'kpi_classification_v2.xlsx'
CUSTOM_RULES_FILE = LIB_DIR / 'kpi_custom_rules.xlsx'
STRATEGY_RECO_FILE = LIB_DIR / 'strategy_recommendations.xlsx'
BACKUP_DIR = LIB_DIR / 'backup_ivy0205'

# Valid strategies
VALID_STRATEGIES = {
    'ABS_THRESHOLD', 'IQR', 'POISSON', 'RELATIVE', 
    'STANDARD_SPC', 'Z_SCORE', 'KS_TEST'
}

# Legacy strategy mapping
LEGACY_MAP = {
    'SEMANTIC_RULE': 'POISSON',      # Most SEMANTIC_RULE are count-based
    'TAIL_AWARE': 'IQR',
    'QUANTILES': 'IQR',
    'RANGE_CONTEXT': 'IQR',
    'RELATIVE_CHANGE': 'RELATIVE',
    'ABS_DELTA_TREND': 'Z_SCORE',
    'WINDOW_COUNT': 'POISSON',
    'SKIP': 'ABS_THRESHOLD',         # Constant data uses absolute check
}

# Specific code overrides (user requested)
SPECIFIC_OVERRIDES = {
    # dB power KPIs → physical_stable + STANDARD_SPC
    'SCOUT_AVG_CB_SRS_Power_WB_BF': ('physical_stable', 'STANDARD_SPC'),
    'SCOUT_NR_2556a': ('physical_stable', 'STANDARD_SPC'),
    'SCOUT_NR_2557a': ('physical_stable', 'STANDARD_SPC'),
    'SCOUT_NR_2558a': ('physical_stable', 'STANDARD_SPC'),
    'SCOUT_AVG_TAS_SRS_Power_WB_BF': ('physical_stable', 'STANDARD_SPC'),
    
    # Count counters → POISSON
    'M55118C07003': (None, 'POISSON'),  # None = keep existing KPI_Type
    'M55118C07004': (None, 'POISSON'),
    'M55142C00525': (None, 'POISSON'),
    'M55187C00001': (None, 'POISSON'),
    'M55190C00001': (None, 'POISSON'),
    'M55187C00002': (None, 'POISSON'),
    'M55190C00002': (None, 'POISSON'),
}


def backup_files():
    """Create backup of original files"""
    BACKUP_DIR.mkdir(exist_ok=True)
    
    for f in [CLASSIFICATION_FILE, CUSTOM_RULES_FILE, STRATEGY_RECO_FILE]:
        if f.exists():
            backup_path = BACKUP_DIR / f.name
            shutil.copy(f, backup_path)
            print(f"Backed up: {f.name}")


def cleanup_classification():
    """Update kpi_classification_v2.xlsx with valid strategies"""
    print("\n" + "="*60)
    print("Cleaning up kpi_classification_v2.xlsx...")
    
    df = pd.read_excel(CLASSIFICATION_FILE)
    
    # Show before stats
    print("\nBefore cleanup - Strategy distribution:")
    print(df['Detection_Strategy'].value_counts())
    
    # Map legacy strategies to valid ones
    updated_count = 0
    for idx, row in df.iterrows():
        code = str(row.get('Code', '')).strip()
        strategy = str(row.get('Detection_Strategy', '')).strip().upper()
        
        # Check for specific overrides first
        if code in SPECIFIC_OVERRIDES:
            kpi_type, new_strategy = SPECIFIC_OVERRIDES[code]
            if new_strategy:
                df.at[idx, 'Detection_Strategy'] = new_strategy
            if kpi_type:
                df.at[idx, 'KPI_Type'] = kpi_type
            updated_count += 1
            continue
        
        # Map legacy strategy
        if strategy in LEGACY_MAP:
            df.at[idx, 'Detection_Strategy'] = LEGACY_MAP[strategy]
            updated_count += 1
    
    # Save
    df.to_excel(CLASSIFICATION_FILE, index=False)
    
    # Show after stats
    print(f"\nUpdated {updated_count} rows")
    print("\nAfter cleanup - Strategy distribution:")
    df = pd.read_excel(CLASSIFICATION_FILE)
    print(df['Detection_Strategy'].value_counts())
    
    # Verify all strategies are valid
    invalid = df[~df['Detection_Strategy'].isin(VALID_STRATEGIES)]
    if len(invalid) > 0:
        print(f"\nWARNING: {len(invalid)} rows have invalid strategies!")
        print(invalid['Detection_Strategy'].value_counts())
    else:
        print("\n✅ All strategies are valid!")


def cleanup_custom_rules():
    """Update kpi_custom_rules.xlsx - clear all overrides since classification is now authoritative"""
    print("\n" + "="*60)
    print("Cleaning up kpi_custom_rules.xlsx...")
    
    df = pd.read_excel(CUSTOM_RULES_FILE)
    
    # Disable all overrides - classification is now the single source of truth
    if 'Enabled' in df.columns:
        df['Enabled'] = False
    
    # Update Default_Strategy to match classification
    df_class = pd.read_excel(CLASSIFICATION_FILE)
    code_to_strategy = dict(zip(df_class['Code'], df_class['Detection_Strategy']))
    
    for idx, row in df.iterrows():
        code = str(row.get('Code', '')).strip()
        if code in code_to_strategy:
            df.at[idx, 'Default_Strategy'] = code_to_strategy[code]
    
    df.to_excel(CUSTOM_RULES_FILE, index=False)
    print("Set all Enabled=False, synced Default_Strategy with classification")


def remove_strategy_recommendations():
    """Remove strategy_recommendations.xlsx (not used by code)"""
    print("\n" + "="*60)
    print("Removing strategy_recommendations.xlsx...")
    
    if STRATEGY_RECO_FILE.exists():
        # Move to backup instead of delete
        backup_path = BACKUP_DIR / STRATEGY_RECO_FILE.name
        shutil.move(STRATEGY_RECO_FILE, backup_path)
        print(f"Moved to backup: {STRATEGY_RECO_FILE.name}")
    else:
        print("File does not exist")


def verify_specific_codes():
    """Verify the specific codes requested by user"""
    print("\n" + "="*60)
    print("Verifying specific codes...")
    
    df = pd.read_excel(CLASSIFICATION_FILE)
    
    for code, (expected_type, expected_strategy) in SPECIFIC_OVERRIDES.items():
        row = df[df['Code'] == code]
        if row.empty:
            print(f"  ⚠️ {code}: NOT FOUND")
            continue
        
        actual_type = row['KPI_Type'].values[0]
        actual_strategy = row['Detection_Strategy'].values[0]
        
        type_ok = expected_type is None or actual_type == expected_type
        strategy_ok = actual_strategy == expected_strategy
        
        status = "✅" if type_ok and strategy_ok else "❌"
        print(f"  {status} {code}: Type={actual_type}, Strategy={actual_strategy}")


def main():
    print("="*60)
    print("Unified Strategy Configuration Cleanup")
    print("="*60)
    
    # Backup first
    backup_files()
    
    # Cleanup classification (main source of truth)
    cleanup_classification()
    
    # Sync custom rules
    cleanup_custom_rules()
    
    # Remove unused file
    remove_strategy_recommendations()
    
    # Verify
    verify_specific_codes()
    
    print("\n" + "="*60)
    print("DONE! Single source of truth: kpi_classification_v2.xlsx")
    print("="*60)


if __name__ == '__main__':
    main()
