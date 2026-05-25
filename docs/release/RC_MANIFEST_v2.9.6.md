# Z-MATRIX-OS v2.9.6-RC1 — Release Candidate Manifest

## 1. RC 信息

| 字段 | 值 |
|------|------|
| RC 名称 | Z-MATRIX-OS v2.9.6-RC1 |
| 基准 commit (Batch D 放行) | `310b6c54256f5b4b6b2df415b9deffb99c47440b` |
| RC gate commit (E-1) | `445d5cd254f825ceb0e20cb1c80cc739712e4e53` |
| RC gate closeout | `79d4e593164e7e826dadc98a0f545d1a6d1f922f` |
| 分支 | master |
| 发布日期 | 2026-05-25 |
| 发布类型 | Release Candidate 1 |

## 2. 已放行 Batch 清单

| Batch | 状态 | 内容 |
|:----:|:----:|------|
| A | ✅ 放行 | 模块边界收口 + G07→G01 + G14 R-Matrix对齐 + G18 adapter |
| B-1 | ✅ 放行 | R-Matrix v2.0真四天王服务 |
| B-2 | ✅ 放行 | G09主流程统一到 evaluate_r_matrix_cycle |
| B-3 | ✅ 放行 | R-Matrix Contract Freeze |
| C-1 | ✅ 放行 | G18 Final Decision Envelope v1.1 |
| C-2 | ✅ 放行 | G18 Upstream Evidence Aggregation v1.0 |
| C-3 | ✅ 放行 | G18 Conflict Resolver v1.0 |
| C-4 | ✅ 放行 | G18 Paper Execution Record v1.0 |
| D-1 | ✅ 放行 | Z9 Calibration Sample Contract v1.0 |
| D-2 | ✅ 放行 | Z9 Ingestion Queue Contract v1.0 |
| D-3 | ✅ 放行 | Z9 Outcome Backfill Contract v1.0 |
| D-4 | ✅ 放行 | Z9 Calibration Policy Preview v1.0 |

## 3. 关键能力链

```
G18 prediction
→ final_decision_envelope (C-1)
→ upstream_evidence (C-2)
→ conflict_resolution (C-3)
→ paper_execution_record (C-4)
→ z9_calibration_sample_preview (D-1)
→ z9_ingestion_queue_preview (D-2)
→ z9_outcome_backfill_task_preview (D-3)
→ z9_calibration_policy_preview (D-4)
```

## 4. 禁止边界

- no real trade (BUY / SELL / ADD / CLEAR / MARKET_ORDER / BROKER_ORDER / AUTO_TRADE / REAL_TRADE)
- no real Z9 write
- no real queue write
- no real market data fetch
- no auto calibration
- no manual intervention required at RC level

## 5. RC 验收命令

```bash
# 编译全模块
python3 -m compileall pipelines tests zmatrix hermes scripts

# 核心 contract 测试
python3 tests/test_core_contracts.py
python3 tests/test_pipeline_smoke.py
python3 tests/test_pipeline_manifest_smoke.py

# R-Matrix 测试
python3 tests/test_rmatrix_service_v20_four_king.py
python3 tests/test_rmatrix_contract_schema.py
python3 tests/test_rmatrix_service_degraded_contract.py

# G18 测试
python3 tests/test_g18_final_decision_envelope_v11.py
python3 tests/test_g18_upstream_evidence_aggregation.py
python3 tests/test_g18_conflict_resolver.py
python3 tests/test_g18_paper_execution_record.py
python3 tests/test_zg18_core.py

# Z9 合约测试
python3 tests/test_z9_calibration_sample_contract.py
python3 tests/test_z9_ingestion_queue_contract.py
python3 tests/test_z9_outcome_backfill_contract.py
python3 tests/test_z9_calibration_policy_contract.py

# RC 验收门
python3 tests/test_rc_verification_gate.py

# 完整 verify 脚本
./scripts/verify_rc_candidate.sh
```

## 6. 回滚策略

- 回滚目标：移除 RC tag，恢复到前一个已放行 commit
- 命令：`git revert <commit>`
- 数据层：Z9 不写真实数据，无数据回滚需求
- 配置层：G18 无持久化配置变更
- 验证：回滚后运行完整 verify_rc_candidate.sh

## 7. 已知保留项

详细文档: `docs/release/RC_KNOWN_LIMITATIONS_v2.9.6.md`

| 项 | 说明 | 状态 |
|:--|------|:----:|
| G09 周期信号桥 | G09信号文件路径依赖本地绝对路径 | ⚠️ non-blocking |
| legacy test_hermes_full.py | memory_bank 接口变更 import error | ⚠️ non-blocking |
| legacy test_zg09_type_a_horizontal | R-Matrix 重构后旧接口不兼容 | ⚠️ non-blocking |
| legacy test_zg09_zg10_contracts | R-Matrix 重构后旧接口不兼容 | ⚠️ non-blocking |
| legacy test_zg14_matrix_reliability | R-Matrix 重构后旧接口不兼容 | ⚠️ non-blocking |
| test_zg09_sell_decision | 价格精度漂移 6.4→6.5 | ⚠️ non-blocking |
| 真实行情回填 | D-3 未实现 | ⏳ 预留 |
| 自动调参 | D-4 仅预览 | ⏳ 预留 |
