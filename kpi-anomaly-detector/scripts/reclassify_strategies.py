# -*- coding: utf-8 -*-
"""
Reclassify KPI/Counter Detection Strategies Based on Historical Data

This script analyzes historical data from kpi_history_records.json
and assigns the most appropriate detection strategy for each code.

Detection Strategies:
- STANDARD_SPC: Default, normal distribution, σ-based rules
- IQR: Interquartile range, robust to outliers and non-normal data
- POISSON: Poisson distribution for count/discrete data
- RELATIVE: Relative percentage change for ratio data
- Z_SCORE: Z-score based detection
- KS_TEST: Kolmogorov-Smirnov test for distribution comparison
- SKIP: Skip detection for constant/saturated data
- ABS_THRESHOLD: Absolute threshold for ceiling/floor saturated data

Classification Logic:
1. If all values = 0 or constant → SKIP
2. If ceiling saturated (mean > 99.9) → ABS_THRESHOLD
3. If floor saturated (mean ≈ 0, occasional non-zero) → ABS_THRESHOLD
4. If count data (integers, mean < 50, CV > 0.3) → POISSON or IQR
5. If ratio data (0-100 range, CV < 0.2) → RELATIVE
6. If high CV (> 0.5) or non-normal → IQR
7. If moderate CV (0.1-0.5) and normal-ish → STANDARD_SPC
8. Otherwise → Z_SCORE or KS_TEST based on data characteristics

Author: ivy0203
Date: 2026-02-03
"""

import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from collections import defaultdict
from scipy import stats


@dataclass
class CodeStats:
    """Statistics for a single code based on historical data"""
    code: str
    code_type: str  # 'KPI' or 'Counter'
    name: str
    # Basic statistics from all historical records
    all_means: List[float]          # means from each historical file
    all_cvs: List[float]            # CVs from each historical file
    all_values: List[float]         # flattened raw values
    n_files: int                    # number of files with this code
    # Aggregated statistics
    overall_mean: float
    overall_std: float
    overall_cv: float
    overall_min: float
    overall_max: float
    # Data characteristics
    is_constant: bool
    is_integer: bool
    is_ceiling_saturated: bool
    is_floor_saturated: bool
    is_ratio_type: bool             # 0-100 percentage
    is_count_type: bool             # discrete counts
    is_high_variance: bool
    is_skewed: bool
    skewness: float
    kurtosis: float
    # Normality test
    shapiro_p: float                # p-value from Shapiro-Wilk test


