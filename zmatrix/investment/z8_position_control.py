"""☯️ Z8 Position Control v1.0 (v2.9.8-dev)

只生成仓位上限建议，不生成实盘买入。
D_REJECT 仓位必须为 0，C_SHORT_EVENT 不得超过短期单票上限。
"""
from __future__ import annotations
from datetime import datetime

_FORBIDDEN = {"BUY", "SELL", "ADD", "CLEAR", "AUTO_TRADE", "MARKET_ORDER", "BROKER_ORDER", "REAL_TRADE"}

ROLE_POSITION_LIMITS = {"A_LONG_CORE": 0.12, "B_MID_ROTATION": 0.08, "C_SHORT_EVENT": 0.05, "D_REJECT": 0.0, "WATCH_ONLY": 0.0}

def evaluate_z8_position_control(candidate: dict, account: dict | None = None, exposure: dict | None = None) -> dict:
    now = datetime.now()
    ticker = candidate.get("ticker", "UNKNOWN")
    role = candidate.get("role", "D_REJECT")
    account = account or {}
    exposure = exposure or {}

    max_position_size = ROLE_POSITION_LIMITS.get(role, 0.0)
    max_loss_budget = account.get("max_loss_per_trade", 0.01)
    position_bucket = role
    violation_reasons = []
    position_allowed = max_position_size > 0.0
    add_position_allowed = position_allowed and exposure.get("exposure_gate_passed", False)

    if not account.get("account_gate_passed", True):
        violation_reasons.append("ACCOUNT_CONSTITUTION_FAILED")
        position_allowed = False

    if role == "D_REJECT":
        violation_reasons.append("ROLE_D_REJECT_NO_POSITION")
        position_allowed = False

    return {
        "module": "z8.position_control", "version": "v1.0",
        "ticker": ticker,
        "position_allowed": position_allowed,
        "add_position_allowed": add_position_allowed and position_allowed,
        "max_position_size": max_position_size,
        "max_loss_budget": max_loss_budget,
        "position_bucket": position_bucket,
        "violation_reasons": violation_reasons,
        "paper_only": True, "real_trade_allowed": False,
    }
