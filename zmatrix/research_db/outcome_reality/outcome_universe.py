"""OutcomeUniverse — market states, event catalog 2005-2026, classification and query."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class MarketState(str, Enum):
    BULL = "BULL"
    BEAR = "BEAR"
    SIDEWAYS = "SIDEWAYS"
    POLICY = "POLICY"
    LIQUIDITY_CRISIS = "LIQUIDITY_CRISIS"
    BLACK_SWAN = "BLACK_SWAN"

    @classmethod
    def classify_from_return(cls, market_return: float, volatility: float = 0.0) -> MarketState:
        if market_return <= -0.20:
            return cls.BEAR
        if market_return >= 0.20:
            return cls.BULL
        if market_return > 0 and market_return < 0.10:
            return cls.SIDEWAYS
        if market_return < 0 and market_return > -0.10:
            return cls.SIDEWAYS
        return cls.SIDEWAYS

    @classmethod
    def all_states(cls) -> list[str]:
        return [s.value for s in cls]


@dataclass
class OutcomeEvent:
    event_id: str
    name: str
    year: int
    type: MarketState
    start_date: str
    end_date: str
    peak_date: Optional[str] = None
    market_return: float = 0.0
    description: str = ""
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self):
        self.production_allowed = False


def _build_catalog() -> list[OutcomeEvent]:
    return [
        OutcomeEvent("EV-2005-01", "A-Share Reform Launch", 2005, MarketState.POLICY,
                     "2005-04-29", "2005-12-31", "2005-06-06", 0.12, "Split-share structure reform kickoff"),
        OutcomeEvent("EV-2006-01", "China Bull Run", 2006, MarketState.BULL,
                     "2006-01-04", "2006-12-29", "2006-12-29", 1.30, "SSE surges 130% in full-year bull"),
        OutcomeEvent("EV-2007-01", "China Bubble Peak", 2007, MarketState.BULL,
                     "2007-01-04", "2007-10-16", "2007-10-16", 0.97, "SSE hits 6124 all-time high"),
        OutcomeEvent("EV-2008-01", "Global Financial Crisis", 2008, MarketState.BLACK_SWAN,
                     "2008-01-14", "2008-11-04", "2008-11-04", -0.65, "Lehman collapse, SSE crashes 65%"),
        OutcomeEvent("EV-2008-02", "China 4 Trillion Stimulus", 2008, MarketState.POLICY,
                     "2008-11-09", "2009-08-04", "2009-08-04", 1.03, "Massive fiscal + monetary stimulus"),
        OutcomeEvent("EV-2009-01", "Stimulus-Fueled Rebound", 2009, MarketState.BULL,
                     "2009-01-05", "2009-12-31", "2009-08-04", 0.80, "Liquidity-driven rally"),
        OutcomeEvent("EV-2010-01", "Tightening Cycle", 2010, MarketState.POLICY,
                     "2010-01-04", "2010-12-31", None, -0.14, "PBOC raises RRR and rates"),
        OutcomeEvent("EV-2011-01", "Inflation Bear", 2011, MarketState.BEAR,
                     "2011-04-18", "2011-12-31", "2011-12-28", -0.22, "Stagflation, SSE falls from 3067"),
        OutcomeEvent("EV-2012-01", "Sideways Grind", 2012, MarketState.SIDEWAYS,
                     "2012-01-04", "2012-12-04", None, 0.03, "Narrow range, low volumes"),
        OutcomeEvent("EV-2013-01", "ChiNext Startup Boom", 2013, MarketState.BULL,
                     "2013-01-04", "2013-12-31", "2013-10-10", 0.83, "Growth stocks/SME board rally"),
        OutcomeEvent("EV-2014-01", "Leverage Bull", 2014, MarketState.BULL,
                     "2014-07-22", "2014-12-31", "2014-12-31", 0.53, "Margin trading fuels rapid rise"),
        OutcomeEvent("EV-2015-01", "A-Share Bubble & Crash", 2015, MarketState.BLACK_SWAN,
                     "2015-01-05", "2015-08-26", "2015-06-12", -0.36, "SSE 5178 crash, circuit breaker, 30%+ drawdown"),
        OutcomeEvent("EV-2015-02", "National Team Rescue", 2015, MarketState.POLICY,
                     "2015-07-06", "2015-12-31", None, 0.12, "Government fund buys stocks to stabilize"),
        OutcomeEvent("EV-2016-01", "Circuit Breaker Crash", 2016, MarketState.BLACK_SWAN,
                     "2016-01-04", "2016-01-07", "2016-01-07", -0.15, "Circuit breaker triggered twice in 4 days, then abolished"),
        OutcomeEvent("EV-2016-02", "Recovery Year", 2016, MarketState.SIDEWAYS,
                     "2016-01-29", "2016-12-31", None, -0.12, "Slow recovery after crash"),
        OutcomeEvent("EV-2017-01", "White Horse Rally", 2017, MarketState.BULL,
                     "2017-01-03", "2017-12-29", "2017-11-13", 0.06, "Large-cap quality stocks outperform"),
        OutcomeEvent("EV-2018-01", "Trade War Bear", 2018, MarketState.BLACK_SWAN,
                     "2018-01-29", "2018-10-19", "2018-10-19", -0.25, "US-China trade war, SSE falls to 2449"),
        OutcomeEvent("EV-2019-01", "Tech Recovery", 2019, MarketState.BULL,
                     "2019-01-04", "2019-04-08", "2019-04-08", 0.22, "Semiconductor/5G rally after trade détente"),
        OutcomeEvent("EV-2020-01", "COVID-19 Crash", 2020, MarketState.BLACK_SWAN,
                     "2020-01-14", "2020-03-23", "2020-03-23", -0.13, "Global pandemic, circuit breaker, V-shaped recovery"),
        OutcomeEvent("EV-2020-02", "Liquidity Flood Recovery", 2020, MarketState.BULL,
                     "2020-03-24", "2020-07-13", "2020-07-13", 0.31, "Global QE + China V-shaped bounce"),
        OutcomeEvent("EV-2021-01", "Sector Rotation Year", 2021, MarketState.SIDEWAYS,
                     "2021-01-04", "2021-12-31", "2021-02-18", 0.05, "Property crackdown, new energy diverges"),
        OutcomeEvent("EV-2021-02", "Evergrande Default", 2021, MarketState.LIQUIDITY_CRISIS,
                     "2021-09-08", "2021-12-31", None, -0.04, "Property sector liquidity crisis spreads"),
        OutcomeEvent("EV-2022-01", "COVID Zero + Property Bear", 2022, MarketState.BEAR,
                     "2022-01-04", "2022-10-31", "2022-10-31", -0.15, "Lockdowns + property crisis, SSE below 2900"),
        OutcomeEvent("EV-2022-02", "Nov-2022 Reopen Rally", 2022, MarketState.POLICY,
                     "2022-11-01", "2022-12-31", None, 0.09, "COVID-zero exit + property 16-point plan"),
        OutcomeEvent("EV-2023-01", "ChatGPT / AI Theme", 2023, MarketState.BULL,
                     "2023-01-30", "2023-06-20", "2023-04-12", 0.18, "AI/LLM theme drives TMT sector"),
        OutcomeEvent("EV-2023-02", "Deflation Concerns", 2023, MarketState.SIDEWAYS,
                     "2023-07-01", "2023-12-31", None, -0.09, "PPI deflation, consumption downgrade, policy wait"),
        OutcomeEvent("EV-2024-01", "Feb-2024 V-Bounce", 2024, MarketState.POLICY,
                     "2024-02-05", "2024-03-18", "2024-02-23", 0.16, "National team buys ETFs, market floor"),
        OutcomeEvent("EV-2024-02", "Sept-24 Stimulus Bazooka", 2024, MarketState.POLICY,
                     "2024-09-24", "2024-10-08", "2024-10-08", 0.27, "PBOC+PBoF+CSRC press conference, strongest policy signal"),
        OutcomeEvent("EV-2025-01", "DeepSeek AI Breakout", 2025, MarketState.BULL,
                     "2025-01-20", "2025-02-24", "2025-02-24", 0.12, "DeepSeek-R1 disrupts global AI, tech re-rating"),
        OutcomeEvent("EV-2026-01", "Tariff Volatility", 2026, MarketState.SIDEWAYS,
                     "2026-01-02", "2026-05-15", None, -0.03, "US-China tariff adjustments, range-bound markets"),
    ]


class OutcomeUniverse:
    def __init__(self, events: list[OutcomeEvent] | None = None):
        self._events: list[OutcomeEvent] = events if events is not None else _build_catalog()
        self._production_allowed: bool = False

    @property
    def production_allowed(self) -> bool:
        return False

    def classify_period(self, start: str, end: str, market_data: dict | None = None) -> dict:
        matched: list[OutcomeEvent] = []
        for e in self._events:
            if e.end_date >= start and e.start_date <= end:
                matched.append(e)
        regime = MarketState.SIDEWAYS
        if matched:
            regime = self._dominant_regime(matched)
        if market_data:
            mr = market_data.get("market_return", 0.0)
            regime = MarketState.classify_from_return(mr)
        return {
            "period_start": start,
            "period_end": end,
            "regime": regime.value,
            "matched_events": len(matched),
            "events": [e.name for e in matched],
        }

    def _dominant_regime(self, events: list[OutcomeEvent]) -> MarketState:
        counts: dict[str, int] = {}
        for e in events:
            counts[e.type.value] = counts.get(e.type.value, 0) + 1
        if not counts:
            return MarketState.SIDEWAYS
        return MarketState(max(counts, key=counts.get))

    def get_events_by_type(self, event_type: MarketState | str) -> list[OutcomeEvent]:
        t = event_type if isinstance(event_type, str) else event_type.value
        return [e for e in self._events if e.type.value == t]

    def list_events(self) -> list[OutcomeEvent]:
        return list(self._events)

    def get_event(self, event_id: str) -> OutcomeEvent | None:
        for e in self._events:
            if e.event_id == event_id:
                return e
        return None

    def count(self) -> int:
        return len(self._events)

    def type_distribution(self) -> dict[str, int]:
        dist: dict[str, int] = {}
        for e in self._events:
            dist[e.type.value] = dist.get(e.type.value, 0) + 1
        return dist

    def events_in_year(self, year: int) -> list[OutcomeEvent]:
        return [e for e in self._events if e.year == year]

    def years_covered(self) -> list[int]:
        return sorted(set(e.year for e in self._events))

    def aggregate_return(self) -> dict[str, float]:
        result: dict[str, float] = {"total": 0.0, "avg": 0.0, "min": 0.0, "max": 0.0, "count": len(self._events)}
        if not self._events:
            return result
        returns = [e.market_return for e in self._events]
        result["total"] = sum(returns)
        result["avg"] = sum(returns) / len(returns)
        result["min"] = min(returns)
        result["max"] = max(returns)
        return result