class HistoryDataAnalyzer:
    """Analyze historical data and recommend detection strategies"""
    
    def __init__(self, history_file: Path):
        self.history_file = history_file
        self.records: List[Dict] = []
        self.code_data: Dict[str, Dict[str, List[Any]]] = defaultdict(lambda: {
            'means': [], 'cvs': [], 'values': [], 'names': [], 'types': []
        })
        self.code_stats: Dict[str, CodeStats] = {}
        
    def load_history(self) -> int:
        """Load and aggregate history data by code"""
        print(f"Loading history from: {self.history_file}")
        with open(self.history_file, 'r', encoding='utf-8') as f:
            self.records = json.load(f)
        
        print(f"Loaded {len(self.records)} historical records")
        
        # Aggregate data by code
        for record in self.records:
            kpi_data = record.get('kpi_data', {})
            for code, info in kpi_data.items():
                # Skip LTE codes, focus on NR
                if code.startswith('LTE_'):
                    continue
                    
                mean_val = info.get('mean', 0)
                cv_val = info.get('cv', 0)
                raw_str = info.get('raw_data', '')
                
                self.code_data[code]['means'].append(mean_val)
                self.code_data[code]['cvs'].append(cv_val)
                self.code_data[code]['names'].append(info.get('kpi_name', ''))
                self.code_data[code]['types'].append(info.get('type', 'Other'))
                
                # Parse raw values
                if raw_str:
                    try:
                        values = [float(x.strip()) for x in raw_str.split(',') if x.strip()]
                        self.code_data[code]['values'].extend(values)
                    except (ValueError, AttributeError):
                        pass
        
        print(f"Aggregated {len(self.code_data)} unique codes")
        return len(self.code_data)
    
    def compute_statistics(self):
        """Compute statistics for each code"""
        print("Computing statistics...")
        
        for code, data in self.code_data.items():
            values = data['values']
            means = data['means']
            cvs = data['cvs']
            names = data['names']
            types = data['types']
            
            if not values:
                continue
            
            # Use most common name and type
            name = max(set(names), key=names.count) if names else ''
            code_type = max(set(types), key=types.count) if types else 'Other'
            
            arr = np.array(values)
            
            # Basic statistics
            overall_mean = np.mean(arr)
            overall_std = np.std(arr)
            overall_cv = overall_std / overall_mean * 100 if overall_mean != 0 else 0
            overall_min = np.min(arr)
            overall_max = np.max(arr)
            
            # Data characteristics
            is_constant = np.std(arr) < 1e-9
            is_integer = all(float(v).is_integer() for v in values)
            
            # Ceiling/floor detection
            is_ceiling_saturated = (overall_mean >= 99.9 and overall_max == 100 and 
                                   overall_min >= 99)
            is_floor_saturated = (overall_mean <= 0.5 and overall_min == 0 and 
                                 overall_max < 5 and not all(v == 0 for v in values))
            
            # Ratio type (0-100 range)
            is_ratio_type = (0 <= overall_min and overall_max <= 100 and 
                           overall_cv < 20 and not is_constant)
            
            # Count type (discrete counts)
            is_count_type = (is_integer and overall_mean < 100 and 
                           overall_min >= 0 and overall_cv > 10)
            
            # High variance
            is_high_variance = overall_cv > 50
            
            # Skewness and kurtosis
            if len(arr) > 8 and not is_constant:
                skewness = stats.skew(arr)
                kurtosis = stats.kurtosis(arr)
                is_skewed = abs(skewness) > 1.0
            else:
                skewness = 0
                kurtosis = 0
                is_skewed = False
            
            # Normality test (Shapiro-Wilk)
            if 3 <= len(arr) <= 5000 and not is_constant:
                try:
                    _, shapiro_p = stats.shapiro(arr[:5000])  # Limit sample size
                except Exception:
                    shapiro_p = 0
            else:
                shapiro_p = 0
            
            self.code_stats[code] = CodeStats(
                code=code,
                code_type=code_type,
                name=name,
                all_means=means,
                all_cvs=cvs,
                all_values=values,
                n_files=len(means),
                overall_mean=overall_mean,
                overall_std=overall_std,
                overall_cv=overall_cv,
                overall_min=overall_min,
                overall_max=overall_max,
                is_constant=is_constant,
                is_integer=is_integer,
                is_ceiling_saturated=is_ceiling_saturated,
                is_floor_saturated=is_floor_saturated,
                is_ratio_type=is_ratio_type,
                is_count_type=is_count_type,
                is_high_variance=is_high_variance,
                is_skewed=is_skewed,
                skewness=skewness,
                kurtosis=kurtosis,
                shapiro_p=shapiro_p
            )
        
        print(f"Computed statistics for {len(self.code_stats)} codes")
    
    def recommend_strategy(self, stats: CodeStats) -> Tuple[str, str]:
        """Recommend detection strategy based on code statistics
        
        Returns:
            (strategy, reason) tuple
        """
        # 1. Constant data → SKIP
        if stats.is_constant:
            return 'SKIP', 'Constant values (σ=0)'
        
        # 2. All zero → SKIP
        if stats.overall_mean == 0 and stats.overall_max == 0:
            return 'SKIP', 'All values are zero'
        
        # 3. Ceiling saturated → ABS_THRESHOLD
        if stats.is_ceiling_saturated:
            return 'ABS_THRESHOLD', f'Ceiling saturated (mean={stats.overall_mean:.2f}%)'
        
        # 4. Floor saturated → ABS_THRESHOLD
        if stats.is_floor_saturated:
            return 'ABS_THRESHOLD', f'Floor saturated (mean={stats.overall_mean:.4f})'
        
        # 5. Count data with small mean → POISSON
        if stats.is_count_type and stats.overall_mean < 30 and stats.overall_mean > 0:
            return 'POISSON', f'Count data (mean={stats.overall_mean:.2f}, integer, CV={stats.overall_cv:.1f}%)'
        
        # 6. Ratio data (0-100%) with low variance → RELATIVE
        if stats.is_ratio_type and stats.overall_cv < 15:
            return 'RELATIVE', f'Ratio data (0-100%, CV={stats.overall_cv:.1f}%)'
        
        # 7. High variance or non-normal → IQR
        if stats.is_high_variance:
            return 'IQR', f'High variance (CV={stats.overall_cv:.1f}%)'
        
        if stats.shapiro_p < 0.05 and stats.shapiro_p > 0:
            # Non-normal distribution
            if stats.is_skewed:
                return 'IQR', f'Non-normal skewed (p={stats.shapiro_p:.4f}, skew={stats.skewness:.2f})'
            elif abs(stats.kurtosis) > 2:
                return 'IQR', f'Non-normal kurtosis (p={stats.shapiro_p:.4f}, kurt={stats.kurtosis:.2f})'
        
        # 8. Moderate CV with moderate distribution → Z_SCORE
        if 10 <= stats.overall_cv <= 50:
            return 'Z_SCORE', f'Moderate variance (CV={stats.overall_cv:.1f}%)'
        
        # 9. Small CV but variable → KS_TEST for distribution comparison
        if stats.overall_cv < 10 and stats.n_files >= 3:
            return 'KS_TEST', f'Low variance (CV={stats.overall_cv:.1f}%), use distribution comparison'
        
        # 10. Default → STANDARD_SPC
        return 'STANDARD_SPC', f'Default (CV={stats.overall_cv:.1f}%)'
    
    def classify_all(self) -> pd.DataFrame:
        """Classify all codes and return DataFrame"""
        results = []
        
        strategy_counts = defaultdict(int)
        
        for code, stats in self.code_stats.items():
            strategy, reason = self.recommend_strategy(stats)
            strategy_counts[strategy] += 1
            
            results.append({
                'Code': code,
                'Name': stats.name,
                'Type': stats.code_type,
                'N_Files': stats.n_files,
                'N_Values': len(stats.all_values),
                'Mean': round(stats.overall_mean, 4),
                'Std': round(stats.overall_std, 4),
                'CV%': round(stats.overall_cv, 2),
                'Min': round(stats.overall_min, 4),
                'Max': round(stats.overall_max, 4),
                'Is_Integer': stats.is_integer,
                'Is_Constant': stats.is_constant,
                'Is_Ceiling': stats.is_ceiling_saturated,
                'Is_Floor': stats.is_floor_saturated,
                'Skewness': round(stats.skewness, 3),
                'Kurtosis': round(stats.kurtosis, 3),
                'Shapiro_P': round(stats.shapiro_p, 4),
                'Recommended_Strategy': strategy,
                'Strategy_Reason': reason
            })
        
        df = pd.DataFrame(results)
        df = df.sort_values(['Recommended_Strategy', 'Code'])
        
        # Print summary
        print("\n" + "="*60)
        print("Strategy Distribution Summary")
        print("="*60)
        for strategy in sorted(strategy_counts.keys()):
            count = strategy_counts[strategy]
            pct = count / len(self.code_stats) * 100
            print(f"  {strategy:20s}: {count:5d} ({pct:5.1f}%)")
        print("="*60)
        print(f"  {'TOTAL':20s}: {len(self.code_stats):5d}")
        
        return df


