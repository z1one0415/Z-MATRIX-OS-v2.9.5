"""Batch-E: Research Manifest — versioned research evidence."""
from __future__ import annotations
from dataclasses import dataclass, field
import json
from datetime import datetime, timezone

@dataclass
class ResearchManifest:
    manifest_id: str; session_id: str; ticker: str
    research_version: str = "v1.0"; data_version: str = "v1.0"
    factor_version: str = "v1.0"; council_version: str = "v1.0"; replay_version: str = "v1.0"
    audit_hash: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

    def to_json(self) -> str:
        return json.dumps({"manifest_id":self.manifest_id,"session_id":self.session_id,"ticker":self.ticker,
            "research_version":self.research_version,"data_version":self.data_version,
            "factor_version":self.factor_version,"council_version":self.council_version,
            "replay_version":self.replay_version,"audit_hash":self.audit_hash,
            "created_at":self.created_at,"production_allowed":False}, indent=2)

    @staticmethod
    def from_session(session, manifest_id: str) -> "ResearchManifest":
        return ResearchManifest(manifest_id=manifest_id, session_id=session.session_id,
                               ticker=session.ticker, audit_hash=session.audit_hash)
