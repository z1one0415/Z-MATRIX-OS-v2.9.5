# Tail-Risk Autonomic Gates Preview Architecture v1.0

## Goal

Establish the v3.0 immune system preview layer.

## Chain

MarketSignals → TailRiskGates → TailRiskControllerPreview → RiskIsolationPreview → RiskEvent → EventStore

## Gates

- LIMIT_DOWN_BLACKHOLE
- DOMESTIC_LIQUIDITY_CRASH
- HIBERNATE_MODE
- WAKEUP_PROBATION
- D_MATRIX_FREEZE
- BMO_RISK_ISOLATION_UNIT

## Not In Scope

- No real trade
- No auto sell / auto buy / auto position close
- No broker connection
- No account modification
- No Hermes memory write
- No real Z9 write
