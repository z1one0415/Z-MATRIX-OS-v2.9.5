"""Tests for Regime Detector."""
from zmatrix.strategy.regime_detector import detect_reversal_momentum_regime
import random
random.seed(42)
def test_insufficient(): assert detect_reversal_momentum_regime([100]*5)["regime_state"] == "DATA_INSUFFICIENT"
def test_momentum():
    prices = [100]; v=100
    for _ in range(50): v*=1+random.uniform(0.005,0.03); prices.append(v)
    r = detect_reversal_momentum_regime(prices)
    assert r["regime_state"] in ("MOMENTUM","TRANSITION")
