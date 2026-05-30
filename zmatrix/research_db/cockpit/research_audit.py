"""Batch-E: Research Audit — evidence integrity verification."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

class AuditStatus(str, Enum):
    PASS="PASS"; FAIL_CLOSED="FAIL_CLOSED"; PARTIAL="PARTIAL"

@dataclass
class AuditResult:
    session_id: str; status: str = "PENDING"
    evidence_complete: bool = False; council_complete: bool = False
    replay_complete: bool = False; hash_valid: bool = False
    fail_reasons: list = field(default_factory=list)
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class ResearchAudit:
    @staticmethod
    def audit(session) -> AuditResult:
        r = AuditResult(session_id=session.session_id)
        r.evidence_complete = bool(session.ticker and session.start_date)
        r.council_complete = bool(session.council_packet)
        r.replay_complete = bool(session.replay_result)
        r.hash_valid = bool(session.audit_hash and len(session.audit_hash) == 16)
        if not r.evidence_complete: r.fail_reasons.append("MISSING_EVIDENCE")
        if not r.council_complete: r.fail_reasons.append("MISSING_COUNCIL")
        if not r.replay_complete: r.fail_reasons.append("MISSING_REPLAY")
        if not r.hash_valid: r.fail_reasons.append("INVALID_HASH")
        r.status = AuditStatus.PASS.value if not r.fail_reasons else AuditStatus.FAIL_CLOSED.value
        return r

    @staticmethod
    def batch_audit(sessions: list) -> list[AuditResult]:
        return [ResearchAudit.audit(s) for s in sessions]
