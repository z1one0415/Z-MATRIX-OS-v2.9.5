"""P5.5-A: Alpha Stability Lab — IC/RankIC/WinRate stability over time."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import statistics

class StabilityStatus(str, Enum):
    STABLE="STABLE"; DEGRADING="DEGRADING"; UNSTABLE="UNSTABLE"

@dataclass
class StabilityResult:
    factor_id: str; status: str = "UNSTABLE"
    ic_mean: float = 0.0; ic_std: float = 0.0; ic_cv: float = 0.0
    rankic_mean: float = 0.0; winrate_mean: float = 0.0
    periods_analyzed: int = 0
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class AlphaStabilityLab:
    @staticmethod
    def compute_stability(factor_id: str, historical_metrics: list[dict]) -> StabilityResult:
        r = StabilityResult(factor_id=factor_id)
        ic_vals = [m.get("ic",0) for m in historical_metrics if m.get("ic") is not None]
        rankic_vals = [m.get("rankic",0) for m in historical_metrics if m.get("rankic") is not None]
        wr_vals = [m.get("win_rate",0) for m in historical_metrics if m.get("win_rate") is not None]
        r.periods_analyzed = len(ic_vals)
        if r.periods_analyzed > 0: r.ic_mean = statistics.mean(ic_vals); r.rankic_mean = statistics.mean(rankic_vals) if rankic_vals else 0.0
        if r.periods_analyzed < 3: r.status = StabilityStatus.UNSTABLE.value; return r
        r.ic_mean = statistics.mean(ic_vals)
        r.ic_std = statistics.stdev(ic_vals) if len(ic_vals) > 1 else 0.0
        r.ic_cv = abs(r.ic_std / r.ic_mean) if r.ic_mean != 0 else float("inf")
        r.rankic_mean = statistics.mean(rankic_vals) if rankic_vals else 0.0
        r.winrate_mean = statistics.mean(wr_vals) if wr_vals else 0.0
        if r.ic_cv < 0.5 and abs(r.ic_mean) > 0.02: r.status = StabilityStatus.STABLE.value
        elif r.ic_cv < 1.0: r.status = StabilityStatus.DEGRADING.value
        else: r.status = StabilityStatus.UNSTABLE.value
        return r

    @staticmethod
    def batch_analyze(factors: list[dict]) -> list[StabilityResult]:
        return [AlphaStabilityLab.compute_stability(f["factor_id"], f.get("metrics",[])) for f in factors]
