# ZC35 CATALYST LIFECYCLE PROTOCOL V10

## Definition
ZC35 identifies and tracks the lifecycle of catalytic events,
not hot topics, not market sentiment, not momentum.

## Lifecycle States
1. PRE_EVENT: event announced but not yet occurred
2. EVENT_ACTIVE: event is occurring or within impact window
3. POST_EVENT_DECAY: event passed, impact decaying
4. EXHAUSTED: no remaining catalytic power

## Residual Power
- Decays exponentially from 1.0 at event peak
- Half-life depends on event evidence_level
- Sell-on-news risk increases as residual power drops below 0.3

## Evidence Levels
- A: Official announcement/financial report/exchange filing
- B: Authoritative media/industry chain confirmation
- C: General media/institutional interpretation
- D: Social media rumor/topic speculation (WATCH_ONLY)

## Forbidden
- catalyst_score (LLM subjective float)
- AUTO_BUY / AUTO_SELL based on catalyst
- Promotion of D-level evidence to trading signal
