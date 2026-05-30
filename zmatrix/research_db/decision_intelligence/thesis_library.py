"""J-1: Thesis Library — hypothesis register + verdict tracking."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

class ThesisVerdict(str, Enum): HYPOTHESIS="HYPOTHESIS"; CONFIRMED="CONFIRMED"; REJECTED="REJECTED"; PARTIAL="PARTIAL"; UNTESTED="UNTESTED"

@dataclass
class ThesisEntry:
    thesis_id: str; statement: str; ticker: str; proposer: str = "research_os"
    evidence: list = field(default_factory=list); verdict: str = "UNTESTED"
    confidence: float = 0.0; created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class ThesisLibrary:
    def __init__(self): self._theses: list[ThesisEntry] = []
    def propose(self, thesis_id: str, statement: str, ticker: str) -> ThesisEntry:
        e = ThesisEntry(thesis_id=thesis_id, statement=statement, ticker=ticker); self._theses.append(e); return e
    def confirm(self, thesis_id: str, evidence: list) -> ThesisEntry | None:
        for t in self._theses:
            if t.thesis_id == thesis_id: t.verdict = ThesisVerdict.CONFIRMED.value; t.evidence = evidence; t.confidence = min(1.0, len(evidence)*0.2); return t
        return None
    def reject(self, thesis_id: str, reason: str) -> ThesisEntry | None:
        for t in self._theses:
            if t.thesis_id == thesis_id: t.verdict = ThesisVerdict.REJECTED.value; t.evidence.append(reason); return t
        return None
    def by_ticker(self, ticker: str) -> list[ThesisEntry]: return [t for t in self._theses if t.ticker == ticker]
    def by_verdict(self, verdict: str) -> list[ThesisEntry]: return [t for t in self._theses if t.verdict == verdict]
    def summary(self) -> dict:
        return {"total":len(self._theses), "confirmed":len(self.by_verdict("CONFIRMED")),
                "rejected":len(self.by_verdict("REJECTED")), "untested":len(self.by_verdict("UNTESTED")), "production_allowed":False}
