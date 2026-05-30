"""AuditCloser — audit trail with hash chain, close_audit, generate_audit_trail."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import json
import hashlib


@dataclass
class AuditClose:
    audit_id: str
    snapshot_id: str
    closed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    overall_status: str = "PASS"
    hash_chain: list[str] = field(default_factory=list)
    trail: str = ""
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self):
        self.production_allowed = False

    def to_dict(self) -> dict:
        return {
            "audit_id": self.audit_id,
            "snapshot_id": self.snapshot_id,
            "closed_at": self.closed_at,
            "overall_status": self.overall_status,
            "hash_chain": list(self.hash_chain),
            "trail": self.trail,
            "production_allowed": False,
        }

    def to_json(self, filepath: str | None = None) -> str:
        data = self.to_dict()
        js = json.dumps(data, indent=2, ensure_ascii=False, default=str)
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(js)
        return js


class AuditCloser:
    _generation: int = 0

    @staticmethod
    def _compute_hash(data: str) -> str:
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    @staticmethod
    def close_audit(snapshot, integrity_result) -> AuditClose:
        from .outcome_snapshot import OutcomeSnapshot
        from .outcome_integrity import IntegrityResult
        AuditCloser._generation += 1
        audit_id = f"AUD-{AuditCloser._generation:04d}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
        chain = AuditCloser._build_hash_chain(snapshot, integrity_result)
        trail = AuditCloser.generate_audit_trail(snapshot, integrity_result)
        return AuditClose(
            audit_id=audit_id,
            snapshot_id=snapshot.snapshot_id,
            overall_status=integrity_result.overall_status.value,
            hash_chain=chain,
            trail=trail,
        )

    @staticmethod
    def _build_hash_chain(snapshot, integrity_result) -> list[str]:
        links = []
        links.append(AuditCloser._compute_hash(snapshot.snapshot_id))
        links.append(AuditCloser._compute_hash(snapshot.as_of_date))
        links.append(AuditCloser._compute_hash(str(snapshot.total_events)))
        links.append(AuditCloser._compute_hash(str(snapshot.market_return)))
        links.append(AuditCloser._compute_hash(json.dumps(snapshot.regime_distribution, sort_keys=True)))
        links.append(AuditCloser._compute_hash(json.dumps(snapshot.event_coverage, sort_keys=True)))
        links.append(AuditCloser._compute_hash(integrity_result.overall_status.value))
        combined = "||".join(links + [integrity_result.overall_status.value])
        chain_hash = AuditCloser._compute_hash(combined)
        links.append(chain_hash)
        return links

    @staticmethod
    def generate_audit_trail(snapshot, integrity_result) -> str:
        from .outcome_snapshot import OutcomeSnapshot
        from .outcome_integrity import IntegrityResult
        lines = []
        lines.append("=" * 60)
        lines.append("OUTCOME AUDIT TRAIL")
        lines.append("=" * 60)
        lines.append(f"Audit Timestamp : {datetime.now(timezone.utc).isoformat()}")
        lines.append(f"Snapshot ID     : {snapshot.snapshot_id}")
        lines.append(f"As Of Date      : {snapshot.as_of_date}")
        lines.append(f"Total Events    : {snapshot.total_events}")
        lines.append(f"Market Return   : {snapshot.market_return:.4f}")
        lines.append(f"")
        lines.append("Integrity Check Results:")
        lines.append(f"  Coverage    : {integrity_result.coverage_status.value} ({integrity_result.coverage_detail})")
        lines.append(f"  Consistency : {integrity_result.consistency_status.value} ({integrity_result.consistency_detail})")
        lines.append(f"  Duplicates  : {integrity_result.duplicates_status.value} ({integrity_result.duplicates_detail})")
        lines.append(f"  Hash        : {integrity_result.hash_status.value} ({integrity_result.hash_detail})")
        lines.append(f"  Overall     : {integrity_result.overall_status.value}")
        if integrity_result.issues:
            lines.append(f"")
            lines.append(f"Issues ({len(integrity_result.issues)}):")
            for i, issue in enumerate(integrity_result.issues, 1):
                lines.append(f"  {i}. {issue}")
        lines.append(f"")
        lines.append(f"Safety Confirmation:")
        lines.append(f"  Production Allowed : BLOCKED (False)")
        lines.append(f"  Real Trade         : BLOCKED (False)")
        lines.append(f"  Broker Orders      : BLOCKED (False)")
        lines.append(f"  Paper Only         : TRUE")
        lines.append(f"  Human Review       : REQUIRED")
        lines.append("=" * 60)
        return "\n".join(lines)

    @staticmethod
    def verify_chain(audit_close: AuditClose, snapshot, integrity_result) -> bool:
        expected = AuditCloser._build_hash_chain(snapshot, integrity_result)
        actual = audit_close.hash_chain
        if len(expected) != len(actual):
            return False
        for i, (e, a) in enumerate(zip(expected, actual)):
            if e != a:
                return False
        return True
