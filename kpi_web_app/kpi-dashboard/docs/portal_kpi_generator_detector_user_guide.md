# KPI Portal User Guide

本文覆盖 Portal 项目下两个模块的基础使用方法：

- `kpi-anomaly-detector`
- `kpi-generator`

同时覆盖不依赖 Portal 前端时的独立使用方法，包括当前公开可用的 CLI 接口。

## 1. 适用目录

- Portal 仓库: `kpi-dashboard`
- Detector 仓库: `kpi-anomaly-detector`
- Generator 仓库: `kpi-generator`

推荐目录布局:

- `kpi_web_app/kpi-dashboard`
- `kpi_web_app/kpi-anomaly-detector`
- `kpi_web_app/kpi-generator`

## 2. Portal 快速开始

在 `kpi-dashboard` 目录下执行:

1. `pip install -r requirements.txt`
2. `python app.py`

启动后访问:

- `http://127.0.0.1:8010`

Portal 中与本文相关的两个模块入口:

- `KPI Anomaly Detector`
- `KPI Generator`

## 3. Portal 模块一: KPI Anomaly Detector

### 3.1 这个模块做什么

该模块用于上传 KPI Excel 文件并运行异常检测，输出 HTML 报告、Excel 报告和 JSON 数据结果。

### 3.2 页面输入项

- `Choose files`: 支持一次选择一个或多个 `.xlsx` 文件
- `Treat upload as Base file`: 将当前上传文件作为 Base file 处理

### 3.3 文件名要求

Detector 在 Portal 和独立 CLI 中都会校验文件名。文件名必须符合:

- `Date_Build_Env_Scenario_otherinfo.xlsx`

核心规则:

- `Date`: 第一个 token
- `Build`: Env 之前的 token block
- `Env`: 第一个以 `Txxx` 或 `Txxxx` 开头的 token
- `Scenario`: 从第一个 `UE` token 开始，到第一个 `csv` token 之前结束
- `otherinfo`: 第一个 `csv` token 及其后续内容

示例:

- `exec20260325T120349_SBTS26R3.ENB.9999.260319.000005_T813.SCF.T813.gNB.25R3.20260224_7UE_DL_Burst_1csv.xlsx`
- `0129.1_26R2.0126.7_T076.SCF_7UEs_SFTPDL_1csv8run.xlsx`

### 3.4 Base file 与普通文件区别

- Base file: 与相同 `Env + Scenario` 的全部历史记录比较
- 普通文件: 与相同 `Env + Scenario` 的历史比较，但会排除相同 `Build` 的历史记录

### 3.5 运行后可以做什么

在 Portal 历史列表或任务详情页中可以:

- 查看状态: `queued` / `running` / `completed` / `failed`
- 查看 HTML 报告
- 下载 Excel 报告
- 下载 JSON 数据
- 查看 stdout / stderr
- `Rerun`
- `Cancel` 正在运行的任务
- `Delete` 已结束任务

### 3.6 输入 Excel 的最小要求

Detector 输入 Excel 至少应包含:

- `Code`
- `KPI Name` 可选
- 一个或多个以 `Txxx.*` 或 `Txxxx.*` 命名的数据列

例如:

- `Code`
- `KPI Name`
- `T080.20260403_010203`
- `T813.20260403_020203`

## 4. Portal 模块二: KPI Generator

Portal 中该模块现在包含两个子功能:

- `Generate Compass KPI report`
- `Convert Scout report to Compass format`

### 4.1 Generate Compass KPI report

#### 页面输入项

- `Template set`: 从 Compass 拉取的模板集合，可为空
- `template_names`: 手工补充模板名，可为空，但必须和 `Template set` 二选一或两者同时使用
- `Build`
- `Env`
- `Scenario`
- `report_timestamps_list`: 通过页面按钮创建，不再直接手输原始列表
- `Auto run detector`
- `Auto run detector as base file`

#### template_names 规则

支持以下分隔方式:

- `;`
- `；`
- `,`
- `，`
- `、`
- 换行
- 多个连续空格或 `Tab`

单个普通空格会保留，因此带空格的 template name 不会被错误拆开。

#### 时间段规则

Portal 页面通过 `Create report timestamps` 创建一个或多个时间组。每个时间组包含:

- `report_start_time`
- `report_end_time`
- `split_interval`

Portal 会把所有时间组展开并合并成最终的 `report_timestamps_list`。

#### 未来时间规则

如果最终合并后的最后一个区间结束时间仍在未来，Portal 不会立即调用 Compass，而是等待:

