# Z9 Review Node Planning — TEST AND PROOF PLAN

> Status: PLANNING | Base: 5032c4d | Branch: plan/skillos-z9-review-node-planning
> Date: 2026-06-09 | Author: Z2 天师

---

## 1. Test Philosophy

Every Z9 Review Node behavior must be provable through automated tests. The test suite
ensures Z9 reviews Z2 explanation quality ONLY, never touches trade_result, and that
z9_review_snapshot_candidate is the sole input. Z9 feedback is advisory and readonly.
DENY_Z9_TRADE_RESULT_FORBIDDEN is enforced at every layer.

## 2. Test Categories (42 Items)

| # | Category | File | Min Tests | Priority |
|---|---|---|---|---|
| 1 | DISABLED_DEFAULT_NOOP produces no output | test_disabled_default.py | 3 | P0 |
| 2 | Valid snapshot accepted | test_models.py | 5 | P0 |
| 3 | Invalid snapshot rejected | test_models.py | 5 | P0 |
| 4 | Input contract enforcement | test_contracts.py | 8 | P0 |
| 5 | Output contract enforcement | test_contracts.py | 8 | P0 |
| 6 | Forbidden input detection | test_contracts.py | 10 | P0 |
| 7 | Forbidden output prevention | test_contracts.py | 10 | P0 |
| 8 | Evidence hash validation | test_evidence.py | 6 | P0 |
| 9 | Evidence completeness assessment | test_evidence.py | 5 | P1 |
| 10 | Evidence gap identification | test_evidence.py | 4 | P1 |
| 11 | Allowed attribution types accepted | test_attribution.py | 7 | P0 |
| 12 | Forbidden attribution types blocked | test_attribution.py | 8 | P0 |
| 13 | Attribution chain integrity | test_attribution.py | 4 | P1 |
| 14 | ALLOW_Z9_READONLY_REVIEW state | test_degradation.py | 3 | P0 |
| 15 | ALLOW_Z9_DEGRADED_REVIEW state | test_degradation.py | 3 | P0 |
| 16 | DENY_Z9_SOURCE_FORBIDDEN trigger | test_degradation.py | 3 | P0 |
| 17 | DENY_Z9_REAL_SOURCE_FORBIDDEN trigger | test_degradation.py | 3 | P0 |
| 18 | DENY_Z9_OUTPUTS_UNSAFE trigger | test_degradation.py | 3 | P0 |
| 19 | DENY_Z9_TRADE_RESULT_FORBIDDEN trigger | test_degradation.py | 5 | P0 |
| 20 | DENY_Z9_EVIDENCE_INCOMPLETE trigger | test_degradation.py | 3 | P0 |
| 21 | DENY_Z9_MEMORY_MUTATION_FORBIDDEN trigger | test_degradation.py | 3 | P0 |
| 22 | DENY_Z9_EXECUTION_FORBIDDEN trigger | test_degradation.py | 3 | P0 |
| 23 | Review builder produces all 12 sections | test_review_builder.py | 5 | P0 |
| 24 | Review builder section metadata complete | test_review_builder.py | 4 | P1 |
| 25 | Review label assignment logic | test_review_builder.py | 6 | P0 |
| 26 | REVIEW_LABEL enum validation | test_review_builder.py | 6 | P0 |
| 27 | z2_feedback_candidate allowed fields | test_z2_feedback.py | 5 | P0 |
| 28 | z2_feedback_candidate forbidden fields blocked | test_z2_feedback.py | 7 | P0 |
| 29 | z2_feedback_candidate readonly enforcement | test_z2_feedback.py | 3 | P0 |
| 30 | z2_feedback_candidate no trade language | test_z2_feedback.py | 4 | P1 |
| 31 | No forbidden imports in review_node package | test_no_forbidden_imports.py | 5 | P0 |
| 32 | No import of Z8 execution modules | test_no_forbidden_imports.py | 3 | P0 |
| 33 | No import of broker modules | test_no_forbidden_imports.py | 3 | P0 |
| 34 | No import of trade pipeline modules | test_no_forbidden_imports.py | 3 | P0 |
| 35 | Kill switch activation on forbidden field | test_contracts.py | 4 | P0 |
| 36 | Kill switch blocks execution paths | test_contracts.py | 3 | P0 |
| 37 | no_trade_result always True in output | test_contracts.py | 5 | P0 |
| 38 | readonly_only always True in output | test_contracts.py | 5 | P0 |
| 39 | Confidence alignment detection | test_review_builder.py | 4 | P1 |
| 40 | Missing evidence propagation | test_review_builder.py | 3 | P1 |
| 41 | Blocked output review logic | test_review_builder.py | 4 | P1 |
| 42 | End-to-end integration (snapshot → review → feedback) | test_review_builder.py | 3 | P0 |

## 3. Test File Mapping

```
tests/skillos/capability_invocation_os/review_node/
├── test_disabled_default.py      → Categories: 1
├── test_models.py                → Categories: 2, 3
├── test_contracts.py             → Categories: 4, 5, 6, 7, 35, 36, 37, 38
├── test_evidence.py              → Categories: 8, 9, 10
├── test_attribution.py           → Categories: 11, 12, 13
├── test_degradation.py           → Categories: 14-22
├── test_review_builder.py        → Categories: 23, 24, 25, 26, 39, 40, 41, 42
├── test_z2_feedback.py           → Categories: 27, 28, 29, 30
└── test_no_forbidden_imports.py  → Categories: 31, 32, 33, 34
```

## 4. Proof Requirements

Each test must prove:
- Positive case (correct behavior with valid input)
- Negative case (correct rejection with invalid input)
- Boundary case (edge values)
- DENY case (forbidden data triggers appropriate gate)

## 5. Coverage Targets

- Line coverage: ≥95%
- Branch coverage: ≥90%
- Kill switch paths: 100% covered
- Forbidden field detection: 100% covered
- All 10 degradation states: 100% covered
- All 6 REVIEW_LABEL values: 100% covered

## 6. Integration Test Strategy

End-to-end tests verify:
- z9_review_snapshot_candidate → Z9 Review Node → z2_feedback_candidate
- No trade_result at any point in the pipeline
- No memory mutation occurs
- No execution path is reachable
- DISABLED_DEFAULT_NOOP is the starting state
- Output hash chain is valid

## 7. Regression Prevention

- Every bug fix requires a new test
- No test may be deleted without review
- Test suite runs on every commit
- Forbidden import test prevents dependency creep
- Kill switch test prevents output leakage
- no_trade_result assertion in every test class
