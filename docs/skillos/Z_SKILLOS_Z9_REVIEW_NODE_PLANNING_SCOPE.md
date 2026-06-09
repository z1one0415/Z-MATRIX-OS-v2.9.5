# Z9 Review Node Planning — SCOPE

> Status: PLANNING | Base: 5032c4d | Branch: plan/skillos-z9-review-node-planning
> Date: 2026-06-09 | Author: Z2 天师

---

## 1. In-Scope

- Review of Z2 explanation quality via z9_review_snapshot_candidate
- Evidence chain completeness assessment
- Confidence alignment validation
- Missing evidence identification
- Degradation status review (ALLOW/DENY classification)
- Blocked output detection and review
- Advisory z2_feedback_candidate generation (readonly)

## 2. Out-of-Scope (FORBIDDEN)

- Any trade_result evaluation — DENY_Z9_TRADE_RESULT_FORBIDDEN
- Paper trade performance — no_paper_trading
- Broker actions — no_broker_action
- Position changes — no_position_change
- Real PnL — no real_pnl field
- Automatic rebalance — forbidden
- Production decisions — forbidden
- Z8 execution paths — forbidden
- V3 sandbox invocation — forbidden
- Z9 memory mutation — DENY_Z9_MEMORY_MUTATION_FORBIDDEN

## 3. Boundary Definition

Z9 operates in a strict readonly review capacity. The boundary is:
- INPUT boundary: only z9_review_snapshot_candidate and its hash fields
- OUTPUT boundary: only review labels, evidence assessments, advisory feedback
- EXECUTION boundary: no code path connects to any trade system
- MEMORY boundary: no mutation of any persistent state

## 4. Stakeholders

- Z2 (upstream producer of snapshot)
- Z9 (this node — reviewer)
- Human reviewer (receives advisory output)
- No broker, no execution engine, no position manager

## 5. Acceptance Criteria

- z9_review_snapshot_candidate is the SOLE input source
- no_trade_result is emitted on every review output
- Z9 feedback is advisory and readonly — verified by contract test
- All REVIEW_LABEL values are explanation-only (never trade-related)
- DISABLED_DEFAULT_NOOP is the default state

## 6. Deliverables

Planning phase (this branch):
- 14 planning docs (this file + 13 others)
- 7 review docs
- 5 merge docs
- All at sufficient depth for implementation readiness

Implementation phase (future):
- 12 Python modules under review_node/
- 9 test files under tests/

## 7. Exclusions Register

| Excluded Item | Reason | Gate |
|---|---|---|
| trade_result | DENY_Z9_TRADE_RESULT_FORBIDDEN | kill_switch |
| broker_result | No execution path | contracts |
| real_pnl | No performance measurement | output_contract |
| position_change | No position authority | kill_switch |
| alpha_claim | No performance claims | attribution |
| paper_trade_order | No simulated trading | output_contract |
| auto_patch_z2_report | Advisory only, no mutation | z2_feedback |
| auto_update_memory | DENY_Z9_MEMORY_MUTATION_FORBIDDEN | degradation |
