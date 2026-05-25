# Z-MATRIX-OS v2.9.6-RC1 Release Notes

## 1. Release Summary

| 字段 | 值 |
|------|------|
| RC 版本 | v2.9.6-RC1 |
| 发布日期 | 2026-05-25 |
| 发布类型 | Release Candidate |
| 分支 | master |
| Package commit | `0882a7802dc68fdc0080933ac6e0fdc1b280eec8` |
| Verification gate | `7b7741d81d84aebb291c3f5b64a78e03aeb4d86f` |

## 2. What's New

| Batch | 内容 |
|:----:|------|
| A | 模块边界收口 + G07→G01 + G14 R-Matrix对齐 + G18 adapter |
| B-1 | R-Matrix v2.0 真四天王服务 (legacy_fallback=False) |
| B-2 | G09主流程统一到 evaluate_r_matrix_cycle |
| B-3 | R-Matrix Contract Freeze (16字段 + 5 JSON样例) |
| C-1 | G18 Final Decision Envelope v1.1 (6条优先级规则) |
| C-2 | G18 Upstream Evidence Aggregation (6 sources) |
| C-3 | G18 Conflict Resolver v1.0 (5条冲突规则) |
| C-4 | G18 Paper Execution Record v1.0 |
| D-1 | Z9 Calibration Sample Contract v1.0 |
| D-2 | Z9 Ingestion Queue Contract v1.0 |
| D-3 | Z9 Outcome Backfill Contract v1.0 |
| D-4 | Z9 Calibration Policy Preview v1.0 |
| E-1 | RC Verification Gate |
| E-2 | RC Packaging |
| E-3 | 本文档 |

## 3. Core Capability Chain

```
G18 prediction
→ final_decision_envelope
→ upstream_evidence
→ conflict_resolution
→ paper_execution_record
→ z9_calibration_sample_preview
→ z9_ingestion_queue_preview
→ z9_outcome_backfill_task_preview
→ z9_calibration_policy_preview
```

## 4. Safety Boundaries

| 边界 | 状态 |
|:----|:----:|
| Real trade (BUY/SELL/ADD/CLEAR) | ❌ 禁止 |
| Broker order (MARKET_ORDER/BROKER_ORDER) | ❌ 禁止 |
| Real Z9 write | ❌ 禁止 |
| Real queue write | ❌ 禁止 |
| Real market data fetch | ❌ 禁止 |
| Auto calibration | ❌ 禁止 |
| 所有校准输出 | 仅 preview 模式 |

## 5. How to Verify

```bash
# 完整 verify 脚本
./scripts/verify_rc_candidate.sh

# 或选择性运行:
python3 tests/test_rc_verification_gate.py    # RC 验收门
python3 tests/test_rc_packaging.py            # 发布包完整性
python3 tests/test_z9_calibration_policy_contract.py  # D-4
python3 tests/test_z9_outcome_backfill_contract.py    # D-3
python3 tests/test_z9_ingestion_queue_contract.py     # D-2
python3 tests/test_z9_calibration_sample_contract.py  # D-1
python3 tests/test_g18_paper_execution_record.py      # C-4
```

## 6. Known Limitations

详细文档: `docs/release/RC_KNOWN_LIMITATIONS_v2.9.6.md`

| 项 | 影响 | 状态 |
|:--|------|:----:|
| legacy R-Matrix 旧接口测试 | 不影响核心管线 | non-blocking |
| Hermes full test import error | 不影响核心管线 | non-blocking |
| 真实行情回填 | D-3 未实现 | 预留 |
| 自动调参 | D-4 仅预览 | 预留 |
| G09信号路径依赖 | 本地绝对路径，降级为WATCH | non-blocking |

## 7. Files Added

| 路径 | 说明 |
|------|------|
| `docs/release/RC_MANIFEST_v2.9.6.md` | RC 版本清单 |
| `docs/release/RC_VERIFICATION_REPORT_TEMPLATE_v2.9.6.md` | 验收报告模板 |
| `docs/release/RC_KNOWN_LIMITATIONS_v2.9.6.md` | 已知限制说明 |
| `docs/contracts/CONTRACT_INDEX_v2.9.6.md` | 全量契约索引 |
| `release/v2.9.6-RC1/` (7+1文件) | 发布包 |
| `tests/test_rc_verification_gate.py` | RC 验收门测试 (9项) |
| `tests/test_rc_packaging.py` | 发布包测试 |
| `scripts/build_rc_package_manifest.py` | checksum 生成工具 |
| `zmatrix/calibration/z9_calibration_sample.py` | Z9 D-1 样本契约 |
| `zmatrix/calibration/z9_ingestion_queue.py` | Z9 D-2 队列契约 |
| `zmatrix/calibration/z9_outcome_backfill.py` | Z9 D-3 回填任务契约 |
| `zmatrix/calibration/z9_calibration_policy.py` | Z9 D-4 校准策略预览 |

## 8. Upgrade Notes

- 无需数据库迁移
- 无需外部 API Key
- 无需券商账户
- 无需 Z9 write 后端
- 不修改已有持仓配置

## 9. Rollback

- 本地：`git revert <release-commit>`
- 数据层：Z9 不写真实数据，无数据回滚需求
- 配置层：G18 无持久化配置变更
- 验证：回滚后运行 `./scripts/verify_rc_candidate.sh`

## 10. Next Steps

| Batch | 内容 |
|:----:|------|
| E-4 | Operator Runbook |
| E-5 | Tag v2.9.6-RC1 |
