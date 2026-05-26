"""Exposure Report — aggregated portfolio exposure analysis"""
from __future__ import annotations
import hashlib
from datetime import datetime, timezone

from zmatrix.portfolio_exposure.exposure_calculator import calc_exposure

def build_exposure_report(positions: list[dict]) -> dict:
    """Build full portfolio exposure report."""
    exposure = calc_exposure(positions)
    seed = f"exposure_report|{len(positions)}|{datetime.now(timezone.utc).isoformat()}"
    report_id = hashlib.sha256(seed.encode()).hexdigest()[:32]
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "report_version": "EXPOSURE_REPORT_V10", "report_id": report_id,
        "created_at": created_at, "position_count": len(positions),
        "sector_exposure": exposure["sector_exposure"],
        "chain_exposure": exposure["chain_exposure"],
        "concentration_warnings": exposure["concentration_warnings"],
        "real_trade_allowed": False, "broker_order_allowed": False,
        "auto_sell_allowed": False, "auto_position_close_allowed": False,
    }
