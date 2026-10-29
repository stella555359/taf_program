#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
History Management Tool for KPI Detector

Manage historical data records (list, delete, backup, restore).

Usage:
    python manage_history.py --list                      # List all records
    python manage_history.py --delete <timestamp>        # Delete specific record
    python manage_history.py --delete-all                # Delete all records (with confirmation)
    python manage_history.py --backup                    # Create backup
    python manage_history.py --restore <backup_file>     # Restore from backup
    python manage_history.py --stats                     # Show statistics
"""

import sys
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import argparse

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
REPORTS_DIR = PROJECT_ROOT / 'reports'
HISTORY_FILE = REPORTS_DIR / 'kpi_history_records.json'
BACKUP_DIR = REPORTS_DIR / 'backups'


def load_history() -> List[dict]:
    """Load history records from JSON file"""
    if not HISTORY_FILE.exists():
        return []
    
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_history(records: List[dict]):
    """Save history records to JSON file"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)


def list_records(verbose: bool = False):
    """List all history records"""
    records = load_history()
    
    if not records:
        print("No history records found.")
        return
    
    print(f"\nHistory Records ({len(records)} total):")
    print("-" * 80)
    
    for i, record in enumerate(records, 1):
        timestamp = record.get('timestamp', 'Unknown')
        kpi_data = record.get('kpi_data', {})
        n_kpis = len(kpi_data)
        
        # Count consistencies
        consistent = sum(1 for d in kpi_data.values() 
                        if d.get('consistency') in ('Consistent', 'OK'))
        inconsistent = n_kpis - consistent
        
        print(f"{i:3}. Timestamp: {timestamp}")
        print(f"     KPIs: {n_kpis} (Consistent: {consistent}, Inconsistent: {inconsistent})")
        
        if verbose and kpi_data:
            # Show first few KPIs
            print("     Sample KPIs:")
            for j, (code, data) in enumerate(list(kpi_data.items())[:3]):
                consistency = data.get('consistency', 'Unknown')
                print(f"       - {code}: {consistency}")
            if len(kpi_data) > 3:
                print(f"       ... and {len(kpi_data) - 3} more")
        print()


def delete_record(timestamp: str):
    """Delete a specific record by timestamp"""
    records = load_history()
    
    # Find record
    original_count = len(records)
    records = [r for r in records if r.get('timestamp') != timestamp]
    
    if len(records) == original_count:
        print(f"No record found with timestamp: {timestamp}")
        return False
    
    # Create automatic backup before deletion
    create_backup(prefix="pre_delete")
    
    save_history(records)
    print(f"Deleted record: {timestamp}")
    print(f"Remaining records: {len(records)}")
    return True


def delete_all_records(force: bool = False):
    """Delete all records with confirmation"""
    records = load_history()
    
    if not records:
        print("No records to delete.")
        return
    
    if not force:
        print(f"\nWARNING: This will delete ALL {len(records)} history records!")
        confirm = input("Type 'yes' to confirm: ")
        if confirm.lower() != 'yes':
            print("Cancelled.")
            return
    
    # Create backup before deletion
    backup_path = create_backup(prefix="pre_delete_all")
    
    save_history([])
    print(f"\nDeleted all {len(records)} records.")
    print(f"Backup saved to: {backup_path}")


def create_backup(prefix: str = "backup") -> Path:
    """Create a backup of the history file"""
    if not HISTORY_FILE.exists():
        print("No history file to backup.")
        return None
    
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{prefix}_{timestamp}.json"
    backup_path = BACKUP_DIR / backup_name
    
    shutil.copy2(HISTORY_FILE, backup_path)
    print(f"Backup created: {backup_path}")
    return backup_path


def list_backups():
    """List available backups"""
    if not BACKUP_DIR.exists():
        print("No backups found.")
        return
    
    backups = list(BACKUP_DIR.glob("*.json"))
    if not backups:
        print("No backups found.")
        return
    
    print(f"\nAvailable Backups ({len(backups)}):")
    print("-" * 60)
    
    for backup in sorted(backups, reverse=True):
        size = backup.stat().st_size / 1024
        mtime = datetime.fromtimestamp(backup.stat().st_mtime)
        print(f"  {backup.name} ({size:.1f} KB) - {mtime.strftime('%Y-%m-%d %H:%M:%S')}")


