#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Update kpi_classification_v2.xlsx Formula column from XML files

This script reads formulas from PMKPI_SBTS26R2_5G.xml and JUMP_KPIs.xml,
then updates the kpi_classification_v2.xlsx file where:
1. Formulas are truncated (end with '...')
2. SCOUT_NR_xy codes that have empty formulas but can be found as NR_xy in JUMP_KPIs.xml
"""

import xml.etree.ElementTree as ET
import pandas as pd
import re
from pathlib import Path


def parse_xml_formulas(xml_path: Path) -> dict:
    """Parse KPI formulas from XML file
    
    Returns:
        dict: {kpi_id: formula}
    """
    formulas = {}
    
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"XML parse error: {e}")
        # Try adding XML header
        with open(xml_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if not content.strip().startswith('<?xml'):
            content = '<?xml version="1.0"?>\n' + content
        root = ET.fromstring(content)
    
    for kpi_elem in root.findall('.//KPI'):
        kpi_id = kpi_elem.get('id', '')
        formula = kpi_elem.get('formula', '')
        if kpi_id and formula:
            formulas[kpi_id] = formula
    
    print(f"Loaded {len(formulas)} formulas from {xml_path.name}")
    return formulas


def normalize_scout_to_nr(code: str) -> str:
    """Convert SCOUT_NR_xy or SCOUT_NTM_NR_xy to NR_xy format
    
    Examples:
        SCOUT_NR_1234a -> NR_1234a
        SCOUT_NTM_NR_5678b -> NR_5678b
    """
    # Pattern: SCOUT_NR_xy or SCOUT_NTM_NR_xy or SCOUT_*_NR_xy
    pattern = r'^SCOUT_(?:NTM_)?(?:.*_)?NR_(\d{2,4}[a-zA-Z])$'
    match = re.match(pattern, code, re.IGNORECASE)
    if match:
        return f'NR_{match.group(1)}'
    return None


def update_excel_formulas(excel_path: Path, pmkpi_formulas: dict, jump_formulas: dict, dry_run: bool = False):
    """Update Excel file with formulas from XML
    
    Args:
        excel_path: Path to kpi_classification_v2.xlsx
        pmkpi_formulas: dict of {kpi_id: formula} from PMKPI XML
        jump_formulas: dict of {kpi_id: formula} from JUMP_KPIs XML
        dry_run: If True, only report changes without saving
    """
    df = pd.read_excel(excel_path)
    
    if 'Code' not in df.columns or 'Formula' not in df.columns:
        print("Error: Excel file missing required columns (Code, Formula)")
        return
    
    updated_truncated = 0
    updated_scout = 0
    truncated_not_found = 0
    scout_not_found = 0
    
    print("\n" + "=" * 60)
    print("Checking for truncated formulas...")
    print("=" * 60)
    
    for idx, row in df.iterrows():
        code = str(row['Code']) if pd.notna(row['Code']) else ''
        current_formula = str(row['Formula']) if pd.notna(row['Formula']) else ''
        
        # Case 1: Formula is truncated (ends with '...')
        if current_formula.endswith('...'):
            # Try to find in PMKPI XML first
            if code in pmkpi_formulas:
                new_formula = pmkpi_formulas[code]
                if not dry_run:
                    df.at[idx, 'Formula'] = new_formula
                updated_truncated += 1
                print(f"  ✓ {code}: Updated from PMKPI ({len(current_formula)} -> {len(new_formula)} chars)")
            # Try JUMP_KPIs XML
            elif code in jump_formulas:
                new_formula = jump_formulas[code]
                if not dry_run:
                    df.at[idx, 'Formula'] = new_formula
                updated_truncated += 1
                print(f"  ✓ {code}: Updated from JUMP ({len(current_formula)} -> {len(new_formula)} chars)")
            else:
                truncated_not_found += 1
                print(f"  ✗ {code}: Not found in XML (truncated: {current_formula[:50]}...)")
    
    print("\n" + "=" * 60)
    print("Checking for SCOUT_NR codes with empty formulas...")
    print("=" * 60)
    
    for idx, row in df.iterrows():
        code = str(row['Code']) if pd.notna(row['Code']) else ''
        current_formula = str(row['Formula']) if pd.notna(row['Formula']) else ''
        
        # Case 2: SCOUT_NR_xy with empty formula
        if code.upper().startswith('SCOUT') and 'NR_' in code.upper():
            # Check if formula is empty or just whitespace
            if not current_formula or current_formula.strip() == '' or current_formula == 'nan':
                nr_code = normalize_scout_to_nr(code)
                if nr_code:
                    # Try to find NR_xy in JUMP_KPIs
                    if nr_code in jump_formulas:
                        new_formula = jump_formulas[nr_code]
                        if not dry_run:
                            df.at[idx, 'Formula'] = new_formula
                        updated_scout += 1
                        print(f"  ✓ {code} -> {nr_code}: Added formula ({len(new_formula)} chars)")
                    elif nr_code in pmkpi_formulas:
                        new_formula = pmkpi_formulas[nr_code]
                        if not dry_run:
                            df.at[idx, 'Formula'] = new_formula
                        updated_scout += 1
                        print(f"  ✓ {code} -> {nr_code}: Added formula from PMKPI ({len(new_formula)} chars)")
                    else:
                        scout_not_found += 1
                        # Only print first few not found
                        if scout_not_found <= 10:
                            print(f"  ✗ {code} -> {nr_code}: Not found in XML")
                        elif scout_not_found == 11:
                            print(f"  ... (more SCOUT codes not found)")
    
    print("\n" + "=" * 60)
    print(f"Summary:")
    print(f"  Total rows: {len(df)}")
    print(f"  Truncated formulas updated: {updated_truncated}")
    print(f"  Truncated not found: {truncated_not_found}")
    print(f"  SCOUT_NR formulas added: {updated_scout}")
    print(f"  SCOUT_NR not found: {scout_not_found}")
    print(f"  Total updated: {updated_truncated + updated_scout}")
    print("=" * 60)
    
    if not dry_run and (updated_truncated + updated_scout) > 0:
        # Backup original
        backup_path = excel_path.with_suffix('.xlsx.bak')
        import shutil
        shutil.copy(excel_path, backup_path)
        print(f"\nBackup saved to: {backup_path.name}")
        
        # Save updated file
        df.to_excel(excel_path, index=False)
        print(f"Updated file saved: {excel_path.name}")
    elif dry_run:
        print("\n[DRY RUN] No changes saved. Run without --dry-run to update.")


def main():
    import sys
    
    # Paths
    base_dir = Path(__file__).parent.parent / 'lib' / 'kpi_xml'
    excel_path = base_dir / 'kpi_classification_v2.xlsx'
    pmkpi_xml_path = base_dir / 'PMKPI_SBTS26R2_5G.xml'
    jump_xml_path = base_dir / 'JUMP_KPIs.xml'
    
    # Check arguments
    dry_run = '--dry-run' in sys.argv
    
    print("=" * 60)
    print("Update Formulas from XML")
    print("=" * 60)
    print(f"Excel file: {excel_path}")
    print(f"PMKPI XML: {pmkpi_xml_path}")
    print(f"JUMP XML: {jump_xml_path}")
    print(f"Mode: {'DRY RUN' if dry_run else 'UPDATE'}")
    
    if not excel_path.exists():
        print(f"Error: Excel file not found: {excel_path}")
        return
    
    # Parse XMLs
    pmkpi_formulas = {}
    jump_formulas = {}
    
    if pmkpi_xml_path.exists():
        pmkpi_formulas = parse_xml_formulas(pmkpi_xml_path)
    else:
        print(f"Warning: PMKPI XML not found: {pmkpi_xml_path}")
    
    if jump_xml_path.exists():
        jump_formulas = parse_xml_formulas(jump_xml_path)
    else:
        print(f"Warning: JUMP XML not found: {jump_xml_path}")
    
    # Update Excel
    update_excel_formulas(excel_path, pmkpi_formulas, jump_formulas, dry_run=dry_run)


if __name__ == "__main__":
    main()
