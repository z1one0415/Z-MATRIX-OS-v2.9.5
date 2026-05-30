"""ResearchDB Outcome Reality — Batch-H: Historical market states, events, PIT snapshots, integrity, reporting, audit."""
from .outcome_universe import OutcomeUniverse, OutcomeEvent, MarketState
from .outcome_snapshot import OutcomeSnapshot
from .outcome_integrity import IntegrityChecker, IntegrityResult, IntegrityStatus
from .outcome_report import OutcomeReport
from .outcome_audit import AuditCloser, AuditClose

__all__ = [
    "OutcomeUniverse", "OutcomeEvent", "MarketState",
    "OutcomeSnapshot",
    "IntegrityChecker", "IntegrityResult", "IntegrityStatus",
    "OutcomeReport",
    "AuditCloser", "AuditClose",
]
