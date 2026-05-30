"""P5.5-B: Regime Robustness — Bull/Bear/Sideways/HighVol/LowVol factor persistence."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

class MarketRegime(str, Enum):
    BULL="BULL"; BEAR="BEAR"; SIDEWAYS="SIDEWAYS"; HIGH_VOL="HIGH_VOL"; LOW_VOL="LOW_VOL"

@dataclass
class RegimeResult:
    factor_id: str; regime: str; ic: float = 0.0; hit_rate: float = 0.0
    sample_size: int = 0; effective: bool = False
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class RegimeRobustness:
    REGIME_THRESHOLDS = {MarketRegime.BULL.value: 0.05, MarketRegime.BEAR.value: -0.05, MarketRegime.SIDEWAYS.value: 0.01}

    @staticmethod
    def evaluate_regime(factor_id: str, regime: str, metrics: dict) -> RegimeResult:
        r = RegimeResult(factor_id=factor_id, regime=regime, ic=metrics.get("ic",0),
                         hit_rate=metrics.get("hit_rate",0), sample_size=metrics.get("sample_size",0))
        threshold = RegimeRobustness.REGIME_THRESHOLDS.get(regime, 0.02)
        r.effective = abs(r.ic) >= abs(threshold)
        return r

    @staticmethod
    def evaluate_all_regimes(factor_id: str, regime_metrics: dict) -> dict:
        results = {}
        for regime, metrics in regime_metrics.items():
            results[regime] = RegimeRobustness.evaluate_regime(factor_id, regime, metrics)
        effective_count = sum(1 for v in results.values() if v.effective)
        total = len(results)
        return {"factor_id": factor_id, "regime_results": results,
                "effective_regimes": effective_count, "total_regimes": total,
                "is_robust": effective_count == total,
                "verdict": "REGIME_ROBUST" if effective_count == total else "REGIME_DEPENDENT",
                "production_allowed": False}

    @staticmethod
    def classify_regime(returns: list[float], volatility: float) -> str:
        if not returns: return MarketRegime.SIDEWAYS.value
        mean_ret = sum(returns) / len(returns)
        if volatility > 0.03: return MarketRegime.HIGH_VOL.value
        if mean_ret > 0.01: return MarketRegime.BULL.value
        if mean_ret < -0.01: return MarketRegime.BEAR.value
        return MarketRegime.SIDEWAYS.value
