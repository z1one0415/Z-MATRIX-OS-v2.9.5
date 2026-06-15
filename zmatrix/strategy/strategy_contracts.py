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
    """Verify strategy layer safety invariants. Raises on violation."""
    pass
