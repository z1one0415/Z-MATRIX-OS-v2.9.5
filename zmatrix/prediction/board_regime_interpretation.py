"""Board/Regime interpretation layer for G18 outputs.

Does NOT modify action contracts. Only adds board/regime context to interpretation.
"""
INTERPRETATIONS = {
    ("MAINBOARD", "REVERSAL", "PAPER_TRACK"): ("WATCH_FOR_PULLBACK_OR_CONFIRMATION", True, False),
    ("MAINBOARD", "TRANSITION", "PAPER_TRACK"): ("CONFIRM_BEFORE_TRACKING", True, False),
    ("STAR", "MOMENTUM", "PAPER_TRACK"): ("TREND_CANDIDATE_OBSERVATION", True, True),
    ("STAR", "TRANSITION", "PAPER_TRACK"): ("CONFIRMED_TREND_CANDIDATE", True, True),
    ("CHINEXT", "MOMENTUM", "PAPER_TRACK"): ("TREND_CANDIDATE_OBSERVATION", True, True),
    ("CHINEXT", "TRANSITION", "PAPER_TRACK"): ("CONFIRMED_TREND_CANDIDATE", True, True),
}

def interpret_g18_action_with_board_regime(raw_action: str, probability: float, board_context: dict) -> dict:
    board = board_context.get("board_type", "UNKNOWN")
    regime = board_context.get("regime_state", "UNKNOWN")
    key = (board, regime, raw_action)
    interpreted, not_chase, b_matrix_possible = (
        "RAW_ACTION_LABEL", True, False)
    for (b, r, a), (interp, nc, bm) in INTERPRETATIONS.items():
        if b == board and r == regime and a == raw_action:
            interpreted, not_chase, b_matrix_possible = interp, nc, bm
            break
    return {
        "raw_action_label": raw_action,
        "interpreted_as": interpreted,
        "not_trade_signal": True,
        "not_alpha_claim": True,
        "not_chase_signal": not_chase,
        "b_matrix_candidate_possible": b_matrix_possible,
        "requires_forward_oos_confirmation": True,
    }
