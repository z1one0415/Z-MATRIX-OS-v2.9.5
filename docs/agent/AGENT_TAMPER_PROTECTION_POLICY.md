# Agent Tamper Protection Policy

## Scanned Patterns
real_trade_allowed=True | broker_order_allowed=True | runtime_enabled=True | auto_buy_allowed=True | auto_sell_allowed=True | production_allowed=True | production_strategy_modified=True | allowed_scopes=["*"] | requires_human_review=false | subprocess | os.system | eval( | exec( | curl | api_key | token | secret

## Rules
- Tamper guard violation → BLOCK | Self-elevation → BLOCK
- Secret pattern detected → REDACT + BLOCK | Workspace escape → BLOCK
