"""Strategy Contracts v1.0 — safety invariants for strategy layer.

No alpha, no promotion, no execution, no broker, no real trade.
"""
STRATEGY_SAFETY_CONTRACT = {
    "formal_alpha": 0,
    "alpha_claim_allowed": False,
    "promotion_allowed": False,
    "candidate_state_update_allowed": False,
    "runner_enabled": False,
    "execution_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED",
}

FORBIDDEN_ACTIONS = ["BUY", "SELL", "ADD", "AUTO_TRADE", "MARKET_ORDER", "PAPER_PROBE"]

def assert_strategy_safety():
    """Verify strategy layer safety invariants. Raises AssertionError on violation."""
    assert STRATEGY_SAFETY_CONTRACT["formal_alpha"] == 0, "formal_alpha must be 0"
    assert STRATEGY_SAFETY_CONTRACT["alpha_claim_allowed"] is False
    assert STRATEGY_SAFETY_CONTRACT["promotion_allowed"] is False
    assert STRATEGY_SAFETY_CONTRACT["candidate_state_update_allowed"] is False
    assert STRATEGY_SAFETY_CONTRACT["runner_enabled"] is False
    assert STRATEGY_SAFETY_CONTRACT["execution_allowed"] is False
    assert STRATEGY_SAFETY_CONTRACT["production"] == "BLOCKED"
    assert STRATEGY_SAFETY_CONTRACT["broker_runtime"] == "BLOCKED"
    assert STRATEGY_SAFETY_CONTRACT["real_trade"] == "BLOCKED"
    for action in FORBIDDEN_ACTIONS:
        assert action not in ["PAPER_TRACK", "CONDITIONAL_TRACK", "WAIT", "WATCH"], \
            f"Forbidden action {action} must not appear in allowed actions"
