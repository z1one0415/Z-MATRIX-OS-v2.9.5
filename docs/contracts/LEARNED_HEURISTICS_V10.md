# Learned Heuristics Contract v1.0 — Preview Only

## Fields

heuristic_id, source_event_id, title, rule, scope, confidence, evidence_count, last_validated_at, decay_status, status

## Status Fields

- decay_status = ACTIVE / STALE / EXPIRED
  Used for heuristic decay and validity tracking.
- status = DRAFT / ACTIVE / RETIRED / SUPERSEDED etc.
  Used for lifecycle management.

PromptPatchPreview must prioritize decay_status=ACTIVE.
If decay_status is missing, it may fall back to status for backward compatibility.

## Safety

- Preview only
- No auto-add to long-term memory
- No prompt auto injection
- No Hermes memory write
- No real trade
- No auto calibration
