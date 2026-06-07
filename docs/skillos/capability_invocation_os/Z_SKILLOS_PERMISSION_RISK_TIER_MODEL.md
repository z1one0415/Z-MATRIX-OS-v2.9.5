# Z-SkillOS Permission Risk Tier Model

## Status

Z_SKILLOS_PERMISSION_RISK_TIER_MODEL_READY

## Scope

FUTURE_PLAN_ONLY. Tier 0–5 classification for all Z-MATRIX capability invocations.

## Tier Definitions

| Tier | Name | Permitted | Requires | Example |
|:--:|:--|:--|:--|:--|
| T0 | docs-only | Read, summarize, format | None | Report gen |
| T1 | analysis-only | Compute, score, rank | Evidence | Z2 research |
| T2 | code/local-repo | Generate, test, verify, commit | Permission + Evidence | GitHub patch |
| T3 | high-impact-advisory | Investment recommendations | Permission + Human + Evidence | Z8 advisory |
| T4 | external-side-effects | Write files, send messages | Permission + Human + Evidence + Rollback | File export |
| T5 | blocked | broker, real_trade, fail-closed | NEVER GRANTED | Trading |

## Escalation Matrix

| Current | → T5 | → T4 | → T3 | → T2 | → T1 |
|:--:|:--:|:--:|:--:|:--:|:--:|
| T0 | BLOCKED | BLOCKED | Human | Permission | Auto |
| T1 | BLOCKED | BLOCKED | Human | Permission | — |
| T2 | BLOCKED | BLOCKED | Human | — | — |
| T3 | BLOCKED | BLOCKED | — | — | — |
| T4 | BLOCKED | — | — | — | — |
| T5 | N/A | N/A | N/A | N/A | N/A |

## No implementation. Level 5 remains BLOCKED.
