# G18 Paper Execution Record v1.0

## Schema
- record_version: "v1.0"
- record_type: "PAPER_EXECUTION_RECORD"
- run_id, ticker, name, timestamp
- prediction: probability, horizon, action_proposal, confidence
- final_decision: full envelope
- conflict_summary: has_conflict, conflict_level, conflict_codes
- paper_execution: allowed, paper_action, entry_intent, exit_intent, action_cap, required_confirmations
- z9_calibration_hooks: needs_future_review, review_horizons, expected_fields
- forbidden_real_trade_checked: True


- upstream_evidence_available: copied from prediction.upstream_evidence.evidence_available
- missing_sources: copied from prediction.upstream_evidence.missing_sources

## Rules
- Conflict codes may contain words like SELL as semantic labels; forbidden action checks only apply to executable action fields.
- Forbidden real trade: targeted field check (entry_intent, exit_intent, paper_action, action_cap), NOT str(record) scan.

- No BUY/SELL/AUTO_TRADE/MARKET_ORDER
- paper_action=None → allowed=False
- Z9 hooks present but never written
- Preserves conflict codes from resolution
- Requires Z16/G17 confirmations for paper actions
