"""Constants for Factor Library Read-Only Adapter. All disabled-default."""

ALLOWED_READONLY_METHODS = frozenset({
    "list_factors", "get_factor_profile", "get_factor_evidence",
    "monitor_candidates", "build_research_context",
})

FORBIDDEN_METHOD_NAMES = frozenset({
    "execute", "run", "call", "invoke", "trade", "optimize",
    "backtest_live", "generate_alpha", "generate_signal",
    "build_portfolio", "place_order",
})

CANONICAL_READONLY_INTENTS = frozenset({
    "REGISTRY_READ", "EVIDENCE_READ", "VALIDATION_SUMMARY",
    "GUARDRAIL_SUMMARY", "CANDIDATE_MONITOR", "RESEARCH_CONTEXT",
    "SCORING_CONTEXT_DRY_PLAN", "COMPOSITION_GRAPH_DRY_PLAN",
})

FORBIDDEN_INTENTS = frozenset({
    "ALPHA_SIGNAL", "ORDER_SIGNAL", "PORTFOLIO_WEIGHT",
    "PAPER_TRADING", "BROKER_RUNTIME", "REAL_TRADE", "PRODUCTION",
})

BLOCKED_OUTPUTS = frozenset({
    "buy_signal", "sell_signal", "position_weight",
    "expected_return_claim", "alpha_claim", "order_signal",
    "broker_runtime", "real_trade", "production",
})
