"""持仓卖出决策状态机 — Position Sell Decision Engine

站在四天王共振之后, 做账户层裁决。
输入: 持仓(股数/成本/现价) + 四王共振结果
输出: position_action / sell_ratio / profit_lines / reason_codes

规则:
  1. 无持仓 → NO_POSITION
  2. 有持仓 → 先判断卖, 后判断买
  3. 长周期坏 → 大减仓
  4. 律动高抛交易仓, 轮动高位减核心仓
  5. 浮盈分级控制卖出比例
  6. 不得输出 BUY/SELL/AUTO_TRADE
"""
from __future__ import annotations
from typing import Any


def evaluate_position_sell_decision(
    ticker: str,
    shares: int,
    cost: float,
    current_price: float,
    resonance: dict,
) -> dict:
    """核心卖出决策 — 律动高抛交易仓, 轮动坏减核心仓."""
    
    profit_pct = round((current_price / cost - 1) * 100, 2) if cost > 0 else 0
    profit_amount = round((current_price - cost) * shares, 2)
    
    # ── 1. 无持仓 ──
    if shares <= 0 or cost <= 0:
        return _no_position()
    
    # ── 2. 浮盈分层 ──
    profit_band = _profit_band(profit_pct)
    
    # ── 3. 读取四王状态 ──
    kings = resonance.get("kings", {})
    rot = kings.get("rotation", {})
    rhythm = kings.get("rhythm", {})
    oscillation = kings.get("oscillation", {})
    impulse = kings.get("impulse", {})
    
    hard_blocks = resonance.get("hard_blocks", [])
    exit_alert = resonance.get("exit_alert", "NONE")
    
    rot_type = rot.get("type", "?") if rot else "?"
    rhythm_action = rhythm.get("action", "?") if rhythm else "?"
    rot_action = rot.get("action", "?") if rot else "?"
    
    # ── 4. 周期卖出规则 ──
    position_action = "HOLD_CORE"
    sell_ratio = 0.0
    reason_codes: list[str] = []
    
    if "ROTATION_TREND_DOWN" in hard_blocks or "RHYTHM_TREND_DOWN" in hard_blocks:
        if "ROTATION_TREND_DOWN" in hard_blocks:
            position_action = "MAJOR_REDUCE_OR_EXIT"
            sell_ratio = 0.67
            reason_codes.append("ROTATION_BROKEN_DO_NOT_WAIT_HIGHER")
        else:
            position_action = "REDUCE_CORE"
            sell_ratio = 0.50
            reason_codes.append("RHYTHM_TREND_DOWN_REDUCE_CORE")
    
    elif exit_alert == "FORCE_HARVEST":
        position_action = "REDUCE_CORE"
        sell_ratio = 0.50
        reason_codes.append("FORCE_HARVEST_REDUCE_CORE")
    
    elif exit_alert == "HARVEST":
        if rhythm_action == "HARVEST" and rot_action == "HARVEST":
            position_action = "REDUCE_CORE"
            sell_ratio = 0.50
            reason_codes.append("RHYTHM_AND_ROTATION_HIGH_REDUCE_CORE")
        elif rhythm_action == "HARVEST" and rot_type != "TREND_DOWN":
            position_action = "SELL_TRADING_KEEP_CORE"
            sell_ratio = 0.33
            reason_codes.append("RHYTHM_HIGH_SELL_TRADING_KEEP_ROTATION_CORE")
        else:
            if profit_pct >= 5:
                position_action = "SELL_TRADING_KEEP_CORE"
                sell_ratio = 0.33
                reason_codes.append("HARVEST_SELL_TRADING")
            else:
                position_action = "HOLD_WAIT_CONFIRM"
                reason_codes.append("HARVEST_BUT_LOW_PROFIT")
    
    elif exit_alert == "WATCH_HARVEST":
        if profit_pct >= 10:
            position_action = "LIGHTEN_TRADING"
            sell_ratio = 0.17
            reason_codes.append("WATCH_HARVEST_LIGHTEN")
        else:
            position_action = "HOLD_PROFIT"
            reason_codes.append("WATCH_HARVEST_HOLD_PROFIT")
    
    elif profit_pct >= 20:
        position_action = "PARTIAL_HARVEST"
        sell_ratio = 0.33
        reason_codes.append("PROFIT_20_PLUS_PROTECT")
    
    elif profit_pct >= 10:
        _osc_pos = oscillation.get("position", 0) if oscillation else 0
        _osc_pos = float(_osc_pos) if isinstance(_osc_pos, str) else _osc_pos
        if oscillation and _osc_pos > 0.75:
            position_action = "LIGHTEN_TRADING"
            sell_ratio = 0.17
            reason_codes.append("PROFIT_10_PLUS_POSITION_HIGH")
        else:
            position_action = "HOLD_PROFIT"
            reason_codes.append("PROFIT_10_PLUS_POSITION_OK")
    
    elif profit_pct >= 5:
        position_action = "HOLD_PROFIT"
        reason_codes.append("PROFIT_5_10")
    
    elif profit_pct >= -5:
        position_action = "HOLD_WAIT_CONFIRM"
        reason_codes.append("NEAR_COST")
    
    elif profit_pct >= -15:
        position_action = "HOLD_LOSS"
        reason_codes.append("LOSS_5_15")
    
    else:
        position_action = "STOP_REVIEW"
        sell_ratio = 0.50
        reason_codes.append("LOSS_15_PLUS_REVIEW")
    
    # ── 5. 计算卖出股数 ──
    sell_shares = round(shares * sell_ratio / 100) * 100 if sell_ratio > 0 else 0
    keep_shares = shares - sell_shares
    
    # ── 6. 保护线 + 利润线 ──
    if profit_pct >= 10:
        protection_line = round(max(cost * 1.05, current_price * 0.95), 2)
    elif profit_pct >= 5:
        protection_line = round(max(cost * 1.03, current_price * 0.97), 2)
    else:
        protection_line = round(cost, 2)
    
    profit_lines = {
        "cost_plus_8": round(cost * 1.08, 2),
        "cost_plus_10": round(cost * 1.10, 2),
        "cost_plus_15": round(cost * 1.15, 2),
        "cost_plus_20": round(cost * 1.20, 2),
    }
    
    # Sanity: no BUY/SELL/AUTO_TRADE
    assert position_action not in {"BUY","SELL","AUTO_TRADE","MARKET_ORDER"}, f"leaked {position_action}"
    
    return {
        "position_action": position_action,
        "sell_ratio": round(sell_ratio, 3),
        "sell_shares": sell_shares,
        "keep_shares": keep_shares,
        "profit_pct": profit_pct,
        "profit_amount": profit_amount,
        "profit_band": profit_band,
        "sell_layer": _sell_layer(sell_ratio),
        "reason_codes": reason_codes,
        "protection_line": protection_line,
        "cost_line": round(cost, 2),
        "profit_lines": profit_lines,
    }


def _profit_band(pct: float) -> str:
    if pct >= 20: return "PROFIT_20_PLUS"
    if pct >= 15: return "PROFIT_15_20"
    if pct >= 10: return "PROFIT_10_15"
    if pct >= 5: return "PROFIT_5_10"
    if pct >= -5: return "NEAR_COST"
    if pct >= -15: return "LOSS_5_15"
    return "LOSS_15_PLUS"


def _sell_layer(ratio: float) -> str:
    if ratio == 0: return "NONE"
    if ratio <= 0.17: return "LIGHTEN"
    if ratio <= 0.33: return "TRADING_LAYER"
    if ratio <= 0.50: return "CORE_REDUCE"
    return "MAJOR_EXIT"


def _no_position() -> dict:
    return {
        "position_action": "NO_POSITION",
        "sell_ratio": 0.0, "sell_shares": 0, "keep_shares": 0,
        "profit_pct": 0.0, "profit_amount": 0.0, "profit_band": "NO_POSITION",
        "sell_layer": "NONE", "reason_codes": ["NO_HOLDING"],
        "protection_line": 0.0, "cost_line": 0.0,
        "profit_lines": {},
    }
