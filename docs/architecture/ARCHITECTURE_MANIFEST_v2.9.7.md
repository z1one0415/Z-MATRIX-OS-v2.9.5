# Architecture Manifest v2.9.7 — Release Candidate

## 基本信息

| 字段 | 值 |
|------|------|
| 架构版本 | v2.9.7-arch-RC1 |
| base tag | v2.9.6-RC1 |
| 当前分支 | v2.9.7-dev |
| 发布时间 | 2026-05-26 |

## 三层架构

### Layer 1: Shared Skill Module Layer
所有通用能力注册为 shared skill，禁止重复建设。
- SHARED_SKILL_REGISTRY (11 skills)

### Layer 2: Pipeline Application Layer
Pipeline 只能组合调用已注册的 skill module。
- PIPELINE_REGISTRY (4 pipelines)
- WORKFLOW_DAG_REGISTRY (3 workflows)

### Layer 3: System Control Layer
Gate / Enforcement / Audit / Controller。
- GATE_REGISTRY (7 gates)
- Architecture Enforcement
- Cross-Pipeline Conflict Audit
- System Controller MVP (plan only)

## 已完成

- F-1 Shared Skill Registry
- F-2 Pipeline Registry
- F-3 Gate Registry
- F-4 Workflow DAG
- F-5 Architecture Enforcement
- F-6 Cross-Pipeline Conflict Audit
- F-7 Architecture RC Package
- F-8 System Controller MVP

## 禁止边界

- no real trade
- no broker order
- no real Z9 write
- no real market fetch
- no auto calibration

## 验收命令

```bash
bash scripts/verify_architecture_candidate.sh
```

## 已知限制

- Architecture Enforcement v1.0 是 registry-level enforcement
- 它不扫描 pipeline 源文件中的未注册内部能力构造
- Source-level enforcement 将在下一轮架构加固阶段处理

## Tag

| 字段 | 值 |
|------|------|
| Tag candidate | v2.9.7-arch-RC1 |
| Tag status | CREATED_EXTERNAL_TARGET_VERIFIED |
| Verified tag target | `393469050bb10816060706250b9301439c1246b4` |
| Tag record | docs/architecture/TAG_RECORD_v2.9.7-arch-RC1.md |

## 下一步

v2.9.7-arch-RC1 tag has been created and externally verified.
