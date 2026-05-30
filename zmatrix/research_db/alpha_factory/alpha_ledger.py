"""Phase 4-F6: Alpha Ledger — immutable record: who discovered, when, validation results, retirement, promotion."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class LedgerEntry:
    entry_id: str; factor_id: str; event_type: str  # DISCOVERED, VALIDATED, PROMOTED, RETIRED
    timestamp: str; details: dict = field(default_factory=dict)
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class AlphaLedger:
    def __init__(self): self._entries: list[LedgerEntry] = []

    def record(self, factor_id: str, event_type: str, details: dict = None) -> LedgerEntry:
        entry = LedgerEntry(entry_id=f"{factor_id}-{event_type}-{len(self._entries)+1:03d}",
                           factor_id=factor_id, event_type=event_type,
                           timestamp=datetime.now(timezone.utc).isoformat(), details=details or {})
        self._entries.append(entry); return entry

    def get_history(self, factor_id: str) -> list[LedgerEntry]:
        return [e for e in self._entries if e.factor_id == factor_id]

    def list_all(self) -> list[LedgerEntry]: return list(self._entries)
    def count(self) -> int: return len(self._entries)

    def get_by_event(self, event_type: str) -> list[LedgerEntry]:
        return [e for e in self._entries if e.event_type == event_type]
