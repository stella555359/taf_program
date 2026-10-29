#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Update KPI classification files based on misclassification analysis

Updates:
1. kpi_classification_v2.xlsx - Main classification file
2. kpi_custom_rules.xlsx - Custom rules file

Focus on high-confidence corrections:
- RTWP counters: low_frequency -> physical_stable
- Other physical measurements with stable patterns
- Floor saturated corrections
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import shutil


def load_misclassified_analysis(analysis_path: Path) -> list:
    """Load misclassified KPIs analysis results"""
    with open(analysis_path, encoding='utf-8') as f:
        return json.load(f)


def filter_high_confidence_updates(misclassified: list) -> list:
    """Filter for high-confidence classification updates
    
    Only include updates where we're confident the new classification is better.
    """
    updates = []
    
    for item in misclassified:
        code = item['code']
        name = item.get('name', '')
        current_type = item['current_type']
        recommended_type = item['recommended_type']
        recommended_strategy = item['recommended_strategy']
        reason = item['reason']
        profile = item.get('data_profile', {})
        
        # Skip if no recommendation
        if not recommended_type or recommended_type == 'unknown':
            continue
        
        confidence = 'low'
        
        # High confidence: low_frequency -> physical_stable for dBm values
        if current_type == 'low_frequency' and recommended_type == 'physical_stable':
            mean = profile.get('mean', 0)
            if mean < 0:  # Negative dBm values
                confidence = 'high'
        
        # High confidence: config_type -> floor_saturated for all-zero
        if current_type == 'config_type' and recommended_type == 'floor_saturated':
            mean = profile.get('mean', 0)
            mean_range = profile.get('mean_range', 0)
            if abs(mean) < 0.001 and mean_range < 0.001:
                confidence = 'high'
        
        # High confidence: ceiling_saturated -> ratio_type for values with variation
        if current_type == 'ceiling_saturated' and recommended_type == 'ratio_type':
            mean_range = profile.get('mean_range', 0)
            if mean_range > 5:  # More than 5% variation
                confidence = 'medium'
        
        # High confidence: ceiling_saturated -> physical_stable for very stable values
        if current_type == 'ceiling_saturated' and recommended_type == 'physical_stable':
            mean_range = profile.get('mean_range', 0)
            if mean_range < 3:  # Very stable
                confidence = 'high'
        
        # High confidence: floor_saturated -> values that are not actually zero
        if current_type == 'floor_saturated':
            mean = profile.get('mean', 0)
            if abs(mean) > 1:  # Not near zero
                confidence = 'medium'
        
        # Add patterns by name for RTWP, RSSI, RIP, etc.
        name_lower = name.lower()
        if any(keyword in name_lower for keyword in ['rtwp', 'rssi', 'rip', 'sinr', 'snr', 'voltage']):
            if recommended_type == 'physical_stable':
                confidence = 'high'
        
        if confidence in ['high', 'medium']:
            updates.append({
                'code': code,
                'name': name,
                'current_type': current_type,
                'new_type': recommended_type,
                'new_strategy': recommended_strategy,
                'reason': reason,
                'confidence': confidence,
                'data_profile': profile
            })
    
    return updates


def update_classification_excel(excel_path: Path, updates: list, dry_run: bool = False) -> int:
    """Update the main classification Excel file"""
    
    # Backup first
    if not dry_run:
        backup_path = excel_path.with_suffix('.xlsx.bak')
        shutil.copy(excel_path, backup_path)
        print(f"Backup created: {backup_path.name}")
    
    df = pd.read_excel(excel_path)
    update_count = 0
    
    for update in updates:
        code = update['code']
        new_type = update['new_type']
        new_strategy = update['new_strategy']
        
        # Find row
        mask = df['Code'] == code
        if mask.any():
            idx = df[mask].index[0]
            
            old_type = df.at[idx, 'KPI_Type']
            old_strategy = df.at[idx, 'Detection_Strategy']
            
            if not dry_run:
                df.at[idx, 'KPI_Type'] = new_type
                df.at[idx, 'Detection_Strategy'] = new_strategy
                
                # Update variance type based on new type
                if new_type == 'physical_stable':
                    df.at[idx, 'Variance_Type'] = 'stable'
                elif new_type == 'floor_saturated':
                    df.at[idx, 'Variance_Type'] = 'floor'
            
            update_count += 1
            
            if update_count <= 30:  # Show first 30
                print(f"  {code}: {old_type}/{old_strategy} -> {new_type}/{new_strategy}")
    
    if update_count > 30:
        print(f"  ... and {update_count - 30} more")
    
    if not dry_run and update_count > 0:
        df.to_excel(excel_path, index=False)
        print(f"Saved {update_count} updates to {excel_path.name}")
    
    return update_count


