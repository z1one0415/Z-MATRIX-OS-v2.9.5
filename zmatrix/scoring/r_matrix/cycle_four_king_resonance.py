"""R-Matrix v2.0 四天王共振裁决器 — Cycle Four-King Resonance

长周期定方向, 中周期定结构, 短周期定位置, 冲动定警报.
"""
from __future__ import annotations

# Action priority (lower = more conservative)
ACTION_RANK = {"AVOID": 0, "WAIT": 1, "WATCH_ENTRY": 2, "HOLD": 3, "RIDE": 4}

# Exit alert priority
EXIT_ALERT_RANK = {"NONE": 0, "WATCH_HARVEST": 1, "HARVEST": 2, "FORCE_HARVEST": 3}


def evaluate_cycle_four_king(impulse: dict | None, oscillation: dict | None,
                              rhythm: dict | None, rotation: dict | None) -> dict:
    """四王共振裁决 — 按长周期定性, 中短周期调节动作上限."""
    hard_blocks: list[str] = []
    conflicts: list[str] = []
    
    # ── 长周期硬否决 ──
    if rotation and rotation.get("type") == "TREND_DOWN":
        hard_blocks.append("ROTATION_TREND_DOWN")
    if rhythm and rhythm.get("type") == "TREND_DOWN":
        hard_blocks.append("RHYTHM_TREND_DOWN")
    
    if hard_blocks:
        return _blocked_result(hard_blocks, impulse, oscillation, rhythm, rotation)
    
    # ── 短周期不硬否决, 只调节 ──
    exit_alert = "NONE"
    if impulse and impulse.get("action") == "HARVEST":
        exit_alert = "WATCH_HARVEST"
    if oscillation and oscillation.get("action") == "HARVEST":
        exit_alert = "HARVEST"
    if rhythm and rhythm.get("action") == "HARVEST" and rhythm.get("position", 0) > 0.85:
        exit_alert = "FORCE_HARVEST"
    
    if oscillation and oscillation.get("type") == "TREND_DOWN":
        conflicts.append("OSCILLATION_TREND_DOWN")
    if impulse and impulse.get("action") == "HARVEST" and oscillation and oscillation.get("position", 0.5) > 0.6:
        conflicts.append("SHORT_TERM_OVERHEAT_LONG_OK")
    
    # ── 方向判断 ──
    has_long_up = (rotation and rotation.get("type") == "TREND_UP") or \
                  (rhythm and rhythm.get("type") == "TREND_UP")
    has_mid_box = rhythm and rhythm.get("type") == "BOX"
    has_short_low = oscillation and oscillation.get("position", 1) < 0.35
    has_short_high = oscillation and oscillation.get("position", 0) > 0.75
    
    # ── 共振状态 ──
    if has_long_up and has_mid_box and has_short_low:
        resonance_status = "CYCLE_RESONANCE_STRONG"
        entry_cap = "RIDE"
        resonance_score = 9.0
    elif (has_long_up or has_mid_box) and has_short_low:
        resonance_status = "CYCLE_RESONANCE_ENTRY"
        entry_cap = "WATCH_ENTRY"
        resonance_score = 7.0
    elif has_long_up and not has_short_high:
        resonance_status = "CYCLE_RESONANCE_RIDE"
        entry_cap = "RIDE" if has_short_low else "HOLD"
        resonance_score = 6.0 if has_short_low else 5.0
    elif has_mid_box and not has_short_high:
        resonance_status = "CYCLE_RESONANCE_BOX"
        entry_cap = "WATCH_ENTRY" if has_short_low else "WAIT"
        resonance_score = 5.0 if has_short_low else 3.0
    elif conflicts:
        resonance_status = "CYCLE_CONFLICT"
        entry_cap = "WAIT"
        resonance_score = 2.0
    else:
        resonance_status = "CYCLE_MIXED"
        entry_cap = "WAIT"
        resonance_score = 1.0
    
    # Exit alert overrides entry cap
    if exit_alert in ("FORCE_HARVEST", "HARVEST"):
        entry_cap = "WAIT"
    
    return {
        "resonance_status": resonance_status,
        "resonance_score": round(resonance_score, 1),
        "entry_action_cap": entry_cap,
        "exit_alert": exit_alert,
        "hard_blocks": hard_blocks,
        "conflicts": conflicts,
        "kings": {
            "impulse": impulse,
            "oscillation": oscillation,
            "rhythm": rhythm,
            "rotation": rotation,
        },
    }


def _blocked_result(hard_blocks, impulse, oscillation, rhythm, rotation) -> dict:
    return {
        "resonance_status": "CYCLE_BLOCKED",
        "resonance_score": 0.0,
        "entry_action_cap": "AVOID",
        "exit_alert": "NONE",
        "hard_blocks": hard_blocks,
        "conflicts": [],
        "kings": {
            "impulse": impulse,
            "oscillation": oscillation,
            "rhythm": rhythm,
            "rotation": rotation,
        },
    }
