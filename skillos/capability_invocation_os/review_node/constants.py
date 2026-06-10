"""Z9 Review Node constants — DISABLED_DEFAULT_P0."""

MODE = "DISABLED_DEFAULT_P0"

ALLOWED_REVIEW_LABELS = frozenset({
    "EXPLANATION_ACCEPTED_STRUCTURE_ONLY",
    "EXPLANATION_DEGRADED_EVIDENCE_GAP",
    "EXPLANATION_BLOCKED_OUTPUT_RISK",
    "EXPLANATION_CONFIDENCE_MISMATCH",
    "EXPLANATION_REQUIRES_FUTURE_VALIDATION",
    "EXPLANATION_REJECTED_UNSAFE_SOURCE",
})

FORBIDDEN_INPUT_KEYS = frozenset({
    "trade_result",
    "paper_trade_result",
    "broker_result",
    "real_pnl",
    "position_change",
    "automatic_rebalance",
    "execution_feedback",
    "z8_execution_output",
    "v3_sandbox_output",
    "z9_persistent_memory_runtime",
    "production_payload",
    "broker_payload",
})

FORBIDDEN_OUTPUT_KEYS = frozenset({
    "trade_instruction",
    "buy_signal",
    "sell_signal",
    "position_weight",
    "order_signal",
    "automatic_rebalance",
    "broker_action",
    "paper_trade_order",
    "real_trade_order",
    "real_pnl",
    "performance_claim",
    "alpha_claim",
    "expected_return_claim",
    "production_decision",
    "memory_mutation_result",
    "persistent_memory_write",
    "trade_result",
    "paper_trade_result",
    "broker_result",
    "position_change",
    "execution_feedback",
})

ALLOWED_REVIEW_SECTIONS = frozenset({
    "review_header",
    "source_z2_report_snapshot",
    "evidence_chain_review",
    "confidence_alignment_review",
    "missing_evidence_review",
    "degradation_review",
    "blocked_output_review",
    "explanation_quality_review",
    "risk_warning_review",
    "next_validation_review",
    "z2_feedback_candidate",
    "closeout_section",
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
    "write_memory",
    "persist_memory",
    "trigger_z8",
    "trigger_broker",
})
