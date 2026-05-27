from __future__ import annotations
import json, csv
from pathlib import Path
from zmatrix.invalidation_anatomy.schema import DEFAULT_INVALIDATION_ANATOMY_SAFETY, DEFAULT_ANATOMY_THRESHOLDS

def _clean_date(x): return str(x or "").replace("-", "").strip()
def _to_float(x):
    try:
        if x in (None, ""): return None
        return float(x)
    except Exception: return None

def load_replay_joined(*, replay_path: str = "runtime_reports/v35_brd_strategy_replay_result.json") -> dict:
    path = Path(replay_path)
    if not path.exists(): return {"dataset_status": "BLOCKED_REPLAY_RESULT_MISSING", "joined": [], "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
    replay = json.loads(path.read_text(encoding="utf-8"))
    actions, outcomes = [], []
    for daily in replay.get("daily_results", []):
        actions.extend(daily.get("paper_actions", []))
        outcomes.extend(daily.get("outcomes", []))
    outcome_by_id = {o.get("paper_id"): o for o in outcomes}
    joined = []
    for a in actions:
        if a.get("paper_action") in ("NO_ACTION", "DATA_GAP", None): continue
        pid = a.get("paper_id"); o = outcome_by_id.get(pid, {})
        if o.get("outcome_status") != "READY": continue
        joined.append({"paper_id": pid, "ticker": a.get("ticker"), "role": a.get("role"), "paper_action": a.get("paper_action"), "entry_date": a.get("entry_date") or a.get("replay_date"), "entry_price": _to_float(a.get("entry_price")), "sector_phase": a.get("sector_phase"), "source_brd_result": a.get("source_brd_result", {}), "baseline_return_t5": o.get("actual_return_t5"), "baseline_return_t20": o.get("actual_return_t20"), "baseline_return_t60": o.get("actual_return_t60"), "baseline_invalidation_triggered": o.get("invalidation_triggered"), "baseline_max_adverse_excursion_pct": o.get("max_adverse_excursion_pct")})
    return {"dataset_version": "V354_REPLAY_JOINED_V10", "dataset_status": "READY" if joined else "BLOCKED_EMPTY_JOINED", "joined_count": len(joined), "joined": joined, "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}

def _load_price_bars(ticker, entry_date, data_root, max_days=80):
    bare = str(ticker).split(".")[0]; path = Path(data_root)/"data"/"price_bars"/f"{bare}.csv"
    if not path.exists(): return []
    entry = _clean_date(entry_date); bars = []
    with open(path, "r", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            d = _clean_date(row.get("trade_date") or row.get("date"))
            if not d or d < entry: continue
            close = row.get("close")
            if close in (None, ""): continue
            try: close_f = float(close)
            except Exception: continue
            bars.append({"trade_date": d, "close": close_f, "open": _to_float(row.get("open")), "high": _to_float(row.get("high")), "low": _to_float(row.get("low")), "volume": _to_float(row.get("vol") or row.get("volume"))})
            if len(bars) >= max_days: break
    return bars

def build_invalidation_event(*, sample: dict, price_bars: list[dict], trigger_loss_pct: float = DEFAULT_ANATOMY_THRESHOLDS["trigger_loss_pct"]) -> dict:
    entry_price = sample.get("entry_price")
    if entry_price in (None, "") and price_bars: entry_price = price_bars[0].get("close")
    entry_price = _to_float(entry_price)
    if entry_price is None or entry_price <= 0: return {"event_status": "BLOCKED_ENTRY_PRICE_MISSING", "paper_id": sample.get("paper_id"), "ticker": sample.get("ticker"), "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
    trigger_bar = None; trace = []
    for i, bar in enumerate(price_bars):
        close = _to_float(bar.get("close"))
        if close is None: continue
        ret = (close - entry_price) / entry_price * 100
        trace.append({"idx": i, "trade_date": bar.get("trade_date"), "close": close, "return_pct": round(ret, 4)})
        if ret <= trigger_loss_pct: trigger_bar = {"trigger_idx": i, "trigger_date": bar.get("trade_date"), "trigger_price": close, "trigger_return_pct": round(ret, 4)}; break
    if not trigger_bar: return {"event_status": "NO_INVALIDATION_TRIGGER", "paper_id": sample.get("paper_id"), "ticker": sample.get("ticker"), "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
    return {"event_version": "V354_INVALIDATION_EVENT_V10", "event_status": "READY", "paper_id": sample.get("paper_id"), "ticker": sample.get("ticker"), "role": sample.get("role"), "entry_date": _clean_date(sample.get("entry_date")), "entry_price": entry_price, **trigger_bar, "time_to_invalidation": trigger_bar["trigger_idx"], "baseline_return_t5": sample.get("baseline_return_t5"), "baseline_return_t20": sample.get("baseline_return_t20"), "baseline_return_t60": sample.get("baseline_return_t60"), "baseline_max_adverse_excursion_pct": sample.get("baseline_max_adverse_excursion_pct"), "price_trace_sample": trace[:15], "label_used_for_analysis_only": True, "must_not_use_as_entry_filter": True, "must_not_use_as_live_decision": True, "real_trade_allowed": False, "broker_order_allowed": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
