"""Board Regime Context Builder — assembles board/regime context for G18 output.

Integrates: board_classifier, regime_detector, strategy_router, b_matrix_router, board_regime_interpretation.
"""
from zmatrix.strategy.board_classifier import classify_board
from zmatrix.strategy.regime_detector import detect_reversal_momentum_regime
from zmatrix.strategy.strategy_router import route_strategy
from zmatrix.strategy.b_matrix_router import is_b_matrix_search_allowed
from zmatrix.prediction.board_regime_interpretation import interpret_g18_action_with_board_regime


def build_board_regime_context(
    ticker: str,
    price_series: list | None = None,
    raw_action: str = "WAIT",
    probability: float = 0.0,
) -> dict:
    """Build full board/regime context for a ticker.

    Returns context dict suitable for inclusion in final_decision_envelope.
    """
    # Board classification
    board = classify_board(ticker)
    board_type = board["board_type"]

    # Regime detection (requires price data)
    regime = {"regime_state": "DATA_INSUFFICIENT", "valid_observations": 0}
    if price_series:
        regime = detect_reversal_momentum_regime(price_series)

    regime_state = regime["regime_state"]

    # Strategy routing
    strategy = route_strategy(board_type, regime_state)

    # B-MATRIX search policy
    b_matrix = is_b_matrix_search_allowed(board_type, regime_state)

    # G18 interpretation
    interpretation = interpret_g18_action_with_board_regime(
        raw_action, probability,
        {"board_type": board_type, "regime_state": regime_state}
    )

    return {
        "board_type": board_type,
        "board_confidence": board.get("confidence", "RULE_BASED"),
        "regime_state": regime_state,
        "regime_metrics": {
            "up_day_next_down_probability": regime.get("up_day_next_down_probability"),
            "avg_up_run_length": regime.get("avg_up_run_length"),
            "trend_slope_20d": regime.get("trend_slope_20d"),
            "volatility_20d": regime.get("volatility_20d"),
            "valid_observations": regime.get("valid_observations", 0),
        },
        "strategy_family": strategy["strategy_family"],
        "interpretation": strategy["interpretation"],
        "b_matrix_search_status": b_matrix["b_matrix_search_status"],
        "b_matrix_search_priority": b_matrix["search_priority"],
        "action_interpretation": {
            "raw_action_label": raw_action,
            "interpreted_as": interpretation["interpreted_as"],
            "not_trade_signal": True,
            "not_alpha_claim": True,
            "not_chase_signal": interpretation.get("not_chase_signal", True),
            "b_matrix_candidate_possible": interpretation.get("b_matrix_candidate_possible", False),
            "requires_forward_oos_confirmation": True,
        },
        "alpha_claim_allowed": False,
        "promotion_allowed": False,
    }
