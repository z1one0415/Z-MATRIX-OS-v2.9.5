# Z-SkillOS Frontend Handoff Scope Lock

## Status: SCOPE_LOCKED

## In Scope
- Dashboard home page with summary cards
- Capability Invocation OS viewer
- Factor Library browser (seal status only)
- Composition Graph visualizer
- Research Report Node viewer
- Z9 Review Node viewer
- Evidence Chain viewer
- Run State Registry
- Gate State Registry
- Audit Trail viewer
- Settings / Safety Boundary

## Out of Scope
- Real-time trading dashboard
- Order entry/modification
- Position management
- PnL tracking
- Broker API integration
- Production deployment config
- Paper trading engine
- Alpha signal generation
- Factor promotion UI
- F8 advancement UI

## Permissions
- All dangerous permissions default to FALSE
- runtime_enabled = false
- runner_enabled = false
- paper_trading_allowed = false
- broker_action_allowed = false
- production_allowed = false
- real_trade = BLOCKED

## Next
A1-A6 agent waves execute in parallel. Integration merge after all waves pass.
