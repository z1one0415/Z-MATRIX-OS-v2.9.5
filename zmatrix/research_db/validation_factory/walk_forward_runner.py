"""F2-A: Walk Forward Runner — train/validate/test split, not in-sample."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class WalkForwardResult:
    experiment_id: str; train_periods: int = 0; val_periods: int = 0; test_periods: int = 0
    train_ic: float = 0.0; val_ic: float = 0.0; test_ic: float = 0.0
    overfit_detected: bool = False; out_of_sample_degradation: float = 0.0
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class WalkForwardRunner:
    OVERFIT_THRESHOLD = 0.30
    @staticmethod
    def run(experiment_id: str, train_data: list[dict], val_data: list[dict], test_data: list[dict],
            factor_fn=None) -> WalkForwardResult:
        r = WalkForwardResult(experiment_id=experiment_id, train_periods=len(train_data),
                              val_periods=len(val_data), test_periods=len(test_data))
        r.train_ic = WalkForwardRunner._mean_ic(train_data)
        r.val_ic = WalkForwardRunner._mean_ic(val_data)
        r.test_ic = WalkForwardRunner._mean_ic(test_data)
        r.out_of_sample_degradation = abs(r.train_ic - r.test_ic)
        r.overfit_detected = r.out_of_sample_degradation > WalkForwardRunner.OVERFIT_THRESHOLD
        return r

    @staticmethod
    def _mean_ic(data: list[dict]) -> float:
        ics = [d.get("ic",0) for d in data if d.get("ic") is not None]
        return sum(ics)/len(ics) if ics else 0.0
