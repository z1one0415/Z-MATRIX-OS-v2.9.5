# V40 ZC35 Catalyst Scope Lock

ZC35 is NOT a hot-topic chasing system. It is a catalyst lifecycle and expected-exhaustion recognition system.

## Allowed Outputs
- catalyst_status
- lifecycle_state: PRE_EVENT / EVENT_ACTIVE / POST_EVENT_DECAY / EXHAUSTED
- sell_on_news_risk: LOW / MEDIUM / HIGH
- residual_power: 0.0 - 1.0
- review_signal: PAPER_ONLY / OBSERVE / NO_ACTION
- evidence_level: A / B / C / D
- human_review_required: True/False

## Forbidden Outputs
- BUY / SELL / HOLD / ADD / REDUCE
- AUTO_BUY / AUTO_SELL
- target_price / target_weight / position_size
- catalyst_score / event_power_score (subjective float)
- REAL_ORDER / BROKER_ORDER

## Mandatory Rules
1. scheduled_event_without_surprise → DOWNGRADED to OBSERVE
2. process_event_without_result → DOWNGRADED to OBSERVE
3. cross-sector weak correlation → NOT a catalyst
4. entity_relevance_gate_enabled: True
5. sell_on_news_detector_enabled: True
6. catalyst_direct_trade_allowed: False
7. LLM must NOT output subjective float scores
