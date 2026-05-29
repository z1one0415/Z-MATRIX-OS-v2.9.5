# allowlist: forbidden-token-definition
"""V4.0-C2.1 ExecutionQuality depth — limit-down, suspension, one-price, route"""
from __future__ import annotations
from dataclasses import dataclass

ALLOWED = {"PAPER_ONLY_OBSERVE","WAIT","NOT_FILLABLE","LIQUIDITY_TRAP","ROUTE_REJECTED","DATA_INSUFFICIENT"}

@dataclass
class TradabilityResult:
    status: str; action: str; executable: bool = False
    real_trade_allowed: bool = False; broker_order_allowed: bool = False
    blocked_reason: str | None = None

class LimitDownSellFailureGate:
    @staticmethod
    def check(bar: dict | None) -> TradabilityResult:
        if not bar: return TradabilityResult("DATA_INSUFFICIENT","DATA_INSUFFICIENT",blocked_reason="MISSING_BAR")
        if bar.get("limit_down") or (bar.get("open")==bar.get("high")==bar.get("low")==bar.get("close") and bar.get("pct_chg",0)<=-9.8):
            return TradabilityResult("LIMIT_DOWN_SELL_FAILURE","NOT_FILLABLE",blocked_reason="ONE_PRICE_LIMIT_DOWN")
        return TradabilityResult("SELL_ROUTE_OBSERVABLE","PAPER_ONLY_OBSERVE")

class SuspensionGate:
    @staticmethod
    def check(status: dict | None) -> TradabilityResult:
        if status and status.get("suspended"): return TradabilityResult("SUSPENDED","DATA_INSUFFICIENT",blocked_reason="SUSPENSION")
        return TradabilityResult("TRADABLE_STATUS","PAPER_ONLY_OBSERVE")

class OnePriceBoardDetector:
    @staticmethod
    def check(bar: dict | None) -> TradabilityResult:
        if not bar: return TradabilityResult("DATA_INSUFFICIENT","DATA_INSUFFICIENT",blocked_reason="MISSING_BAR")
        if bar.get("open")==bar.get("high")==bar.get("low")==bar.get("close"): return TradabilityResult("ONE_PRICE_BOARD","NOT_FILLABLE",blocked_reason="ONE_PRICE_BOARD")
        return TradabilityResult("NOT_ONE_PRICE","PAPER_ONLY_OBSERVE")

class RouteCompetition:
    @staticmethod
    def compare(routes: list[dict]) -> dict:
        if not routes: return {"status":"DATA_INSUFFICIENT","winner":None,"action":"DATA_INSUFFICIENT","real_trade_allowed":False,"broker_order_allowed":False}
        ranked = sorted(routes, key=lambda r: (r.get("cost_bps",999), -r.get("fill_probability",0)))
        w = ranked[0]; a = "PAPER_ONLY_OBSERVE" if w.get("fill_probability",0)>0 else "ROUTE_REJECTED"
        return {"status":"ROUTE_COMPARED","winner":w.get("route_id"),"action":a,"real_trade_allowed":False,"broker_order_allowed":False}
