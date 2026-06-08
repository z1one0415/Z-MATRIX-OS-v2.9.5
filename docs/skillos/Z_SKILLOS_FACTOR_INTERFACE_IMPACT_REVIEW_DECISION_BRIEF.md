# Factor Interface Impact Review — Decision Brief

## Status: Z_SKILLOS_FACTOR_INTERFACE_IMPACT_REVIEW_DECISION_BRIEF_READY
Branch: plan/...factor-interface-impact-review-a1-b1 | Level 5: BLOCKED

## Recommendation
**INSERT_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING_BEFORE_A1_B1_MERGE**

## Sub-decisions
| # | Decision | Recommendation |
|:--:|:--|:--|
| 1 | C1 status | ACCEPTED — no rework needed |
| 2 | A1 merge | BLOCKED — needs factor interface alignment hardening |
| 3 | B1 merge | BLOCKED — needs FactorInvocationResponse + blocked-output filtering |
| 4 | Factor Library Read-Only Adapter Planning | CREATE AFTER HUMAN DECISION |

## Recommended Sequence
1. Human approves Factor Library Read-Only Adapter Planning
2. Create planning branch and produce 26 docs
3. Harden A1 with factor-interface dependency
4. Harden B1 with FactorInvocationResponse payload and blocked-output filtering
5. Merge in order: Factor Library → A1 → B1

## Evidence Summary
- Parent baseline: d02b60c9 (8 canonical intents, 7 forbidden, Batch3 F21-F34)
- A1: 0/8 intents covered, 0/8 factor components covered → MISSING
- B1: 0/8 intents in node/edge contracts → MISSING
- C1: generic sandbox evidence, does not need rework → ACCEPTED

## Human must decide. No auto-decision. No auto-merge.

> Factor Interface | Impact Review | Decision Brief | Level 5 BLOCKED