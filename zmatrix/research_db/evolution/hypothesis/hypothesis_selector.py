"""EV2: Hypothesis Selector — variant selection by fitness."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class SelectionResult:
    hypothesis_id: str; selected: bool; fitness: float; reason: str
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class HypothesisSelector:
    MIN_FITNESS = 0.3
    @staticmethod
    def select(hypothesis_id: str, metrics: dict) -> SelectionResult:
        ic = abs(metrics.get("ic", 0)); fitness = min(1.0, ic * 10 + metrics.get("coverage", 0) * 0.3)
        selected = fitness >= HypothesisSelector.MIN_FITNESS
        return SelectionResult(hypothesis_id=hypothesis_id, selected=selected, fitness=fitness, reason=f"IC={ic:.3f}, fitness={fitness:.3f}")