def restore_backup(backup_name: str):
    """Restore from a backup file"""
    backup_path = BACKUP_DIR / backup_name
    
    if not backup_path.exists():
        # Try without path
        matches = list(BACKUP_DIR.glob(f"*{backup_name}*"))
        if matches:
            backup_path = matches[0]
        else:
            print(f"Backup not found: {backup_name}")
            list_backups()
            return False
    
    # Create backup of current state
    if HISTORY_FILE.exists():
        create_backup(prefix="pre_restore")
    
    shutil.copy2(backup_path, HISTORY_FILE)
    print(f"Restored from: {backup_path}")
    
    # Show restored records
    records = load_history()
    print(f"Restored {len(records)} records.")
    return True


def show_stats():
    """Show statistics about history data"""
    records = load_history()
    
    if not records:
        print("No history records found.")
        return
    
    print(f"\n{'='*60}")
    print("History Statistics")
    print(f"{'='*60}")
    
    print(f"\nTotal Records: {len(records)}")
    
    # Collect all codes
    all_codes = set()
    consistency_counts = {'Consistent': 0, 'Inconsistent': 0, 'Other': 0}
    
    for record in records:
        kpi_data = record.get('kpi_data', {})
        all_codes.update(kpi_data.keys())
        
        for data in kpi_data.values():
            consistency = data.get('consistency', '')
            if consistency in ('Consistent', 'OK'):
                consistency_counts['Consistent'] += 1
            elif consistency in ('Inconsistent', 'NG'):
                consistency_counts['Inconsistent'] += 1
            else:
                consistency_counts['Other'] += 1
    
    print(f"Unique KPI/Counter Codes: {len(all_codes)}")
    
    print(f"\nConsistency Distribution:")
    total = sum(consistency_counts.values())
    for status, count in consistency_counts.items():
        pct = count / total * 100 if total else 0
        print(f"  {status}: {count} ({pct:.1f}%)")
    
    # Time range
    timestamps = [r.get('timestamp') for r in records if r.get('timestamp')]
    if timestamps:
        print(f"\nTime Range:")
        print(f"  First: {min(timestamps)}")
        print(f"  Last:  {max(timestamps)}")
    
    # File size
    if HISTORY_FILE.exists():
        size_kb = HISTORY_FILE.stat().st_size / 1024
        print(f"\nFile Size: {size_kb:.1f} KB")


def interactive_delete():
    """Interactive mode for deleting records"""
    records = load_history()
    
    if not records:
        print("No records to delete.")
        return
    
    list_records()
    
    print("\nOptions:")
    print("  Enter record number (1-{}) to delete".format(len(records)))
    print("  Enter 'all' to delete all")
    print("  Enter 'q' to quit")
    
    while True:
        choice = input("\nYour choice: ").strip()
        
        if choice.lower() == 'q':
            break
        elif choice.lower() == 'all':
            delete_all_records()
            break
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(records):
                    timestamp = records[idx].get('timestamp')
                    confirm = input(f"Delete record {timestamp}? (y/n): ")
                    if confirm.lower() == 'y':
                        delete_record(timestamp)
                        # Reload
                        records = load_history()
                        if not records:
                            print("All records deleted.")
                            break
                else:
                    print("Invalid number.")
            except ValueError:
                print("Invalid input.")


def main():
    parser = argparse.ArgumentParser(description='Manage KPI history records')
    parser.add_argument('--list', '-l', action='store_true', help='List all records')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--delete', '-d', type=str, metavar='TIMESTAMP', help='Delete specific record')
    parser.add_argument('--delete-all', action='store_true', help='Delete all records')
    parser.add_argument('--backup', '-b', action='store_true', help='Create backup')
    parser.add_argument('--list-backups', action='store_true', help='List available backups')
    parser.add_argument('--restore', '-r', type=str, metavar='FILE', help='Restore from backup')
    parser.add_argument('--stats', '-s', action='store_true', help='Show statistics')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive delete mode')
    
    args = parser.parse_args()
    
    # Default to --list if no arguments
    if len(sys.argv) == 1:
        args.list = True
    
    if args.list:
        list_records(verbose=args.verbose)
    elif args.delete:
        delete_record(args.delete)
    elif args.delete_all:
        delete_all_records()
    elif args.backup:
        create_backup()
    elif args.list_backups:
        list_backups()
    elif args.restore:
        restore_backup(args.restore)
    elif args.stats:
        show_stats()
    elif args.interactive:
        interactive_delete()


if __name__ == "__main__":
    main()
