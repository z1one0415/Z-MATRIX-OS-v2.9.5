<!-- allowlist: forbidden-token-definition -->
# V40 FINAL PATCH NOTES

## Version
v4.0-FINAL-HARDGATES RC1 (Batch 0-5)

## Based On
v3.5.20 Research OS RC (commit dc4b980)
V4.0-0.6 Platform Governance Hardening (commit 11b0dd6)

## Key Additions
1. ZC40 LimitBoardFillabilityGate — A-share one-price board tradability hard gate
2. ZC45 ProxyHedgeStressTest — correlation/liquidity stress test for proxy hedges
3. Runtime LLMProviderFailoverPolicy — LLM/API failure degradation hard gate
4. Parser-Scorer Split enforcement — LLM reads world, Z-MATRIX computes world
5. Research Council 12-Seat Skill Pack (Batch 2)
6. Report Template Library (Batch 2)
7. DataForge + FactorFactory (Batch 3)
8. ExecutionQuality + AccountGovernance (Batch 4)
9. System Cockpit + Audit + IRF (Batch 5)

## Safety Baseline
- real_trade_allowed: False
- broker_order_allowed: False
- runtime_enabled: False
- auto_buy/sell: False
- production_strategy_modified: False
- classifier_production_modified: False
- market_neutral_claim: BLOCKED
- LLM_subjective_float_score: BANNED
