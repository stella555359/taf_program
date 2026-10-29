#2026-01-15: outputfile 改为 "_一致性检查2":加了剔除最大值最小值的一致性二次判断
import pandas as pd
import numpy as np
import re
import sys
from pathlib import Path


def filter_code_by_max_suffix(df):
    """
    对Code列进行优化：保留相同数字编号中字母后缀最大的行
    
    Code格式: NR_xy 或 SCOUT_NR_xy
    其中 x 为2-4位数字, y 为字母(大小写忽略)
    
    如果x相同但y不同，只保留y值最大的行
    """
    if 'Code' not in df.columns:
        print("未找到'Code'列，跳过Code过滤")
        return df
    
    # 匹配模式: NR_数字字母 或 SCOUT_NR_数字字母
    pattern = r'^((?:SCOUT_)?NR_)(\d{2,4})([a-zA-Z])$'
    
    # 解析Code列，提取前缀、数字和字母后缀
    def parse_code(code):
        if pd.isna(code):
            return None, None, None
        match = re.match(pattern, str(code))
        if match:
            prefix = match.group(1)  # NR_ 或 SCOUT_NR_
            num = match.group(2)     # 数字部分
            suffix = match.group(3).lower()  # 字母后缀，转小写便于比较
            return prefix, num, suffix
        return None, None, None
    
    # 解析所有Code
    parsed = df['Code'].apply(parse_code)
    df['_code_prefix'] = parsed.apply(lambda x: x[0])
    df['_code_num'] = parsed.apply(lambda x: x[1])
    df['_code_suffix'] = parsed.apply(lambda x: x[2])
    
    # 找出有效的Code行（能匹配模式的行）
    valid_mask = df['_code_num'].notna()
    
    if not valid_mask.any():
        print("Code列中未找到符合格式的数据，跳过过滤")
        df = df.drop(columns=['_code_prefix', '_code_num', '_code_suffix'])
        return df
    
    # 按前缀+数字分组，找出每组中字母后缀最大的行
    # 创建分组键
    df['_group_key'] = df['_code_prefix'].astype(str) + df['_code_num'].astype(str)
    
    # 统计每个分组的行数
    group_counts = df[valid_mask].groupby('_group_key').size()
    duplicate_groups = group_counts[group_counts > 1]
    
    if duplicate_groups.empty:
        print("Code列中没有需要去重的数据")
        df = df.drop(columns=['_code_prefix', '_code_num', '_code_suffix', '_group_key'])
        return df
    
    print(f"\n发现 {len(duplicate_groups)} 组重复的Code编号:")
    
    rows_to_remove = []
    for group_key in duplicate_groups.index:
        group_rows = df[(df['_group_key'] == group_key) & valid_mask]
        
        # 找出字母后缀最大的行
        max_suffix = group_rows['_code_suffix'].max()
        max_suffix_rows = group_rows[group_rows['_code_suffix'] == max_suffix]
        
        # 要删除的行（不是最大后缀的行）
        rows_to_delete = group_rows[group_rows['_code_suffix'] != max_suffix]
        
        if not rows_to_delete.empty:
            codes_to_delete = rows_to_delete['Code'].tolist()
            code_to_keep = max_suffix_rows['Code'].iloc[0]
            print(f"  保留: {code_to_keep}, 删除: {codes_to_delete}")
            rows_to_remove.extend(rows_to_delete.index.tolist())
    
    # 删除行
    if rows_to_remove:
        original_count = len(df)
        df = df.drop(index=rows_to_remove)
        print(f"\n已删除 {len(rows_to_remove)} 行重复数据 ({original_count} -> {len(df)} 行)")
    
    # 清理临时列
    df = df.drop(columns=['_code_prefix', '_code_num', '_code_suffix', '_group_key'])
    
    return df.reset_index(drop=True)

