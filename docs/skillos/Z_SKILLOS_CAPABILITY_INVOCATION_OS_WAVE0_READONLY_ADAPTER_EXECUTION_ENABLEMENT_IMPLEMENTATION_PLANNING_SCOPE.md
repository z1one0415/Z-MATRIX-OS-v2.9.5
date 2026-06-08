# Impl ✓ SCOPE

## Status: IMPLEMENTATION_PLANNING_SCOPE_READY
Phase: WAVE0_ENABLEMENT_IMPLEMENTATION_PLANNING | Level 5: BLOCKED

## In Scope
| 领域 | 内容 | 产出 |
|:--|:--|:--|
| GitHub Readonly Enablement | 从 P0 skeleton 到 enabled 的步骤 | CONFIG/FILE_LEVEL/GATE_FLOW |
| Doc Gen Enablement | doc gen adapter 启用蓝图 | 同上 |
| Report Reader Enablement | report reader 启用蓝图 | 同上 |
| Config Change | 3 adapter 配置变更计划 | CONFIG_CHANGE_PLAN |
| Permission Check | 权限门禁设计 | PERMISSION_CHECK_PLAN |
| Kill Switch | 紧急回滚/降级开关 | KILL_SWITCH_PLAN |
| No Side Effect | 只读 adapter 副作用零保证 | NO_SIDE_EFFECT_PLAN |
| Rollback | 启用失败回滚路径 | ROLLBACK_PLAN |
| Test Plan | 验证测试用例 | TEST_PLAN/PROOF_MATRIX |
| Evidence Sink | 调用证据收集 | EVIDENCE_SINK_PLAN |
| Risk Assessment | 启用风险矩阵 | RISK_REGISTER×3 |
| Gate Flow | Review→Merge→Post-Merge 门禁 | GATE_FLOW_PLAN |
| Decision Records | 关键决策追踪 | DECISION_BRIEF/RECORD/SEAL |

## Out of Scope (永久禁止)
Runtime code | Adapter enablement in code(Phase 12) | Network calls | File writes | Z-MATRIX imports | invoke_skill mutation | Level 5

## Deliverables: 33 docs (14 Plan + 7 Review + 5 Merge + 7 Governance)

## Next: SCOPE finalized → Plan 层扩写 → CLOSEOUT → REVIEW_GATE

> Cap OS Phase 11 | Scope v2 | Level 5 BLOCKED