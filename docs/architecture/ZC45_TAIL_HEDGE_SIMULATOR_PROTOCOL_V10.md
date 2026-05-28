# ZC45 TAIL HEDGE SIMULATOR PROTOCOL V10

## Definition
Tail hedge simulation estimates portfolio impact under extreme scenarios.
It is paper-only. It does NOT generate real orders.

## Scenarios
1. 2008 Global Financial Crisis
2. 2015 China A-share crash
3. 2020 COVID crash
4. 2024 liquidity event

## Output
- scenario_id
- portfolio_impact_pct
- hedge_effectiveness
- correlation_breakdown_flag
- human_review_required

## Forbidden
- AUTO_ORDER from simulation
- REAL_HEDGE_ORDER
- Claim of protection or guarantee
