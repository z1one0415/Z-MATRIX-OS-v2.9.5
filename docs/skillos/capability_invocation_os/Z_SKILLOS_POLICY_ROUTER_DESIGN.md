# Z-SkillOS Policy Router Design

## Status

Z_SKILLOS_POLICY_ROUTER_DESIGN_READY

## Scope

FUTURE_PLAN_ONLY. Intent → capability → tier → gate → execution. No implementation.

## Router Pipeline

```
intent_classification → capability_selection → risk_tiering → policy_gate → human_approval → execution_mode → deny_or_degrade
```

## Execution Mode Tiers

| Tier | Mode | Example |
|:--:|:--|:--|
| T0 | docs-only | Report generation, summarization |
| T1 | analysis-only | Scoring, ranking, computation |
| T2 | code/local-repo | Code generation, test, verify |
| T3 | high-impact-advisory | Investment recommendations |
| T4 | external-side-effects | File writes, message sends |
| T5 | blocked | broker, real_trade, fail-closed |

## Tier Escalation Rules

| From | To | Trigger |
|:--:|:--:|:--|
| T0 | T1 | Output includes computation |
| T1 | T2 | Output includes code |
| T2 | T3 | Involves investment decision |
| T3 | Human gate | Always requires human |
| T4 | Human gate | Always requires human |
| T5 | BLOCKED | Never reached |

## No implementation. Level 5 remains BLOCKED.
