# ZC45 PROXY HEDGE DEFENSIVE ALLOCATION PROTOCOL V10

## Definition
ZC45 is a defensive allocation preview system. It is NOT:
- A short-selling system
- A Market Neutral strategy
- An auto-allocation system
- A real hedge execution system

## Allowed
- beta_exposure measurement
- defensive_allocation_preview (paper-only)
- hedge_proxy_suitability check
- tail_hedge_simulation (paper-only)
- beta_reduction_review
- Stress test pass/fail

## Forbidden
- MARKET_NEUTRAL claims
- AUTO_ALLOCATE / REAL_HEDGE_ORDER
- Absolute return promises
- Real ETF/futures/options orders
- hedge_score (LLM subjective float)

## Stress Test
ProxyHedgeStressTest must run before any allocation preview:
1. CorrelationBreakdownDetector: correlation during last 3 liquidity events
2. LiquidityCrashScenario: 2008/2015/2020/2024 scenario replay
3. DefensiveAssetStressReport: all defensive assets simultaneously stressed
