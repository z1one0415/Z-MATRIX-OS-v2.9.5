"""V4.0-C2-1 DataForge depth modules"""
from __future__ import annotations
import hashlib, json
from dataclasses import dataclass, field

@dataclass
class EvidenceCard:
    evidence_id: str; ticker: str | None = None; trade_date: str | None = None
    source_id: str = ""; field_name: str = ""; field_value = None
    as_of_date: str = ""; pit_status: str = "UNKNOWN"; freshness_status: str = "UNKNOWN"
    quality_score: float = 0.0; usable_for_production: bool = False
    evidence_hash: str = ""
    def __post_init__(self): self.evidence_hash = evidence_hash_build(self)

def evidence_hash_build(card) -> str:
    payload = f"{card.evidence_id}|{card.ticker}|{card.field_name}|{card.field_value}|{card.as_of_date}"
    return hashlib.sha256(payload.encode()).hexdigest()[:16]

@dataclass
class PITSnapshot:
    snapshot_id: str; trade_date: str; as_of_date: str
    records: list = field(default_factory=list); pit_safe: bool = False
    usable_for_backtest: bool = False; production_allowed: bool = False

class CrossSourceValidation:
    @staticmethod
    def check(fields_by_source: dict, tolerance: float = 0.1):
        conflicts = []; consistent = []
        for field, sources in (fields_by_source or {}).items():
            vals = [s.get('value') for s in sources if s.get('value') is not None]
            if len(vals) < 2: continue
            if max(vals)-min(vals) > tolerance*max(abs(min(vals)),1): conflicts.append(field)
            else: consistent.append(field)
        status = "CONFLICTED" if conflicts else "CONSISTENT"
        return {"status":status,"conflicts":conflicts,"consistent":consistent,"conflicted_blocked":len(conflicts)>0}

class FactExtractionStore:
    def __init__(self): self._facts = {}
    def append(self, fact: EvidenceCard): self._facts[fact.evidence_id] = fact
    def get_by_ticker(self, ticker: str): return [f for f in self._facts.values() if f.ticker == ticker]
    def get_stale(self): return [f for f in self._facts.values() if f.freshness_status == "STALE"]
    def production_allowed(self): return False
