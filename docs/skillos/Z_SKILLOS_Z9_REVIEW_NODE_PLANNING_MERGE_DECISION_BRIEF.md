# Z9 Review Node Planning — MERGE DECISION BRIEF

> Status: MERGE | Base: 5032c4d | Branch: plan/skillos-z9-review-node-planning
> Date: 2026-06-09 | Merge Reviewer: Final Gate

---

## 1. Brief Purpose

This brief summarizes the merge decision for the Z9 Review Node planning branch.
The branch contains 26 docs-only planning files that specify a readonly, advisory
review system for Z2 explanation quality. z9_review_snapshot_candidate is sole input.
Z9 reviews Z2 explanation quality ONLY — no trade review.

## 2. Branch Summary

| Attribute | Value |
|---|---|
| Branch | plan/skillos-z9-review-node-planning |
| Base | 5032c4d |
| Files added | 26 (.md only) |
| Code added | 0 |
| Tests added | 0 |
| Config changes | 0 |
| Merge conflicts | 0 (expected) |
| Purpose | Z9 Review Node planning specification |

## 3. Design Summary

The Z9 Review Node:
- Consumes z9_review_snapshot_candidate (frozen, from Z2)
- Produces explanation quality labels (6 values)
- Produces z2_feedback_candidate (advisory, readonly)
- Enforces DENY_Z9_TRADE_RESULT_FORBIDDEN at every layer
- Defaults to DISABLED_DEFAULT_NOOP
- Has 10 degradation states (ALLOW/DENY)
- Produces 12-section review schema
- Includes kill switch for forbidden outputs
- Emits no_trade_result = True on every output
- Z9 feedback is advisory and readonly

## 4. Safety Assessment

Safety layers specified in planning:
1. Input contract — rejects trade_result and forbidden data
2. Kill switch — blocks forbidden output fields
3. Import guard — prevents module contamination (Z8, broker)
4. Degradation states — terminal on violation
5. Output validation — post-build scan for forbidden content
6. Test suite — 42 categories, 9 test files planned

## 5. Merge Justification

Reasons to merge:
- Planning is complete (14 docs) and reviewed (7 docs)
- No code impact (docs only)
- No runtime behavior change
- Specifications locked for future implementation reference
- All safety constraints documented and verifiable
- DENY_Z9_TRADE_RESULT_FORBIDDEN comprehensive
- trade_result forbidden at input, output, attribution, and feedback layers

## 6. Merge Conditions

For merge to proceed:
- Human reviewer must sign off
- No objections from stakeholders
- All PENDING fields in decision record acknowledged
- Merge checklist substantially complete
- No blocking issues from risk registers
- z9_review_snapshot_candidate scope confirmed
- no_trade_result enforcement confirmed

## 7. Final Recommendation

**Recommendation: APPROVE MERGE (pending human sign-off)**

Rationale:
- Docs-only branch with zero code impact
- Comprehensive safety specification
- Clear scope limitation (explanation quality only)
- No execution paths possible from documentation
- All required phrases present across documents
- 5032c4d base verified
- Branch clean and conflict-free
- Z9 feedback is advisory and readonly
- z2_feedback_candidate properly constrained
