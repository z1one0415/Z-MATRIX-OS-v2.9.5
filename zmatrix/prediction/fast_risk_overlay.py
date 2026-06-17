"""G18 Fast Risk Overlay v2.0 — context-aware risk gates.

v2.0 changes:
- R3 split: planned entry cost line only (existing holding → R11)
- R7 split: R7a_BLACKSWAN / R7b_SCHEDULED_MACRO / R7c_EVENT_DAY
- R6 fix: market structure only (R4+R5), excludes personal cost line
- R11 added: POSITION_OVERSOLD_REVIEW (flag only, no penalty, no BUY/ADD)

Core principle: slow variables provide base_score; fast risk gates own action veto.
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
    "R3_ENTRY_COST_LINE_BREAK": {"severity": "HIGH", "penalty": -15},
    "R4_D1_SUPPORT_BREAK": {"severity": "HIGH", "penalty": -15},
    "R5_CYCLE_ORIGIN_BREAK": {"severity": "HIGH", "penalty": -20},
    "R6_MULTI_MARKET_STRUCTURE_BREAK": {"severity": "CRITICAL", "penalty": -35},
    "R7a_BLACKSWAN_EVENT": {"severity": "CRITICAL", "penalty": -10},
    "R7b_SCHEDULED_MACRO_EVENT": {"severity": "MEDIUM", "penalty": -5},
    "R7c_SCHEDULED_EVENT_DAY": {"severity": "LOW", "penalty": 0},
    "R8_SECTOR_ROTATION_FADE": {"severity": "MEDIUM", "penalty": -15},
    "R9_MARKET_STYLE_HEADWIND": {"severity": "MEDIUM", "penalty": -10},
    "R10_CATALYST_DECAY_EXPIRED": {"severity": "MEDIUM", "penalty": -10},
}

SEVERITY_ORDER = {"CRITICAL": 3, "HIGH": 2, "MEDIUM": 1, "LOW": 0, "NONE": 0}


# ═══════════════════════════════════════════════════════
# Market Snapshot (v2.0 — context-aware)
# ═══════════════════════════════════════════════════════

@dataclass
class MarketSnapshot:
    """Input data for fast risk evaluation."""
    # ── price fields (original) ──
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
    close_series: list | None = None  # v2.1: historical closes for regime detection

    # ── position fields (v2.0) ──
    position_state: str = "NO_POSITION"     # NO_POSITION / HOLDING / WATCHING
    shares: float = 0.0
    planned_entry_price: float | None = None
    avg_holding_cost: float | None = None
    cost_line_source: str = "none"           # planned_entry / avg_holding_cost / none
    oversold_zscore: float | None = None
    ma60_deviation_pct: float | None = None
    fundamental_deteriorated: bool = False
    catalyst_active: bool = False
    close_series: list | None = None

    # ── event fields (v2.0) ──
    event_type: str | None = None
    event_risk_severity: str | None = None   # scheduled / blackswans / none
    event_phase: str | None = None           # pre_2d / pre_1d / event_day / post_48h / none
    event_expected: bool = False
    event_confirmation_received: bool = False


# ═══════════════════════════════════════════════════════
# Gate Evaluation Functions
# ═══════════════════════════════════════════════════════

def _check_r1_volume_climax(snap: MarketSnapshot) -> bool:
    if snap.volume is None or snap.avg_volume_20d is None: return False
    if snap.avg_volume_20d <= 0: return False
    return snap.volume >= 2.0 * snap.avg_volume_20d

def _check_r2_long_upper_shadow(snap: MarketSnapshot) -> bool:
    if snap.high is None or snap.close is None: return False
    if snap.high <= 0: return False
    return (snap.high - snap.close) / snap.high >= 0.03


def _check_r3_entry_cost_line_break(snap: MarketSnapshot) -> bool:
    """R3_ENTRY_COST_LINE_BREAK v2.0:
    Only triggers for planned entry, NOT for existing holding positions.
    """
    if snap.position_state != "NO_POSITION":
        return False
    if snap.cost_line_source not in ("planned_entry",):
        return False
    if snap.close is None or snap.planned_entry_price is None:
        return False
    return snap.close < snap.planned_entry_price


def _check_r4_d1_support_break(snap: MarketSnapshot) -> bool:
    if snap.close is None or snap.d1_support is None: return False
    return snap.close < snap.d1_support

def _check_r5_cycle_origin_break(snap: MarketSnapshot) -> bool:
    if snap.close is None or snap.cycle_origin is None: return False
    return snap.close < snap.cycle_origin


def _check_r6_multi_market_structure_break(r4: bool, r5: bool) -> bool:
    """R6_MULTI_MARKET_STRUCTURE_BREAK v2.0:
    R4 + R5 only. R3 (personal cost line) excluded from market structure count.
    """
    return sum([r4, r5]) >= 2


def _check_r7a_blackswan_event(snap: MarketSnapshot) -> bool:
    """R7a: Blackswan event (war, sanctions, default, trading halt, policy shock)."""
    return (snap.event_risk_severity == "blackswans"
            and snap.event_window_active
            and not snap.event_confirmation_received)


def _check_r7b_scheduled_macro_event(snap: MarketSnapshot) -> bool:
    """R7b: Scheduled macro event (FOMC, CPI, NFP, PMI, central bank).
    Only triggers in pre-event phase (pre_2d, pre_1d)."""
    return (snap.event_risk_severity == "scheduled"
            and snap.event_window_active
            and snap.event_phase in ("pre_2d", "pre_1d"))


def _check_r7c_scheduled_event_day(snap: MarketSnapshot) -> bool:
    """R7c: Event day — no new entry interpretation, existing holding review allowed."""
    return (snap.event_risk_severity == "scheduled"
            and snap.event_window_active
            and snap.event_phase == "event_day")


def _check_r8_sector_rotation_fade(snap: MarketSnapshot) -> bool:
    if snap.sector_momentum_rank_current is None or snap.sector_momentum_rank_prior is None: return False
    return snap.sector_momentum_rank_current - snap.sector_momentum_rank_prior >= 5

def _check_r9_market_style_headwind(snap: MarketSnapshot) -> bool:
    return snap.style_mismatch_duration_days >= 5

def _check_r10_catalyst_decay_expired(snap: MarketSnapshot) -> bool:
    if snap.days_since_catalyst is None: return False
    return (snap.days_since_catalyst > snap.catalyst_decay_threshold and not snap.catalyst_refreshed)


def _check_r11_position_oversold_review(snap: MarketSnapshot) -> bool:
    """R11_POSITION_OVERSOLD_REVIEW v2.0:
    Existing holding + extreme floating loss + technical oversold + fundamentals intact.
    Outputs position_management FLAG only. Does NOT trigger BUY/ADD/penalty.
    """
    if snap.position_state != "HOLDING":
        return False
    if snap.shares <= 0 or snap.avg_holding_cost is None or snap.close is None:
        return False
    if snap.avg_holding_cost <= 0:
        return False
    floating_loss_pct = snap.close / snap.avg_holding_cost - 1
    ma60_drop = snap.ma60_deviation_pct or 0
    return (
        floating_loss_pct <= -0.15
        and ma60_drop <= -12
        and not snap.fundamental_deteriorated
    )


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
    position_management_flags: list = field(default_factory=list)


def evaluate_fast_risk_overlay(
    snap: MarketSnapshot,
    base_score: int = 75,
) -> FastRiskResult:
    """Evaluate fast risk gates and compute final gated score.

    v2.0: Context-aware — separates new entry risk from existing holding risk.
    """
    result = FastRiskResult()

    # ── Individual gates ──
    r3 = _check_r3_entry_cost_line_break(snap)
    r4 = _check_r4_d1_support_break(snap)
    r5 = _check_r5_cycle_origin_break(snap)

    gates_triggered = {
        "R1_VOLUME_CLIMAX": _check_r1_volume_climax(snap),
        "R2_LONG_UPPER_SHADOW": _check_r2_long_upper_shadow(snap),
        "R3_ENTRY_COST_LINE_BREAK": r3,
        "R4_D1_SUPPORT_BREAK": r4,
        "R5_CYCLE_ORIGIN_BREAK": r5,
        "R6_MULTI_MARKET_STRUCTURE_BREAK": _check_r6_multi_market_structure_break(r4, r5),
        "R7a_BLACKSWAN_EVENT": _check_r7a_blackswan_event(snap),
        "R7b_SCHEDULED_MACRO_EVENT": _check_r7b_scheduled_macro_event(snap),
        "R7c_SCHEDULED_EVENT_DAY": _check_r7c_scheduled_event_day(snap),
        "R8_SECTOR_ROTATION_FADE": _check_r8_sector_rotation_fade(snap),
        "R9_MARKET_STYLE_HEADWIND": _check_r9_market_style_headwind(snap),
        "R10_CATALYST_DECAY_EXPIRED": _check_r10_catalyst_decay_expired(snap),
    }

    # ── R11: position management flag (not a penalty gate) ──
    r11 = _check_r11_position_oversold_review(snap)
    if r11:
        result.position_management_flags.append({
            "gate": "R11_POSITION_OVERSOLD_REVIEW",
            "status": "OVERSOLD_REVIEW_ELIGIBLE",
            "not_new_entry_signal": True,
            "not_auto_add_signal": True,
            "forbidden_actions": ["BUY", "ADD", "AUTO_TRADE", "MARKET_ORDER"],
        })

    triggered = [gid for gid, fired in gates_triggered.items() if fired]
    result.triggered_gates = triggered
    result.gate_details = gates_triggered

    if not triggered:
        result.final_score = base_score
        result.recommended_action = _score_to_action(base_score, paper_track_allowed=True)
        return result

    # ── Calculate penalties with compound dedup ──
    r6_triggered = "R6_MULTI_MARKET_STRUCTURE_BREAK" in triggered
    total_penalty = 0
    for gid in triggered:
        if r6_triggered and gid in ("R4_D1_SUPPORT_BREAK", "R5_CYCLE_ORIGIN_BREAK"):
            continue
        total_penalty += GATE_DEFINITIONS[gid]["penalty"]

    result.total_penalty = total_penalty

    # ── Severity counts ──
    severities = [GATE_DEFINITIONS[gid]["severity"] for gid in triggered]
    result.critical_count = severities.count("CRITICAL")
    result.high_count = severities.count("HIGH")
    result.max_severity = max(severities, key=lambda s: SEVERITY_ORDER.get(s, 0))

    # ── Action gate rules ──
    paper_track_allowed = True
    score_cap = 100
    action_gate_reason = ""

    # CRITICAL gates (R6, R7a) → hard veto
    if result.critical_count > 0:
        paper_track_allowed = False
        score_cap = min(score_cap, 40)
        action_gate_reason = "CRITICAL_GATE_TRIGGERED"

    # TWO OR MORE HIGH
    if result.high_count >= 2:
        paper_track_allowed = False
        score_cap = min(score_cap, 55)
        if not action_gate_reason:
            action_gate_reason = "MULTIPLE_HIGH_GATES"

    # Volume + Shadow combo
    if "R1_VOLUME_CLIMAX" in triggered and "R2_LONG_UPPER_SHADOW" in triggered:
        paper_track_allowed = False
        score_cap = min(score_cap, 50)
        if not action_gate_reason:
            action_gate_reason = "VOLUME_SHADOW_COMBO"

    # Entry cost + support combo
    if "R3_ENTRY_COST_LINE_BREAK" in triggered and (
        "R4_D1_SUPPORT_BREAK" in triggered or "R5_CYCLE_ORIGIN_BREAK" in triggered
    ):
        paper_track_allowed = False
        score_cap = min(score_cap, 40)
        if not action_gate_reason:
            action_gate_reason = "COST_SUPPORT_COMBO"

    # Entry cost line break alone — no paper entry when planned price broken
    if "R3_ENTRY_COST_LINE_BREAK" in triggered:
        paper_track_allowed = False
        score_cap = min(score_cap, 65)
        if not action_gate_reason:
            action_gate_reason = "ENTRY_COST_LINE_BREAK"

    # Blackswan event — hard veto
    if "R7a_BLACKSWAN_EVENT" in triggered:
        paper_track_allowed = False
        score_cap = min(score_cap, 60)
        if not action_gate_reason:
            action_gate_reason = "BLACKSWAN_EVENT"

    # Scheduled macro event — reduce interpretation strength, no full veto
    if "R7b_SCHEDULED_MACRO_EVENT" in triggered:
        if not action_gate_reason:
            action_gate_reason = "SCHEDULED_MACRO_EVENT_PRE"

    # Event day — no new entry, but allow holding review
    if "R7c_SCHEDULED_EVENT_DAY" in triggered:
        if not action_gate_reason:
            action_gate_reason = "SCHEDULED_EVENT_DAY_NO_NEW_ENTRY"

    # ── Final score ──
    raw_score = base_score + total_penalty
    final_score = max(0, min(raw_score, score_cap))

    result.paper_track_allowed = paper_track_allowed
    result.final_score_cap = score_cap
    result.final_score = final_score
    result.action_gate_reason = action_gate_reason
    result.recommended_action = _score_to_action(final_score, paper_track_allowed)

    return result


def _score_to_action(score: int, paper_track_allowed: bool) -> str:
    if score >= 75:
        return "PAPER_TRACK" if paper_track_allowed else "CONDITIONAL_TRACK"
    elif score >= 60: return "CONDITIONAL_TRACK"
    elif score >= 45: return "WAIT"
    elif score >= 30: return "REDUCE_OR_WAIT"
    else: return "AVOID"
