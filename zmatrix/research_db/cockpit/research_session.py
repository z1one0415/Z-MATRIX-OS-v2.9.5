"""Batch-E: Research Session — unified research object."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json, hashlib

@dataclass
class ResearchSession:
    session_id: str; ticker: str
    benchmark_id: str = "CSI300"; start_date: str = ""; end_date: str = ""
    factor_snapshot: dict = field(default_factory=dict)
    outcome_snapshot: dict = field(default_factory=dict)
    replay_result: dict = field(default_factory=dict)
    council_packet: dict = field(default_factory=dict)
    audit_hash: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

    def compute_audit_hash(self) -> str:
        h = hashlib.sha256()
        h.update(self.session_id.encode()); h.update(self.ticker.encode())
        h.update(json.dumps(self.factor_snapshot,sort_keys=True).encode())
        h.update(json.dumps(self.outcome_snapshot,sort_keys=True).encode())
        self.audit_hash = h.hexdigest()[:16]; return self.audit_hash
