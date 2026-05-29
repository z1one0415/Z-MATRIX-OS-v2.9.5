"""V4.0-C2.1 AccountGovernance depth — holding alpha, watchlist, risk budget"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class HoldingAlpha:
    ticker: str; holding_return: float; benchmark_return: float; alpha: float
    production_allowed: bool = False; real_trade_allowed: bool = False
    @classmethod
    def compute(cls, ticker, hret, bret): return cls(ticker,hret,bret,hret-bret)

class WatchlistOpportunityCurve:
    def __init__(self): self.items = []
    def append(self, ticker, signal_ret, benchmark_ret):
        self.items.append({"ticker":ticker,"signal_return":signal_ret,"benchmark_return":benchmark_ret,"opportunity_alpha":signal_ret-benchmark_ret,"real_trade_allowed":False,"broker_order_allowed":False})
    def summary(self):
        n=len(self.items); avg=sum(i["opportunity_alpha"] for i in self.items)/n if n else 0
        return {"count":n,"avg_opportunity_alpha":avg,"real_trade_allowed":False,"broker_order_allowed":False}

class RiskBudget:
    @staticmethod
    def check(current_dd, max_dd):
        if current_dd <= -abs(max_dd): return {"status":"RISK_BUDGET_BREACHED","action":"ACTION_BLOCKED","real_trade_allowed":False,"broker_order_allowed":False,"production_allowed":False}
        return {"status":"RISK_BUDGET_OK","action":"HUMAN_REVIEW_REQUIRED","real_trade_allowed":False,"broker_order_allowed":False,"production_allowed":False}
