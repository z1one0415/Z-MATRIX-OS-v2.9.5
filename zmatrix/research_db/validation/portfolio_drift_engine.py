"""P5.5-D: Portfolio Drift Engine — detect sector/style/factor drift over time."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

class DriftType(str, Enum):
    SECTOR_DRIFT="SECTOR_DRIFT"; STYLE_DRIFT="STYLE_DRIFT"; FACTOR_DRIFT="FACTOR_DRIFT"; NONE="NONE"

@dataclass
class DriftResult:
    portfolio_id: str; drift_type: str = "NONE"; drift_detected: bool = False
    drift_magnitude: float = 0.0; original_allocation: dict = field(default_factory=dict)
    current_allocation: dict = field(default_factory=dict)
    drifted_sectors: list = field(default_factory=list)
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class PortfolioDriftEngine:
    DRIFT_THRESHOLD = 0.20

    @staticmethod
    def detect_sector_drift(portfolio_id: str, original_weights: dict, current_weights: dict) -> DriftResult:
        r = DriftResult(portfolio_id=portfolio_id, drift_type=DriftType.SECTOR_DRIFT.value,
                        original_allocation=original_weights, current_allocation=current_weights)
        for sector in set(list(original_weights.keys()) + list(current_weights.keys())):
            diff = abs(current_weights.get(sector, 0) - original_weights.get(sector, 0))
            if diff > PortfolioDriftEngine.DRIFT_THRESHOLD:
                r.drift_detected = True; r.drifted_sectors.append(sector); r.drift_magnitude += diff
        return r

    @staticmethod
    def detect_style_drift(portfolio_id: str, original_style: dict, current_style: dict) -> DriftResult:
        r = DriftResult(portfolio_id=portfolio_id, drift_type=DriftType.STYLE_DRIFT.value,
                        original_allocation=original_style, current_allocation=current_style)
        for dim in set(list(original_style.keys()) + list(current_style.keys())):
            diff = abs(current_style.get(dim, 0) - original_style.get(dim, 0))
            if diff > PortfolioDriftEngine.DRIFT_THRESHOLD:
                r.drift_detected = True; r.drift_magnitude += diff
        return r

    @staticmethod
    def detect_factor_drift(portfolio_id: str, original_factors: list[str], current_factors: list[str]) -> DriftResult:
        r = DriftResult(portfolio_id=portfolio_id, drift_type=DriftType.FACTOR_DRIFT.value)
        o_set = set(original_factors); c_set = set(current_factors)
        removed = o_set - c_set; added = c_set - o_set
        r.drift_magnitude = (len(removed) + len(added)) / max(len(o_set | c_set), 1)
        r.drift_detected = r.drift_magnitude > PortfolioDriftEngine.DRIFT_THRESHOLD
        return r
