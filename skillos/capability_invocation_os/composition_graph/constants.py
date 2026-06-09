"""Composition Graph Factor Bridge constants — DISABLED_DEFAULT_P0."""

GRAPH_MODE = "DISABLED_DEFAULT_P0"

ALLOWED_NODE_TYPES: frozenset[str] = frozenset({
    "static_input_node",
    "capability_registry_node",
    "a1_factor_bridge_response_node",
    "a1_factor_bridge_denied_context_node",
    "factor_evidence_summary_node",
    "local_report_reading_node",
    "document_generation_in_memory_node",
    "composition_summary_node",
})

BLOCKED_NODE_TYPES: frozenset[str] = frozenset({
    "factor_library_direct_node",
    "real_factor_node",
    "z2_runtime_node",
    "z8_execution_node",
    "z9_memory_mutation_node",
    "v3_sandbox_node",
    "broker_node",
    "real_trade_node",
    "alpha_signal_node",
    "paper_trading_node",
    "portfolio_weight_node",
    "order_signal_node",
    "production_node",
})

ALLOWED_EDGE_TYPES: frozenset[str] = frozenset({
    "readonly_context_edge",
    "evidence_hash_edge",
    "permission_tier_edge",
    "degradation_edge",
    "denied_context_edge",
    "blocked_output_filter_edge",
    "c1_handoff_edge",
    "a1_bridge_source_edge",
})

BLOCKED_EDGE_TYPES: frozenset[str] = frozenset({
    "execution_edge",
    "trade_edge",
    "broker_edge",
    "real_time_feedback_edge",
    "autonomous_retry_edge",
    "mutation_edge",
    "production_edge",
    "alpha_signal_edge",
})

FORBIDDEN_GRAPH_OUTPUTS: frozenset[str] = frozenset({
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
