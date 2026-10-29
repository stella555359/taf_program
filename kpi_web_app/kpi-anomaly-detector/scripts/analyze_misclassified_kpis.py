#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Analyze history records to find misclassified KPIs
Identify KPIs that should use different detection strategies
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from collections import defaultdict


def load_history_data(history_path: Path) -> list:
    """Load history records"""
    with open(history_path, encoding='utf-8') as f:
        return json.load(f)


def load_classification(excel_path: Path) -> pd.DataFrame:
    """Load KPI classification"""
    return pd.read_excel(excel_path)


def analyze_kpi_characteristics(history_data: list) -> dict:
    """Analyze KPI characteristics across all history records"""
    kpi_stats = defaultdict(lambda: {
        'name': '',
        'means': [],
        'cvs': [],
        'stds': [],
        'mins': [],
        'maxs': [],
        'ranges': [],  # within-file range
        'consistencies': [],
        'raw_samples': []
    })
    
    for rec in history_data:
        kpi_data = rec.get('kpi_data', {})
        for code, info in kpi_data.items():
            stats = kpi_stats[code]
            stats['name'] = info.get('kpi_name', '')
            
            mean = info.get('mean')
            cv = info.get('cv')
            raw = info.get('raw_data', '')
            
            if mean is not None:
                stats['means'].append(mean)
            if cv is not None:
                stats['cvs'].append(cv)
            
            if raw:
                try:
                    values = [float(v) for v in raw.split(',') if v.strip()]
                    if values:
                        stats['mins'].append(min(values))
                        stats['maxs'].append(max(values))
                        stats['ranges'].append(max(values) - min(values))
                        stats['stds'].append(np.std(values))
                        stats['raw_samples'].append(values)
                except:
                    pass
            
            stats['consistencies'].append(info.get('consistency', ''))
    
    return dict(kpi_stats)


def classify_by_data_characteristics(code: str, stats: dict) -> dict:
    """Determine recommended classification based on data characteristics"""
    result = {
        'code': code,
        'name': stats['name'],
        'recommended_type': None,
        'recommended_strategy': None,
        'reason': '',
        'data_profile': {}
    }
    
    means = [m for m in stats['means'] if m is not None]
    if not means:
        result['reason'] = 'No data'
        return result
    
    mean_of_means = np.mean(means)
    std_of_means = np.std(means) if len(means) > 1 else 0
    ranges = stats['ranges']
    avg_within_range = np.mean(ranges) if ranges else 0
    
    # Data profile
    result['data_profile'] = {
        'mean': mean_of_means,
        'mean_std': std_of_means,
        'mean_range': max(means) - min(means) if len(means) > 1 else 0,
        'avg_within_file_range': avg_within_range,
        'cv_mean': np.mean([abs(c) for c in stats['cvs'] if c]) if stats['cvs'] else None,
        'n_records': len(means)
    }
    
    # Classification logic
    abs_mean = abs(mean_of_means)
    
    # 1. Floor saturated (all zeros or near zero with floor behavior)
    if abs_mean < 0.001 and avg_within_range < 0.001:
        result['recommended_type'] = 'floor_saturated'
        result['recommended_strategy'] = 'ABS_THRESHOLD'
        result['reason'] = 'All values near zero (floor)'
        return result
    
    # 2. Ceiling saturated (near 100% or 1.0)
    if 99 < mean_of_means <= 100.5 or (0.99 < mean_of_means <= 1.005):
        if avg_within_range < 1:  # Very stable near ceiling
            result['recommended_type'] = 'ceiling_saturated'
            result['recommended_strategy'] = 'CEILING_PROXIMITY'
            result['reason'] = 'Values near ceiling (100% or 1.0)'
            return result
    
    # 3. Physical stable (stable physical measurement like dBm, temperature)
    # Characteristics: negative values (dBm), very small relative variation
    relative_variation = std_of_means / abs_mean if abs_mean > 0 else float('inf')
    
    if mean_of_means < 0 and relative_variation < 0.01:  # Negative and very stable
        result['recommended_type'] = 'physical_stable'
        result['recommended_strategy'] = 'PHYSICAL_RANGE'
        result['reason'] = f'Stable physical measurement (mean={mean_of_means:.2f}, rel_var={relative_variation:.4f})'
        return result
    
    if abs_mean > 1 and relative_variation < 0.005:  # Very stable positive values
        result['recommended_type'] = 'physical_stable'
        result['recommended_strategy'] = 'PHYSICAL_RANGE'
        result['reason'] = f'Stable physical measurement (rel_var={relative_variation:.4f})'
        return result
    
    # 4. Low frequency (rare events, mean near 0 but occasional spikes)
    if 0 < mean_of_means < 1 and avg_within_range < 5:
        result['recommended_type'] = 'low_frequency'
        result['recommended_strategy'] = 'WINDOW_COUNT'
        result['reason'] = 'Low frequency events'
        return result
    
    # 5. Config type (discrete values, very few unique values)
    if stats['raw_samples']:
        all_values = [v for sample in stats['raw_samples'] for v in sample]
        unique_count = len(set(all_values))
        if unique_count <= 3 and avg_within_range < 1:
            result['recommended_type'] = 'config_type'
            result['recommended_strategy'] = 'SEMANTIC_RULE'
            result['reason'] = f'Config/discrete values ({unique_count} unique)'
            return result
    
    # 6. Count type (integer counts, typically >= 0)
    if mean_of_means >= 0 and all(m >= 0 for m in means):
        if stats['raw_samples']:
            all_values = [v for sample in stats['raw_samples'] for v in sample]
            if all(v == int(v) for v in all_values if v == v):  # All integers
                result['recommended_type'] = 'count_type'
                result['recommended_strategy'] = 'STANDARD_SPC'
                result['reason'] = 'Integer count values'
                return result
    
    # 7. Ratio type (0-100 or 0-1 range, percentage)
    if 0 <= mean_of_means <= 100:
        if stats['raw_samples']:
            all_values = [v for sample in stats['raw_samples'] for v in sample]
            if all(0 <= v <= 100 for v in all_values):
                result['recommended_type'] = 'ratio_type'
                result['recommended_strategy'] = 'STANDARD_SPC'
                result['reason'] = 'Ratio/percentage values (0-100)'
                return result
    
    # Default: Standard SPC
    result['recommended_type'] = 'unknown'
    result['recommended_strategy'] = 'STANDARD_SPC'
    result['reason'] = 'Default classification'
    
    return result


