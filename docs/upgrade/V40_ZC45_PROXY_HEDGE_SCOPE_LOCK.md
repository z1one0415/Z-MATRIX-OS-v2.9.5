# V40 ZC45 Proxy Hedge Scope Lock

ZC45 is NOT a short-selling system, NOT Market Neutral, NOT an auto-allocation system.

## Allowed Outputs
- beta_exposure: float
- defensive_allocation_preview: dict (paper-only)
- hedge_proxy_suitability: SUITABLE / PARTIAL / UNSUITABLE
- tail_hedge_simulation: dict (paper-only)
- beta_reduction_review: str
- human_review_required: True

## Forbidden Outputs
- MARKET_NEUTRAL / ABSOLUTE_RETURN
- REAL_HEDGE_ORDER / AUTO_ALLOCATE
- hedge_score / defensive_score (subjective float)
- target_hedge_ratio / auto_rebalance
- REAL_ORDER / BROKER_ORDER

## Mandatory Rules
1. ProxyHedgeStressTest: enabled
2. CorrelationBreakdownDetector: enabled
3. LiquidityCrashScenario: enabled
4. DefensiveAssetStressReport: enabled
5. BetaBudgetGovernor: enabled
6. market_neutral_claim_allowed: False
7. defensive_allocation_auto_execute: False
8. tail_hedge_real_order_allowed: False
9. hedge_proxy_suitability_checked: True
