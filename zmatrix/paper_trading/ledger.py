"""Paper Trade Ledger v1.0"""
from __future__ import annotations
from datetime import datetime
import hashlib

_FORBIDDEN = {"BUY","SELL","ADD","CLEAR","AUTO_TRADE","MARKET_ORDER","BROKER_ORDER","REAL_TRADE"}
ALLOWED_ROLES = {"A_LONG_CORE","B_MID_ROTATION","C_SHORT_EVENT"}
ALLOWED_HORIZONS = {"T5","T20","T60"}

def build_paper_trade_entry(*, ticker, role, entry_date, entry_price, paper_action, reason, target_horizon, max_loss_plan, invalidation_condition) -> dict:
    if role not in ALLOWED_ROLES:
        raise ValueError(f"role {role} cannot generate paper ledger (allowed: {ALLOWED_ROLES})")
    action_upper = str(paper_action).upper()
    for token in _FORBIDDEN:
        if token in action_upper:
            raise ValueError(f"forbidden token '{token}' in paper_action: {paper_action}")
    if target_horizon not in ALLOWED_HORIZONS:
        raise ValueError(f"invalid target_horizon: {target_horizon}")

    raw = f"{ticker}{entry_date}{paper_action}{datetime.now().isoformat()}"
    paper_id = hashlib.sha256(raw.encode()).hexdigest()[:32]
    return {
        "paper_id": paper_id, "ticker": ticker, "role": role,
        "entry_date": entry_date, "entry_price": float(entry_price),
        "paper_action": paper_action, "reason": reason,
        "target_horizon": target_horizon, "max_loss_plan": float(max_loss_plan),
        "invalidation_condition": invalidation_condition,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "real_trade_allowed": False,
    }
