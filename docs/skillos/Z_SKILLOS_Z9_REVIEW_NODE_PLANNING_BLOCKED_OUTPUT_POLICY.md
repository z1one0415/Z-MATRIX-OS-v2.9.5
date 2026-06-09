# Z9 Review Node Planning — BLOCKED OUTPUT POLICY

> Status: PLANNING | Base: 5032c4d | Branch: plan/skillos-z9-review-node-planning
> Date: 2026-06-09 | Author: Z2 天师

---

## 1. Blocked Output Definition

Blocked outputs are fields that were removed from Z2's report before snapshot generation,
OR fields that Z9 must never emit. Z9 reviews the blocked_outputs_removed list from
z9_review_snapshot_candidate and assesses whether blocking was appropriate.

## 2. Z2 Blocked Outputs (Inherited)

The z9_review_snapshot_candidate contains blocked_outputs_removed list:
- These are fields Z2 self-blocked before sending snapshot
- Z9 reviews whether the blocking was justified
- Z9 does NOT unblock or restore these fields
- Z9 produces blocked_output_review section

## 3. Z9 Blocked Outputs (Self-Enforced)

Z9 will never emit these fields regardless of input:
| Blocked Output | Category | Enforcement |
|---|---|---|
| trade_instruction | Execution | kill_switch hardcoded |
| buy_signal | Execution | kill_switch hardcoded |
| sell_signal | Execution | kill_switch hardcoded |
| position_weight | Position | kill_switch hardcoded |
| order_signal | Execution | kill_switch hardcoded |
| automatic_rebalance | Execution | kill_switch hardcoded |
| broker_action | Broker | kill_switch hardcoded |
| paper_trade_order | Simulated | kill_switch hardcoded |
| real_trade_order | Real trade | kill_switch hardcoded |
| real_pnl | Performance | kill_switch hardcoded |
| performance_claim | Performance | kill_switch hardcoded |
| alpha_claim | Performance | kill_switch hardcoded |
| expected_return_claim | Performance | kill_switch hardcoded |
| production_decision | Production | kill_switch hardcoded |

## 4. Blocked Output Review Logic

When Z9 reviews blocked_outputs_removed from Z2:
1. Check each blocked field against known dangerous fields
2. If a dangerous field was correctly blocked → EXPLANATION_ACCEPTED_STRUCTURE_ONLY
3. If a dangerous field was NOT blocked → EXPLANATION_BLOCKED_OUTPUT_RISK
4. Document the assessment in blocked_output_review section
5. Include in z2_feedback_candidate if issues found
6. All assessment is advisory — Z9 feedback is advisory and readonly

## 5. Kill Switch Integration

The kill_switch module enforces blocked outputs at multiple levels:
- Import-time: forbidden modules cannot be imported
- Build-time: output dataclass has no forbidden fields
- Runtime: post-build validation scans for forbidden keys
- Test-time: test_no_forbidden_imports.py verifies isolation
- DENY_Z9_OUTPUTS_UNSAFE triggers if enforcement fails

## 6. Blocked Output Attribution

When outputs are blocked:
- blocked_output_risk_attribution explains why
- no_trade_result confirms no trade data leaked
- DENY_Z9_TRADE_RESULT_FORBIDDEN if trade output attempted
- Evidence chain preserved (hashes valid)
- z9_review_snapshot_candidate remains sole input

## 7. Audit Trail for Blocked Outputs

Every blocked output event is recorded:
- Which field was blocked
- Why it was blocked (policy reference)
- When it was blocked (in which section)
- Hash of the review at block point
- No blocked output can be unblocked retroactively
- Audit trail is immutable and append-only
