"""EventStore v1.0 — Unified Event Ledger (v2.9.11-dev)

EventStore is the first living bone of v3.0.
It provides a unified, append-only, auditable event ledger
with ID lineage, local SQLite/JSONL persistence, and safety boundaries.

Safety invariants:
- No real trade
- No real Z9 write
- No Hermes memory write
- No auto calibration
- No prompt auto injection
- Local EventStore write only
"""
from __future__ import annotations

__version__ = "EVENT_STORE_V10"
