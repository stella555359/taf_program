# -*- coding: utf-8 -*-
"""
KPI Anomaly Detector - Main Detection Module
Integrates consistency check (CV analysis) and t-test comparison
Enhanced with type-based anomaly detection (ivy0126)
Enhanced with alternative detection methods (ivy0202): IQR, Poisson, Relative change
"""

import pandas as pd
import numpy as np
import json
import re
from pathlib import Path
from datetime import datetime
from scipy import stats

from .config import (PATHS, COLORS, DEFAULT_CV_THRESHOLD, DEFAULT_P_VALUE_THRESHOLD,
                     HISTORY_FILENAME)
from .utils import (
    calculate_cv,
    calculate_trimmed_cv,
    classify_code,
    extract_history_context,
    extract_history_context_from_record,
    parse_raw_data,
)
from .shewhart import calculate_severity_from_history
from .excel_report import ExcelReportGenerator
from .html_report import HTMLReportGenerator
from .kpi_types import (get_classifier, get_type_based_detector, get_strategy_based_detector,
                        KPIType, DetectionStrategy)
from .guard_rails import (GuardRails, GuardRailConfig, integrate_guard_rails_with_detection)


class KPIAnomalyDetector:
    """KPI Anomaly Detector - Integrates consistency and t-test analysis"""
    
    def __init__(self, current_file, cv_threshold=DEFAULT_CV_THRESHOLD, 
                 p_value_threshold=DEFAULT_P_VALUE_THRESHOLD):
        """Initialize detector
        
        Args:
            current_file: Path to Excel file to analyze
            cv_threshold: CV threshold percentage (default 5%)
            p_value_threshold: P-value threshold for t-test (default 0.05)
        """
        self.current_file = Path(current_file)
        self.cv_threshold = cv_threshold
        self.p_value_threshold = p_value_threshold
        
        self.current_df = None
        self.data_cols = []
        self.analysis_results = {}
        
        # History records - stored in reports directory
        self.history_file_path = PATHS['reports'] / HISTORY_FILENAME
        self.history_records = []
        self.previous_record = None
        
        # Report output directory
        self.reports_dir = PATHS['reports']
        self.last_report_files = {'excel': None, 'html': None}
        self.last_current_record = None
        
        # Deduplication info
        self.dedup_info = {'total_dropped': 0, 'details': []}
        
        # Current file environment/scenario history identifier
        self.current_history_context = extract_history_context(self.current_file.name)
        
        # Type-based detection (ivy0126)
        self.kpi_classifier = get_classifier()
        self.type_based_detector = get_type_based_detector()
        
        # Guard Rails detection (ivy0127)
        self.guard_rails = GuardRails()
        
        # Strategy-based detection (ivy0202) - configured via Excel
        self.strategy_detector = get_strategy_based_detector()
    
    def _is_same_history_context(self, record):
        """Check if a history record belongs to the same environment and scenario."""
        if self.current_history_context is None:
            return True

        other_context = extract_history_context_from_record(record)
        if other_context is None:
            return True

        return other_context.get('history_key') == self.current_history_context.get('history_key')
    
    def load_history(self):
        """Load history records"""
        if self.history_file_path.exists():
            try:
                with open(self.history_file_path, 'r', encoding='utf-8') as f:
                    all_records = json.load(f)
                
                # Filter records matching current environment/scenario AND exclude current file
                current_filename = self.current_file.name
                self.history_records = [
                    r for r in all_records 
                    if self._is_same_history_context(r)
                    and r.get('filename', '') != current_filename  # Exclude current file
                ]
                
                print(f"History loaded: {len(all_records)} total records")
                
                if self.current_history_context:
                    print(
                        f"  Current history group: {self.current_history_context.get('environment', 'UNKNOWN')}"
                        f" + {self.current_history_context.get('scenario', 'UNKNOWN')}"
                    )
                    print(f"  Matching history records (excluding current): {len(self.history_records)}")
                
                # Get most recent matching record for comparison
                if self.history_records:
                    self.previous_record = self.history_records[-1]
                    print(f"  Previous matching analysis: {self.previous_record.get('filename', 'N/A')} @ {self.previous_record.get('timestamp', 'N/A')}")
                else:
                    print(f"  No matching environment/scenario history")
                
                # Keep all records for saving (don't lose other scenario data)
                self._all_history_records = all_records
                
            except Exception as e:
                print(f"Warning: Failed to load history - {e}")
                self.history_records = []
                self._all_history_records = []
        else:
            print("First run, no history records")
            self.history_records = []
            self._all_history_records = []
    
    def save_history(self, current_result):
        """Save current result to history
        
        If current file already exists in history, update it instead of appending.
        """
        all_records = getattr(self, '_all_history_records', [])
        current_filename = current_result.get('filename', '')
        
        # Remove existing record for current file (if any)
        all_records = [r for r in all_records if r.get('filename', '') != current_filename]
        
        # Append current result
        all_records.append(current_result)
        
        try:
            with open(self.history_file_path, 'w', encoding='utf-8') as f:
                json.dump(all_records, f, ensure_ascii=False, indent=2)
            
            same_scenario_count = sum(
                1 for r in all_records 
                if self._is_same_history_context(r)
            )
            print(f"History updated (total {len(all_records)}, matching env/scenario {same_scenario_count})")
        except Exception as e:
            print(f"Warning: Failed to save history - {e}")
    
    def load_data(self):
        """Load data from Excel file"""
        print(f"\nLoading current file: {self.current_file.name}")
        self.current_df = pd.read_excel(self.current_file)
        print(f"  Original data shape: {self.current_df.shape}")
        
        # Find data columns (T076/T080/T073/T283/T813/T816/T284)
        data_prefixes = ('T076', 'T080', 'T073', 'T283', 'T813', 'T816', 'T284')
        self.data_cols = [
            col for col in self.current_df.columns
            if any(prefix in str(col) for prefix in data_prefixes)
        ]
        print(f"  Found {len(self.data_cols)} data columns ({', '.join(data_prefixes)})")
        
        # Deduplicate data
        self.deduplicate_data()
        
        # Load history
        self.load_history()
        
        # Auto-detect and register new codes not in kpi_config_unified.xlsx (ivy0210)
        self._register_unknown_codes()
    
    def deduplicate_data(self):
        """Remove duplicate Code data
        
        Rule: For codes formatted as NR_Ax or SCOUT_NR_Ax (A is 2-4 digit number, x is letter),
        if NR_A part is same but x differs, keep the one with largest x, remove others.
        Example: NR_5089a, NR_5089b, NR_5089e -> keep NR_5089e
        """
        if self.current_df is None or self.current_df.empty:
            return
        
        print("\n========== Data Deduplication ==========")
        
        # Pattern: NR_number+letter or SCOUT_NR_number+letter
        pattern = r'((?:SCOUT_)?NR_\d{2,4})([a-zA-Z])'
        
        # Find all matching codes and their groups
        code_groups = {}  # {base: [(code, suffix, idx), ...]}
        
        for idx, row in self.current_df.iterrows():
            code = str(row.get('Code', '')).strip() if pd.notna(row.get('Code')) else ''
            match = re.search(pattern, code, re.IGNORECASE)
            if match:
                base = match.group(1).upper()
                suffix = match.group(2).upper()
                if base not in code_groups:
                    code_groups[base] = []
                code_groups[base].append((code, suffix, idx))
        
        # Find rows to drop
        rows_to_drop = []
        dedup_details = []
        
        for base, items in code_groups.items():
            if len(items) > 1:
                # Sort by suffix (alphabetical), keep largest
                items.sort(key=lambda x: x[1], reverse=True)
                kept = items[0]
                dropped = items[1:]
                dedup_details.append({
                    'kept': kept[0],
                    'dropped': [d[0] for d in dropped]
                })
                for _, _, idx in dropped:
                    rows_to_drop.append(idx)
        
        if rows_to_drop:
            print(f"  Found {len(dedup_details)} duplicate groups, dropping {len(rows_to_drop)} rows")
            for detail in dedup_details:
                print(f"    Keep: {detail['kept']}, Drop: {detail['dropped']}")
            
            self.current_df = self.current_df.drop(rows_to_drop).reset_index(drop=True)
            print(f"  Data shape after dedup: {self.current_df.shape}")
        else:
            print("  No duplicates found")
        
        self.dedup_info = {
            'total_dropped': len(rows_to_drop),
            'details': dedup_details
        }
    
    def _register_unknown_codes(self):
        """Auto-detect codes not in kpi_config_unified.xlsx and register them (ivy0210)
        
        Searches XML files for the code info, then appends to the unified xlsx.
        """
        if self.current_df is None or self.current_df.empty:
            return
        
        # Collect all codes from current data
        all_codes = []
        if 'Code' in self.current_df.columns:
            for _, row in self.current_df.iterrows():
                code = str(row.get('Code', '')).strip() if pd.notna(row.get('Code')) else ''
                if code:
                    all_codes.append(code)
        
        if not all_codes:
            return
        
        # Filter to codes not in classifier
        unknown_codes = []
        for code in all_codes:
            cls = self.kpi_classifier.get_classification(code)
            if cls is None:
                unknown_codes.append(code)
        
        if unknown_codes:
            print(f"\n========== Auto-Register Unknown Codes (ivy0210) ==========")
            print(f"  Found {len(unknown_codes)} codes not in kpi_config_unified.xlsx")
            new_codes = self.kpi_classifier.register_new_codes(unknown_codes, default_strategy='IQR')
            if new_codes:
                print(f"  Successfully registered {len(new_codes)} new codes")

    def analyze_consistency(self):
        """Analyze consistency (CV analysis)"""
        print("\n========== Consistency Analysis ==========")
        
        if not self.data_cols:
            print("Error: No data columns found")
            return
        
        data_cols = self.current_df[self.data_cols]
        
        results = []
        for idx, row in self.current_df.iterrows():
            code = str(row.get('Code', '')).strip() if pd.notna(row.get('Code')) else ''
            kpi_name = str(row.get('KPI Name', '')).strip() if 'KPI Name' in row.index and pd.notna(row.get('KPI Name')) else ''
            
            row_data = data_cols.iloc[idx]
            non_null = row_data.dropna()
            
            # Initialize Trimmed values
            trimmed_mean = np.nan
            trimmed_std = np.nan
            trimmed_cv = np.nan
            trimmed_status = ''
            use_trimmed = False
            
            if len(non_null) == 0:
                status = 'NULL'
                cv = np.nan
                mean_val = np.nan
                std_val = np.nan
            elif len(non_null) < len(self.data_cols):
                # Partial null values
                if len(non_null.unique()) == 1 and (non_null.iloc[0] == 0 or non_null.iloc[0] == 100):
                    status = 'Consistent'
                    cv = 0
                else:
                    status = 'partial NULL'
                    cv = np.nan
                mean_val = non_null.mean()
                std_val = non_null.std(ddof=0)
            else:
                mean_val = non_null.mean()
                std_val = non_null.std(ddof=0)
                
                if non_null.nunique() == 1:
                    status = 'Consistent'
                    cv = 0
                elif abs(mean_val) < 0.001:
                    # Very small values, use absolute difference
                    if (non_null.max() - non_null.min()) < 0.001:
                        status = 'Consistent'
                        cv = 0
                    else:
                        status = 'Inconsistent'
                        cv = np.nan
                else:
                    cv = (std_val / mean_val) * 100
                    status = 'Consistent' if cv < self.cv_threshold else 'Inconsistent'
                
                # If data >= 5, calculate trimmed results (remove min and max)
                if len(non_null) >= 5:
                    use_trimmed = True
                    sorted_vals = non_null.sort_values()
                    trimmed_vals = sorted_vals.iloc[1:-1]
                    trimmed_mean = trimmed_vals.mean()
                    trimmed_std = trimmed_vals.std(ddof=0)
                    
                    if trimmed_vals.nunique() == 1:
                        trimmed_cv = 0
                        trimmed_status = 'Consistent'
                    elif abs(trimmed_mean) < 0.001:
                        if (trimmed_vals.max() - trimmed_vals.min()) < 0.001:
                            trimmed_cv = 0
                            trimmed_status = 'Consistent'
                        else:
                            trimmed_cv = np.nan
                            trimmed_status = 'Inconsistent'
                    else:
                        trimmed_cv = (trimmed_std / trimmed_mean) * 100
                        trimmed_status = 'Consistent' if trimmed_cv < self.cv_threshold else 'Inconsistent'
            
            results.append({
                'Code': code,
                'KPI Name': kpi_name,
                'Type': classify_code(code),
                'Mean': round(mean_val, 2) if pd.notna(mean_val) else np.nan,
                'Std': round(std_val, 2) if pd.notna(std_val) else np.nan,
                'CV(%)': round(cv, 2) if pd.notna(cv) else np.nan,
                'Consistency': status,
                'DataCount': len(non_null),
                'Trimmed_Mean': round(trimmed_mean, 2) if use_trimmed and pd.notna(trimmed_mean) else np.nan,
                'Trimmed_Std': round(trimmed_std, 2) if use_trimmed and pd.notna(trimmed_std) else np.nan,
                'Trimmed_CV(%)': round(trimmed_cv, 2) if use_trimmed and pd.notna(trimmed_cv) else np.nan,
                'Trimmed_Consistency': trimmed_status if use_trimmed else '',
                'RawData': ','.join([str(v) for v in non_null.tolist()]) if len(non_null) > 0 else ''
            })
        
        self.analysis_results['consistency'] = pd.DataFrame(results)
        
        # Statistics
        consistency_df = self.analysis_results['consistency']
        print(f"  Consistent: {(consistency_df['Consistency'] == 'Consistent').sum()}")
        print(f"  Inconsistent: {(consistency_df['Consistency'] == 'Inconsistent').sum()}")
        print(f"  partial NULL: {(consistency_df['Consistency'] == 'partial NULL').sum()}")
        print(f"  NULL: {(consistency_df['Consistency'] == 'NULL').sum()}")
    
    def analyze_ttest_with_history(self):
        """Analyze t-test (compare with history)"""
        if not self.previous_record:
            print("\nNo history records, skipping t-test analysis")
            return
        
        print("\n========== T-Test Analysis (vs History) ==========")
        print(f"  Comparing with: {self.previous_record.get('filename', 'N/A')}")
        
        prev_data = self.previous_record.get('kpi_data', {})
        
        if not prev_data:
            print("  Warning: No KPI data in history record")
            return
        
        results = []
        consistency_df = self.analysis_results.get('consistency', pd.DataFrame())
        
        for _, row in consistency_df.iterrows():
            code = row['Code']
            if not code or code not in prev_data:
                continue
            
            # Current data
            current_raw = row['RawData']
            if not current_raw:
                continue
            current_values = [float(x) for x in current_raw.split(',') if x.strip()]
            
            # History data
            prev_raw = prev_data[code].get('raw_data', '')
            if not prev_raw:
                continue
            prev_values = [float(x) for x in prev_raw.split(',') if x.strip()]
            
            # Perform t-test
            if len(current_values) >= 2 and len(prev_values) >= 2:
                current_mean = np.mean(current_values)
                prev_mean = np.mean(prev_values)
                
                # Check for zero variance
                if np.std(current_values) == 0 and np.std(prev_values) == 0:
                    if current_mean == prev_mean:
                        p_value = 1.0
                        t_stat = 0
                    else:
                        p_value = 0.0
                        t_stat = float('inf')
                else:
                    try:
                        t_stat, p_value = stats.ttest_ind(current_values, prev_values, equal_var=False)
                    except:
                        t_stat = np.nan
                        p_value = np.nan
                
                diff = current_mean - prev_mean
                diff_pct = (diff / prev_mean * 100) if prev_mean != 0 else (np.nan if diff == 0 else float('inf'))
                
                # Determine result
                if pd.notna(p_value) and p_value < self.p_value_threshold:
                    ttest_result = 'Fail'
                else:
                    ttest_result = 'Pass'
                
                results.append({
                    'Code': code,
                    'KPI Name': row['KPI Name'],
                    'Type': row['Type'],
                    'Current_Mean': round(current_mean, 2),
                    'History_Mean': round(prev_mean, 2),
                    'Diff': round(diff, 2),
                    'Diff(%)': round(diff_pct, 2) if np.isfinite(diff_pct) else np.nan,
                    'T_Stat': round(t_stat, 2) if np.isfinite(t_stat) else np.nan,
                    'P_Value': round(p_value, 4) if pd.notna(p_value) else np.nan,
                    'TTest_Result': ttest_result,
                    'Current_Data': current_raw,
                    'History_Data': prev_raw
                })
        
        self.analysis_results['ttest'] = pd.DataFrame(results)
        
        if len(results) > 0:
            ttest_df = self.analysis_results['ttest']
            print(f"  Compared KPIs: {len(ttest_df)}")
            print(f"  Pass: {(ttest_df['TTest_Result'] == 'Pass').sum()}")
            print(f"  Fail: {(ttest_df['TTest_Result'] == 'Fail').sum()}")
    
    def analyze_all_codes_with_history(self):
        """Analyze all codes based on historical data
        
        Severity judgment (primarily based on historical statistics, T-Test as reference):
        - Normal: Current mean within historical mean +/-2 sigma
        - Suspicious: Exceeds +/-2 sigma but not +/-3 sigma
        - Regression: Exceeds +/-3 sigma or trend deviation
        - NoHistory: Insufficient historical data (<2 records)
        """
        print("\n========== All Codes Analysis (History-based + Type-based) ==========")
        
        all_codes_analysis = []
        
        consistency_df = self.analysis_results.get('consistency', pd.DataFrame())
        ttest_df = self.analysis_results.get('ttest', pd.DataFrame())
        
        if consistency_df.empty:
            print("  Error: No consistency analysis data")
            return
        
        # Get history data
        prev_data = {}
        if self.previous_record:
            prev_data = self.previous_record.get('kpi_data', {})
        
        # Process all codes
        for _, row in consistency_df.iterrows():
            code = row['Code']
            if not code:
                continue
            
            # Basic info
            kpi_name = row['KPI Name']
            code_type = row['Type']
            cv_value = row['CV(%)']
            consistency = row['Consistency']
            raw_data = row['RawData']
            trimmed_consistency = row.get('Trimmed_Consistency', '')
            data_count = row.get('DataCount', 0)
            
            # Get T-Test result (as reference)
            ttest_result = 'N/A'
            p_value = np.nan
            diff_pct = np.nan
            if not ttest_df.empty:
                ttest_row = ttest_df[ttest_df['Code'] == code]
                if not ttest_row.empty:
                    ttest_result = ttest_row['TTest_Result'].iloc[0]
                    p_value = ttest_row['P_Value'].iloc[0]
                    diff_pct = ttest_row['Diff(%)'].iloc[0]
            
            # Get history data
            history_data = ''
            history_consistency = 'N/A'
            if code in prev_data:
                history_data = prev_data[code].get('raw_data', '')
                history_consistency = prev_data[code].get('consistency', 'N/A')
            
            # Parse current data
            current_values = []
            if raw_data:
                try:
                    current_values = [float(x) for x in raw_data.split(',') if x.strip()]
                except:
                    pass
            
            # Calculate severity based on history (standard method)
            hist_result = calculate_severity_from_history(code, current_values, self.history_records)
            
            # ========== Type-based detection (ivy0126) ==========
            # Get KPI classification info
            kpi_cls = self.kpi_classifier.get_classification(code)
            kpi_type_str = kpi_cls.kpi_type.value if kpi_cls else 'unknown'
            detection_strategy = self.kpi_classifier.get_detection_strategy(code).value
            custom_rule_applied = self.kpi_classifier.is_custom_rule_applied(code)
            units = kpi_cls.units if kpi_cls else ''
            # Use new methods that support SCOUT_NR_ → NR_ lookup
            related_counters = self.kpi_classifier.get_related_counters(code)
            related_kpis = self.kpi_classifier.get_related_kpis(code)  # For counters
            xml_level = kpi_cls.level if kpi_cls else ''
            formula = self.kpi_classifier.get_formula(code)
            
            # Apply type-based detection if we have history
            type_based_result = None
            type_based_severity = None
            if hist_result['hist_mean'] is not None and hist_result['hist_std'] is not None:
                type_based_result = self.type_based_detector.detect_anomaly(
                    code, current_values, 
                    hist_result['hist_mean'], hist_result['hist_std'],
                    self.history_records
                )
                type_based_severity = type_based_result.get('severity')
            
            # Final severity: use type-based for known types, standard for unknown
            if kpi_type_str != 'unknown' and type_based_result:
                severity = type_based_severity
                # Merge anomaly indices from type-based detection
                type_anomaly_indices = type_based_result.get('anomaly_indices', [])
                level_shift = type_based_result.get('level_shift_detected', False)
            else:
                severity = hist_result['severity']
                type_anomaly_indices = []
                level_shift = False
            
            # ========== Guard Rails Check (ivy0127) ==========
            # Apply Guard Rails if we have history data
            guard_rail_violations = []
            guard_rail_details = {}
            guard_rail_severity = ''  # ivy0129: track GR severity separately
            strategy_detection_method = ''  # ivy0202: track strategy-based detection method
            strategy_detection_result = None
            
            if hist_result['hist_mean'] is not None and hist_result['hist_std'] is not None:
                # Collect history values for Guard Rails check
                history_values = []
                for record in self.history_records:
                    kpi_data = record.get('kpi_data', {})
                    if code in kpi_data:
                        hist_raw_data = kpi_data[code].get('raw_data', '')
                        if hist_raw_data:
                            try:
                                vals = [float(x) for x in hist_raw_data.split(',') if x.strip()]
                                history_values.extend(vals)
                            except:
                                pass
                
                if current_values and history_values:
                    # ========== Strategy-Based Detection (ivy0203 refactored) ==========
                    # Get detection strategy from Excel configuration
                    strategy = self.kpi_classifier.get_detection_strategy(code)
                    strategy_detection_method = strategy.value
                    
                    # Apply strategy-based detection for non-STANDARD_SPC strategies
                    from .kpi_types import StrategyBasedDetector, DetectionStrategy, normalize_strategy
                    normalized_strategy = normalize_strategy(strategy)
                    
                    if StrategyBasedDetector.is_alternative_strategy(normalized_strategy):
                        strat_sev, strat_reason, strat_details = self.strategy_detector.detect(
                            normalized_strategy, current_values, history_values,
                            hist_result['hist_mean'], hist_result['hist_std']
                        )
                        if strat_sev:
                            strategy_detection_result = {
                                'severity': strat_sev,
                                'reason': strat_reason,
                                'details': strat_details
                            }
                            # ivy0203: Strategy result is PRIMARY when not STANDARD_SPC
                            # Override severity with strategy result (SPC only as reference)
                            severity = strat_sev
                    
                    # Guard Rails apply to ALL strategies as baseline check (ivy0203 pm)
                    # Guard Rails can upgrade severity regardless of strategy type
                    new_severity, guard_upgrade_reason, guard_rail_details = integrate_guard_rails_with_detection(
                        current_values=current_values,
                        history_values=history_values,
                        hist_mean=hist_result['hist_mean'],
                        hist_std=hist_result['hist_std'],
                        base_severity=severity,
                        base_reason=''
                    )
                    
                    # Update severity if upgraded by Guard Rails
                    if new_severity != severity:
                        severity = new_severity
                    
                    # Collect violations
                    if guard_upgrade_reason:
                        guard_rail_violations = [guard_upgrade_reason]
                        guard_rail_details['violation'] = guard_upgrade_reason
                        guard_rail_severity = new_severity
                    
                    # ========== Physical Floor Constraint for dB/dBm KPIs (ivy0204) ==========
                    # For physical_stable KPIs with dB/dBm units:
                    # - If absolute change < 1dB, cap severity at Suspicious (not Regression)
                    # - This prevents statistically significant but physically irrelevant changes
                    #   from being flagged as Regression
                    if kpi_type_str == 'physical_stable' and units and 'dB' in units:
                        current_mean = np.mean(current_values) if current_values else 0
                        abs_delta = abs(current_mean - hist_result['hist_mean'])
                        DB_FLOOR_THRESHOLD = 0.5  # 1dB physical significance threshold
                        
                        if abs_delta < DB_FLOOR_THRESHOLD and severity == 'Regression':
                            # Downgrade to Suspicious - change is statistically but not physically significant
                            severity = 'Suspicious'
                            guard_rail_details['physical_floor_applied'] = True
                            guard_rail_details['abs_delta_db'] = abs_delta
                            guard_rail_details['db_floor_threshold'] = DB_FLOOR_THRESHOLD
            
            # Get Shewhart chart data (always collected for reference/visualization)
            shewhart_data = hist_result.get('shewhart', {})
            shewhart_zone = shewhart_data.get('zone', '')
            shewhart_violations = shewhart_data.get('violations', [])
            control_limits = shewhart_data.get('control_limits', {})
            
            # Build analysis reasons (ivy0203 refactored)
            analysis_reasons = []
            
            # ivy0204: Add physical floor info for dB/dBm KPIs
            if guard_rail_details.get('physical_floor_applied'):
                abs_delta_db = guard_rail_details.get('abs_delta_db', 0)
                analysis_reasons.append(f"[dB Floor] Δ={abs_delta_db:.2f}dB < 1dB, capped at Suspicious")
            
            # ivy0203: Strategy detection result is PRIMARY (shown first)
            if strategy_detection_result and strategy_detection_result.get('reason'):
                analysis_reasons.append(f"[{strategy_detection_method}] {strategy_detection_result['reason']}")
            
            # Guard Rails (may be primary for SPC, or reference for other strategies)
            if guard_rail_violations:
                # For non-SPC strategies, GR reasons already have "(ref)" prefix
                analysis_reasons.append(guard_rail_violations[0])
            
            # Add type-based detection reasons (if applicable)
            if type_based_result and type_based_result.get('reasons'):
                analysis_reasons.extend(type_based_result['reasons'])
            
            # Add consistency info (as reference)
            if consistency == 'Inconsistent':
                if data_count >= 5 and trimmed_consistency == 'Consistent':
                    analysis_reasons.append('CV inconsistent, trimmed consistent')
                else:
                    analysis_reasons.append('CV inconsistent')
            elif consistency == 'partial NULL':
                analysis_reasons.append('Partial null values')
            
            # ivy0203: Add SPC/history reasons only for STANDARD_SPC strategy
            # For other strategies, SPC is reference only
            from .kpi_types import DetectionStrategy, normalize_strategy
            if normalize_strategy(self.kpi_classifier.get_detection_strategy(code)) == DetectionStrategy.STANDARD_SPC:
                if kpi_type_str == 'unknown' and hist_result['judgment_reasons']:
                    analysis_reasons.extend(hist_result['judgment_reasons'])
            else:
                # Add SPC info as reference for non-SPC strategies
                if shewhart_violations:
                    spc_ref = f"(SPC ref: {'; '.join(shewhart_violations[:2])})"
                    if spc_ref not in str(analysis_reasons):
                        analysis_reasons.append(spc_ref)
            
            # T-Test result as reference
            if ttest_result == 'Fail':
                analysis_reasons.append('T-Test Fail (ref)')
            
            all_codes_analysis.append({
                'Code': code,
                'KPI Name': kpi_name,
                'Type': code_type,
                'Severity': severity,
                'Reasons': '; '.join(analysis_reasons) if analysis_reasons else 'Normal',
                'CV(%)': cv_value,
                'Consistency': consistency,
                'Trimmed_Consistency': trimmed_consistency,
                'TTest_Result': ttest_result,
                'P_Value': p_value,
                'Diff(%)': diff_pct,
                'Z_Score': hist_result['z_score'],
                'Sigma_Level': hist_result['sigma_level'],
                'Anomaly_Count': hist_result['anomaly_count'],
                'Total_Points': len(current_values),
                'Anomaly_Ratio(%)': hist_result['anomaly_ratio'] * 100 if hist_result['anomaly_ratio'] else 0,
                'Trend': hist_result['trend_direction'] or '',
                'Hist_Mean': hist_result['hist_mean'],
                'Hist_Std': hist_result['hist_std'],
                'Current_Mean': hist_result['current_mean'],
                # Degenerate case fields
                'Is_Degenerate': hist_result.get('is_degenerate', False),
                'Degenerate_Type': hist_result.get('degenerate_type', ''),
                # Shewhart chart fields
                'SPC_Zone': shewhart_zone,
                'SPC_Violations': '; '.join(shewhart_violations) if shewhart_violations else '',
                'SPC_UCL': control_limits.get('UCL'),
                'SPC_LCL': control_limits.get('LCL'),
                'SPC_CL': control_limits.get('CL'),
                'Current_Data': raw_data,
                'History_Data': history_data,
                # Full Shewhart chart_data for HTML visualization
                '_shewhart_chart': shewhart_data.get('chart_data', {}),
                # Type-based detection fields (ivy0126)
                'KPI_Type': kpi_type_str,
                'Detection_Strategy': detection_strategy,
                'Custom_Rule_Applied': custom_rule_applied,
                'Units': units,
                'Related_Counters': ','.join(related_counters) if related_counters else '',
                'Related_KPIs': ','.join(related_kpis) if related_kpis else '',
                'Formula': formula,
                'XML_Level': xml_level,
                'Level_Shift': level_shift,
                'Type_Anomaly_Indices': type_anomaly_indices,
                # Guard Rails fields (ivy0127, ivy0129: fixed severity tracking)
                'Guard_Rail_Violations': '; '.join(guard_rail_violations) if guard_rail_violations else '',
                'Guard_Rail_Overall': guard_rail_severity if guard_rail_severity else '',
                # Strategy-based detection method fields (ivy0202)
                'Detection_Strategy': strategy_detection_method,
            })
        
        # Create DataFrame and sort
        all_codes_df = pd.DataFrame(all_codes_analysis)
        if not all_codes_df.empty:
            severity_order = {'Regression': 0, 'Suspicious': 1, 'NoHistory': 2, 'Normal': 3}
            all_codes_df['_severity_order'] = all_codes_df['Severity'].map(severity_order)
            all_codes_df = all_codes_df.sort_values(['_severity_order', 'Sigma_Level'], ascending=[True, False])
            all_codes_df = all_codes_df.drop(columns=['_severity_order'])
        
        self.analysis_results['all_codes'] = all_codes_df
        
        # Statistics
        print(f"  Total Codes: {len(all_codes_df)}")
        print(f"  Regression (Performance Degradation): {(all_codes_df['Severity'] == 'Regression').sum()}")
        print(f"  Suspicious: {(all_codes_df['Severity'] == 'Suspicious').sum()}")
        print(f"  Normal: {(all_codes_df['Severity'] == 'Normal').sum()}")
        print(f"  NoHistory: {(all_codes_df['Severity'] == 'NoHistory').sum()}")
        
        # Compatible with old suspicious interface
        suspicious_df = all_codes_df[all_codes_df['Severity'] != 'Normal'].copy()
        self.analysis_results['suspicious'] = suspicious_df
        
        print(f"\n  Codes requiring attention: {len(suspicious_df)}")
    
    def identify_suspicious_kpis(self):
        """Compatible with old interface, calls new analysis method"""
        self.analyze_all_codes_with_history()
    
    def build_current_record(self):
        """Build current result record for saving to history"""
        consistency_df = self.analysis_results.get('consistency', pd.DataFrame())
        suspicious_df = self.analysis_results.get('suspicious', pd.DataFrame())

        def has_columns(*column_names):
            return all(column_name in consistency_df.columns for column_name in column_names)

        def filtered_consistency_by_type(type_name):
            if 'Type' not in consistency_df.columns:
                return pd.DataFrame(columns=consistency_df.columns)
            return consistency_df[consistency_df['Type'] == type_name]
        
        # KPI data dictionary (for next t-test comparison)
        kpi_data = {}
        for _, row in consistency_df.iterrows():
            code = row.get('Code', '')
            if code:
                kpi_data[code] = {
                    'kpi_name': row.get('KPI Name', ''),
                    'type': row.get('Type', 'Other'),
                    'mean': float(row['Mean']) if 'Mean' in row and pd.notna(row['Mean']) else None,
                    'cv': float(row['CV(%)']) if 'CV(%)' in row and pd.notna(row['CV(%)']) else None,
                    'consistency': row.get('Consistency', 'Unknown'),
                    'raw_data': row.get('RawData', '')
                }
        
        # Get all_codes analysis results
        all_codes_df = self.analysis_results.get('all_codes', pd.DataFrame())
        
        # Build per-code severity map (ivy0210)
        code_severity_map = {}
        if not all_codes_df.empty:
            for _, row in all_codes_df.iterrows():
                c = row.get('Code', '')
                if c:
                    code_severity_map[c] = row.get('Severity', 'Normal')
        
        # Statistics summary
        kpi_df = filtered_consistency_by_type('KPI')
        counter_df = filtered_consistency_by_type('Counter')
        
        stats_summary = {
            'total_codes': len(consistency_df),
            'consistent': int((consistency_df['Consistency'] == 'Consistent').sum()) if 'Consistency' in consistency_df.columns else 0,
            'inconsistent': int((consistency_df['Consistency'] == 'Inconsistent').sum()) if 'Consistency' in consistency_df.columns else 0,
            'inconsistent_kpi': int((kpi_df['Consistency'] == 'Inconsistent').sum()) if 'Consistency' in kpi_df.columns else 0,
            'inconsistent_counter': int((counter_df['Consistency'] == 'Inconsistent').sum()) if 'Consistency' in counter_df.columns else 0,
            'inconsistent_kpi_trimmed': int(((kpi_df['Consistency'] == 'Inconsistent') & 
                                             ((kpi_df['DataCount'] < 5) | (kpi_df['Trimmed_Consistency'] == 'Inconsistent'))).sum()) if has_columns('Consistency', 'DataCount', 'Trimmed_Consistency') else 0,
            'inconsistent_counter_trimmed': int(((counter_df['Consistency'] == 'Inconsistent') & 
                                                  ((counter_df['DataCount'] < 5) | (counter_df['Trimmed_Consistency'] == 'Inconsistent'))).sum()) if has_columns('Consistency', 'DataCount', 'Trimmed_Consistency') else 0,
            'partial_null': int((consistency_df['Consistency'] == 'partial NULL').sum()) if 'Consistency' in consistency_df.columns else 0,
            'null': int((consistency_df['Consistency'] == 'NULL').sum()) if 'Consistency' in consistency_df.columns else 0,
            'severity_regression': int((all_codes_df['Severity'] == 'Regression').sum()) if not all_codes_df.empty else 0,
            'severity_suspicious': int((all_codes_df['Severity'] == 'Suspicious').sum()) if not all_codes_df.empty else 0,
            'severity_normal': int((all_codes_df['Severity'] == 'Normal').sum()) if not all_codes_df.empty else 0,
            'severity_nohistory': int((all_codes_df['Severity'] == 'NoHistory').sum()) if not all_codes_df.empty else 0,
        }
        
        # Inconsistent codes list (considering trimmed data)
        inconsistent_codes = []
        for _, row in consistency_df.iterrows():
            if row.get('Consistency') == 'Inconsistent':
                if row.get('DataCount', 0) >= 5 and row.get('Trimmed_Consistency') == 'Consistent':
                    continue
                inconsistent_codes.append(row.get('Code', ''))
        
        history_context = self.current_history_context or {}

        return {
            'filename': self.current_file.name,
            'filepath': str(self.current_file),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'environment': history_context.get('environment'),
            'test_config': history_context.get('test_config'),
            'scenario': history_context.get('scenario'),
            'scenario_key': history_context.get('scenario_key'),
            'history_key': history_context.get('history_key'),
            'ue_count': history_context.get('ue_count'),
            'stats': stats_summary,
            'inconsistent_codes': inconsistent_codes,
            'kpi_data': kpi_data,
            'code_severity': code_severity_map  # ivy0210: per-code severity for trend tracking
        }
    
    def compare_with_history(self):
        """Compare with history, generate change analysis"""
        if not self.previous_record:
            return None
        
        current_stats = self.analysis_results.get('consistency', pd.DataFrame())
        prev_stats = self.previous_record.get('stats', {})
        prev_inconsistent = set(self.previous_record.get('inconsistent_codes', []))
        
        # Get current inconsistent codes (considering trimmed data)
        current_inconsistent = set()
        for _, row in current_stats.iterrows():
            if row['Consistency'] == 'Inconsistent':
                if row['DataCount'] >= 5 and row['Trimmed_Consistency'] == 'Consistent':
                    continue
                current_inconsistent.add(row['Code'])
        
        # Calculate changes
        new_inconsistent = current_inconsistent - prev_inconsistent
        fixed = prev_inconsistent - current_inconsistent
        persistent = current_inconsistent & prev_inconsistent
        
        comparison = {
            'previous_file': self.previous_record.get('filename', 'N/A'),
            'previous_time': self.previous_record.get('timestamp', 'N/A'),
            'delta_inconsistent': len(current_inconsistent) - len(prev_inconsistent),
            'new_inconsistent': list(new_inconsistent),
            'fixed': list(fixed),
            'persistent': list(persistent),
            'prev_stats': prev_stats
        }
        
        self.analysis_results['comparison'] = comparison
        
        print("\n========== History Comparison ==========")
        print(f"  Previous file: {comparison['previous_file']}")
        print(f"  Inconsistent change: {comparison['delta_inconsistent']:+d}")
        print(f"  New inconsistent: {len(new_inconsistent)}")
        print(f"  Fixed: {len(fixed)}")
        print(f"  Persistent inconsistent: {len(persistent)}")
        
        return comparison
    
    def generate_report(self, generate_html=True):
        """Generate reports (Excel and optionally HTML)
        
        Args:
            generate_html: Whether to generate HTML report (default True)
            
        Returns:
            Path to generated Excel report
        """
        print("\n========== Generating Reports ==========")
        
        comparison = self.analysis_results.get('comparison', None)
        current_record = self.build_current_record()
        self.last_current_record = current_record
        
        # Generate Excel report
        excel_gen = ExcelReportGenerator(self.reports_dir)
        excel_file = excel_gen.generate(
            filename=self.current_file.stem,
            analysis_results=self.analysis_results,
            comparison=comparison,
            history_records=self.history_records,
            current_record=current_record,
            previous_record=self.previous_record  # ivy0210: for severity change tracking
        )
        
        # Generate HTML report
        html_file = None
        if generate_html:
            html_gen = HTMLReportGenerator(self.reports_dir)
            html_file = html_gen.generate(
                filename=self.current_file.stem,
                analysis_results=self.analysis_results,
                comparison=comparison,
                history_records=self.history_records
            )

        self.last_report_files = {
            'excel': excel_file,
            'html': html_file,
        }
        
        return excel_file
    
    def run(self, generate_html=True):
        """Run full analysis
        
        Args:
            generate_html: Whether to generate HTML report (default True)
            
        Returns:
            Path to generated report file
        """
        print("=" * 60)
        print("KPI Anomaly Detector (with History Tracking)")
        print("=" * 60)
        
        self.load_data()
        self.analyze_consistency()
        self.analyze_ttest_with_history()
        self.identify_suspicious_kpis()
        self.compare_with_history()
        
        report_file = self.generate_report(generate_html=generate_html)
        
        # Save current result to history
        current_record = self.build_current_record()
        self.save_history(current_record)
        
        return report_file
