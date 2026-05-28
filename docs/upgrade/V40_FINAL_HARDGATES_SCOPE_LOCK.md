# V40 Final Hard Gates Scope Lock

## Three Upgrade Hard Gates

### 1. ZC40 LimitBoardFillabilityGate
- One-price limit-up boards: NOT_FILLABLE → no new entry
- Open board chase: OPEN_BOARD_CONFIRMATION_REQUIRED or CHASE_RISK
- Consecutive limit-up decay: integrate with ZC35 residual_power

### 2. ZC45 ProxyHedgeStressTest
- Correlation stability test under liquidity crisis scenarios
- May NOT claim Market Neutral
- Defensive assets: preview only, no auto-allocation
- Tail hedge: simulation only, no real orders

### 3. Runtime LLMProviderFailoverPolicy
- LLM/API failure: NO new judgment generation
- Cached facts: must be marked stale
- Stale facts: only DATA_INSUFFICIENT / DEGRADED output
- IRF pipeline: must degrade gracefully, never crash
- Audit trail: failover_trace + cache_trace + stale_data_trace required

## Scope of Each Hard Gate
Each gate is enabled across all batches (0-5). Any module in any batch that
interacts with limit boards, proxy hedging, or LLM calls must pass the
corresponding gate check.

## Out of Scope
- Real trading
- Broker execution
- Market Neutral claims
- LLM subjective scores
- Production strategy modification
