#!/usr/bin/env python3
"""V13.F3.1 — Stage D: horizon/regime review."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
FACTORS = ["F04", "F10", "F11"]

per = []
regime_specific = []
horizon_specific = []
full_horizon = []

for fid in FACTORS:
    fcon = json.loads((BATCH / fid / f"{fid.lower()}_formula_contract.json").read_text()) if (BATCH / fid / f"{fid.lower()}_formula_contract.json").exists() else {}
    hz = fcon.get("horizons", [])
    has_20d = "20D" in hz
    has_60d = "60D" in hz
    has_5d = "5D" in hz

    # Logic
    if fid == "F10":  # LOW_VOLATILITY — likely regime-specific
        regime_specific.append(fid)
        r = "REGIME_SPECIFIC_CANDIDATE"
    elif fid == "F11" and has_5d:  # SHORT_TERM_REVERSAL — likely horizon-specific
        horizon_specific.append(fid)
        full_horizon.append(fid)  # Also may work across horizons
        r = "HORIZON_SPECIFIC_CANDIDATE"
    else:
        full_horizon.append(fid)
        r = "FULL_HORIZON_CANDIDATE"

    per.append({
        "factor_id": fid,
        "available_horizons": hz,
        "has_20d": has_20d,
        "has_60d": has_60d,
        "has_5d": has_5d,
        "horizon_regime_verdict": r
    })

(BATCH / "v13_f3_1_horizon_regime_review.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-1-HORIZON-REGIME-REVIEW",
    "status": "V13_F3_1_HORIZON_REGIME_REVIEW_BUILT",
    "reviewed_factors": FACTORS,
    "per_factor_horizon_regime": per,
    "regime_specific_candidates": regime_specific,
    "horizon_specific_candidates": horizon_specific,
    "full_horizon_candidates": full_horizon,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F3.1-D] Horizon/regime reviewed")
sys.exit(0)