def main():
    """Main function"""
    # Paths
    base_dir = Path(__file__).parent.parent
    history_file = base_dir / 'reports' / 'kpi_history_records.json'
    output_file = base_dir / 'lib' / 'kpi_xml' / 'strategy_recommendations.xlsx'
    classification_file = base_dir / 'lib' / 'kpi_xml' / 'kpi_classification_v2.xlsx'
    custom_rules_file = base_dir / 'lib' / 'kpi_xml' / 'kpi_custom_rules.xlsx'
    
    if not history_file.exists():
        print(f"Error: History file not found: {history_file}")
        return
    
    # Analyze history
    analyzer = HistoryDataAnalyzer(history_file)
    analyzer.load_history()
    analyzer.compute_statistics()
    
    # Classify and get recommendations
    df = analyzer.classify_all()
    
    # Save recommendations
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Summary sheet
        summary_df = df.groupby('Recommended_Strategy').size().reset_index(name='Count')
        summary_df['Percentage'] = (summary_df['Count'] / summary_df['Count'].sum() * 100).round(1)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # All codes
        df.to_excel(writer, sheet_name='All_Codes', index=False)
        
        # Separate sheets by strategy
        for strategy in df['Recommended_Strategy'].unique():
            strategy_df = df[df['Recommended_Strategy'] == strategy]
            sheet_name = strategy[:31]  # Excel limit
            strategy_df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"\nRecommendations saved to: {output_file}")
    
    # Now update kpi_classification_v2.xlsx
    print("\n" + "="*60)
    print("Updating kpi_classification_v2.xlsx...")
    print("="*60)
    
    update_classification_file(classification_file, df)
    
    # Update kpi_custom_rules.xlsx with special cases
    print("\n" + "="*60)
    print("Updating kpi_custom_rules.xlsx...")
    print("="*60)
    
    update_custom_rules_file(custom_rules_file, df)
    
    print("\nDone!")


