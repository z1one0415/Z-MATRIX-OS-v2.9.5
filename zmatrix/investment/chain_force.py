"""☯️ 10链×5力筛选模块 v1.0 (v2.9.8-dev)"""
from __future__ import annotations
from datetime import datetime

_FORBIDDEN = {"BUY", "SELL", "ADD", "CLEAR", "AUTO_TRADE", "MARKET_ORDER", "BROKER_ORDER", "REAL_TRADE"}

def evaluate_chain_force_10x5(candidate: dict) -> dict:
    now = datetime.now()
    ticker = candidate.get("ticker", "UNKNOWN")
    chain = candidate.get("chain", "UNKNOWN")
    forces = candidate.get("force_scores", {})
    available = sum(1 for v in forces.values() if v is not None)
    degraded = available < 2
    chain_status = "UNKNOWN"
    chain_gate_passed = False

    if not degraded:
        favorable = sum(1 for v in forces.values() if v and v >= 7)
        unfavorable = sum(1 for v in forces.values() if v and v < 4)
        if favorable > unfavorable:
            chain_status = "FAVORABLE"; chain_gate_passed = True
        elif unfavorable > favorable:
            chain_status = "UNFAVORABLE"
        else:
            chain_status = "NEUTRAL"; chain_gate_passed = True

    return {
        "module": "chain_force.evaluate_10x5", "version": "v1.0",
        "ticker": ticker, "chain": chain,
        "force_scores": forces,
        "chain_status": chain_status, "chain_gate_passed": chain_gate_passed,
        "degraded": degraded, "reasons": ["INSUFFICIENT_DATA"] if degraded else [],
        "real_trade_allowed": False,
    }
