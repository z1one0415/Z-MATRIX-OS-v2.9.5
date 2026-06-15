"""B-MATRIX Router v1.0 — board-aware search policy for B-MATRIX candidates.

Default: research_only. Priority: STAR/CHINEXT + MOMENTUM.
Mainboard + REVERSAL → blocked_by_default.
"""
POLICY = {
    ("STAR", "MOMENTUM"):    ("ALLOWED", "HIGH", "STAR board under MOMENTUM regime"),
    ("STAR", "TRANSITION"):  ("CONDITIONAL", "MEDIUM", "Confirm trend before search"),
    ("CHINEXT", "MOMENTUM"): ("ALLOWED", "HIGH", "CHINEXT board under MOMENTUM regime"),
    ("CHINEXT", "TRANSITION"): ("CONDITIONAL", "MEDIUM", "Confirm trend before search"),
    ("MAINBOARD", "MOMENTUM"): ("CONDITIONAL", "LOW", "Mainboard momentum requires strict confirmation"),
    ("MAINBOARD", "REVERSAL"): ("BLOCKED", None, "Mainboard reversal does not use B-MATRIX search"),
    ("MAINBOARD", "TRANSITION"): ("CONDITIONAL", "LOW", "Wait for confirmed direction"),
}

def is_b_matrix_search_allowed(board_type: str, regime_state: str) -> dict:
    key = (board_type, regime_state)
    status, priority, reason = POLICY.get(key, ("BLOCKED", None, "No policy match — blocked by default"))
    return {
        "b_matrix_search_status": status,
        "search_priority": priority,
        "reason": reason,
        "not_alpha_claim": True,
        "not_trade_signal": True,
        "requires_forward_oos_confirmation": True,
    }
