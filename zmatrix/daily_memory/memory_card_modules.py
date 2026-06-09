"""☯️ G05 Daily Memory Card — Supplementary Modules v1.0

Adds 5 missing capability modules to complete the 9-module daily memory card.
These are called by the G05 gate_pipeline during card generation.

Modules:
  1. collect_g18_decisions      — G18 final decisions for watched tickers
  2. collect_g17_risk_events    — G17 risk assessments for positions
  3. collect_factor_monitoring_snapshot — factor library status summary
  4. collect_z9_posterior_entries — Z9 posterior review entry points
  5. generate_tomorrow_focus    — tomorrow's focus/review list

All modules are failsafe: missing data → graceful degradation, never crash.

签章: ☯️ Z2天师 Hermes Research Kernel | Z-MATRIX-OS v2.9.5
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# ═══ Path Constants ═══
_WORKSPACE = Path(__file__).resolve().parent.parent.parent
_RESEARCH_ROOT = _WORKSPACE / "research"
_FACTOR_LIBRARY = _RESEARCH_ROOT / "factor_library"
_PREDICTIONS_DIR = _WORKSPACE / "predictions"
_HERMES_DIR = _WORKSPACE / "hermes"

TZ = timezone(timedelta(hours=8))


# ═══════════════════════════════════════════════════════
# Module 1: G18 Decisions
# ═══════════════════════════════════════════════════════

def collect_g18_decisions(tickers: list[str]) -> dict:
    """Collect today's G18 final decisions for watched tickers.

    Returns: {ticker: {action, score, paper_track_allowed, risk_flags}}
    If G18 hasn't run today, returns empty with note.
    """
    try:
        today_str = datetime.now(TZ).strftime("%Y-%m-%d")
        results: dict[str, Any] = {}

        # Try importing G18 decision store
        try:
            from zmatrix.investment.g18_decision_store import get_today_decisions
            decisions = get_today_decisions(today_str)
            for ticker in tickers:
                if ticker in decisions:
                    d = decisions[ticker]
                    results[ticker] = {
                        "action": d.get("action", "OBSERVE"),
                        "score": d.get("score", 0),
                        "paper_track_allowed": d.get("paper_track_allowed", True),
                        "risk_flags": d.get("risk_flags", []),
                    }
        except ImportError:
            pass

        # Fallback: check JSON state files from G18 pipeline output
        if not results:
            g18_output_dir = _WORKSPACE / "pipelines" / "Z-G18_决策" / "output"
            state_file = g18_output_dir / f"{today_str}_decisions.json"
            if state_file.exists():
                with open(state_file) as f:
                    raw = json.load(f)
                for ticker in tickers:
                    if ticker in raw:
                        d = raw[ticker]
                        results[ticker] = {
                            "action": d.get("action", "OBSERVE"),
                            "score": d.get("score", 0),
                            "paper_track_allowed": d.get("paper_track_allowed", True),
                            "risk_flags": d.get("risk_flags", []),
                        }

        if not results:
            return {
                "status": "no_decisions_today",
                "note": f"G18 has not run for {today_str} or no decisions for given tickers",
                "tickers_checked": tickers,
            }

        return {"status": "ok", "date": today_str, "decisions": results}

    except Exception as e:
        return {"status": "unavailable", "reason": str(e)}


# ═══════════════════════════════════════════════════════
# Module 2: G17 Risk Events
# ═══════════════════════════════════════════════════════

def collect_g17_risk_events(tickers: list[str]) -> dict:
    """Collect G17 risk assessments for all positions.

    Returns: {ticker: {risk_level, triggered_rules, action_gate, must_review}}
    Uses human_risk_engine if available.
    """
    try:
        results: dict[str, Any] = {}

        try:
            from zmatrix.prediction.human_risk_engine import evaluate_human_risk
            from zmatrix.prediction.human_risk_schema import HumanRiskInput

            for ticker in tickers:
                # Build minimal input for risk evaluation
                risk_input = HumanRiskInput(
                    ticker=ticker,
                    position_pnl_pct=0.0,
                    holding_days=0,
                    consecutive_down_days=0,
                    drawdown_from_peak_pct=0.0,
                    sector_divergence=False,
                    has_stop_loss=False,
                    news_sentiment="neutral",
                )
                assessment = evaluate_human_risk(risk_input)
                results[ticker] = {
                    "risk_level": assessment.risk_level,
                    "triggered_rules": [r.rule_id for r in assessment.triggered_rules],
                    "action_gate": assessment.action_gate,
                    "must_review": assessment.risk_level in ("RED", "BLACK"),
                }
        except (ImportError, TypeError, AttributeError):
            # human_risk_engine not available or schema mismatch
            for ticker in tickers:
                results[ticker] = {
                    "risk_level": "UNKNOWN",
                    "triggered_rules": [],
                    "action_gate": "OBSERVE",
                    "must_review": False,
                }

        return {"status": "ok", "assessments": results}

    except Exception as e:
        return {"status": "unavailable", "reason": str(e)}


# ═══════════════════════════════════════════════════════
# Module 3: Factor Monitoring Snapshot
# ═══════════════════════════════════════════════════════

def collect_factor_monitoring_snapshot() -> dict:
    """Summarize factor monitoring status.

    Returns: {total_factors, signal_ready, monitoring_done, blocked, last_run_date}
    Reads from research/factor_library/ state files.
    """
    try:
        registry_path = _FACTOR_LIBRARY / "registry.json"
        if not registry_path.exists():
            return {
                "status": "unavailable",
                "reason": "factor_library/registry.json not found",
            }

        with open(registry_path) as f:
            registry = json.load(f)

        # Count factors by status
        total_factors = 0
        signal_ready = 0
        monitoring_done = 0
        blocked = 0
        last_run_date = None

        if isinstance(registry, dict):
            factors = registry.get("factors", registry)
            if isinstance(factors, list):
                total_factors = len(factors)
                for fac in factors:
                    status = fac.get("status", "")
                    if status in ("signal_ready", "active"):
                        signal_ready += 1
                    elif status in ("monitoring", "monitoring_done"):
                        monitoring_done += 1
                    elif status in ("blocked", "rejected"):
                        blocked += 1
                    run_date = fac.get("last_run", fac.get("updated"))
                    if run_date and (not last_run_date or run_date > last_run_date):
                        last_run_date = run_date
            elif isinstance(factors, dict):
                total_factors = len(factors)
                for fid, fac in factors.items():
                    status = fac.get("status", "")
                    if status in ("signal_ready", "active"):
                        signal_ready += 1
                    elif status in ("monitoring", "monitoring_done"):
                        monitoring_done += 1
                    elif status in ("blocked", "rejected"):
                        blocked += 1
                    run_date = fac.get("last_run", fac.get("updated"))
                    if run_date and (not last_run_date or run_date > last_run_date):
                        last_run_date = run_date

        return {
            "status": "ok",
            "total_factors": total_factors,
            "signal_ready": signal_ready,
            "monitoring_done": monitoring_done,
            "blocked": blocked,
            "last_run_date": last_run_date,
        }

    except Exception as e:
        return {"status": "unavailable", "reason": str(e)}


# ═══════════════════════════════════════════════════════
# Module 4: Z9 Posterior Entries
# ═══════════════════════════════════════════════════════

def collect_z9_posterior_entries(date_str: str) -> dict:
    """Generate Z9 posterior review entry points for today.

    Returns: {predictions_due: [...], validations_pending: [...], calibration_status: {...}}
    """
    try:
        predictions_due: list[dict] = []
        validations_pending: list[dict] = []
        calibration_status: dict[str, Any] = {
            "total_predictions": 0,
            "validated": 0,
            "accuracy_pct": None,
        }

        # Check predictions directory for due items
        pred_dir = _PREDICTIONS_DIR
        if pred_dir.exists():
            for pfile in sorted(pred_dir.glob("*.json")):
                try:
                    with open(pfile) as f:
                        pred = json.load(f)
                    due_date = pred.get("validation_due", pred.get("due_date"))
                    if due_date == date_str:
                        predictions_due.append({
                            "id": pred.get("id", pfile.stem),
                            "ticker": pred.get("ticker", "?"),
                            "prediction": pred.get("prediction", "?"),
                            "made_date": pred.get("date", "?"),
                        })
                    status = pred.get("status", "")
                    if status == "pending_validation":
                        validations_pending.append({
                            "id": pred.get("id", pfile.stem),
                            "ticker": pred.get("ticker", "?"),
                            "due": due_date or "?",
                        })
                    calibration_status["total_predictions"] += 1
                    if status == "validated":
                        calibration_status["validated"] += 1
                except (json.JSONDecodeError, KeyError):
                    continue

        # Calculate accuracy
        total = calibration_status["total_predictions"]
        validated = calibration_status["validated"]
        if total > 0 and validated > 0:
            calibration_status["accuracy_pct"] = round(validated / total * 100, 1)

        # Also check hermes prediction records
        hermes_pred = _HERMES_DIR / "predictions"
        if hermes_pred.exists():
            for pfile in sorted(hermes_pred.glob(f"{date_str}*.json")):
                try:
                    with open(pfile) as f:
                        pred = json.load(f)
                    predictions_due.append({
                        "id": pred.get("id", pfile.stem),
                        "ticker": pred.get("ticker", "?"),
                        "prediction": pred.get("prediction", "?"),
                        "made_date": pred.get("date", date_str),
                    })
                except (json.JSONDecodeError, KeyError):
                    continue

        return {
            "status": "ok",
            "date": date_str,
            "predictions_due": predictions_due,
            "validations_pending": validations_pending[:20],
            "calibration_status": calibration_status,
        }

    except Exception as e:
        return {"status": "unavailable", "reason": str(e)}


# ═══════════════════════════════════════════════════════
# Module 5: Tomorrow Focus List
# ═══════════════════════════════════════════════════════

def generate_tomorrow_focus(
    g18_decisions: dict,
    g17_events: dict,
    catalysts: list,
) -> list[dict]:
    """Generate tomorrow's focus/review list based on today's state.

    Returns: [{ticker, reason, priority, action_required}]
    Priority order: events > risk > decisions > routine
    """
    try:
        focus_items: list[dict] = []
        seen_tickers: set[str] = set()

        # Priority 1: Catalysts (events) — highest priority
        if catalysts:
            for cat in catalysts:
                ticker = cat.get("ticker", "MACRO")
                if ticker not in seen_tickers:
                    focus_items.append({
                        "ticker": ticker,
                        "reason": f"催化剂: {cat.get('event', '未知事件')}",
                        "priority": "HIGH",
                        "action_required": "REVIEW_IMPACT",
                    })
                    seen_tickers.add(ticker)

        # Priority 2: Risk events (G17 RED/BLACK)
        assessments = g17_events.get("assessments", {})
        for ticker, assessment in assessments.items():
            if ticker in seen_tickers:
                continue
            risk_level = assessment.get("risk_level", "GREEN")
            if risk_level in ("RED", "BLACK", "ORANGE"):
                focus_items.append({
                    "ticker": ticker,
                    "reason": f"风控{risk_level}: {', '.join(assessment.get('triggered_rules', [])[:3])}",
                    "priority": "HIGH" if risk_level in ("RED", "BLACK") else "MEDIUM",
                    "action_required": assessment.get("action_gate", "REVIEW"),
                })
                seen_tickers.add(ticker)

        # Priority 3: G18 decisions requiring action
        decisions = g18_decisions.get("decisions", {})
        for ticker, decision in decisions.items():
            if ticker in seen_tickers:
                continue
            action = decision.get("action", "OBSERVE")
            if action not in ("OBSERVE", "HOLD"):
                focus_items.append({
                    "ticker": ticker,
                    "reason": f"G18决策: {action} (评分{decision.get('score', 0)})",
                    "priority": "MEDIUM",
                    "action_required": action,
                })
                seen_tickers.add(ticker)

        # Priority 4: Routine — risk flags without high risk
        for ticker, assessment in assessments.items():
            if ticker in seen_tickers:
                continue
            if assessment.get("triggered_rules"):
                focus_items.append({
                    "ticker": ticker,
                    "reason": f"常规复核: {assessment.get('risk_level', 'YELLOW')}",
                    "priority": "LOW",
                    "action_required": "MONITOR",
                })
                seen_tickers.add(ticker)

        # Sort by priority
        priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        focus_items.sort(key=lambda x: priority_order.get(x.get("priority", "LOW"), 3))

        return focus_items

    except Exception as e:
        return [{"ticker": "SYSTEM", "reason": f"生成失败: {e}", "priority": "LOW", "action_required": "NONE"}]
