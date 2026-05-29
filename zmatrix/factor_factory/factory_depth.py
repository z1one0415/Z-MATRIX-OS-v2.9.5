"""V4.0-C2-2 FactorFactory depth — trading calendar, strict T20/T60, executable return"""
from __future__ import annotations

class TradingCalendar:
    @staticmethod
    def count_forward_trading_days(trade_dates: list[str], start: str, horizon: int) -> int:
        return sum(1 for d in (trade_dates or []) if d > start)

class OutcomeHorizonDepth:
    RULES = {"t5":5,"t20":20,"t60":60}
    @classmethod
    def check(cls, trade_dates: list, start: str, horizon: str) -> dict:
        req = cls.RULES.get(horizon, 0); avail = cls._count_forward(trade_dates, start)
        ready = avail >= req
        return {"horizon":horizon.upper(),"required_days":req,"available_days":avail,"horizon_ready":ready,"actual_return":None,"sample_ready":ready,"fallback_last_price_allowed":False,"blocked_reason":None if ready else "INSUFFICIENT_FORWARD_WINDOW","promotion_allowed":False}
    @staticmethod
    def _count_forward(dates, start):
        return sum(1 for d in (dates or []) if d > start)

class ICICalculator:
    @staticmethod
    def pearson_ic(xs, ys):
        if len(xs) < 5: return {"ic":None,"status":"DATA_INSUFFICIENT","sample_size":len(xs)}
        n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
        num = sum((x-mx)*(y-my) for x,y in zip(xs,ys)); dx = sum((x-mx)**2 for x in xs); dy = sum((y-my)**2 for y in ys)
        ic = num/(dx*dy)**0.5 if dx and dy else 0
        return {"ic":ic,"sample_size":n,"production_allowed":False}

class NetExecutableReturn:
    @staticmethod
    def compute(gross_pct, limit_board=None):
        lb = limit_board or {}; cost = 0.0003*2 + 0.001 + 0.0005
        blocked = lb.get('limit_up') or lb.get('limit_down') or lb.get('suspension') or lb.get('one_price_board')
        if blocked: return {"net_executable_return":None,"executable":False,"blocked_reason":"TRADABILITY_BLOCKED","gross_return":gross_pct}
        return {"net_executable_return":gross_pct - cost*100,"executable":True,"blocked_reason":None,"gross_return":gross_pct,"production_allowed":False}
