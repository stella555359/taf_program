# KPI Portal Quick Start

这是一页式 quick start，适合直接发给最终使用者。

覆盖模块:

- `kpi-anomaly-detector`
- `kpi-generator`

## 1. 打开 Portal

在 `kpi-dashboard` 目录启动 Portal:

1. `pip install -r requirements.txt`
2. `python app.py`

默认访问地址:

-  https://10.57.159.149/kpi-dashboard/

## 2. KPI Anomaly Detector 快速使用

### 你需要准备什么

- 一个或多个 `.xlsx` 文件
- 文件名必须符合: `Date_Build_Env_Scenario_otherinfo.xlsx`
  （对上传了不符合规则的文件名已经另外加了一层rename功能，会根据你输入的Build,Env,Scenario生成符合规定的xlsx文件名）
- Excel文件内容里至少包含:
  - `Code`
  - 可选 `KPI Name`
  - 一个或多个 `Txxx.*` 或 `Txxxx.*` 数据列

### 怎么用

1. 打开 `KPI Anomaly Detector`
2. 点击 `Choose files`
3. 选择一个或多个 `.xlsx`
4. 如需把当前文件当作基线，勾选 `Treat upload as Base file`
   勾选了代表所有包的所有测试结果都会被当历史数据
   不勾选代表同一个包的不同round的测试不会被当作历史数据，只跟之前跑的其他包的历史数据作比较
5. 点击 `Run detector`

### 结果在哪里看

任务完成后可在任务列表或任务详情页查看:

- HTML 报告
- Excel 报告
- JSON 数据
- stdout / stderr

## 3. KPI Generator 快速使用

Portal 中有两个入口:

- `Generate Compass KPI report`
- `Convert Scout report to Compass format`

### 3.1 Generate Compass KPI report

#### 你需要填写什么

- `Template set` 和/或 `template_names`
- `Build`
- `Env`
- `Scenario`
- 一个或多个服务器时间段

#### Template set 固定选项

- 不选
- `ivy_26R1_vdt`
- `ivy_26R2_vdt`

不再从 Compass 动态读取 template set。

这个位置现在支持两种用法:

- 直接选择建议值：不选、`ivy_26R1_vdt`、`ivy_26R2_vdt`
- 如果建议值里没有你要的，也可以直接手工输入任意 template set 名字

#### 时间段怎么填

不要直接手写 `report_timestamps_list`。

正确方式:

1. 点击 `Create report timestamps`
2. 填 `report_start_time`
3. 填 `report_end_time`
4. 选 `split_interval`
5. 点击 `Create`
6. 重复以上步骤可添加多个时间组

Portal 会自动把所有时间组合并成最终的 `report_timestamps_list`。

#### template_names 怎么填

支持这些分隔方式:

- `;`
- `；`
- `,`
- `，`
- `、`
- 换行
- 多个连续空格

单个普通空格会保留，所以带空格的模板名不会被拆开。

#### 特别说明

- 如果最后一个时间区间的结束时间还在未来，Portal 会等到 `结束时间 + 40 分钟（按服务器时间）` 再开始调用 Compass
- 可以勾选 `Auto run detector`，生成成功后自动把结果送去 detector

### 3.2 Convert Scout report to Compass format

#### 你需要填写什么

- `Scout report` (`.xlsx`)
- `Build`
- `Env`
- `Scenario`
- `DistName filter`

#### 特别说明

- Portal 固定读取 Scout 文件中的 `Chart Data`
- 页面上不需要再填 `sheet name`
- 转换结果不再包含旧的 `Type` 列

## 4. 不用 Portal 时怎么跑

### Detector CLI

在 `kpi-anomaly-detector` 目录:

1. `python scripts/run_detector.py`
2. `python scripts/run_detector.py your_file.xlsx`
3. `python scripts/run_detector.py your_file.xlsx --no-html`

### Generator CLI

在 `kpi-generator` 目录:

标准生成模式:

1. `python kpi_generator.py --request-json request.json --output-dir outputs`
2. `python kpi_generator.py --request-json request.json --output-dir outputs --result-json result.json`

Scout 转换模式:

1. `python kpi_generator.py --scout-report input.xlsx --dist-name T813 --build SBTS26R3.ENB.9999.260319.000005 --environment T813.SCF.T813.gNB.25R3.20260224 --scenario 7UEs_SFTPDL`

## 5. 常见问题

### Portal 打不开

- 默认端口是 `8010`，不是 `8088`

### Detector 拒绝上传

通常是以下原因之一:

- 不是 `.xlsx`
- 文件名不符合规则
- Excel 缺少 `Code` 或缺少 `Txxx.*` / `Txxxx.*` 数据列

### Generator 不能提交

通常是以下原因之一:

- `template_set_name` 和 `template_names` 都没填
- 没有创建任何时间段
- `Build` / `Env` / `Scenario` 缺失

### Scout conversion 为什么没有 sheet name

- 因为当前固定读取 `Chart Data`，不再需要用户输入
- 现在 `DistName filters` 支持一次输入多个值
- Portal 会把每个 filter 的结果分别写入同一个输出 Excel 的不同 sheet
- 输出文件名会额外带上 `scout` 后缀

### Scout conversion 最短使用方式

1. 上传标准 Scout `.xlsx`
2. 填 `Build`、`Env`、`Scenario`
3. 在 `DistName filters` 里输入一个或多个 filter
4. 使用 `;`、`,`、换行或多个连续空格分隔多个 filter
5. 运行后在同一个 Excel 中查看多个 sheet

### Scout 自动 detector 会发生什么

1. 如果生成文件名带 `scout` 后缀，detector 会进入 scout 多 sheet 模式
2. 多个 sheet 会分别分析
3. Portal artifact 上默认显示总 HTML summary
4. 总 HTML 里可以打开每个 sheet 对应的 detail HTML