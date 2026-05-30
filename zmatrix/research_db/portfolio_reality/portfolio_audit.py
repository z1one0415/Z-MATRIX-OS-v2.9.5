"""Batch-I: Portfolio Audit — hash-chain audit closer."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from typing import Optional


class AuditVerdict(str, Enum):
    PASS = "PASS"
    FAIL_CLOSED = "FAIL_CLOSED"
    PARTIAL = "PARTIAL"


@dataclass
class AuditEntry:
    entry_id: str
    portfolio_id: str
    event_type: str
    prev_hash: str = ""
    audit_hash: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    evidence: dict = field(default_factory=dict)
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self):
        self.production_allowed = False


@dataclass
class AuditCloser:
    portfolio_id: str
    chain_valid: bool = False
    entry_count: int = 0
    break_index: int = -1
    verdict: str = AuditVerdict.PASS.value
    fail_reasons: list = field(default_factory=list)
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self):
        self.production_allowed = False


class PortfolioAudit:
    GENESIS_HASH = "0000000000000000"

    @staticmethod
    def record(
        portfolio_id: str,
        event_type: str,
        prev_hash: str = "",
        evidence: dict = None,
        ledger: list = None,
    ) -> AuditEntry:
        import hashlib
        import json

        if ledger is None:
            ledger = []
        prev = prev_hash or (ledger[-1].audit_hash if ledger else PortfolioAudit.GENESIS_HASH)
        seq = len(ledger) + 1
        entry_id = f"{portfolio_id}-{event_type}-{seq:03d}"
        payload = json.dumps({
            "eid": entry_id, "pid": portfolio_id,
            "et": event_type, "ph": prev,
            "ev": evidence or {},
        }, sort_keys=True)
        audit_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
        entry = AuditEntry(
            entry_id=entry_id, portfolio_id=portfolio_id,
            event_type=event_type, prev_hash=prev,
            audit_hash=audit_hash, evidence=evidence or {},
        )
        ledger.append(entry)
        return entry

    @staticmethod
    def close_chain(
        portfolio_id: str,
        ledger: list[AuditEntry],
    ) -> AuditCloser:
        closer = AuditCloser(
            portfolio_id=portfolio_id,
            entry_count=len(ledger),
        )
        if len(ledger) <= 1:
            closer.chain_valid = True
            closer.verdict = AuditVerdict.PASS.value
            return closer
        for i in range(1, len(ledger)):
            if ledger[i].prev_hash != ledger[i - 1].audit_hash:
                closer.break_index = i
                closer.chain_valid = False
                closer.fail_reasons.append(
                    f"HASH_BREAK at entry {i}: "
                    f"prev={ledger[i].prev_hash[:8]} expected={ledger[i-1].audit_hash[:8]}"
                )
        if closer.fail_reasons:
            closer.verdict = AuditVerdict.FAIL_CLOSED.value
        else:
            closer.chain_valid = True
            closer.verdict = AuditVerdict.PASS.value
        return closer

    @staticmethod
    def verify_chain(ledger: list[AuditEntry]) -> bool:
        if not ledger:
            return True
        for i in range(1, len(ledger)):
            if ledger[i].prev_hash != ledger[i - 1].audit_hash:
                return False
        return True

    @staticmethod
    def batch_close(
        portfolios: list[tuple[str, list[AuditEntry]]],
    ) -> list[AuditCloser]:
        return [
            PortfolioAudit.close_chain(pid, ledger)
            for pid, ledger in portfolios
        ]
