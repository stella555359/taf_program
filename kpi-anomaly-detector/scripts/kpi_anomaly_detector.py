# KPI异常检测综合工
# 整合一致性检查（CV分析）和t-test比较，找出可疑的KPI/Counter
# 2026-01-21 - 添加目录结构配置支持

import pandas as pd
import numpy as np
import re
import json
from pathlib import Path
from datetime import datetime
from scipy import stats
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows


# ========== 目录配置 ==========
# 基础目录（脚本所在目录的父目录，即项目根目录
BASE_DIR = Path(__file__).parent.parent

# 子目录配
PATHS = {
    'scripts': BASE_DIR / 'scripts',      # 脚本文件
    'data': BASE_DIR / 'data',            # 原始数据文件 (.xlsx)
    'reports': BASE_DIR / 'reports',      # 报告输出 (Excel报告, HTML趋势
    'docs': BASE_DIR / 'docs',            # 文档和更新日(.md)
}

# 确保目录存在
for path in PATHS.values():
    path.mkdir(parents=True, exist_ok=True)


class KPIAnomalyDetector:
    """KPI异常检测器 - 综合一致性和t-test分析"""
    
    # 颜色定义
    COLORS = {
        'critical': 'FF0000',      # 红色 - 严重异常
        'warning': 'FFA500',       # 橙色 - 警告
        'suspicious': '9370DB',    # 紫色 - 可疑（CV一致但T-Test Fail
        'caution': 'FFFF00',       # 黄色 - 注意
        'normal': '90EE90',        # 浅绿 - 正常
        'header': '4472C4',        # 蓝色 - 表头
        'light_blue': 'ADD8E6',    # 浅蓝
        'grey': 'D3D3D3',          # 灰色
        'improved': '00FF00',      # 亮绿 - 改善
        'worsened': 'FF6B6B',      # 浅红 - 恶化
    }
    
    # 历史记录文件
    HISTORY_FILE = 'kpi_history_records.json'
    
    # 文件名场景匹配模
    # Group 1: 版本(26R2.0115.2)
    # Group 2: 测试配置 (T076.SCF.26R1post5)
    # Group 3: UE数量 (32UEs)
    # Group 4: 场景描述 (httpDL_bigShort)
    FILENAME_PATTERN = r'(\d{2}R\d\.\d{4}\.\d{1,3})_(T\d+\.SCF\.\w+)[._](\d+UEs)[._](.+?)_\d+csv'
    
    def __init__(self, current_file, cv_threshold=5.0, p_value_threshold=0.05):
        """
        初始化检测器
        
        参数:
            current_file: 当前要分析的Excel文件
            cv_threshold: CV阈值，默认5%
            p_value_threshold: p值阈值，默认0.05
        """
        self.current_file = Path(current_file)
        self.cv_threshold = cv_threshold
        self.p_value_threshold = p_value_threshold
        
        self.current_df = None
        self.t076_cols = []
        self.analysis_results = {}
        
        # 历史记录 - 存放在reports目录
        self.history_file_path = PATHS['reports'] / self.HISTORY_FILE
        self.history_records = []
        self.previous_record = None
        
        # 报告输出目录
        self.reports_dir = PATHS['reports']
        
        # 去重信息
        self.dedup_info = {'total_dropped': 0, 'details': []}
        
        # 当前文件的场景标
        self.current_scenario = self._extract_scenario(self.current_file.name)
        
    def _extract_scenario(self, filename):
        """从文件名提取测试场景标识
        
        返回: (UE数量, 场景描述) 元组，如 ('32UEs', 'httpDL_bigShort')
        如果无法匹配，返None
        """
        match = re.search(self.FILENAME_PATTERN, filename, re.IGNORECASE)
        if match:
            ue_count = match.group(3)  # 32UEs
            scenario = match.group(4)  # httpDL_bigShort
            return (ue_count, scenario)
        return None
    
    def _is_same_scenario(self, filename):
        """判断文件是否与当前文件属于同一测试场景"""
        if self.current_scenario is None:
            # 当前文件无法匹配模式，不过滤
            return True
        
        other_scenario = self._extract_scenario(filename)
        if other_scenario is None:
            # 历史文件无法匹配模式，不过滤
            return True
        
        # 比较 UE数量 和 场景描述
        return self.current_scenario == other_scenario
        
    def load_history(self):
        """加载历史记录"""
        if self.history_file_path.exists():
            try:
                with open(self.history_file_path, 'r', encoding='utf-8') as f:
                    all_records = json.load(f)
                
                # 过滤出与当前文件相同测试场景的历史记录
                self.history_records = [
                    r for r in all_records 
                    if self._is_same_scenario(r.get('filename', ''))
                ]
                
                print(f"已加载历史记录: {len(all_records)} 条总记录")
                
                # 显示场景信息
                if self.current_scenario:
                    print(f"  当前场景: {self.current_scenario[0]} + {self.current_scenario[1]}")
                    print(f"  匹配场景的历史记录: {len(self.history_records)} 条")
                
                # 获取最近一条同场景记录用于比较
                if self.history_records:
                    self.previous_record = self.history_records[-1]
                    print(f"  上次同场景分析: {self.previous_record.get('filename', 'N/A')} @ {self.previous_record.get('timestamp', 'N/A')}")
                else:
                    print(f"  无同场景历史记录")
                    
                # 保留所有记录用于保存（不丢失其他场景的数据）
                self._all_history_records = all_records
                
            except Exception as e:
                print(f"警告: 加载历史记录失败 - {e}")
                self.history_records = []
                self._all_history_records = []
        else:
            print("首次运行，无历史记录")
            self.history_records = []
            self._all_history_records = []
            
    def save_history(self, current_result):
        """保存当前结果到历史记录"""
        # 使用所有记录（包括其他场景的）来保存，避免丢失数据
        all_records = getattr(self, '_all_history_records', [])
        all_records.append(current_result)
        
        try:
            with open(self.history_file_path, 'w', encoding='utf-8') as f:
                json.dump(all_records, f, ensure_ascii=False, indent=2)
            
            # 统计同场景记录数
            same_scenario_count = sum(
                1 for r in all_records 
                if self._is_same_scenario(r.get('filename', ''))
            )
            print(f"历史记录已更(总计 {len(all_records)}  同场{same_scenario_count} ")
        except Exception as e:
            print(f"警告: 保存历史记录失败 - {e}")
        
    def load_data(self):
        """加载数据"""
        print(f"\n正在加载当前文件: {self.current_file.name}")
        self.current_df = pd.read_excel(self.current_file)
        print(f"  原始数据形状: {self.current_df.shape}")
        
        # 查找T076列
        self.t076_cols = [col for col in self.current_df.columns if 'T076' in str(col)]
        print(f"  找到 {len(self.t076_cols)} 个T076列")
        
        # 数据去重
        self.deduplicate_data()
        
        # 加载历史记录
        self.load_history()
            
    def deduplicate_data(self):
        """去除重复的Code数据
        
        规则：对于格式为 NR_Ax 或 SCOUT_NR_Ax 的Code（A为2-4位数字，x为字母），
        如果NR_A部分相同但x不同，保留x最大的，删除其他的
        例如：NR_5089a, NR_5089b, NR_5089e -> 保留NR_5089e
        """
        if self.current_df is None or self.current_df.empty:
            return
        
        print("\n========== 数据去重 ==========")
        
        # 正则匹配 NR_数字字母 或 SCOUT_NR_数字字母
        # A为2-4位数字，x为字母
        pattern = r'((?:SCOUT_)?NR_\d{2,4})([a-zA-Z])'
        
        # 找出所有匹配的Code及其分组
        code_groups = {}  # {base: [(code, suffix, idx), ...]}
        
        for idx, row in self.current_df.iterrows():
            code = str(row.get('Code', '')).strip() if pd.notna(row.get('Code')) else ''
            match = re.search(pattern, code, re.IGNORECASE)
            if match:
                base = match.group(1).upper()  # NR_5089 或 SCOUT_NR_5089
                suffix = match.group(2).upper()  # A, B, E 等
                if base not in code_groups:
                    code_groups[base] = []
                code_groups[base].append((code, suffix, idx))
        
        # 找出需要删除的行
        rows_to_drop = []
        dedup_details = []  # 记录去重详情
        
        for base, items in code_groups.items():
            if len(items) > 1:
                # 按suffix排序（字母顺序），保留最大的
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
            print(f"  发现 {len(dedup_details)} 组重复数据，删除 {len(rows_to_drop)} 行")
            for detail in dedup_details:
                print(f"    保留: {detail['kept']}, 删除: {detail['dropped']}")
            
            self.current_df = self.current_df.drop(rows_to_drop).reset_index(drop=True)
            print(f"  去重后数据形状: {self.current_df.shape}")
        else:
            print("  未发现重复数据")
        
        # 保存去重信息供报告使用
        self.dedup_info = {
            'total_dropped': len(rows_to_drop),
            'details': dedup_details
        }
    
    def classify_code(self, code):
        """分类Code为Counter或KPI类型"""
        code = str(code).strip()
        if re.match(r'^M\d{5}C\d{1,5}$', code, re.IGNORECASE):
            return 'Counter'
        elif re.search(r'NR', code, re.IGNORECASE):
            return 'KPI'
        else:
            return 'Other'
    
    def _calculate_severity_from_history(self, code, current_values, history_records):
        """基于历史数据计算Severity等级
        
        Severity判断逻辑（基于历史统计）:
        - Normal: 当前均值落在历史均±2σ 
        - Suspicious: 超出 ±2σ 但未超过 ±3σ，或触发Shewhart警告规则
        - Regression: 超出 ±3σ 或触发Shewhart严重规则（趋势、连续偏移等
        - NoHistory: 无足够历史数据（<2条记录）
        
        Returns:
            dict: {
                'severity': str,  # Normal / Suspicious / Regression / NoHistory
                'z_score': float or None,
                'anomaly_count': int,  # 超出±2σ的数据点
                'anomaly_ratio': float,
                'trend_direction': str or None,  # 'increasing' / 'decreasing' / None
                'hist_mean': float or None,
                'hist_std': float or None,
                'current_mean': float or None,
                'sigma_level': float or None,  # 当前偏离的σ倍数
                'judgment_reasons': list,
                'shewhart': dict  # Shewhart控制图分析结
            }
        """
        result = {
            'severity': 'NoHistory',
            'z_score': None,
            'anomaly_count': 0,
            'anomaly_ratio': 0.0,
            'trend_direction': None,
            'hist_mean': None,
            'hist_std': None,
            'current_mean': None,
            'sigma_level': None,
            'judgment_reasons': [],
            'shewhart': {}
        }
        
        if not current_values:
            result['judgment_reasons'].append('无当前数据')
            return result
        
        if not history_records:
            result['judgment_reasons'].append('无历史数据')
            return result
        
        # 收集历史数据（每条记录的均值）
        hist_all_values = []  # 所有历史数据点
        hist_means = []  # 每次测试的均值（用于趋势检测）
        hist_cvs = []
        
        for record in history_records:
            kpi_data = record.get('kpi_data', {})
            if code in kpi_data:
                raw_data = kpi_data[code].get('raw_data', '')
                cv_value = kpi_data[code].get('cv', None)
                mean_value = kpi_data[code].get('mean', None)
                if raw_data:
                    try:
                        values = [float(x) for x in raw_data.split(',') if x.strip()]
                        hist_all_values.extend(values)
                        if values:
                            hist_means.append(np.mean(values))
                    except:
                        pass
                if mean_value is not None:
                    if not hist_means or hist_means[-1] != mean_value:
                        # 避免重复添加
                        pass
                if cv_value is not None:
                    hist_cvs.append(cv_value)
        
        if len(hist_means) < 2:
            result['judgment_reasons'].append('历史数据不足(<2次)')
            return result
        
        # 计算历史统计
        hist_mean = np.mean(hist_all_values)
        hist_std = np.std(hist_all_values)
        
        result['hist_mean'] = float(hist_mean)
        result['hist_std'] = float(hist_std)
        
        # 计算当前均值
        current_mean = np.mean(current_values)
        result['current_mean'] = float(current_mean)
        
        # 计算Z-Score和σ倍数
        if hist_std > 0:
            z_score = (current_mean - hist_mean) / hist_std
            result['z_score'] = float(z_score)
            result['sigma_level'] = float(abs(z_score))
        else:
            # 历史标准差为0，说明历史数据完全一致
            if current_mean == hist_mean:
                result['z_score'] = 0.0
                result['sigma_level'] = 0.0
            else:
                result['z_score'] = float('inf') if current_mean > hist_mean else float('-inf')
                result['sigma_level'] = float('inf')
        
        # 异常点检测（超出历史±2σ的点
        if hist_std > 0:
            upper_2sigma = hist_mean + 2 * hist_std
            lower_2sigma = hist_mean - 2 * hist_std
            anomaly_count = sum(1 for v in current_values if v > upper_2sigma or v < lower_2sigma)
            result['anomaly_count'] = anomaly_count
            result['anomaly_ratio'] = float(anomaly_count / len(current_values))
        
        # 趋势检测（检查最近几次是否有连续同方向偏移）
        if len(hist_means) >= 3:
            # 添加当前均
            all_means = hist_means + [current_mean]
            # 检查最次（或所有）的趋
            recent_means = all_means[-min(4, len(all_means)):]
            if len(recent_means) >= 3:
                diffs = [recent_means[i+1] - recent_means[i] for i in range(len(recent_means)-1)]
                if all(d > 0 for d in diffs):
                    result['trend_direction'] = 'increasing'
                elif all(d < 0 for d in diffs):
                    result['trend_direction'] = 'decreasing'
        
        # ===== 应用Shewhart控制图规=====
        shewhart_result = self._apply_shewhart_rules(code, current_mean, history_records)
        result['shewhart'] = shewhart_result
        
        # 判断Severity（综合level和Shewhart规则
        sigma_level = result.get('sigma_level', 0) or 0
        shewhart_violations = shewhart_result.get('violations', [])
        
        # 基础判断（基于level
        if sigma_level <= 2:
            result['severity'] = 'Normal'
            result['judgment_reasons'].append(f'在σ(σ={sigma_level:.2f})')
        elif sigma_level <= 3:
            result['severity'] = 'Suspicious'
            result['judgment_reasons'].append(f'超出±2σ但在±3σ(σ={sigma_level:.2f})')
        else:
            result['severity'] = 'Regression'
            result['judgment_reasons'].append(f'超出±3σ (σ={sigma_level:.2f})')
        
        # Shewhart规则升级判断
        if shewhart_violations:
            # 严重规则（升级为Regression
            severe_rules = ['Rule1', 'Rule3', 'Rule4']  # 超出控制限、趋势、连续偏
            warning_rules = ['Rule2']  # 警告规则
            
            has_severe = any(any(r in v for r in severe_rules) for v in shewhart_violations)
            has_warning = any(any(r in v for r in warning_rules) for v in shewhart_violations)
            
            if has_severe and result['severity'] != 'Regression':
                result['severity'] = 'Regression'
            elif has_warning and result['severity'] == 'Normal':
                result['severity'] = 'Suspicious'
            
            # 添加Shewhart违规到原
            for v in shewhart_violations:
                result['judgment_reasons'].append(f'SPC:{v}')
        
        # 添加Zone信息
        if shewhart_result.get('zone'):
            zone = shewhart_result['zone']
            if zone == 'OutOfControl':
                result['judgment_reasons'].append('Zone:失控')
            elif zone == 'A':
                result['judgment_reasons'].append('Zone:A(警告')
        
        # 趋势性偏移升级为Regression（如果Shewhart规则没有检测到
        if result['trend_direction'] and 'Rule3' not in str(shewhart_violations):
            if result['severity'] != 'Regression':
                result['severity'] = 'Regression'
                result['judgment_reasons'].append(f"趋势性偏{result['trend_direction']})")
        
        # 异常点比例过高时升级
        if result['anomaly_ratio'] > 0.5 and result['severity'] == 'Normal':
            result['severity'] = 'Suspicious'
            result['judgment_reasons'].append(f"异常点过{result['anomaly_count']}{len(current_values)})")
        
        return result
    
    def _apply_shewhart_rules(self, code, current_mean, history_records):
        """应用Shewhart控制图规则（适合小样本，基于批次均值）
        
        控制图类型：X-bar Chart（基于每批次的均值）
        - 每次测试的均值作为控制图上的一个点
        - 使用历史批次均值计算控制限
        
        简化规则（适合历史批次数≥2的情况）:
        - Rule 1: 单点超出±3σ (UCL/LCL)
        - Rule 2: 连续3点超出σ（同侧）
        - Rule 3: 连续4点单调递增/递减
        - Rule 4: 连续3点在CL同一
        - Zone Rule: 检查点在各Zone的分
        
        Returns:
            dict: {
                'violations': list,  # 违反的规则列
                'control_limits': dict,  # 控制{UCL, UWL, CL, LWL, LCL}
                'zone': str,  # 当前点所在Zone (A/B/C)
                'batch_means': list,  # 历史批次均值序
                'chart_data': dict,  # 用于绘制控制图的数据
            }
        """
        result = {
            'violations': [],
            'control_limits': {},
            'zone': None,
            'batch_means': [],
            'chart_data': {}
        }
        
        if current_mean is None:
            return result
        
        # 收集历史批次均
        batch_means = []
        batch_timestamps = []
        
        for record in history_records:
            kpi_data = record.get('kpi_data', {})
            if code in kpi_data:
                raw_data = kpi_data[code].get('raw_data', '')
                if raw_data:
                    try:
                        values = [float(x) for x in raw_data.split(',') if x.strip()]
                        if values:
                            batch_means.append(np.mean(values))
                            batch_timestamps.append(record.get('timestamp', ''))
                    except:
                        pass
        
        if len(batch_means) < 2:
            # 历史数据不足，无法建立控制限
            return result
        
        result['batch_means'] = batch_means.copy()
        
        # 计算控制限（基于历史批次均值）
        # 使用所有历史批次均值计算中心线和标准差
        cl = np.mean(batch_means)  # Center Line
        
        # 对于X-bar chart，使用批次均值的标准差
        # 当样本量小时，使用样本标准差
        sigma = np.std(batch_means, ddof=1) if len(batch_means) > 1 else 0
        
        # 如果sigma为0（所有历史均值相同），使用一个小的默认值避免除零
        if sigma == 0:
            # 检查当前值是否与历史不同
            if current_mean != cl:
                result['violations'].append('历史数据完全一致但当前值偏离')
                result['zone'] = 'OutOfControl'
            else:
                result['zone'] = 'C'
            result['control_limits'] = {'UCL': cl, 'UWL': cl, 'CL': cl, 'LWL': cl, 'LCL': cl}
            return result
        
        # 控制限
        ucl = cl + 3 * sigma  # Upper Control Limit
        uwl = cl + 2 * sigma  # Upper Warning Limit
        lwl = cl - 2 * sigma  # Lower Warning Limit
        lcl = cl - 3 * sigma  # Lower Control Limit
        
        result['control_limits'] = {
            'UCL': float(ucl),
            'UWL': float(uwl),
            'CL': float(cl),
            'LWL': float(lwl),
            'LCL': float(lcl),
            'sigma': float(sigma)
        }
        
        # 添加当前均值到序列末尾
        all_means = batch_means + [current_mean]
        
        # ===== Rule 1: 单点超出±3σ =====
        if current_mean > ucl:
            result['violations'].append(f'Rule1: 超出UCL(+3σ)')
        elif current_mean < lcl:
            result['violations'].append(f'Rule1: 超出LCL(-3σ)')
        
        # ===== Rule 2: 连续3点超出σ（同侧）=====
        if len(all_means) >= 3:
            last_3 = all_means[-3:]
            # 检查上
            above_uwl = sum(1 for m in last_3 if m > uwl)
            if above_uwl >= 3:
                result['violations'].append(f'Rule2: 连续3点超2σ')
            # 检查下
            below_lwl = sum(1 for m in last_3 if m < lwl)
            if below_lwl >= 3:
                result['violations'].append(f'Rule2: 连续3点超2σ')
        
        # ===== Rule 3: 连续4点单调递增/递减 =====
        if len(all_means) >= 4:
            last_4 = all_means[-4:]
            diffs = [last_4[i+1] - last_4[i] for i in range(len(last_4)-1)]
            if all(d > 0 for d in diffs):
                result['violations'].append(f'Rule3: 连续4点递增趋势')
            elif all(d < 0 for d in diffs):
                result['violations'].append(f'Rule3: 连续4点递减趋势')
        
        # ===== Rule 4: 连续3点在中心线同一=====
        if len(all_means) >= 3:
            last_3 = all_means[-3:]
            above_cl = sum(1 for m in last_3 if m > cl)
            below_cl = sum(1 for m in last_3 if m < cl)
            if above_cl == 3:
                result['violations'].append(f'Rule4: 连续3点在CL上方')
            elif below_cl == 3:
                result['violations'].append(f'Rule4: 连续3点在CL下方')
        
        # ===== 确定当前点所在Zone =====
        # Zone A: ±2σ ~ ±3σ (Warning Zone)
        # Zone B: ±1σ ~ ±2σ  
        # Zone C: 0 ~ ±1σ (Normal Zone)
        z_score = (current_mean - cl) / sigma
        abs_z = abs(z_score)
        
        if abs_z > 3:
            result['zone'] = 'OutOfControl'
        elif abs_z > 2:
            result['zone'] = 'A'  # Warning
        elif abs_z > 1:
            result['zone'] = 'B'
        else:
            result['zone'] = 'C'  # Normal
        
        # 构建图表数据
        result['chart_data'] = {
            'batch_labels': [f'Test{i+1}' for i in range(len(batch_means))] + ['Current'],
            'batch_values': all_means,
            'timestamps': batch_timestamps + ['Current'],
            'ucl': ucl,
            'uwl': uwl,
            'cl': cl,
            'lwl': lwl,
            'lcl': lcl,
            'zones': self._calculate_zones_for_series(all_means, cl, sigma)
        }
        
        return result
    
    def _calculate_zones_for_series(self, values, cl, sigma):
        """计算序列中每个点所在的Zone"""
        zones = []
        for v in values:
            z = abs((v - cl) / sigma) if sigma > 0 else 0
            if z > 3:
                zones.append('OutOfControl')
            elif z > 2:
                zones.append('A')
            elif z > 1:
                zones.append('B')
            else:
                zones.append('C')
        return zones
    
    def _generate_sparkline(self, raw_data):
        """生成文本形式的Sparkline（使用Unicode柱状图字符）"""
        if not raw_data:
            return ''
        
        try:
            values = [float(x) for x in raw_data.split(',') if x.strip()]
            if not values:
                return ''
            
            # Unicode柱状图字符（从低到高
            bars = '▁▂▃▄▅▆▇█'
            
            min_val = min(values)
            max_val = max(values)
            
            if max_val == min_val:
                # 所有值相同，使用中间高度
                return bars[4] * len(values)
            
            # 归一化到0-7范围
            sparkline = ''
            for v in values:
                normalized = (v - min_val) / (max_val - min_val)
                bar_idx = int(normalized * 7)
                bar_idx = min(7, max(0, bar_idx))
                sparkline += bars[bar_idx]
            
            return sparkline
        except:
            return ''
    
    def analyze_consistency(self):
        """分析一致性(CV分析)"""
        print("\n========== 一致性分析 ==========")
        
        if not self.t076_cols:
            print("错误: 未找到T076列")
            return
        
        data_cols = self.current_df[self.t076_cols]
        
        results = []
        for idx, row in self.current_df.iterrows():
            code = str(row.get('Code', '')).strip() if pd.notna(row.get('Code')) else ''
            kpi_name = str(row.get('KPI Name', '')).strip() if 'KPI Name' in row.index and pd.notna(row.get('KPI Name')) else ''
            
            row_data = data_cols.iloc[idx]
            non_null = row_data.dropna()
            
            # 初始化Trimmed
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
            elif len(non_null) < len(self.t076_cols):
                # 部分空值
                if len(non_null.unique()) == 1 and (non_null.iloc[0] == 0 or non_null.iloc[0] == 100):
                    status = '一致'
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
                    status = '一致'
                    cv = 0
                elif abs(mean_val) < 0.001:
                    # 极小值，使用绝对差异
                    if (non_null.max() - non_null.min()) < 0.001:
                        status = '一致'
                        cv = 0
                    else:
                        status = '不一致'
                        cv = np.nan
                else:
                    cv = (std_val / mean_val) * 100
                    status = '一致' if cv < self.cv_threshold else '不一致'
                
                # 如果数据>=5，计算去掉最大最小值后的结果
                if len(non_null) >= 5:
                    use_trimmed = True
                    sorted_vals = non_null.sort_values()
                    trimmed_vals = sorted_vals.iloc[1:-1]  # 去掉最大最小值
                    trimmed_mean = trimmed_vals.mean()
                    trimmed_std = trimmed_vals.std(ddof=0)
                    
                    if trimmed_vals.nunique() == 1:
                        trimmed_cv = 0
                        trimmed_status = '一致'
                    elif abs(trimmed_mean) < 0.001:
                        if (trimmed_vals.max() - trimmed_vals.min()) < 0.001:
                            trimmed_cv = 0
                            trimmed_status = '一致'
                        else:
                            trimmed_cv = np.nan
                            trimmed_status = '不一致'
                    else:
                        trimmed_cv = (trimmed_std / trimmed_mean) * 100
                        trimmed_status = '一致' if trimmed_cv < self.cv_threshold else '不一致'
            
            results.append({
                'Code': code,
                'KPI Name': kpi_name,
                'Type': self.classify_code(code),
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
        
        # 统计
        consistency_df = self.analysis_results['consistency']
        print(f"  一致: {(consistency_df['Consistency'] == '一致').sum()}")
        print(f"  不一致: {(consistency_df['Consistency'] == '不一致').sum()}")
        print(f"  partial NULL: {(consistency_df['Consistency'] == 'partial NULL').sum()}")
        print(f"  NULL: {(consistency_df['Consistency'] == 'NULL').sum()}")
        
    def analyze_ttest_with_history(self):
        """分析t-test(与历史记录比较)"""
        if not self.previous_record:
            print("\n无历史记录，跳过t-test分析")
            return
        
        print("\n========== T-Test分析（与历史比较）==========")
        print(f"  比较文件: {self.previous_record.get('filename', 'N/A')}")
        
        # 从历史记录获取数据
        prev_data = self.previous_record.get('kpi_data', {})
        
        if not prev_data:
            print("  警告: 历史记录中无KPI数据")
            return
        
        results = []
        consistency_df = self.analysis_results.get('consistency', pd.DataFrame())
        
        for _, row in consistency_df.iterrows():
            code = row['Code']
            if not code or code not in prev_data:
                continue
            
            # 当前数据
            current_raw = row['RawData']
            if not current_raw:
                continue
            current_values = [float(x) for x in current_raw.split(',') if x.strip()]
            
            # 历史数据
            prev_raw = prev_data[code].get('raw_data', '')
            if not prev_raw:
                continue
            prev_values = [float(x) for x in prev_raw.split(',') if x.strip()]
            
            # 执行t-test
            if len(current_values) >= 2 and len(prev_values) >= 2:
                current_mean = np.mean(current_values)
                prev_mean = np.mean(prev_values)
                
                # 检查是否全或全相同
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
                
                # 判断结果
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
            print(f"  比较的KPI {len(ttest_df)}")
            print(f"  Pass: {(ttest_df['TTest_Result'] == 'Pass').sum()}")
            print(f"  Fail: {(ttest_df['TTest_Result'] == 'Fail').sum()}")
    
    def analyze_all_codes_with_history(self):
        """分析所有Code并基于历史数据判断Severity
        
        Severity判断逻辑(主要基于历史统计,T-Test仅作参考):
        - Normal: 当前均值落在历史均值正负2sigma内
        - Suspicious: 超出正负2sigma但未超过正负3sigma
        - Regression: 超出正负3sigma或出现趋势性偏移
        - NoHistory: 无足够历史数据(<2条记录)
        """
        print("\n========== 分析所有Code（基于历史统计）==========")
        
        all_codes_analysis = []
        
        consistency_df = self.analysis_results.get('consistency', pd.DataFrame())
        ttest_df = self.analysis_results.get('ttest', pd.DataFrame())
        
        if consistency_df.empty:
            print("  错误: 无一致性分析数据")
            return
        
        # 获取历史数据
        prev_data = {}
        if self.previous_record:
            prev_data = self.previous_record.get('kpi_data', {})
        
        # 遍历所有Code
        for _, row in consistency_df.iterrows():
            code = row['Code']
            if not code:
                continue
            
            # 基础信息
            kpi_name = row['KPI Name']
            code_type = row['Type']
            cv_value = row['CV(%)']
            consistency = row['Consistency']
            raw_data = row['RawData']
            trimmed_consistency = row.get('Trimmed_Consistency', '')
            data_count = row.get('DataCount', 0)
            
            # 获取T-Test结果（仅作参考）
            ttest_result = 'N/A'
            p_value = np.nan
            diff_pct = np.nan
            if not ttest_df.empty:
                ttest_row = ttest_df[ttest_df['Code'] == code]
                if not ttest_row.empty:
                    ttest_result = ttest_row['TTest_Result'].iloc[0]
                    p_value = ttest_row['P_Value'].iloc[0]
                    diff_pct = ttest_row['Diff(%)'].iloc[0]
            
            # 获取历史数据
            history_data = ''
            history_consistency = 'N/A'
            if code in prev_data:
                history_data = prev_data[code].get('raw_data', '')
                history_consistency = prev_data[code].get('consistency', 'N/A')
            
            # 解析当前数据
            current_values = []
            if raw_data:
                try:
                    current_values = [float(x) for x in raw_data.split(',') if x.strip()]
                except:
                    pass
            
            # 基于历史数据计算Severity
            hist_result = self._calculate_severity_from_history(code, current_values, self.history_records)
            
            # 最终Severity（基于历史统计）
            severity = hist_result['severity']
            
            # 获取Shewhart控制图数
            shewhart_data = hist_result.get('shewhart', {})
            shewhart_zone = shewhart_data.get('zone', '')
            shewhart_violations = shewhart_data.get('violations', [])
            control_limits = shewhart_data.get('control_limits', {})
            
            # 构建分析原因
            analysis_reasons = []
            
            # 添加一致性信息（作为参考）
            if consistency == '不一致':
                if data_count >= 5 and trimmed_consistency == '一致':
                    analysis_reasons.append('CV不一致,trimmed后一致')
                else:
                    analysis_reasons.append('CV不一致')
            elif consistency == 'partial NULL':
                analysis_reasons.append('部分空值')
            
            # 添加历史分析原因
            if hist_result['judgment_reasons']:
                analysis_reasons.extend(hist_result['judgment_reasons'])
            
            # T-Test结果作为参考
            if ttest_result == 'Fail':
                analysis_reasons.append(f'T-Test Fail(参考)')
            
            all_codes_analysis.append({
                'Code': code,
                'KPI Name': kpi_name,
                'Type': code_type,
                'Severity': severity,
                'Reasons': '; '.join(analysis_reasons) if analysis_reasons else '正常',
                'CV(%)': cv_value,
                'Consistency': consistency,
                'Trimmed_Consistency': trimmed_consistency,
                'TTest_Result': ttest_result,
                'P_Value': p_value,
                'Diff(%)': diff_pct,
                'Z_Score': hist_result['z_score'],
                'Sigma_Level': hist_result['sigma_level'],
                'Anomaly_Count': hist_result['anomaly_count'],
                'Anomaly_Ratio(%)': hist_result['anomaly_ratio'] * 100 if hist_result['anomaly_ratio'] else 0,
                'Trend': hist_result['trend_direction'] or '',
                'Hist_Mean': hist_result['hist_mean'],
                'Hist_Std': hist_result['hist_std'],
                'Current_Mean': hist_result['current_mean'],
                # Shewhart控制图相关字
                'SPC_Zone': shewhart_zone,
                'SPC_Violations': '; '.join(shewhart_violations) if shewhart_violations else '',
                'SPC_UCL': control_limits.get('UCL'),
                'SPC_LCL': control_limits.get('LCL'),
                'SPC_CL': control_limits.get('CL'),
                'Current_Data': raw_data,
                'History_Data': history_data,
                # 保存完整的Shewhart chart_data用于HTML可视
                '_shewhart_chart': shewhart_data.get('chart_data', {})
            })
        
        # 创建DataFrame并排
        all_codes_df = pd.DataFrame(all_codes_analysis)
        if not all_codes_df.empty:
            # 按Severity排序
            severity_order = {'Regression': 0, 'Suspicious': 1, 'NoHistory': 2, 'Normal': 3}
            all_codes_df['_severity_order'] = all_codes_df['Severity'].map(severity_order)
            all_codes_df = all_codes_df.sort_values(['_severity_order', 'Sigma_Level'], ascending=[True, False])
            all_codes_df = all_codes_df.drop(columns=['_severity_order'])
        
        self.analysis_results['all_codes'] = all_codes_df
        
        # 统计
        print(f"  总Code {len(all_codes_df)}")
        print(f"  Regression (性能退: {(all_codes_df['Severity'] == 'Regression').sum()}")
        print(f"  Suspicious (可疑): {(all_codes_df['Severity'] == 'Suspicious').sum()}")
        print(f"  Normal (正常): {(all_codes_df['Severity'] == 'Normal').sum()}")
        print(f"  NoHistory (无历: {(all_codes_df['Severity'] == 'NoHistory').sum()}")
        
        # 兼容旧的suspicious接口（筛选出非Normal的）
        suspicious_df = all_codes_df[all_codes_df['Severity'] != 'Normal'].copy()
        self.analysis_results['suspicious'] = suspicious_df
        
        print(f"\n  需关注的Code: {len(suspicious_df)}")
    
    # 保留旧方法名的兼容性
    def identify_suspicious_kpis(self):
        """兼容旧接口,调用新的分析方法"""
        self.analyze_all_codes_with_history()
    
    def build_current_record(self):
        """构建当前结果记录用于保存到历史"""
        consistency_df = self.analysis_results.get('consistency', pd.DataFrame())
        suspicious_df = self.analysis_results.get('suspicious', pd.DataFrame())
        
        # KPI数据字典（用于下次t-test比较
        kpi_data = {}
        for _, row in consistency_df.iterrows():
            code = row['Code']
            if code:
                kpi_data[code] = {
                    'kpi_name': row['KPI Name'],
                    'type': row['Type'],
                    'mean': float(row['Mean']) if pd.notna(row['Mean']) else None,
                    'cv': float(row['CV(%)']) if pd.notna(row['CV(%)']) else None,
                    'consistency': row['Consistency'],
                    'raw_data': row['RawData']
                }
        
        # 获取all_codes分析结果（包含Severity
        all_codes_df = self.analysis_results.get('all_codes', pd.DataFrame())
        
        # 统计摘要
        kpi_df = consistency_df[consistency_df['Type'] == 'KPI']
        counter_df = consistency_df[consistency_df['Type'] == 'Counter']
        
        stats_summary = {
            'total_codes': len(consistency_df),
            'consistent': int((consistency_df['Consistency'] == '一致').sum()),
            'inconsistent': int((consistency_df['Consistency'] == '不一致').sum()),
            'inconsistent_kpi': int((kpi_df['Consistency'] == '不一致').sum()),
            'inconsistent_counter': int((counter_df['Consistency'] == '不一致').sum()),
            # Trimmed后仍然不一致的统计（数据点>=5且trimmed后仍不一致）
            'inconsistent_kpi_trimmed': int(((kpi_df['Consistency'] == '不一致') & 
                                             ((kpi_df['DataCount'] < 5) | (kpi_df['Trimmed_Consistency'] == '不一致'))).sum()),
            'inconsistent_counter_trimmed': int(((counter_df['Consistency'] == '不一致') & 
                                                  ((counter_df['DataCount'] < 5) | (counter_df['Trimmed_Consistency'] == '不一致'))).sum()),
            'partial_null': int((consistency_df['Consistency'] == 'partial NULL').sum()),
            'null': int((consistency_df['Consistency'] == 'NULL').sum()),
            # 新的Severity统计（基于历史sigma判断）
            'severity_regression': int((all_codes_df['Severity'] == 'Regression').sum()) if not all_codes_df.empty else 0,
            'severity_suspicious': int((all_codes_df['Severity'] == 'Suspicious').sum()) if not all_codes_df.empty else 0,
            'severity_normal': int((all_codes_df['Severity'] == 'Normal').sum()) if not all_codes_df.empty else 0,
            'severity_nohistory': int((all_codes_df['Severity'] == 'NoHistory').sum()) if not all_codes_df.empty else 0,
        }
        
        # 不一致Code列表（考虑trimmed数据）
        inconsistent_codes = []
        for _, row in consistency_df.iterrows():
            if row['Consistency'] == '不一致':
                # 如果数据>=5且trimmed后一致，则跳过
                if row['DataCount'] >= 5 and row['Trimmed_Consistency'] == '一致':
                    continue
                inconsistent_codes.append(row['Code'])
        
        return {
            'filename': self.current_file.name,
            'filepath': str(self.current_file),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'stats': stats_summary,
            'inconsistent_codes': inconsistent_codes,
            'kpi_data': kpi_data
        }
    
    def compare_with_history(self):
        """与历史比较,生成变化分析"""
        if not self.previous_record:
            return None
        
        current_stats = self.analysis_results.get('consistency', pd.DataFrame())
        prev_stats = self.previous_record.get('stats', {})
        prev_inconsistent = set(self.previous_record.get('inconsistent_codes', []))
        
        # 获取当前不一致的Code（考虑trimmed数据）
        # 如果数据>=5且trimmed后一致，则不视为不一致
        current_inconsistent = set()
        for _, row in current_stats.iterrows():
            if row['Consistency'] == '不一致':
                # 如果数据>=5且trimmed后一致，则跳过
                if row['DataCount'] >= 5 and row['Trimmed_Consistency'] == '一致':
                    continue
                current_inconsistent.add(row['Code'])
        
        # 计算变化
        new_inconsistent = current_inconsistent - prev_inconsistent  # 新增不一致
        fixed = prev_inconsistent - current_inconsistent  # 已修复
        persistent = current_inconsistent & prev_inconsistent  # 持续不一致
        
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
        
        print("\n========== 与历史比==========")
        print(f"  上次文件: {comparison['previous_file']}")
        print(f"  不一致变 {comparison['delta_inconsistent']:+d}")
        print(f"  新增不一 {len(new_inconsistent)}")
        print(f"  已修 {len(fixed)}")
        print(f"  持续不一 {len(persistent)}")
        
        return comparison
        
    def generate_report(self):
        """生成报表"""
        print("\n========== 生成报表 ==========")
        
        output_file = self.reports_dir / f"{self.current_file.stem}_异常分析报告.xlsx"
        
        wb = openpyxl.Workbook()
        
        # 删除默认sheet
        wb.remove(wb.active)
        
        # 定义样式
        header_fill = PatternFill(start_color=self.COLORS['header'], end_color=self.COLORS['header'], fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        
        critical_fill = PatternFill(start_color=self.COLORS['critical'], end_color=self.COLORS['critical'], fill_type="solid")
        suspicious_fill = PatternFill(start_color=self.COLORS['suspicious'], end_color=self.COLORS['suspicious'], fill_type="solid")
        warning_fill = PatternFill(start_color=self.COLORS['warning'], end_color=self.COLORS['warning'], fill_type="solid")
        caution_fill = PatternFill(start_color=self.COLORS['caution'], end_color=self.COLORS['caution'], fill_type="solid")
        normal_fill = PatternFill(start_color=self.COLORS['normal'], end_color=self.COLORS['normal'], fill_type="solid")
        improved_fill = PatternFill(start_color=self.COLORS['improved'], end_color=self.COLORS['improved'], fill_type="solid")
        worsened_fill = PatternFill(start_color=self.COLORS['worsened'], end_color=self.COLORS['worsened'], fill_type="solid")
        
        thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        consistency_df = self.analysis_results.get('consistency', pd.DataFrame())
        ttest_df = self.analysis_results.get('ttest', pd.DataFrame())
        suspicious_df = self.analysis_results.get('suspicious', pd.DataFrame())
        comparison = self.analysis_results.get('comparison', None)
        
        # ========== 1. 摘要sheet ==========
        ws_summary = wb.create_sheet(title='1_摘要')
        
        current_row = 1
        
        # 标题
        ws_summary.cell(row=current_row, column=1, value='KPI异常检测报告')
        ws_summary.cell(row=current_row, column=1).font = Font(bold=True, size=16)
        current_row += 2
        
        # 文件信息
        ws_summary.cell(row=current_row, column=1, value='分析文件')
        ws_summary.cell(row=current_row, column=2, value=self.current_file.name)
        current_row += 1
        ws_summary.cell(row=current_row, column=1, value='分析时间')
        ws_summary.cell(row=current_row, column=2, value=pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'))
        current_row += 2
        
        # ========== 一致性分析表==========
        ws_summary.cell(row=current_row, column=1, value='========== 一致性分==========')
        ws_summary.cell(row=current_row, column=1).font = Font(bold=True)
        current_row += 2
        
        if not consistency_df.empty:
            # 按类型分组统
            kpi_df = consistency_df[consistency_df['Type'] == 'KPI']
            counter_df = consistency_df[consistency_df['Type'] == 'Counter']
            other_df = consistency_df[consistency_df['Type'] == 'Other']
            
            # 表头
            headers = ['', f'[总体] ({len(consistency_df)})', f'[KPI] ({len(kpi_df)})', f'[Counter] ({len(counter_df)})']
            if len(other_df) > 0:
                headers.append(f'[Other] ({len(other_df)})')
            
            for col_idx, header in enumerate(headers, start=1):
                cell = ws_summary.cell(row=current_row, column=col_idx, value=header)
                cell.fill = header_fill
                cell.font = header_font
                cell.border = thin_border
                cell.alignment = Alignment(horizontal='center')
            current_row += 1
            
            # 数据行
            status_list = ['一致', '不一致', 'partial NULL', 'NULL']
            for status in status_list:
                row_data = [
                    f'  - {status}',
                    int((consistency_df['Consistency'] == status).sum()),
                    int((kpi_df['Consistency'] == status).sum()),
                    int((counter_df['Consistency'] == status).sum()),
                ]
                if len(other_df) > 0:
                    row_data.append(int((other_df['Consistency'] == status).sum()))
                
                for col_idx, value in enumerate(row_data, start=1):
                    cell = ws_summary.cell(row=current_row, column=col_idx, value=value)
                    cell.border = thin_border
                    if col_idx > 1:
                        cell.alignment = Alignment(horizontal='center')
                    # 高亮不一致行
                    if status == '不一致' and col_idx > 1 and value > 0:
                        cell.fill = warning_fill
                current_row += 1
            
            # 添加trimmed不一致行（去除极值后仍然不一致）
            # 计算trimmed后仍然不一致的数量
            def count_trimmed_inconsistent(df):
                return int(((df['Consistency'] == '不一致') & 
                           ((df['DataCount'] < 5) | (df['Trimmed_Consistency'] == '不一致'))).sum())
            
            trimmed_row_data = [
                '  - 不一致_trimmed',
                count_trimmed_inconsistent(consistency_df),
                count_trimmed_inconsistent(kpi_df),
                count_trimmed_inconsistent(counter_df),
            ]
            if len(other_df) > 0:
                trimmed_row_data.append(count_trimmed_inconsistent(other_df))
            
            for col_idx, value in enumerate(trimmed_row_data, start=1):
                cell = ws_summary.cell(row=current_row, column=col_idx, value=value)
                cell.border = thin_border
                if col_idx > 1:
                    cell.alignment = Alignment(horizontal='center')
                    if value > 0:
                        cell.fill = critical_fill
                        cell.font = Font(color="FFFFFF")
            current_row += 1
        
        current_row += 1
        
        # ========== 可疑KPI/Counter表格 ==========
        if not suspicious_df.empty:
            ws_summary.cell(row=current_row, column=1, value='========== 可疑KPI/Counter (以trimmed为准) ==========')
            ws_summary.cell(row=current_row, column=1).font = Font(bold=True)
            current_row += 2
            
            # 过滤出trimmed后仍然有问题的可疑项
            # 对于不一致类型：数据5 trimmed后仍不一
            # 对于partial NULL类型：保
            # 对于T-Test Fail但一致的：保留（与trimmed无关
            def is_trimmed_suspicious(row):
                code = row['Code']
                # 查找对应的一致性数
                cons_row = consistency_df[consistency_df['Code'] == code]
                if cons_row.empty:
                    return True  # 找不到数据则保留
                
                consistency = cons_row['Consistency'].iloc[0]
                data_count = cons_row['DataCount'].iloc[0]
                trimmed_consistency = cons_row['Trimmed_Consistency'].iloc[0]
                
                # 如果是不一致
                if consistency == '不一致':
                    # 数据<5 或 trimmed后仍不一致 则保留
                    if data_count < 5 or trimmed_consistency == '不一致':
                        return True
                    else:
                        return False  # trimmed后变一致了，不计入
                else:
                    # partial NULL 或其他情况保留
                    return True
            
            # 应用过滤
            trimmed_suspicious_df = suspicious_df[suspicious_df.apply(is_trimmed_suspicious, axis=1)]
            
            # 按类型分组（基于trimmed）
            susp_kpi = trimmed_suspicious_df[trimmed_suspicious_df['Type'] == 'KPI']
            susp_counter = trimmed_suspicious_df[trimmed_suspicious_df['Type'] == 'Counter']
            susp_other = trimmed_suspicious_df[trimmed_suspicious_df['Type'] == 'Other']
            
            # 表头 - 显示trimmed后的数量
            susp_headers = ['', f'[总体] ({len(trimmed_suspicious_df)})', f'[KPI_trimmed] ({len(susp_kpi)})', f'[Counter_trimmed] ({len(susp_counter)})']
            if len(susp_other) > 0:
                susp_headers.append(f'[Other] ({len(susp_other)})')
            
            for col_idx, header in enumerate(susp_headers, start=1):
                cell = ws_summary.cell(row=current_row, column=col_idx, value=header)
                cell.fill = header_fill
                cell.font = header_font
                cell.border = thin_border
                cell.alignment = Alignment(horizontal='center')
            current_row += 1
            
            # 数据
            severity_list = [('Critical', '严重', critical_fill), ('Suspicious', '可疑', suspicious_fill), ('Warning', '警告', warning_fill)]
            for severity, label, fill in severity_list:
                row_data = [
                    f'  - {severity} ({label})',
                    int((trimmed_suspicious_df['Severity'] == severity).sum()),
                    int((susp_kpi['Severity'] == severity).sum()),
                    int((susp_counter['Severity'] == severity).sum()),
                ]
                if len(susp_other) > 0:
                    row_data.append(int((susp_other['Severity'] == severity).sum()))
                
                for col_idx, value in enumerate(row_data, start=1):
                    cell = ws_summary.cell(row=current_row, column=col_idx, value=value)
                    cell.border = thin_border
                    if col_idx > 1:
                        cell.alignment = Alignment(horizontal='center')
                        if value > 0:
                            cell.fill = fill
                            if severity == 'Critical':
                                cell.font = Font(color="FFFFFF")
                current_row += 1
            
            current_row += 1
            
            # ========== 综合判定统计（CV + T-Test + 辅助方法=========
            ws_summary.cell(row=current_row, column=1, value='========== 综合判定 (CV + T-Test + 辅助方法) ==========')
            ws_summary.cell(row=current_row, column=1).font = Font(bold=True)
            current_row += 2
            
            # 检查是否有Final_Judgment
            if 'Final_Judgment' in trimmed_suspicious_df.columns:
                judgment_headers = ['', '[总体]', '[KPI_trimmed]', '[Counter_trimmed]']
                for col_idx, header in enumerate(judgment_headers, start=1):
                    cell = ws_summary.cell(row=current_row, column=col_idx, value=header)
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.border = thin_border
                    cell.alignment = Alignment(horizontal='center')
                current_row += 1
                
                judgment_list = [
                    ('确认异常', '2-3项异常', critical_fill),
                    ('可能异常', '1项异常', warning_fill),
                    ('待观察', '0项异常', normal_fill)
                ]
                for judgment, desc, fill in judgment_list:
                    row_data = [
                        f'  - {judgment} ({desc})',
                        int((trimmed_suspicious_df['Final_Judgment'] == judgment).sum()),
                        int((susp_kpi['Final_Judgment'] == judgment).sum()) if 'Final_Judgment' in susp_kpi.columns else 0,
                        int((susp_counter['Final_Judgment'] == judgment).sum()) if 'Final_Judgment' in susp_counter.columns else 0,
                    ]
                    
                    for col_idx, value in enumerate(row_data, start=1):
                        cell = ws_summary.cell(row=current_row, column=col_idx, value=value)
                        cell.border = thin_border
                        if col_idx > 1:
                            cell.alignment = Alignment(horizontal='center')
                            if value > 0:
                                cell.fill = fill
                                if judgment == '确认异常':
                                    cell.font = Font(color="FFFFFF")
                    current_row += 1
        
        current_row += 1
        
        # T-test统计
        if not ttest_df.empty:
            ws_summary.cell(row=current_row, column=1, value='========== T-Test分析（与历史比较=========')
            ws_summary.cell(row=current_row, column=1).font = Font(bold=True)
            current_row += 2
            
            ws_summary.cell(row=current_row, column=1, value='  - Pass')
            ws_summary.cell(row=current_row, column=2, value=int((ttest_df['TTest_Result'] == 'Pass').sum()))
            current_row += 1
            ws_summary.cell(row=current_row, column=1, value='  - Fail')
            cell = ws_summary.cell(row=current_row, column=2, value=int((ttest_df['TTest_Result'] == 'Fail').sum()))
            if int((ttest_df['TTest_Result'] == 'Fail').sum()) > 0:
                cell.fill = critical_fill
                cell.font = Font(color="FFFFFF")
            current_row += 2
        
        # 与历史比
        if comparison:
            ws_summary.cell(row=current_row, column=1, value='========== 与历史比较 ==========')
            ws_summary.cell(row=current_row, column=1).font = Font(bold=True)
            current_row += 2
            
            compare_data = [
                ['上次分析文件', comparison['previous_file']],
                ['上次分析时间', comparison['previous_time']],
                ['', ''],
                ['不一致数变化', f"{comparison['delta_inconsistent']:+d}"],
                ['新增不一致', len(comparison['new_inconsistent'])],
                ['已修复', len(comparison['fixed'])],
                ['持续不一致', len(comparison['persistent'])],
            ]
            
            for row_data in compare_data:
                ws_summary.cell(row=current_row, column=1, value=row_data[0])
                cell = ws_summary.cell(row=current_row, column=2, value=row_data[1])
                # 高亮变化
                if '变化' in str(row_data[0]):
                    try:
                        val = int(str(row_data[1]).replace('+', ''))
                        if val > 0:
                            cell.fill = worsened_fill
                        elif val < 0:
                            cell.fill = improved_fill
                    except:
                        pass
                current_row += 1
        
        # 设置列宽
        ws_summary.column_dimensions['A'].width = 25
        ws_summary.column_dimensions['B'].width = 18
        ws_summary.column_dimensions['C'].width = 18
        ws_summary.column_dimensions['D'].width = 18
        ws_summary.column_dimensions['E'].width = 18
        
        # ========== 2. 可疑KPI sheet ==========
        if not suspicious_df.empty:
            ws_suspicious = wb.create_sheet(title='2_可疑KPI')
            
            # 需要排除的列（内部使用，不写入Excel
            exclude_cols = ['_shewhart_chart']
            headers = [h for h in suspicious_df.columns.tolist() if h not in exclude_cols]
            # 在Current_Data之前插入Current_Sparkline，在History_Data之前插入History_Sparkline
            if 'Current_Data' in headers:
                curr_idx = headers.index('Current_Data')
                headers.insert(curr_idx, 'Current_Sparkline')
            if 'History_Data' in headers:
                hist_idx = headers.index('History_Data')
                headers.insert(hist_idx, 'History_Sparkline')
            
            for col_idx, header in enumerate(headers, start=1):
                cell = ws_suspicious.cell(row=1, column=col_idx, value=header)
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = header_alignment
                cell.border = thin_border
            
            # 写入数据
            for row_idx, (_, row) in enumerate(suspicious_df.iterrows(), start=2):
                for col_idx, header in enumerate(headers, start=1):
                    if header == 'Current_Sparkline':
                        # 生成当前数据Sparkline
                        raw_data = row['Current_Data']
                        sparkline = self._generate_sparkline(raw_data)
                        cell = ws_suspicious.cell(row=row_idx, column=col_idx, value=sparkline)
                        cell.font = Font(name='Consolas', size=9)
                    elif header == 'History_Sparkline':
                        # 生成历史数据Sparkline
                        history_data = row['History_Data']
                        sparkline = self._generate_sparkline(history_data)
                        cell = ws_suspicious.cell(row=row_idx, column=col_idx, value=sparkline)
                        cell.font = Font(name='Consolas', size=9, color='808080')  # 灰色显示历史
                    else:
                        value = row[header]
                        # 处理特殊
                        if pd.isna(value):
                            value = ''
                        elif isinstance(value, float) and not np.isfinite(value):
                            value = ''
                        elif isinstance(value, dict):
                            value = ''  # 跳过dict类型的
                        cell = ws_suspicious.cell(row=row_idx, column=col_idx, value=value)
                        
                        # 根据严重程度设置背景
                        if header == 'Severity':
                            if value == 'Critical':
                                cell.fill = critical_fill
                                cell.font = Font(bold=True, color="FFFFFF")
                            elif value == 'Suspicious':
                                cell.fill = suspicious_fill
                                cell.font = Font(bold=True, color="FFFFFF")
                            elif value == 'Warning':
                                cell.fill = warning_fill
                        
                        # 高亮不一致
                        if header == 'Consistency' and value == '不一致':
                            cell.fill = warning_fill
                        
                        # 高亮Fail
                        if header == 'TTest_Result' and value == 'Fail':
                            cell.fill = critical_fill
                            cell.font = Font(color="FFFFFF")
                        
                        # 高亮辅助判断异常
                        if header == 'Aux_Judgment' and value == '异常':
                            cell.fill = warning_fill
                        
                        # 高亮综合判定
                        if header == 'Final_Judgment':
                            if value == '确认异常':
                                cell.fill = critical_fill
                                cell.font = Font(bold=True, color="FFFFFF")
                            elif value == '可能异常':
                                cell.fill = warning_fill
                            elif value == '待观察':
                                cell.fill = normal_fill
            
            # 设置列宽（包括新增的辅助判断列）
            col_widths = {
                'A': 18,   # Code
                'B': 50,   # KPI Name
                'C': 10,   # Type
                'D': 12,   # Severity
                'E': 25,   # Reasons
                'F': 10,   # CV
                'G': 12,   # Consistency
                'H': 12,   # TTest
                'I': 10,   # P_Value
                'J': 10,   # Diff%
                'K': 10,   # Z_Score
                'L': 12,   # Anomaly_Count
                'M': 12,   # Anomaly_Ratio
                'N': 10,   # CV_Ratio
                'O': 10,   # Aux_Judgment
                'P': 25,   # Aux_Reasons
                'Q': 12,   # Final_Judgment
                'R': 12,   # Current_Sparkline
                'S': 35,   # Current_Data
                'T': 12,   # History_Sparkline
                'U': 35,   # History_Data
            }
            for col, width in col_widths.items():
                ws_suspicious.column_dimensions[col].width = width
            
            ws_suspicious.freeze_panes = 'A2'
        
        # ========== 3. 变化追踪sheet ==========
        if comparison:
            ws_changes = wb.create_sheet(title='3_变化追踪')
            
            # 新增不一
            row = 1
            ws_changes.cell(row=row, column=1, value='新增不一(需关注)')
            ws_changes.cell(row=row, column=1).font = Font(bold=True, size=12)
            ws_changes.cell(row=row, column=1).fill = worsened_fill
            row += 1
            
            if comparison['new_inconsistent']:
                for code in comparison['new_inconsistent']:
                    ws_changes.cell(row=row, column=1, value=code)
                    # 获取KPI Name
                    kpi_row = consistency_df[consistency_df['Code'] == code]
                    if not kpi_row.empty:
                        ws_changes.cell(row=row, column=2, value=kpi_row['KPI Name'].iloc[0])
                    ws_changes.cell(row=row, column=1).fill = worsened_fill
                    row += 1
            else:
                ws_changes.cell(row=row, column=1, value='(')
                row += 1
            
            row += 1
            
            # 已修
            ws_changes.cell(row=row, column=1, value='已修(改善)')
            ws_changes.cell(row=row, column=1).font = Font(bold=True, size=12)
            ws_changes.cell(row=row, column=1).fill = improved_fill
            row += 1
            
            if comparison['fixed']:
                for code in comparison['fixed']:
                    ws_changes.cell(row=row, column=1, value=code)
                    ws_changes.cell(row=row, column=1).fill = improved_fill
                    row += 1
            else:
                ws_changes.cell(row=row, column=1, value='(')
                row += 1
            
            row += 1
            
            # 持续不一
            ws_changes.cell(row=row, column=1, value='持续不一(需跟进)')
            ws_changes.cell(row=row, column=1).font = Font(bold=True, size=12)
            ws_changes.cell(row=row, column=1).fill = warning_fill
            row += 1
            
            if comparison['persistent']:
                for code in comparison['persistent']:
                    ws_changes.cell(row=row, column=1, value=code)
                    kpi_row = consistency_df[consistency_df['Code'] == code]
                    if not kpi_row.empty:
                        ws_changes.cell(row=row, column=2, value=kpi_row['KPI Name'].iloc[0])
                    ws_changes.cell(row=row, column=1).fill = warning_fill
                    row += 1
            else:
                ws_changes.cell(row=row, column=1, value='(')
                row += 1
            
            ws_changes.column_dimensions['A'].width = 20
            ws_changes.column_dimensions['B'].width = 60
        
        # ========== 4. 历史摘要sheet ==========
        # 构建当前记录
        current_record = self.build_current_record()
        
        ws_history = wb.create_sheet(title='4_历史摘要')
        
        # 表头
        hist_headers = ['序号', '文件名', '分析时间', '一致', '不一致', '不一致_KPI', '不一致_Counter', 
                       '不一致_KPI_trimmed', '不一致_Counter_trimmed', 'Partial NULL', 'NULL', 
                       'Critical', 'Suspicious', 'Warning']
        for col_idx, header in enumerate(hist_headers, start=1):
            cell = ws_history.cell(row=1, column=col_idx, value=header)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = header_alignment
            cell.border = thin_border
        
        # 合并历史记录和当前记录
        all_records = self.history_records.copy() if self.history_records else []
        # 将当前记录添加到最前面（最新）
        all_records.append(current_record)
        
        # 数据（按时间倒序，当前文件在最上面）
        for row_idx, record in enumerate(reversed(all_records), start=2):
            stats = record.get('stats', {})
            is_current = (record == current_record)
            data = [
                len(all_records) - row_idx + 2,  # 序号
                record.get('filename', 'N/A'),
                record.get('timestamp', 'N/A'),
                stats.get('consistent', 0),
                stats.get('inconsistent', 0),
                stats.get('inconsistent_kpi', 0),
                stats.get('inconsistent_counter', 0),
                stats.get('inconsistent_kpi_trimmed', 0),
                stats.get('inconsistent_counter_trimmed', 0),
                stats.get('partial_null', 0),
                stats.get('null', 0),
                stats.get('suspicious_critical', 0),
                stats.get('suspicious_suspicious', 0),
                stats.get('suspicious_warning', 0),
            ]
            for col_idx, value in enumerate(data, start=1):
                cell = ws_history.cell(row=row_idx, column=col_idx, value=value)
                cell.border = thin_border
                # 高亮不一致数
                if col_idx == 5 and value > 0:  # 不一致列
                    cell.fill = warning_fill
                if col_idx == 6 and value > 0:  # 不一致_KPI
                    cell.fill = warning_fill
                if col_idx == 7 and value > 0:  # 不一致_Counter
                    cell.fill = warning_fill
                if col_idx == 8 and value > 0:  # 不一致_KPI_trimmed
                    cell.fill = critical_fill
                    cell.font = Font(color="FFFFFF")
                if col_idx == 9 and value > 0:  # 不一致_Counter_trimmed
                    cell.fill = critical_fill
                    cell.font = Font(color="FFFFFF")
                # 当前文件用蓝色背景标
                if is_current and col_idx <= 3:
                    cell.fill = PatternFill(start_color="CCE5FF", end_color="CCE5FF", fill_type="solid")
        
        # 设置列宽
        ws_history.column_dimensions['A'].width = 8
        ws_history.column_dimensions['B'].width = 60
        ws_history.column_dimensions['C'].width = 20
        for col in 'DEFGHIJKLMN':
            ws_history.column_dimensions[col].width = 14
        
        ws_history.freeze_panes = 'A2'
        
        # ========== 5. 一致性详情sheet ==========
        if not consistency_df.empty:
            ws_consistency = wb.create_sheet(title='5_一致性详情')
            
            # 添加Sparkline列到headers
            headers = consistency_df.columns.tolist()
            # 在RawData之前插入Sparkline
            if 'RawData' in headers:
                raw_idx = headers.index('RawData')
                headers.insert(raw_idx, 'Sparkline')
            
            for col_idx, header in enumerate(headers, start=1):
                cell = ws_consistency.cell(row=1, column=col_idx, value=header)
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = header_alignment
                cell.border = thin_border
            
            for row_idx, (_, row) in enumerate(consistency_df.iterrows(), start=2):
                for col_idx, header in enumerate(headers, start=1):
                    if header == 'Sparkline':
                        # 生成Sparkline（使用Unicode柱状图字符）
                        raw_data = row['RawData']
                        sparkline = self._generate_sparkline(raw_data)
                        cell = ws_consistency.cell(row=row_idx, column=col_idx, value=sparkline)
                        cell.font = Font(name='Consolas', size=9)
                    else:
                        value = row[header]
                        if pd.isna(value):
                            value = ''
                        elif isinstance(value, float) and not np.isfinite(value):
                            value = ''
                        cell = ws_consistency.cell(row=row_idx, column=col_idx, value=value)
                    
                    cell.border = thin_border
                    
                    if header == 'Consistency':
                        if value == '一致':
                            cell.fill = normal_fill
                        elif value == '不一致':
                            cell.fill = warning_fill
                    
                    # Trimmed一致性也加颜色
                    if header == 'Trimmed_Consistency':
                        if value == '一致':
                            cell.fill = normal_fill
                        elif value == '不一致':
                            cell.fill = warning_fill
                    
                    # 标记新增不一致
                    if comparison and header == 'Code' and value in comparison.get('new_inconsistent', []):
                        cell.fill = worsened_fill
                        cell.font = Font(bold=True)
            
            # 设置列宽
            ws_consistency.column_dimensions['A'].width = 18   # Code
            ws_consistency.column_dimensions['B'].width = 50   # KPI Name
            ws_consistency.column_dimensions['C'].width = 10   # Type
            ws_consistency.column_dimensions['D'].width = 12   # Mean
            ws_consistency.column_dimensions['E'].width = 12   # Std
            ws_consistency.column_dimensions['F'].width = 10   # CV
            ws_consistency.column_dimensions['G'].width = 12   # Consistency
            ws_consistency.column_dimensions['H'].width = 10   # DataCount
            ws_consistency.column_dimensions['I'].width = 12   # Trimmed_Mean
            ws_consistency.column_dimensions['J'].width = 12   # Trimmed_Std
            ws_consistency.column_dimensions['K'].width = 12   # Trimmed_CV
            ws_consistency.column_dimensions['L'].width = 14   # Trimmed_Consistency
            ws_consistency.column_dimensions['M'].width = 20   # Sparkline
            ws_consistency.column_dimensions['N'].width = 40   # RawData
            ws_consistency.freeze_panes = 'A2'
        
        # ========== 6. T-Test详情sheet ==========
        if not ttest_df.empty:
            ws_ttest = wb.create_sheet(title='6_TTest详情')
            
            headers = ttest_df.columns.tolist()
            for col_idx, header in enumerate(headers, start=1):
                cell = ws_ttest.cell(row=1, column=col_idx, value=header)
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = header_alignment
                cell.border = thin_border
            
            for row_idx, (_, row) in enumerate(ttest_df.iterrows(), start=2):
                for col_idx, header in enumerate(headers, start=1):
                    value = row[header]
                    if pd.isna(value):
                        value = ''
                    elif isinstance(value, float) and not np.isfinite(value):
                        value = ''
                    cell = ws_ttest.cell(row=row_idx, column=col_idx, value=value)
                    cell.border = thin_border
                    
                    if header == 'TTest_Result':
                        if value == 'Pass':
                            cell.fill = normal_fill
                        elif value == 'Fail':
                            cell.fill = critical_fill
                            cell.font = Font(color="FFFFFF")
            
            ws_ttest.column_dimensions['A'].width = 18
            ws_ttest.column_dimensions['B'].width = 50
            ws_ttest.freeze_panes = 'A2'
        
        # ========== 7. 数据验证sheet ==========
        # 注意：不使用跨sheet公式，避免Excel兼容性问题
        ws_verify = wb.create_sheet(title='7_数据验证')
        
        # 验证说明
        verify_info = [
            ['数据验证说明', '', '', ''],
            ['', '', '', ''],
            ['此sheet显示Python计算的统计结果', '', '', ''],
            ['您可以手动在Excel中验证这些数值是否正确', '', '', ''],
            ['验证方法：在对应的详情sheet中使用COUNTIF函数', '', '', ''],
            ['', '', '', ''],
        ]
        
        for row_idx, row_data in enumerate(verify_info, start=1):
            for col_idx, value in enumerate(row_data, start=1):
                cell = ws_verify.cell(row=row_idx, column=col_idx, value=value)
                if row_idx == 1:
                    cell.font = Font(bold=True, size=14)
        
        current_row = 7
        
        # ========== 一致性统计 ==========
        ws_verify.cell(row=current_row, column=1, value='========== 一致性统计 ==========')
        ws_verify.cell(row=current_row, column=1).font = Font(bold=True)
        current_row += 2
        
        # 表头
        for col_idx, header in enumerate(['统计项', 'Python计算值', '验证公式参考'], start=1):
            cell = ws_verify.cell(row=current_row, column=col_idx, value=header)
            cell.fill = header_fill
            cell.font = header_font
            cell.border = thin_border
        current_row += 1
        
        if not consistency_df.empty:
            cons_col_idx = consistency_df.columns.tolist().index('Consistency') + 1
            cons_col_letter = openpyxl.utils.get_column_letter(cons_col_idx)
            
            verify_data = [
                ['一致', int((consistency_df['Consistency'] == '一致').sum()), 
                 f"COUNTIF('5_一致性详情'!{cons_col_letter}:{cons_col_letter},\"一致\")"],
                ['不一致', int((consistency_df['Consistency'] == '不一致').sum()),
                 f"COUNTIF('5_一致性详情'!{cons_col_letter}:{cons_col_letter},\"不一致\")"],
                ['partial NULL', int((consistency_df['Consistency'] == 'partial NULL').sum()),
                 f"COUNTIF('5_一致性详情'!{cons_col_letter}:{cons_col_letter},\"partial NULL\")"],
                ['NULL', int((consistency_df['Consistency'] == 'NULL').sum()),
                 f"COUNTIF('5_一致性详情'!{cons_col_letter}:{cons_col_letter},\"NULL\")"],
                ['总行数', len(consistency_df), "COUNTA('5_一致性详情'!A:A)-1"],
            ]
            
            for row_data in verify_data:
                for col_idx, value in enumerate(row_data, start=1):
                    cell = ws_verify.cell(row=current_row, column=col_idx, value=value)
                    cell.border = thin_border
                current_row += 1
        
        current_row += 1
        
        # ========== 可疑KPI统计 ==========
        if not suspicious_df.empty:
            ws_verify.cell(row=current_row, column=1, value='========== 可疑KPI统计 ==========')
            ws_verify.cell(row=current_row, column=1).font = Font(bold=True)
            current_row += 2
            
            for col_idx, header in enumerate(['统计项', 'Python计算值', '验证公式参考'], start=1):
                cell = ws_verify.cell(row=current_row, column=col_idx, value=header)
                cell.fill = header_fill
                cell.font = header_font
                cell.border = thin_border
            current_row += 1
            
            sev_col_idx = suspicious_df.columns.tolist().index('Severity') + 1
            sev_col_letter = openpyxl.utils.get_column_letter(sev_col_idx)
            
            susp_verify = [
                ['Critical', int((suspicious_df['Severity'] == 'Critical').sum()),
                 f"COUNTIF('2_可疑KPI'!{sev_col_letter}:{sev_col_letter},\"Critical\")"],
                ['Suspicious', int((suspicious_df['Severity'] == 'Suspicious').sum()),
                 f"COUNTIF('2_可疑KPI'!{sev_col_letter}:{sev_col_letter},\"Suspicious\")"],
                ['Warning', int((suspicious_df['Severity'] == 'Warning').sum()),
                 f"COUNTIF('2_可疑KPI'!{sev_col_letter}:{sev_col_letter},\"Warning\")"],
                ['总计', len(suspicious_df), "COUNTA('2_可疑KPI'!A:A)-1"],
            ]
            
            for row_data in susp_verify:
                for col_idx, value in enumerate(row_data, start=1):
                    cell = ws_verify.cell(row=current_row, column=col_idx, value=value)
                    cell.border = thin_border
                current_row += 1
        
        current_row += 1
        
        # ========== T-Test统计 ==========
        if not ttest_df.empty:
            ws_verify.cell(row=current_row, column=1, value='========== T-Test统计 ==========')
            ws_verify.cell(row=current_row, column=1).font = Font(bold=True)
            current_row += 2
            
            for col_idx, header in enumerate(['统计项', 'Python计算值', '验证公式参考'], start=1):
                cell = ws_verify.cell(row=current_row, column=col_idx, value=header)
                cell.fill = header_fill
                cell.font = header_font
                cell.border = thin_border
            current_row += 1
            
            ttest_col_idx = ttest_df.columns.tolist().index('TTest_Result') + 1
            ttest_col_letter = openpyxl.utils.get_column_letter(ttest_col_idx)
            
            ttest_verify = [
                ['Pass', int((ttest_df['TTest_Result'] == 'Pass').sum()),
                 f"COUNTIF('6_TTest详情'!{ttest_col_letter}:{ttest_col_letter},\"Pass\")"],
                ['Fail', int((ttest_df['TTest_Result'] == 'Fail').sum()),
                 f"COUNTIF('6_TTest详情'!{ttest_col_letter}:{ttest_col_letter},\"Fail\")"],
            ]
            
            for row_data in ttest_verify:
                for col_idx, value in enumerate(row_data, start=1):
                    cell = ws_verify.cell(row=current_row, column=col_idx, value=value)
                    cell.border = thin_border
                current_row += 1
        
        # 设置列宽
        ws_verify.column_dimensions['A'].width = 20
        ws_verify.column_dimensions['B'].width = 18
        ws_verify.column_dimensions['C'].width = 55
        
        # 保存
        wb.save(output_file)
        print(f"报告已保存到: {output_file}")
        
        return output_file
    
    def run(self):
        """运行完整分析"""
        print("=" * 60)
        print("KPI异常检测工具(带历史追踪)")
        print("=" * 60)
        
        self.load_data()
        self.analyze_consistency()
        self.analyze_ttest_with_history()
        self.identify_suspicious_kpis()
        self.compare_with_history()
        
        report_file = self.generate_report()
        
        # 保存当前结果到历史
        current_record = self.build_current_record()
        self.save_history(current_record)
        
        return report_file


def main():
    """主函数"""
    
    print("=" * 60)
    print("KPI异常检测工具")
    print("=" * 60)
    print(f"\n📁 目录结构:")
    print(f"   数据目录: {PATHS['data']}")
    print(f"   报告目录: {PATHS['reports']}")
    print(f"   脚本目录: {PATHS['scripts']}")
    print(f"   文档目录: {PATHS['docs']}")
    
    # 从data目录列出Excel文件
    data_dir = PATHS['data']
    excel_files = list(data_dir.glob("*.xlsx"))
    excel_files = [f for f in excel_files if not f.name.startswith('~$') and '异常分析' not in f.name]
    
    if len(excel_files) == 0:
        print(f"\n⚠️ data目录没有找到Excel数据文件")
        print(f"   请将原始数据文件(.xlsx)放入: {data_dir}")
        return
    
    print(f"\n📋 可用的数据文件({len(excel_files)}个):")
    for i, f in enumerate(excel_files):
        print(f"   {i + 1}. {f.name}")
    
    choice = input("\n请选择文件编号(或按Enter选择第1个): ").strip()
    
    if choice == '':
        choice = '1'
    
    try:
        choice_num = int(choice)
        if choice_num < 1 or choice_num > len(excel_files):
            print("无效选择")
            return
    except ValueError:
        print("无效选择")
        return
    
    # 运行分析
    current_file = str(excel_files[choice_num - 1])
    detector = KPIAnomalyDetector(current_file)
    detector.run()
    
    print("\n" + "=" * 60)
    print(f"📊 报告已保存到: {PATHS['reports']}")
    print(f"📁 历史记录: {PATHS['reports'] / 'kpi_history_records.json'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
