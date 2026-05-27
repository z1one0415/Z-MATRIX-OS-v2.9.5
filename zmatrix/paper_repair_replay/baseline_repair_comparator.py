from __future__ import annotations
from statistics import median
from zmatrix.paper_repair_replay.schema import DEFAULT_REPAIR_REPLAY_SAFETY

def _clean(xs):
    out = []
    for x in xs:
        if x is None: continue
        try: out.append(float(x))
        except Exception: pass
    return out

def _metrics(xs):
    xs = _clean(xs); wins = [x for x in xs if x > 0]
    return {"count": len(xs), "win_rate": len(wins) / len(xs) if xs else None, "mean": sum(xs) / len(xs) if xs else None, "median": median(xs) if xs else None, "best": max(xs) if xs else None, "worst": min(xs) if xs else None}

def compare_baseline_vs_repaired(*, repaired_result: dict) -> dict:
    rows = repaired_result.get("rows", [])
    baseline = [r.get("baseline_return_t20") for r in rows if r.get("baseline_return_t20") is not None]
    repaired = [r.get("simulation", {}).get("repaired_return") for r in rows if r.get("simulation", {}).get("simulation_status") == "READY"]
    base_m = _metrics(baseline); rep_m = _metrics(repaired)
    return {"comparison_version": "V353_BASELINE_REPAIR_COMPARISON_V10", "baseline": base_m, "repaired": rep_m, "delta": {"win_rate_delta": rep_m["win_rate"] - base_m["win_rate"] if rep_m["win_rate"] is not None and base_m["win_rate"] is not None else None, "median_delta": rep_m["median"] - base_m["median"] if rep_m["median"] is not None and base_m["median"] is not None else None, "mean_delta": rep_m["mean"] - base_m["mean"] if rep_m["mean"] is not None and base_m["mean"] is not None else None}, "safety": dict(DEFAULT_REPAIR_REPLAY_SAFETY), "real_trade_allowed": False, "broker_order_allowed": False}
