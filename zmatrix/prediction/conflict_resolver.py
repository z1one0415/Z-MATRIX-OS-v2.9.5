"""G18 Conflict Resolver v1.0 — identify and downgrade upstream evidence conflicts.

Rules:
  1. G09 sell vs G18 paper entry → HIGH, WAIT
  2. G09 hard_blocks → HIGH, WAIT
  3. G08 narrative decay/bubble → MEDIUM, WATCH
  4. G11 warning only → LOW/MEDIUM, never direct WAIT
  5. Z16/G17 unconfirmed for paper action → MEDIUM, pending confirmation

Conflict resolver can only DOWNGRADE, never upgrade actions.
"""
from __future__ import annotations


def resolve_upstream_conflicts(upstream_evidence: dict, prediction=None) -> dict:
    up = upstream_evidence or {}
    g09 = up.get("g09", {})
    g08 = up.get("g08", {})
    g11 = up.get("g11", {})
    z16 = up.get("z16", {})
    g17 = up.get("g17", {})

    conflicts = []
    current_action = prediction.action_proposal if prediction else "WAIT"
    final_cap = current_action

    # ── Rule 1: G09 sell vs G18 paper entry ──
    sell = g09.get("sell_decision", {})
    pos_action = g09.get("position_action") or sell.get("position_action", "")
    sell_actions = ("REDUCE_CORE", "MAJOR_REDUCE_OR_EXIT", "SELL_TRADING_KEEP_CORE", "LIGHTEN_TRADING")
    if pos_action in sell_actions and current_action in ("PAPER_TRACK", "PAPER_PROBE_ELIGIBLE", "PAPER_PROBE_ELIGIBLE_PENDING_Z16_Z17"):
        conflicts.append({
            "code": "G09_SELL_VS_G18_ENTRY", "level": "HIGH",
            "description": f"G09 recommends {pos_action} but G18 action is {current_action}",
            "suggested_action_cap": "WAIT",
            "source_pair": ["g09", "g18"],
        })
        final_cap = "WAIT"

    # ── Rule 2: G09 hard_blocks ──
    if g09.get("hard_blocks"):
        conflicts.append({
            "code": "G09_HARD_BLOCKS_ACTIVE", "level": "HIGH",
            "description": f"G09 hard_blocks: {g09['hard_blocks']}",
            "suggested_action_cap": "WAIT",
            "source_pair": ["g09"],
        })
        final_cap = "WAIT"

    # ── Rule 3: G08 narrative decay/bubble ──
    if g08.get("available"):
        decay = g08.get("narrative_decay", 0)
        bubble = g08.get("bubble_temperature", 0)
        if decay >= 0.7 or bubble >= 0.8:
            cap = "WATCH"
            conflicts.append({
                "code": "G08_NARRATIVE_DECAY_OR_BUBBLE", "level": "MEDIUM",
                "description": f"narrative_decay={decay} bubble={bubble}",
                "suggested_action_cap": cap,
                "source_pair": ["g08"],
            })
            final_cap = _lower_cap(final_cap, cap)

    # ── Rule 4: G11 warning only ──
    if g11.get("warnings"):
        if g11.get("hard_veto_allowed") is not True:
            cap = "WATCH"
            conflicts.append({
                "code": "G11_WARNING_ONLY", "level": "LOW" if len(g11["warnings"]) <= 2 else "MEDIUM",
                "description": f"G11 warnings: {g11['warnings'][:3]}",
                "suggested_action_cap": cap,
                "source_pair": ["g11"],
            })
            final_cap = _lower_cap(final_cap, cap)

    # ── Rule 5: Z16/G17 unconfirmed for paper ──
    if current_action in ("PAPER_TRACK", "PAPER_PROBE_ELIGIBLE", "PAPER_PROBE_ELIGIBLE_PENDING_Z16_Z17", "WATCH"):
        z16_ok = z16.get("available") is True
        g17_ok = g17.get("available") is True
        if not z16_ok or not g17_ok:
            cap = "PAPER_PROBE_ELIGIBLE_PENDING_Z16_Z17"
            missing = [s for s, ok in [("z16", z16_ok), ("g17", g17_ok)] if not ok]
            conflicts.append({
                "code": "Z16_G17_CONFIRMATION_MISSING", "level": "MEDIUM",
                "description": f"Confirmations missing: {missing}",
                "suggested_action_cap": cap,
                "source_pair": ["z16", "g17"],
            })
            final_cap = _lower_cap(final_cap, cap)

    has_conflict = len(conflicts) > 0
    levels = [c["level"] for c in conflicts]
    if "HIGH" in levels: conflict_level = "HIGH"
    elif "MEDIUM" in levels: conflict_level = "MEDIUM"
    elif "LOW" in levels: conflict_level = "LOW"
    else: conflict_level = "NONE"

    return {
        "conflict_version": "v1.0",
        "has_conflict": has_conflict,
        "conflict_level": conflict_level,
        "conflicts": conflicts,
        "suggested_action_cap": final_cap,
        "warnings": [c["description"] for c in conflicts],
    }


def _lower_cap(current, proposed):
    """Return the more conservative action cap."""
    order = ["PAPER_PROBE_ELIGIBLE_PENDING_Z16_Z17", "PAPER_PROBE_ELIGIBLE", "PAPER_TRACK", "WATCH", "WAIT"]
    for action in order:
        if current == action or proposed == action:
            return action
    return current
