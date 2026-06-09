# Z2 Research Report Node Implementation Planning — SPEC

> Status: PLANNING_COMPLETE
> Seal: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED
> Date: 2026-06-09
> Branch: plan/skillos-z2-research-report-node-implementation-planning
> Base: c5f69f5

---

## 1. Status

| Field | Value |
|-------|-------|
| Phase | Planning (docs-only) |
| Confidence | HIGH_WITH_STRUCTURE_ONLY |
| Degradation | DENY_Z2_OUTPUTS_UNSAFE when kill-switch active |
| Upstream sealed | Z2_RESEARCH_REPORT_NODE_PLANNING_CLEAN_MERGED_AND_SEALED |
| Upstream sealed | Z9_REVIEW_NODE_PLANNING_MERGED_AND_SEALED |
| Upstream sealed | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED |
| Upstream sealed | A1_FACTOR_LIBRARY_BRIDGE_DISABLED_DEFAULT_P0_MERGED_AND_SEALED |
| Upstream sealed | FACTOR_LIBRARY_READONLY_ADAPTER_DISABLED_DEFAULT_P0_MERGED_AND_SEALED |
| postmerge HEAD | c5f69f5 |

## 2. Scope

This specification defines the implementation plan for the Z2 Research Report Node within the SkillOS Capability Invocation framework. The node consumes B1 CompositionGraphResponse as its primary input, produces structured research reports, and emits z9_review_snapshot_candidate for downstream Z9 review processing.

### Primary Deliverables
- ResearchReportNodeRequest / ResearchReportNodeResponse models
- ResearchReportSection, ResearchReportEvidence, ResearchReportDecision, ResearchReportSummary
- Z9ReviewSnapshotCandidate output contract
- ReportDegradationStatus for graceful failure
- Kill-switch with disabled-by-default pattern
- Section builder pipeline
- Evidence validation layer
- Degradation handler

### Future Code Files (plan only)
- skillos/capability_invocation_os/research_report_node/__init__.py
- skillos/capability_invocation_os/research_report_node/constants.py
- skillos/capability_invocation_os/research_report_node/config.py
- skillos/capability_invocation_os/research_report_node/kill_switch.py
- skillos/capability_invocation_os/research_report_node/models.py
- skillos/capability_invocation_os/research_report_node/contracts.py
- skillos/capability_invocation_os/research_report_node/section_builder.py
- skillos/capability_invocation_os/research_report_node/evidence.py
- skillos/capability_invocation_os/research_report_node/degradation.py
- skillos/capability_invocation_os/research_report_node/report_builder.py
- skillos/capability_invocation_os/research_report_node/z9_snapshot.py
- skillos/capability_invocation_os/research_report_node/registry.py

### Future Test Files (plan only)
- tests/skillos/capability_invocation_os/research_report_node/test_disabled_default.py
- tests/skillos/capability_invocation_os/research_report_node/test_models.py
- tests/skillos/capability_invocation_os/research_report_node/test_contracts.py
- tests/skillos/capability_invocation_os/research_report_node/test_section_builder.py
- tests/skillos/capability_invocation_os/research_report_node/test_evidence.py
- tests/skillos/capability_invocation_os/research_report_node/test_degradation.py
- tests/skillos/capability_invocation_os/research_report_node/test_report_builder.py
- tests/skillos/capability_invocation_os/research_report_node/test_z9_snapshot.py
- tests/skillos/capability_invocation_os/research_report_node/test_no_forbidden_imports.py

## 3. Dependency

| Dependency | Status | Seal |
|------------|--------|------|
| Z2 Research Report Node Planning | Merged | Z2_RESEARCH_REPORT_NODE_PLANNING_CLEAN_MERGED_AND_SEALED |
| Z9 Review Node Planning | Merged | Z9_REVIEW_NODE_PLANNING_MERGED_AND_SEALED |
| B1 Composition Graph Factor Bridge | Merged | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED |
| A1 Factor Library Bridge | Merged | A1_FACTOR_LIBRARY_BRIDGE_DISABLED_DEFAULT_P0_MERGED_AND_SEALED |
| Factor Library Readonly Adapter | Merged | FACTOR_LIBRARY_READONLY_ADAPTER_DISABLED_DEFAULT_P0_MERGED_AND_SEALED |
| postmerge HEAD | c5f69f5 | Verified |

## 4. Boundary

- This plan covers ONLY the research_report_node module
- Input boundary: B1 CompositionGraphResponse (read-only consumption)
- Output boundary: z9_review_snapshot_candidate (structured emission)
- No direct database access — all state via upstream contracts
- No network calls — all data arrives via function parameters
- No file I/O — pure computation pipeline
- Kill-switch defaults to DISABLED (node produces no output until explicitly enabled)

## 5. Forbidden

The following fields are PERMANENTLY FORBIDDEN in any model or output:
- alpha_claim
- expected_return_claim
- buy_signal
- sell_signal
- position_weight
- order_signal
- trade_instruction
- paper_trade_order
- broker_action
- portfolio_rebalance
- real_trade_order
- production_decision
- real_pnl
- trade_result

Violation of any forbidden field constitutes a P0 security breach.

## 6. Proof

- All planning docs pass 7-section structure validation
- All status markers present and correct
- Dependency chain verified against postmerge HEAD c5f69f5
- Forbidden field list exhaustive and cross-referenced
- Future code map complete (12 source + 9 test files)
- No code created in planning phase

## 7. Next

- Human review of planning documentation
- Approval gate before implementation phase
- Implementation will follow disabled-by-default pattern
- First implementation batch: models + contracts + kill_switch
- Second batch: section_builder + evidence + degradation
- Third batch: report_builder + z9_snapshot + registry
- All batches require test-first development

---

**SEAL: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED**
