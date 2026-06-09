"""G18 Fast Risk Overlay v1.0 — dynamic risk gates that override static base_score.

Core principle: slow variables (lineage, cycle, horizon) provide base_score only;
fast variables (volume, shadows, support breaks, events) own action gate veto power.

This module evaluates 10 fast risk gates and produces:
  - triggered_gates: list of fired gate IDs
  - total_penalty: cumulative score reduction
  - paper_track_allowed: boolean veto
  - final_score_cap: maximum allowed score
  - recommended_action: action derived from gated score

Usage:
    from zmatrix.prediction.fast_risk_overlay import evaluate_fast_risk_overlay
    result = evaluate_fast_risk_overlay(market_snapshot, base_score=75)
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


# ═══════════════════════════════════════════════════════
# Gate Definitions
# ═══════════════════════════════════════════════════════

GATE_DEFINITIONS = {
    "R1_VOLUME_CLIMAX": {"severity": "HIGH", "penalty": -10},
    "R2_LONG_UPPER_SHADOW": {"severity": "HIGH", "penalty": -15},
    "R3_COST_LINE_BREAK": {"severity": "HIGH", "penalty": -15},
    "R4_D1_SUPPORT_BREAK": {"severity": "HIGH", "penalty": -15},
    "R5_CYCLE_ORIGIN_BREAK": {"severity": "HIGH", "penalty": -20},
    "R6_MULTI_SUPPORT_BREAK": {"severity": "CRITICAL", "penalty": -35},
    "R7_EVENT_RISK_WINDOW": {"severity": "MEDIUM", "penalty": -10},
    "R8_SECTOR_ROTATION_FADE": {"severity": "MEDIUM", "penalty": -15},
    "R9_MARKET_STYLE_HEADWIND": {"severity": "MEDIUM", "penalty": -10},
    "R10_CATALYST_DECAY_EXPIRED": {"severity": "MEDIUM", "penalty": -10},
}

SEVERITY_ORDER = {"CRITICAL": 3, "HIGH": 2, "MEDIUM": 1, "NONE": 0}


# ═══════════════════════════════════════════════════════
# Market Snapshot (input contract)
# ═══════════════════════════════════════════════════════

@dataclass
class MarketSnapshot:
    """Input data for fast risk evaluation."""
    close: float | None = None
    high: float | None = None
    volume: float | None = None
    avg_volume_20d: float | None = None
    user_cost_line: float | None = None
    d1_support: float | None = None
    cycle_origin: float | None = None
    event_window_active: bool = False
    event_confirmation_received: bool = False
    sector_momentum_rank_current: int | None = None
    sector_momentum_rank_prior: int | None = None
    style_mismatch_duration_days: int = 0
    days_since_catalyst: int | None = None
    catalyst_decay_threshold: int = 20
    catalyst_refreshed: bool = False


# ═══════════════════════════════════════════════════════
# Gate Evaluation Functions
# ═══════════════════════════════════════════════════════

def _check_r1_volume_climax(snap: MarketSnapshot) -> bool:
    """R1: volume >= 2.0 * avg_volume_20d"""
    if snap.volume is None or snap.avg_volume_20d is None:
        return False
    if snap.avg_volume_20d <= 0:
        return False
    return snap.volume >= 2.0 * snap.avg_volume_20d


def _check_r2_long_upper_shadow(snap: MarketSnapshot) -> bool:
    """R2: (high - close) / high >= 0.03"""
    if snap.high is None or snap.close is None:
        return False
    if snap.high <= 0:
        return False
    return (snap.high - snap.close) / snap.high >= 0.03


def _check_r3_cost_line_break(snap: MarketSnapshot) -> bool:
    """R3: close < user_cost_line"""
    if snap.close is None or snap.user_cost_line is None:
        return False
    return snap.close < snap.user_cost_line


def _check_r4_d1_support_break(snap: MarketSnapshot) -> bool:
    """R4: close < d1_support"""
    if snap.close is None or snap.d1_support is None:
        return False
    return snap.close < snap.d1_support


def _check_r5_cycle_origin_break(snap: MarketSnapshot) -> bool:
    """R5: close < cycle_origin"""
    if snap.close is None or snap.cycle_origin is None:
        return False
    return snap.close < snap.cycle_origin


def _check_r6_multi_support_break(r3: bool, r4: bool, r5: bool) -> bool:
    """R6: two or more of R3/R4/R5 triggered"""
    return sum([r3, r4, r5]) >= 2


def _check_r7_event_risk_window(snap: MarketSnapshot) -> bool:
    """R7: event_window_active AND no confirmation"""
    return snap.event_window_active and not snap.event_confirmation_received


def _check_r8_sector_rotation_fade(snap: MarketSnapshot) -> bool:
    """R8: sector_momentum_rank drop >= 5"""
    if snap.sector_momentum_rank_current is None or snap.sector_momentum_rank_prior is None:
        return False
    return snap.sector_momentum_rank_current - snap.sector_momentum_rank_prior >= 5


def _check_r9_market_style_headwind(snap: MarketSnapshot) -> bool:
    """R9: style_mismatch_duration >= 5 trading days"""
    return snap.style_mismatch_duration_days >= 5


def _check_r10_catalyst_decay_expired(snap: MarketSnapshot) -> bool:
    """R10: days_since_catalyst > threshold AND no refresh"""
    if snap.days_since_catalyst is None:
        return False
    return (snap.days_since_catalyst > snap.catalyst_decay_threshold
            and not snap.catalyst_refreshed)


# ═══════════════════════════════════════════════════════
# Core Evaluation Engine
# ═══════════════════════════════════════════════════════

@dataclass
class FastRiskResult:
    """Output of fast risk overlay evaluation."""
    triggered_gates: list = field(default_factory=list)
    gate_details: dict = field(default_factory=dict)
    max_severity: str = "NONE"
    high_count: int = 0
    critical_count: int = 0
    total_penalty: int = 0
    paper_track_allowed: bool = True
    final_score_cap: int = 100
    final_score: int = 75
    recommended_action: str = "PAPER_TRACK"
    action_gate_reason: str = ""


def evaluate_fast_risk_overlay(
    snap: MarketSnapshot,
    base_score: int = 75,
) -> FastRiskResult:
    """Evaluate all 10 fast risk gates and compute final gated score.

    Args:
        snap: MarketSnapshot with current price action data
        base_score: Slow-variable base score (default 75 from lineage cap)

    Returns:
        FastRiskResult with all gate evaluations and final action
    """
    result = FastRiskResult()

    # ── Evaluate individual gates ──
    r3 = _check_r3_cost_line_break(snap)
    r4 = _check_r4_d1_support_break(snap)
    r5 = _check_r5_cycle_origin_break(snap)

    gates_triggered = {
        "R1_VOLUME_CLIMAX": _check_r1_volume_climax(snap),
        "R2_LONG_UPPER_SHADOW": _check_r2_long_upper_shadow(snap),
        "R3_COST_LINE_BREAK": r3,
        "R4_D1_SUPPORT_BREAK": r4,
        "R5_CYCLE_ORIGIN_BREAK": r5,
        "R6_MULTI_SUPPORT_BREAK": _check_r6_multi_support_break(r3, r4, r5),
        "R7_EVENT_RISK_WINDOW": _check_r7_event_risk_window(snap),
        "R8_SECTOR_ROTATION_FADE": _check_r8_sector_rotation_fade(snap),
        "R9_MARKET_STYLE_HEADWIND": _check_r9_market_style_headwind(snap),
        "R10_CATALYST_DECAY_EXPIRED": _check_r10_catalyst_decay_expired(snap),
    }

    # ── Collect triggered gates ──
    triggered = [gid for gid, fired in gates_triggered.items() if fired]
    result.triggered_gates = triggered
    result.gate_details = gates_triggered

    if not triggered:
        result.final_score = base_score
        result.recommended_action = _score_to_action(base_score, paper_track_allowed=True)
        return result

    # ── Calculate penalties with compound dedup ──
    r6_triggered = "R6_MULTI_SUPPORT_BREAK" in triggered
    total_penalty = 0
    for gid in triggered:
        if r6_triggered and gid in ("R3_COST_LINE_BREAK", "R4_D1_SUPPORT_BREAK", "R5_CYCLE_ORIGIN_BREAK"):
            # R6 replaces individual R3/R4/R5 penalties
            continue
        total_penalty += GATE_DEFINITIONS[gid]["penalty"]

    result.total_penalty = total_penalty

    # ── Determine severity counts ──
    severities = [GATE_DEFINITIONS[gid]["severity"] for gid in triggered]
    result.critical_count = severities.count("CRITICAL")
    result.high_count = severities.count("HIGH")
    result.max_severity = max(severities, key=lambda s: SEVERITY_ORDER.get(s, 0))

    # ── Apply compound action gate rules ──
    paper_track_allowed = True
    score_cap = 100
    action_gate_reason = ""

    # Rule: ANY CRITICAL
    if result.critical_count > 0:
        paper_track_allowed = False
        score_cap = min(score_cap, 40)
        action_gate_reason = "CRITICAL_GATE_TRIGGERED"

    # Rule: TWO OR MORE HIGH
    if result.high_count >= 2:
        paper_track_allowed = False
        score_cap = min(score_cap, 55)
        if not action_gate_reason:
            action_gate_reason = "MULTIPLE_HIGH_GATES"

    # Rule: Volume + Shadow combo
    if "R1_VOLUME_CLIMAX" in triggered and "R2_LONG_UPPER_SHADOW" in triggered:
        paper_track_allowed = False
        score_cap = min(score_cap, 50)
        if not action_gate_reason:
            action_gate_reason = "VOLUME_SHADOW_COMBO"

    # Rule: Cost line + support combo
    if "R3_COST_LINE_BREAK" in triggered and (
        "R4_D1_SUPPORT_BREAK" in triggered or "R5_CYCLE_ORIGIN_BREAK" in triggered
    ):
        paper_track_allowed = False
        score_cap = min(score_cap, 40)
        if not action_gate_reason:
            action_gate_reason = "COST_SUPPORT_COMBO"

    # Rule: Cost line break alone blocks PAPER_TRACK (floating loss = no adding)
    if "R3_COST_LINE_BREAK" in triggered:
        paper_track_allowed = False
        score_cap = min(score_cap, 65)
        if not action_gate_reason:
            action_gate_reason = "COST_LINE_BREAK_FLOATING_LOSS"

    # Rule: Event window blocks PAPER_TRACK upgrade
    if "R7_EVENT_RISK_WINDOW" in triggered:
        paper_track_allowed = False
        score_cap = min(score_cap, 70)
        if not action_gate_reason:
            action_gate_reason = "EVENT_WINDOW_BLOCK"

    # ── Compute final score ──
    raw_score = base_score + total_penalty
    final_score = max(0, min(raw_score, score_cap))

    result.paper_track_allowed = paper_track_allowed
    result.final_score_cap = score_cap
    result.final_score = final_score
    result.action_gate_reason = action_gate_reason
    result.recommended_action = _score_to_action(final_score, paper_track_allowed)

    return result


def _score_to_action(score: int, paper_track_allowed: bool) -> str:
    """Map final score to action, respecting paper_track_allowed veto."""
    if score >= 75:
        if paper_track_allowed:
            return "PAPER_TRACK"
        else:
            return "CONDITIONAL_TRACK"
    elif score >= 60:
        return "CONDITIONAL_TRACK"
    elif score >= 45:
        return "WAIT"
    elif score >= 30:
        return "REDUCE_OR_WAIT"
    else:
        return "AVOID"
