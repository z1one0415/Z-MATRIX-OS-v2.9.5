"""V2 Ledger — Append-only state machine for prediction market lifecycle."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib, json

class LedgerEventType:
    PREDICTION_MADE="PREDICTION_MADE"; PREDICTION_RESOLVED="PREDICTION_RESOLVED"
    CALIBRATION_UPDATED="CALIBRATION_UPDATED"; RANKING_PUBLISHED="RANKING_PUBLISHED"
    MARKET_FORMED="MARKET_FORMED"; CONSENSUS_REACHED="CONSENSUS_REACHED"

@dataclass
class LedgerRecord:
    record_id: str; event_type: str; payload: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    previous_hash: str = ""; current_hash: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class DecisionLedgerV2:
    def __init__(self): self._records: list[LedgerRecord] = []; self._last_hash = "GENESIS"

    def record(self, record_id: str, event_type: str, payload: dict = None) -> LedgerRecord:
        r = LedgerRecord(record_id=record_id, event_type=event_type, payload=payload or {}, previous_hash=self._last_hash)
        r.current_hash = hashlib.sha256(json.dumps({"id":record_id,"type":event_type,"prev":self._last_hash,"payload":payload or {}},sort_keys=True,default=str).encode()).hexdigest()[:16]
        self._last_hash = r.current_hash; self._records.append(r); return r

    def get_chain(self) -> list[dict]:
        return [{"id":r.record_id, "event":r.event_type, "hash":r.current_hash, "prev":r.previous_hash} for r in self._records]

    def verify_chain(self) -> bool:
        for i in range(1, len(self._records)):
            if self._records[i].previous_hash != self._records[i-1].current_hash: return False
        return True

    def count(self) -> int: return len(self._records)
