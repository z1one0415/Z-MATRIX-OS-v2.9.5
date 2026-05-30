# Phase 1 Acceptance Matrix

| Item | Status |
|------|:------:|
| Private Data Guardrail (.gitignore) | ✅ DONE |
| test_private_data_guardrail | ✅ DONE |
| raw_import_schema + CSV field defs | ✅ DONE |
| trade_normalizer | ✅ DONE |
| position_normalizer | ✅ DONE |
| cashflow_normalizer | ✅ DONE |
| account_snapshot_normalizer | ✅ DONE |
| account_reconciler | ✅ DONE |
| capital_curve_builder | ✅ DONE |
| holding_pnl_builder (FIFO) | ✅ DONE |
| drawdown_calculator | ✅ DONE |
| trade_quality_checker | ✅ DONE |
| missing_data_detector | ✅ DONE |
| account_truth_report generator | ✅ DONE |
| import_audit | ✅ DONE |
| Sample fixtures (4 CSV) | ✅ DONE |
| Signal + watchlist CSVs | ✅ DONE |
| test_account_truth_framework (34 tests) | ✅ DONE |
| verify_research_db_phase1_account_truth.sh | ✅ DONE |

## Safety

- Real broker raw data imported: FALSE
- Real data committed: FALSE
- Production: BLOCKED
- Broker/runtime: BLOCKED
