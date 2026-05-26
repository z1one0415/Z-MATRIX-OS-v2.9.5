# Event Lineage v1.0

## Fields

- source_event_id: optional reference to originating event
- parent_event_id: optional reference to parent event in lineage chain

## Tracing

trace_event_lineage() walks upward via parent_event_id.
Cycle detection: visited set.
Missing parent: stops and marks missing_parent=True.
If no parent_event_id, the event is a root event.

## Rules

- source_event_id and parent_event_id must be 32-char hex when present
- Lineage is tree-structured (not DAG) — parent_event_id forms a chain
- A root event is one with parent_event_id=None

## Lineage Example

```
ResearchEvent (002472 chain_analysis)
→ RoleClassificationEvent (A_LONG_CORE)
→ PaperDecisionEvent (paper_trade allowed)
→ PaperLedgerEvent (BUY 300)
→ OutcomeBackfillEvent (T5: +3.2%)
→ MistakeAttributionEvent (entry price too high)
```
