# Z-SkillOS v1.1-B.x Semantic Drift CI Integration Gate

## Status

Z_SKILLOS_V1_1_BX_SEMANTIC_DRIFT_CI_INTEGRATION_GATE_READY

## Current Baseline

- v1.1-B standalone semantic drift audit: APPROVAL_READY (`cd9092e`)
- v1.1-A CI wrapper: `verify_skillos_v1_1_ci_audit.sh`
- Level 2 enforcement reached
- Level 3-5: BLOCKED

## Questions To Approve

| # | Question | Default |
|:--:|------|:--:|
| Q1 | Allow modifying `verify_skillos_v1_1_ci_audit.sh` to add drift audit? | No → GO changes to Yes |
| Q2 | Drift WARN: CI PASS or CI FAIL? | **PASS** |
| Q3 | Drift FAIL_CI: CI PASS or CI FAIL? | **FAIL** |
| Q4 | Drift INFO: CI PASS or CI FAIL? | **PASS** |
| Q5 | Continue blocking runtime action? | **Yes** |
| Q6 | Continue blocking baseline auto-update? | **Yes** |
| Q7 | Require stdout-only output? | **Yes** |
| Q8 | Add test coverage for CI wrapper drift command? | **Yes** |
| Q9 | Continue blocking Level 3-5? | **Yes** |

## Proposed Exit Code Strategy

| Drift Severity | CI Exit Code | CI Effect | Runtime Effect |
|:--|:--:|------|------|
| INFO | 0 | PASS | NONE |
| WARN | 0 | PASS | NONE |
| FAIL_CI | 1 | FAIL | NONE (never runtime) |

## Proposed CI Wrapper Change

Add one line to `verify_skillos_v1_1_ci_audit.sh`:

```bash
echo "--- audit_semantic_drift ---"
PYTHONPATH=. python3 scripts/skillos/audit_semantic_drift.py
```

That is the only allowed modification.

## Decision

PENDING

- [ ] GO: allow adding drift audit to CI wrapper with WARN=PASS, FAIL_CI=FAIL
- [ ] NO-GO: drift auditor remains standalone only

## Explicit Non-Scope

- no runtime integration
- no baseline auto-update
- no invoke_skill modification
- no result_envelope modification
- no production / broker / real_trade
- no Level 3-5
