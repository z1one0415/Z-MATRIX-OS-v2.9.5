"""☯️ 板块阶段检测模块 v1.0 (v2.9.8-dev)

阶段枚举: IGNITION, CONFIRMATION, LEADING, DIFFUSION, CLIMAX, DIVERGENCE, RETREAT, REPAIR
硬规则: CONFIRMATION/LEADING/REPAIR → 可中期候选; CLIMAX → 不追后排; RETREAT → 禁止新开仓
"""
from __future__ import annotations
from datetime import datetime

SECTOR_STAGES = {"IGNITION", "CONFIRMATION", "LEADING", "DIFFUSION", "CLIMAX", "DIVERGENCE", "RETREAT", "REPAIR"}
_FORBIDDEN = {"BUY", "SELL", "ADD", "CLEAR", "AUTO_TRADE", "MARKET_ORDER", "BROKER_ORDER", "REAL_TRADE"}

def detect_sector_stage(candidate: dict) -> dict:
    now = datetime.now()
    ticker = candidate.get("ticker", "UNKNOWN")
    sector = candidate.get("sector", "UNKNOWN")
    stage = candidate.get("sector_stage", "UNKNOWN")
    if stage not in SECTOR_STAGES:
        stage = "UNKNOWN"

    mid_rotation_allowed = stage in {"CONFIRMATION", "LEADING", "REPAIR"}
    new_position_allowed = stage not in {"CLIMAX", "RETREAT", "DIVERGENCE", "UNKNOWN"}

    return {
        "module": "sector_stage.detect", "version": "v1.0",
        "ticker": ticker, "sector": sector,
        "sector_stage": stage,
        "mid_rotation_allowed": mid_rotation_allowed,
        "new_position_allowed": new_position_allowed,
        "reasons": [], "real_trade_allowed": False,
    }
