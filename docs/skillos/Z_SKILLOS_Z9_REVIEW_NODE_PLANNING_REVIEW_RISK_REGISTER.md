# Z9 Review Node Planning — REVIEW RISK REGISTER

> Status: REVIEW | Base: 5032c4d | Branch: plan/skillos-z9-review-node-planning
> Date: 2026-06-09 | Reviewer: Planning Review

---

## 1. Risk Register Purpose

This register identifies risks in the Z9 Review Node planning phase. All risks relate
to the potential for Z9 to exceed its scope (explanation quality review only) or
accidentally connect to trade/execution systems. z9_review_snapshot_candidate is sole input.

## 2. Risk Table

| # | Risk ID | Description | Likelihood | Impact | Mitigation |
|---|---|---|---|---|---|
| 1 | RSK-001 | trade_result leaks into input validation | Low | Critical | Input contract rejects; DENY_Z9_TRADE_RESULT_FORBIDDEN |
| 2 | RSK-002 | Forbidden output field emitted | Low | Critical | Kill switch + frozen dataclass |
| 3 | RSK-003 | Z8 module accidentally imported | Low | Critical | test_no_forbidden_imports.py |
| 4 | RSK-004 | Broker module accidentally imported | Low | Critical | test_no_forbidden_imports.py |
| 5 | RSK-005 | Memory mutation via z2_feedback | Medium | High | readonly_only enforcement |
| 6 | RSK-006 | Execution path via degradation bypass | Low | Critical | DENY states are terminal |
| 7 | RSK-007 | trade_result in free-text fields | Medium | High | Content scanning in validation |
| 8 | RSK-008 | Attribution type confusion (pnl_attribution) | Low | High | Enum validation + tests |
| 9 | RSK-009 | DISABLED_DEFAULT_NOOP bypassed | Low | Critical | Default state test coverage |
| 10 | RSK-010 | Evidence hash tampering | Low | Medium | Immutable frozen dataclass |
| 11 | RSK-011 | z2_feedback_candidate auto-applies | Medium | Critical | No pipeline connection |
| 12 | RSK-012 | real_pnl data in snapshot | Low | Critical | Input contract rejects |
| 13 | RSK-013 | position_change in output | Low | Critical | Frozen output dataclass |
| 14 | RSK-014 | Automatic rebalance triggered | Low | Critical | No execution interface |
| 15 | RSK-015 | Performance claim in review output | Medium | High | Output validation scan |
| 16 | RSK-016 | Alpha claim in attribution | Low | High | Forbidden attribution list |
| 17 | RSK-017 | Paper trade order in feedback | Low | Critical | Feedback field validation |
| 18 | RSK-018 | V3 sandbox invoked from Z9 | Low | Critical | No V3 import allowed |
| 19 | RSK-019 | Production decision emitted | Low | Critical | Kill switch blocks |
| 20 | RSK-020 | Insufficient test coverage at impl | Medium | Medium | ≥95% line coverage target |
| 21 | RSK-021 | Future developer adds execution path | Medium | Critical | Kill switch + import guard |
| 22 | RSK-022 | Degradation state machine has dead states | Low | Low | State transition tests |
| 23 | RSK-023 | Schema validation incomplete | Low | Medium | 12-section verification test |
| 24 | RSK-024 | Hash chain broken by Z9 modification | Low | High | Z9 never modifies hashes |
| 25 | RSK-025 | Rollback marker modified by Z9 | Low | Medium | Immutable inheritance |

## 3. Risk Categories

| Category | Count | Highest Impact |
|---|---|---|
| Execution/Trade leakage | 12 | Critical |
| Memory/State mutation | 3 | Critical |
| Import contamination | 4 | Critical |
| Coverage/Testing gaps | 3 | Medium |
| Data integrity | 3 | High |

## 4. Critical Risk Summary

All critical risks relate to Z9 accidentally:
- Processing trade_result data (mitigated by DENY_Z9_TRADE_RESULT_FORBIDDEN)
- Emitting execution outputs (mitigated by kill_switch)
- Importing forbidden modules (mitigated by test_no_forbidden_imports)
- Triggering automatic actions (mitigated by no execution interface)

## 5. Risk Acceptance Criteria

- No critical risk may remain unmitigated
- All high risks must have at least one test
- Medium risks must have documented mitigation
- Low risks are accepted with monitoring
- Z9 feedback is advisory and readonly — this is the primary mitigation

## 6. Risk Monitoring

Post-implementation, risks are monitored via:
- Automated test suite (runs on every commit)
- Import guard tests (prevents module contamination)
- Output validation (scans every review output)
- Kill switch (immediate halt on violation)
- no_trade_result assertion (every output)

## 7. Risk Owner

All risks are owned by the Z9 Review Node implementation team.
Review of risk register: PENDING
Acceptance of residual risk: PENDING
Sign-off authority: Human reviewer (requires_human_review = True)
