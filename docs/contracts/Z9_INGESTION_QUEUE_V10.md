# Z9 Ingestion Queue v1.0 — Contract Freeze

## Input
- Z9_CALIBRATION_SAMPLE v1.0

## Output
- queue_version: v1.0
- queue_type: Z9_INGESTION_QUEUE_ITEM
- idempotency: sha256(sample_id+ticker+version+record_ref), dedup=ticker_sample_id
- state: PENDING_REVIEW | WAITING_MARKET_DATA | READY_FOR_REVIEW | REJECTED
- write_policy: queue_write_allowed=False, z9_write_allowed=False
- forbidden_real_trade_checked: True

## Rules
- No real queue write
- No real Z9 write
- No real trade
- D-3 may define real outcome backfill
- D-4 may define parameter calibration
