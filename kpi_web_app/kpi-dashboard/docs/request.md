# KPI Web App Rebuild Request Specification

## 1. Purpose

This document defines the minimum requirement package needed to rebuild the `kpi_web_app` family with low ambiguity.

Covered capability domains:

- Portal shell: `kpi-dashboard`
- KPI anomaly detection: `kpi-anomaly-detector`
- KPI report generation: `kpi-generator`
- Traffic orchestration: `kpi_traffic_model`
- Supporting report scripts: `get-kpi-report`

## 2. Product Boundary

Before implementation, the requester must clarify:

- whether the target is only a Portal UI or also a local execution platform
- whether sibling repositories remain independent or become one product
- which modules are in phase 1 and which are postponed
- whether scheduling, persistence, audit, and recovery belong to the Portal

## 3. Required Requirement Domains

### 3.1 Business capability requirements

For each capability, define:

- capability name
- business objective
- trigger condition
- input artifacts
- processing rules
- output artifacts
- failure expectation
- owner team

### 3.2 Functional requirements

For each function, define:

- function ID
- actor
- preconditions
- main flow
- exception flow
- postconditions
- acceptance criteria

Minimum scope:

- Portal home page
- module navigation
- upload and validation
- background job creation
- status transitions
- job detail rendering
- artifact download
- rerun, cancel, delete
- env inspection and traffic request submission

### 3.3 Data requirements

Must include:

- input file formats
- filename rules
- schema validation rules
- derived fields
- output schema
- retention policy
- versioning rules

Important project-specific contracts:

- detector filename parsing rules
- KPI Excel schema
- generator request payload
- traffic model request payload
- job metadata schema
- artifact metadata schema

### 3.4 Integration requirements

For each integration, define:

- system name
- integration type
- authentication mode
- timeout and retry policy
- failure behavior
- contract versioning rule

Likely integrations:

- local Python execution for detector and generator
- traffic-model execution handoff
- Compass-related APIs
- local filesystem artifacts
- Portal SQLite job store

### 3.5 UI requirements

Each page must define:

- page objective
- entry route
- core components
- validation rules
- table columns
- filter behavior
- empty and error states
- auto-refresh behavior
- success and download feedback

### 3.6 Workflow and orchestration requirements

Each async flow must define:

- trigger source
- queueing rule
- ordering rule
- concurrency rule
- timeout rule
- cancel semantics
- rerun semantics
- restart recovery behavior
- artifact collection points

### 3.7 Non-functional requirements

Must define measurable targets for:

- performance
- availability
- reliability
- scalability
- security
- maintainability
- deployability
- observability

### 3.8 Operations requirements

Must define:

- environment model
- config source
- backup and cleanup policy
- artifact retention
- rollback strategy
- release process

### 3.9 Security requirements

Must clarify:

- authentication need
- RBAC need
- who can upload, rerun, cancel, delete
- secret storage model
- audit requirements

### 3.10 Acceptance requirements

Acceptance must cover:

- function
- UI
- integration
- data correctness
- performance
- deployment
- operations

## 4. Recommended Input Template

Prepare these sections before development:

- project charter
- module inventory
- use-case matrix
- data contract matrix
- integration matrix
- page inventory
- workflow matrix
- deployment and operations matrix
- acceptance checklist

## 5. Core Conclusion

`kpi_web_app` is not only a website rebuild task. It is a Portal-plus-capability-platform rebuild task. The requester must therefore provide both UI requirements and execution-orchestration requirements.