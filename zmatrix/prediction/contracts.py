"""Z-G18 Tianji Engine — prediction contracts (INV-TG18-05: No Trade Action)"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

# Allowed: research/paper/watch only
ALLOWED_ACTIONS = frozenset({
    "WATCH", "WAIT", "WAIT_CONFIRM", "PAPER_TRACK",
    "DIAGNOSTIC_ONLY", "PAPER_PROBE_ELIGIBLE_PENDING_Z16_Z17",
})

# Forbidden: any real trade execution
FORBIDDEN_ACTIONS = frozenset({
    "BUY", "SELL", "ADD", "CLEAR", "AUTO_TRADE",
    "MARKET_ORDER", "PAPER_PROBE", "PAPER_PROBE_FROM_INTRADAY",
})

ALLOWED_ACTION_VALUES = {a: a for a in ALLOWED_ACTIONS}


@dataclass
class PredictionResult:
    ticker: str
    name: str = ""
    probability: float = 0.5
    horizon: dict = field(default_factory=lambda: {"T1": None, "T5": None, "T20": None})
    evidence_coverage: float = 0.0
    data_lineage: dict = field(default_factory=dict)
    temporal_consistency: dict = field(default_factory=dict)
    next_triggers: list = field(default_factory=list)
    action_proposal: str = "WAIT"
    z9_sample: dict = field(default_factory=dict)
    raw_score: float = 0.0
    confidence: str = "LOW"
    warnings: list = field(default_factory=list)

    def validate_action(self):
        if self.action_proposal in FORBIDDEN_ACTIONS:
            raise ValueError(f"Z-G18 leaked forbidden action: {self.action_proposal}")
        if self.action_proposal not in ALLOWED_ACTIONS:
            raise ValueError(f"Z-G18 unknown action: {self.action_proposal}")


@dataclass
class DataLineageEntry:
    source: str = "UNKNOWN"
    market_data: str = "UNKNOWN_PROXY"
    intraday: str = "NOT_CONNECTED"
    m1: bool = False
    l2: bool = False
    upstream_status: str = "DEGRADED_MISSING_LINEAGE"
    trust: str = "LOW"
    confidence_cap: str = "LOW"
    probability_cap: float = 0.60


DEFAULT_DEGRADED_PROXY = DataLineageEntry().to_dict() if hasattr(DataLineageEntry, "to_dict") else {
    "source": "UNKNOWN", "market_data": "UNKNOWN_PROXY",
    "intraday": "NOT_CONNECTED", "m1": False, "l2": False,
    "upstream_status": "DEGRADED_MISSING_LINEAGE", "trust": "LOW",
}


@dataclass
class Z9Sample:
    ticker: str = ""
    prediction_date: str = ""
    target_days: int = 5
    probability: float = 0.5
    signals: dict = field(default_factory=dict)
    strict_t_plus_n_required: bool = True
    auto_adjust_allowed: bool = False
    resolved: bool = False
    actual_outcome: float | None = None
