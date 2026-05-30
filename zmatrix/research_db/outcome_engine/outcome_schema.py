"""Phase 3-B: Outcome Schema — SignalOutcome dataclass."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class QualityStatus(str, Enum):
    VALIDATED = "VALIDATED"
    WARNING = "WARNING"
    BLOCKED = "BLOCKED"
    UNKNOWN = "UNKNOWN"


@dataclass
class SignalOutcome:
    signal_id: str
    ticker: str
    name: str
    signal_date: str
    horizon: str
    required_forward_days: int = 0
    available_forward_days: int = 0
    ready: bool = False
    blocked_reason: Optional[str] = None
    entry_price: Optional[float] = None
    exit_date: Optional[str] = None
    exit_price: Optional[float] = None
    gross_return: Optional[float] = None
    market_return: Optional[float] = None
    industry_return: Optional[float] = None
    theme_return: Optional[float] = None
    alpha_vs_market: Optional[float] = None
    alpha_vs_industry: Optional[float] = None
    alpha_vs_theme: Optional[float] = None
    max_favorable_excursion: Optional[float] = None
    max_adverse_excursion: Optional[float] = None
    net_executable_return: Optional[float] = None
    execution_blocked: bool = False
    execution_blocked_reason: Optional[str] = None
    quality_status: str = QualityStatus.VALIDATED.value
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self):
        self.production_allowed = False
