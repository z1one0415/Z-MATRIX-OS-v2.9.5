"""☯️ G17 Human Risk Rule Engine v1.0

Position-level risk assessment: evaluates whether a stock is currently dangerous.
NOT behavioral tilt detection (that's in the pipeline).
This is: "Is this position in danger?" vs "Is the human being emotional?"

Output: risk_level (GREEN/YELLOW/ORANGE/RED/BLACK) + action gates + triggered rules.

Usage:
    from zmatrix.prediction.human_risk_engine import evaluate_human_risk
    result = evaluate_human_risk(input_data)
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from zmatrix.prediction.human_risk_schema import (
    HumanRiskInput,
    HumanRiskAssessment,
    TriggeredRule,
)


# ═══════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════

SEVERITY_WEIGHT = {"LOW": 1, "MEDIUM": 2, "HIGH": 4, "CRITICAL": 8}

ACTION_GATE_MAP = {
    "GREEN": "OBSERVE",
    "YELLOW": "CONDITIONAL_TRACK",
    "ORANGE": "WAIT",
    "RED": "REDUCE_OR_WAIT",
    "BLACK": "EXIT_REVIEW",
}

_DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "configs" / "risk_rules" / "human_risk_rules_v1.json"


# ═══════════════════════════════════════════════════════
# Config loader
# ═══════════════════════════════════════════════════════

def load_rule_config(config_path: Optional[str] = None) -> dict:
    """Load rule thresholds from JSON config. Falls back to hardcoded defaults."""
    path = Path(config_path) if config_path else _DEFAULT_CONFIG_PATH
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return _default_config()


def _default_config() -> dict:
    """Hardcoded defaults if JSON not found."""
    return {
        "version": "1.0",
        "rules": {
            "R01": {"severity": "HIGH"},
            "R02": {"threshold": -0.05, "severity": "MEDIUM"},
            "R03": {"combined_threshold": -0.04, "severity": "MEDIUM"},
            "R04": {"severity": "HIGH"},
            "R05": {"min_breaks": 2, "severity": "CRITICAL"},
            "R06": {"volume_ratio": 2.0, "shadow_ratio": 0.03, "severity": "HIGH"},
            "R07": {"volume_ratio": 1.5, "return_threshold": -0.02, "severity": "MEDIUM"},
            "R08": {"volume_ratio": 0.6, "severity": "LOW"},
            "R09": {"sector_threshold": -0.03, "severity": "MEDIUM"},
            "R10": {"index_threshold": -0.03, "severity": "MEDIUM"},
            "R11": {"days_threshold": 3, "severity": "MEDIUM"},
            "R12": {"loss_threshold": -0.15, "severity": "HIGH"},
        },
        "risk_level_thresholds": {
            "BLACK": {"critical_count": 1, "loss_pct": -0.20},
            "RED": {"critical_count": 1, "high_count": 3},
            "ORANGE": {"high_count": 2, "high_plus_medium": [1, 2]},
            "YELLOW": {"high_count": 1, "medium_count": 2},
        },
    }


# ═══════════════════════════════════════════════════════
# Rule Evaluation Functions (R01–R12)
# ═══════════════════════════════════════════════════════

def _eval_r01_cost_line_break(inp: HumanRiskInput, cfg: dict) -> Optional[TriggeredRule]:
    """R01: close < user_cost_line"""
    if inp.close is None or inp.user_cost_line is None:
        return None
    if inp.close < inp.user_cost_line:
        return TriggeredRule(
            rule_id="R01", name="成本线跌破", severity=cfg["rules"]["R01"]["severity"],
            description=f"收盘价 {inp.close:.2f} < 成本线 {inp.user_cost_line:.2f}",
            values={"close": inp.close, "cost_line": inp.user_cost_line},
        )
    return None


def _eval_r02_daily_drop(inp: HumanRiskInput, cfg: dict) -> Optional[TriggeredRule]:
    """R02: daily_return < -5%"""
    if inp.daily_return is None:
        return None
    threshold = cfg["rules"]["R02"]["threshold"]
    if inp.daily_return < threshold:
        return TriggeredRule(
            rule_id="R02", name="单日跌幅超阈值", severity=cfg["rules"]["R02"]["severity"],
            description=f"日跌幅 {inp.daily_return*100:.1f}% < {threshold*100:.0f}%",
            values={"daily_return": inp.daily_return, "threshold": threshold},
        )
    return None


def _eval_r03_consecutive_decline(inp: HumanRiskInput, cfg: dict) -> Optional[TriggeredRule]:
    """R03: day1 < 0 AND day2 < 0 AND combined < -4%"""
    if inp.daily_return is None or inp.prior_day_return is None:
        return None
    combined_threshold = cfg["rules"]["R03"]["combined_threshold"]
    if inp.daily_return < 0 and inp.prior_day_return < 0:
        combined = inp.daily_return + inp.prior_day_return
        if combined < combined_threshold:
            return TriggeredRule(
                rule_id="R03", name="连续两日下跌", severity=cfg["rules"]["R03"]["severity"],
                description=f"两日合计跌幅 {combined*100:.1f}% < {combined_threshold*100:.0f}%",
                values={"daily_return": inp.daily_return, "prior_day_return": inp.prior_day_return, "combined": combined},
            )
    return None


def _eval_r04_support_break(inp: HumanRiskInput, cfg: dict) -> Optional[TriggeredRule]:
    """R04: close < d1_support"""
    if inp.close is None or inp.d1_support is None:
        return None
    if inp.close < inp.d1_support:
        return TriggeredRule(
            rule_id="R04", name="支撑位跌破", severity=cfg["rules"]["R04"]["severity"],
            description=f"收盘价 {inp.close:.2f} < 支撑位 {inp.d1_support:.2f}",
            values={"close": inp.close, "d1_support": inp.d1_support},
        )
    return None


def _eval_r05_multi_break(inp: HumanRiskInput, cfg: dict) -> Optional[TriggeredRule]:
    """R05: cost_break + support_break + cycle_break >= 2"""
    # Compute breaks from data if not pre-computed
    cost_brk = inp.cost_break
    if cost_brk is None and inp.close is not None and inp.user_cost_line is not None:
        cost_brk = inp.close < inp.user_cost_line
    support_brk = inp.support_break
    if support_brk is None and inp.close is not None and inp.d1_support is not None:
        support_brk = inp.close < inp.d1_support
    cycle_brk = inp.cycle_break
    if cycle_brk is None and inp.close is not None and inp.cycle_origin is not None:
        cycle_brk = inp.close < inp.cycle_origin

    breaks = sum(1 for b in [cost_brk, support_brk, cycle_brk] if b)
    min_breaks = cfg["rules"]["R05"]["min_breaks"]
    if breaks >= min_breaks:
        return TriggeredRule(
            rule_id="R05", name="三线共振破位", severity=cfg["rules"]["R05"]["severity"],
            description=f"破位数 {breaks}/3 (成本={cost_brk}, 支撑={support_brk}, 周期={cycle_brk})",
            values={"cost_break": cost_brk, "support_break": support_brk, "cycle_break": cycle_brk, "count": breaks},
        )
    return None


def _eval_r06_volume_climax_shadow(inp: HumanRiskInput, cfg: dict) -> Optional[TriggeredRule]:
    """R06: volume >= 2.0 * avg_vol_20d AND (high-close)/high >= 0.03"""
    if inp.volume is None or inp.avg_volume_20d is None:
        return None
    if inp.high is None or inp.close is None:
        return None
    if inp.avg_volume_20d <= 0 or inp.high <= 0:
        return None
    vol_ratio_thresh = cfg["rules"]["R06"]["volume_ratio"]
    shadow_thresh = cfg["rules"]["R06"]["shadow_ratio"]
    vol_ratio = inp.volume / inp.avg_volume_20d
    shadow_ratio = (inp.high - inp.close) / inp.high
    if vol_ratio >= vol_ratio_thresh and shadow_ratio >= shadow_thresh:
        return TriggeredRule(
            rule_id="R06", name="天量长上影", severity=cfg["rules"]["R06"]["severity"],
            description=f"量比 {vol_ratio:.1f}x ≥ {vol_ratio_thresh}x, 上影 {shadow_ratio*100:.1f}% ≥ {shadow_thresh*100:.0f}%",
            values={"volume_ratio": vol_ratio, "shadow_ratio": shadow_ratio},
        )
    return None


def _eval_r07_volume_decline(inp: HumanRiskInput, cfg: dict) -> Optional[TriggeredRule]:
    """R07: volume >= 1.5 * avg_vol_20d AND daily_return < -2%"""
    if inp.volume is None or inp.avg_volume_20d is None or inp.daily_return is None:
        return None
    if inp.avg_volume_20d <= 0:
        return None
    vol_ratio_thresh = cfg["rules"]["R07"]["volume_ratio"]
    return_thresh = cfg["rules"]["R07"]["return_threshold"]
    vol_ratio = inp.volume / inp.avg_volume_20d
    if vol_ratio >= vol_ratio_thresh and inp.daily_return < return_thresh:
        return TriggeredRule(
            rule_id="R07", name="放量下跌", severity=cfg["rules"]["R07"]["severity"],
            description=f"量比 {vol_ratio:.1f}x ≥ {vol_ratio_thresh}x, 跌幅 {inp.daily_return*100:.1f}%",
            values={"volume_ratio": vol_ratio, "daily_return": inp.daily_return},
        )
    return None


def _eval_r08_thin_rebound(inp: HumanRiskInput, cfg: dict) -> Optional[TriggeredRule]:
    """R08: volume < 0.6 * avg_vol_20d AND daily_return > 0 AND prior_breakdown"""
    if inp.volume is None or inp.avg_volume_20d is None or inp.daily_return is None:
        return None
    if inp.avg_volume_20d <= 0:
        return None
    if not inp.prior_breakdown:
        return None
    vol_ratio_thresh = cfg["rules"]["R08"]["volume_ratio"]
    vol_ratio = inp.volume / inp.avg_volume_20d
    if vol_ratio < vol_ratio_thresh and inp.daily_return > 0:
        return TriggeredRule(
            rule_id="R08", name="缩量反弹", severity=cfg["rules"]["R08"]["severity"],
            description=f"量比 {vol_ratio:.2f}x < {vol_ratio_thresh}x, 涨幅 {inp.daily_return*100:.1f}%, 此前已破位",
            values={"volume_ratio": vol_ratio, "daily_return": inp.daily_return, "prior_breakdown": True},
        )
    return None


def _eval_r09_sector_headwind(inp: HumanRiskInput, cfg: dict) -> Optional[TriggeredRule]:
    """R09: sector_5d_return < -3%"""
    if inp.sector_5d_return is None:
        return None
    threshold = cfg["rules"]["R09"]["sector_threshold"]
    if inp.sector_5d_return < threshold:
        return TriggeredRule(
            rule_id="R09", name="板块逆风", severity=cfg["rules"]["R09"]["severity"],
            description=f"板块5日涨跌 {inp.sector_5d_return*100:.1f}% < {threshold*100:.0f}%",
            values={"sector_5d_return": inp.sector_5d_return},
        )
    return None


def _eval_r10_market_risk(inp: HumanRiskInput, cfg: dict) -> Optional[TriggeredRule]:
    """R10: index_5d_return < -3% OR vix_equiv > threshold"""
    index_threshold = cfg["rules"]["R10"]["index_threshold"]
    index_triggered = inp.index_5d_return is not None and inp.index_5d_return < index_threshold
    vix_triggered = inp.vix_equiv is not None and inp.vix_equiv > inp.vix_threshold
    if index_triggered or vix_triggered:
        parts = []
        if index_triggered:
            parts.append(f"大盘5日 {inp.index_5d_return*100:.1f}%")
        if vix_triggered:
            parts.append(f"VIX等价 {inp.vix_equiv:.1f} > {inp.vix_threshold:.0f}")
        return TriggeredRule(
            rule_id="R10", name="大盘风险", severity=cfg["rules"]["R10"]["severity"],
            description=" + ".join(parts),
            values={"index_5d_return": inp.index_5d_return, "vix_equiv": inp.vix_equiv},
        )
    return None


def _eval_r11_event_window(inp: HumanRiskInput, cfg: dict) -> Optional[TriggeredRule]:
    """R11: event_window_active AND days_to_event <= 3"""
    if not inp.event_window_active:
        return None
    days_thresh = cfg["rules"]["R11"]["days_threshold"]
    if inp.days_to_event is not None and inp.days_to_event <= days_thresh:
        return TriggeredRule(
            rule_id="R11", name="事件风险窗口", severity=cfg["rules"]["R11"]["severity"],
            description=f"事件窗口激活, {inp.days_to_event}日内有重大事件",
            values={"days_to_event": inp.days_to_event},
        )
    return None


def _eval_r12_loss_threshold(inp: HumanRiskInput, cfg: dict) -> Optional[TriggeredRule]:
    """R12: unrealized_loss_pct > 15% (stored as negative decimal)"""
    if inp.unrealized_loss_pct is None:
        return None
    loss_threshold = cfg["rules"]["R12"]["loss_threshold"]
    if inp.unrealized_loss_pct < loss_threshold:
        return TriggeredRule(
            rule_id="R12", name="持仓亏损阈值", severity=cfg["rules"]["R12"]["severity"],
            description=f"浮亏 {inp.unrealized_loss_pct*100:.1f}% 超过 {loss_threshold*100:.0f}%",
            values={"unrealized_loss_pct": inp.unrealized_loss_pct, "threshold": loss_threshold},
        )
    return None


# ═══════════════════════════════════════════════════════
# Risk Level Classification
# ═══════════════════════════════════════════════════════

ALL_RULE_EVALUATORS = [
    _eval_r01_cost_line_break,
    _eval_r02_daily_drop,
    _eval_r03_consecutive_decline,
    _eval_r04_support_break,
    _eval_r05_multi_break,
    _eval_r06_volume_climax_shadow,
    _eval_r07_volume_decline,
    _eval_r08_thin_rebound,
    _eval_r09_sector_headwind,
    _eval_r10_market_risk,
    _eval_r11_event_window,
    _eval_r12_loss_threshold,
]


def classify_risk_level(triggered_rules: list, unrealized_loss_pct: Optional[float] = None) -> str:
    """Classify aggregate risk level from triggered rules.

    BLACK: any CRITICAL + unrealized_loss > 20%
    RED: any CRITICAL OR 3+ HIGH
    ORANGE: 2+ HIGH OR (1 HIGH + 2 MEDIUM)
    YELLOW: 1 HIGH OR 2+ MEDIUM
    GREEN: 0 HIGH, 0-1 MEDIUM
    """
    severities = [r.severity for r in triggered_rules]
    critical_count = severities.count("CRITICAL")
    high_count = severities.count("HIGH")
    medium_count = severities.count("MEDIUM")

    loss = unrealized_loss_pct if unrealized_loss_pct is not None else 0.0

    # BLACK: CRITICAL + deep loss
    if critical_count >= 1 and loss < -0.20:
        return "BLACK"

    # RED: any CRITICAL OR 3+ HIGH
    if critical_count >= 1 or high_count >= 3:
        return "RED"

    # ORANGE: 2+ HIGH OR (1 HIGH + 2+ MEDIUM)
    if high_count >= 2 or (high_count >= 1 and medium_count >= 2):
        return "ORANGE"

    # YELLOW: 1 HIGH OR 2+ MEDIUM
    if high_count >= 1 or medium_count >= 2:
        return "YELLOW"

    # GREEN
    return "GREEN"


def compute_risk_score(triggered_rules: list) -> int:
    """Compute 0-100 risk score from triggered rules.

    Weighted sum of severities, capped at 100.
    """
    if not triggered_rules:
        return 0
    total = sum(SEVERITY_WEIGHT.get(r.severity, 0) for r in triggered_rules)
    # Normalize: 1 CRITICAL(8) + 2 HIGH(8) + 3 MEDIUM(6) = 22 → aim for 100 at ~20 weight
    score = min(100, int(total * 5))
    return score


# ═══════════════════════════════════════════════════════
# Main Entry Point
# ═══════════════════════════════════════════════════════

def evaluate_human_risk(
    inp: HumanRiskInput,
    config_path: Optional[str] = None,
) -> HumanRiskAssessment:
    """Evaluate all 12 human risk rules and produce risk assessment.

    Args:
        inp: HumanRiskInput with current position/market data
        config_path: optional path to JSON rule config

    Returns:
        HumanRiskAssessment with risk_level, action_gate, and explanations
    """
    cfg = load_rule_config(config_path)

    # ── Evaluate all rules ──
    triggered: list[TriggeredRule] = []
    for evaluator in ALL_RULE_EVALUATORS:
        result = evaluator(inp, cfg)
        if result is not None:
            triggered.append(result)

    # ── Classify risk level ──
    risk_level = classify_risk_level(triggered, inp.unrealized_loss_pct)

    # ── Compute score ──
    risk_score = compute_risk_score(triggered)

    # ── Determine action gate ──
    action_gate = ACTION_GATE_MAP[risk_level]

    # ── Determine permissions ──
    if risk_level == "GREEN":
        add_position_allowed = True
        paper_track_allowed = True
        must_review = False
    elif risk_level == "YELLOW":
        add_position_allowed = True
        paper_track_allowed = True
        must_review = False
    elif risk_level == "ORANGE":
        add_position_allowed = False
        paper_track_allowed = False
        must_review = True
    elif risk_level == "RED":
        add_position_allowed = False
        paper_track_allowed = False
        must_review = True
    else:  # BLACK
        add_position_allowed = False
        paper_track_allowed = False
        must_review = True

    # ── Build explanation ──
    explain = {
        "summary": _build_summary(risk_level, triggered),
        "rule_count": len(triggered),
        "severity_breakdown": {
            "CRITICAL": sum(1 for r in triggered if r.severity == "CRITICAL"),
            "HIGH": sum(1 for r in triggered if r.severity == "HIGH"),
            "MEDIUM": sum(1 for r in triggered if r.severity == "MEDIUM"),
            "LOW": sum(1 for r in triggered if r.severity == "LOW"),
        },
    }

    return HumanRiskAssessment(
        ticker=inp.ticker,
        risk_level=risk_level,
        risk_score=risk_score,
        triggered_rules=triggered,
        action_gate=action_gate,
        add_position_allowed=add_position_allowed,
        paper_track_allowed=paper_track_allowed,
        must_review=must_review,
        explain=explain,
    )


def _build_summary(risk_level: str, triggered: list) -> str:
    """Human-readable one-line summary."""
    if not triggered:
        return "无风险规则触发，持仓安全。"
    names = [r.name for r in triggered]
    return f"风险等级 {risk_level}，触发 {len(triggered)} 条规则: {', '.join(names)}"
