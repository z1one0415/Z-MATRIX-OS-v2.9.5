# G18 Final Decision Envelope v1.1

## Priority Rules
1. G09 sell_decision > G18 probability
2. G09 hard_blocks prevent paper entry
3. G11: STRONG_WARNING_ONLY, never hard veto
4. G14: provenance only
5. Paper actions require Z16/G17 confirmation
6. No BUY/SELL/AUTO_TRADE/MARKET_ORDER

## Output Fields
- decision_version: "v1.1"
- entry_intent: WAIT|WATCH|PAPER_TRACK|PAPER_PROBE_ELIGIBLE_PENDING_Z16_Z17
- exit_intent: None or REDUCE_CORE etc
- paper_action: PAPER_TRACK or None
- required_confirmations: [Z16_PRICE_GATE, G17_ACCOUNT_CONFIRMATION]
- blocking_reasons: reasons that forced entry to WAIT
- risk_warnings: G11 warnings only
- provenance: g09/g08/g11/g14/z16/g17
- forbidden_real_trade_checked: True


## G09 Evidence Input

Supports:
1. Flat: g09.position_action = REDUCE_CORE
2. Nested: g09.sell_decision.position_action = REDUCE_CORE

Availability: g09.available==True OR g09.status in (PASS, DEGRADED)

Adapter must output: available, source, version, status, r_score,
r_resonance_status, r_action_cap, entry_action_cap, exit_alert,
hard_blocks, conflicts, sell_decision, position_action

Example: docs/contracts/examples/g18_final_decision_v11_example.json
