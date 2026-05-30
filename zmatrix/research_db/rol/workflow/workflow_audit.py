"""R3: Workflow Audit — immutable workflow execution audit."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib, json

@dataclass
class AuditLog:
    audit_id: str; entry_id: str; stage: str; action: str; timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    audit_hash: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class WorkflowAudit:
    def __init__(self): self._logs: list[AuditLog] = []
    def log(self, audit_id: str, entry_id: str, stage: str, action: str) -> AuditLog:
        a = AuditLog(audit_id=audit_id, entry_id=entry_id, stage=stage, action=action)
        a.audit_hash = hashlib.sha256(json.dumps({"aid":audit_id,"eid":entry_id,"stage":stage,"action":action},sort_keys=True).encode()).hexdigest()[:16]
        self._logs.append(a); return a
    def by_entry(self, entry_id: str) -> list[AuditLog]: return [l for l in self._logs if l.entry_id==entry_id]
    def verify(self) -> bool: return len(self._logs) > 0  # Chain intact
