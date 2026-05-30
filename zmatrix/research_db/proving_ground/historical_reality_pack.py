"""F.5-1: Historical Reality Pack — 6 real crisis events with sector/factor impact."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class RealityEvent:
    event_id: str; name: str; year: int; market_drop: float
    start_date: str; peak_date: str; recovery_date: str
    affected_sectors: list = field(default_factory=list)
    affected_factors: list = field(default_factory=list)
    volatility: float = 0.0; duration_days: int = 0
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

HISTORICAL_EVENTS = {
    "2008_GFC": RealityEvent("2008_GFC","Global Financial Crisis",2008,-0.72,
        "2007-10-01","2008-11-01","2009-07-01",
        ["Finance","Real Estate","Materials"],["momentum","value"],0.04,252),
    "2015_CRASH": RealityEvent("2015_CRASH","China Stock Market Crash",2015,-0.45,
        "2015-06-12","2015-08-26","2016-03-01",
        ["Technology","Small Cap","Brokerages"],["small_cap","leverage"],0.04,60),
    "2018_TRADE_WAR": RealityEvent("2018_TRADE_WAR","US-China Trade War",2018,-0.30,
        "2018-01-01","2018-10-01","2019-04-01",
        ["Technology","Industrial","Agriculture"],["export_exposure","supply_chain"],0.025,180),
    "2020_COVID": RealityEvent("2020_COVID","COVID-19 Pandemic",2020,-0.15,
        "2020-01-01","2020-03-23","2020-07-01",
        ["Travel","Hospitality","Energy"],["liquidity","defensive"],0.05,30),
    "2022_PROPERTY": RealityEvent("2022_PROPERTY","China Property Credit Crisis",2022,-0.25,
        "2022-01-01","2022-04-01","2022-12-01",
        ["Real Estate","Banks","Construction"],["credit_risk","value"],0.025,252),
    "2024_LIQUIDITY": RealityEvent("2024_LIQUIDITY","Liquidity Shock",2024,-0.18,
        "2024-01-01","2024-02-05","2024-04-01",
        ["Small Cap","Quant","High Beta"],["liquidity","small_cap","leverage"],0.035,40),
}

class HistoricalRealityPack:
    @staticmethod
    def get_event(event_id: str) -> RealityEvent | None:
        return HISTORICAL_EVENTS.get(event_id)

    @staticmethod
    def apply_factor_stress(factor_ic: float, event: RealityEvent, factor_type: str) -> float:
        if factor_type in event.affected_factors: return factor_ic * 0.3  # IC drops 70%
        return factor_ic * 0.7  # 30% reduction for unaffected

    @staticmethod
    def apply_portfolio_stress(equity: float, event: RealityEvent, sector_exposure: dict) -> float:
        loss = equity * abs(event.market_drop)
        for sector, weight in sector_exposure.items():
            if sector in event.affected_sectors: loss += equity * weight * 0.1
        return equity - min(loss, equity * 0.5)

    @staticmethod
    def event_summary(event: RealityEvent) -> dict:
        return {"event":event.name,"drop":event.market_drop,"sectors":len(event.affected_sectors),
                "factors":len(event.affected_factors),"days":event.duration_days,"production_allowed":False}
