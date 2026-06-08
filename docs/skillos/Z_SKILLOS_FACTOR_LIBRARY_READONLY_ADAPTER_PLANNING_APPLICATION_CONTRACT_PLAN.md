# Factor Library Read-Only Adapter Planning — Application Contract Plan

## Status: Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING_APPLICATION_CONTRACT_PLAN_READY
Branch: plan/...factor-library-adapter | Base: 22252711 | Level 5: BLOCKED

## Scope
Plan the FactorApplicationContract read-only adapter component. Contract defines what modes, outputs, and downstream consumers are allowed for a factor. No execution.

### Contract Properties (future read-only)
- allowed_application_modes: 8 canonical readonly intents (REGISTRY_READ through COMPOSITION_GRAPH_DRY_PLAN)
- blocked_application_modes: 7/7 (ALPHA_SIGNAL, PORTFOLIO_WEIGHT, ORDER_SIGNAL, PAPER_TRADING, BROKER_RUNTIME, REAL_TRADE, PRODUCTION)
- blocked_outputs: 5/5 (buy_signal, sell_signal, position_weight, expected_return_claim, alpha_claim)
- blocked_downstream_consumers: 4/4 (Z8_EXECUTION_RUNTIME, V3_TRADE_SANDBOX, BROKER, REAL_TRADE)
- execution_requested: const false
- promotion_allowed: const false
- alpha_claim_allowed: const false
- production: BLOCKED
- broker_runtime: BLOCKED
- real_trade: BLOCKED

### Contract Verification Logic
1. Check requested intent is in allowed_application_modes
2. Check no blocked_outputs in request
3. Check no blocked_downstream_consumers in request
4. Check execution_requested=false
5. Check promotion_allowed=false
6. Check alpha_claim_allowed=false
7. DENY if any check fails

### Implementation Plan (future)
- FactorApplicationContract class in zmatrix_adapters/factor_library/contract.py
- Methods: verify_contract, get_allowed_modes, get_blocked_modes (read-only)
- Tests in test_contract.py

## Parent Interface: d02b60c9. Contract properties defined per Batch3 factor.

## Boundary: No implementation. Level 5 BLOCKED.

## Forbidden: Same as OVERVIEW. No contract bypass.

## Proof: All contract fields documented. 7/7 blocked modes. 5/5 blocked outputs. 4/4 blocked downstream.

## Next: Invocation Request/Response Plan.

> Factor Library | Planning | Application Contract | FUTURE_PLAN_ONLY | Level 5 BLOCKED