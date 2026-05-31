# Z-G16 Merge Readiness Audit
Merge: researchdb-phase-0-5-agent-kernel → v4.0-batch-0

## Gate Checks
- [x] Tests pass (1335+) | [x] Ledgers empty (real check) | [x] No external API
- [x] No production | [x] No trade/verdict | [x] No broker/runtime
- [x] Verify chain explicit (ZK + agent + research_db + ledger + forbidden)
- [x] Pycache in working tree: minimal | [x] test_v43: NOT PRESENT
- [x] pull_core12_market_data.py: REMOVED (empty file)
- [ ] 4 cases conflicts → KEEP_PARENT (human decision)

## Conflicts (4 cases files → KEEP_PARENT)
1. data/research_db/cases/case_registry_v1.csv → KEEP_PARENT
2. runtime_reports/cases/case_coverage_audit.json → KEEP_PARENT
3. runtime_reports/cases/case_expansion_v1_closeout.json → KEEP_PARENT
4. scripts/cases/run_core_12_cases.sh → KEEP_PARENT

Recommendation: MERGE_READY_RECOMMENDED_PENDING_CASES_RESOLUTION
All G16 scope hygiene items: PASS
DO NOT auto-merge. Human decision required.
