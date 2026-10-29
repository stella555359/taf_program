#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
KPI/Counter Classification Tool V2

Enhanced classification based on:
1. XML definitions (PMKPI, JUMP_KPIs, PMPegs)
2. Historical data characteristics
3. KPI type-based anomaly detection strategies

KPI Types (based on user requirements):
- ceiling_saturated: Success rate ≈100%, σ=0 → ABS_THRESHOLD ONLY
- floor_saturated: Failure count ≈0, σ=0 → ABS_THRESHOLD ONLY
- count_type: Discrete counts, high variance → RANGE + CONTEXT
- ratio_type: Non-saturated 0-100% → RELATIVE CHANGE
- physical_stable: dB/dBm, low variance → ABS_DELTA + TREND
- throughput_type: MB/bytes, right-skewed → QUANTILES
- latency_type: ms/us, right-skewed → TAIL AWARE
- low_frequency: Mostly 0, occasional 1 → WINDOW COUNT
- config_type: Discrete states → SEMANTIC RULE

Usage:
    python kpi_classifier_v2.py                    # Generate classification Excel
    python kpi_classifier_v2.py --compare          # Compare with current method
"""

import sys
import re
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict
from enum import Enum

import pandas as pd
import numpy as np

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
LIB_DIR = PROJECT_ROOT / 'lib' / 'kpi_xml'
REPORTS_DIR = PROJECT_ROOT / 'reports'
HISTORY_FILE = REPORTS_DIR / 'kpi_history_records.json'


class KPIType(Enum):
    """KPI classification types based on anomaly detection strategy"""
    CEILING_SATURATED = "ceiling_saturated"      # Success rate ~100%
    FLOOR_SATURATED = "floor_saturated"          # Failure count ~0
    COUNT_TYPE = "count_type"                    # Discrete counts
    RATIO_TYPE = "ratio_type"                    # Non-saturated ratios
    PHYSICAL_STABLE = "physical_stable"          # dB/dBm measurements
    THROUGHPUT_TYPE = "throughput_type"          # Data volume
    LATENCY_TYPE = "latency_type"                # Time delays
    LOW_FREQUENCY = "low_frequency"              # Rare events
    CONFIG_TYPE = "config_type"                  # Configuration states
    UNKNOWN = "unknown"


class DetectionStrategy(Enum):
    """Anomaly detection strategies"""
    ABS_THRESHOLD = "ABS_THRESHOLD"      # Absolute threshold only
    RANGE_CONTEXT = "RANGE_CONTEXT"      # Range with context
    RELATIVE_CHANGE = "RELATIVE_CHANGE"  # Relative delta
    ABS_DELTA_TREND = "ABS_DELTA_TREND"  # Absolute delta + trend
    QUANTILES = "QUANTILES"              # Percentile-based
    TAIL_AWARE = "TAIL_AWARE"            # Tail distribution
    WINDOW_COUNT = "WINDOW_COUNT"        # Window counting
    SEMANTIC_RULE = "SEMANTIC_RULE"      # Rule-based
    STANDARD_SPC = "STANDARD_SPC"        # Standard SPC


@dataclass
class KPIDefinition:
    """KPI definition from XML"""
    id: str
    name: str
    level: str = ''
    formula: str = ''
    units: str = ''
    desc: str = ''
    ne: str = ''
    category: str = ''
    related_counters: List[str] = field(default_factory=list)


@dataclass
class CounterDefinition:
    """Counter definition from XML"""
    name: str
    netact: str = ''
    units: str = ''
    time_aggregation: str = ''
    desc: str = ''
    peg_type: str = ''
    measurement_id: str = ''
    measurement_name: str = ''


@dataclass
class CodeClassification:
    """Complete classification for a code"""
    code: str
    original_code: str  # Original code before normalization
    code_type: str  # 'KPI' or 'Counter'
    name: str
    units: str
    
    # From XML
    xml_found: bool = False
    level: str = ''
    formula: str = ''
    desc: str = ''
    related_counters: List[str] = field(default_factory=list)
    
    # From history analysis
    has_history: bool = False
    hist_mean: float = 0.0
    hist_std: float = 0.0
    hist_cv: float = 0.0
    hist_min: float = 0.0
    hist_max: float = 0.0
    n_records: int = 0
    n_values: int = 0
    consistency_rate: float = 0.0
    
    # Classification result
    kpi_type: KPIType = KPIType.UNKNOWN
    detection_strategy: DetectionStrategy = DetectionStrategy.STANDARD_SPC
    variance_type: str = ''  # ceiling/floor/constant/stable/moderate/high_variance
    classification_reason: str = ''
    
    # Detection parameters
    thresholds: str = ''
    forbidden_methods: str = ''


class KPIClassifierV2:
    """Enhanced KPI/Counter classifier"""
    
    def __init__(self):
        self.kpis: Dict[str, KPIDefinition] = {}
        self.counters: Dict[str, CounterDefinition] = {}
        self.history_codes: Set[str] = set()
        self.classifications: Dict[str, CodeClassification] = {}
        
    def parse_kpi_xml(self, xml_path: Path) -> int:
        """Parse KPI definition XML file"""
        print(f"Parsing KPI XML: {xml_path.name}")
        
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"  Warning: XML parse error - {e}")
            with open(xml_path, 'r', encoding='utf-8') as f:
                content = f.read()
            if not content.strip().startswith('<?xml'):
                content = '<?xml version="1.0"?>\n' + content
            root = ET.fromstring(content)
        
        count = 0
        for kpi_elem in root.findall('.//KPI'):
            kpi_id = kpi_elem.get('id', '')
            if not kpi_id:
                continue
                
            kpi = KPIDefinition(
                id=kpi_id,
                name=kpi_elem.get('name', ''),
                level=kpi_elem.get('level', ''),
                formula=kpi_elem.get('formula', ''),
                units=kpi_elem.get('units', ''),
                desc=kpi_elem.get('desc', ''),
                ne=kpi_elem.get('ne', ''),
            )
            
            # Extract related counters from formula
            kpi.related_counters = self._extract_counters_from_formula(kpi.formula)
            
            # Extract category from level
            kpi.category = self._extract_category(kpi.level)
            
            self.kpis[kpi_id] = kpi
            count += 1
        
        print(f"  Loaded {count} KPIs")
        return count
    
    def parse_counter_xml(self, xml_path: Path) -> int:
        """Parse Counter (PMPegs) definition XML file"""
        print(f"Parsing Counter XML: {xml_path.name}")
        
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"  Warning: XML parse error - {e}")
            return 0
        
        count = 0
        for measurement in root.findall('.//Measurement'):
            meas_id = measurement.get('id', '')
            meas_name = measurement.get('name', '')
            
            for peg in measurement.findall('peg'):
                counter_name = peg.get('name', '')
                if not counter_name:
                    continue
                
                counter = CounterDefinition(
                    name=counter_name,
                    netact=peg.get('NetAct', ''),
                    units=peg.get('units', ''),
                    time_aggregation=peg.get('timeAggregation', ''),
                    desc=peg.get('desc', ''),
                    peg_type=peg.get('type', ''),
                    measurement_id=meas_id,
                    measurement_name=meas_name,
                )
                self.counters[counter_name] = counter
                count += 1
        
        print(f"  Loaded {count} Counters")
        return count
    
    def _extract_counters_from_formula(self, formula: str) -> List[str]:
        """Extract counter references from KPI formula"""
        if not formula:
            return []
        pattern = r'M\d+C\d+'
        return list(set(re.findall(pattern, formula)))
    
    def _extract_category(self, level: str) -> str:
        """Extract category from KPI level"""
        if not level:
            return 'Unknown'
        
        categories = ['Accessibility', 'Retainability', 'Integrity', 'Mobility', 
                      'Availability', 'Throughput', 'Utilization', 'Energy']
        
        for cat in categories:
            if cat in level:
                return cat
        
        return level.split()[-1] if level else 'Other'
    
    def _normalize_code(self, code: str) -> str:
        """Normalize code for lookup (handle SCOUNT_NR_ prefix)"""
        # Remove SCOUNT_ prefix for lookup
        if code.startswith('SCOUNT_'):
            return code[7:]  # Remove 'SCOUNT_'
        return code
    
    def _find_definition(self, code: str) -> Tuple[Optional[KPIDefinition], Optional[CounterDefinition]]:
        """Find KPI or Counter definition for a code"""
        # Direct lookup
        if code in self.kpis:
            return self.kpis[code], None
        if code in self.counters:
            return None, self.counters[code]
        
        # Normalized lookup (for SCOUNT_ prefix)
        norm_code = self._normalize_code(code)
        if norm_code != code:
            if norm_code in self.kpis:
                return self.kpis[norm_code], None
            if norm_code in self.counters:
                return None, self.counters[norm_code]
        
        return None, None
    
    def analyze_history(self) -> Dict[str, dict]:
        """Analyze historical data for all codes"""
        print(f"\nAnalyzing historical data: {HISTORY_FILE}")
        
        if not HISTORY_FILE.exists():
            print("  No history file found")
            return {}
        
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            records = json.load(f)
        
        print(f"  Found {len(records)} historical records")
        
        # Collect all values for each code
        code_values: Dict[str, List[float]] = defaultdict(list)
        code_means: Dict[str, List[float]] = defaultdict(list)
        code_consistencies: Dict[str, List[str]] = defaultdict(list)
        code_names: Dict[str, str] = {}
        
        for record in records:
            kpi_data = record.get('kpi_data', {})
            for code, data in kpi_data.items():
                self.history_codes.add(code)
                
                # Store name
                if 'kpi_name' in data and code not in code_names:
                    code_names[code] = data['kpi_name']
                
                raw_data = data.get('raw_data', '')
                if raw_data:
                    try:
                        values = [float(x) for x in raw_data.split(',') if x.strip()]
                        code_values[code].extend(values)
                        if values:
                            code_means[code].append(np.mean(values))
                    except:
                        pass
                consistency = data.get('consistency', '')
                if consistency:
                    code_consistencies[code].append(consistency)
        
        print(f"  Total unique codes in history: {len(self.history_codes)}")
        
        # Calculate statistics
        stats = {}
        for code in self.history_codes:
            values = code_values.get(code, [])
            means = code_means.get(code, [])
            consistencies = code_consistencies.get(code, [])
            
            if values:
                arr = np.array(values)
                mean_val = float(np.mean(arr))
                std_val = float(np.std(arr))
                cv = (std_val / mean_val * 100) if mean_val != 0 else (float('inf') if std_val > 0 else 0)
                
                stats[code] = {
                    'name': code_names.get(code, ''),
                    'mean': mean_val,
                    'std': std_val,
                    'cv': cv,
                    'min': float(np.min(arr)),
                    'max': float(np.max(arr)),
                    'n_records': len(means),
                    'n_values': len(values),
                    'consistencies': consistencies,
                }
            else:
                stats[code] = {
                    'name': code_names.get(code, ''),
                    'mean': 0,
                    'std': 0,
                    'cv': 0,
                    'min': 0,
                    'max': 0,
                    'n_records': 0,
                    'n_values': 0,
                    'consistencies': consistencies,
                }
        
        return stats
    
    def classify_all_codes(self, history_stats: Dict[str, dict]):
        """Classify all codes from history"""
        print(f"\nClassifying {len(self.history_codes)} codes from history...")
        
        for code in self.history_codes:
            stats = history_stats.get(code, {})
            
            # Find XML definition
            kpi_def, counter_def = self._find_definition(code)
            
            # Create classification object
            cls = CodeClassification(
                code=code,
                original_code=code,
                code_type='KPI' if kpi_def else ('Counter' if counter_def else 'Unknown'),
                name=stats.get('name', '') or (kpi_def.name if kpi_def else (counter_def.netact if counter_def else '')),
                units=kpi_def.units if kpi_def else (counter_def.units if counter_def else ''),
            )
            
            # Fill XML info
            if kpi_def:
                cls.xml_found = True
                cls.level = kpi_def.level
                cls.formula = kpi_def.formula
                cls.desc = kpi_def.desc
                cls.related_counters = kpi_def.related_counters
            elif counter_def:
                cls.xml_found = True
                cls.desc = counter_def.desc
            
            # Fill history stats
            if stats.get('n_values', 0) > 0:
                cls.has_history = True
                cls.hist_mean = stats['mean']
                cls.hist_std = stats['std']
                cls.hist_cv = stats['cv']
                cls.hist_min = stats['min']
                cls.hist_max = stats['max']
                cls.n_records = stats['n_records']
                cls.n_values = stats['n_values']
                
                # Consistency rate
                consistencies = stats.get('consistencies', [])
                if consistencies:
                    consistent_count = sum(1 for c in consistencies if c in ('Consistent', 'OK'))
                    cls.consistency_rate = consistent_count / len(consistencies) * 100
            
            # Classify KPI type and strategy
            self._classify_kpi_type(cls)
            
            self.classifications[code] = cls
        
        # Summary
        type_counts = defaultdict(int)
        for cls in self.classifications.values():
            type_counts[cls.kpi_type.value] += 1
        
        print("\n  KPI Type Distribution:")
        for ktype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"    {ktype}: {count}")
    
    def _classify_kpi_type(self, cls: CodeClassification):
        """Classify KPI type based on all available information"""
        name_lower = cls.name.lower()
        units_lower = cls.units.lower()
        code_lower = cls.code.lower()
        
        # Step 1: Determine variance type from history
        if cls.has_history:
            if cls.hist_std == 0:
                if cls.hist_mean == 100 or (cls.hist_mean >= 99.9 and 'ratio' in name_lower):
                    cls.variance_type = 'ceiling'
                elif cls.hist_mean == 0 or cls.hist_mean < 0.01:
                    cls.variance_type = 'floor'
                else:
                    cls.variance_type = 'constant'
            elif cls.hist_cv < 1:
                cls.variance_type = 'near_zero_var'
            elif cls.hist_cv < 5:
                cls.variance_type = 'stable'
            elif cls.hist_cv < 20:
                cls.variance_type = 'moderate'
            else:
                cls.variance_type = 'high_variance'
        
        # Step 2: Classify by type (priority order)
        
        # 2a. Config/State type (discrete)
        if any(kw in name_lower for kw in ['enabled', 'disabled', 'config', 'feature', 'mode', 'state']):
            cls.kpi_type = KPIType.CONFIG_TYPE
            cls.detection_strategy = DetectionStrategy.SEMANTIC_RULE
            cls.classification_reason = "Configuration/state KPI, discrete values"
            cls.thresholds = "Rule: value change detection"
            cls.forbidden_methods = "All statistical methods"
            return
        
        # 2b. Ceiling saturated (success rate ~100%)
        if cls.variance_type == 'ceiling':
            cls.kpi_type = KPIType.CEILING_SATURATED
            cls.detection_strategy = DetectionStrategy.ABS_THRESHOLD
            cls.classification_reason = f"Ceiling KPI: mean={cls.hist_mean:.2f}, σ=0"
            cls.thresholds = "Normal=100%, Acceptable≥99.9%, Suspicious≥99%, Regression<99%"
            cls.forbidden_methods = "SPC, ±kσ, T-test"
            return
        
        # Check for success rate by name/formula
        is_success_rate = (
            any(kw in name_lower for kw in ['success ratio', 'success rate', 'completion rate']) or
            (cls.units == '%' and '100' in cls.formula and any(kw in name_lower for kw in ['ratio', 'rate']))
        )
        if is_success_rate and cls.hist_mean >= 95:
            cls.kpi_type = KPIType.CEILING_SATURATED
            cls.detection_strategy = DetectionStrategy.ABS_THRESHOLD
            cls.classification_reason = f"Success rate KPI with high baseline: mean={cls.hist_mean:.2f}%"
            cls.thresholds = "Normal≥99.5%, Suspicious≥95%, Regression<95%"
            cls.forbidden_methods = "SPC (when σ→0), T-test"
            return
        
        # 2c. Floor saturated (failure/error ~0)
        if cls.variance_type == 'floor':
            cls.kpi_type = KPIType.FLOOR_SATURATED
            cls.detection_strategy = DetectionStrategy.ABS_THRESHOLD
            cls.classification_reason = f"Floor KPI: mean={cls.hist_mean:.4f}, σ=0"
            cls.thresholds = "Normal=0, Acceptable≤0.1, Suspicious≤1, Regression>1"
            cls.forbidden_methods = "SPC, ±kσ, T-test"
            return
        
        # Check for failure/error by name
        is_failure_type = any(kw in name_lower for kw in ['fail', 'error', 'drop', 'reject', 'abort', 'release'])
        if is_failure_type and cls.hist_mean <= 1:
            cls.kpi_type = KPIType.FLOOR_SATURATED
            cls.detection_strategy = DetectionStrategy.ABS_THRESHOLD
            cls.classification_reason = f"Low failure rate KPI: mean={cls.hist_mean:.4f}"
            cls.thresholds = "Normal≤0.1, Suspicious≤1, Regression>1"
            cls.forbidden_methods = "SPC (when σ→0)"
            return
        
        # 2d. Low frequency events (mostly 0)
        if cls.has_history and cls.hist_max <= 5 and cls.hist_mean < 1:
            cls.kpi_type = KPIType.LOW_FREQUENCY
            cls.detection_strategy = DetectionStrategy.WINDOW_COUNT
            cls.classification_reason = f"Low frequency events: mean={cls.hist_mean:.4f}, max={cls.hist_max}"
            cls.thresholds = "Window sum, event rate threshold"
            cls.forbidden_methods = "SPC, σ-based methods"
            return
        
        # 2e. Physical stable (dB/dBm)
        if any(u in units_lower for u in ['db', 'dbm']):
            cls.kpi_type = KPIType.PHYSICAL_STABLE
            cls.detection_strategy = DetectionStrategy.ABS_DELTA_TREND
            cls.classification_reason = f"Physical measurement KPI (units={cls.units})"
            if cls.variance_type in ('near_zero_var', 'stable'):
                cls.thresholds = "Δ>0.5dB warning, Δ>1dB regression, trend detection"
            else:
                cls.thresholds = "Δ>1dB warning, Δ>2dB regression, trend detection"
            cls.forbidden_methods = "Single point ±2σ, σ amplification"
            return
        
        # 2f. Latency type (ms, microsecond)
        if any(u in units_lower for u in ['ms', 'microsecond', 'millisecond', 'second', 'us']):
            cls.kpi_type = KPIType.LATENCY_TYPE
            cls.detection_strategy = DetectionStrategy.TAIL_AWARE
            cls.classification_reason = f"Latency KPI (units={cls.units})"
            cls.thresholds = "P95/P99 monitoring, tail growth detection"
            cls.forbidden_methods = "Mean ±σ"
            return
        
        if any(kw in name_lower for kw in ['time', 'delay', 'latency', 'duration']):
            cls.kpi_type = KPIType.LATENCY_TYPE
            cls.detection_strategy = DetectionStrategy.TAIL_AWARE
            cls.classification_reason = "Latency KPI (by name)"
            cls.thresholds = "P95/P99 monitoring, tail growth detection"
            cls.forbidden_methods = "Mean ±σ"
            return
        
        # 2g. Throughput type (MB, bytes, bits)
        if any(u in units_lower for u in ['mb', 'byte', 'bit', 'kbit', 'mbit', 'gbit']):
            cls.kpi_type = KPIType.THROUGHPUT_TYPE
            cls.detection_strategy = DetectionStrategy.QUANTILES
            cls.classification_reason = f"Throughput KPI (units={cls.units})"
            cls.thresholds = "P50/P95 change detection, relative Δ%"
            cls.forbidden_methods = "Mean ±σ, T-test (unless large sample)"
            return
        
        if any(kw in name_lower for kw in ['throughput', 'volume', 'traffic', 'data']):
            cls.kpi_type = KPIType.THROUGHPUT_TYPE
            cls.detection_strategy = DetectionStrategy.QUANTILES
            cls.classification_reason = "Throughput KPI (by name)"
            cls.thresholds = "P50/P95 change detection, relative Δ%"
            cls.forbidden_methods = "Mean ±σ, T-test (unless large sample)"
            return
        
        # 2h. Count type (integer counts, high variance)
        is_counter = (
            cls.code_type == 'Counter' or
            'number' in units_lower or 'integer' in units_lower or
            any(kw in name_lower for kw in ['count', 'number of', 'attempt', 'request', 'transition'])
        )
        if is_counter:
            cls.kpi_type = KPIType.COUNT_TYPE
            cls.detection_strategy = DetectionStrategy.RANGE_CONTEXT
            cls.classification_reason = "Count type KPI/Counter"
            cls.thresholds = "Range [μ-2σ, μ+2σ], Poisson check, context-aware"
            cls.forbidden_methods = "Small sample T-test, single point judgment"
            return
        
        # 2i. Ratio type (non-saturated percentages)
        if cls.units == '%' or any(kw in name_lower for kw in ['ratio', 'rate', 'percentage']):
            cls.kpi_type = KPIType.RATIO_TYPE
            cls.detection_strategy = DetectionStrategy.RELATIVE_CHANGE
            cls.classification_reason = "Non-saturated ratio KPI"
            cls.thresholds = "|Δ%| thresholds, SPC trend rules"
            cls.forbidden_methods = "Normal assumption, single T-test"
            return
        
        # 2j. Default: Standard SPC
        cls.kpi_type = KPIType.UNKNOWN
        cls.detection_strategy = DetectionStrategy.STANDARD_SPC
        cls.classification_reason = "Unclassified, using standard SPC"
        cls.thresholds = "Standard: Normal≤2σ, Suspicious≤3σ, Regression>3σ"
        cls.forbidden_methods = "None (use with caution)"
    
    def generate_classification_excel(self, output_path: Path = None):
        """Generate enhanced classification Excel file"""
        if output_path is None:
            output_path = LIB_DIR / 'kpi_classification_v2.xlsx'
        
        print(f"\nGenerating classification Excel: {output_path}")
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Sheet 1: All Codes Classification (main sheet)
            main_rows = []
            for code, cls in self.classifications.items():
                main_rows.append({
                    'Code': cls.code,
                    'Type': cls.code_type,
                    'Name': cls.name,
                    'XML_Found': '✓' if cls.xml_found else '',
                    'Has_History': '✓' if cls.has_history else '',
                    'Units': cls.units,
                    'KPI_Type': cls.kpi_type.value,
                    'Detection_Strategy': cls.detection_strategy.value,
                    'Variance_Type': cls.variance_type,
                    'Mean': round(cls.hist_mean, 4) if cls.has_history else '',
                    'Std': round(cls.hist_std, 4) if cls.has_history else '',
                    'CV(%)': round(cls.hist_cv, 2) if cls.has_history and cls.hist_cv < float('inf') else '',
                    'Min': round(cls.hist_min, 4) if cls.has_history else '',
                    'Max': round(cls.hist_max, 4) if cls.has_history else '',
                    'N_Records': cls.n_records,
                    'Consistency_Rate': round(cls.consistency_rate, 1) if cls.has_history else '',
                    'Classification_Reason': cls.classification_reason,
                    'Thresholds': cls.thresholds,
                    'Forbidden_Methods': cls.forbidden_methods,
                    'Level': cls.level,
                    'Formula': cls.formula[:80] + '...' if len(cls.formula) > 80 else cls.formula,
                    'Related_Counters': ', '.join(cls.related_counters[:3]),
                })
            
            main_df = pd.DataFrame(main_rows)
            # Sort by KPI Type
            type_order = {t.value: i for i, t in enumerate(KPIType)}
            main_df['_sort'] = main_df['KPI_Type'].map(type_order)
            main_df = main_df.sort_values(['_sort', 'Code']).drop(columns=['_sort'])
            main_df.to_excel(writer, sheet_name='1_All_Codes_Classification', index=False)
            print(f"  Sheet 1: {len(main_df)} codes (ALL history codes)")
            
            # Sheet 2: Summary by KPI Type
            type_summary = []
            type_counts = defaultdict(lambda: {'count': 0, 'xml_found': 0, 'examples': []})
            for cls in self.classifications.values():
                t = cls.kpi_type.value
                type_counts[t]['count'] += 1
                if cls.xml_found:
                    type_counts[t]['xml_found'] += 1
                if len(type_counts[t]['examples']) < 5:
                    type_counts[t]['examples'].append(cls.code)
            
            for ktype in KPIType:
                info = type_counts[ktype.value]
                strategy = {
                    KPIType.CEILING_SATURATED: DetectionStrategy.ABS_THRESHOLD,
                    KPIType.FLOOR_SATURATED: DetectionStrategy.ABS_THRESHOLD,
                    KPIType.COUNT_TYPE: DetectionStrategy.RANGE_CONTEXT,
                    KPIType.RATIO_TYPE: DetectionStrategy.RELATIVE_CHANGE,
                    KPIType.PHYSICAL_STABLE: DetectionStrategy.ABS_DELTA_TREND,
                    KPIType.THROUGHPUT_TYPE: DetectionStrategy.QUANTILES,
                    KPIType.LATENCY_TYPE: DetectionStrategy.TAIL_AWARE,
                    KPIType.LOW_FREQUENCY: DetectionStrategy.WINDOW_COUNT,
                    KPIType.CONFIG_TYPE: DetectionStrategy.SEMANTIC_RULE,
                    KPIType.UNKNOWN: DetectionStrategy.STANDARD_SPC,
                }.get(ktype, DetectionStrategy.STANDARD_SPC)
                
                type_summary.append({
                    'KPI_Type': ktype.value,
                    'Count': info['count'],
                    'XML_Found': info['xml_found'],
                    'Detection_Strategy': strategy.value,
                    'Description': self._get_type_description(ktype),
                    'Examples': ', '.join(info['examples'][:3]),
                })
            
            summary_df = pd.DataFrame(type_summary)
            summary_df.to_excel(writer, sheet_name='2_Type_Summary', index=False)
            print(f"  Sheet 2: Type summary ({len(KPIType)} types)")
            
            # Sheet 3: Detection Strategy Guide
            strategy_guide = [
                {'Strategy': 'ABS_THRESHOLD', 'When_to_Use': 'Ceiling/Floor saturated KPIs (σ=0)',
                 'Method': 'Fixed absolute thresholds', 'Forbidden': 'SPC, ±kσ, T-test'},
                {'Strategy': 'RANGE_CONTEXT', 'When_to_Use': 'Count type KPIs/Counters',
                 'Method': 'Range [μ-2σ, μ+2σ], Poisson', 'Forbidden': 'Small sample T-test'},
                {'Strategy': 'RELATIVE_CHANGE', 'When_to_Use': 'Non-saturated ratios',
                 'Method': '|Δ%| thresholds, SPC trends', 'Forbidden': 'Normal assumption'},
                {'Strategy': 'ABS_DELTA_TREND', 'When_to_Use': 'Physical measurements (dB)',
                 'Method': 'Absolute Δ + trend detection', 'Forbidden': 'Single point ±2σ'},
                {'Strategy': 'QUANTILES', 'When_to_Use': 'Throughput, right-skewed data',
                 'Method': 'P50/P95 change detection', 'Forbidden': 'Mean ±σ'},
                {'Strategy': 'TAIL_AWARE', 'When_to_Use': 'Latency, timing KPIs',
                 'Method': 'P95/P99 monitoring', 'Forbidden': 'Mean-based methods'},
                {'Strategy': 'WINDOW_COUNT', 'When_to_Use': 'Low frequency events',
                 'Method': 'Window sum, event rate', 'Forbidden': 'SPC, σ-based'},
                {'Strategy': 'SEMANTIC_RULE', 'When_to_Use': 'Config/State KPIs',
                 'Method': 'Rule-based, value change', 'Forbidden': 'All statistical'},
                {'Strategy': 'STANDARD_SPC', 'When_to_Use': 'Default/Unknown',
                 'Method': '±2σ/3σ control limits', 'Forbidden': 'None (use caution)'},
            ]
            guide_df = pd.DataFrame(strategy_guide)
            guide_df.to_excel(writer, sheet_name='3_Strategy_Guide', index=False)
            print(f"  Sheet 3: Strategy guide")
            
            # Sheet 4: XML Definition Lookup
            xml_rows = []
            for kpi_id, kpi in self.kpis.items():
                xml_rows.append({
                    'Code': kpi_id,
                    'Type': 'KPI',
                    'Name': kpi.name,
                    'Level': kpi.level,
                    'Category': kpi.category,
                    'Units': kpi.units,
                    'Formula': kpi.formula[:100] + '...' if len(kpi.formula) > 100 else kpi.formula,
                    'NE': kpi.ne,
                    'Description': kpi.desc[:100] + '...' if len(kpi.desc) > 100 else kpi.desc,
                })
            for counter_name, counter in self.counters.items():
                xml_rows.append({
                    'Code': counter_name,
                    'Type': 'Counter',
                    'Name': counter.netact,
                    'Level': '',
                    'Category': counter.measurement_name,
                    'Units': counter.units,
                    'Formula': '',
                    'NE': '',
                    'Description': counter.desc[:100] + '...' if len(counter.desc) > 100 else counter.desc,
                })
            xml_df = pd.DataFrame(xml_rows)
            xml_df.to_excel(writer, sheet_name='4_XML_Definitions', index=False)
            print(f"  Sheet 4: {len(xml_df)} XML definitions")
            
            # Sheet 5: Codes NOT found in XML
            not_found = []
            for code, cls in self.classifications.items():
                if not cls.xml_found:
                    norm_code = self._normalize_code(code)
                    not_found.append({
                        'Code': code,
                        'Normalized_Code': norm_code if norm_code != code else '',
                        'Name': cls.name,
                        'Has_History': '✓' if cls.has_history else '',
                        'Mean': round(cls.hist_mean, 4) if cls.has_history else '',
                        'KPI_Type': cls.kpi_type.value,
                    })
            not_found_df = pd.DataFrame(not_found)
            not_found_df.to_excel(writer, sheet_name='5_Codes_Not_In_XML', index=False)
            print(f"  Sheet 5: {len(not_found_df)} codes not found in XML")
        
        print(f"\nClassification Excel saved to: {output_path}")
        return output_path
    
    def _get_type_description(self, kpi_type: KPIType) -> str:
        """Get description for KPI type"""
        descriptions = {
            KPIType.CEILING_SATURATED: "Success rate ~100%, σ=0, e.g., RRC setup success ratio",
            KPIType.FLOOR_SATURATED: "Failure count ~0, σ=0, e.g., Drop rate",
            KPIType.COUNT_TYPE: "Discrete counts, UE/time dependent, e.g., RRC transitions",
            KPIType.RATIO_TYPE: "Non-saturated 0-100%, e.g., BLER",
            KPIType.PHYSICAL_STABLE: "dB/dBm measurements, low variance, e.g., RSSI, RIP",
            KPIType.THROUGHPUT_TYPE: "Data volume, right-skewed, e.g., DL throughput",
            KPIType.LATENCY_TYPE: "Time delays, right-skewed, e.g., RRC setup time",
            KPIType.LOW_FREQUENCY: "Rare events, mostly 0, e.g., Resume fail count",
            KPIType.CONFIG_TYPE: "Discrete states, e.g., Feature enabled",
            KPIType.UNKNOWN: "Unclassified, requires manual review",
        }
        return descriptions.get(kpi_type, "")
    
    def run(self):
        """Run enhanced classification"""
        print("=" * 60)
        print("KPI/Counter Classification Tool V2")
        print("=" * 60)
        
        # Parse XML files
        for xml_file in LIB_DIR.glob('PMKPI*.xml'):
            self.parse_kpi_xml(xml_file)
        
        for xml_file in LIB_DIR.glob('JUMP*.xml'):
            self.parse_kpi_xml(xml_file)
        
        for xml_file in LIB_DIR.glob('PMPegs*.xml'):
            self.parse_counter_xml(xml_file)
        
        # Analyze history
        history_stats = self.analyze_history()
        
        # Classify all codes
        self.classify_all_codes(history_stats)
        
        # Generate Excel
        output_path = self.generate_classification_excel()
        
        print("\n" + "=" * 60)
        print("Summary:")
        print(f"  XML KPIs: {len(self.kpis)}")
        print(f"  XML Counters: {len(self.counters)}")
        print(f"  History Codes: {len(self.history_codes)}")
        print(f"  Classified: {len(self.classifications)}")
        
        # XML match rate
        xml_found = sum(1 for c in self.classifications.values() if c.xml_found)
        print(f"  XML Match Rate: {xml_found}/{len(self.classifications)} ({xml_found/len(self.classifications)*100:.1f}%)")
        print("=" * 60)
        
        return output_path


def main():
    """Main entry point"""
    classifier = KPIClassifierV2()
    classifier.run()


if __name__ == "__main__":
    main()
