# No Production Boundary

## Hard Boundaries

- ResearchDB never directly executes trades.
- ResearchDB never connects to a broker.
- ResearchDB never generates broker_order.
- ResearchDB never starts a runtime daemon.
- ResearchDB never performs auto_buy or auto_sell.

## Global Safety Flags

```json
{
  "real_trade_allowed": false,
  "broker_order_allowed": false,
  "runtime_enabled": false,
  "auto_buy_allowed": false,
  "auto_sell_allowed": false,
  "production_allowed": false,
  "paper_only": true,
  "human_review_required": true
}
```

## Enforcement

Any module that violates these boundaries is blocked from Phase promotion.
The verify script checks all zmatrix/research_db/ for forbidden boolean flags.
