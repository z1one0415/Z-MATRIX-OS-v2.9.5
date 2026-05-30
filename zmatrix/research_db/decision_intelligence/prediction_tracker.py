"""J-3: Prediction Tracker — prediction vs actual, deviation stats."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
import statistics

@dataclass
class PredictionEntry:
    prediction_id: str; ticker: str; predicted_return: float; horizon_days: int
    made_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    actual_return: float = 0.0; outcome_recorded: bool = False; deviation: float = 0.0
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

@dataclass
class PredictionResult:
    forecaster_id: str; total_predictions: int = 0; recorded: int = 0; mean_deviation: float = 0.0
    mae: float = 0.0; rmse: float = 0.0; directional_accuracy: float = 0.0
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class PredictionTracker:
    def __init__(self): self._predictions: list[PredictionEntry] = []
    def predict(self, pid: str, ticker: str, predicted_return: float, horizon_days: int) -> PredictionEntry:
        e = PredictionEntry(prediction_id=pid, ticker=ticker, predicted_return=predicted_return, horizon_days=horizon_days)
        self._predictions.append(e); return e
    def record_outcome(self, pid: str, actual_return: float) -> PredictionEntry | None:
        for p in self._predictions:
            if p.prediction_id == pid: p.actual_return = actual_return; p.outcome_recorded = True; p.deviation = actual_return - p.predicted_return; return p
        return None
    def evaluate(self, forecaster_id: str) -> PredictionResult:
        ps = [p for p in self._predictions if p.outcome_recorded]
        r = PredictionResult(forecaster_id=forecaster_id, total_predictions=len(self._predictions), recorded=len(ps))
        if not ps: return r
        devs = [p.deviation for p in ps]; r.mean_deviation = statistics.mean(devs); r.mae = statistics.mean(abs(d) for d in devs)
        r.rmse = (statistics.mean(d**2 for d in devs))**0.5; r.directional_accuracy = sum(1 for p in ps if (p.predicted_return>0)==(p.actual_return>0))/len(ps)
        return r
