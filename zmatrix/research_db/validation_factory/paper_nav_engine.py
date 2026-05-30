"""F1-E: Paper NAV Engine — equity curve with drawdown."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class NavPoint:
    date: str; equity: float = 0.0; return_pct: float = 0.0
    drawdown: float = 0.0; peak: float = 0.0
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class PaperNavEngine:
    @staticmethod
    def compute_nav_curve(dates: list[str], equity_series: list[float], initial_capital: float) -> list[NavPoint]:
        curve = []; peak = initial_capital
        for i, (date, eq) in enumerate(zip(dates, equity_series)):
            ret = (eq - equity_series[i-1]) / equity_series[i-1] if i > 0 else (eq - initial_capital) / initial_capital
            peak = max(peak, eq); dd = (eq - peak) / peak if peak > 0 else 0
            curve.append(NavPoint(date=date, equity=eq, return_pct=ret, drawdown=dd, peak=peak))
        return curve

    @staticmethod
    def compute_metrics(curve: list[NavPoint]) -> dict:
        if not curve: return {"total_return":0,"max_drawdown":0,"sharpe":0,"volatility":0}
        returns = [p.return_pct for p in curve]
        total_ret = (curve[-1].equity - curve[0].equity) / curve[0].equity if curve[0].equity>0 else 0
        max_dd = min(p.drawdown for p in curve)
        import statistics; std = statistics.stdev(returns) if len(returns)>1 else 0
        sharpe = (statistics.mean(returns)/std)*252**0.5 if std>0 else 0
        return {"total_return":total_ret,"max_drawdown":max_dd,"sharpe":sharpe,"volatility":std,"production_allowed":False}
