# Z9 Calibration Sample v1.0 — Contract Freeze

## Input
- G18 paper_execution_record v1.0

## Output
- sample_version: v1.0
- sample_type: Z9_CALIBRATION_SAMPLE
- source_record: reference to paper record
- prediction_snapshot: probability, horizon, action_proposal, confidence
- decision_snapshot: entry/exit_intent, paper_action, blocking_reasons, risk_warnings
- evidence_snapshot: upstream_evidence_available, missing_sources, conflict_summary
- review_plan: needs_future_review, review_horizons (T1/T5/T20), expected_fields
- outcome_placeholder: all None, decision_outcome=PENDING_REVIEW, review_status=WAITING
- calibration_hooks: ev/r_matrix/g18 all False, requires_future_outcome=True
- z9_write_policy: write_allowed=False, write_status=DEFERRED_NOT_CONNECTED
- forbidden_real_trade_checked: True

## Rules
- No real Z9 write
- No real trade actions
- Forbidden check on action fields only, not str(record)
- D-2 may define Z9 ingestion queue
- D-3 may define real outcome backfill
- D-4 may define parameter calibration automation
