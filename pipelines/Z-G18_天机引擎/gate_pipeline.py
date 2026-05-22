#!/usr/bin/env python3
"""☯️ Z-G18 天机引擎 — v2.1.1 | 概率化预测与严格后验校准中枢

8条不变量:
  INV-TG18-01 Sigmoid Shield: raw→sigmoid FIRST, penalties AFTER
  INV-TG18-02 Data Lineage Cap: DAILY_OHLCV_PROXY→cap≤0.75
  INV-TG18-03 Temporal Action Gate: T5强+T1弱→WAIT_CONFIRM
  INV-TG18-04 Auto-Weight Freeze: <50 strict T+N→locked
  INV-TG18-05 No Trade Action: WATCH/WAIT/PAPER_TRACK only
  INV-TG18-06 Proxy Cannot Become PASS: inherit upstream proxy
  INV-TG18-07 Missing Lineage Is Degraded: DEFAULT→LOW confidence
  INV-TG18-08 Trigger Eligibility Is Not Execution: pending Z16/Z17

输出: 多周期概率 + 证据覆盖 + 数据血统 + 天机签 + Z9 prediction_sample
禁止: BUY/SELL/ADD/CLEAR/AUTO_TRADE/MARKET_ORDER
"""
import argparse, json, sys, os
from datetime import datetime, timedelta, timezone
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE))
TZ = timezone(timedelta(hours=8))

from zmatrix.prediction.contracts import (
    PredictionResult, ALLOWED_ACTIONS, FORBIDDEN_ACTIONS, Z9Sample,
)
from zmatrix.prediction.probability_model import fermi_weighted
from zmatrix.prediction.data_lineage import evaluate_lineage, apply_lineage_cap
from zmatrix.prediction.temporal_calibrator import evaluate_temporal_consistency
from zmatrix.prediction.event_store import PredictionEventStore, ConfigurationLockedError

try:
    from pipelines.z17_loader import market_truth, get_kline, get_financials, dq_score, l4_health
    _HAS_Z01 = True
except ImportError:
    market_truth = lambda t: {"status": "stub", "name": "?", "price": 0}
    get_kline = lambda t, d: {"prices": [], "count": 0}
    get_financials = lambda t: {}
    dq_score = lambda t: {"total": 0}
    l4_health = lambda t: {"status": "stub"}
    _HAS_Z01 = False


def _predict_single(ticker: str, name: str = "", lineage: dict | None = None) -> PredictionResult:
    """Run prediction for a single ticker. Returns PredictionResult."""
    g1 = market_truth(ticker) if _HAS_Z01 else {}
    kl = get_kline(ticker, 500) if _HAS_Z01 else {"prices": [], "count": 0}
    prices = kl.get("prices", [])
    fin = get_financials(ticker) if _HAS_Z01 else {}
    dq = dq_score(ticker) if _HAS_Z01 else {"total": 0}

    # ── Build lineage ──
    if lineage is None:
        lineage = {
            "market_data": "UNKNOWN_PROXY" if not _HAS_Z01 else "REALTIME",
            "intraday": "DAILY_OHLCV_PROXY",
            "m1": False, "l2": False,
            "source": ["Z-G01"] if _HAS_Z01 else ["UNKNOWN"],
            "upstream_status": "PASS" if _HAS_Z01 else "DEGRADED_MISSING_LINEAGE",
            "trust": "MEDIUM" if _HAS_Z01 else "LOW",
        }

    lin = evaluate_lineage(lineage)

    # ── Simple factor scoring ──
    score = 0.0
    if dq.get("total", 0) > 70: score += 2
    if fin.get("has_finance"): score += 1
    if fin.get("roe_5y_avg") and fin["roe_5y_avg"] > 10: score += 1.5
    if fin.get("pe_ttm") and fin["pe_ttm"] < 20: score += 1
    if len(prices) >= 20:
        recent = prices[-20:]
        if recent[-1] > sum(recent) / len(recent): score += 1  # above MA20
        if max(recent) / min(recent) - 1 < 0.3: score += 0.5  # low volatility

    # ── INV-TG18-01: Sigmoid Shield ──
    cov = lin.get("probability_cap", 0.75) / 0.95  # normalize to 0-1
    result_raw = fermi_weighted(raw_score=score, coverage_adj=min(cov, 1.0))

    # ── INV-TG18-02: Lineage cap ──
    raw_prob = apply_lineage_cap(result_raw["probability"], lin)
    cap = lin["probability_cap"]

    def _clamp(x, lo=0.0, hi=cap):
        return round(max(lo, min(x, hi)), 4)

    # ── Multi-horizon estimates (clamped to lineage cap) ──
    t1 = _clamp(raw_prob - 0.05)
    t5 = _clamp(raw_prob)
    t20 = _clamp(raw_prob + 0.05 if score > 3 else raw_prob - 0.05)

    # ── INV-TG18-03: Temporal consistency ──
    temporal = evaluate_temporal_consistency(t1, t5, t20)

    # ── INV-TG18-04: Auto-weight freeze — Z-G18 never allows auto-adjust ──
    z9_allowed = False
    z9_reason = "Z_G18_WRITES_PREDICTION_SAMPLE_ONLY_AUTO_ADJUST_FORBIDDEN"
    try:
        store = PredictionEventStore()
        _ = store.count_resolved_strict()  # for diagnostic, not for permission
    except Exception:
        pass  # store unavailable is fine, Z-G18 never adjusts

    # ── INV-TG18-08: Action capped, never direct PAPER_PROBE ──
    action = temporal["action_cap"]
    for forbidden in FORBIDDEN_ACTIONS:
        assert action != forbidden, f"Z-G18 leaked {forbidden}"

    return PredictionResult(
        ticker=ticker,
        name=name or g1.get("name", "?"),
        probability=round(raw_prob, 4),
        horizon={"T1": round(t1, 4), "T5": round(t5, 4), "T20": round(t20, 4)},
        evidence_coverage=round(cov, 3),
        data_lineage=lin,
        temporal_consistency=temporal,
        next_triggers=temporal.get("next_triggers", []),
        action_proposal=action,
        z9_sample={
            "strict_t_plus_n_required": True,
            "auto_adjust_allowed": z9_allowed,
            "auto_adjust_reason": z9_reason if not z9_allowed else "",
        },
        raw_score=score,
        confidence=lin["confidence_cap"],
        warnings=[],
    )