def find_misclassified_kpis(history_data: list, classification_df: pd.DataFrame) -> list:
    """Find KPIs that may be misclassified based on their data characteristics"""
    
    # Analyze all KPIs from history
    kpi_stats = analyze_kpi_characteristics(history_data)
    
    misclassified = []
    
    for code, stats in kpi_stats.items():
        # Get current classification
        row = classification_df[classification_df['Code'] == code]
        if len(row) == 0:
            continue
        
        current_type = str(row['KPI_Type'].values[0]) if pd.notna(row['KPI_Type'].values[0]) else ''
        current_strategy = str(row['Detection_Strategy'].values[0]) if pd.notna(row['Detection_Strategy'].values[0]) else ''
        
        # Get recommended classification
        recommendation = classify_by_data_characteristics(code, stats)
        
        if not recommendation['recommended_type']:
            continue
        
        # Check for mismatch
        rec_type = recommendation['recommended_type']
        rec_strategy = recommendation['recommended_strategy']
        
        # Normalize for comparison
        current_type_norm = current_type.lower().replace('_', '')
        rec_type_norm = rec_type.lower().replace('_', '')
        
        if current_type_norm != rec_type_norm:
            misclassified.append({
                'code': code,
                'name': stats['name'],
                'current_type': current_type,
                'current_strategy': current_strategy,
                'recommended_type': rec_type,
                'recommended_strategy': rec_strategy,
                'reason': recommendation['reason'],
                'data_profile': recommendation['data_profile']
            })
    
    return misclassified


def main():
    base_dir = Path(__file__).parent.parent
    history_path = base_dir / 'reports' / 'kpi_history_records.json'
    classification_path = base_dir / 'lib' / 'kpi_xml' / 'kpi_classification_v2.xlsx'
    
    print("Loading data...")
    history_data = load_history_data(history_path)
    classification_df = load_classification(classification_path)
    
    print(f"History records: {len(history_data)}")
    print(f"Classification entries: {len(classification_df)}")
    
    print("\nAnalyzing misclassified KPIs...")
    misclassified = find_misclassified_kpis(history_data, classification_df)
    
    print(f"\nFound {len(misclassified)} potentially misclassified KPIs:")
    print("=" * 100)
    
    # Group by current type
    by_current_type = defaultdict(list)
    for m in misclassified:
        by_current_type[m['current_type']].append(m)
    
    for current_type, items in sorted(by_current_type.items()):
        print(f"\n### Currently classified as: {current_type}")
        print("-" * 80)
        for item in items[:10]:  # Show first 10 of each type
            profile = item['data_profile']
            print(f"  {item['code']}: {item['name'][:50]}")
            print(f"    Current: {item['current_type']} / {item['current_strategy']}")
            print(f"    Recommend: {item['recommended_type']} / {item['recommended_strategy']}")
            print(f"    Reason: {item['reason']}")
            if profile:
                print(f"    Data: mean={profile.get('mean', 'N/A'):.4f}, mean_range={profile.get('mean_range', 'N/A'):.4f}")
            print()
        if len(items) > 10:
            print(f"    ... and {len(items) - 10} more")
    
    # Save results
    output_path = base_dir / 'reports' / 'misclassified_kpis_analysis.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(misclassified, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to: {output_path}")
    
    return misclassified


if __name__ == '__main__':
    main()