def check_consistency(excel_file, traffic_model=""):
    """
    检查Excel文件中header包含'T076'关键字的列的数据一致性（使用CV < 5%作为标准）
    并将结果写入H列，保存到新文件
    
    参数:
        excel_file: Excel文件路径
        traffic_model: 流量模型名称，用于汇总表格
    """
    try:
        # 读取Excel文件
        print(f"正在读取文件: {excel_file}")
        df = pd.read_excel(excel_file)
        
        print(f"文件形状: {df.shape}")
        print(f"列名: {df.columns.tolist()}")
        
        # 查找header中包含'T076'的列
        t076_cols = [col for col in df.columns if 'T076' in str(col)]
        
        if len(t076_cols) == 0:
            print("错误: 未找到包含'T076'关键字的列")
            return None
        
        print(f"\n找到 {len(t076_cols)} 个包含'T076'的列:")
        for col in t076_cols:
            print(f"  - {col}")
        
        # 获取包含T076的列的数据
        data_cols = df[t076_cols]
        
        # 检查每行的空值情况
        null_counts = data_cols.isna().sum(axis=1)
        total_t076_cols = len(t076_cols)
        
        # 计算每行的均值和标准差
        means = data_cols.mean(axis=1)
        # 使用总体标准差(ddof=0)，避免只有一个非空值时std为NaN
        stds = data_cols.std(axis=1, ddof=0)
        
        # 计算最大值和最小值的绝对差异
        max_vals = data_cols.max(axis=1)
        min_vals = data_cols.min(axis=1)
        abs_diff = max_vals - min_vals
        
        # 计算变异系数 CV (%)
        # 避免除以0或NaN，当均值为0或NaN时记为Inf；当std为NaN时也记为Inf
        cv_raw = (stds / means) * 100
        cv = np.where(np.isfinite(means) & (means != 0) & np.isfinite(stds), cv_raw, np.inf)
        
        # 判断是否一致（CV < 5%），如果所有值相同则一致
        # 对于接近0的极小值，使用绝对差异而非CV
        SMALL_VALUE_THRESHOLD = 0.001  # 小于此值认为是极小值
        ABS_DIFF_THRESHOLD = 0.001     # 绝对差异小于此值认为一致
        
        consistency_result = []
        for i in range(len(df)):
            if null_counts.iloc[i] == total_t076_cols:  # 所有T076列都是空值
                consistency_result.append('NULL')
            elif null_counts.iloc[i] > 0:  # 部分空值
                row = data_cols.iloc[i]
                # 获取非空值的唯一值集合
                non_null_values = row.dropna().unique()
                
                # 检查是否只包含0或只包含100（除了空值）
                if len(non_null_values) == 0:
                    # 全是空值
                    consistency_result.append('NULL')
                elif len(non_null_values) == 1 and (non_null_values[0] == 0 or non_null_values[0] == 100):
                    # 只有0和空，或只有100和空
                    consistency_result.append('一致')
                else:
                    consistency_result.append('partial NULL')
            else:
                row = data_cols.iloc[i]
                if row.nunique(dropna=False) == 1:  # 所有值相同
                    consistency_result.append('一致')
                elif abs(means.iloc[i]) < SMALL_VALUE_THRESHOLD:
                    # 均值很小（接近0），使用绝对差异判断
                    if abs_diff.iloc[i] < ABS_DIFF_THRESHOLD:
                        consistency_result.append('一致')
                    else:
                        consistency_result.append('不一致')
                elif cv[i] < 5:  # 无空值且CV < 5%
                    consistency_result.append('一致')
                else:  # 无空值但CV >= 5%
                    consistency_result.append('不一致')
        
        consistency_result = np.array(consistency_result)
        
        # 删除包含'Group Name'的列
        group_name_cols = [col for col in df.columns if 'Group Name' in str(col)]
        if group_name_cols:
            df = df.drop(columns=group_name_cols)
            print(f"\n已删除列: {group_name_cols}")
        
        # 动态添加一致性判断列、变异系数列和sparklines列
        # 在所有T076列之后添加这些列
        df['T076_一致性判断'] = consistency_result
        df['T076_变异系数(%)'] = np.round(cv, 2)
        df['sparklines'] = ''  # 占位列，实际sparkline会在Excel中设置
        
        # ========== 新增：剔除最大最小值后的分析（仅当T076列>=5时） ==========
        trimmed_analysis = len(t076_cols) >= 5
        if trimmed_analysis:
            print(f"\nT076列数 >= 5 ({len(t076_cols)}列)，启用剔除极值分析")
            
            # 计算剔除最大最小值后的统计量
            trimmed_means = []
            trimmed_stds = []
            trimmed_cv = []
            trimmed_consistency = []
            
            for i in range(len(df)):
                row = data_cols.iloc[i]
                non_null_values = row.dropna()
                
                if len(non_null_values) < 3:
                    # 剔除后不足1个值，无法计算
                    trimmed_means.append(np.nan)
                    trimmed_stds.append(np.nan)
                    trimmed_cv.append(np.inf)
                    if null_counts.iloc[i] == total_t076_cols:
                        trimmed_consistency.append('NULL')
                    elif null_counts.iloc[i] > 0:
                        trimmed_consistency.append('partial NULL')
                    else:
                        trimmed_consistency.append('数据不足')
                else:
                    # 剔除最大值和最小值
                    sorted_values = non_null_values.sort_values()
                    trimmed_values = sorted_values.iloc[1:-1]  # 去掉第一个(最小)和最后一个(最大)
                    
                    t_mean = trimmed_values.mean()
                    t_std = trimmed_values.std(ddof=0)
                    trimmed_means.append(t_mean)
                    trimmed_stds.append(t_std)
                    
                    # 计算CV
                    if t_mean != 0 and np.isfinite(t_mean) and np.isfinite(t_std):
                        t_cv = (t_std / t_mean) * 100
                    else:
                        t_cv = np.inf
                    trimmed_cv.append(t_cv)
                    
                    # 判断一致性
                    if trimmed_values.nunique() == 1:
                        trimmed_consistency.append('一致')
                    elif abs(t_mean) < SMALL_VALUE_THRESHOLD:
                        t_abs_diff = trimmed_values.max() - trimmed_values.min()
                        if t_abs_diff < ABS_DIFF_THRESHOLD:
                            trimmed_consistency.append('一致')
                        else:
                            trimmed_consistency.append('不一致')
                    elif t_cv < 5:
                        trimmed_consistency.append('一致')
                    else:
                        trimmed_consistency.append('不一致')
            
            df['T076_剔除极值_一致性'] = trimmed_consistency
            df['T076_剔除极值_CV(%)'] = np.round(trimmed_cv, 2)
            
            print(f"  已添加剔除极值分析列")
        
        # 对Code列进行优化：保留相同数字编号中字母后缀最大的行
        df = filter_code_by_max_suffix(df)
        
        # 生成输出文件名
        input_path = Path(excel_file)
        output_file = input_path.parent / f"{input_path.stem}_一致性检查2{input_path.suffix}"
        
        # 保存到新文件，按'T076_一致性判断'列的值分sheet
        with pd.ExcelWriter(output_file, engine='xlsxwriter', 
                           engine_kwargs={'options': {'nan_inf_to_errors': True}}) as writer:
            # 先保存完整数据到'全部数据' sheet
            df.to_excel(writer, sheet_name='全部数据', index=False)
            
            # 获取workbook和worksheet对象
            workbook = writer.book
            worksheet = writer.sheets['全部数据']
            
            # 定义格式
            header_format = workbook.add_format({
                'text_wrap': True,
                'bold': True,
                'align': 'center',
                'valign': 'vcenter'
            })
            light_blue_format = workbook.add_format({
                'bg_color': '#ADD8E6'
            })
            # 最小值高亮格式 - Dark Red
            min_value_format = workbook.add_format({
                'bg_color': '#8B0000',  # Dark Red
                'font_color': '#FFFFFF'  # 白色字体便于阅读
            })
            # 最大值高亮格式 - Tan
            max_value_format = workbook.add_format({
                'bg_color': '#D2B48C'  # Tan
            })
            
            # 获取T076列在Excel中的列号
            t076_col_indices = [df.columns.get_loc(col) for col in t076_cols]
            sparkline_col_index = df.columns.get_loc('sparklines')
            
            # 设置header行高度和格式
            worksheet.set_row(0, 80, header_format)
            # 重新写入表头以应用换行格式
            for col_idx, col_name in enumerate(df.columns):
                worksheet.write(0, col_idx, col_name, header_format)
            
            # 冻结首行
            worksheet.freeze_panes(1, 0)
            
            # 设置T076列背景色和列宽，高亮最大最小值
            for col_idx in t076_col_indices:
                # 设置列宽为15
                worksheet.set_column(col_idx, col_idx, 15)
            
            # 逐行处理T076列，找出每行的最大最小值并高亮
            for row in range(1, len(df) + 1):
                row_data = df.iloc[row-1][t076_cols]
                row_values = row_data.dropna()
                
                if len(row_values) > 0:
                    row_min = row_values.min()
                    row_max = row_values.max()
                else:
                    row_min = row_max = None
                
                for col_idx in t076_col_indices:
                    value = df.iloc[row-1, col_idx]
                    if pd.notna(value):
                        # 判断是否为最小值或最大值
                        if row_min is not None and row_max is not None and row_min != row_max:
                            if value == row_min:
                                worksheet.write(row, col_idx, value, min_value_format)
                            elif value == row_max:
                                worksheet.write(row, col_idx, value, max_value_format)
                            else:
                                worksheet.write(row, col_idx, value, light_blue_format)
                        else:
                            worksheet.write(row, col_idx, value, light_blue_format)
                    else:
                        worksheet.write_blank(row, col_idx, None, light_blue_format)
            
            # 设置KPI Name列宽度为50
            kpi_name_cols = [i for i, col in enumerate(df.columns) if 'KPI Name' in str(col)]
            for col_idx in kpi_name_cols:
                worksheet.set_column(col_idx, col_idx, 50)
            
            # 自动调整其他列宽度
            for i, col in enumerate(df.columns):
                if i not in kpi_name_cols:
                    max_len = max(df[col].astype(str).apply(len).max(), len(str(col))) + 2
                    worksheet.set_column(i, i, min(max_len, 50))
            
            # 为每一行添加sparkline
            for row_idx in range(len(df)):
                # 构建数据范围（T076列的范围）
                first_col = t076_col_indices[0]
                last_col = t076_col_indices[-1]
                excel_row = row_idx + 1  # Excel行从1开始（0是header）
                
                # 创建sparkline配置（更接近Excel原生效果）
                sparkline_options = {
                    'range': f"'全部数据'!{chr(65+first_col)}{excel_row+1}:{chr(65+last_col)}{excel_row+1}",
                    'type': 'column',
                    'style': 11,  # 预设样式11，接近Excel默认蓝色主题
                    'high_point': False,  # 高亮最高点
                    'low_point': False,   # 高亮最低点
                    'first_point': False,
                    'last_point': False,
                    'axis': True,  # 显示零值坐标轴
                    'series_color': '#4472C4',  # 使用Excel默认蓝色
                }
                
                # 添加sparkline到单元格
                worksheet.add_sparkline(excel_row , sparkline_col_index, sparkline_options)
            
            # 获取'T076_一致性判断'列的所有唯一值
            unique_values = df['T076_一致性判断'].unique()
            
            # 为每个唯一值创建一个sheet
            for value in unique_values:
                # 过滤出该值的所有行
                filtered_df = df[df['T076_一致性判断'] == value]
                
                # sheet名称不能超过31个字符，且不能包含特殊字符
                sheet_name = str(value)[:31]
                # 替换Excel不允许的字符
                for char in [':', '\\', '/', '?', '*', '[', ']']:
                    sheet_name = sheet_name.replace(char, '_')
                
                # 写入sheet
                filtered_df.to_excel(writer, sheet_name=sheet_name, index=False)
                filtered_worksheet = writer.sheets[sheet_name]
                
                # 设置header行高度和格式
                filtered_worksheet.set_row(0, 80, header_format)
                # 重新写入表头以应用换行格式
                for col_idx, col_name in enumerate(filtered_df.columns):
                    filtered_worksheet.write(0, col_idx, col_name, header_format)
                
                # 冻结首行
                filtered_worksheet.freeze_panes(1, 0)
                
                # 设置T076列列宽
                for col_idx in t076_col_indices:
                    filtered_worksheet.set_column(col_idx, col_idx, 15)
                
                # 逐行处理T076列，找出每行的最大最小值并高亮
                for row in range(1, len(filtered_df) + 1):
                    row_data = filtered_df.iloc[row-1][t076_cols]
                    row_values = row_data.dropna()
                    
                    if len(row_values) > 0:
                        row_min = row_values.min()
                        row_max = row_values.max()
                    else:
                        row_min = row_max = None
                    
                    for col_idx in t076_col_indices:
                        value = filtered_df.iloc[row-1, col_idx]
                        if pd.notna(value):
                            # 判断是否为最小值或最大值
                            if row_min is not None and row_max is not None and row_min != row_max:
                                if value == row_min:
                                    filtered_worksheet.write(row, col_idx, value, min_value_format)
                                elif value == row_max:
                                    filtered_worksheet.write(row, col_idx, value, max_value_format)
                                else:
                                    filtered_worksheet.write(row, col_idx, value, light_blue_format)
                            else:
                                filtered_worksheet.write(row, col_idx, value, light_blue_format)
                        else:
                            filtered_worksheet.write_blank(row, col_idx, None, light_blue_format)
                
                # 设置KPI Name列宽度为50
                for col_idx in kpi_name_cols:
                    filtered_worksheet.set_column(col_idx, col_idx, 50)
                
                ## 自动调整其他列宽度
                #for i, col in enumerate(filtered_df.columns):
                #    if i not in kpi_name_cols:
                #        max_len = max(filtered_df[col].astype(str).apply(len).max(), len(str(col))) + 2
                #        filtered_worksheet.set_column(i, i, min(max_len, 50))
                
                # 为分类sheet也添加sparklines
                for idx, (orig_row_idx, row_series) in enumerate(filtered_df.iterrows()):
                    excel_row = idx + 1
                    sparkline_options = {
                        'range': f"'{sheet_name}'!{chr(65+t076_col_indices[0])}{excel_row+1}:{chr(65+t076_col_indices[-1])}{excel_row+1}",
                        'type': 'column',
                        'style': 11,  # 预设样式11，接近Excel默认蓝色主题
                        'high_point': True,  # 高亮最高点
                        'low_point': True,   # 高亮最低点
                        'negative_points': True,  # 高亮负值
                        'first_point': False,
                        'last_point': False,
                        'axis': True,  # 显示零值坐标轴
                        'series_color': '#4472C4',  # 使用Excel默认蓝色
                    }
                    filtered_worksheet.add_sparkline(excel_row, sparkline_col_index, sparkline_options)
                
                print(f"  创建sheet '{sheet_name}': {len(filtered_df)} 行数据")
            
            # 设置默认打开'不一致'sheet
            inconsistent_sheet_name = '不一致'
            if inconsistent_sheet_name in writer.sheets:
                writer.sheets[inconsistent_sheet_name].activate()
                writer.sheets['全部数据'].hide()
                writer.sheets['全部数据'].set_first_sheet()  
                writer.sheets[inconsistent_sheet_name].set_first_sheet()
        
        print(f"\n✓ 已保存到: {output_file}")
        
        # 打印统计信息
        consistent_count = (consistency_result == '一致').sum()
        inconsistent_count = (consistency_result == '不一致').sum()
        partial_null_count = (consistency_result == 'partial NULL').sum()
        null_count = (consistency_result == 'NULL').sum()
        notnull_count = len(df) - null_count
        print(f"\n统计结果:")
        # 对齐打印统计信息
        total_rows = len(df)
        label_width = max(len(s) for s in ["一致的行数", "不一致的行数", "partial NULL的行数", "NULL的行数"]) + 1
        count_width = max(6, len(str(total_rows)))

        def pct(num, den):
            return (num / den * 100) if den else np.nan

        def fmt(p):
            return f"{p:.1f}%" if np.isfinite(p) else "N/A"

        print(f"  {'一致的行数:':<{label_width}} {consistent_count:>{count_width}} ({fmt(pct(consistent_count, total_rows)):>6}) ({fmt(pct(consistent_count, notnull_count)):>6} of 非NULL行)")
        print(f"  {'不一致的行数:':<{label_width}} {inconsistent_count:>{count_width}} ({fmt(pct(inconsistent_count, total_rows)):>6}) ({fmt(pct(inconsistent_count, notnull_count)):>6} of 非NULL行)")
        print(f"  {'partial NULL的行数:':<{label_width}} {partial_null_count:>{count_width}} ({fmt(pct(partial_null_count, total_rows)):>6}) ({fmt(pct(partial_null_count, notnull_count)):>6} of 非NULL行)")
        print(f"  {'NULL的行数:':<{label_width}} {null_count:>{count_width}} ({fmt(pct(null_count, total_rows)):>6})")
        print(f"  总行数: {len(df)}")
        
        # 显示变异系数的统计
        valid_cv = cv[np.isfinite(cv)]  # 仅保留有限值，排除NaN和Inf
        if valid_cv.size > 0:
            print(f"\n变异系数统计:")
            print(f"  最小值: {np.min(valid_cv):.2f}%")
            print(f"  最大值: {np.max(valid_cv):.2f}%")
            print(f"  平均值: {np.mean(valid_cv):.2f}%")
            print(f"  中位数: {np.median(valid_cv):.2f}%")
        else:
            print("\n变异系数统计: 所有值均为NaN或Inf，无法计算统计。")
        
        # 初始化剔除极值的统计变量（用于汇总表格）
        trimmed_consistent = 0
        trimmed_inconsistent = 0
        
        # 显示剔除极值后的统计信息
        if trimmed_analysis:
            trimmed_consistency_arr = np.array(trimmed_consistency)
            trimmed_consistent = (trimmed_consistency_arr == '一致').sum()
            trimmed_inconsistent = (trimmed_consistency_arr == '不一致').sum()
            
            print(f"\n剔除极值后统计结果:")
            print(f"  {'一致的行数:':<{label_width}} {trimmed_consistent:>{count_width}} ({fmt(pct(trimmed_consistent, total_rows)):>6})")
            print(f"  {'不一致的行数:':<{label_width}} {trimmed_inconsistent:>{count_width}} ({fmt(pct(trimmed_inconsistent, total_rows)):>6})")
            
            # 对比原始和剔除极值后的结果
            improved = ((consistency_result == '不一致') & (trimmed_consistency_arr == '一致')).sum()
            worsened = ((consistency_result == '一致') & (trimmed_consistency_arr == '不一致')).sum()
            print(f"\n剔除极值效果:")
            print(f"  由'不一致'变为'一致': {improved} 行")
            print(f"  由'一致'变为'不一致': {worsened} 行")
            
            valid_trimmed_cv = np.array(trimmed_cv)
            valid_trimmed_cv = valid_trimmed_cv[np.isfinite(valid_trimmed_cv)]
            if valid_trimmed_cv.size > 0:
                print(f"\n剔除极值后变异系数统计:")
                print(f"  最小值: {np.min(valid_trimmed_cv):.2f}%")
                print(f"  最大值: {np.max(valid_trimmed_cv):.2f}%")
                print(f"  平均值: {np.mean(valid_trimmed_cv):.2f}%")
                print(f"  中位数: {np.median(valid_trimmed_cv):.2f}%")
        
        # ========== 将统计结果写入汇总表格 ==========
        summary_file = input_path.parent / "random_consistency_result.xlsx"
        
        # 准备汇总数据
        # 当trimmed_analysis为False时，使用原始一致性数据填充ratio列
        if trimmed_analysis and notnull_count > 0:
            consistent_ratio = f"{trimmed_consistent / notnull_count:2f}%"
            # 使用百分比格式，需要乘以100
            consistent_ratio =   f"{(trimmed_consistent   / notnull_count) * 100:.2f}%"
            inconsistent_ratio = f"{(trimmed_inconsistent / notnull_count) * 100:.2f}%"
        elif notnull_count > 0:
            # 不满足5列条件，使用原始数据（同样乘以100）
            consistent_ratio =   f"{(consistent_count   / notnull_count) * 100:.2f}%"
            inconsistent_ratio = f"{(inconsistent_count / notnull_count) * 100:.2f}%"
            # 不满足5列条件，使用原始数据
            consistent_ratio =   f"{(consistent_count / notnull_count) * 100:.2f}%"
            inconsistent_ratio = f"{(inconsistent_count / notnull_count) * 100:.2f}%"
        else:
            consistent_ratio = np.nan
            inconsistent_ratio = np.nan
        
        # 收集不一致的Code列表
        # 如果有trimmed_不一致的行数，使用T076_剔除极值_一致性列
        # 否则使用T076_一致性判断列
        if trimmed_analysis and trimmed_inconsistent > 0:
            # 使用剔除极值后的不一致Code
            inconsistent_codes = df[df['T076_剔除极值_一致性'] == '不一致']['Code'].dropna().astype(str).tolist()
        else:
            # 使用原始的不一致Code
            inconsistent_codes = df[df['T076_一致性判断'] == '不一致']['Code'].dropna().astype(str).tolist()
        
        not_consistency_code_list = ','.join(inconsistent_codes) if inconsistent_codes else ''
        
        # 定义Code分类函数
        def classify_code(code):
            """分类Code为Counter或KPI类型"""
            import re
            code = str(code).strip()
            # MxCy格式：x为5位数字，y为1-5位数字
            if re.match(r'^M\d{5}C\d{1,5}$', code, re.IGNORECASE):
                return 'Counter'
            # 带NR关键字（不区分大小写）
            elif re.search(r'NR', code, re.IGNORECASE):
                return 'KPI'
            else:
                return 'Other'
        
        summary_data = {
            'filename': Path(excel_file).name,
            'traffic_model': traffic_model,
            'KPI总行数': total_rows,
            '一致的行数': consistent_count,
            'trimmed_一致的行数': trimmed_consistent if trimmed_analysis else np.nan,
            '不一致的行数': inconsistent_count,
            'trimmed_不一致的行数': trimmed_inconsistent if trimmed_analysis else np.nan,
            'partial NULL的行数': partial_null_count,
            'NULL的行数': null_count,
            '非NULL的行数': notnull_count,
            'trimmed_一致_ratio%(no_NULL)': consistent_ratio,
            'trimmed_不一致_ratio%(no_NULL)': inconsistent_ratio,
            'NotConsistency_Code_List': not_consistency_code_list,
            'New_NotConsistency_Counter': '',  # 新建时为空
            'New_NotConsistency_KPI': '',  # 新建时为空
            'Total_New_NotConsistency_Counter': '',  # 新建时为空
            'Total_New_NotConsistency_KPI': '',  # 新建时为空
            'NotAppeared_NotConsistency_Counter': '',  # 新建时为空
            'NotAppeared_NotConsistency_KPI': '',  # 新建时为空
            'Total_NotAppeared_NotConsistency_Counter': '',  # 新建时为空
            'Total_NotAppeared_NotConsistency_KPI': '',  # 新建时为空
            # ========== 新增Delta变化量列 ==========
            'Delta_一致行数': '',  # 新建时为空
            'Delta_不一致行数': '',  # 新建时为空
            'Trend': '',  # 新建时为空（改善/恶化/稳定）
            # ========== CV值变化跟踪 ==========
            'Improved_Codes': '',  # CV变小的Code列表
            'Worsened_Codes': '',  # CV变大的Code列表
            'Total_Improved': '',  # 改善数量
            'Total_Worsened': '',  # 恶化数量
            # ========== 连续跟踪 ==========
            'Persistent_NotConsistency_Codes': '',  # 连续不一致的Code（>=2次）
            'Total_Persistent': '',  # 持续问题数量
        }
        
        # 读取或创建汇总表格
        is_new_summary_file = not summary_file.exists()
        
        if is_new_summary_file:
            # 新建文件，使用xlsxwriter进行格式化
            summary_df = pd.DataFrame([summary_data])
            
            with pd.ExcelWriter(summary_file, engine='xlsxwriter') as summary_writer:
                summary_df.to_excel(summary_writer, sheet_name='consistencyRatio', index=False)
                
                # 设置格式
                summary_workbook = summary_writer.book
                summary_worksheet = summary_writer.sheets['consistencyRatio']
                
                # 定义格式
                header_format = summary_workbook.add_format({
                    'text_wrap': True,
                    'bold': True,
                    'align': 'center',
                    'valign': 'vcenter'
                })
                wrap_format = summary_workbook.add_format({
                    'text_wrap': True,
                    'valign': 'vcenter'
                })
                olive_green_format = summary_workbook.add_format({
                    'bg_color': '#808000'  # Olive Green
                })
                light_orange_format = summary_workbook.add_format({
                    'bg_color': '#FFD699'  # Light Orange
                })
                
                # 设置header行高度为60，冻结首行
                summary_worksheet.set_row(0, 60, header_format)
                summary_worksheet.freeze_panes(1, 0)
                
                # 重新写入表头以应用格式
                for col_idx, col_name in enumerate(summary_df.columns):
                    summary_worksheet.write(0, col_idx, col_name, header_format)
                
                # 设置第一列(filename)宽度为36
                summary_worksheet.set_column(0, 0, 36)
                
                # 获取特定列的索引
                filename_col_idx = summary_df.columns.get_loc('filename')
                trimmed_consistent_col_idx = summary_df.columns.get_loc('trimmed_一致的行数')
                trimmed_inconsistent_col_idx = summary_df.columns.get_loc('trimmed_不一致的行数')
                
                # 设置filename列单元格wrap text
                for row in range(1, len(summary_df) + 1):
                    value = summary_df.iloc[row-1, filename_col_idx]
                    summary_worksheet.write(row, filename_col_idx, value, wrap_format)
                
                # 设置trimmed_一致的行数列高亮olive green
                for row in range(1, len(summary_df) + 1):
                    value = summary_df.iloc[row-1, trimmed_consistent_col_idx]
                    if pd.notna(value):
                        summary_worksheet.write(row, trimmed_consistent_col_idx, value, olive_green_format)
                
                # 设置trimmed_不一致的行数列高亮light orange
                for row in range(1, len(summary_df) + 1):
                    value = summary_df.iloc[row-1, trimmed_inconsistent_col_idx]
                    if pd.notna(value):
                        summary_worksheet.write(row, trimmed_inconsistent_col_idx, value, light_orange_format)
                
                # 自动调整其他列宽度
                for i, col in enumerate(summary_df.columns):
                    if i != 0:  # 跳过第一列（已设置为36）
                        max_len = max(summary_df[col].astype(str).apply(len).max(), len(str(col))) + 2
                        summary_worksheet.set_column(i, i, min(max_len, 50))
                
                # 设置NotConsistency_Code_List列宽度为50
                notconsistency_col_idx = summary_df.columns.get_loc('NotConsistency_Code_List')
                summary_worksheet.set_column(notconsistency_col_idx, notconsistency_col_idx, 50)
            
            print(f"  已创建新文件并添加 'consistencyRatio' sheet")
        else:
            # 文件已存在，使用openpyxl追加数据以保留原有格式
            import openpyxl
            from openpyxl.styles import PatternFill, Font, Alignment
            
            wb_summary = openpyxl.load_workbook(summary_file)
            
            if 'consistencyRatio' in wb_summary.sheetnames:
                ws_summary = wb_summary['consistencyRatio']
                next_row = ws_summary.max_row + 1
                
                # 定义样式
                wrap_alignment = Alignment(wrap_text=True, vertical='center')
                olive_green_fill = PatternFill(start_color="808000", end_color="808000", fill_type="solid")
                light_orange_fill = PatternFill(start_color="FFD699", end_color="FFD699", fill_type="solid")
                
                # 获取上一行的NotConsistency_Code_List进行比较
                prev_row = next_row - 1
                prev_code_list_col = 13  # NotConsistency_Code_List列（第13列）
                prev_code_list_value = ws_summary.cell(row=prev_row, column=prev_code_list_col).value
                prev_codes = set(prev_code_list_value.split(',')) if prev_code_list_value else set()
                # 去除空字符串
                prev_codes = {c.strip() for c in prev_codes if c.strip()}
                
                # 当前的Code列表
                current_codes = set(not_consistency_code_list.split(',')) if not_consistency_code_list else set()
                current_codes = {c.strip() for c in current_codes if c.strip()}
                
                # 计算新增和消失的Code
                new_codes = current_codes - prev_codes  # 当前有但上一行没有
                disappeared_codes = prev_codes - current_codes  # 上一行有但当前没有
                
                # 分类新增的Code
                new_counter_codes = [c for c in new_codes if classify_code(c) == 'Counter']
                new_kpi_codes = [c for c in new_codes if classify_code(c) == 'KPI']
                
                # 分类消失的Code
                disappeared_counter_codes = [c for c in disappeared_codes if classify_code(c) == 'Counter']
                disappeared_kpi_codes = [c for c in disappeared_codes if classify_code(c) == 'KPI']
                
                summary_data['New_NotConsistency_Counter'] = ','.join(sorted(new_counter_codes)) if new_counter_codes else ''
                summary_data['New_NotConsistency_KPI'] = ','.join(sorted(new_kpi_codes)) if new_kpi_codes else ''
                summary_data['Total_New_NotConsistency_Counter'] = len(new_counter_codes) if new_counter_codes else ''
                summary_data['Total_New_NotConsistency_KPI'] = len(new_kpi_codes) if new_kpi_codes else ''
                summary_data['NotAppeared_NotConsistency_Counter'] = ','.join(sorted(disappeared_counter_codes)) if disappeared_counter_codes else ''
                summary_data['NotAppeared_NotConsistency_KPI'] = ','.join(sorted(disappeared_kpi_codes)) if disappeared_kpi_codes else ''
                summary_data['Total_NotAppeared_NotConsistency_Counter'] = len(disappeared_counter_codes) if disappeared_counter_codes else ''
                summary_data['Total_NotAppeared_NotConsistency_KPI'] = len(disappeared_kpi_codes) if disappeared_kpi_codes else ''
                
                # ========== 计算Delta变化量和趋势 ==========
                # 获取上一行的一致/不一致行数
                prev_consistent_col = 5  # trimmed_一致的行数列（第5列）
                prev_inconsistent_col = 7  # trimmed_不一致的行数列（第7列）
                prev_consistent_value = ws_summary.cell(row=prev_row, column=prev_consistent_col).value
                prev_inconsistent_value = ws_summary.cell(row=prev_row, column=prev_inconsistent_col).value
                
                # 计算Delta
                current_consistent = trimmed_consistent if trimmed_analysis else consistent_count
                current_inconsistent = trimmed_inconsistent if trimmed_analysis else inconsistent_count
                
                if prev_consistent_value is not None and pd.notna(prev_consistent_value):
                    delta_consistent = current_consistent - int(prev_consistent_value)
                    summary_data['Delta_一致行数'] = delta_consistent
                else:
                    delta_consistent = 0
                    summary_data['Delta_一致行数'] = ''
                
                if prev_inconsistent_value is not None and pd.notna(prev_inconsistent_value):
                    delta_inconsistent = current_inconsistent - int(prev_inconsistent_value)
                    summary_data['Delta_不一致行数'] = delta_inconsistent
                else:
                    delta_inconsistent = 0
                    summary_data['Delta_不一致行数'] = ''
                
                # 判断趋势
                if delta_inconsistent < 0:
                    summary_data['Trend'] = '改善'
                elif delta_inconsistent > 0:
                    summary_data['Trend'] = '恶化'
                else:
                    summary_data['Trend'] = '稳定'
                
                # ========== CV值变化跟踪 ==========
                # 构建当前Code到CV的映射
                cv_col_name = 'T076_剔除极值_CV(%)' if trimmed_analysis else 'T076_变异系数(%)'
                current_code_cv = {}
                if 'Code' in df.columns and cv_col_name in df.columns:
                    for _, row in df.iterrows():
                        code = str(row['Code']).strip() if pd.notna(row['Code']) else ''
                        cv_val = row[cv_col_name] if pd.notna(row[cv_col_name]) else np.inf
                        if code:
                            current_code_cv[code] = cv_val
                
                # 尝试读取上一次的output文件获取CV值
                prev_code_cv = {}
                # 从上一行获取filename，构建历史文件路径
                prev_filename_col = 1
                prev_filename = ws_summary.cell(row=prev_row, column=prev_filename_col).value
                if prev_filename:
                    prev_output_file = input_path.parent / f"{Path(prev_filename).stem}_一致性检查2.xlsx"
                    if prev_output_file.exists():
                        try:
                            prev_df = pd.read_excel(prev_output_file, sheet_name='全部数据')
                            prev_cv_col = 'T076_剔除极值_CV(%)' if 'T076_剔除极值_CV(%)' in prev_df.columns else 'T076_变异系数(%)'
                            if 'Code' in prev_df.columns and prev_cv_col in prev_df.columns:
                                for _, row in prev_df.iterrows():
                                    code = str(row['Code']).strip() if pd.notna(row['Code']) else ''
                                    cv_val = row[prev_cv_col] if pd.notna(row[prev_cv_col]) else np.inf
                                    if code:
                                        prev_code_cv[code] = cv_val
                        except Exception as e:
                            print(f"  警告: 无法读取历史文件CV数据: {e}")
                
                # 比较CV值变化（只比较共同存在的Code）
                improved_codes = []
                worsened_codes = []
                common_codes = set(current_code_cv.keys()) & set(prev_code_cv.keys())
                for code in common_codes:
                    curr_cv = current_code_cv.get(code, np.inf)
                    prev_cv = prev_code_cv.get(code, np.inf)
                    if np.isfinite(curr_cv) and np.isfinite(prev_cv):
                        if curr_cv < prev_cv - 0.5:  # CV减少超过0.5%认为改善
                            improved_codes.append(code)
                        elif curr_cv > prev_cv + 0.5:  # CV增加超过0.5%认为恶化
                            worsened_codes.append(code)
                
                summary_data['Improved_Codes'] = ','.join(sorted(improved_codes)) if improved_codes else ''
                summary_data['Worsened_Codes'] = ','.join(sorted(worsened_codes)) if worsened_codes else ''
                summary_data['Total_Improved'] = len(improved_codes) if improved_codes else ''
                summary_data['Total_Worsened'] = len(worsened_codes) if worsened_codes else ''
                
                # ========== 连续跟踪功能 ==========
                # 持续不一致的Code = 当前不一致 且 上次也不一致
                persistent_codes = current_codes & prev_codes
                summary_data['Persistent_NotConsistency_Codes'] = ','.join(sorted(persistent_codes)) if persistent_codes else ''
                summary_data['Total_Persistent'] = len(persistent_codes) if persistent_codes else ''
                
                # 按列顺序写入数据
                summary_columns = ['filename', 'traffic_model', 'KPI总行数', '一致的行数', 'trimmed_一致的行数',
                                   '不一致的行数', 'trimmed_不一致的行数', 'partial NULL的行数', 'NULL的行数',
                                   '非NULL的行数', 'trimmed_一致_ratio%(no_NULL)', 'trimmed_不一致_ratio%(no_NULL)',
                                   'NotConsistency_Code_List', 
                                   'New_NotConsistency_Counter', 'New_NotConsistency_KPI',
                                   'Total_New_NotConsistency_Counter', 'Total_New_NotConsistency_KPI',
                                   'NotAppeared_NotConsistency_Counter', 'NotAppeared_NotConsistency_KPI',
                                   'Total_NotAppeared_NotConsistency_Counter', 'Total_NotAppeared_NotConsistency_KPI',
                                   'Delta_一致行数', 'Delta_不一致行数', 'Trend',
                                   'Improved_Codes', 'Worsened_Codes', 'Total_Improved', 'Total_Worsened',
                                   'Persistent_NotConsistency_Codes', 'Total_Persistent']
                
                # 定义额外的样式
                green_fill = PatternFill(start_color="90EE90", end_color="90EE90", fill_type="solid")  # 浅绿色-改善
                red_fill = PatternFill(start_color="FF6B6B", end_color="FF6B6B", fill_type="solid")  # 浅红色-恶化
                
                for col_idx, col_name in enumerate(summary_columns, start=1):
                    value = summary_data.get(col_name, '')
                    cell = ws_summary.cell(row=next_row, column=col_idx, value=value)
                    
                    # 应用特定列的样式
                    if col_name == 'filename':
                        cell.alignment = wrap_alignment
                    elif col_name == 'trimmed_一致的行数' and pd.notna(value):
                        cell.fill = olive_green_fill
                    elif col_name == 'trimmed_不一致的行数' and pd.notna(value):
                        cell.fill = light_orange_fill
                    elif col_name == 'Trend':
                        if value == '改善':
                            cell.fill = green_fill
                        elif value == '恶化':
                            cell.fill = red_fill
                
                wb_summary.save(summary_file)
                print(f"  已追加数据到 'consistencyRatio' sheet (第 {next_row} 行)")
                
                # ========== 在output_file中高亮对应的Code ==========
                # 合并所有新增的Code (Counter + KPI)
                all_new_codes = set(new_counter_codes + new_kpi_codes)
                # 合并所有消失的Code (Counter + KPI)
                all_disappeared_codes = set(disappeared_counter_codes + disappeared_kpi_codes)
                
                if all_new_codes or all_disappeared_codes:
                    # 打开output_file进行高亮处理
                    wb_output = openpyxl.load_workbook(output_file)
                    yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
                    grey_fill = PatternFill(start_color="808080", end_color="808080", fill_type="solid")
                    
                    # 在"不一致"sheet中高亮新增的Code为yellow
                    if all_new_codes and '不一致' in wb_output.sheetnames:
                        ws_inconsistent = wb_output['不一致']
                        # 找到Code列的索引
                        code_col_idx = None
                        for col in range(1, ws_inconsistent.max_column + 1):
                            if ws_inconsistent.cell(row=1, column=col).value == 'Code':
                                code_col_idx = col
                                break
                        
                        if code_col_idx:
                            for row in range(2, ws_inconsistent.max_row + 1):
                                cell_value = ws_inconsistent.cell(row=row, column=code_col_idx).value
                                if cell_value and str(cell_value).strip() in all_new_codes:
                                    ws_inconsistent.cell(row=row, column=code_col_idx).fill = yellow_fill
                            print(f"  已在 '不一致' sheet中高亮 {len(all_new_codes)} 个新增Code为yellow")
                    
                    # 在"全部数据"sheet中高亮消失的Code为grey
                    if all_disappeared_codes and '全部数据' in wb_output.sheetnames:
                        ws_all_data = wb_output['全部数据']
                        # 找到Code列的索引
                        code_col_idx = None
                        for col in range(1, ws_all_data.max_column + 1):
                            if ws_all_data.cell(row=1, column=col).value == 'Code':
                                code_col_idx = col
                                break
                        
                        if code_col_idx:
                            for row in range(2, ws_all_data.max_row + 1):
                                cell_value = ws_all_data.cell(row=row, column=code_col_idx).value
                                if cell_value and str(cell_value).strip() in all_disappeared_codes:
                                    ws_all_data.cell(row=row, column=code_col_idx).fill = grey_fill
                            print(f"  已在 '全部数据' sheet中高亮 {len(all_disappeared_codes)} 个消失Code为grey")
                    
                    wb_output.save(output_file)
                    print(f"  高亮结果已保存到: {output_file}")
                
                # ========== 生成详细差异分析sheet ==========
                # 只有当有历史CV数据时才生成
                if prev_code_cv:
                    wb_output = openpyxl.load_workbook(output_file)
                    
                    # 创建或覆盖"差异分析"sheet
                    if '差异分析' in wb_output.sheetnames:
                        del wb_output['差异分析']
                    ws_diff = wb_output.create_sheet(title='差异分析')
                    
                    # 写入header（新增上次文件名、上次原始数据、本次原始数据、KPI Name）
                    diff_headers = ['Code', 'KPI Name', '上次文件名', '上次状态', '本次状态', '上次CV(%)', '本次CV(%)', 
                                    'CV变化', '变化类型', '上次原始数据', '本次原始数据']
                    for col_idx, header in enumerate(diff_headers, start=1):
                        cell = ws_diff.cell(row=1, column=col_idx, value=header)
                        cell.font = Font(bold=True)
                        cell.alignment = Alignment(horizontal='center', vertical='center')
                    
                    # 冻结首行
                    ws_diff.freeze_panes = 'A2'
                    
                    # 构建上次一致性状态映射和原始数据映射
                    prev_consistency_status = {}
                    prev_raw_data = {}  # Code -> 原始T076数据字符串
                    prev_kpi_name = {}  # Code -> KPI Name
                    prev_t076_cols = []
                    if prev_output_file.exists():
                        try:
                            prev_all_df = pd.read_excel(prev_output_file, sheet_name='全部数据')
                            consistency_col = 'T076_剔除极值_一致性' if 'T076_剔除极值_一致性' in prev_all_df.columns else 'T076_一致性判断'
                            # 获取上次的T076列
                            prev_t076_cols = [col for col in prev_all_df.columns if 'T076' in str(col) and col not in ['T076_一致性判断', 'T076_变异系数(%)', 'T076_剔除极值_一致性', 'T076_剔除极值_CV(%)']]
                            # 查找KPI Name列
                            prev_kpi_name_col = [col for col in prev_all_df.columns if 'KPI Name' in str(col)]
                            prev_kpi_name_col = prev_kpi_name_col[0] if prev_kpi_name_col else None
                            
                            if 'Code' in prev_all_df.columns and consistency_col in prev_all_df.columns:
                                for _, row in prev_all_df.iterrows():
                                    code = str(row['Code']).strip() if pd.notna(row['Code']) else ''
                                    status = row[consistency_col] if pd.notna(row[consistency_col]) else ''
                                    if code:
                                        prev_consistency_status[code] = status
                                        # 获取KPI Name
                                        if prev_kpi_name_col and pd.notna(row[prev_kpi_name_col]):
                                            prev_kpi_name[code] = str(row[prev_kpi_name_col])
                                        # 获取该Code的T076原始数据
                                        raw_values = []
                                        for t_col in prev_t076_cols:
                                            val = row[t_col]
                                            if pd.notna(val):
                                                raw_values.append(str(val))
                                            else:
                                                raw_values.append('')
                                        prev_raw_data[code] = ','.join(raw_values)
                        except Exception:
                            pass
                    
                    # 构建当前一致性状态映射和原始数据映射
                    current_consistency_status = {}
                    current_raw_data = {}  # Code -> 原始T076数据字符串
                    current_kpi_name = {}  # Code -> KPI Name
                    consistency_col = 'T076_剔除极值_一致性' if trimmed_analysis else 'T076_一致性判断'
                    # 获取当前的T076列（排除计算列）
                    current_t076_cols = [col for col in df.columns if 'T076' in str(col) and col not in ['T076_一致性判断', 'T076_变异系数(%)', 'T076_剔除极值_一致性', 'T076_剔除极值_CV(%)']]
                    # 查找KPI Name列
                    current_kpi_name_col = [col for col in df.columns if 'KPI Name' in str(col)]
                    current_kpi_name_col = current_kpi_name_col[0] if current_kpi_name_col else None
                    
                    if 'Code' in df.columns and consistency_col in df.columns:
                        for _, row in df.iterrows():
                            code = str(row['Code']).strip() if pd.notna(row['Code']) else ''
                            status = row[consistency_col] if pd.notna(row[consistency_col]) else ''
                            if code:
                                current_consistency_status[code] = status
                                # 获取KPI Name
                                if current_kpi_name_col and pd.notna(row[current_kpi_name_col]):
                                    current_kpi_name[code] = str(row[current_kpi_name_col])
                                # 获取该Code的T076原始数据
                                raw_values = []
                                for t_col in current_t076_cols:
                                    val = row[t_col]
                                    if pd.notna(val):
                                        raw_values.append(str(val))
                                    else:
                                        raw_values.append('')
                                current_raw_data[code] = ','.join(raw_values)
                    
                    # 收集所有Code并生成差异数据
                    all_codes_union = set(current_code_cv.keys()) | set(prev_code_cv.keys())
                    diff_data = []
                    
                    for code in sorted(all_codes_union):
                        prev_status = prev_consistency_status.get(code, 'N/A')
                        curr_status = current_consistency_status.get(code, 'N/A')
                        prev_cv = prev_code_cv.get(code, None)
                        curr_cv = current_code_cv.get(code, None)
                        
                        # 计算CV变化
                        if prev_cv is not None and curr_cv is not None and np.isfinite(prev_cv) and np.isfinite(curr_cv):
                            cv_change = curr_cv - prev_cv
                        else:
                            cv_change = None
                        
                        # 判断变化类型
                        if prev_status == 'N/A' and curr_status != 'N/A':
                            change_type = '新增Code'
                        elif prev_status != 'N/A' and curr_status == 'N/A':
                            change_type = '移除Code'
                        elif prev_status == '一致' and curr_status == '不一致':
                            change_type = '恶化'
                        elif prev_status == '不一致' and curr_status == '一致':
                            change_type = '改善'
                        elif prev_status == curr_status and cv_change is not None:
                            if cv_change < -0.5:
                                change_type = 'CV改善'
                            elif cv_change > 0.5:
                                change_type = 'CV恶化'
                            else:
                                change_type = '稳定'
                        else:
                            change_type = '稳定'
                        
                        # 只记录有变化的Code（排除完全稳定的）
                        if change_type != '稳定':
                            # 获取KPI Name（优先使用当前的，如果没有则用上次的）
                            kpi_name = current_kpi_name.get(code, prev_kpi_name.get(code, 'N/A'))
                            
                            diff_data.append({
                                'Code': code,
                                'KPI Name': kpi_name,
                                '上次文件名': prev_filename if prev_filename else 'N/A',
                                '上次状态': prev_status,
                                '本次状态': curr_status,
                                '上次CV(%)': f"{prev_cv:.2f}" if prev_cv is not None and np.isfinite(prev_cv) else 'N/A',
                                '本次CV(%)': f"{curr_cv:.2f}" if curr_cv is not None and np.isfinite(curr_cv) else 'N/A',
                                'CV变化': f"{cv_change:+.2f}" if cv_change is not None else 'N/A',
                                '变化类型': change_type,
                                '上次原始数据': prev_raw_data.get(code, 'N/A'),
                                '本次原始数据': current_raw_data.get(code, 'N/A')
                            })
                    
                    # 写入差异数据
                    # 定义样式
                    improve_fill = PatternFill(start_color="90EE90", end_color="90EE90", fill_type="solid")  # 浅绿
                    worsen_fill = PatternFill(start_color="FF6B6B", end_color="FF6B6B", fill_type="solid")  # 浅红
                    new_fill = PatternFill(start_color="87CEEB", end_color="87CEEB", fill_type="solid")  # 天蓝
                    remove_fill = PatternFill(start_color="D3D3D3", end_color="D3D3D3", fill_type="solid")  # 浅灰
                    
                    for row_idx, data in enumerate(diff_data, start=2):
                        for col_idx, header in enumerate(diff_headers, start=1):
                            cell = ws_diff.cell(row=row_idx, column=col_idx, value=data.get(header, ''))
                        
                        # 根据变化类型设置整行背景色
                        change_type = data.get('变化类型', '')
                        if change_type in ['改善', 'CV改善']:
                            fill = improve_fill
                        elif change_type in ['恶化', 'CV恶化']:
                            fill = worsen_fill
                        elif change_type == '新增Code':
                            fill = new_fill
                        elif change_type == '移除Code':
                            fill = remove_fill
                        else:
                            fill = None
                        
                        if fill:
                            for col_idx in range(1, len(diff_headers) + 1):
                                ws_diff.cell(row=row_idx, column=col_idx).fill = fill
                    
                    # 设置列宽
                    ws_diff.column_dimensions['A'].width = 20  # Code
                    ws_diff.column_dimensions['B'].width = 50  # KPI Name
                    ws_diff.column_dimensions['C'].width = 40  # 上次文件名
                    ws_diff.column_dimensions['D'].width = 12  # 上次状态
                    ws_diff.column_dimensions['E'].width = 12  # 本次状态
                    ws_diff.column_dimensions['F'].width = 12  # 上次CV
                    ws_diff.column_dimensions['G'].width = 12  # 本次CV
                    ws_diff.column_dimensions['H'].width = 10  # CV变化
                    ws_diff.column_dimensions['I'].width = 12  # 变化类型
                    ws_diff.column_dimensions['J'].width = 50  # 上次原始数据
                    ws_diff.column_dimensions['K'].width = 50  # 本次原始数据
                    
                    wb_output.save(output_file)
                    print(f"  已创建 '差异分析' sheet，共 {len(diff_data)} 条变化记录")
                
                # ========== 生成历史异常分析sheet ==========
                # 读取所有历史的NotConsistency_Code_List进行统计
                all_history_codes = []  # 每行的不一致Code集合列表
                all_history_filenames = []  # 对应的文件名列表
                
                # 从consistencyRatio sheet读取所有历史记录
                for row in range(2, next_row + 1):  # 包含当前新追加的行
                    code_list_value = ws_summary.cell(row=row, column=13).value  # NotConsistency_Code_List列
                    filename_value = ws_summary.cell(row=row, column=1).value  # filename列
                    
                    if code_list_value:
                        codes = {c.strip() for c in code_list_value.split(',') if c.strip()}
                    else:
                        codes = set()
                    all_history_codes.append(codes)
                    all_history_filenames.append(filename_value if filename_value else f"记录{row-1}")
                
                total_records = len(all_history_codes)
                
                if total_records >= 2:  # 至少有2条记录才进行历史分析
                    # 统计每个Code的历史不一致情况
                    all_codes_ever = set()
                    for codes in all_history_codes:
                        all_codes_ever.update(codes)
                    
                    history_stats = {}
                    for code in all_codes_ever:
                        # 统计出现次数和对应的文件名
                        occurrence_count = 0
                        occurrence_filenames = []  # 记录该Code出现不一致的文件名
                        for i, codes in enumerate(all_history_codes):
                            if code in codes:
                                occurrence_count += 1
                                occurrence_filenames.append(all_history_filenames[i])
                        
                        # 计算连续不一致次数（从最后往前数）
                        consecutive_count = 0
                        for i in range(len(all_history_codes) - 1, -1, -1):
                            if code in all_history_codes[i]:
                                consecutive_count += 1
                            else:
                                break
                        
                        # 计算不一致比例
                        inconsistency_ratio = occurrence_count / total_records * 100
                        
                        # 判断状态
                        if inconsistency_ratio == 100:
                            status = '固定异常'
                        elif consecutive_count >= 3:
                            status = '持续异常'
                        elif inconsistency_ratio >= 50:
                            status = '频繁异常'
                        else:
                            status = '偶发'
                        
                        history_stats[code] = {
                            'Code': code,
                            '历史出现次数': total_records,
                            '不一致次数': occurrence_count,
                            '不一致比例': f"{inconsistency_ratio:.1f}%",
                            '连续不一致次数': consecutive_count,
                            '状态': status,
                            '异常文件名': occurrence_filenames  # 保存文件名列表
                        }
                    
                    # 获取KPI Name映射（使用当前数据）
                    code_to_kpi_name = {}
                    kpi_name_col = [col for col in df.columns if 'KPI Name' in str(col)]
                    kpi_name_col = kpi_name_col[0] if kpi_name_col else None
                    if 'Code' in df.columns and kpi_name_col:
                        for _, row_data in df.iterrows():
                            code = str(row_data['Code']).strip() if pd.notna(row_data['Code']) else ''
                            kpi_name = str(row_data[kpi_name_col]) if pd.notna(row_data[kpi_name_col]) else ''
                            if code:
                                code_to_kpi_name[code] = kpi_name
                    
                    # 打开output_file添加历史异常分析sheet
                    wb_output = openpyxl.load_workbook(output_file)
                    
                    # 创建或覆盖"历史异常分析"sheet
                    if '历史异常分析' in wb_output.sheetnames:
                        del wb_output['历史异常分析']
                    ws_history = wb_output.create_sheet(title='历史异常分析')
                    
                    # 写入header（添加异常文件名列）
                    history_headers = ['Code', 'KPI Name', '历史记录数', '不一致次数', '不一致比例', '连续不一致次数', '状态', '异常文件名']
                    for col_idx, header in enumerate(history_headers, start=1):
                        cell = ws_history.cell(row=1, column=col_idx, value=header)
                        cell.font = Font(bold=True)
                        cell.alignment = Alignment(horizontal='center', vertical='center')
                    
                    # 冻结首行
                    ws_history.freeze_panes = 'A2'
                    
                    # 定义状态颜色
                    fixed_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")  # 红色-固定异常
                    persistent_fill = PatternFill(start_color="FF6B6B", end_color="FF6B6B", fill_type="solid")  # 浅红-持续异常
                    frequent_fill = PatternFill(start_color="FFA500", end_color="FFA500", fill_type="solid")  # 橙色-频繁异常
                    occasional_fill = PatternFill(start_color="90EE90", end_color="90EE90", fill_type="solid")  # 浅绿-偶发
                    
                    # 按状态优先级排序：固定异常 > 持续异常 > 频繁异常 > 偶发
                    status_priority = {'固定异常': 0, '持续异常': 1, '频繁异常': 2, '偶发': 3}
                    sorted_codes = sorted(history_stats.keys(), 
                                         key=lambda x: (status_priority.get(history_stats[x]['状态'], 4), 
                                                       -history_stats[x]['不一致次数'],
                                                       x))
                    
                    # 写入数据
                    for row_idx, code in enumerate(sorted_codes, start=2):
                        stats = history_stats[code]
                        kpi_name = code_to_kpi_name.get(code, 'N/A')
                        
                        ws_history.cell(row=row_idx, column=1, value=code)
                        ws_history.cell(row=row_idx, column=2, value=kpi_name)
                        ws_history.cell(row=row_idx, column=3, value=stats['历史出现次数'])
                        ws_history.cell(row=row_idx, column=4, value=stats['不一致次数'])
                        ws_history.cell(row=row_idx, column=5, value=stats['不一致比例'])
                        ws_history.cell(row=row_idx, column=6, value=stats['连续不一致次数'])
                        ws_history.cell(row=row_idx, column=7, value=stats['状态'])
                        
                        # 对于频繁异常和偶发状态，写入异常文件名（用分号隔开）
                        status = stats['状态']
                        if status in ['频繁异常', '偶发']:
                            filenames_str = ';'.join(stats['异常文件名'])
                            ws_history.cell(row=row_idx, column=8, value=filenames_str)
                        else:
                            ws_history.cell(row=row_idx, column=8, value='')
                        
                        # 根据状态设置背景色
                        if status == '固定异常':
                            fill = fixed_fill
                        elif status == '持续异常':
                            fill = persistent_fill
                        elif status == '频繁异常':
                            fill = frequent_fill
                        else:
                            fill = occasional_fill
                        
                        for col_idx in range(1, len(history_headers) + 1):
                            ws_history.cell(row=row_idx, column=col_idx).fill = fill
                    
                    # 设置列宽
                    ws_history.column_dimensions['A'].width = 20  # Code
                    ws_history.column_dimensions['B'].width = 50  # KPI Name
                    ws_history.column_dimensions['C'].width = 14  # 历史记录数
                    ws_history.column_dimensions['D'].width = 12  # 不一致次数
                    ws_history.column_dimensions['E'].width = 12  # 不一致比例
                    ws_history.column_dimensions['F'].width = 16  # 连续不一致次数
                    ws_history.column_dimensions['G'].width = 12  # 状态
                    ws_history.column_dimensions['H'].width = 60  # 异常文件名
                    
                    wb_output.save(output_file)
                    
                    # 统计各状态数量
                    status_counts = {}
                    for code, stats in history_stats.items():
                        s = stats['状态']
                        status_counts[s] = status_counts.get(s, 0) + 1
                    
                    print(f"  已创建 '历史异常分析' sheet，共 {len(history_stats)} 个Code:")
                    for s in ['固定异常', '持续异常', '频繁异常', '偶发']:
                        if s in status_counts:
                            print(f"    - {s}: {status_counts[s]} 个")
                
            else:
                # consistencyRatio sheet不存在，创建新的
                ws_summary = wb_summary.create_sheet(title='consistencyRatio')
                
                # 写入header
                summary_columns = ['filename', 'traffic_model', 'KPI总行数', '一致的行数', 'trimmed_一致的行数',
                                   '不一致的行数', 'trimmed_不一致的行数', 'partial NULL的行数', 'NULL的行数',
                                   '非NULL的行数', 'trimmed_一致_ratio%(no_NULL)', 'trimmed_不一致_ratio%(no_NULL)',
                                   'NotConsistency_Code_List', 
                                   'New_NotConsistency_Counter', 'New_NotConsistency_KPI',
                                   'Total_New_NotConsistency_Counter', 'Total_New_NotConsistency_KPI',
                                   'NotAppeared_NotConsistency_Counter', 'NotAppeared_NotConsistency_KPI',
                                   'Total_NotAppeared_NotConsistency_Counter', 'Total_NotAppeared_NotConsistency_KPI',
                                   'Delta_一致行数', 'Delta_不一致行数', 'Trend',
                                   'Improved_Codes', 'Worsened_Codes', 'Total_Improved', 'Total_Worsened',
                                   'Persistent_NotConsistency_Codes', 'Total_Persistent']
                
                for col_idx, col_name in enumerate(summary_columns, start=1):
                    cell = ws_summary.cell(row=1, column=col_idx, value=col_name)
                    cell.font = Font(bold=True)
                    cell.alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
                
                # 写入数据（新建时8个新列为空）
                for col_idx, col_name in enumerate(summary_columns, start=1):
                    value = summary_data.get(col_name, '')
                    ws_summary.cell(row=2, column=col_idx, value=value)
                
                ws_summary.freeze_panes = 'A2'
                wb_summary.save(summary_file)
                print(f"  已创建 'consistencyRatio' sheet并写入数据")
        
        print(f"\n✓ 统计结果已追加到: {summary_file}")
        
        return output_file
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # 在这里指定要处理的Excel文件路径
    #excel_file = r"0112.1_26R2.0112.2.T076.SCF.26R1post5_32UEs_httpDL_bigfile_shortCall_2csv_5run.xlsx"
    #excel_file = r"0116.2_26R2.0115.2_T076.SCF.26R1post5_32UEs_httpDL_bigFile_shortCall_2csv6run.xlsx"
    excel_file = r"0117.2_26R2.0115.2_T076.SCF.26R1post5_32UEs_httpDL_bigShort_2csv5run.xlsx"
    #excel_file = r"26R2.0115.2_T076.SCF.26R1post5_32UEs_httpDL_bigFile_short_2csv5runmerge.xlsx"
    #excel_file = r"0112.2_26R2.0112.2_T076.SCF.26R1post5__32UEs_httpDL_smallfile_longCall_2csv6run.xlsx"
    #excel_file = r"0115.1_26R2.0115.2_T076.SCF.26R1post5_32UEs_httpDL_bigFile_shortCall_2csv3run.xlsx"
    
    # 根据excel文件名自动推断 traffic_model
    def infer_traffic_model(excel_path: str) -> str:
        name = Path(excel_path).name.lower()
        parts = []
        # 业务类型
        if 'httpdl' in name:
            parts.append('httpDL')
        elif 'httpul' in name:
            parts.append('httpUL')
        elif 'http' in name:
            parts.append('http')
        # 文件大小
        if 'big' in name:
            parts.append('big')
        elif 'small' in name:
            parts.append('small')
        # 呼叫时长
        if 'short' in name:
            parts.append('short')
        elif 'long' in name:
            parts.append('long')
        return '_'.join(parts) if parts else 'unknown'

    traffic_model = infer_traffic_model(excel_file)
    # 如果文件不存在，尝试查找当前目录下的excel文件
    if not Path(excel_file).exists():
        current_dir = Path(".")
        excel_files = list(current_dir.glob("*.xlsx")) + list(current_dir.glob("*.xls"))
        excel_files = [f for f in excel_files if not f.name.startswith('~$')]
        
        if excel_files:
            print(f"未找到指定文件，发现以下Excel文件:")
            for i, f in enumerate(excel_files, 1):
                print(f"  {i}. {f.name}")
            
            choice = input("\n请输入文件编号（或按Enter退出）: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(excel_files):
                excel_file = excel_files[int(choice) - 1]
            else:
                print("未选择文件，退出")
                sys.exit(1)
        else:
            print(f"错误: 未找到文件 {excel_file}")
            sys.exit(1)
    
    check_consistency(excel_file, traffic_model)
