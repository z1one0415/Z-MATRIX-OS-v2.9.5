# EventStore Architecture v1.0

EventStore is the first living bone of v3.0.

## Goal

- Unified event ledger
- ID lineage
- Append-only audit
- Local SQLite/JSONL
- No real Z9 write
- No auto evolution

## Event Chain Example

```
ResearchEvent
→ CandidateReviewEvent
→ RoleClassificationEvent
→ PaperDecisionEvent
→ PaperLedgerEvent
→ OutcomeBackfillEvent
→ MistakeAttributionEvent
→ MemoryCandidateEvent
→ HumanApprovalEvent
```

## Safety

- No real trade
- No broker order
- No real Z9 write
- No Hermes memory write
- No auto calibration
- No prompt auto injection
- Local EventStore write only
