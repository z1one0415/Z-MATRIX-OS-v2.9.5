"""PATCH-A-1: Outcome Horizon Hardening — 防止回测标签污染"""
from __future__ import annotations

HORIZON_REQUIREMENTS = {"t5": 5, "t20": 20, "t60": 60}

def check_outcome_horizon_ready(*, forward_bars: list[dict], horizon: str) -> dict:
    required = HORIZON_REQUIREMENTS.get(horizon.lower(), 0)
    available = len(forward_bars or [])
    ready = available >= required
    status = "READY" if ready else "INSUFFICIENT_FORWARD_DATA"
    return {"horizon": horizon.upper(), "required_days": required, "available_days": available, "horizon_ready": ready, "outcome_status": status}

def check_all_horizons(*, forward_bars: list[dict]) -> dict:
    results = {}
    for h in HORIZON_REQUIREMENTS:
        results[h] = check_outcome_horizon_ready(forward_bars=forward_bars, horizon=h)
    return {"horizon_check_version": "PATCH_A_HORIZON_CHECK_V10", "horizons": results, "all_ready": all(r["horizon_ready"] for r in results.values()), "any_ready": any(r["horizon_ready"] for r in results.values())}

def build_hardened_outcome(*, original_outcome: dict, forward_bars: list[dict]) -> dict:
    checks = check_all_horizons(forward_bars=forward_bars)
    result = dict(original_outcome or {})
    for h in HORIZON_REQUIREMENTS:
        key = f"actual_return_{h}"
        ck = checks["horizons"].get(h, {})
        result[f"outcome_status_{h}"] = ck.get("outcome_status")
        if not ck.get("horizon_ready"): result[key] = None
    result["required_forward_days"] = {h: HORIZON_REQUIREMENTS[h] for h in HORIZON_REQUIREMENTS}
    result["available_forward_days"] = len(forward_bars or [])
    result["horizon_data_ready"] = checks["all_ready"]
    return result
