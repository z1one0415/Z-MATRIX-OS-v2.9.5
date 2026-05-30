# Research OS Truth Audit

Generated: 2026-05-30T09:45:10.985138+00:00
Baseline: 131 modules, 1093 test functions, 97% coverage

## Package Distribution
| Package | Modules | Tests | Tests/Module |
|---------|:--:|:--:|:--:|
| market_data | 14 | 701 | 50.1 |
| master_data | 14 | 369 | 26.4 |
| account_truth | 13 | 364 | 28.0 |
| validation_factory | 12 | 468 | 39.0 |
| root | 8 | 66 | 8.2 |
| council | 7 | 273 | 39.0 |
| alpha_factory | 6 | 276 | 46.0 |
| portfolio_reality | 6 | 456 | 76.0 |
| proving_ground | 6 | 288 | 48.0 |
| replay | 6 | 288 | 48.0 |
| attribution | 5 | 215 | 43.0 |
| cockpit | 5 | 165 | 33.0 |
| data_supply | 5 | 370 | 74.0 |
| outcome_reality | 5 | 375 | 75.0 |
| validation | 5 | 190 | 38.0 |
| decision_intelligence | 4 | 104 | 26.0 |
| portfolio | 4 | 140 | 35.0 |
| factor_foundation | 3 | 192 | 64.0 |
| outcome_engine | 3 | 31 | 10.3 |

## Modules Without Tests (4)
- `market_data/market_data_guardrail.py`
- `master_data/import_audit.py`
- `master_data/master_schema.py`
- `research_db_status.py`

## Verdict
- Coverage: 97% ✅
- Test density: 8 avg tests/module
- Verdict: **HEALTHY** — no significant test gaps
- Risk: test overlap (same module counted in multiple test files)
