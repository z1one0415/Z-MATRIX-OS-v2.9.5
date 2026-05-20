"""D-Matrix / D-Band scoring modules.

v2.1 remains the conservative Phase1 warm-up detector.
v2.2 adds the physical-data and anti-fake foundation for dark-horse source detection:
M1 contracts, confidence discount, false-preheat filtering, silent accumulation,
M1 micro-absorption approximation, and the D_Early_v2.2 aggregator.
"""

try:
    from .d_early_scorer import evaluate_d_band
except Exception:  # pragma: no cover
    evaluate_d_band = None

from .d_early_v22_scorer import evaluate_d_early_v22

__all__ = ["evaluate_d_band", "evaluate_d_early_v22"]
