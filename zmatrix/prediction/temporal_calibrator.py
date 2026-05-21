"""Temporal calibrator — INV-TG18-03 + INV-TG18-08

Multi-horizon: T1/T5/T20.
T5 high + T1 weak → action capped to WAIT_CONFIRM/PAPER_TRACK.
PAPER_PROBE_ELIGIBLE must be pending Z16/Z17.
"""
from __future__ import annotations


def evaluate_temporal_consistency(t1_score: float | None, t5_score: float | None,
                                  t20_score: float | None) -> dict:
    """Check multi-horizon alignment. Returns consistency + action recommendation."""
    scores = []
    if t1_score is not None: scores.append(("T1", t1_score))
    if t5_score is not None: scores.append(("T5", t5_score))
    if t20_score is not None: scores.append(("T20", t20_score))

    if not scores:
        return {"consistency": "UNKNOWN", "action_cap": "WAIT", "next_triggers": []}

    high = [(h, s) for h, s in scores if s >= 0.75]
    low = [(h, s) for h, s in scores if s < 0.58]

    # INV-TG18-03: T5 high but T1 weak
    has_t5_high = any(h == "T5" and s > 0.65 for h, s in high)
    has_t1_weak = any(h == "T1" and s < 0.40 for h, s in low)
    has_all_high = len(high) == len(scores) and len(scores) >= 2
    has_all_low = len(low) == len(scores) and len(scores) >= 2

    if has_t5_high and has_t1_weak:
        action_cap = "WAIT_CONFIRM"
        consistency = "LONG_STRONG_SHORT_WEAK"
        triggers = [{
            "trigger_id": "NEXT_AUCTION_WEAK_TO_STRONG",
            "source_pipeline": "Z-G03",
            "required_signal": "DAILY_WEAK_TO_STRONG",
            "deadline": "NEXT_TRADING_DAY_09:35",
            "on_pass": "PAPER_PROBE_ELIGIBLE_PENDING_Z16_Z17",
            "on_fail": "EXPIRED",
        }]
    elif has_all_high:
        action_cap = "PAPER_PROBE_ELIGIBLE_PENDING_Z16_Z17"
        consistency = "ALL_HORIZON_STRONG"
        triggers = [{
            "trigger_id": "Z16_PAPER_EXECUTION_REVIEW",
            "source_pipeline": "Z-G16",
            "required_signal": "PAPER_PLAN_APPROVED",
            "deadline": "NEXT_TRADING_DAY_15:00",
            "on_pass": "PAPER_TRACK",
            "on_fail": "WAIT",
        }]
    elif has_all_low:
        action_cap = "WAIT"
        consistency = "ALL_HORIZON_WEAK"
        triggers = []
    else:
        action_cap = "PAPER_TRACK" if high else "WAIT"
        consistency = "MIXED"
        triggers = []

    return {
        "consistency": consistency,
        "action_cap": action_cap,
        "next_triggers": triggers,
        "horizons": {h: round(s, 3) for h, s in scores},
    }
