# Z9 Review Node Implementation Branch Approval Gate
## Status: Z_SKILLOS_Z9_REVIEW_NODE_IMPLEMENTATION_BRANCH_APPROVAL_GATE_READY
## Base HEAD: 9a6b9c4 | Branch: gate/...-approval | Mode: DISABLED_DEFAULT_P0
## Target: impl/skillos-z9-review-node-disabled-default-p0 (if approved)

## Allowed Future Branch
impl/skillos-z9-review-node-disabled-default-p0

## Allowed Future Scope
- review_node package skeleton (12 source files)
- disabled-default config (all enabled→False)
- kill switch (all active→True)
- models (Z9ReviewNodeRequest, Response, Section, Evidence, Decision, Summary, Z2FeedbackCandidate, DegradationStatus)
- contracts (validate Z2 snapshot, review output, section, attribution, feedback, denied review)
- evidence (inherit from Z2 z9_review_snapshot_candidate, generate z9_review_node_hash, section_hash, feedback_hash)
- attribution (explanation attribution only: evidence_gap, confidence_mismatch, degradation_reason, blocked_output_risk, missing_source, structural_readiness, future_validation, z2_report_consistency, z9_feedback_candidate)
- degradation (10 decisions: ALLOW_Z9_READONLY_REVIEW through DISABLED_DEFAULT_NOOP)
- review_builder (facade: Z2 snapshot readonly review)
- z2_feedback (advisory/readonly, requires human review)
- registry (P0 static placeholder)
- proof tests (disabled_default, models, contracts, evidence, attribution, degradation, review_builder, z2_feedback, no_forbidden_imports)

## Future Input Allowed
Z2 z9_review_snapshot_candidate ONLY. 15 specific fields.

## Future Direct Inputs Forbidden
B1 CompositionGraphResponse directly, FactorInvocationResponse, raw factor values, research/factor_library files, real returns, trade_result, paper_trade_result, broker_result, real_pnl, position_change, automatic_rebalance, execution_feedback, Z8 execution output, V3 sandbox output, Z9 persistent memory runtime, production payload, broker payload

## Future Output Allowed
Explanation quality review, evidence completeness review, confidence alignment review, missing evidence review, degradation review, blocked output review, readonly Z2 feedback candidate, next validation requirement, human review requirement

## Future Output Forbidden
trade_instruction, buy_signal, sell_signal, position_weight, order_signal, automatic_rebalance, broker_action, paper_trade_order, real_trade_order, real_pnl, performance_claim, alpha_claim, expected_return_claim, production_decision, memory_mutation_result, persistent_memory_write

## Key Statements
- Z9 Review Node reviews explanation quality and evidence completeness only.
- Z9 Review Node does not evaluate trading profit.
- Z9 Review Node does not issue trade instructions.
- Z9 Review Node cannot trigger Z8 or broker.
- Z9 Review Node cannot mutate persistent memory in P0.
- Level 5 remains BLOCKED.
- No runtime enablement. No adapter execution enablement. No capability execution.
