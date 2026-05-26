# Working Context Contract v1.0 — Event-Derived Context

## Fields

context_id, context_type, ticker, chain, sector, role, event_ids, summary, created_at

## Safety

- Read-only from EventStore events
- No Hermes memory write
- No real Z9 write
- No auto calibration
- No real trade
