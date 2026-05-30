"""Outcome Engine — Phase 3-B: forward horizon, alpha calculation, signal outcomes."""
from .outcome_schema import SignalOutcome, QualityStatus
from .forward_horizon import OutcomeHorizonEngine
from .alpha_calculator import compute_gross_return, compute_benchmark_return, compute_alpha, compute_max_excursion

__all__ = [
    "SignalOutcome", "QualityStatus",
    "OutcomeHorizonEngine",
    "compute_gross_return", "compute_benchmark_return", "compute_alpha", "compute_max_excursion",
]
