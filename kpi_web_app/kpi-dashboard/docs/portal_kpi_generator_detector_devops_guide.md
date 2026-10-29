# KPI Portal DevOps Guide

本文面向开发、测试和运维同学，聚焦这两个模块在 Portal 中的运行方式、依赖、输出目录、环境变量、常见故障与排查办法。

覆盖模块:

- `kpi-anomaly-detector`
- `kpi-generator`

## 1. 目录关系

推荐工作区布局:

- `kpi_web_app/kpi-dashboard`
- `kpi_web_app/kpi-anomaly-detector`
- `kpi_web_app/kpi-generator`

Portal 通过 sibling repository 方式调用另外两个仓库。

## 2. Portal 运行方式

### 启动命令

在 `kpi-dashboard` 目录:

1. `pip install -r requirements.txt`
2. `python app.py`

### 当前依赖

`kpi-dashboard/requirements.txt` 当前只声明:

- `Flask>=3.0,<4.0`

### 当前默认监听

Portal 当前默认配置来自 `app.py`:

- Host: `0.0.0.0`
- Port: `8010`
- Debug: 关闭

### Portal 环境变量

- `KPI_DASHBOARD_HOST`
- `KPI_DASHBOARD_PORT`
- `KPI_DASHBOARD_DEBUG`

示例:

1. `set KPI_DASHBOARD_PORT=8088`
2. `set KPI_DASHBOARD_DEBUG=1`
3. `python app.py`

## 3. Portal 作业目录

Portal 任务元数据和中间文件都写在:

- `kpi-dashboard/instance/jobs/`

具体模块目录:

- `kpi-dashboard/instance/jobs/kpi-anomaly-detector/`
- `kpi-dashboard/instance/jobs/kpi-generator/`

每个任务目录通常会包含:

- `job.json`
- 输入文件或请求文件
- `stdout.log`
- `stderr.log`
- `result.json`

## 4. kpi-anomaly-detector 依赖与输出

### Python 依赖

从 detector README 可确认的主要依赖:

- `pandas`
- `numpy`
- `scipy`
- `openpyxl`

建议 Python 版本:

- `3.8+`

### 关键目录

在 `kpi-anomaly-detector/scripts/kpi_detector/config.py` 中定义:

- 输入目录: `kpi-anomaly-detector/data`
- 输出目录: `kpi-anomaly-detector/reports`
- 文档目录: `kpi-anomaly-detector/docs`

### 常见输出

- `*_trend_viewer.html`
- `*_analysis.xlsx`
- `kpi_history_records.json`

### Detector 相关环境变量

- `KPI_DETECTOR_TIMEOUT_SECONDS`
- `KPI_HTML_HISTORY_LIMIT`

用途:

- `KPI_DETECTOR_TIMEOUT_SECONDS`: Portal 侧运行超时保护
- `KPI_HTML_HISTORY_LIMIT`: 控制 HTML 报告嵌入的历史深度

## 5. kpi-generator 依赖与输出

### Python 依赖

从 `kpi_generator.py` 当前 import 可确认的主要依赖:

- `pandas`
- `requests`
- `urllib3`
- `openpyxl`

### 外部系统依赖

Generator 标准模式依赖 Compass 网络访问，包括:

- 登录接口
- template set 查询接口
- 报告生成接口
- combine / compare / horizontal merge 接口

### Generator 相关环境变量

- `COMPASS_USERNAME`
- `COMPASS_PASSWORD`
- `KPI_GENERATOR_PYTHON`

说明:

- `COMPASS_USERNAME` / `COMPASS_PASSWORD`: 覆盖默认 Compass 账户
- `KPI_GENERATOR_PYTHON`: Portal 调 generator 时使用的 Python 可执行文件

### 输出位置

#### Portal 模式

Portal 下 generator 的结果通常写到:

- `kpi-dashboard/instance/jobs/kpi-generator/<job_id>/outputs/`

#### 独立 CLI 模式

- 标准生成模式写到 `--output-dir`
- Scout 转换模式默认写到输入文件同目录，或使用 `--output-path` 指定

## 6. CLI 接口说明

### Detector CLI

入口:

- `python scripts/run_detector.py`

支持:

1. 交互式目录选择
2. 单文件直接分析
3. `--no-html` 跳过 HTML 输出

### Generator CLI

入口:

- `python kpi_generator.py`

两种模式:

1. 标准生成模式: `--request-json`
2. Scout 转换模式: `--scout-report`

#### 标准生成模式最小命令

1. `python kpi_generator.py --request-json request.json --output-dir outputs`

#### Scout 转换模式最小命令

1. `python kpi_generator.py --scout-report input.xlsx --dist-name T813 --build SBTS26R3.ENB.9999.260319.000005 --environment T813.SCF.T813.gNB.25R3.20260224 --scenario 7UEs_SFTPDL`

#### 兼容但已隐藏的参数

