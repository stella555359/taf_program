#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Update dB/dBm KPIs to physical_stable type with STANDARD_SPC strategy

For dB/dBm physical quantities:
- KPI_Type: physical_stable
- Detection_Strategy: STANDARD_SPC

The physical floor constraint (1dB) is applied in detector.py
"""

import pandas as pd
from pathlib import Path

# Paths
LIB_DIR = Path(__file__).parent.parent / 'lib' / 'kpi_xml'
CLASSIFICATION_FILE = LIB_DIR / 'kpi_classification_v2.xlsx'
CUSTOM_RULES_FILE = LIB_DIR / 'kpi_custom_rules.xlsx'


def update_db_kpis():
    """Update dB/dBm KPIs in both Excel files"""
    
    # Read classification file
    print("Reading kpi_classification_v2.xlsx...")
    df_class = pd.read_excel(CLASSIFICATION_FILE)
    
    # Find dB/dBm KPIs
    db_mask = df_class['Units'].str.contains('dB', na=False, case=False)
    db_codes = df_class.loc[db_mask, 'Code'].tolist()
    
    print(f"\nFound {len(db_codes)} dB/dBm KPIs")
    
    # Show current status
    print("\nCurrent KPI_Type distribution for dB/dBm KPIs:")
    print(df_class.loc[db_mask, 'KPI_Type'].value_counts())
    print("\nCurrent Detection_Strategy distribution for dB/dBm KPIs:")
    print(df_class.loc[db_mask, 'Detection_Strategy'].value_counts())
    
    # Update kpi_classification_v2.xlsx
    print("\n" + "="*60)
    print("Updating kpi_classification_v2.xlsx...")
    
    # Update KPI_Type to physical_stable
    df_class.loc[db_mask, 'KPI_Type'] = 'physical_stable'
    
    # Update Detection_Strategy to STANDARD_SPC
    df_class.loc[db_mask, 'Detection_Strategy'] = 'STANDARD_SPC'
    
    # Save
    df_class.to_excel(CLASSIFICATION_FILE, index=False)
    print(f"Updated {len(db_codes)} KPIs in kpi_classification_v2.xlsx")
    
    # Read custom rules file
    print("\n" + "="*60)
    print("Updating kpi_custom_rules.xlsx...")
    df_custom = pd.read_excel(CUSTOM_RULES_FILE)
    
    # Find dB/dBm codes in custom rules
    custom_db_mask = df_custom['Code'].isin(db_codes)
    custom_db_count = custom_db_mask.sum()
    
    if custom_db_count > 0:
        print(f"Found {custom_db_count} dB/dBm KPIs in custom rules")
        
        # Update Default_Strategy
        df_custom.loc[custom_db_mask, 'Default_Strategy'] = 'STANDARD_SPC'
        
        # Disable custom rules (use classification strategy)
        df_custom.loc[custom_db_mask, 'Enabled'] = False
        
        # Save
        df_custom.to_excel(CUSTOM_RULES_FILE, index=False)
        print(f"Updated {custom_db_count} KPIs in kpi_custom_rules.xlsx")
    else:
        print("No dB/dBm KPIs found in custom rules")
    
    # Verify alignment
    print("\n" + "="*60)
    print("Verification...")
    
    # Reload
    df_class = pd.read_excel(CLASSIFICATION_FILE)
    df_custom = pd.read_excel(CUSTOM_RULES_FILE)
    
    db_mask = df_class['Units'].str.contains('dB', na=False, case=False)
    
    print("\nAfter update - KPI_Type distribution for dB/dBm KPIs:")
    print(df_class.loc[db_mask, 'KPI_Type'].value_counts())
    print("\nAfter update - Detection_Strategy distribution for dB/dBm KPIs:")
    print(df_class.loc[db_mask, 'Detection_Strategy'].value_counts())
    
    # List the updated codes
    print(f"\n{'='*60}")
    print(f"Updated dB/dBm KPI codes ({len(db_codes)} total):")
    for i, code in enumerate(sorted(db_codes)[:20]):
        print(f"  {code}")
    if len(db_codes) > 20:
        print(f"  ... and {len(db_codes) - 20} more")
    
    return db_codes


if __name__ == '__main__':
    update_db_kpis()
