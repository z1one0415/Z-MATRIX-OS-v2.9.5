"""Connection Validator — validate BRD connection report"""
from __future__ import annotations

def validate_brd_connection_report(report):
    brd_connected = bool(report.get("brd_connected"))
    fallback_rate = report.get("fallback_rate")
    blocking = []
    if not brd_connected: blocking.append("BRD classifier not connected")
    if fallback_rate is not None and fallback_rate >= 0.05:
        blocking.append(f"fallback_rate too high: {fallback_rate}")
    return {"validator_version":"BRD_CONNECTION_VALIDATOR_V10","brd_connected":brd_connected,
            "fallback_rate":fallback_rate,"pass":len(blocking)==0,"blocking_issues":blocking,
            "real_trade_allowed":False,"broker_order_allowed":False}
