#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
KPI Anomaly Detector - Main Entry Point
Run this script to analyze KPI data files

Usage:
    python run_detector.py                    # Interactive mode (select directory then files)
    python run_detector.py <file.xlsx>        # Analyze specific file
    python run_detector.py --no-html          # Skip HTML report generation
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from kpi_detector import KPIAnomalyDetector, PATHS


def get_subdirectories(data_dir: Path) -> list:
    """Get list of subdirectories in data directory"""
    subdirs = [d for d in data_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    return sorted(subdirs, key=lambda x: x.name)


def get_excel_files(directory: Path) -> list:
    """Get list of Excel files in a directory"""
    files = list(directory.glob("*.xlsx"))
    files = [f for f in files if not f.name.startswith('~$') and 'analysis' not in f.name.lower()]
    return sorted(files, key=lambda x: x.name)


def parse_selection(choice: str, max_num: int) -> list:
    """Parse selection string like '1', '1,3,5', '1-5', '1,3-5,7'"""
    if not choice:
        return [1] if max_num >= 1 else []
    
    selected = []
    try:
        parts = choice.replace(' ', '').split(',')
        for part in parts:
            if '-' in part:
                start, end = part.split('-')
                for i in range(int(start), int(end) + 1):
                    if 1 <= i <= max_num:
                        selected.append(i)
            else:
                i = int(part)
                if 1 <= i <= max_num:
                    selected.append(i)
    except ValueError:
        return []
    
    # Remove duplicates while preserving order
    seen = set()
    return [x for x in selected if not (x in seen or seen.add(x))]


def select_directory(data_dir: Path) -> Path:
    """Interactive directory selection"""
    subdirs = get_subdirectories(data_dir)
    
    # Check if there are files in the root data directory
    root_files = get_excel_files(data_dir)
    
    print(f"\n📁 Data Directory: {data_dir}")
    print("-" * 50)
    
    # Option 0: root directory (if has files)
    if root_files:
        print(f"   0. [ROOT] ({len(root_files)} files)")
    
    # List subdirectories
    if subdirs:
        for i, d in enumerate(subdirs, 1):
            file_count = len(get_excel_files(d))
            print(f"   {i}. {d.name}/ ({file_count} files)")
    
    if not subdirs and not root_files:
        print("   No data files or subdirectories found!")
        return None
    
    # Get selection
    prompt = "\nSelect directory (0=root" if root_files else "\nSelect directory ("
    if subdirs:
        prompt += f", 1-{len(subdirs)}" if root_files else f"1-{len(subdirs)}"
    prompt += ", Enter=0): " if root_files else ", Enter=1): "
    
    choice = input(prompt).strip()
    
    if choice == '' or choice == '0':
        if root_files:
            return data_dir
        elif subdirs:
            return subdirs[0]
        return None
    
    try:
        idx = int(choice)
        if 1 <= idx <= len(subdirs):
            return subdirs[idx - 1]
    except ValueError:
        pass
    
    print("Invalid selection")
    return None


def select_files(directory: Path) -> list:
    """Interactive file selection from a directory"""
    files = get_excel_files(directory)
    
    if not files:
        print(f"\n⚠️ No Excel files found in: {directory}")
        return []
    
    print(f"\n📄 Files in {directory.name if directory.name != 'data' else 'ROOT'}:")
    print("-" * 50)
    for i, f in enumerate(files, 1):
        print(f"   {i}. {f.name}")
    
    choice = input(f"\nSelect file(s) (1-{len(files)}, e.g., '1' or '1,3' or '1-3', Enter=1): ").strip()
    
    selected = parse_selection(choice, len(files))
    if not selected:
        print("Invalid selection")
        return []
    
    return [files[i - 1] for i in selected]


def run_analysis(files: list, generate_html: bool = True):
    """Run analysis on selected files"""
    print(f"\n{'='*60}")
    print(f"Will process {len(files)} file(s)")
    print(f"{'='*60}")
    
    for idx, file_path in enumerate(files, 1):
        print(f"\n{'='*60}")
        print(f"[{idx}/{len(files)}] Analyzing: {file_path.name}")
        print(f"{'='*60}")

        try:
            detector = KPIAnomalyDetector(str(file_path))
            detector.run(generate_html=generate_html)
        except ValueError as exc:
            print(f"\nError: {exc}")
    
    print("\n" + "=" * 60)
    print(f"Completed {len(files)} file(s)")
    print(f"Reports saved to: {PATHS['reports']}")
    print(f"History files: {PATHS['reports'] / 'kpi_history_records.json'} ; {PATHS['reports'] / 'kpi_history_records_scout.json'}")
    print("=" * 60)


def main():
    """Main entry point"""
    
    print("=" * 60)
    print("KPI Anomaly Detector")
    print("=" * 60)
    print(f"\nDirectory Structure:")
    print(f"   Data Dir: {PATHS['data']}")
    print(f"   Reports Dir: {PATHS['reports']}")
    print(f"   Scripts Dir: {PATHS['scripts']}")
    print(f"   Docs Dir: {PATHS['docs']}")
    
    # Check command line arguments
    generate_html = True
    target_file = None
    
    args = sys.argv[1:]
    for arg in args:
        if arg == '--no-html':
            generate_html = False
        elif arg.endswith('.xlsx'):
            target_file = arg
    
    # If file specified via command line
    if target_file:
        file_path = Path(target_file)
        if not file_path.exists():
            # Try in data directory
            file_path = PATHS['data'] / target_file
        
        if not file_path.exists():
            print(f"\nError: File not found: {target_file}")
            return
        
        print(f"\nAnalyzing: {file_path.name}")
        try:
            detector = KPIAnomalyDetector(str(file_path))
            detector.run(generate_html=generate_html)
        except ValueError as exc:
            print(f"\nError: {exc}")
            return
        
        print("\n" + "=" * 60)
        print(f"Report saved to: {PATHS['reports']}")
        print(f"History files: {PATHS['reports'] / 'kpi_history_records.json'} ; {PATHS['reports'] / 'kpi_history_records_scout.json'}")
        print("=" * 60)
        return
    
    # Interactive mode: Select directory first
    selected_dir = select_directory(PATHS['data'])
    if not selected_dir:
        return
    
    # Then select files
    selected_files = select_files(selected_dir)
    if not selected_files:
        return
    
    # Run analysis
    run_analysis(selected_files, generate_html)


if __name__ == "__main__":
    main()