"""☯️ G17 Human Final Veto v1.0 (v2.9.8-dev)

G17 优先级最高。任何系统输出只能到 paper/action preview。
真实买入必须经过人工确认。
"""
from __future__ import annotations
from datetime import datetime

_FORBIDDEN = {"BUY", "SELL", "ADD", "CLEAR", "AUTO_TRADE", "MARKET_ORDER", "BROKER_ORDER", "REAL_TRADE"}

def build_g17_human_veto_preview(candidate: dict) -> dict:
    now = datetime.now()
    ticker = candidate.get("ticker", "UNKNOWN")
    return {
        "module": "g17.manual_veto.preview", "version": "v1.0",
        "ticker": ticker,
        "human_final_override_required": True,
        "system_action_limit": "PAPER_ONLY",
        "human_must_confirm_before_real_trade": True,
        "g17_can_veto_all": True,
        "real_trade_allowed": False,
    }