def update_classification_file(classification_file: Path, recommendations_df: pd.DataFrame):
    """Update kpi_classification_v2.xlsx with new strategies"""
    if not classification_file.exists():
        print(f"Warning: Classification file not found: {classification_file}")
        return
    
    # Create code to strategy mapping
    code_to_strategy = dict(zip(recommendations_df['Code'], recommendations_df['Recommended_Strategy']))
    code_to_reason = dict(zip(recommendations_df['Code'], recommendations_df['Strategy_Reason']))
    
    # Read existing file
    try:
        df_class = pd.read_excel(classification_file, sheet_name='1_All_Codes_Classification')
    except Exception:
        try:
            df_class = pd.read_excel(classification_file, sheet_name=0)
        except Exception as e:
            print(f"Error reading classification file: {e}")
            return
    
    # Update Detection_Strategy column
    updated_count = 0
    for idx, row in df_class.iterrows():
        code = str(row.get('Code', '')).strip()
        if code in code_to_strategy:
            new_strategy = code_to_strategy[code]
            old_strategy = str(row.get('Detection_Strategy', '')).strip()
            if old_strategy != new_strategy:
                df_class.at[idx, 'Detection_Strategy'] = new_strategy
                updated_count += 1
    
    # Save updated file
    backup_file = classification_file.with_suffix('.xlsx.bak2')
    if classification_file.exists():
        import shutil
        shutil.copy(classification_file, backup_file)
        print(f"Backup created: {backup_file}")
    
    with pd.ExcelWriter(classification_file, engine='openpyxl') as writer:
        df_class.to_excel(writer, sheet_name='1_All_Codes_Classification', index=False)
    
    print(f"Updated {updated_count} codes in {classification_file.name}")


def update_custom_rules_file(custom_rules_file: Path, recommendations_df: pd.DataFrame):
    """Update kpi_custom_rules.xlsx with codes needing special strategies"""
    # Select codes that need non-default strategies
    special_codes = recommendations_df[
        recommendations_df['Recommended_Strategy'].isin(['IQR', 'POISSON', 'RELATIVE', 'KS_TEST'])
    ].copy()
    
    if special_codes.empty:
        print("No special strategy codes to add")
        return
    
    # Prepare custom rules data
    custom_rules = []
    for _, row in special_codes.iterrows():
        custom_rules.append({
            'Code': row['Code'],
            'Override_Strategy': row['Recommended_Strategy'],
            'Enabled': True,
            'Comment': f"ivy0203: {row['Strategy_Reason']}"
        })
    
    # Create or update Excel file
    backup_file = custom_rules_file.with_suffix('.xlsx.bak2')
    if custom_rules_file.exists():
        import shutil
        shutil.copy(custom_rules_file, backup_file)
        print(f"Backup created: {backup_file}")
        
        # Read existing rules
        try:
            df_existing = pd.read_excel(custom_rules_file, sheet_name='1_Custom_Rules')
            existing_codes = set(df_existing['Code'].astype(str).tolist())
        except Exception:
            df_existing = pd.DataFrame()
            existing_codes = set()
    else:
        df_existing = pd.DataFrame()
        existing_codes = set()
    
    # Add only new codes
    new_rules = [r for r in custom_rules if r['Code'] not in existing_codes]
    
    if new_rules:
        df_new = pd.DataFrame(new_rules)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_existing
        print("All special codes already exist in custom rules")
    
    # Save
    with pd.ExcelWriter(custom_rules_file, engine='openpyxl') as writer:
        df_combined.to_excel(writer, sheet_name='1_Custom_Rules', index=False)
    
    print(f"Added {len(new_rules)} new custom rules to {custom_rules_file.name}")


if __name__ == '__main__':
    main()
