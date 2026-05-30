"""J-2: Decision Ledger — why buy/sell/pass, immutable record."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

class DecisionType(str, Enum): BUY="BUY"; SELL="SELL"; PASS="PASS"; ADD="ADD"; REDUCE="REDUCE"

@dataclass
class DecisionEntry:
    entry_id: str; ticker: str; decision_type: str; thesis_id: str = ""
    reason: str = ""; price: float = 0.0; quantity: int = 0; expected_holding_days: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    outcome_recorded: bool = False; outcome_verdict: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class DecisionLedger:
    def __init__(self): self._entries: list[DecisionEntry] = []
    def record(self, entry_id: str, ticker: str, decision_type: str, thesis_id: str = "", reason: str = "", price: float = 0.0, quantity: int = 0) -> DecisionEntry:
        e = DecisionEntry(entry_id=entry_id, ticker=ticker, decision_type=decision_type, thesis_id=thesis_id, reason=reason, price=price, quantity=quantity)
        self._entries.append(e); return e
    def by_ticker(self, ticker: str) -> list[DecisionEntry]: return [e for e in self._entries if e.ticker == ticker]
    def by_type(self, decision_type: str) -> list[DecisionEntry]: return [e for e in self._entries if e.decision_type == decision_type]
    def by_thesis(self, thesis_id: str) -> list[DecisionEntry]: return [e for e in self._entries if e.thesis_id == thesis_id]
    def record_outcome(self, entry_id: str, verdict: str) -> DecisionEntry | None:
        for e in self._entries:
            if e.entry_id == entry_id: e.outcome_recorded = True; e.outcome_verdict = verdict; return e
        return None
    def summary(self) -> dict:
        buy = len(self.by_type("BUY")); sell = len(self.by_type("SELL")); pas = len(self.by_type("PASS"))
        return {"total":len(self._entries),"buy":buy,"sell":sell,"pass":pas,"outcome_recorded":sum(1 for e in self._entries if e.outcome_recorded),"production_allowed":False}
