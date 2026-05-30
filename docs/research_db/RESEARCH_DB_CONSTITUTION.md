# ResearchDB Constitution

## Identity

ResearchDB is the long-term research data foundation of Z-MATRIX-OS.

- ResearchDB is NOT a production database.
- ResearchDB is NOT a broker database.
- ResearchDB does NOT generate real trade orders.
- All ResearchDB data defaults to research_only / paper_only.

## 10 Constitutional Principles

1. **事实先于结论** — Data precedes conclusions.
2. **数据先于叙事** — Evidence precedes narratives.
3. **时间戳先于回测** — As-of timestamps precede backtesting claims.
4. **证据等级先于评分** — Evidence grade precedes numerical scores.
5. **结果验证先于规则晋级** — Outcome validation precedes rule promotion.
6. **单案例不得形成规则** — A single case forms a lesson, not a rule.
7. **当前截面不得伪装历史PIT** — Current snapshots must not masquerade as historical PIT.
8. **Paper-only不得变成production** — Research output stays research.
9. **人工裁决高于系统自动晋级** — Human adjudication overrides auto-promotion.
10. **所有数据变更必须可审计** — All data mutations must be auditable.

## Production Boundary

```
real_trade_allowed: FALSE
broker_order_allowed: FALSE
runtime_enabled: FALSE
auto_buy_allowed: FALSE
auto_sell_allowed: FALSE
production_allowed: FALSE
paper_only: TRUE
human_review_required: TRUE
```
