"""Decision Intelligence V2 — Prediction Market + Confidence Calibration + Researcher Ranking."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

class PredictionDirection(str, Enum): UP="UP"; DOWN="DOWN"; FLAT="FLAT"

@dataclass
class PredictionEntry:
    prediction_id: str; forecaster_id: str; ticker: str; direction: str
    magnitude_bps: float = 0.0; confidence: float = 0.5; horizon_days: int = 20
    made_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    actual_outcome: Optional[float] = None; resolved: bool = False
    was_correct: bool = False; calibration_error: float = 0.0
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

@dataclass
class CalibrationProfile:
    forecaster_id: str; total_predictions: int = 0; correct_predictions: int = 0
    mean_confidence: float = 0.0; actual_accuracy: float = 0.0
    overconfidence_score: float = 0.0; brier_score: float = 0.0
    calibration_grade: str = "UNGRADED"; production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

@dataclass
class ResearcherRank:
    forecaster_id: str; forecaster_type: str = "FACTOR"; rank: int = 0
    directional_accuracy: float = 0.0; calibration_score: float = 0.0
    stability_score: float = 0.0; composite_score: float = 0.0
    trend: str = "STABLE"; production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

@dataclass
class PredictionMarketResult:
    market_id: str; ticker: str; consensus_direction: str = "FLAT"
    consensus_magnitude: float = 0.0; forecaster_count: int = 0
    agreement_ratio: float = 0.0; disagreement_index: float = 0.0
    contrarian_signals: list = field(default_factory=list)
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False
