#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
KPI Custom Rules Manager - Excel-based rule management

This script manages custom detection strategy rules via Excel file.
Users can edit the Excel file directly, and the script will:
1. Load rules from Excel
2. Apply rules to KPI detection
3. Track modification history

Usage:
    python manage_custom_rules.py              # Show current rules
    python manage_custom_rules.py --init       # Initialize Excel template
    python manage_custom_rules.py --apply      # Apply rules from Excel
    python manage_custom_rules.py --export     # Export current rules to Excel
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.datavalidation import DataValidation

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))


STRATEGIES = [
    "STANDARD_SPC",
    "ABS_THRESHOLD",
    "RANGE_CONTEXT",
    "RELATIVE_CHANGE",
    "ABS_DELTA_TREND",
    "QUANTILES",
    "TAIL_AWARE",
    "WINDOW_COUNT",
    "SEMANTIC_RULE",
    "(使用默认)"
]

STRATEGY_DESCRIPTIONS = {
    "STANDARD_SPC": "标准SPC控制图方法 - 适用于大多数KPI",
    "ABS_THRESHOLD": "绝对阈值判定 - 适用于ceiling/floor饱和型(如success ratio=100%)",
    "RANGE_CONTEXT": "区间上下文判定 - 适用于计数型",
    "RELATIVE_CHANGE": "相对变化率判定 - 适用于比例型(非饱和)",
    "ABS_DELTA_TREND": "绝对变化+趋势 - 适用于物理量稳定型(dB/dBm)",
    "QUANTILES": "分位数判定 - 适用于throughput型",
    "TAIL_AWARE": "尾部感知判定 - 适用于latency型",
    "WINDOW_COUNT": "滑窗计数判定 - 适用于低频事件型",
    "SEMANTIC_RULE": "语义规则判定 - 适用于配置型",
}


