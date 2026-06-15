# G18 Context-Aware Risk Rules v1.0

## Core Principles
- probability = conviction, not trade action
- action label = safety-capped expression
- risk overlay = admissibility filter
- new entry and existing holding must be separated
- user cost line != market support line
- R11 = position management review only, not buy signal

## Gate Changes (v1.0 → v2.0)
- R3: now only triggers on planned entry price breach, not existing holding cost
- R6: market structure only (R4+R5), excludes personal cost line
- R7: split into R7a_BLACKSWAN, R7b_SCHEDULED_MACRO, R7c_EVENT_DAY
- R11: NEW — position oversold review flag (no penalty, no BUY/ADD)

## Safety Invariants
- No BUY/SELL/ADD/AUTO_TRADE/MARKET_ORDER
- Formal alpha = 0
- Promotion = BLOCKED
- Runner/Execution = BLOCKED
- Production/Broker/RealTrade = BLOCKED
