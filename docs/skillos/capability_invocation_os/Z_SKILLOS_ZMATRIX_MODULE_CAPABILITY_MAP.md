# Z-SkillOS Z-MATRIX Module Capability Map

## Status

Z_SKILLOS_ZMATRIX_MODULE_CAPABILITY_MAP_READY

## Scope

FUTURE_PLAN_ONLY. Maps Z-MATRIX modules to capabilities, risk tiers, and adapter status.

## Module Capability Matrix

| Module | Primary Capabilities | Risk Tier | Allowed Mode | Forbidden Mode | Adapter | Evidence |
|:--|:--|:--:|:--|:--|:--:|:--:|
| Z2 信息熔炉 | Industry chain research, stock scoring | T2 | analysis-only | trading | Planning | Required |
| Z8 投资执行 | Position management, execution | T3 | advisory-only | broker/trade | Planning | Required |
| Z9 预测引擎 | Alpha prediction, calibration | T2 | analysis-only | trading | Planning | Required |
| V3 量化引擎 | Factor signals, risk metrics | T2 | analysis-only | trading | Planning | Required |
| B-Matrix | Bottom-position classification | T2 | analysis-only | execution | Planning | Required |
| D-Matrix | Dark horse detection | T2 | analysis-only | execution | Planning | Required |
| R-Matrix | Rotation candidate ranking | T2 | analysis-only | execution | Planning | Required |
| World Blocks OS | World-building, assembly-line design | T2 | docs/code | production | Planning | Required |
| Deal Compass | Deal flow analysis, negotiation prep | T2 | analysis-only | trading | Planning | Required |
| MissNail Model | Business model analysis | T2 | analysis-only | execution | Planning | Required |
| GitHub Engineering | Code, patches, audits | T2 | repo-write | external-write | Planning | Required |
| Doc/HTML Report Gen | Report generation | T1 | docs-only | code-execution | Planning | Required |

## Risk Tier Quick Reference

| Tier | Level | Capabilities |
|:--:|:--|:--|
| T0 | docs-only | Read, summarize, format |
| T1 | analysis-only | Compute, score, rank |
| T2 | code/local | Generate, test, verify |
| T3 | advisory | Recommend, warn, escalate |
| T4 | external | Write files, send messages |
| T5 | blocked | broker/real_trade/fail-closed |

## No implementation. Level 5 remains BLOCKED.
