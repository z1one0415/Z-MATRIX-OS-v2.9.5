"""P5.5-C: Factor Decay Observatory — T1/T5/T10/T20/T60 alpha decay curves."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class DecayResult:
    factor_id: str; half_life_days: int = 0; decay_speed: float = 0.0
    decay_pattern: str = "UNKNOWN"; t1_ic: float = 0.0; t5_ic: float = 0.0
    t10_ic: float = 0.0; t20_ic: float = 0.0; t60_ic: float = 0.0
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class FactorDecayObservatory:
    @staticmethod
    def compute_decay(factor_id: str, horizon_ics: dict) -> DecayResult:
        r = DecayResult(factor_id=factor_id)
        r.t1_ic = horizon_ics.get("T1", 0); r.t5_ic = horizon_ics.get("T5", 0)
        r.t10_ic = horizon_ics.get("T10", 0); r.t20_ic = horizon_ics.get("T20", 0); r.t60_ic = horizon_ics.get("T60", 0)
        ic_series = [r.t1_ic, r.t5_ic, r.t10_ic, r.t20_ic, r.t60_ic]
        r.decay_speed = abs(ic_series[0] - ic_series[-1]) if len(ic_series) >= 2 else 0.0
        if r.decay_speed < 0.01: r.decay_pattern = "PERSISTENT"
        elif r.decay_speed < 0.05: r.decay_pattern = "MODERATE_DECAY"
        else: r.decay_pattern = "RAPID_DECAY"
        r.half_life_days = FactorDecayObservatory._estimate_half_life(ic_series, [1,5,10,20,60])
        return r

    @staticmethod
    def _estimate_half_life(ic_series: list[float], horizons: list[int]) -> int:
        if not ic_series or abs(ic_series[0]) < 0.001: return 0
        half_value = abs(ic_series[0]) / 2
        for i, ic in enumerate(ic_series):
            if abs(ic) <= half_value: return horizons[i]
        return horizons[-1] if ic_series else 0

    @staticmethod
    def batch_analyze(factors: list[dict]) -> list[DecayResult]:
        return [FactorDecayObservatory.compute_decay(f["factor_id"], f.get("ics",{})) for f in factors]
