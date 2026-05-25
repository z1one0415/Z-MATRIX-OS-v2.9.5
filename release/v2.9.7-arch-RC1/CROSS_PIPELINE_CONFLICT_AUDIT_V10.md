# Cross-Pipeline Conflict Audit v1.0 — 管线间冲突审计

## 功能

审计不同 pipeline 是否重复造能力、冲突使用 shared skill、边界声明不一致。

## 审计项

| 审计函数 | 目标 |
|----------|------|
| `audit_rmatrix_single_source_of_truth()` | R-Matrix 只能有一个 canonical skill: r_matrix.evaluate_cycle |
| `audit_z9_preview_boundary_consistency()` | Z-G18 必须完整覆盖 Z9 preview chain |
| `audit_gate_coverage_gaps()` | RC-release 必须覆盖 packaging/verification/safety；Z-G18 必须经过 z9.preview_only |
| `audit_pipeline_skill_conflicts()` | 检查有无 skill 被标记为 duplicate_allowed=True |

## 集成

`run_cross_pipeline_conflict_audit()` 一次性执行所有审计，返回违规列表。