- `latest_end_time + 40 minutes (server local time)`

任务列表和任务详情页会显示倒计时。

#### 最终输出

成功后会生成一个最终 `.xlsx` 报告，并在 Portal 任务页中提供:

- 请求 JSON
- 结果 JSON
- stdout / stderr
- 最终报告下载
- 自动触发的 detector 任务链接（如果启用）

### 4.2 Convert Scout report to Compass format

#### 页面输入项

- `Scout report`: 原始 Scout `.xlsx`
- `Build`
- `Env`
- `Scenario`
- `DistName filters`
- `Auto run detector`
- `Auto run detector as base file`

#### 当前固定行为

- Portal 固定读取 Scout 工作簿中的 `Chart Data` sheet
- 前端不再暴露 `sheet name` 输入框

#### 转换逻辑

Portal 会调用 `kpi-generator/kpi_generator.py` 的 scout conversion 模式，完成以下处理:

- 读取 `Chart Data`
- 解析 `DistName filters`，支持 `;`、`；`、`,`、`，`、换行和多个连续空格
- 对每个单独的 DistName filter 做模糊匹配
- 把时间戳透视成数据列
- 把每个 filter 的结果写入同一个输出 Excel 的不同 sheet
- sheet 名默认取对应的单个 DistName filter，如果超过 Excel 31 字符限制或存在非法字符，Portal 会自动清洗；如果重名，会自动追加序号
- 输出文件名按原 detector 风格生成，但会在后缀追加 `scout`

输出结果中不再包含旧的 `Type` 列。

#### 输出与兼容性

- Scout conversion 生成的是单个 Excel 文件，但可能包含多个 sheet
- Job 详情页会展示每个 sheet 对应的 filter、匹配数、时间列数和输出行数
- 原先普通 generator 产物和单 sheet Compass detector 文件命名不变
- 原先 detector 对非 `*_scout.xlsx` 文件的处理逻辑不变

## 5. 独立使用: kpi-anomaly-detector

### 5.1 适用场景

适合不通过 Portal，直接在命令行中运行 detector。

工作目录:

- `kpi-anomaly-detector`

### 5.2 CLI 接口

当前公开入口脚本:

- `python scripts/run_detector.py`

支持的用法:

1. 交互模式
   `python scripts/run_detector.py`
2. 直接分析单个文件
   `python scripts/run_detector.py path\to\your_file.xlsx`
3. 分析单个文件且不生成 HTML
   `python scripts/run_detector.py path\to\your_file.xlsx --no-html`
4. 交互模式且不生成 HTML
   `python scripts/run_detector.py --no-html`

### 5.3 输入要求

- 文件必须是 `.xlsx`
- 文件名必须符合 detector 的命名规则
- Excel 内至少有 `Code` 和一个或多个 `Txxx.*` / `Txxxx.*` 数据列

### 5.4 输出位置

主要输出目录:

- `reports/`

常见输出:

- `*_trend_viewer.html`
- `*_analysis.xlsx`
- `kpi_history_records.json`

如果输入文件名带 `scout` 后缀，并且 Excel 含多个 sheet，则 detector 会进入 scout 多 sheet 模式:

- 遍历每个 sheet，分别做独立检测
- 每个 sheet 生成一份单独 HTML 报告，文件名追加 `sheet_name`
- 额外生成一个总 HTML summary，用于汇总所有 sheet 的检测结果并跳转到对应 detail HTML
- 使用独立历史文件 `kpi_history_records_scout.json`
- scout 历史按 `Env + Scenario + sheet_name` 分组，不会污染原有单 sheet Compass 历史
- `kpi_history_records_scout.json`

### 5.5 适合 CLI 使用者的建议

- 先用一个文件跑通命名规则和列格式
- 如果只想验证 Excel 结果，可加 `--no-html`
- 如果文件不在 `data/` 目录，可以直接传绝对路径或相对路径

## 6. 独立使用: kpi-generator

### 6.1 适用场景

适合直接在命令行里跑 Compass KPI 报告生成，或做 Scout 转 Compass 转换。

工作目录:

- `kpi-generator`

主入口脚本:

- `python kpi_generator.py`

该脚本有两个主要 CLI 模式:

- 标准生成模式: `--request-json`
- Scout 转换模式: `--scout-report`

### 6.2 CLI 模式一: 标准生成模式

#### 命令格式

1. `python kpi_generator.py --request-json request.json --output-dir outputs`
2. `python kpi_generator.py --request-json request.json --output-dir outputs --result-json result.json`
3. `python kpi_generator.py --request-json request.json --output-dir outputs --result-json result.json --verbose`

