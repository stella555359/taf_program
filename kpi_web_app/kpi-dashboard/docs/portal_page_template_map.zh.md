# Portal 页面到模板文件映射

## 1. 文档目的

本文档把每个 Portal 页面对应到模板文件、路由、按钮动作以及前端回调链路。

## 2. 全局布局

### 共享外壳

- 模板：`portal/templates/base.html`
- 职责：
  - 统一 HTML 外壳
  - 全局样式引入
  - 顶部导航
  - flash 消息展示
- 主要导航目标：
  - `portal.home`
  - `kpi_detector.index`
  - `kpi_generator.index`
  - `kpi_traffic_model.index`

## 3. 首页

### 页面映射

- 路由：`GET /`
- handler：`portal.home`
- 模板：`portal/templates/home.html`
- 后端数据源：`repo_registry.get_module_cards()`

### 主要动作

- `Open module` 按钮
  - 动作：`url_for(module.route_name)`
  - 结果：进入对应模块首页

## 4. Detector 页面

### Detector 首页

- 路由：`GET /kpi-anomaly-detector/`
- handler：`kpi_detector.index`
- 模板：`portal/templates/modules/kpi_detector.html`

### 主要表单和按钮

- 上传表单
  - 动作：`POST /kpi-anomaly-detector/submit`
  - 字段：`files`、`is_base_file`、文件名覆盖隐藏字段
- 过滤表单
  - 动作：`GET /kpi-anomaly-detector/`
  - 字段：`q`、`status`、`release`、`environment`、`scenario`、`page`
- 批量重跑
  - 动作：`POST /kpi-anomaly-detector/jobs/bulk/rerun`
- 批量删除
  - 动作：`POST /kpi-anomaly-detector/jobs/bulk/delete`
- 行内文件名链接
  - 动作：`GET /kpi-anomaly-detector/jobs/<job_id>`
- 行内重跑
  - 动作：`POST /kpi-anomaly-detector/jobs/<job_id>/rerun`
- 行内取消
  - 动作：`POST /kpi-anomaly-detector/jobs/<job_id>/cancel`
- 行内删除
  - 动作：`POST /kpi-anomaly-detector/jobs/<job_id>/delete`

### 前端回调链路

- 文件名校验回调
  - JS 通过 `fetch()` 调用 `POST /kpi-anomaly-detector/validate-upload-filenames`
  - 若文件名不符合规则，则弹出覆盖对话框
  - 用户填写 Env 和 Scenario
  - 脚本写入隐藏字段后继续提交
- 过滤联动回调
  - 页面使用 `scenario_map` 在 release 或 environment 变化时重建 scenario 选项
- 可见作业自动刷新回调
  - JS 轮询 `GET /kpi-anomaly-detector/api/jobs/<job_id>`
  - 刷新列表行状态、artifact 区域和按钮区
  - 通过 `window.setTimeout()` 循环触发

### Detector 详情页

- 路由：`GET /kpi-anomaly-detector/jobs/<job_id>`
- handler：`kpi_detector.job_detail`
- 模板：`portal/templates/modules/kpi_detector_job.html`

### 主要动作

- 返回模块首页
- 再次运行
- 取消
- 删除
- 下载 stdout、stderr
- 打开 HTML 报告、下载 Excel、下载 JSON
- 打开分 sheet HTML 和 Excel
- 打开关联 job

### 前端回调链路

- 详情自动刷新回调
  - JS 轮询 `GET /kpi-anomaly-detector/api/jobs/<job_id>`
  - 运行中定时刷新页面
  - 当状态进入终态时停止轮询或直接重载

## 5. Generator 页面

### Generator 首页

- 路由：`GET /kpi-generator/`
- handler：`kpi_generator.index`
- 模板：`portal/templates/modules/kpi_generator.html`

### 主要表单和按钮

- generator 提交表单
  - 动作：`POST /kpi-generator/jobs`
  - 用途：按 template set 或 template_names 生成报表
- scout conversion 表单
  - 动作：`POST /kpi-generator/jobs`
  - 用途：把 scout workbook 转成 Compass 风格输出
- 过滤表单
  - 动作：`GET /kpi-generator/`
- 历史记录链接
  - 动作：`GET /kpi-generator/jobs/<job_id>`
- 行内重跑、取消、删除

### 前端回调链路

- 模板预览回调
  - 浏览器端把 template set 和手填 `template_names` 合并预览
- 时间片构造回调
  - 用户多次创建时间范围
  - 脚本展开并合并区间
  - 提交前写入隐藏字段 `report_timestamps_list`

### Generator 详情页

- 路由：`GET /kpi-generator/jobs/<job_id>`
- handler：`kpi_generator.job_detail`
- 模板：`portal/templates/modules/kpi_generator_job.html`

### 主要动作

- 返回模块页
- 打开关联 detector job
- 重跑
- 取消
- 删除
- 下载 source 和 final report
- 页面内打开 request、result、stdout、stderr、final report

### 前端回调链路

- 详情自动刷新回调
  - JS 轮询 `GET /kpi-generator/api/jobs/<job_id>`
  - 排队中或运行中定时刷新页面
  - 倒计时区域由前端定时逻辑刷新

## 6. Traffic Model 页面

### Traffic Model 首页

- 路由：`GET /kpi-traffic-model/`
- handler：`kpi_traffic_model.index`
- 模板：`portal/templates/modules/kpi_traffic_model.html`

### 主要表单和按钮

- env 解析表单
  - 动作：`GET /kpi-traffic-model/`
  - 字段：`env`
- 工作流提交表单
  - 动作：`POST /kpi-traffic-model/jobs`
  - 字段包括 env、选中的 UE、运行参数、stage 与 traffic item 配置
- 历史 job 链接
- 预览 artifact 下载链接

### 前端回调链路

- 当前首页基本以服务端渲染为主
- 未观察到显著的首页轮询逻辑
- env 解析结果通过页面重新渲染返回

### Traffic Model 详情页

- 路由：`GET /kpi-traffic-model/jobs/<job_id>`
- handler：`kpi_traffic_model.job_detail`
- 模板：`portal/templates/modules/kpi_traffic_model_job.html`

### 主要动作

- 返回模块页
- 删除
- 下载 artifact
- 打开关联 job

### 前端回调链路

- 自动刷新回调
  - 对排队中或运行中的 job，页面通过 `window.setTimeout()` 后执行 `window.location.reload()`
  - 当前模板中的刷新间隔为 4 秒

## 7. 总结

Portal 的前端模式是“先服务端渲染，再少量脚本增强”。

主要回调模式只有三类：

- 表单提交到 blueprint
- 通过 `fetch()` 做校验或状态轮询
- 用 `window.setTimeout()` 做定时刷新或倒计时