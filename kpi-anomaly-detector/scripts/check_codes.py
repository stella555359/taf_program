#!/usr/bin/env python
# Check specific codes' detection results
import json

with open('../reports/kpi_history_records.json', 'r', encoding='utf-8') as f:
    records = json.load(f)

print(f'Total records: {len(records)}')
for r in records[-3:]:
    print(f"  - {r.get('filename')} @ {r.get('timestamp')}")

# Check specific codes
target_codes = ['SCOUT_C_NR_1442a', 'SCOUT_NR_71b', 'SCOUT_NR_1763b']
print("\n=== Specific Codes Data ===")
for code in target_codes:
    print(f"\n{code}:")
    for r in records[-2:]:
        if code in r.get('kpi_data', {}):
            data = r['kpi_data'][code]
            print(f"  {r['filename'][:40]}...")
            print(f"    mean: {data.get('mean')}, cv: {data.get('cv')}")
            print(f"    raw_data: {data.get('raw_data')[:60]}...")
