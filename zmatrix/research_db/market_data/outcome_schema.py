"""Phase 3-B: Outcome Horizon Schema — readiness only, no return/alpha."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class OutcomeHorizon(str, Enum):
    T1 = "T1"; T5 = "T5"; T10 = "T10"; T20 = "T20"; T60 = "T60"

class OutcomeReadinessStatus(str, Enum):
    READY = "READY"
    INSUFFICIENT_FORWARD_DAYS = "INSUFFICIENT_FORWARD_DAYS"
    MISSING_ENTRY_BAR = "MISSING_ENTRY_BAR"
    MISSING_EXIT_BAR = "MISSING_EXIT_BAR"
    SUSPENDED_ENTRY = "SUSPENDED_ENTRY"
    SUSPENDED_EXIT = "SUSPENDED_EXIT"
    INVALID_HORIZON = "INVALID_HORIZON"
    BLOCKED = "BLOCKED"

@dataclass
class OutcomeHorizonRequest:
    ticker: str; observation_date: str; horizon: OutcomeHorizon
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed = False

@dataclass
class OutcomeHorizonResult:
    ticker: str; observation_date: str; horizon: str; required_forward_days: int
    entry_date: Optional[str] = None; exit_date: Optional[str] = None
    readiness_status: str = "BLOCKED"; reason: str = ""
    entry_bar_available: bool = False; exit_bar_available: bool = False
    entry_suspended: bool = False; exit_suspended: bool = False
    fallback_used: bool = False
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed = False; self.fallback_used = False

HORIZON_FORWARD_DAYS = {"T1": 1, "T5": 5, "T10": 10, "T20": 20, "T60": 60}
