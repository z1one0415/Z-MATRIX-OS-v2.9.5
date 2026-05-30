"""F.5-2: Regime Expansion — 20+ combined regimes (Bull+HighVol, Bear+Liquidity, etc.)."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class CombinedRegime:
    regime_id: str; name: str; base_regimes: list = field(default_factory=list)
    description: str = ""; ic_threshold: float = 0.02
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

EXPANDED_REGIMES = [
    CombinedRegime("BULL_HIVOL","Bull + High Volatility",["BULL","HIGH_VOL"],"Strong trend with high uncertainty",0.03),
    CombinedRegime("BULL_LOWVOL","Bull + Low Volatility",["BULL","LOW_VOL"],"Steady uptrend",0.02),
    CombinedRegime("BEAR_HIVOL","Bear + High Volatility",["BEAR","HIGH_VOL"],"Panic selling",0.03),
    CombinedRegime("BEAR_LOWVOL","Bear + Low Volatility",["BEAR","LOW_VOL"],"Slow grind down",0.02),
    CombinedRegime("SIDEWAYS_HIVOL","Sideways + High Volatility",["SIDEWAYS","HIGH_VOL"],"Choppy range",0.025),
    CombinedRegime("SIDEWAYS_LOWVOL","Sideways + Low Volatility",["SIDEWAYS","LOW_VOL"],"Dead market",0.015),
    CombinedRegime("LIQUIDITY_CRUNCH","Liquidity Contraction",["ILLIQUID","BEAR"],"Capital outflow",0.04),
    CombinedRegime("LIQUIDITY_BOOM","Liquidity Expansion",["LIQUID","BULL"],"Capital inflow",0.02),
    CombinedRegime("POLICY_TIGHTENING","Policy Tightening",["POLICY_TIGHT","CREDIT_CON"],"Rate hikes + credit contraction",0.03),
    CombinedRegime("POLICY_EASING","Policy Easing",["POLICY_LOOSE","CREDIT_EXP"],"Rate cuts + credit expansion",0.02),
    CombinedRegime("COMMODITY_INFLATION","Commodity-Driven Inflation",["HIGH_VOL","POLICY_TIGHT"],"Rising commodity prices",0.025),
    CombinedRegime("DEFLATION_SHOCK","Deflation Shock",["BEAR","POLICY_LOOSE"],"Falling prices, policy response",0.03),
    CombinedRegime("GROWTH_SCARE","Growth Scare",["BEAR","HIGH_VOL","CREDIT_CON"],"Sharp growth slowdown",0.035),
    CombinedRegime("RISK_ON","Risk On",["BULL","LOWVOL","LIQUID"],"Strong risk appetite",0.015),
    CombinedRegime("RISK_OFF","Risk Off",["BEAR","HIGH_VOL","ILLIQUID"],"Flight to safety",0.03),
    CombinedRegime("SECTOR_ROTATION","Sector Rotation",["SIDEWAYS","LIQUID"],"Money moving between sectors",0.02),
    CombinedRegime("MACRO_TAIL","Macro Tail Risk",["BEAR","HIGH_VOL","ILLIQUID","CREDIT_CON"],"Extreme event",0.04),
    CombinedRegime("QUIET_BULL","Quiet Bull Market",["BULL","LOWVOL","LIQUID","CREDIT_EXP"],"Ideal investing environment",0.015),
    CombinedRegime("STAGFLATION","Stagflation",["SIDEWAYS","POLICY_TIGHT","COMMODITY_INFLATION"],"Low growth + high inflation",0.03),
    CombinedRegime("RECOVERY","Recovery",["BULL","POLICY_LOOSE","CREDIT_EXP"],"Post-crisis recovery",0.02),
]

class RegimeExpansion:
    @staticmethod
    def classify(market_return: float, volatility: float, turnover: float, credit_spread: float) -> str:
        if market_return > 0.02 and volatility < 0.015 and turnover > 0.5 and credit_spread < 0.02:
            return "QUIET_BULL"
        if market_return < -0.03 and volatility > 0.03: return "BEAR_HIVOL"
        if market_return > 0.01 and volatility > 0.03: return "BULL_HIVOL"
        if market_return < -0.02 and volatility < 0.015: return "BEAR_LOWVOL"
        if credit_spread > 0.04 and volatility > 0.03: return "LIQUIDITY_CRUNCH"
        if turnover < 0.3 and market_return < -0.01: return "RISK_OFF"
        if market_return > 0.015 and volatility < 0.02 and turnover > 0.5: return "RISK_ON"
        if abs(market_return) < 0.01: return "SIDEWAYS_LOWVOL"
        return "STAGFLATION" if volatility > 0.02 else "SIDEWAYS_HIVOL"

    @staticmethod
    def evaluate_factor_in_regime(factor_ic: float, regime: CombinedRegime) -> bool:
        return abs(factor_ic) >= regime.ic_threshold

    @staticmethod
    def factor_regime_matrix(factor_id: str, regime_ics: dict) -> dict:
        results = {}
        for rid, r in [(r.regime_id, r) for r in EXPANDED_REGIMES]:
            ic = regime_ics.get(rid, 0.0)
            results[rid] = {"ic": ic, "effective": abs(ic) >= r.ic_threshold}
        effective = sum(1 for v in results.values() if v["effective"])
        return {"factor_id": factor_id, "total_regimes": len(results), "effective_regimes": effective,
                "robustness_pct": effective / max(len(results), 1), "results": results, "production_allowed": False}
