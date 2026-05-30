"""Phase 5: Portfolio Ledger — append-only lifecycle: CANDIDATE→VALIDATED→RESEARCH→APPROVED."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

class PortfolioStatus(str, Enum):
    CANDIDATE="CANDIDATE"; VALIDATED="VALIDATED"; RESEARCH="RESEARCH"; APPROVED="APPROVED"

@dataclass
class PortfolioEntry:
    entry_id: str; portfolio_id: str; event_type: str  # CREATED, VALIDATED, PROMOTED, SNAPSHOT
    from_status: str = ""; to_status: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    details: dict = field(default_factory=dict); audit_hash: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class PortfolioLedger:
    def __init__(self): self._entries: list[PortfolioEntry] = []

    def record(self, portfolio_id: str, event_type: str, from_status: str = "", to_status: str = "", details: dict = None) -> PortfolioEntry:
        e = PortfolioEntry(entry_id=f"{portfolio_id}-{event_type}-{len(self._entries)+1:03d}",
                          portfolio_id=portfolio_id, event_type=event_type,
                          from_status=from_status, to_status=to_status, details=details or {})
        import hashlib, json
        e.audit_hash = hashlib.sha256(json.dumps({"pid":portfolio_id,"event":event_type,"ts":e.timestamp},sort_keys=True).encode()).hexdigest()[:16]
        self._entries.append(e); return e

    def get_history(self, portfolio_id: str) -> list[PortfolioEntry]:
        return [e for e in self._entries if e.portfolio_id == portfolio_id]

    def current_status(self, portfolio_id: str) -> str:
        hist = self.get_history(portfolio_id)
        return hist[-1].to_status if hist else PortfolioStatus.CANDIDATE.value

    def list_all(self) -> list[PortfolioEntry]: return list(self._entries)
    def count(self) -> int: return len(self._entries)