#### request.json 必填字段

- `build`
- `environment`
- `scenario`
- `report_timestamps_list`
- `template_set_name` 或 `template_names` 至少提供一个

#### request.json 可选字段

- `template_set_name`
- `template_names`
- `timestamp_delta_minutes`
- `test_line`

#### request.json 示例

```json
{
  "template_set_name": "ivy_25R3_example_template_set",
  "template_names": "ExtraTemplateA; Extra Template B",
  "build": "SBTS26R3.ENB.9999.260319.000005",
  "environment": "T813.SCF.T813.gNB.25R3.20260224",
  "scenario": "7UE_DL_Burst",
  "report_timestamps_list": [
    ["2026-04-01 11:24:52", "2026-04-01 12:24:52"],
    ["2026-04-01 12:24:52", "2026-04-01 13:24:52"]
  ]
}
```

#### 字段说明

- `template_set_name`: 直接指定 Compass template set 名称
- `template_names`: 手工模板名，支持与 `template_set_name` 合并使用
- `report_timestamps_list`: 需要是 `[start_time, end_time]` 的列表
- `timestamp_delta_minutes`: 可选。若提供，后端会再按该间隔继续切分时间段
- `test_line`: 可选。不传时会根据 `environment` 自动映射

#### 输出内容

- 最终生成的 `.xlsx` 报告写入 `--output-dir`
- 若提供 `--result-json`，会写入结构化结果 JSON
- 标准输出会持续输出进度事件

### 6.3 CLI 模式二: Scout 转换模式

#### 命令格式

1. `python kpi_generator.py --scout-report input.xlsx --dist-name T813 --build SBTS26R3.ENB.9999.260319.000005 --environment T813.SCF.T813.gNB.25R3.20260224 --scenario 7UEs_SFTPDL`
2. `python kpi_generator.py --scout-report input.xlsx --dist-name T813 --build SBTS26R3.ENB.9999.260319.000005 --environment T813.SCF.T813.gNB.25R3.20260224 --scenario 7UEs_SFTPDL --output-path out.xlsx --result-json result.json`
3. `python kpi_generator.py --scout-report input.xlsx --dist-name T813 --build SBTS26R3.ENB.9999.260319.000005 --environment T813.SCF.T813.gNB.25R3.20260224 --scenario 7UEs_SFTPDL --verbose`

#### 必填参数

- `--scout-report`
- `--dist-name`
- `--build`
- `--environment`
- `--scenario`

#### 可选参数

- `--output-path`
- `--result-json`
- `--verbose`

#### 当前固定行为

- 脚本固定读取 `Chart Data`
- `--sheet-name` 参数仍保留兼容，但已经隐藏，且即使传入其他值也会被忽略

#### 输出内容

- 生成一个 Compass 风格的 `.xlsx` 报告
- 结果 sheet 名称为 `KPI Report`
- 若提供 `--result-json`，会输出转换摘要 JSON

### 6.4 CLI 使用建议

- 先用 `--result-json` 跑一遍，确认参数和结果摘要都符合预期
- `environment` 建议直接使用能体现 `Txxx` 或 `Txxxx` 的原始环境字符串
- `build`、`environment`、`scenario` 会进入最终文件名，建议使用规范命名

## 7. 常见问题

### 7.1 Generator 标准模式里 `template_set_name` 和 `template_names` 怎么选

- 只用 Compass 模板集合: 仅传 `template_set_name`
- 只用手工模板: 仅传 `template_names`
- 两者一起: 同时传，系统会合并去重

### 7.2 Scout conversion 还能不能改 sheet name

当前不建议，也不会生效。

- Portal 已固定为 `Chart Data`
- CLI 里即使传 `--sheet-name`，也会被忽略并回退到 `Chart Data`

### 7.3 Detector 为什么会拒绝文件

最常见原因:

- 文件扩展名不是 `.xlsx`
- 文件名不符合命名规则
- Excel 中缺少 `Code` 或缺少 `Txxx.*` / `Txxxx.*` 数据列

## 8. 推荐使用顺序

### 8.1 想要最快上手

1. 先用 Portal 跑一遍
2. 确认输入格式和输出结果都符合预期
3. 再把同样参数转成 CLI 命令做批量化

### 8.2 想做自动化

1. `kpi-generator` 使用 `--request-json` 或 `--scout-report` 模式
2. 产出 Excel 后，再用 `python scripts/run_detector.py your_file.xlsx`
3. 需要结构化状态时，优先同时输出 `--result-json`