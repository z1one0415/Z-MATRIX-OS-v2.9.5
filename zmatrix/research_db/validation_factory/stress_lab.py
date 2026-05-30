"""F6: Stress Lab — historical extreme scenarios."""
from __future__ import annotations
from dataclasses import dataclass, field

STRESS_SCENARIOS = {
    "2008_GFC": {"year": 2008, "market_drop": -0.65, "volatility": 0.05, "duration_days": 252},
    "2015_CRASH": {"year": 2015, "market_drop": -0.35, "volatility": 0.04, "duration_days": 60},
    "2018_TRADE_WAR": {"year": 2018, "market_drop": -0.25, "volatility": 0.025, "duration_days": 180},
    "2020_COVID": {"year": 2020, "market_drop": -0.15, "volatility": 0.04, "duration_days": 30},
    "2022_BEAR": {"year": 2022, "market_drop": -0.25, "volatility": 0.025, "duration_days": 252},
    "GAP_OPEN": {"event": "gap_open", "gap_pct": -0.05, "impact": "IMMEDIATE"},
    "LIMIT_DOWN": {"event": "limit_down", "tickers": ["ALL"], "fill_rate": 0.0},
    "LIQUIDITY_FREEZE": {"event": "freeze", "capacity_pct": 0.1, "impact": "95% slippage increase"},
}

@dataclass
class StressResult:
    scenario_id: str; portfolio_loss: float = 0.0
    drawdown: float = 0.0; recovery_days: int = 0
    survived: bool = True; fail_reason: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class StressLab:
    @staticmethod
    def apply_market_stress(portfolio_equity: float, scenario_id: str) -> StressResult:
        scenario = STRESS_SCENARIOS.get(scenario_id, {})
        if not scenario: return StressResult(scenario_id=scenario_id)
        drop = scenario.get("market_drop", 0)
        loss = portfolio_equity * abs(drop) if drop < 0 else 0
        r = StressResult(scenario_id=scenario_id, portfolio_loss=loss, drawdown=drop)
        r.survived = loss < portfolio_equity * 0.5
        if not r.survived: r.fail_reason = f"Loss {loss} exceeds 50% of equity {portfolio_equity}"
        return r

    @staticmethod
    def apply_all_stresses(portfolio_equity: float) -> list[StressResult]:
        return [StressLab.apply_market_stress(portfolio_equity, sid) for sid in STRESS_SCENARIOS]

    @staticmethod
    def stress_summary(results: list[StressResult]) -> dict:
        survived = sum(1 for r in results if r.survived)
        return {"total_scenarios": len(results), "survived": survived,
                "failed": len(results)-survived, "max_drawdown": min(r.drawdown for r in results),
                "production_allowed": False}
