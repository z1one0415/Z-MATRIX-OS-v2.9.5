# Z9 Review Node Planning — REVIEW DECISION BRIEF

> Status: REVIEW | Base: 5032c4d | Branch: plan/skillos-z9-review-node-planning
> Date: 2026-06-09 | Reviewer: Planning Review

---

## 1. Decision Context

The Z9 Review Node planning phase has produced 14 planning documents specifying a readonly,
advisory review system for Z2 explanation quality. This decision brief summarizes the
key design choices for reviewer consideration. Z9 consumes z9_review_snapshot_candidate only.

## 2. Key Design Decisions

| # | Decision | Rationale | Alternative Considered |
|---|---|---|---|
| 1 | Sole input: z9_review_snapshot_candidate | Isolation from trade data | Multiple input sources |
| 2 | DISABLED_DEFAULT_NOOP as default | Safety-first design | Active-by-default |
| 3 | Frozen dataclasses for I/O | Immutability guarantee | Mutable dicts |
| 4 | Kill switch for forbidden outputs | Defense in depth | Validation only |
| 5 | Import guard tests | Prevent module contamination | Runtime checks only |
| 6 | 12-section review schema | Structured assessment | Free-form review |
| 7 | Advisory-only feedback | No automatic mutation | Auto-patch Z2 |
| 8 | 10 degradation states | Comprehensive coverage | Simple pass/fail |
| 9 | 6 REVIEW_LABEL values | Explanation-focused labels | Trade-related labels |
| 10 | Hash chain inheritance | Audit trail continuity | Fresh hash chain |

## 3. Scope Decision

The fundamental scope decision: Z9 reviews Z2 explanation quality ONLY.
- NO trade review
- NO profit evaluation
- NO broker assessment
- NO position management
- Z9 feedback is advisory and readonly
- no_trade_result is always True
- DENY_Z9_TRADE_RESULT_FORBIDDEN is the primary safety gate

## 4. Architecture Decision

Z9 is a pure logic node with:
- No external API calls
- No database writes (beyond audit append)
- No execution interface
- No broker connection
- No memory mutation (DENY_Z9_MEMORY_MUTATION_FORBIDDEN)
- Stateless between invocations

## 5. Safety Decision

Multiple layers of safety:
1. Input contract (rejects forbidden data)
2. Kill switch (blocks forbidden outputs)
3. Import guard (prevents module contamination)
4. Degradation states (terminal on violation)
5. Output validation (post-build scan)
6. Test suite (regression prevention)

## 6. Feedback Decision

z2_feedback_candidate is advisory only:
- Human must review and decide
- No automatic application to Z2
- No pipeline triggered by feedback
- readonly_only = True enforced
- requires_human_review field available
- trade_result never in feedback

## 7. Recommendation

Recommendation: **PROCEED TO MERGE READINESS**

Rationale:
- All specifications are complete and consistent
- Safety mechanisms are comprehensive (5 layers)
- Test plan covers all critical paths (42 categories)
- No execution risk identified in planning
- DENY_Z9_TRADE_RESULT_FORBIDDEN properly enforced
- z9_review_snapshot_candidate properly isolated
- z2_feedback_candidate properly constrained
