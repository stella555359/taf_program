# 软考高级系统架构设计师论文集

## 1. 文档定位

本目录以 `jenkins_robotframework` 的真实架构和实施过程为案例，整理五篇软考高级系统架构设计师论文初稿。

这些稿件不是五篇互不相关的范文，而是围绕同一个项目建立的“母项目论文库”。进入考场后，应根据题目中的三个子问题选择最接近的一篇，并重新组织标题、理论段和实践段，不能不审题直接照搬。

按近年机考常见形式，本论文集以“120 分钟完成一篇、正文非空字符控制在 2200～2400”的训练目标编写，为个性化补充预留空间。实际题量、字数和作答规则应以当次考试说明与机考界面为准。

## 2. 母项目摘要

项目面向 5G GNB 自动化测试，把原来偏人工的 Jenkins 与 Robot Framework 执行方式，演进为一个轻量化测试平台。端到端主线为：

```text
Automation Portal
  -> Platform API
  -> Jenkins
  -> Robot Framework / Test Workflow Runner
  -> KPI Generator / Detector
  -> Artifact / Callback
  -> SQLite
  -> Portal Run Detail / AI Analysis
```

核心模块包括：

- `automation-portal`：React、TypeScript、Vite，负责测试提交和结果展示。
- `platform-api`：FastAPI、Pydantic、SQLite，负责运行契约、持久化、Jenkins 调度、回调和查询。
- `jenkins-integration`：JCasC、Job DSL、Pipeline 和 Python 辅助脚本，负责持续集成和长任务调度。
- `test-workflow-runner`：Python 工作流编排器，负责 stage/item 执行、资源锁、KPI 后处理和统一结果。
- AI Analysis Worker：基于运行证据生成日志摘要、根因建议和测试报告。

## 3. 五篇论文与考点覆盖

### 第一篇：分层架构与面向服务架构

文件：[paper-01-layered-and-service-oriented-architecture.md](paper-01-layered-and-service-oriented-architecture.md)

主考点：

- 软件架构风格
- 层次式架构
- 面向服务架构
- 企业应用集成
- 接口契约与松耦合
- 数据与文件分离

可改写题目：

- 论软件架构风格及其应用
- 论面向服务架构设计及其应用
- 论企业集成架构设计
- 论多数据源或异构系统集成

### 第二篇：基于架构的软件开发、评估与演化

文件：[paper-02-architecture-based-development-and-evolution.md](paper-02-architecture-based-development-and-evolution.md)

主考点：

- 系统建模
- 基于架构的软件开发方法
- 架构需求与质量属性场景
- 架构评估
- 架构演化与维护
- 构件化和可扩展设计

可改写题目：

- 论基于架构的软件开发方法及其应用
- 论软件架构评估
- 论软件架构演化
- 论基于构件的软件开发

### 第三篇：可靠性、容错与性能设计

文件：[paper-03-reliability-fault-tolerance-and-performance.md](paper-03-reliability-fault-tolerance-and-performance.md)

主考点：

- 软件可靠性
- 容错和故障隔离
- 并发与资源竞争
- 性能风险控制
- 可观测性与故障恢复

可改写题目：

- 论软件系统可靠性设计
- 论系统容错技术

高可用、负载均衡和完整性能测试在本文中只能作为演进方向，不能写成当前项目已经落地的实践。

### 第四篇：安全架构与保密性设计

文件：[paper-04-security-and-confidentiality-architecture.md](paper-04-security-and-confidentiality-architecture.md)

主考点：

- 安全架构
- 身份鉴别与访问控制
- 凭据和密钥管理
- 传输与存储安全
- 技术执行证据与可追溯
- AI 数据安全和人工确认边界

可改写题目：

- 论信息系统安全架构设计
- 论系统安全性和保密性设计
- 论 DevSecOps
- 论数据安全与隐私保护

### 第五篇：持续集成、自动化测试与自动化运维

文件：[paper-05-devops-testing-and-automated-operations.md](paper-05-devops-testing-and-automated-operations.md)

主考点：

- DevOps
- 持续集成与持续交付
- 软件测试方法
- Debian/Jenkins 平台部署与自动化运维
- 配置即代码
- 监控、日志、发布与回滚

可改写题目：

- 论软件测试方法及其应用
- 论持续集成与持续交付
- 论软件维护方法及其应用

以下题目只有在本人另有真实落地经历时才可改写使用，不能由当前仓库直接支撑：

- 完整模型驱动架构及 CIM/PIM/PSM 转换
- 多实例高可用与负载均衡
- 零信任架构落地
- 云资源编排和云上自动化运维
- Kubernetes、服务网格等完整云原生实践

## 4. 统一考场结构

每篇正文都采用以下结构：

1. 摘要：项目、角色、主题方法和效果。
2. 项目背景：业务目标、原有问题、约束和本人职责。
3. 理论说明：回答题目要求的概念、过程、方法或分类。
4. 项目实践：以三至四项关键架构决策回答“如何应用”。
5. 效果与不足：说明验证结果、架构收益、遗留风险和改进方向。

建议时间分配：

- 5 分钟：四题选一并圈出子问题。
- 10 分钟：列摘要和正文提纲。
- 85 分钟：完成正文。
- 20 分钟：检查题目呼应、术语、错字和未替换内容。

## 5. 考场前必须个性化的信息

仓库不能证明以下事实，因此五篇正文不会擅自编造：

- 项目预算、合同金额
- 团队人数和精确分工
- 用户数量、并发量、QPS
- 可用性百分比、平均响应时间
- 平均故障恢复时间
- 缺陷下降率、效率提升率

