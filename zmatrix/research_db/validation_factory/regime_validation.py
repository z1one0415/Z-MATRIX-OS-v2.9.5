"""F3: Regime Validation Lab — 10+ market regimes."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class RegimeDefinition:
    regime_id: str; name: str; description: str
    thresholds: dict = field(default_factory=dict)
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

REGIME_DEFINITIONS = [
    RegimeDefinition("BULL","Bull Market","Sustained uptrend",{"min_return":0.01}),
    RegimeDefinition("BEAR","Bear Market","Sustained downtrend",{"max_return":-0.01}),
    RegimeDefinition("SIDEWAYS","Sideways","Low directional movement",{"max_abs_return":0.01}),
    RegimeDefinition("HIGH_VOL","High Volatility","VIX-like spike",{"min_volatility":0.03}),
    RegimeDefinition("LOW_VOL","Low Volatility","Quiet market",{"max_volatility":0.01}),
    RegimeDefinition("LIQUID","Liquidity Expansion","Credit easing",{"min_turnover":0.5}),
    RegimeDefinition("ILLIQUID","Liquidity Contraction","Credit tightening",{"max_turnover":0.3}),
    RegimeDefinition("CREDIT_EXP","Credit Expansion","Falling spreads",{"max_spread":0.02}),
    RegimeDefinition("CREDIT_CON","Credit Contraction","Rising spreads",{"min_spread":0.05}),
    RegimeDefinition("POLICY_LOOSE","Policy Easing","Rate cuts",{"rate_direction":"down"}),
    RegimeDefinition("POLICY_TIGHT","Policy Tightening","Rate hikes",{"rate_direction":"up"}),
    RegimeDefinition("MACRO_TAIL","Tail Risk","Extreme event",{"min_drawdown":0.10}),
]

@dataclass
class RegimeValidationResult:
    factor_id: str; regime_id: str; ic: float = 0.0; effective: bool = False
    sample_size: int = 0
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class RegimeValidator:
    @staticmethod
    def evaluate(factor_id: str, regime_id: str, metrics: dict, threshold_ic: float = 0.02) -> RegimeValidationResult:
        ic = metrics.get("ic",0)
        r = RegimeValidationResult(factor_id=factor_id, regime_id=regime_id, ic=ic, sample_size=metrics.get("sample_size",0))
        r.effective = abs(ic) >= threshold_ic
        return r

    @staticmethod
    def evaluate_all(factor_id: str, regime_metrics: dict) -> dict:
        results = {}
        for rid, m in regime_metrics.items():
            results[rid] = RegimeValidator.evaluate(factor_id, rid, m)
        effective = sum(1 for v in results.values() if v.effective)
        return {"factor_id": factor_id, "total_regimes": len(results), "effective": effective,
                "coverage_pct": effective/max(len(results),1), "is_robust": effective>=len(results)*0.7,
                "production_allowed": False}
