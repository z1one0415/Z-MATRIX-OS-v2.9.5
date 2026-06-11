# Risk Acknowledgement

## Status: RISK_ACK_REQUIRED_BEFORE_RC_MERGE | Must acknowledge: true

## Risk Items
- Visual QA is source-level/contract-level only, not browser render QA
- Browser render QA has not been executed
- Frontend runs in mock mode by default
- Readonly API mode prepared but not live-backend integrated
- No production, broker, real_trade, runtime, runner, paper trading, alpha, promotion, F8 authorized

## Safety: Production/Broker/RealTrade=BLOCKED | Runtime=DISABLED_DEFAULT | Runner/PaperTrading=DISABLED | F8=BLOCKED
