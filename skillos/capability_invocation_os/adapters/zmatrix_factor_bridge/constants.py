BRIDGE_MODE = "DISABLED_DEFAULT_P0"

ALLOWED_BRIDGE_INPUT_SOURCE_CLASSES = frozenset({
    "factor_library_fixture",
    "factor_library_disabled_default",
})

REQUIRED_PASSTHROUGH_FIELDS = frozenset({
    "no_real_source_flag",
    "fixture_source_commit",
    "source_class",
    "forbidden_outputs_removed",
    "decision",
    "permission_tier",
    "request_hash",
    "response_hash_placeholder",
    "decision_hash",
})

FORBIDDEN_BRIDGE_OUTPUTS = frozenset({
    "alpha_claim",
    "expected_return_claim",
    "position_weight",
    "buy_signal",
    "sell_signal",
    "order_signal",
    "broker_runtime",
    "real_trade",
    "production",
})

FORBIDDEN_BRIDGE_METHOD_NAMES = frozenset({
    "execute", "run", "call", "invoke", "trade", "optimize",
    "backtest_live", "generate_alpha", "generate_signal",
    "build_portfolio", "place_order",
})
