"""Composition Graph Factor Bridge constants — DISABLED_DEFAULT_P0."""

GRAPH_MODE = "DISABLED_DEFAULT_P0"

ALLOWED_NODE_TYPES: frozenset[str] = frozenset({
    "a1_bridge_response",
    "a1_bridge_denied_context",
    "graph_evidence",
    "graph_source_summary",
    "graph_degradation",
    "graph_readonly_summary",
    "graph_c1_handoff",
    "graph_noop",
})

BLOCKED_NODE_TYPES: frozenset[str] = frozenset({
    "execution_node",
    "alpha_node",
    "signal_node",
    "order_node",
    "portfolio_node",
    "trade_node",
    "broker_node",
    "backtest_live_node",
    "optimizer_node",
    "real_source_node",
    "production_node",
    "runtime_node",
    "mutable_state_node",
})

ALLOWED_EDGE_TYPES: frozenset[str] = frozenset({
    "bridge_to_graph",
    "graph_to_evidence",
    "graph_to_summary",
    "graph_to_degradation",
    "graph_to_c1_handoff",
    "graph_to_noop",
    "denied_to_context",
    "evidence_to_summary",
})

BLOCKED_EDGE_TYPES: frozenset[str] = frozenset({
    "execution_edge",
    "alpha_edge",
    "signal_edge",
    "order_edge",
    "trade_edge",
    "broker_edge",
    "portfolio_edge",
    "mutable_state_edge",
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
