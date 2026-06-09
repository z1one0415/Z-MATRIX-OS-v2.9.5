# Z9 Review Node Planning — OVERVIEW

> Status: PLANNING | Base: 5032c4d | Branch: plan/skillos-z9-review-node-planning
> Date: 2026-06-09 | Author: Z2 天师

---

## 1. Purpose

The Z9 Review Node evaluates Z2 explanation quality ONLY. It consumes z9_review_snapshot_candidate
from Z2 and produces a readonly, advisory review of evidence structure, confidence alignment,
and explanation completeness. Z9 does NOT evaluate profit, trades, pnl, or broker actions.

## 2. Scope

- Z9 reviews Z2 explanation quality — no trade review
- Input: z9_review_snapshot_candidate (from Z2)
- Output: review labels, evidence gap summaries, confidence alignment assessments
- Z9 feedback is advisory and readonly
- All trade_result fields are DENY_Z9_TRADE_RESULT_FORBIDDEN
- Output includes no_trade_result marker on every review

## 3. Architecture

Z9 Review Node sits downstream of Z2 report generation. It receives a frozen snapshot
(z9_review_snapshot_candidate) and produces z2_feedback_candidate for advisory purposes only.
No mutation of Z2 state occurs. No execution path exists.

## 4. Constraints

- FORBIDDEN: trade_result, paper_trade_result, broker_result, real_pnl
- FORBIDDEN: position_change, automatic_rebalance, execution_feedback
- FORBIDDEN: broker payload, production, Z8 execution, V3 sandbox, Z9 memory mutation
- Default state: DISABLED_DEFAULT_NOOP until explicit activation

## 5. Integration Points

- Upstream: Z2 report_node (provides snapshot)
- Downstream: z2_feedback_candidate (advisory, readonly)
- Kill switch: DENY_Z9_EXECUTION_FORBIDDEN
- No connection to Z8, no broker interface, no trade pipeline

## 6. Success Criteria

- All reviews produce explanation_quality_label
- No forbidden output fields ever emitted
- z9_review_snapshot_candidate consumed correctly
- z2_feedback_candidate produced as advisory only
- DISABLED_DEFAULT_NOOP when not explicitly triggered

## 7. Future Implementation

Code paths (DO NOT CREATE NOW):
- skillos/capability_invocation_os/review_node/__init__.py
- skillos/capability_invocation_os/review_node/constants.py
- skillos/capability_invocation_os/review_node/config.py
- skillos/capability_invocation_os/review_node/models.py
- skillos/capability_invocation_os/review_node/contracts.py
- skillos/capability_invocation_os/review_node/evidence.py
- skillos/capability_invocation_os/review_node/attribution.py
- skillos/capability_invocation_os/review_node/degradation.py
- skillos/capability_invocation_os/review_node/review_builder.py
- skillos/capability_invocation_os/review_node/z2_feedback.py
- skillos/capability_invocation_os/review_node/kill_switch.py
- skillos/capability_invocation_os/review_node/registry.py
