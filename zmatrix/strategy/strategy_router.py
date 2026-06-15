"""Strategy Router v1.0 — routes strategy based on board + regime.

Outputs strategy family and interpretation. Never BUY/SELL/ADD.
"""
ROUTES = {
    ("MAINBOARD", "REVERSAL"):  ("REVERSAL_REPAIR", "Rebound candidates under strict size/depth confirmation"),
    ("MAINBOARD", "TRANSITION"): ("PULLBACK_CONFIRMATION", "Monitor for pullback-to-support confirmation"),
    ("MAINBOARD", "MOMENTUM"):  ("CONDITIONAL_MOMENTUM_WITH_STRICT_CONFIRMATION", "Momentum only under multi-timeframe+volume confirmation"),
    ("STAR", "MOMENTUM"):       ("B_MATRIX_MOMENTUM", "Trend candidates may be researched under stricter risk controls"),
    ("STAR", "TRANSITION"):     ("B_MATRIX_WATCH_CONFIRM", "Monitor for confirmed trend before research"),
    ("STAR", "REVERSAL"):       ("HIGH_BETA_PULLBACK_REPAIR", "High-beta pullback repair is risky; confirm support zones first"),
    ("CHINEXT", "MOMENTUM"):    ("B_MATRIX_MOMENTUM", "Trend candidates may be researched under stricter risk controls"),
    ("CHINEXT", "TRANSITION"):  ("CONFIRMED_MOMENTUM_OR_WAIT", "Requires volume/price confirmation before tracking"),
    ("CHINEXT", "REVERSAL"):    ("HIGH_BETA_REVERSAL_REPAIR", "High-beta reversal is risky; confirm support zones first"),
}

def route_strategy(board_type: str, regime_state: str) -> dict:
    key = (board_type, regime_state)
    family, interpretation = ROUTES.get(key, ("DIAGNOSTIC_ONLY", "No strategy match for board/regime combination"))
    return {
        "board_type": board_type,
        "regime_state": regime_state,
        "strategy_family": family,
        "interpretation": interpretation,
        "not_trade_signal": True,
        "requires_forward_oos_confirmation": True,
        "alpha_claim_allowed": False,
        "promotion_allowed": False,
    }