请在考前根据本人真实经历补齐：

```text
项目周期：
本人真实职位和职责：
团队人数：
部署节点规模：
日均或峰值任务量：
接口平均/分位响应时间：
任务成功率：
故障定位时间变化：
回归耗时变化：
上线后的真实改进数据：
```

如果没有可靠数字，宁可写“通过服务器 smoke 和接口自动化达到当前阶段验收标准”，也不要编造百分比或把尚未完成的端到端验证写成已通过。可以使用项目中可核验的结构性数字，例如四个主模块、三类已建模执行路径、四类 Runner 结果桶和多层测试资产。文档中的八阶段 Pipeline 属于推荐架构蓝图，不能写成单条已经完整落地的流水线实绩。

## 6. 已核验的项目事实边界

可作为论文事实使用：

- Jenkins Master、HTTPS 子路径和 Agent 基线已有用户验证记录。
- Platform API 的 run contract、callback、artifact/KPI 查询和 execution-ready detail 已有验证记录。
- Portal、FastAPI、Jenkins、Runner、KPI 工具和 AI 分析的代码骨架已经形成。
- `robot`、`python_orchestrator`、`internal_tool` 三类执行路径已经建模。
- Runner 已具备 stage/item、串并行、安全校验、资源锁、timeline 和 artifact manifest。
- Jenkins 已采用 JCasC、Job DSL、Pipeline 与 Python 辅助脚本。
- SQLite 保存元数据，Jenkins artifact 或文件系统保存 XML、HTML、Excel 和日志。

不能写成“全部生产验证通过”的内容：

- 真实 `testline_configuration + robotws + TAF + T813` 端到端链路仍在收口。
- KPI Runner 非 dry-run、真实 Compass generator/detector 仍需目标环境验证。
- Portal 完整前端测试框架和服务器 UI 回归仍待补齐。
- 当前部署不是 Kubernetes，也不是完整云原生微服务集群。
- Jenkins、SQLite 和单机服务还不能宣称已经实现多活或无单点。

## 7. 写作时的事实使用原则

1. 把“已设计”“代码已实现”“用户已验证”“待真实环境验证”分开表述。
2. 不把模块化单体或独立服务简单夸大成微服务。
3. 不把 Jenkins 的任务并发写成 HTTP 高并发。
4. 不把 SQLite 写成分布式数据库或高可用数据库。
5. 不把 AI 建议写成自动决策；当前边界是证据分析、RCA 建议和报告生成。
6. 不写公司名、真实内网地址、账号、令牌、密钥和敏感日志。

## 8. 本次学习记录

### 解决的问题

把同一个真实项目整理成五套可应对不同命题的论文母稿，避免每次遇到新题都重新编造项目。

### 文件及作用

- 本文件：考点矩阵、使用方法、事实边界和个性化清单。
- `paper-01`：架构风格、分层、服务化和系统集成。
- `paper-02`：系统建模、ABSD、评估和演化。
- `paper-03`：可靠性、容错、性能和可观测性。
- `paper-04`：安全、保密、访问控制和 AI 安全边界。
- `paper-05`：DevOps、软件测试、自动化运维和发布回滚。

### 核心调用流

五篇论文共用同一条事实主线：

```text
提交请求
  -> 创建平台 run_id
  -> Jenkins 调度执行
  -> Robot 或 Python Runner 执行
  -> KPI 后处理与产物归档
  -> Callback 回写
  -> SQLite 保存元数据
  -> Portal 和 AI 分析读取结果
```

### 关键字段

- `run_id`：平台主键，保存于 SQLite，并贯穿触发、执行、回调和查询。
- `executor_type`：区分 `robot`、`python_orchestrator` 等执行模式。
- `workflow_spec`：Python workflow 的 stage/item 结构。
- `jenkins_build_ref`：外部 Jenkins queue/build 引用。
- `artifact_manifest`：产物路径、类型和 URL 的结构化清单。
- `kpi_summary`、`detector_summary`：KPI 与异常检测摘要。
- `failure_signature`：当前已生成的标准化质量信号，可供后续同类失败检索或分组；历史聚类能力尚未实现。

### 用户自检命令

请在本地 PowerShell 执行：

```powershell
cd C:\TA\jenkins_robotframework
Get-ChildItem docs\overview\system-architect-papers\paper-*.md
Get-ChildItem docs\overview\system-architect-papers\paper-*.md |
  ForEach-Object {
    $text = Get-Content $_.FullName -Raw
    $body = [regex]::Match(
      $text,
      '(?s)## 论文正文\s*(.*?)\s*## 考场改写提示'
    ).Groups[1].Value
    [PSCustomObject]@{
      File = $_.Name
      BodyCharacters = ($body -replace '\s', '').Length
    }
  }
```

预期结果：

- 能看到五个 `paper-*.md` 文件。
- 每篇都包含摘要、项目背景、理论、项目实践、效果与不足、改写提示。
- 五篇 `BodyCharacters` 均应位于 2200～2400。

常见失败：

- 少于五个文件：说明文件未完整创建。
- 正文中仍有方括号占位：考前尚未完成个性化。
- 正文超过 2400：按题目子问题删除非主题段，而不是优先缩短项目实践。
- 正文少于 2200：优先补充架构决策、方案权衡和真实实施效果。

### 复盘问题

1. 本人在项目中的真实角色能否支撑“我主持架构设计”的表述？
2. 哪些服务器验证结果可以转化为可信的量化指标？
3. 当题目限定某种技术时，哪三段实践最能直接回答子问题？
4. 当前项目的遗留风险是否被如实写出，而不是只写成功经验？
