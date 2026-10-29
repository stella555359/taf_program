#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Debug script to check strategy configuration"""

import pandas as pd
import json

# Check the strategy in kpi_custom_rules.xlsx
df = pd.read_excel('../lib/kpi_xml/kpi_custom_rules.xlsx', sheet_name='1_Custom_Rules')
print("Columns:", df.columns.tolist())
print()

codes = ['M55360C01139', 'M55360C00141']
for code in codes:
    row = df[df['Code'] == code]
    if not row.empty:
        print(f'{code}:')
        for col in df.columns:
            val = row[col].values[0]
            print(f'  {col}: {val}')
    else:
        print(f'{code}: NOT FOUND in 1_Custom_Rules')
    print()

# Also check kpi_classification_v2.xlsx
print("="*60)
print("Checking kpi_classification_v2.xlsx...")
df2 = pd.read_excel('../lib/kpi_xml/kpi_classification_v2.xlsx')
for code in codes:
    row = df2[df2['Code'] == code]
    if not row.empty:
        print(f'{code}:')
        strat_col = [c for c in df2.columns if 'strat' in c.lower()]
        for col in strat_col:
            print(f'  {col}: {row[col].values[0]}')
    else:
        print(f'{code}: NOT FOUND')

# Check historical data
print()
print("="*60)
print("Checking historical data...")
with open('../reports/kpi_history_records.json', 'r') as f:
    history = json.load(f)

for code in codes:
    print(f'\n=== {code} ===')
    for record in history:
        kpi_data = record.get('kpi_data', {})
        if code in kpi_data:
            data = kpi_data[code]
            fname = record.get('filename', 'unknown')
            raw = data.get('raw_data', '')
            print(f"  File: {fname[:60]}")
            print(f"  Raw: {raw[:100]}")
            print(f"  Mean: {data.get('mean')}, CV: {data.get('cv')}")
