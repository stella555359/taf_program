#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Analyze RTWP KPIs from history records"""

import json
from pathlib import Path

def main():
    history_path = Path(__file__).parent.parent / 'reports' / 'kpi_history_records.json'
    data = json.load(open(history_path, encoding='utf-8'))
    
    # 收集所有RTWP数据进行统计分析
    all_rtwp = {}
    for rec in data:
        kpi_data = rec.get('kpi_data', {})
        for code, info in kpi_data.items():
            if 'RTWP for UL Spatial stream' in str(info.get('kpi_name', '')):
                if code not in all_rtwp:
                    all_rtwp[code] = {
                        'name': info.get('kpi_name'), 
                        'means': [], 
                        'cvs': [], 
                        'consistencies': [],
                        'raw_samples': []
                    }
                all_rtwp[code]['means'].append(info.get('mean'))
                all_rtwp[code]['cvs'].append(info.get('cv'))
                all_rtwp[code]['consistencies'].append(info.get('consistency'))
                if info.get('raw_data'):
                    all_rtwp[code]['raw_samples'].append(info.get('raw_data'))
    
    print('RTWP KPI Analysis (RTWP for UL Spatial stream)')
    print('='*80)
    print(f'Found {len(all_rtwp)} unique RTWP counters\n')
    
    for code, info in list(all_rtwp.items()):
        means = [m for m in info['means'] if m is not None]
        cvs = [c for c in info['cvs'] if c is not None]
        cons = info['consistencies']
        
        name = info['name']
        print(f'{code}: {name}')
        
        if means:
            print(f'  Means across files: min={min(means):.2f}, max={max(means):.2f}, range={max(means)-min(means):.4f}')
        
        if cvs:
            print(f'  CVs (first 5): {[round(c, 4) for c in cvs[:5]]}')
        
        print(f'  Consistency results: {dict((c, cons.count(c)) for c in set(cons))}')
        
        # Show raw data sample
        if info['raw_samples']:
            raw = info['raw_samples'][0]
            values = [float(v) for v in raw.split(',') if v]
            print(f'  Raw data sample: {values[:6]}...')
            if len(values) > 1:
                val_range = max(values) - min(values)
                print(f'  Within-file range: {val_range:.4f}')
        print()

if __name__ == '__main__':
    main()
