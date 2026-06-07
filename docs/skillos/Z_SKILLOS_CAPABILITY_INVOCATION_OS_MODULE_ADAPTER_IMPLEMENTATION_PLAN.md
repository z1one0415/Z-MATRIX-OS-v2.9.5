# Z-SkillOS Capability Invocation OS Module Adapter Implementation Plan

## Status
Z_SKILLOS_MODULE_ADAPTER_IMPLEMENTATION_PLAN_READY

## Scope
FUTURE_PLAN_ONLY. Adapter development wave plan. No adapter code.

## Wave 0: Docs/Report/Engineering (Planning Ready)
| Module | Capability | Complexity | Risk Tier | Status |
|:--|:--|:--:|:--:|:--:|
| Document Generation | Report format, render | Low | T1 | Planning |
| HTML Report Generation | HTML render, export | Low | T1 | Planning |
| GitHub Engineering | Code audit, patch, seal | Medium | T2 | Planning |

## Wave 1: Deal Compass / World Blocks (Planning Ready)
| Module | Capability | Complexity | Risk Tier | Status |
|:--|:--|:--:|:--:|:--:|
| Deal Compass | Deal flow, negotiation | Medium | T2 | Planning |
| World Blocks OS | Assembly-line design | Medium | T2 | Planning |

## Wave 2: Z2 / Z9 / V3 Research (Future Planning)
| Module | Capability | Complexity | Risk Tier | Status |
|:--|:--|:--:|:--:|:--:|
| Z2 信息熔炉 | Industry chain research | High | T2 | Future |
| Z9 预测引擎 | Alpha prediction | High | T2 | Future |
| V3 量化引擎 | Factor signals | High | T2 | Future |
| B/R/D-Matrix | Stock classification | High | T2 | Future |

## Wave 3: Z8 Advisory (Future Planning, No Real-Trade)
| Module | Capability | Complexity | Risk Tier | Forbidden |
|:--|:--|:--:|:--:|:--|
| Z8 投资执行 | Advisory only | Critical | T3 | broker/real_trade |

## Wave 4: Advanced Composition (Future Planning)
Cross-module composition, still no broker/real_trade.

## Adapter Requirements
- Separate approval: each Wave requires separate human approval
- No broker/real_trade: all adapters permanently exclude production paths
- Contract-first: adapter must satisfy skill contract before execution
- Rollback: each adapter must define rollback path

## No adapter code. Level 5 remains BLOCKED.
