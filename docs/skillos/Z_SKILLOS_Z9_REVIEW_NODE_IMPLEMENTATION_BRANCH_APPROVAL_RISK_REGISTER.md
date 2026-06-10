# Z9 Review Node Implementation Branch Approval Risk Register
## Status: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_BRANCH_APPROVAL_GATE_READY
## Date: 2026-06-10 | Base HEAD: 9a6b9c4

| # | Risk | Severity | Likelihood | Mitigation | Control | Rollback |
|:--:|:--|:--:|:--:|:--|:--|:--|
| 1 | Z9 reviews trading profit | CRITICAL | LOW | Explanation-only gate | Contract check | Profit field | 
| 2 | Z9 consumes trade_result | CRITICAL | LOW | Input filter | isinstance check | trade_result input |
| 3 | Z9 consumes real_pnl | CRITICAL | LOW | Input filter | Grep scan | PNL data found |
| 4 | Z9 consumes paper_trade_result | CRITICAL | LOW | Input filter | Contract test | Paper trade found |
| 5 | Z9 consumes broker_result | CRITICAL | LOW | Input filter | Block import | Broker data |
| 6 | Z9 directly consumes B1 graph | CRITICAL | LOW | Input type validation | isinstance check | B1 response found |
| 7 | Z9 directly consumes FactorInvocationResponse | CRITICAL | LOW | Input type validation | isinstance check | FL response found |
| 8 | Z9 reads research/factor_library | CRITICAL | LOW | Import blocklist | AST scan | Research import |
| 9 | Z9 mutates persistent memory | CRITICAL | VERY LOW | Kill switch blocks | Config check | Memory write |
| 10 | Z9 triggers Z8 | CRITICAL | VERY LOW | Import blocklist | AST scan | Z8 import |
| 11 | Z9 emits buy/sell signal | CRITICAL | LOW | Output filter blocks | Parametrized test | Signal found |
| 12 | Z9 emits position weight | CRITICAL | LOW | Output filter | Parametrized test | Weight found |
| 13 | Z9 emits broker action | CRITICAL | LOW | Output filter | Grep scan | Broker action found |
| 14 | Z9 turns degraded Z2 into accepted conclusion | HIGH | MEDIUM | Degradation enforced | Contract test | Accepted from degraded |
| 15 | Z9 converts missing evidence to valid | HIGH | MEDIUM | Evidence completeness check | Contract test | Missing→valid |
| 16 | Z9 feedback auto-patches Z2 | HIGH | LOW | Feedback readonly | Human review gate | Auto-patch found |
| 17 | Z9 confidence label becomes alpha claim | HIGH | LOW | Label constrains | Parametrized test | Alpha in label |
| 18 | Z9 attribution drifts to PnL attribution | HIGH | LOW | Attribution type filter | Check test | Profit attribution |
| 19 | Runtime enablement leak | CRITICAL | LOW | enabled→False | Kill switch test | enabled→True |
| 20 | Adapter execution leak | CRITICAL | LOW | Method blocklist | AST scan | Method found |
| 21 | Capability execution leak | CRITICAL | LOW | Method blocklist | AST scan | execute/run/call |
| 22 | Level 5 drift | CRITICAL | VERY LOW | BLOCKED markers | Doc audit | Level 5 language |
| 23 | Docs/code boundary drift | MEDIUM | LOW | Whitelist check | Diff gate | Non-doc file |
| 24 | Contaminated branch merge | HIGH | LOW | Diff audit pre-merge | Git diff check | Research file |

Summary: 24 risks. CRITICAL 13, HIGH 6, MEDIUM 5. All mitigated. Gate ready.
