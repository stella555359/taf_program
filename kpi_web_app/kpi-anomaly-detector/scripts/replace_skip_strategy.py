#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Replace SKIP strategy with ABS_THRESHOLD for constant-value codes.

SKIP codes are those with σ=0 (constant values) in historical data.
They should use ABS_THRESHOLD because any deviation from the constant value is abnormal.

Created: 2026-02-03 (ivy0203)
"""

import pandas as pd
from pathlib import Path

def replace_skip_in_recommendations():
    """Replace SKIP with ABS_THRESHOLD in strategy_recommendations.xlsx"""
    excel_path = Path('lib/kpi_xml/strategy_recommendations.xlsx')
    
    if not excel_path.exists():
        print(f"File not found: {excel_path}")
        return
    
    # Read all sheets
    with pd.ExcelFile(excel_path) as xls:
        sheets = {}
        for sheet_name in xls.sheet_names:
            sheets[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)
    
    # Update SKIP -> ABS_THRESHOLD in All_Codes sheet
    if 'All_Codes' in sheets:
        df = sheets['All_Codes']
        skip_count = (df['Recommended_Strategy'] == 'SKIP').sum()
        df.loc[df['Recommended_Strategy'] == 'SKIP', 'Recommended_Strategy'] = 'ABS_THRESHOLD'
        df.loc[df['Strategy_Reason'] == 'Constant values (σ=0)', 'Strategy_Reason'] = 'Constant values - any change is anomaly'
        sheets['All_Codes'] = df
        print(f"Updated {skip_count} SKIP -> ABS_THRESHOLD in All_Codes")
    
    # Update summary sheet if exists
    if 'Summary' in sheets:
        summary = sheets['Summary']
        # Find SKIP row and add its count to ABS_THRESHOLD
        skip_row = summary[summary['Recommended_Strategy'] == 'SKIP']
        abs_row = summary[summary['Recommended_Strategy'] == 'ABS_THRESHOLD']
        
        if len(skip_row) > 0 and len(abs_row) > 0:
            skip_count = skip_row['Count'].values[0]
            abs_idx = abs_row.index[0]
            summary.loc[abs_idx, 'Count'] += skip_count
            summary = summary[summary['Recommended_Strategy'] != 'SKIP']
            # Recalculate percentages
            total = summary['Count'].sum()
            summary['Percentage'] = (summary['Count'] / total * 100).round(1)
            sheets['Summary'] = summary
            print(f"Updated Summary: merged SKIP ({skip_count}) into ABS_THRESHOLD")
    
    # Save back
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        for sheet_name, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"Saved {excel_path}")


def replace_skip_in_custom_rules():
    """Replace SKIP with ABS_THRESHOLD in kpi_custom_rules.xlsx"""
    excel_path = Path('lib/kpi_xml/kpi_custom_rules.xlsx')
    
    if not excel_path.exists():
        print(f"File not found: {excel_path}")
        return
    
    # Read all sheets
    with pd.ExcelFile(excel_path) as xls:
        sheets = {}
        for sheet_name in xls.sheet_names:
            sheets[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)
    
    total_updated = 0
    for sheet_name, df in sheets.items():
        if 'Default_Strategy' in df.columns:
            skip_count = (df['Default_Strategy'] == 'SKIP').sum()
            if skip_count > 0:
                df.loc[df['Default_Strategy'] == 'SKIP', 'Default_Strategy'] = 'ABS_THRESHOLD'
                sheets[sheet_name] = df
                print(f"  {sheet_name}: {skip_count} SKIP -> ABS_THRESHOLD")
                total_updated += skip_count
    
    if total_updated > 0:
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            for sheet_name, df in sheets.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"Total updated: {total_updated} in {excel_path}")
    else:
        print(f"No SKIP found in {excel_path}")


def update_kpi_types_remove_skip():
    """
    Instructions to update kpi_types.py:
    
    1. In DetectionStrategy enum:
       - Keep SKIP but mark as deprecated
       - Or remove completely
    
    2. In normalize_strategy():
       - Map SKIP -> ABS_THRESHOLD
    
    3. In LEGACY_STRATEGY_MAP:
       - Already handled by normalize_strategy
    """
    print("\n" + "="*60)
    print("Manual update needed in scripts/kpi_detector/kpi_types.py:")
    print("="*60)
    print("""
1. In normalize_strategy() function, add:
   if strategy in ('SKIP', DetectionStrategy.SKIP):
       return DetectionStrategy.ABS_THRESHOLD

2. Optionally, mark SKIP as deprecated in comments:
   SKIP = "SKIP"  # DEPRECATED: Use ABS_THRESHOLD instead
""")


def main():
    print("Replacing SKIP strategy with ABS_THRESHOLD...")
    print("="*60)
    
    replace_skip_in_recommendations()
    print()
    replace_skip_in_custom_rules()
    
    update_kpi_types_remove_skip()
    
    print("\n" + "="*60)
    print("Done! SKIP strategy replaced with ABS_THRESHOLD.")
    print("="*60)


if __name__ == '__main__':
    main()
