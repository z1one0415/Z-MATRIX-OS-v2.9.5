"""G09 signal adapter — bridge Z-G09 cycle outputs into Z-G18 probability engine

G09 is the upstream cycle structure engine (四天王 + resonance + sell_decision).
G18 must consume G09 outputs as cycle evidence and be constrained by them.

Rules:
  1. G09 sell_decision (SELL_TRADING/REDUCE_CORE/MAJOR_REDUCE) → G18 cannot output PAPER_PROBE
  2. G09 exit_alert (HARVEST/FORCE_HARVEST) → G18 action_cap ≤ WAIT
  3. G09 hard_blocks non-empty → G18 probability_cap ≤ 0.55, confidence ≤ LOW
  4. G09 CYCLE_RESONANCE_STRONG → G18 can boost T5/T20 confidence (within lineage cap)
"""
from __future__ import annotations
from typing import Any


def load_g09_signals(ticker: str, g09_r_pool: list[dict] | None = None) -> dict:
    """Extract Z-G09 cycle signals for a ticker from r_pool.
    
    Returns g09_cycle evidence dict ready for Z-G18 consumption.
    """
    if not g09_r_pool:
        return _empty_g09_signal(ticker)

    for candidate in g09_r_pool:
        if candidate.get("ticker") == ticker:
            return _extract_signal(ticker, candidate)

    return _empty_g09_signal(ticker)


def _extract_signal(ticker: str, candidate: dict) -> dict:
    sell = candidate.get("sell_decision", {})
    kings = candidate.get("kings", {})

    return {
        "ticker": ticker,
        "source": "G09_CYCLE_FOUR_KING",
        "available": True,
        "resonance_status": candidate.get("resonance_status", "UNKNOWN"),
        "resonance_score": candidate.get("resonance_score", 0),
        "entry_action_cap": candidate.get("entry_action_cap", "WAIT"),
        "exit_alert": candidate.get("exit_alert", "NONE"),
        "hard_blocks": candidate.get("hard_blocks", []),
        "conflicts": candidate.get("conflicts", []),
        # Sell decision
        "position_action": sell.get("position_action", "NO_POSITION"),
        "sell_ratio": sell.get("sell_ratio", 0),
        "profit_pct": sell.get("profit_pct"),
        "profit_band": sell.get("profit_band"),
        # Kings
        "rhythm_type": kings.get("rhythm", {}).get("type") if kings.get("rhythm") else None,
        "rhythm_position": kings.get("rhythm", {}).get("position") if kings.get("rhythm") else None,
        "rhythm_action": kings.get("rhythm", {}).get("action") if kings.get("rhythm") else None,
        "rotation_type": kings.get("rotation", {}).get("type") if kings.get("rotation") else None,
        "rotation_action": kings.get("rotation", {}).get("action") if kings.get("rotation") else None,
        "oscillation_position": kings.get("oscillation", {}).get("position") if kings.get("oscillation") else None,
    }


def _empty_g09_signal(ticker: str) -> dict:
    return {
        "ticker": ticker,
        "source": "G09_UNAVAILABLE",
        "available": False,
    }


