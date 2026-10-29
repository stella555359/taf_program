# Portal 新增第四模块接入 SOP

## 1. 文档目的

本文档定义“往 Portal 里新增第四个模块”的标准接入流程，目的是让后续扩展保持和当前架构一致。

## 2. 接入前提

新模块负责人至少需要提供：

- 模块名称和 key
- 仓库路径
- readme 路径
- 入口候选文件
- 执行模型
- 输入契约
- 输出 artifact
- 支持的生命周期动作
- 状态模型

## 3. 接入检查清单

新模块必须接入以下层：

1. repository registry
2. adapter 层
3. contracts 与 schemas
4. blueprint 层
5. templates
6. 启动恢复逻辑
7. artifact 映射和关联链路
8. 文档与测试

## 4. 标准步骤

### 第 1 步：注册模块元数据

修改 `portal/services/repo_registry.py`，补充：

- `key`
- `title`
- `summary`
- `route_name`
- `repo_path`
- `readme_path`
- `entry_candidates`

建议：

- key 命名风格保持与现有模块一致，例如 `kpi-anomaly-detector`

### 第 2 步：定义输入 schema

如果模块输入是结构化的，就在 `portal/schemas/input_models.py` 中增加 dataclass。

建议：

- 复用 `PortalJobCommonFields`
- 复用 `PortalRuntimeOptions`
- 增加 `from_form()` 或类似构造方法
- 用户可见校验失败统一抛 `InputValidationError`

### 第 3 步：实现 adapter

在 `portal/adapters/` 下新增适配器文件，例如 `kpi_new_module.py`。

最小职责：

- `describe_module()`
- `sample_command()`
- `list_jobs()`
- `get_job()`
- `submit(...)` 或 `submit_request(...)`
- `artifact_path()`
- `delete()`

如果模块支持，再补：

- `query_jobs()`
- `filter_options()`
- `rerun()`
- `cancel()`
- `recover_startup_jobs()`

### 第 4 步：定义 job 字段和 artifact

以 `job_store.create_job()` 的公共字段为基础，在 adapter 中补充模块自己的业务字段，例如：

- 业务上下文字段
- 进度字段
- 结果路径
- 报告路径
- 下游 job 关联 ID

同时确保 artifact 能进入 `platform_artifacts` 和 `platform_download_artifacts`。

### 第 5 步：实现 blueprint

在 `portal/blueprints/` 下新增 blueprint 文件，例如 `kpi_new_module.py`。

最小路由建议：

- 模块首页
- submit 接口
- job 详情页
- 状态 API
- artifact 下载接口
- delete 接口

可选路由：

- rerun
- cancel
- 过滤 API
- preview API

### 第 6 步：注册 blueprint

在 `portal/app_factory.py` 中注册新 blueprint，保证应用启动时可用。

同时确认 URL prefix 部署场景不受影响。

### 第 7 步：补模板

在 `portal/templates/modules/` 下至少新增：

- `<module>.html`
- `<module>_job.html`

建议：

- 首页负责提交和历史记录
- 详情页负责状态、artifact、events、links、logs

### 第 8 步：更新导航

修改 `portal/templates/base.html`，把新模块加到顶部导航。

首页卡片通常会因 registry 自动出现，除非有额外展示逻辑。

### 第 9 步：补统一契约

如果页面要依赖统一能力描述，继续对齐：

- `ModuleCapabilityContract`
- `JobContract`
- `SummaryContract`

### 第 10 步：补启动恢复

如果模块会启动后台任务，需要实现 `recover_startup_jobs()` 并接入 Portal 启动恢复流程。

### 第 11 步：补测试

最少建议有：

- schema 校验测试
- adapter 提交测试
- blueprint 路由测试
- artifact 接口测试
- 删除和重跑行为测试

### 第 12 步：补文档

新增模块后需要同步更新：

- Portal 架构说明
- Portal API 契约
- 页面到模板映射
- 必要时补用户指南

## 5. 参考实现

按复杂度可参考：

- 最轻量参考：`kpi_traffic_model`
- 中等参考：`kpi_generator`
- 功能最完整参考：`kpi_detector`

## 6. 常见错误

应避免：

- 把执行逻辑直接写进 blueprint
- 不做 schema 校验，直接到处使用 `request.form`
- artifact 没注册到 job store 就直接暴露
- 模板依赖未经标准化的 adapter 字段
- 长任务忘记补启动恢复
- 新 blueprint 忘记注册

## 7. 完成标准

满足以下条件才算接入完成：

- 首页卡片已出现
- 顶部导航可见
- 可以从模块首页提交 job
- job 能写入 SQLite
- 详情页渲染正常
- artifact 可以下载
- 生命周期动作符合设计
- 文档和测试已经同步更新

## 8. 结论

最稳妥的扩展路径始终相同：先注册模块元数据，再用 schema 规范输入，用 adapter 隔离模块差异，让 blueprint 保持薄层，并继续复用现有 job store 模型。