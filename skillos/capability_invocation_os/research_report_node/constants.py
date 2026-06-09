"""Research Report Node constants — DISABLED_DEFAULT_P0."""

REPORT_NODE_MODE = "DISABLED_DEFAULT_P0"

ALLOWED_INPUT_TYPES = frozenset({"B1 CompositionGraphResponse"})

ALLOWED_REPORT_SECTIONS = frozenset({
    "report_header",
    "source_graph_summary",
    "factor_context_summary",
    "evidence_chain_summary",
    "structural_readiness_summary",
    "research_interpretation",
    "risk_warning",
    "missing_evidence",
    "blocked_outputs_removed",
    "confidence_section",
    "z9_review_snapshot_candidate",
    "next_validation_requirement",
})

ALLOWED_CONFIDENCE_LEVELS = frozenset({
    "LOW",
    "MEDIUM",
    "HIGH_WITH_STRUCTURE_ONLY",
})

FORBIDDEN_REPORT_OUTPUTS = frozenset({
    "alpha_claim",
    "expected_return_claim",
    "buy_signal",
    "sell_signal",
    "position_weight",
    "order_signal",
    "trade_instruction",
    "paper_trade_order",
    "broker_action",
    "portfolio_rebalance",
    "real_trade_order",
    "production_decision",
    "real_pnl",
    "trade_result",
})

ALLOWED_DECISIONS = frozenset({
    "ALLOW_Z2_READONLY_REPORT",
    "ALLOW_Z2_DEGRADED_REPORT",
    "DENY_Z2_SOURCE_FORBIDDEN",
    "DENY_Z2_REAL_SOURCE_FORBIDDEN",
    "DENY_Z2_OUTPUTS_UNSAFE",
    "DENY_Z2_GRAPH_DENIED",
    "DENY_Z2_EVIDENCE_INCOMPLETE",
    "DENY_Z2_EXECUTION_FORBIDDEN",
    "DISABLED_DEFAULT_NOOP",
})

FORBIDDEN_METHOD_NAMES = frozenset({
    "execute",
    "run",
    "call",
    "invoke",
    "trade",
    "optimize",
    "backtest_live",
    "generate_alpha",
    "generate_signal",
    "build_portfolio",
    "place_order",
    "rebalance",
    "mutate_memory",
})
