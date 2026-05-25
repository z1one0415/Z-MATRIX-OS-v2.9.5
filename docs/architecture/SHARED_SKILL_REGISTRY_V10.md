# Shared Skill Registry v1.0 — Z-MATRIX-OS 三层架构收束

## 注册表路径

`zmatrix/architecture/skill_registry.py` → `SHARED_SKILL_REGISTRY`

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| layer | str | ✅ | 固定为 `"shared_skill"` |
| module | str | ✅ | Python 模块导入路径 |
| public_function | str | ✅ | 对外暴露的公开函数名 |
| owner | str | ✅ | 技能归属方 (R-Matrix / G18 / Z9 / SystemCore / RC) |
| used_by | list[str] | ✅ | 消费该技能的管线 ID 列表 |
| contract | str | ❌ | 合约文档路径 (可选，部分技能无独立 contract) |
| test | str | ✅ | 测试文件路径 |
| duplicate_allowed | bool | ✅ | 默认为 False，禁止重复建设 |
| safety_boundary | str | ✅ | 安全边界说明 |

## 已注册技能

| skill_id | owner | module |
|----------|-------|--------|
| `r_matrix.evaluate_cycle` | R-Matrix | `zmatrix.scoring.r_matrix.r_matrix_service` |
| `evidence.aggregate_upstream` | G18 | `zmatrix.prediction.upstream_evidence_aggregator` |
| `conflict.resolve` | G18 | `zmatrix.prediction.conflict_resolver` |
| `decision.finalize` | G18 | `zmatrix.prediction.final_decision_envelope` |
| `paper.record` | G18 | `zmatrix.prediction.paper_execution_record` |
| `z9.sample.build` | Z9 | `zmatrix.calibration.z9_calibration_sample` |
| `z9.queue.build` | Z9 | `zmatrix.calibration.z9_ingestion_queue` |
| `z9.backfill_task.build` | Z9 | `zmatrix.calibration.z9_outcome_backfill` |
| `z9.calibration_policy.preview` | Z9 | `zmatrix.calibration.z9_calibration_policy` |
| `safety.no_real_trade` | SystemCore | `zmatrix.action.action_contracts` |
| `rc.checksum.build` | RC | `scripts.build_rc_package_manifest` |

## 约束

- `duplicate_allowed` 除显式标记外恒为 False
- R-Matrix 只能有一个 canonical skill id
- 无任何 skill 可声明 real trade enabled
- 所有 skill 必须同时存在 contract 或 test

## 安全边界

所有已注册技能的 safety_boundary 均已声明 `no real trade` 或等价约束。
