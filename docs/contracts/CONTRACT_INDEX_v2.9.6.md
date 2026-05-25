# Z-MATRIX-OS v2.9.6 — Contract Index

> RC 基准 commit: `310b6c54256f5b4b6b2df415b9deffb99c47440b`

## R-Matrix

| 项 | 路径 | 状态 |
|:--|------|:----:|
| Contract | `docs/contracts/R_MATRIX_V2_CONTRACT.md` | ✅ |
| Example (PASS) | `docs/contracts/examples/r_matrix_v2_pass_example.json` | ✅ |
| Example (DEGRADED) | `docs/contracts/examples/r_matrix_v2_degraded_example.json` | ✅ |
| Test | `tests/test_rmatrix_contract_schema.py` | ✅ |
| Test | `tests/test_rmatrix_service_v20_four_king.py` | ✅ |
| Test | `tests/test_rmatrix_service_degraded_contract.py` | ✅ |
| Verify status | 3/3 PASS (pytest aggregate) |
| Real-write boundary | no real trade, no real R-Matrix parameter update |

## G18 — Final Decision Envelope

| 项 | 路径 | 状态 |
|:--|------|:----:|
| Contract | `docs/contracts/G18_FINAL_DECISION_ENVELOPE_V11.md` | ✅ |
| Test | `tests/test_g18_final_decision_envelope_v11.py` | ✅ |
| Verify status | PASS (pytest aggregate) |
| Real-write boundary | no real trade, no broker order |

## G18 — Upstream Evidence

| 项 | 路径 | 状态 |
|:--|------|:----:|
| Contract | `docs/contracts/G18_UPSTREAM_EVIDENCE_V10.md` | ✅ |
| Test | `tests/test_g18_upstream_evidence_aggregation.py` | ✅ |
| Verify status | PASS |
| Real-write boundary | no real trade |

## G18 — Conflict Resolver

| 项 | 路径 | 状态 |
|:--|------|:----:|
| Contract | `docs/contracts/G18_CONFLICT_RESOLVER_V10.md` | ✅ |
| Test | `tests/test_g18_conflict_resolver.py` | ✅ |
| Verify status | PASS |
| Real-write boundary | no real trade |

## G18 — Paper Execution Record

| 项 | 路径 | 状态 |
|:--|------|:----:|
| Contract | `docs/contracts/G18_PAPER_EXECUTION_RECORD_V10.md` | ✅ |
| Test | `tests/test_g18_paper_execution_record.py` | ✅ |
| Verify status | PASS (pytest aggregate) |
| Real-write boundary | no real trade, no real Z9 write |

## Z9 — Calibration Sample

| 项 | 路径 | 状态 |
|:--|------|:----:|
| Contract | `docs/contracts/Z9_CALIBRATION_SAMPLE_V10.md` | ✅ |
| Example | `docs/contracts/examples/z9_calibration_sample_v10_example.json` | ✅ |
| Test | `tests/test_z9_calibration_sample_contract.py` | ✅ |
| Verify status | 6/6 PASS |
| Real-write boundary | no real trade, no real Z9 write |

## Z9 — Ingestion Queue

| 项 | 路径 | 状态 |
|:--|------|:----:|
| Contract | `docs/contracts/Z9_INGESTION_QUEUE_V10.md` | ✅ |
| Example | `docs/contracts/examples/z9_ingestion_queue_item_v10_example.json` | ✅ |
| Test | `tests/test_z9_ingestion_queue_contract.py` | ✅ |
| Verify status | 12/12 PASS |
| Real-write boundary | no real trade, no real queue write, no real Z9 write |

## Z9 — Outcome Backfill Task

| 项 | 路径 | 状态 |
|:--|------|:----:|
| Contract | `docs/contracts/Z9_OUTCOME_BACKFILL_V10.md` | ✅ |
| Example | `docs/contracts/examples/z9_outcome_backfill_task_v10_example.json` | ✅ |
| Test | `tests/test_z9_outcome_backfill_contract.py` | ✅ |
| Verify status | 18/18 PASS |
| Real-write boundary | no real trade, no real market fetch, no real outcome backfill |

## Z9 — Calibration Policy Preview

| 项 | 路径 | 状态 |
|:--|------|:----:|
| Contract | `docs/contracts/Z9_CALIBRATION_POLICY_V10.md` | ✅ |
| Example | `docs/contracts/examples/z9_calibration_policy_preview_v10_example.json` | ✅ |
| Test | `tests/test_z9_calibration_policy_contract.py` | ✅ |
| Verify status | 24/24 PASS |
| Real-write boundary | no real trade, no real EV weight change, no real R-Matrix param change, no real G18 rule change |

## Z9 — Calibration (Legacy)

| 项 | 路径 | 状态 |
|:--|------|:----:|
| Contract | `docs/contracts/Z9_CALIBRATION_V10.md` | ✅ |
| Test | `tests/test_z9_calibration_contract.py` | ✅ |
| Verify status | PASS |
| Real-write boundary | no real trade |

## RC Gate

| 项 | 路径 | 状态 |
|:--|------|:----:|
| RC Manifest | `docs/release/RC_MANIFEST_v2.9.6.md` | ✅ |
| RC Verification Template | `docs/release/RC_VERIFICATION_REPORT_TEMPLATE_v2.9.6.md` | ✅ |
| RC Known Limitations | `docs/release/RC_KNOWN_LIMITATIONS_v2.9.6.md` | ✅ |
| RC Gate Test | `tests/test_rc_verification_gate.py` | ✅ |
| Verify script | `scripts/verify_rc_candidate.sh` | ✅ |
| Real-write boundary | no real trade, no real Z9 write, no real market fetch, no auto calibration |