def apply_g09_constraints(
    g09_signal: dict,
    current_action: str,
    current_probability: float,
    lineage_cap: float,
) -> dict:
    """Apply G09 cycle constraints to G18 prediction outputs.

    Returns {action_override, probability_override, reason_codes, warnings}
    """
    if not g09_signal.get("available"):
        return {
            "action_override": current_action,
            "probability_override": current_probability,
            "reason_codes": ["G09_UNAVAILABLE"],
        }

    action = current_action
    prob = current_probability
    reasons = []
    warnings = []

    sell_action = g09_signal.get("position_action", "")
    exit_alert = g09_signal.get("exit_alert", "NONE")
    hard_blocks = g09_signal.get("hard_blocks", [])
    resonance = g09_signal.get("resonance_status", "UNKNOWN")

    # ── Rule 1: G09 sell signal suppresses G18 buy tendency ──
    if sell_action in ("SELL_TRADING_KEEP_CORE", "REDUCE_CORE", "MAJOR_REDUCE_OR_EXIT", "LIGHTEN_TRADING"):
        if action in ("PAPER_TRACK", "PAPER_PROBE_ELIGIBLE_PENDING_Z16_Z17"):
            action = "WAIT"
            reasons.append("G09_SELL_SIGNAL_SUPPRESSES_PAPER_PROBE")
            warnings.append(f"G09 recommends {sell_action}, G18 downgraded from PAPER_PROBE to WAIT")

    # ── Rule 2: G09 exit_alert caps G18 action ──
    if exit_alert in ("HARVEST", "FORCE_HARVEST"):
        if action not in ("WAIT", "WAIT_CONFIRM"):
            action = "WAIT"
            reasons.append("G09_EXIT_ALERT_CAPS_ACTION")
            warnings.append(f"G09 exit_alert={exit_alert}, G18 capped to WAIT")

    # ── Rule 3: G09 hard_blocks → probability & confidence cap ──
    if hard_blocks:
        prob = min(prob, 0.55)
        reasons.append("G09_HARD_BLOCKS_CAP_PROBABILITY")
        warnings.append(f"G09 hard_blocks={hard_blocks}, prob capped to 0.55")

    # ── Rule 4: Resonance strong → can boost confidence (within lineage) ──
    if resonance == "CYCLE_RESONANCE_STRONG" and not hard_blocks:
        reasons.append("G09_STRONG_RESONANCE_BOOST")
        # No direct prob boost — that's the sigmoid model's job.
        # But we signal to the oracle that this has strong cycle backing.

    return {
        "action_override": action,
        "probability_override": round(prob, 4),
        "reason_codes": reasons,
        "warnings": warnings,
    }

from pathlib import Path

def load_g09_signals_for_tickers(tickers: list[str], universe: str = "WATCHLIST") -> dict:
    """Targeted G09 signal fetch — does NOT run full universe G09 scan."""
    result = {"available": False, "reason": "not_implemented", "signals": {}, "r_pool": []}
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("zg09_gate",
            str(Path(__file__).resolve().parents[2] / "pipelines" / "Z-G09_全局轮动筛选" / "gate_pipeline.py"))
        zg09 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(zg09)
        # Targeted scan: only requested tickers, not full universe top20
        for t in tickers:
            try:
                from pipelines.z17_loader import get_kline
                kl = get_kline(t, 500)
                prices = kl.get("prices", [])
                if len(prices) >= 260:
                    from zmatrix.scoring.r_matrix.r_matrix_service import evaluate_r_matrix_cycle
                    cycle = evaluate_r_matrix_cycle(t, prices)
                    sell = cycle.get("sell_decision") or {}
                    result["signals"][t] = {
                        "ticker": t, "available": True, "source": "G09_TARGETED_SCAN",
                        "version": cycle.get("version"), "status": cycle.get("status"),
                        "r_score": cycle.get("r_score"), "r_resonance_status": cycle.get("r_resonance_status"),
                        "r_action_cap": cycle.get("r_action_cap"), "entry_action_cap": cycle.get("entry_action_cap"),
                        "exit_alert": cycle.get("exit_alert", "NONE"), "hard_blocks": cycle.get("hard_blocks", []),
                        "conflicts": cycle.get("conflicts", []), "sell_decision": sell,
                        "position_action": sell.get("position_action", "NO_POSITION"),
                    }
                else:
                    result["signals"][t] = {"ticker": t, "available": False,
                        "reason": f"INSUFFICIENT_BARS:{len(prices)}", "source": "G09_TARGETED_SCAN"}
            except Exception as e:
                result["signals"][t] = {"ticker": t, "available": False,
                    "reason": f"SERVICE_ERROR:{str(e)[:60]}", "source": "G09_TARGETED_SCAN"}
        result["available"] = any(sig.get("available") for sig in result["signals"].values()) if result["signals"] else False
        result["reason"] = "targeted_scan" if result["available"] else "no_data"
    except Exception as e:
        result["reason"] = str(e)[:120]
    return result