class CustomRulesManager:
    """Manage custom KPI detection rules via Excel"""
    
    def __init__(self, lib_dir: Path = None):
        self.lib_dir = lib_dir or Path(__file__).parent.parent / 'lib' / 'kpi_xml'
        self.excel_file = self.lib_dir / 'kpi_custom_rules.xlsx'
        self.json_file = self.lib_dir / 'kpi_custom_rules.json'
        self.history_file = self.lib_dir / 'kpi_rules_history.json'
        
        # Styles
        self.header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        self.header_font = Font(bold=True, color="FFFFFF")
        self.edit_fill = PatternFill(start_color="FFFFD7", end_color="FFFFD7", fill_type="solid")  # Light yellow
        self.modified_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")  # Light green
        self.thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
    
    def init_excel(self, codes_data: list = None):
        """Initialize Excel template with optional codes data
        
        Args:
            codes_data: List of dicts with keys: Code, KPI_Name, KPI_Type, Default_Strategy, Current_Strategy
        """
        wb = Workbook()
        
        # Sheet 1: Custom Rules (editable)
        ws_rules = wb.active
        ws_rules.title = "1_Custom_Rules"
        
        headers = ['Code', 'KPI_Name', 'KPI_Type', 'Default_Strategy', 'Override_Strategy', 'Enabled', 'Comment']
        for col, h in enumerate(headers, 1):
            cell = ws_rules.cell(row=1, column=col, value=h)
            cell.fill = self.header_fill
            cell.font = self.header_font
            cell.border = self.thin_border
        
        # Add data validation for Override_Strategy column
        dv = DataValidation(
            type="list",
            formula1=f'"{",".join(STRATEGIES)}"',
            allow_blank=True
        )
        dv.error = "请从下拉列表中选择策略"
        dv.errorTitle = "无效的策略"
        ws_rules.add_data_validation(dv)
        
        # Add data validation for Enabled column
        dv_enabled = DataValidation(
            type="list",
            formula1='"TRUE,FALSE"',
            allow_blank=True
        )
        ws_rules.add_data_validation(dv_enabled)
        
        if codes_data:
            for row_idx, data in enumerate(codes_data, 2):
                ws_rules.cell(row=row_idx, column=1, value=data.get('Code', '')).border = self.thin_border
                ws_rules.cell(row=row_idx, column=2, value=data.get('KPI_Name', '')).border = self.thin_border
                ws_rules.cell(row=row_idx, column=3, value=data.get('KPI_Type', '')).border = self.thin_border
                ws_rules.cell(row=row_idx, column=4, value=data.get('Default_Strategy', '')).border = self.thin_border
                
                # Override_Strategy - editable with yellow background
                cell = ws_rules.cell(row=row_idx, column=5, value=data.get('Override_Strategy', ''))
                cell.fill = self.edit_fill
                cell.border = self.thin_border
                dv.add(cell)
                
                # Enabled - editable
                cell = ws_rules.cell(row=row_idx, column=6, value=data.get('Enabled', 'FALSE'))
                cell.fill = self.edit_fill
                cell.border = self.thin_border
                dv_enabled.add(cell)
                
                ws_rules.cell(row=row_idx, column=7, value=data.get('Comment', '')).border = self.thin_border
        else:
            # Add example row
            example = ['M55124C03001', 'Example KPI', 'config_type', 'SEMANTIC_RULE', 'STANDARD_SPC', 'TRUE', '用户自定义']
            for col, val in enumerate(example, 1):
                cell = ws_rules.cell(row=2, column=col, value=val)
                cell.border = self.thin_border
                if col in [5, 6]:
                    cell.fill = self.edit_fill
        
        # Set column widths
        col_widths = [18, 50, 18, 18, 18, 10, 30]
        for i, w in enumerate(col_widths, 1):
            ws_rules.column_dimensions[chr(64+i)].width = w
        
        ws_rules.freeze_panes = 'A2'
        
        # Sheet 2: Strategy Reference
        ws_ref = wb.create_sheet(title="2_Strategy_Reference")
        ws_ref['A1'] = "检测策略说明"
        ws_ref['A1'].font = Font(bold=True, size=14)
        
        ref_headers = ['Strategy', 'Description', 'Suitable_For']
        for col, h in enumerate(ref_headers, 1):
            cell = ws_ref.cell(row=3, column=col, value=h)
            cell.fill = self.header_fill
            cell.font = self.header_font
            cell.border = self.thin_border
        
        ref_data = [
            ("STANDARD_SPC", "标准SPC控制图方法", "通用，默认方法"),
            ("ABS_THRESHOLD", "绝对阈值判定", "ceiling_saturated (success ratio=100%), floor_saturated"),
            ("RANGE_CONTEXT", "区间上下文判定 [μ±2σ]", "count_type (计数型KPI)"),
            ("RELATIVE_CHANGE", "相对变化率判定", "ratio_type (比例型，非饱和)"),
            ("ABS_DELTA_TREND", "绝对变化+Level Shift检测", "physical_stable (dB/dBm，低方差)"),
            ("QUANTILES", "分位数判定 (P50/P95)", "throughput_type (吞吐量)"),
            ("TAIL_AWARE", "尾部感知判定 (P95/P99)", "latency_type (延迟)"),
            ("WINDOW_COUNT", "滑窗计数判定", "low_frequency (低频事件)"),
            ("SEMANTIC_RULE", "语义规则判定", "config_type (配置/状态型)"),
        ]
        
        for row_idx, (strategy, desc, suitable) in enumerate(ref_data, 4):
            ws_ref.cell(row=row_idx, column=1, value=strategy).border = self.thin_border
            ws_ref.cell(row=row_idx, column=2, value=desc).border = self.thin_border
            ws_ref.cell(row=row_idx, column=3, value=suitable).border = self.thin_border
        
        ws_ref.column_dimensions['A'].width = 20
        ws_ref.column_dimensions['B'].width = 40
        ws_ref.column_dimensions['C'].width = 50
        
        # Sheet 3: Modification History
        ws_history = wb.create_sheet(title="3_Modification_History")
        
        hist_headers = ['Timestamp', 'Code', 'KPI_Name', 'Original_Strategy', 'New_Strategy', 'Modified_By']
        for col, h in enumerate(hist_headers, 1):
            cell = ws_history.cell(row=1, column=col, value=h)
            cell.fill = self.header_fill
            cell.font = self.header_font
            cell.border = self.thin_border
        
        # Load existing history
        history = self._load_history()
        for row_idx, record in enumerate(history, 2):
            ws_history.cell(row=row_idx, column=1, value=record.get('timestamp', '')).border = self.thin_border
            ws_history.cell(row=row_idx, column=2, value=record.get('code', '')).border = self.thin_border
            ws_history.cell(row=row_idx, column=3, value=record.get('kpi_name', '')).border = self.thin_border
            ws_history.cell(row=row_idx, column=4, value=record.get('original_strategy', '')).border = self.thin_border
            ws_history.cell(row=row_idx, column=5, value=record.get('new_strategy', '')).border = self.thin_border
            ws_history.cell(row=row_idx, column=6, value=record.get('modified_by', 'user')).border = self.thin_border
        
        hist_widths = [20, 18, 50, 18, 18, 15]
        for i, w in enumerate(hist_widths, 1):
            ws_history.column_dimensions[chr(64+i)].width = w
        
        ws_history.freeze_panes = 'A2'
        
        # Sheet 4: Instructions
        ws_inst = wb.create_sheet(title="4_使用说明")
        instructions = [
            "KPI 自定义检测规则 - 使用说明",
            "",
            "【如何使用】",
            "1. 在 Sheet '1_Custom_Rules' 中找到要修改的 KPI",
            "2. 在 'Override_Strategy' 列选择新的检测策略（下拉列表）",
            "3. 在 'Enabled' 列设置为 TRUE 启用该规则",
            "4. 保存 Excel 文件",
            "5. 运行命令: python scripts/manage_custom_rules.py --apply",
            "",
            "【注意事项】",
            "- 黄色背景的列是可编辑的",
            "- 绿色背景表示已被用户修改",
            "- 修改历史会自动记录在 Sheet '3_Modification_History'",
            "- 如果 Override_Strategy 为空或 Enabled=FALSE，将使用默认策略",
            "",
            "【策略选择参考】",
            "- 如果 KPI 的 sigma=0 且值为 100%，使用 ABS_THRESHOLD",
            "- 如果 KPI 波动大，使用 STANDARD_SPC",
            "- 如果是吞吐量类型，使用 QUANTILES",
            "- 如果是延迟类型，使用 TAIL_AWARE",
            "- 具体说明见 Sheet '2_Strategy_Reference'",
        ]
        
        for row_idx, text in enumerate(instructions, 1):
            cell = ws_inst.cell(row=row_idx, column=1, value=text)
            if row_idx == 1:
                cell.font = Font(bold=True, size=14)
            elif text.startswith("【"):
                cell.font = Font(bold=True)
        
        ws_inst.column_dimensions['A'].width = 80
        
        wb.save(self.excel_file)
        print(f"Excel template created: {self.excel_file}")
        return self.excel_file
    
    def _load_history(self) -> list:
        """Load modification history from JSON"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_history(self, history: list):
        """Save modification history to JSON"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    
    def _add_history_record(self, code: str, kpi_name: str, original: str, new: str):
        """Add a modification record to history"""
        history = self._load_history()
        history.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'code': code,
            'kpi_name': kpi_name,
            'original_strategy': original,
            'new_strategy': new,
            'modified_by': 'user'
        })
        self._save_history(history)
        return history
    
    def apply_from_excel(self) -> dict:
        """Read Excel and apply rules, updating JSON and tracking changes
        
        Returns:
            dict with 'applied', 'skipped', 'history' counts
        """
        if not self.excel_file.exists():
            print(f"Error: Excel file not found: {self.excel_file}")
            print("Run with --init to create template first")
            return {'applied': 0, 'skipped': 0, 'history': 0}
        
        # Load current JSON rules to detect changes
        current_rules = {}
        if self.json_file.exists():
            try:
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for rule in data.get('rules', []):
                    if rule.get('codes'):
                        for code in rule['codes']:
                            current_rules[code] = rule.get('detection_strategy', '')
            except:
                pass
        
        # Read Excel
        df = pd.read_excel(self.excel_file, sheet_name='1_Custom_Rules')
        
        applied = 0
        skipped = 0
        new_history = []
        
        code_rules = []
        
        for _, row in df.iterrows():
            code = str(row.get('Code', '')).strip()
            if not code:
                continue
            
            override = str(row.get('Override_Strategy', '')).strip()
            enabled = str(row.get('Enabled', 'FALSE')).strip().upper() == 'TRUE'
            
            if not enabled or not override or override == '(使用默认)':
                skipped += 1
                continue
            
            # Check if this is a change
            original = current_rules.get(code, row.get('Default_Strategy', 'STANDARD_SPC'))
            if override != original:
                kpi_name = str(row.get('KPI_Name', '')).strip()
                self._add_history_record(code, kpi_name, original, override)
                new_history.append(code)
            
            code_rules.append(code)
            applied += 1
        
        # Build JSON
        json_data = {
            "_description": "KPI 自定义检测规则 - 由 Excel 自动生成",
            "_last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "_source_file": str(self.excel_file),
            "rules": []
        }
        
        if code_rules:
            # Group by override strategy
            strategy_groups = {}
            for _, row in df.iterrows():
                code = str(row.get('Code', '')).strip()
                if code not in code_rules:
                    continue
                override = str(row.get('Override_Strategy', '')).strip()
                if override not in strategy_groups:
                    strategy_groups[override] = []
                strategy_groups[override].append(code)
            
            for strategy, codes in strategy_groups.items():
                json_data['rules'].append({
                    "_comment": f"从Excel导入的规则 ({len(codes)} codes)",
                    "codes": sorted(codes),
                    "detection_strategy": strategy,
                    "enabled": True
                })
        
        # Save JSON
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        
        # Update Excel history sheet
        self._update_excel_history()
        
        print(f"Rules applied from Excel:")
        print(f"  - Applied: {applied} rules")
        print(f"  - Skipped: {skipped} (disabled or no override)")
        print(f"  - New changes: {len(new_history)}")
        print(f"  - JSON saved: {self.json_file}")
        
        return {'applied': applied, 'skipped': skipped, 'history': len(new_history)}
    
    def _update_excel_history(self):
        """Update history sheet in Excel from JSON history"""
        if not self.excel_file.exists():
            return
        
        history = self._load_history()
        
        wb = load_workbook(self.excel_file)
        if '3_Modification_History' not in wb.sheetnames:
            return
        
        ws = wb['3_Modification_History']
        
        # Clear existing data (keep header)
        for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
            for cell in row:
                cell.value = None
        
        # Write history
        for row_idx, record in enumerate(history[-100:], 2):  # Keep last 100 records
            ws.cell(row=row_idx, column=1, value=record.get('timestamp', '')).border = self.thin_border
            ws.cell(row=row_idx, column=2, value=record.get('code', '')).border = self.thin_border
            ws.cell(row=row_idx, column=3, value=record.get('kpi_name', '')).border = self.thin_border
            ws.cell(row=row_idx, column=4, value=record.get('original_strategy', '')).border = self.thin_border
            cell = ws.cell(row=row_idx, column=5, value=record.get('new_strategy', ''))
            cell.border = self.thin_border
            cell.fill = self.modified_fill
            ws.cell(row=row_idx, column=6, value=record.get('modified_by', 'user')).border = self.thin_border
        
        wb.save(self.excel_file)
    
    def export_to_excel(self, codes_with_info: list = None):
        """Export current classification to Excel for editing
        
        Args:
            codes_with_info: List of dicts with Code, KPI_Name, KPI_Type, Default_Strategy
        """
        # Load existing overrides
        existing_overrides = {}
        if self.excel_file.exists():
            try:
                df = pd.read_excel(self.excel_file, sheet_name='1_Custom_Rules')
                for _, row in df.iterrows():
                    code = str(row.get('Code', '')).strip()
                    override = str(row.get('Override_Strategy', '')).strip()
                    enabled = str(row.get('Enabled', 'FALSE')).strip()
                    comment = str(row.get('Comment', '')).strip()
                    if code and (override or comment):
                        existing_overrides[code] = {
                            'override': override,
                            'enabled': enabled,
                            'comment': comment
                        }
            except:
                pass
        
        # Merge with new data
        if codes_with_info:
            for item in codes_with_info:
                code = item.get('Code', '')
                if code in existing_overrides:
                    item['Override_Strategy'] = existing_overrides[code].get('override', '')
                    item['Enabled'] = existing_overrides[code].get('enabled', 'FALSE')
                    item['Comment'] = existing_overrides[code].get('comment', '')
                else:
                    item['Override_Strategy'] = ''
                    item['Enabled'] = 'FALSE'
                    item['Comment'] = ''
        
        return self.init_excel(codes_with_info)
    
    def show_status(self):
        """Show current rules status"""
        print("=" * 60)
        print("KPI Custom Rules Status")
        print("=" * 60)
        
        print(f"\nExcel file: {self.excel_file}")
        print(f"  Exists: {self.excel_file.exists()}")
        
        print(f"\nJSON file: {self.json_file}")
        print(f"  Exists: {self.json_file.exists()}")
        
        if self.json_file.exists():
            with open(self.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            rules = data.get('rules', [])
            total_codes = sum(len(r.get('codes', [])) for r in rules if r.get('enabled', True))
            print(f"  Active rules: {len([r for r in rules if r.get('enabled', True)])}")
            print(f"  Total codes affected: {total_codes}")
        
        print(f"\nHistory file: {self.history_file}")
        history = self._load_history()
        print(f"  Total modifications: {len(history)}")
        if history:
            print(f"  Last modification: {history[-1].get('timestamp', 'N/A')}")
            print(f"    Code: {history[-1].get('code', 'N/A')}")
            print(f"    Change: {history[-1].get('original_strategy', '')} → {history[-1].get('new_strategy', '')}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='KPI Custom Rules Manager')
    parser.add_argument('--init', action='store_true', help='Initialize Excel template')
    parser.add_argument('--apply', action='store_true', help='Apply rules from Excel to JSON')
    parser.add_argument('--export', action='store_true', help='Export current classification to Excel')
    parser.add_argument('--status', action='store_true', help='Show current status')
    
    args = parser.parse_args()
    
    manager = CustomRulesManager()
    
    if args.init:
        manager.init_excel()
    elif args.apply:
        manager.apply_from_excel()
    elif args.export:
        # Load classification data
        try:
            from kpi_detector.kpi_types import KPITypeClassifier
            classifier = KPITypeClassifier()
            classifier.load()
            
            codes_data = []
            for code, cls in classifier.classifications.items():
                codes_data.append({
                    'Code': code,
                    'KPI_Name': cls.name,
                    'KPI_Type': cls.kpi_type.value,
                    'Default_Strategy': cls.detection_strategy.value,
                })
            
            codes_data.sort(key=lambda x: x['Code'])
            manager.export_to_excel(codes_data)
            print(f"Exported {len(codes_data)} codes to Excel")
        except Exception as e:
            print(f"Error loading classification: {e}")
            manager.init_excel()
    elif args.status:
        manager.show_status()
    else:
        manager.show_status()
        print("\n使用 --help 查看更多选项")


if __name__ == "__main__":
    main()
