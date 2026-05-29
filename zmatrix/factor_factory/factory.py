"""V4.0-C2 FactorFactory — outcome horizon + IC + promotion gate"""
from __future__ import annotations
from dataclasses import dataclass

HORIZON_RULES = {"t5":5,"t20":20,"t60":60}

class OutcomeHorizonIntegrity:
    @staticmethod
    def check(forward_bars: list, horizon: str) -> dict:
        required = HORIZON_RULES.get(horizon, 0); available = len(forward_bars or [])
        ready = available >= required
        return {"horizon":horizon.upper(),"required_days":required,"available_days":available,"horizon_ready":ready,"fallback_last_price_allowed":False,"sample_ready":ready}

class NetReturnCalculator:
    @staticmethod
    def compute(gross_return_pct, entry_price=10, exit_price=10, volume=1000):
        commission = max(5, entry_price*volume*0.0003) + max(5, exit_price*volume*0.0003)
        stamp = exit_price*volume*0.001; notional = entry_price*volume
        cost_pct = (commission+stamp)/notional*100 if notional else 0
        return {"gross_return_pct":gross_return_pct,"net_return_pct":gross_return_pct-cost_pct-0.05,"cost_drag_bps":(cost_pct+0.05)*100,"production_allowed":False}

class FactorPromotionGate:
    @staticmethod
    def check(horizon_ready=False, net_return_ready=False, evidence_ready=False, pit_safe=False, sample_size=0):
        passed = horizon_ready and net_return_ready and evidence_ready and pit_safe and sample_size>=100
        return {"promotion_allowed":False,"research_validated":passed,"paper_only_validated":passed,"production_allowed":False}
