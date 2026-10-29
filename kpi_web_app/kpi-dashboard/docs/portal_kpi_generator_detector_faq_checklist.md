# KPI Portal FAQ + Troubleshooting Checklist

这是一线使用者排错短页，只保留最常见问题和最短排查动作。

覆盖模块:

- `kpi-anomaly-detector`
- `kpi-generator`

## 1. Portal 打不开

### 先看这 3 项

1. 是否已经在 `kpi-dashboard` 目录执行了 `python app.py`
2. 浏览器访问的是否是 `http://127.0.0.1:8010`
3. 当前机器上 `8010` 端口是否被别的程序占用

### 如果还不行

1. 看启动终端里有没有报错
2. 检查是否设置了 `KPI_DASHBOARD_PORT`

## 2. Detector 上传失败

### 最常见原因

1. 上传的不是 `.xlsx`
2. 文件名不符合 `Date_Build_Env_Scenario_otherinfo.xlsx`
3. Excel 缺少 `Code` 列
4. Excel 没有任何 `Txxx.*` / `Txxxx.*` 数据列

### 最短排查动作

1. 确认文件扩展名是 `.xlsx`
2. 检查文件名里是否包含 `Build`、`Txxx/Txxxx`、`Scenario`、`csv`
3. 打开 Excel 看列名里是否有 `Code`
4. 打开 Excel 看是否至少有一列像 `T080.xxxx` 或 `T813.xxxx`

## 3. Detector 任务一直跑或失败

### 先看哪里

1. 打开任务详情页
2. 看 `stdout`
3. 看 `stderr`

### 常见原因

1. 输入文件过大
2. 历史数据过多
3. 文件内容格式不完整

### 快速判断

1. 如果 `stderr` 明确写缺列或文件名错误，先修输入文件
2. 如果长时间无输出，先怀疑文件体量或环境卡住

## 4. Generator 提交不了

### 最常见原因

1. `Template set` 和 `template_names` 都没填
2. 没有创建任何时间段
3. `Build` / `Env` / `Scenario` 没填
4. 时间格式不对

### 最短排查动作

1. 确认 `Template set` 或 `template_names` 至少填了一个
2. 确认页面里已经点击过 `Create report timestamps`
3. 确认预览框里已经有最终 `report_timestamps_list`
4. 确认时间格式是 `YYYY-MM-DD HH:MM:SS`

## 5. Generator 提交后一直不开始

### 先确认这是不是正常现象

如果最后一个时间区间结束时间还在未来，Portal 会等到:

- `最后结束时间 + 40 分钟（按服务器时间）`

才开始真正调用 Compass。

### 最短排查动作

1. 打开任务详情页
2. 看是否有倒计时或 waiting 状态
3. 如果有倒计时，通常不是故障，是正常等待

## 6. Template set 有了，但生成还是不对

### 常见原因

1. 手工 `template_names` 又额外加了一些模板
2. 输入了重复模板名
3. 分隔符使用不规范

### 最短排查动作

1. 看页面上的 `Template names from selected template set`
2. 看页面上的 `Merged final template_names`
3. 以页面最终 merged preview 为准，不要只看原始输入框

## 7. template_names 输入后没有按预期拆分

### 当前支持的分隔方式

1. `;`
2. `；`
3. `,`
4. `，`
5. `、`
6. 换行
7. 多个连续空格

### 注意

- 单个普通空格不会拆分
- 这是为了保留带空格的 template name

## 8. Scout conversion 跑不了

### 最常见原因

1. 上传的不是 `.xlsx`
2. `DistName filters` 没填
3. 源文件里没有 `Chart Data`
4. `Chart Data` 里缺少关键列

### 关键列

1. `DistName`
2. `EntryName`
3. `GroupName`
4. `TimeStamp`
5. `Value`

### 最短排查动作

1. 手工打开源文件，确认有 `Chart Data`
2. 确认关键列名拼写完全正确
3. 确认每个 `DistName filter` 都能匹配到目标行

### 多个 DistName filter 怎么填

支持以下分隔方式:

1. `;`
2. `；`
3. `,`
4. `，`
5. 换行
6. 多个连续空格

单个普通空格不会拆分，用于保留本身带空格的 filter。

## 9. 为什么 Scout conversion 页面没有 sheet name

因为当前行为已经固定:

1. Portal 固定读取 `Chart Data`
2. 不再需要用户手填 `sheet name`
3. CLI 中即使传其他 `sheet name`，也会被忽略并回退到 `Chart Data`
4. 如果输入多个 `DistName filter`，Portal 会把结果写到多个输出 sheet，而不是读取多个输入 sheet

## 10. 为什么 detector 现在只显示一个总 HTML

如果上传的是带 `scout` 后缀的文件，且文件中含多个 sheet，这是设计行为:

1. detector 会对每个 sheet 单独生成 detail HTML
2. Portal artifact 只展示总 HTML summary
3. 总 HTML 内提供进入每个 sheet detail HTML 的入口
4. 这样可以避免 job artifact 区域被多个 HTML 链接污染

## 11. 自动触发 detector 没有跑起来

### 先看这 3 项

1. 是否勾选了 `Auto run detector`
2. generator 任务是否真的成功完成
3. 最终生成的文件名是否符合 detector 规则

### 最短排查动作

1. 打开 generator 任务详情
2. 看有没有 linked detector job
3. 如果没有，先看 generator 自己是否 completed

## 12. 最小自检顺序

遇到问题时，按这个顺序查最快:

1. 看页面 flash message
2. 看任务状态
3. 看任务详情页的 `stdout` / `stderr`
4. 回头检查输入文件名
5. 回头检查 Excel 列名
6. 回头检查 Portal 页面预览区内容

## 13. 什么时候该找开发/运维

满足下面任意一条，建议升级给开发/运维:

1. Portal 根本起不来
2. Compass 登录持续失败
3. 同一输入以前能跑、现在突然全部失败
4. `stdout` / `stderr` 内容看不懂或像代码异常
5. 任务目录、日志或输出文件明显异常增长