def update_custom_rules_excel(excel_path: Path, updates: list, dry_run: bool = False) -> int:
    """Update the custom rules Excel file
    
    Add high-confidence updates as custom rules for tracking.
    """
    if not excel_path.exists():
        print(f"Custom rules file not found: {excel_path}")
        return 0
    
    # Backup first
    if not dry_run:
        backup_path = excel_path.with_suffix('.xlsx.bak')
        shutil.copy(excel_path, backup_path)
        print(f"Backup created: {backup_path.name}")
    
    # Read all sheets
    xls = pd.ExcelFile(excel_path)
    sheets = {}
    for sheet_name in xls.sheet_names:
        sheets[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)
    
    # Get the main rules sheet (first sheet or 'Rules')
    rules_sheet_name = 'Rules' if 'Rules' in sheets else xls.sheet_names[0]
    rules_df = sheets[rules_sheet_name]
    
    # Filter for high confidence only for custom rules
    high_conf_updates = [u for u in updates if u['confidence'] == 'high']
    
    new_rules = []
    existing_codes = set(rules_df['Code'].dropna().tolist()) if 'Code' in rules_df.columns else set()
    
    for update in high_conf_updates:
        code = update['code']
        
        # Skip if already exists
        if code in existing_codes:
            continue
        
        new_rule = {
            'Code': code,
            'KPI_Type': update['new_type'],
            'Detection_Strategy': update['new_strategy'],
            'Thresholds': '',
            'Forbidden_Methods': '',
            'Notes': f'Auto-added {datetime.now().strftime("%Y-%m-%d")}: {update["reason"][:50]}',
            'Active': True
        }
        new_rules.append(new_rule)
    
    if new_rules:
        # Append new rules
        new_rules_df = pd.DataFrame(new_rules)
        rules_df = pd.concat([rules_df, new_rules_df], ignore_index=True)
        sheets[rules_sheet_name] = rules_df
        
        if not dry_run:
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                for sheet_name, sheet_df in sheets.items():
                    sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"Added {len(new_rules)} new custom rules")
    
    return len(new_rules)


def main():
    import sys
    
    base_dir = Path(__file__).parent.parent
    
    # Paths
    analysis_path = base_dir / 'reports' / 'misclassified_kpis_analysis.json'
    classification_path = base_dir / 'lib' / 'kpi_xml' / 'kpi_classification_v2.xlsx'
    custom_rules_path = base_dir / 'lib' / 'kpi_xml' / 'kpi_custom_rules.xlsx'
    
    # Check arguments
    dry_run = '--dry-run' in sys.argv
    
    print("=" * 60)
    print("Update KPI Classification Files")
    print("=" * 60)
    print(f"Mode: {'DRY RUN' if dry_run else 'UPDATE'}")
    print(f"Analysis file: {analysis_path}")
    print(f"Classification file: {classification_path}")
    print(f"Custom rules file: {custom_rules_path}")
    
    # Load analysis
    if not analysis_path.exists():
        print(f"\nError: Analysis file not found. Run analyze_misclassified_kpis.py first.")
        return
    
    misclassified = load_misclassified_analysis(analysis_path)
    print(f"\nLoaded {len(misclassified)} misclassified KPIs")
    
    # Filter high confidence updates
    updates = filter_high_confidence_updates(misclassified)
    print(f"Filtered to {len(updates)} high/medium confidence updates")
    
    # Group by confidence
    high_conf = [u for u in updates if u['confidence'] == 'high']
    medium_conf = [u for u in updates if u['confidence'] == 'medium']
    print(f"  High confidence: {len(high_conf)}")
    print(f"  Medium confidence: {len(medium_conf)}")
    
    # Show summary by change type
    print("\nUpdates by change type:")
    from collections import Counter
    changes = Counter(f"{u['current_type']} -> {u['new_type']}" for u in updates)
    for change, count in changes.most_common():
        print(f"  {change}: {count}")
    
    # Update classification file
    print(f"\n{'='*60}")
    print("Updating kpi_classification_v2.xlsx:")
    print("-" * 60)
    
    update_count = update_classification_excel(classification_path, updates, dry_run)
    
    # Update custom rules file (high confidence only)
    print(f"\n{'='*60}")
    print("Updating kpi_custom_rules.xlsx (high confidence only):")
    print("-" * 60)
    
    rules_count = update_custom_rules_excel(custom_rules_path, updates, dry_run)
    
    # Summary
    print(f"\n{'='*60}")
    print("Summary:")
    print(f"  Classification updates: {update_count}")
    print(f"  Custom rules added: {rules_count}")
    
    if dry_run:
        print("\n[DRY RUN] No changes saved. Run without --dry-run to apply.")
    else:
        print("\nChanges saved successfully!")


if __name__ == '__main__':
    main()
