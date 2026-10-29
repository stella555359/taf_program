#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Analyze historical KPI data to recommend optimal detection methods

This script analyzes all KPI/Counter codes in history records and recommends:
- IQR method for high-variance data (CV > 10%)
- Poisson method for small count data (mean < 10, integer-like)
- Relative change method for ratio/percentage data
- Standard σ-based SPC for normal data
- Skip detection for saturated data

Output: JSON file with detection method recommendations per code
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
import numpy as np

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from kpi_detector.guard_rails import AlternativeDetectors, DetectionMethod, analyze_data_characteristics


def load_history_records(history_file: Path) -> list:
    """Load history records from JSON file"""
    if not history_file.exists():
        print(f"Error: History file not found: {history_file}")
        return []
    
    with open(history_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def collect_code_data(records: list) -> dict:
    """Collect all data points for each code across all records
    
    Returns:
        {code: {'values': [...], 'kpi_name': str, 'type': str, 'scenarios': [...]}}
    """
    code_data = defaultdict(lambda: {'values': [], 'kpi_name': '', 'type': '', 'scenarios': set()})
    
    for record in records:
        filename = record.get('filename', '')
        kpi_data = record.get('kpi_data', {})
        
        for code, data in kpi_data.items():
            raw_data = data.get('raw_data', '')
            if raw_data:
                try:
                    values = [float(x) for x in raw_data.split(',') if x.strip()]
                    code_data[code]['values'].extend(values)
                except:
                    pass
            
            if data.get('kpi_name'):
                code_data[code]['kpi_name'] = data['kpi_name']
            if data.get('type'):
                code_data[code]['type'] = data['type']
            
            # Extract scenario from filename
            import re
            match = re.search(r'(\d+UEs)[._](.+?)_\d+csv', filename)
            if match:
                scenario = f"{match.group(1)}_{match.group(2)}"
                code_data[code]['scenarios'].add(scenario)
    
    # Convert sets to lists for JSON serialization
    for code in code_data:
        code_data[code]['scenarios'] = list(code_data[code]['scenarios'])
    
    return dict(code_data)


def analyze_and_recommend(code_data: dict) -> dict:
    """Analyze each code and recommend detection method
    
    Returns:
        {code: {
            'kpi_name': str,
            'type': str,
            'recommended_method': str,
            'characteristics': {...},
            'reason': str
        }}
    """
    recommendations = {}
    detector = AlternativeDetectors()
    
    method_counts = defaultdict(int)
    
    for code, data in code_data.items():
        values = data['values']
        
        if not values:
            recommendations[code] = {
                'kpi_name': data['kpi_name'],
                'type': data['type'],
                'recommended_method': 'skip',
                'reason': 'No data values',
                'characteristics': {'valid': False}
            }
            method_counts['skip_no_data'] += 1
            continue
        
        # Analyze characteristics
        chars = analyze_data_characteristics(values)
        
        # Get recommended method
        method = detector.recommend_method(values)
        
        # Build reason
        reasons = []
        if chars['is_small_value']:
            reasons.append(f"small value (mean={chars['mean']:.4f})")
        if chars['is_high_variance']:
            reasons.append(f"high variance (CV={chars['cv']:.1f}%)")
        if chars['is_ratio_like'] and not chars['is_high_variance']:
            reasons.append("ratio/percentage range")
        if chars['is_integer_like'] and chars['mean'] < 10:
            reasons.append("count-like data")
        if chars['unique_values'] <= 2:
            reasons.append("saturated/constant")
        
        recommendations[code] = {
            'kpi_name': data['kpi_name'],
            'type': data['type'],
            'recommended_method': method.value,
            'reason': ', '.join(reasons) if reasons else 'standard distribution',
            'characteristics': {
                'count': int(chars['count']),
                'mean': round(float(chars['mean']), 6),
                'std': round(float(chars['std']), 6),
                'cv': round(float(chars['cv']), 2) if chars['cv'] != float('inf') else None,
                'min': round(float(chars['min']), 6),
                'max': round(float(chars['max']), 6),
                'is_small_value': bool(chars['is_small_value']),
                'is_high_variance': bool(chars['is_high_variance']),
                'is_ratio_like': bool(chars['is_ratio_like']),
                'is_integer_like': bool(chars['is_integer_like']),
                'unique_values': int(chars['unique_values'])
            },
            'scenarios': data['scenarios']
        }
        
        method_counts[method.value] += 1
    
    return recommendations, dict(method_counts)


def find_misclassified_codes(recommendations: dict) -> list:
    """Find codes that might have been misclassified by GR-M1
    
    These are codes with:
    - Small values (mean < 0.1)
    - Non-zero data
    - Would have been flagged by old magnitude_min_value=0.01
    """
    misclassified = []
    
    for code, rec in recommendations.items():
        chars = rec.get('characteristics', {})
        if not chars.get('count'):
            continue
        
        mean_val = chars.get('mean', 0)
        min_val = chars.get('min', 0)
        
        # Codes with mean between 0.001 and 0.1 (would be affected by old threshold)
        if 0.001 <= abs(mean_val) <= 0.1 and min_val > 0:
            misclassified.append({
                'code': code,
                'kpi_name': rec['kpi_name'],
                'type': rec['type'],
                'mean': mean_val,
                'min': min_val,
                'max': chars.get('max'),
                'cv': chars.get('cv'),
                'recommended_method': rec['recommended_method'],
                'reason': rec['reason']
            })
    
    return sorted(misclassified, key=lambda x: x['mean'])


def main():
    """Main entry point"""
    print("=" * 70)
    print("KPI Detection Method Analyzer")
    print("=" * 70)
    
    # Paths
    base_dir = Path(__file__).parent.parent
    history_file = base_dir / 'reports' / 'kpi_history_records.json'
    output_file = base_dir / 'reports' / 'detection_method_recommendations.json'
    
    print(f"\nLoading history from: {history_file}")
    records = load_history_records(history_file)
    print(f"Loaded {len(records)} history records")
    
    if not records:
        return
    
    # Collect data
    print("\nCollecting data for all codes...")
    code_data = collect_code_data(records)
    print(f"Found {len(code_data)} unique codes")
    
    # Analyze and recommend
    print("\nAnalyzing data characteristics and recommending methods...")
    recommendations, method_counts = analyze_and_recommend(code_data)
    
    # Summary
    print("\n" + "=" * 70)
    print("DETECTION METHOD RECOMMENDATIONS SUMMARY")
    print("=" * 70)
    
    total = sum(method_counts.values())
    for method, count in sorted(method_counts.items(), key=lambda x: -x[1]):
        pct = count / total * 100
        print(f"  {method:15s}: {count:5d} ({pct:5.1f}%)")
    
    # Find potentially misclassified codes
    misclassified = find_misclassified_codes(recommendations)
    
    print("\n" + "=" * 70)
    print(f"CODES POTENTIALLY AFFECTED BY OLD GR-M1 THRESHOLD (magnitude_min_value=0.01)")
    print(f"These codes have 0.001 <= mean <= 0.1 with non-zero data")
    print("=" * 70)
    
    if misclassified:
        print(f"\nFound {len(misclassified)} potentially affected codes:\n")
        for item in misclassified[:30]:  # Show first 30
            print(f"  {item['code']:30s} mean={item['mean']:.6f}  CV={item['cv'] or 'N/A':>6}  method={item['recommended_method']}")
            print(f"    {item['kpi_name'][:60]}")
        
        if len(misclassified) > 30:
            print(f"\n  ... and {len(misclassified) - 30} more codes")
    else:
        print("  No potentially affected codes found")
    
    # Save recommendations
    output_data = {
        'summary': {
            'total_codes': len(recommendations),
            'method_distribution': method_counts,
            'potentially_misclassified_count': len(misclassified)
        },
        'misclassified_codes': misclassified,
        'recommendations': recommendations
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n\nRecommendations saved to: {output_file}")
    
    # Print specific codes mentioned by user
    print("\n" + "=" * 70)
    print("SPECIFIC CODES MENTIONED BY USER")
    print("=" * 70)
    
    target_codes = ['SCOUT_C_NR_1442a', 'SCOUT_NR_71b', 'SCOUT_NR_1763b']
    for code in target_codes:
        if code in recommendations:
            rec = recommendations[code]
            chars = rec['characteristics']
            print(f"\n{code}:")
            print(f"  KPI Name: {rec['kpi_name']}")
            print(f"  Type: {rec['type']}")
            print(f"  Mean: {chars.get('mean')}, CV: {chars.get('cv')}")
            print(f"  Range: [{chars.get('min')}, {chars.get('max')}]")
            print(f"  Recommended Method: {rec['recommended_method']}")
            print(f"  Reason: {rec['reason']}")
        else:
            print(f"\n{code}: Not found in history")


if __name__ == '__main__':
    main()