- `--sheet-name`

当前行为:

- 参数仍保留兼容
- CLI help 中已隐藏
- 即使传入其他值，实际仍固定回退为 `Chart Data`

## 7. 常见报错与排查

### 7.1 Portal 页面打不开

检查:

1. `python app.py` 是否已启动
2. 当前端口是否为 `8010`
3. 是否被本地防火墙或占用端口拦截

排查方法:

1. 看启动终端输出
2. 检查 `KPI_DASHBOARD_PORT` 是否被覆盖

### 7.2 Detector 上传被拒绝

常见原因:

1. 文件不是 `.xlsx`
2. 文件名不符合 `Date_Build_Env_Scenario_otherinfo.xlsx`
3. 上传文件缺少 `Code` 列
4. 上传文件没有任何 `Txxx.*` / `Txxxx.*` 数据列

排查方法:

1. 先看 Portal flash message
2. 用独立 detector CLI 直接跑一次同一文件
3. 打开 Excel 检查列名是否被额外空格、换行或手工改坏

### 7.3 Detector 任务运行很久或超时

检查:

1. 输入文件是否过大
2. 历史记录是否过多
3. `KPI_DETECTOR_TIMEOUT_SECONDS` 是否过小

排查方法:

1. 看 Portal 任务详情的 `stdout` / `stderr`
2. 看 `kpi-anomaly-detector/reports/` 是否已经部分产出结果

### 7.4 Generator 提交失败

常见原因:

1. `template_set_name` 和 `template_names` 都为空
2. `build` / `environment` / `scenario` 缺失
3. `report_timestamps_list` 为空或格式不合法
4. `environment` 中没有可识别的 `Txxx` / `Txxxx`

排查方法:

1. 检查 Portal 表单和 preview 内容
2. 如果是 CLI，打开 `request.json` 逐项核对
3. 确认时间格式是 `YYYY-MM-DD HH:MM:SS`

### 7.5 Compass 登录或拉取模板失败

常见原因:

1. 网络不可达
2. Compass 用户名/密码无效
3. Compass 服务端暂时不可用

排查方法:

1. 检查 `stderr.log` 或 Portal 任务详情错误信息
2. 确认 `COMPASS_USERNAME` / `COMPASS_PASSWORD`
3. 在 Portal 页面查看 template set 加载错误提示

### 7.6 Scout conversion 结果异常

常见原因:

1. 源文件不是标准 Scout `.xlsx`
2. `Chart Data` 中缺少 `DistName` / `EntryName` / `GroupName` / `TimeStamp` / `Value`
3. 某个 `DistName filter` 没有匹配到任何数据
4. 同一组 `Group Name + Code + KPI Name + TimeStamp` 存在冲突值
5. 多个 filter 生成的 sheet 名在清洗后发生重名，Portal 会自动追加序号，这属于正常行为

排查方法:

1. 检查 `result.json`
2. 检查 `stderr.log`
3. 手工打开源文件确认 `Chart Data` 是否存在且列名正确
4. 如果输入了多个 `DistName filters`，逐个确认都能命中原始数据
5. 确认输出文件名末尾已包含 `scout`

### 7.7 Scout detector 多 sheet 结果和历史异常

说明:

1. 带 `scout` 后缀的文件会进入独立 detector 分支
2. 多 sheet 会分别检测
3. scout 历史写入 `kpi_history_records_scout.json`
4. 历史 key 为 `Env + Scenario + sheet_name`

排查方法:

1. 检查 Portal detector job 详情页中的 `Report mode` 是否为 `scout_multi_sheet`
2. 打开 detector summary HTML，确认每个 sheet 是否都有 detail HTML 入口
3. 检查 `kpi-anomaly-detector/reports/kpi_history_records_scout.json`
4. 确认 Excel 中每个 sheet 都满足 detector 的列要求

### 7.8 自动触发 detector 没有运行

检查:

1. 是否勾选了 `Auto run detector`
2. generator 任务是否真正完成
3. 输出文件名是否符合 detector 命名规则

排查方法:

1. 打开 generator 任务详情
2. 查看 linked detector job 是否生成
3. 检查 generator 产出的最终文件名是否规范

## 8. 运维建议

### 8.1 建议的最小检查项

每天至少检查:

1. Portal 进程是否存活
2. `kpi-dashboard/instance/jobs/` 是否异常膨胀
3. `kpi-anomaly-detector/reports/` 是否持续产出
4. Compass 连通性是否正常

### 8.2 清理建议

建议定期清理:

1. Portal 历史任务目录
2. 过旧的 detector HTML / Excel 报告
3. 体积异常大的 stdout / stderr 日志

### 8.3 变更建议

做代码升级前建议:

1. 先保留一份 `instance/jobs/` 备份
2. 记录当前 `COMPASS_USERNAME` / `COMPASS_PASSWORD` 配置来源
3. 用一个最小样例分别验证 detector 和 generator