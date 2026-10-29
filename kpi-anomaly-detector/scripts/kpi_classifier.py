code#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
KPI/Counter Classification Tool

Parses XML definition files and historical data to classify KPIs/Counters
for improved anomaly detection strategies.

Usage:
    python kpi_classifier.py                    # Generate classification Excel
    python kpi_classifier.py --analyze-history  # Include historical data analysis
"""

import sys
import re
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict

import pandas as pd
import numpy as np

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
LIB_DIR = PROJECT_ROOT / 'lib' / 'kpi_xml'
REPORTS_DIR = PROJECT_ROOT / 'reports'
HISTORY_FILE = REPORTS_DIR / 'kpi_history_records.json'


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
    # Derived fields
    category: str = ''
    data_type: str = ''  # success_rate, counter, latency, throughput, other
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


class KPIClassifier:
    """Parse XML files and classify KPIs/Counters"""
    
    def __init__(self):
        self.kpis: Dict[str, KPIDefinition] = {}
        self.counters: Dict[str, CounterDefinition] = {}
        self.history_stats: Dict[str, Dict] = {}
        
    def parse_kpi_xml(self, xml_path: Path) -> int:
        """Parse KPI definition XML file"""
        print(f"Parsing KPI XML: {xml_path.name}")
        
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"  Warning: XML parse error - {e}")
            # Try to parse with error recovery
            with open(xml_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Simple recovery: wrap in root if needed
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
            
            # Classify data type
            kpi.data_type = self._classify_data_type(kpi)
            
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
        # Pattern: M followed by digits and C followed by digits (e.g., M55110C00003)
        pattern = r'M\d+C\d+'
        return list(set(re.findall(pattern, formula)))
    
    def _classify_data_type(self, kpi: KPIDefinition) -> str:
        """Classify KPI data type based on formula and units"""
        formula_lower = kpi.formula.lower()
        units_lower = kpi.units.lower()
        name_lower = kpi.name.lower()
        
        # Success rate: units=% and formula contains 100*
        if kpi.units == '%' or '100 *' in kpi.formula or '100*' in kpi.formula:
            if 'ratio' in name_lower or 'rate' in name_lower or 'success' in name_lower:
                return 'success_rate'
            if 'failure' in name_lower or 'drop' in name_lower:
                return 'failure_rate'
            return 'percentage'
        
        # Latency
        if any(u in units_lower for u in ['ms', 'microsecond', 'second', 'millisecond']):
            return 'latency'
        
        # Throughput
        if any(u in units_lower for u in ['mb', 'byte', 'bit', 'kbit']):
            return 'throughput'
        
        # Signal quality
        if any(u in units_lower for u in ['db', 'dbm']):
            return 'signal_quality'
        
        # Counter (no units or integer)
        if not kpi.units or 'integer' in units_lower or 'number' in units_lower:
            # Check if it's derived (ratio formula)
            if '/' in kpi.formula and '100' not in kpi.formula:
                return 'ratio'
            return 'counter'
        
        return 'other'
    
    def _extract_category(self, level: str) -> str:
        """Extract category from KPI level"""
        if not level:
            return 'Unknown'
        
        # Common categories
        categories = ['Accessibility', 'Retainability', 'Integrity', 'Mobility', 
                      'Availability', 'Throughput', 'Utilization', 'Energy']
        
        for cat in categories:
            if cat in level:
                return cat
        
        return level.split()[-1] if level else 'Other'
    
    def analyze_history(self) -> Dict[str, Dict]:
        """Analyze historical data to understand KPI behavior"""
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
        
        for record in records:
            kpi_data = record.get('kpi_data', {})
            for code, data in kpi_data.items():
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
        
        # Calculate statistics
        stats = {}
        for code in code_values:
            values = code_values[code]
            means = code_means[code]
            consistencies = code_consistencies[code]
            
            if not values:
                continue
            
            arr = np.array(values)
            mean_val = np.mean(arr)
            std_val = np.std(arr)
            cv = (std_val / mean_val * 100) if mean_val != 0 else 0
            
            # Determine variance type
            if std_val == 0:
                if mean_val == 100:
                    variance_type = 'ceiling'
                elif mean_val == 0:
                    variance_type = 'floor'
                else:
                    variance_type = 'constant'
            elif cv < 5:
                variance_type = 'stable'
            elif cv < 20:
                variance_type = 'moderate'
            else:
                variance_type = 'high_variance'
            
            # Check trend
            trend = 'none'
            if len(means) >= 3:
                diffs = [means[i+1] - means[i] for i in range(len(means)-1)]
                if all(d > 0 for d in diffs):
                    trend = 'increasing'
                elif all(d < 0 for d in diffs):
                    trend = 'decreasing'
            
            # Consistency rate
            consistent_count = sum(1 for c in consistencies if c in ('Consistent', 'OK'))
            consistency_rate = consistent_count / len(consistencies) * 100 if consistencies else 0
            
            stats[code] = {
                'mean': round(mean_val, 4),
                'std': round(std_val, 4),
                'cv': round(cv, 2),
                'min': round(np.min(arr), 4),
                'max': round(np.max(arr), 4),
                'n_records': len(means),
                'n_values': len(values),
                'variance_type': variance_type,
                'trend': trend,
                'consistency_rate': round(consistency_rate, 1),
            }
        
        self.history_stats = stats
        print(f"  Analyzed {len(stats)} codes")
        
        # Summary
        variance_counts = defaultdict(int)
        for s in stats.values():
            variance_counts[s['variance_type']] += 1
        
        print("\n  Variance distribution:")
        for vtype, count in sorted(variance_counts.items(), key=lambda x: -x[1]):
            print(f"    {vtype}: {count}")
        
        return stats
    
    def generate_classification_excel(self, output_path: Path = None):
        """Generate classification Excel file"""
        if output_path is None:
            output_path = LIB_DIR / 'kpi_classification.xlsx'
        
        print(f"\nGenerating classification Excel: {output_path}")
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Sheet 1: KPI Classification
            kpi_rows = []
            for kpi_id, kpi in self.kpis.items():
                hist = self.history_stats.get(kpi_id, {})
                kpi_rows.append({
                    'Code': kpi_id,
                    'KPI Name': kpi.name,
                    'Category': kpi.category,
                    'Level': kpi.level,
                    'Data Type': kpi.data_type,
                    'Units': kpi.units,
                    'Formula': kpi.formula[:100] + '...' if len(kpi.formula) > 100 else kpi.formula,
                    'Related Counters': ', '.join(kpi.related_counters[:5]),
                    'NE': kpi.ne,
                    # History stats
                    'Hist_Mean': hist.get('mean', ''),
                    'Hist_Std': hist.get('std', ''),
                    'Hist_CV': hist.get('cv', ''),
                    'Variance_Type': hist.get('variance_type', ''),
                    'Trend': hist.get('trend', ''),
                    'Consistency_Rate': hist.get('consistency_rate', ''),
                    'N_Records': hist.get('n_records', ''),
                })
            
            kpi_df = pd.DataFrame(kpi_rows)
            kpi_df.to_excel(writer, sheet_name='1_KPI_Classification', index=False)
            print(f"  Sheet 1: {len(kpi_df)} KPIs")
            
            # Sheet 2: Counter Classification
            counter_rows = []
            for name, counter in self.counters.items():
                hist = self.history_stats.get(name, {})
                counter_rows.append({
                    'Code': name,
                    'NetAct Name': counter.netact,
                    'Units': counter.units,
                    'Peg Type': counter.peg_type,
                    'Time Aggregation': counter.time_aggregation,
                    'Measurement': f"{counter.measurement_id} ({counter.measurement_name})",
                    'Description': counter.desc[:100] + '...' if len(counter.desc) > 100 else counter.desc,
                    # History stats
                    'Hist_Mean': hist.get('mean', ''),
                    'Hist_Std': hist.get('std', ''),
                    'Hist_CV': hist.get('cv', ''),
                    'Variance_Type': hist.get('variance_type', ''),
                    'Trend': hist.get('trend', ''),
                    'Consistency_Rate': hist.get('consistency_rate', ''),
                    'N_Records': hist.get('n_records', ''),
                })
            
            counter_df = pd.DataFrame(counter_rows)
            counter_df.to_excel(writer, sheet_name='2_Counter_Classification', index=False)
            print(f"  Sheet 2: {len(counter_df)} Counters")
            
            # Sheet 3: KPI-Counter Relations
            relation_rows = []
            for kpi_id, kpi in self.kpis.items():
                for counter_name in kpi.related_counters:
                    counter = self.counters.get(counter_name)
                    relation_rows.append({
                        'KPI Code': kpi_id,
                        'KPI Name': kpi.name,
                        'Counter Code': counter_name,
                        'Counter NetAct': counter.netact if counter else '',
                        'Counter Units': counter.units if counter else '',
                    })
            
            relation_df = pd.DataFrame(relation_rows)
            relation_df.to_excel(writer, sheet_name='3_KPI_Counter_Relations', index=False)
            print(f"  Sheet 3: {len(relation_df)} relations")
            
            # Sheet 4: History Statistics Summary
            if self.history_stats:
                hist_rows = []
                for code, stats in self.history_stats.items():
                    # Determine if it's KPI or Counter
                    code_type = 'KPI' if code in self.kpis else ('Counter' if code in self.counters else 'Unknown')
                    
                    # Get additional info
                    kpi = self.kpis.get(code)
                    counter = self.counters.get(code)
                    
                    hist_rows.append({
                        'Code': code,
                        'Type': code_type,
                        'Name': kpi.name if kpi else (counter.netact if counter else ''),
                        'Data Type': kpi.data_type if kpi else '',
                        'Units': kpi.units if kpi else (counter.units if counter else ''),
                        'Mean': stats['mean'],
                        'Std': stats['std'],
                        'CV(%)': stats['cv'],
                        'Min': stats['min'],
                        'Max': stats['max'],
                        'Variance Type': stats['variance_type'],
                        'Trend': stats['trend'],
                        'Consistency Rate(%)': stats['consistency_rate'],
                        'N Records': stats['n_records'],
                        'N Values': stats['n_values'],
                    })
                
                hist_df = pd.DataFrame(hist_rows)
                # Sort by variance type for easy review
                type_order = {'ceiling': 0, 'floor': 1, 'constant': 2, 'stable': 3, 'moderate': 4, 'high_variance': 5}
                hist_df['_sort'] = hist_df['Variance Type'].map(type_order)
                hist_df = hist_df.sort_values(['_sort', 'CV(%)']).drop(columns=['_sort'])
                hist_df.to_excel(writer, sheet_name='4_History_Statistics', index=False)
                print(f"  Sheet 4: {len(hist_df)} codes with history")
            
            # Sheet 5: Anomaly Strategy Recommendations
            strategy_rows = []
            for code, stats in self.history_stats.items():
                kpi = self.kpis.get(code)
                variance_type = stats['variance_type']
                data_type = kpi.data_type if kpi else 'counter'
                
                # Recommend strategy
                if variance_type in ('ceiling', 'floor', 'constant'):
                    strategy = 'rule_based'
                    reason = f"Zero-variance ({variance_type}), σ=0, SPC invalid"
                    thresholds = self._get_rule_based_thresholds(variance_type, stats['mean'], data_type)
                elif data_type == 'success_rate':
                    strategy = 'threshold_based'
                    reason = "Success rate KPI, use fixed thresholds"
                    thresholds = "Normal>=99%, Suspicious>=95%, Regression<95%"
                elif data_type == 'failure_rate':
                    strategy = 'threshold_based'
                    reason = "Failure rate KPI, lower is better"
                    thresholds = "Normal<=1%, Suspicious<=5%, Regression>5%"
                elif stats['cv'] < 5:
                    strategy = 'strict_spc'
                    reason = f"Low variance (CV={stats['cv']}%), use strict 2σ/3σ"
                    thresholds = "Normal<=2σ, Suspicious<=3σ, Regression>3σ"
                else:
                    strategy = 'standard_spc'
                    reason = f"Standard variance (CV={stats['cv']}%)"
                    thresholds = "Normal<=2σ, Suspicious<=3σ, Regression>3σ"
                
                strategy_rows.append({
                    'Code': code,
                    'Data Type': data_type,
                    'Variance Type': variance_type,
                    'CV(%)': stats['cv'],
                    'Recommended Strategy': strategy,
                    'Reason': reason,
                    'Thresholds': thresholds,
                })
            
            strategy_df = pd.DataFrame(strategy_rows)
            strategy_df.to_excel(writer, sheet_name='5_Strategy_Recommendations', index=False)
            print(f"  Sheet 5: {len(strategy_df)} strategy recommendations")
        
        print(f"\nClassification Excel saved to: {output_path}")
        return output_path
    
    def _get_rule_based_thresholds(self, variance_type: str, mean_val: float, data_type: str) -> str:
        """Get rule-based thresholds for zero-variance KPIs"""
        if variance_type == 'ceiling':
            return "Normal=100%, Acceptable>=99.8%, Suspicious>=99%, Regression<99%"
        elif variance_type == 'floor':
            return "Normal=0, Acceptable<=0.2, Suspicious<=1, Regression>1"
        else:
            if abs(mean_val) >= 10:
                return f"Normal=±0.5%, Suspicious=±2%, Regression>2% (relative)"
            else:
                return f"Normal=±0.1, Suspicious=±1, Regression>1 (absolute)"
    
    def run(self, analyze_history: bool = True):
        """Run classification"""
        print("=" * 60)
        print("KPI/Counter Classification Tool")
        print("=" * 60)
        
        # Parse XML files
        for xml_file in LIB_DIR.glob('PMKPI*.xml'):
            self.parse_kpi_xml(xml_file)
        
        for xml_file in LIB_DIR.glob('JUMP*.xml'):
            self.parse_kpi_xml(xml_file)
        
        for xml_file in LIB_DIR.glob('PMPegs*.xml'):
            self.parse_counter_xml(xml_file)
        
        # Analyze history
        if analyze_history:
            self.analyze_history()
        
        # Generate Excel
        output_path = self.generate_classification_excel()
        
        print("\n" + "=" * 60)
        print("Summary:")
        print(f"  Total KPIs: {len(self.kpis)}")
        print(f"  Total Counters: {len(self.counters)}")
        print(f"  Codes with history: {len(self.history_stats)}")
        print("=" * 60)
        
        return output_path


def main():
    """Main entry point"""
    analyze_history = '--analyze-history' in sys.argv or True  # Default to analyze
    
    classifier = KPIClassifier()
    classifier.run(analyze_history=analyze_history)


if __name__ == "__main__":
    main()
