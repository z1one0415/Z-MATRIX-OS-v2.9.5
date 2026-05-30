"""P5.5-E: Research Truth Ledger — hypothesis→validation→retirement graveyard/archive/winners."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

class TruthVerdict(str, Enum):
    HYPOTHESIS="HYPOTHESIS"; VALIDATED="VALIDATED"; REJECTED="REJECTED"
    RETIRED="RETIRED"; ARCHIVED="ARCHIVED"; WINNER="WINNER"

@dataclass
class TruthEntry:
    entry_id: str; hypothesis_id: str; statement: str
    verdict: str = "HYPOTHESIS"; evidence: list = field(default_factory=list)
    validated_by: list = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class ResearchTruthLedger:
    def __init__(self):
        self._hypotheses: list[TruthEntry] = []
        self._validated: list[TruthEntry] = []
        self._rejected: list[TruthEntry] = []
        self._archived: list[TruthEntry] = []
        self._winners: list[TruthEntry] = []

    def propose(self, hypothesis_id: str, statement: str) -> TruthEntry:
        e = TruthEntry(entry_id=f"HYP-{hypothesis_id}", hypothesis_id=hypothesis_id, statement=statement)
        self._hypotheses.append(e); return e

    def validate(self, hypothesis_id: str, evidence: list) -> TruthEntry | None:
        for h in self._hypotheses:
            if h.hypothesis_id == hypothesis_id:
                h.verdict = TruthVerdict.VALIDATED.value; h.evidence = evidence
                self._validated.append(h); self._hypotheses.remove(h); return h
        return None

    def reject(self, hypothesis_id: str, reason: str) -> TruthEntry | None:
        for h in self._hypotheses:
            if h.hypothesis_id == hypothesis_id:
                h.verdict = TruthVerdict.REJECTED.value; h.evidence = [reason]
                self._rejected.append(h); self._hypotheses.remove(h); return h
        return None

    def archive(self, hypothesis_id: str) -> TruthEntry | None:
        for lst in [self._hypotheses, self._validated, self._rejected]:
            for h in lst:
                if h.hypothesis_id == hypothesis_id:
                    h.verdict = TruthVerdict.ARCHIVED.value
                    self._archived.append(h); lst.remove(h); return h
        return None

    def declare_winner(self, hypothesis_id: str) -> TruthEntry | None:
        for h in self._validated:
            if h.hypothesis_id == hypothesis_id:
                h.verdict = TruthVerdict.WINNER.value
                self._winners.append(h); self._validated.remove(h); return h
        return None

    def summary(self) -> dict:
        return {"hypotheses": len(self._hypotheses), "validated": len(self._validated),
                "rejected": len(self._rejected), "archived": len(self._archived),
                "winners": len(self._winners), "production_allowed": False}
