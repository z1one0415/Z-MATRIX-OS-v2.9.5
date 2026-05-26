# EventStore Contract v1.0 — Unified Event Ledger

## Purpose

EventStore is the first living bone of v3.0.
It is a unified, append-only, auditable event ledger.

## Safety

Local EventStore is an audit ledger, not Z9 long-term memory.
EventStore writes do not equal strategy evolution.
MemoryCandidateEvent is candidate only — never auto-activated.
CalibrationEvent is candidate only — never auto-tunes.
PromptPatchEvent is candidate only — never auto-injected.
Long-term memory writes must wait for Approval-Required Reflection Loop.

## Boundaries

- No real trade
- No broker order
- No real Z9 write
- No Hermes memory write
- No auto calibration
- No prompt auto injection
- Local EventStore write only
