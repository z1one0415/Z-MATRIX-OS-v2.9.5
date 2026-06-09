# Z2 Research Report Node Implementation Planning — RISK REGISTER

> Status: PLANNING_COMPLETE
> Seal: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED
> Date: 2026-06-09
> Branch: plan/skillos-z2-research-report-node-implementation-planning
> Base: c5f69f5

---

## 1. Status

| Field | Value |
|-------|-------|
| Phase | Planning (docs-only) |
| Confidence | HIGH_WITH_STRUCTURE_ONLY |
| Total risks cataloged | 24 |
| P0 risks | 6 |
| P1 risks | 10 |
| P2 risks | 8 |

## 2. Scope

Comprehensive risk register for the Z2 Research Report Node implementation planning phase.

## 3. Dependency

- All upstream sealed; postmerge HEAD = c5f69f5
- Risk assessment based on sealed upstream contracts

## 4. Boundary

- Risks scoped to research_report_node module only
- Cross-module risks tracked in orchestrator risk register

## 5. Forbidden

- No risk mitigation may introduce forbidden fields
- No risk workaround may bypass kill-switch

## 6. Proof

### Risk Register (24 Risks)

| # | Risk | Severity | Likelihood | Mitigation | Control | Rollback Trigger |
|---|------|----------|-----------|------------|---------|-----------------|
| R01 | Forbidden field leaks into model | P0-Critical | Low | Pydantic field introspection test; CI grep scan | test_no_forbidden_imports.py + model introspection | Any forbidden field detected in any model |
| R02 | Kill-switch bypass discovered | P0-Critical | Very Low | Single env-var check, no override mechanism | test_disabled_default.py covers all bypass vectors | Any code path produces output when kill-switch disabled |
| R03 | B1 CompositionGraphResponse schema drift | P1-High | Medium | Pin to sealed version; contract validation at entry | test_contracts.py schema check | Input validation failure rate >1% |
| R04 | Z9 snapshot contract incompatibility | P1-High | Low | Contract tests against Z9 sealed spec | test_z9_snapshot.py round-trip | Z9 node rejects snapshot candidate |
| R05 | Degradation mode fails silently | P0-Critical | Low | Every degradation path tested explicitly | test_degradation.py exhaustive mode coverage | Any invocation returns success without valid report |
| R06 | Import of forbidden library (network/DB) | P0-Critical | Low | AST-based import scanning in CI | test_no_forbidden_imports.py | Any forbidden import detected |
| R07 | Section builder produces non-deterministic output | P1-High | Medium | Same-input-same-output test with fixed seed | test_section_builder.py determinism suite | Different output for identical input |
| R08 | Evidence validation too strict (false rejects) | P2-Medium | Medium | Threshold tuning with calibration dataset | test_evidence.py boundary cases | >10% valid evidence rejected |
| R09 | Evidence validation too loose (garbage through) | P1-High | Medium | Minimum quality bar with negative tests | test_evidence.py negative cases | Invalid evidence passes validation |
| R10 | Report builder timeout (>30s) | P2-Medium | Low | Performance benchmark in test suite | Timeout wrapper with degradation | p95 latency > 15s in test |
| R11 | Memory leak in section builder loop | P2-Medium | Low | Bounded iteration; no unbounded allocations | Resource monitoring in integration test | Memory growth >100MB per 1000 invocations |
| R12 | Pydantic v2 breaking change | P2-Medium | Very Low | Pin pydantic version; test on upgrade | CI dependency check | Pydantic upgrade breaks model validation |
| R13 | Registry double-registration | P1-High | Low | Idempotent registration with duplicate check | test_registry.py duplicate protection | Same node registered twice |
| R14 | Type annotation mismatch (runtime vs static) | P1-High | Medium | mypy strict mode in CI | Static analysis gate | mypy errors in module |
| R15 | Missing test coverage for edge case | P1-High | Medium | Coverage threshold ≥95%; mutation testing | Coverage report in CI | Coverage drops below 95% |
| R16 | Incorrect confidence level assignment | P1-High | Medium | Enum-only confidence with no string fallback | test_models.py enum validation | Non-enum confidence value detected |
| R17 | Partial report emitted as complete | P0-Critical | Low | Completion flag required; section count validation | test_report_builder.py completeness | Partial report lacks degradation flag |
| R18 | Z9 snapshot missing required fields | P1-High | Low | Z9 contract schema validation | test_z9_snapshot.py required fields | Z9 validation failure |
| R19 | Config override injection attack | P2-Medium | Very Low | Config override schema validation; no eval() | test_contracts.py config validation | Unexpected config field accepted |
| R20 | Log output contains sensitive data | P2-Medium | Medium | Structured logging with field allowlist | Log output review in test | Sensitive field in log output |
| R21 | Race condition in concurrent invocations | P2-Medium | Low | Stateless design; no shared mutable state | Concurrent invocation test | Different results under concurrency |
| R22 | Upstream contract version mismatch post-merge | P1-High | Low | Contract version pinning; postmerge verification | CI contract compatibility check | Contract hash mismatch |
| R23 | Test fixture staleness | P2-Medium | Medium | Fixture generation from sealed contracts | Fixture freshness check | Fixture schema diverges from model |
| R24 | Documentation-code divergence | P1-High | Medium | Doc generation from source; cross-reference check | Doc-code sync CI step | Behavioral divergence detected |

## 7. Next

- P0 risks require mitigation BEFORE implementation begins
- P1 risks require mitigation IN implementation phase
- P2 risks monitored and mitigated as encountered
- Risk register reviewed at each phase gate

---

**SEAL: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED**
