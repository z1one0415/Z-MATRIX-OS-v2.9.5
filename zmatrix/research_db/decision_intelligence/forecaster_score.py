"""J-4: Forecaster Score — rank forecasters, factors, and council members."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class ForecasterProfile:
    forecaster_id: str; forecaster_type: str  # FACTOR, COUNCIL_MEMBER, PORTFOLIO
    total_predictions: int = 0; directional_accuracy: float = 0.0
    mae: float = 0.0; rmse: float = 0.0; hit_rate: float = 0.0
    reliability_score: float = 0.0; rank: int = 0
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class ForecasterScore:
    def __init__(self): self._profiles: dict[str, ForecasterProfile] = {}
    def register(self, forecaster_id: str, forecaster_type: str) -> ForecasterProfile:
        p = ForecasterProfile(forecaster_id=forecaster_id, forecaster_type=forecaster_type)
        self._profiles[forecaster_id] = p; return p
    def update(self, forecaster_id: str, evaluation: "PredictionResult") -> ForecasterProfile | None:
        p = self._profiles.get(forecaster_id)
        if not p: return None
        p.total_predictions = evaluation.total_predictions; p.directional_accuracy = evaluation.directional_accuracy
        p.mae = evaluation.mae; p.rmse = evaluation.rmse; p.hit_rate = evaluation.directional_accuracy
        p.reliability_score = (p.directional_accuracy * 0.5 + (1.0 / (1.0 + p.mae)) * 0.3 + (1.0 / (1.0 + p.rmse)) * 0.2)
        return p
    def rank_all(self) -> list[ForecasterProfile]:
        ranked = sorted(self._profiles.values(), key=lambda p: p.reliability_score, reverse=True)
        for i, p in enumerate(ranked): p.rank = i + 1
        return ranked
    def most_reliable(self) -> ForecasterProfile | None:
        ranked = self.rank_all(); return ranked[0] if ranked else None
    def summary(self) -> list[dict]:
        return [{"id":p.forecaster_id, "type":p.forecaster_type, "score":p.reliability_score, "rank":p.rank} for p in self.rank_all()]