def run(tickers=None, mode="daily"):
    now = datetime.now(TZ)
    tickers = tickers or ["002472", "601899"]

    result = {
        "pipeline_signature": "Z-G18_天机引擎_v2.1.1",
        "status": "PASS_PROXY" if _HAS_Z01 else "DEGRADED",
        "mode": mode,
        "data_lineage": {},
        "predictions": [],
        "sections": {},
        "warnings": [],
        "errors": [],
    }

    print(f"\n☯️ Z-G18 天机引擎 v2.1.1 — {now.strftime('%Y-%m-%d %H:%M')}")
    print(f"   8条不变量: SigmoidShield|LineageCap|TemporalGate|WeightFreeze|NoTrade|ProxyNotPASS|MissingDegraded|TriggerNotExecute")
    print(f"   {'Z-G01已连接' if _HAS_Z01 else '⚠️ stub模式'}")
    print("=" * 60)

    strict_count = 0
    try:
        store = PredictionEventStore()
        strict_count = store.count_resolved_strict()
        print(f"\n📊 Z9状态: {strict_count}/50 strict T+N samples")
    except Exception:
        print(f"\n📊 Z9状态: store unavailable")

    predictions = []
    for t in tickers:
        pred = _predict_single(t)
        pred.validate_action()
        predictions.append(pred)

        icon = "🟢" if pred.probability > 0.65 else ("🟡" if pred.probability > 0.40 else "🔴")
        print(f"\n  {icon} {pred.ticker} {pred.name:<8s} {pred.probability*100:.0f}%"
              f" T1:{pred.horizon['T1']*100:.0f}% T5:{pred.horizon['T5']*100:.0f}%"
              f" {pred.action_proposal} [{pred.confidence}]")

    result["predictions"] = [{
        "ticker": p.ticker, "name": p.name,
        "probability": p.probability,
        "horizon": p.horizon,
        "evidence_coverage": p.evidence_coverage,
        "data_lineage": p.data_lineage,
        "temporal_consistency": p.temporal_consistency,
        "next_triggers": p.next_triggers,
        "action_proposal": p.action_proposal,
        "z9": p.z9_sample,
    } for p in predictions]

    result["sections"]["z9_strict_samples"] = strict_count
    result["sections"]["z9_samples_written"] = 0
    result["sections"]["z9_write_status"] = "DEFERRED_NOT_CONNECTED"
    result["sections"]["z9_prediction_samples_ready"] = len(predictions)
    result["sections"]["auto_adjust_allowed"] = False
    result["sections"]["auto_adjust_reason"] = "Z_G18_WRITES_PREDICTION_SAMPLE_ONLY_AUTO_ADJUST_FORBIDDEN"
    
    # Aggregate top-level data_lineage from predictions
    if predictions:
        caps = [p.data_lineage.get("probability_cap", 0.60) for p in predictions]
        confs = [p.data_lineage.get("confidence_cap", "LOW") for p in predictions]
        result["data_lineage"] = {
            "global_data_precision": "DAILY_OHLCV_PROXY",
            "probability_cap": round(min(caps), 3),
            "confidence_cap": "LOW" if "LOW" in confs else ("MEDIUM" if "MEDIUM" in confs else "HIGH"),
            "m1_connected": False, "l2_connected": False,
            "source": "AGGREGATED_FROM_PREDICTIONS",
        }
    else:
        result["data_lineage"] = {
            "global_data_precision": "DATA_GAP", "probability_cap": 0.60,
            "confidence_cap": "LOW", "m1_connected": False, "l2_connected": False,
            "source": "NO_PREDICTIONS",
        }

    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G18 天机引擎 v2.1.1")
    p.add_argument("--tickers", type=str, default="002472,601899")
    args = p.parse_args()
    run(args.tickers.split(","))
