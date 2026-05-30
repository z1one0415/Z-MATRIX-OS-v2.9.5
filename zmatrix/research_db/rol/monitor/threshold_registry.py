"""R2: Threshold Registry — configurable thresholds for all monitored metrics."""
from __future__ import annotations

class ThresholdRegistry:
    DEFAULT_THRESHOLDS = {"ic": {"min_abs": 0.02}, "rankic": {"min_abs": 0.02}, "coverage": {"min": 0.3},
        "stability": {"max": 2.0}, "decay": {"max": 0.05}, "drift": {"max": 0.20}, "prediction_streak": {"max": 5},
        "turnover": {"max": 100}, "slippage": {"max": 50}, "max_dd": {"max": 0.30}}

    def __init__(self): self._thresholds: dict[str, dict] = dict(self.DEFAULT_THRESHOLDS)
    def get(self, object_id: str, metric: str) -> dict | None:
        key = f"{object_id}:{metric}"
        return self._thresholds.get(key) or self._thresholds.get(metric)
    def set(self, metric: str, thresholds: dict): self._thresholds[metric] = thresholds
    def list_all(self) -> dict: return dict(self._thresholds)
