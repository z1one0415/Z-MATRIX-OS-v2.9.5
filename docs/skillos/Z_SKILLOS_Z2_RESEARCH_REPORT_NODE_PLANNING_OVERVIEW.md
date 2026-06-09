# Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING — OVERVIEW

> Planning document for Z2 Research Report Node capability.
> Branch: plan/skillos-z2-research-report-node-planning
> Base commit: 74c27fa

---

## 1. Status

| Field | Value |
|-------|-------|
| Document | OVERVIEW |
| Status | PLANNING |
| Created | 2026-06-09 |
| Seal Target | Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING_SEALED |
| Closeout Target | Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING_READY_FOR_REVIEW |
| Base Commit | 74c27fa |
| Dependency | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED (postmerge HEAD = 74c27fa) |

---

## 2. Scope

The Z2 Research Report Node is an explanatory research report generation capability.

- **Purpose**: Generate human-readable research reports from B1 CompositionGraphResponse data
- **Nature**: Explanatory research report — NOT investment advice, NOT trade signal
- **Input**: B1 CompositionGraphResponse exclusively as primary structured input
- **Output**: Structured 12-section research report with evidence chain, confidence levels, and z9_review_snapshot_candidate
- **Invariant**: no_alpha_claim = true, no_trade_signal = true at all times
- **Hash anchor**: z2_report_node_hash computed per report instance

### What Z2 Research Report Node IS:
- A readonly explanatory report builder
- A structured evidence summarizer consuming B1 graph outputs
- A z9_review_snapshot_candidate producer for downstream review

### What Z2 Research Report Node is NOT:
- NOT a trade signal generator
- NOT an alpha claim system
- NOT a position weight calculator
- NOT a broker action dispatcher
- NOT a portfolio rebalancer

---

## 3. Dependency / Evidence

| Dependency | Source | Status |
|-----------|--------|--------|
| B1 CompositionGraphResponse | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED | MERGED at 74c27fa |
| B1 graph evidence chain | Inherited from B1 postmerge | AVAILABLE |
| A1 bridge evidence through B1 | Transitive via B1 | AVAILABLE |
| Factor Library readonly metadata | Through B1/A1 only | AVAILABLE (readonly) |
| FactorEvaluationMatrix | Future optional | NOT YET AVAILABLE |
| Small Real Sample summary | Future optional | NOT YET AVAILABLE |
| Static user research question | Runtime context | AVAILABLE |
| Local in-memory report template | Internal | AVAILABLE |

---

## 4. Boundary

- Z2 Research Report Node operates in READONLY mode only
- No writes to any external system
- No network calls to broker, trading, or production systems
- No access to raw factor values or FactorInvocationResponse
- No access to research/factor_library files directly
- No access to Z8/Z9/V3 runtime internals
- Confidence level restricted to: LOW, MEDIUM, HIGH_WITH_STRUCTURE_ONLY
- All outputs must pass blocked_outputs_removed validation before emission

---

## 5. Forbidden Actions

The following are DIRECTLY FORBIDDEN:
- Consuming FactorInvocationResponse
- Consuming raw factor values
- Reading research/factor_library files directly
- Accessing broker/production/real returns/real trades/paper trades
- Accessing Z2 runtime internals, Z8, Z9, or V3 directly
- Emitting alpha_claim, expected_return_claim, buy_signal, sell_signal
- Emitting position_weight, order_signal, trade_instruction
- Emitting paper_trade_order, broker_action, portfolio_rebalance
- Emitting real_trade_order, production_decision
- Any action that bypasses the B1 CompositionGraphResponse contract

---

## 6. Proof / Review Requirements

- All 26 planning documents must be created and pass line count validation
- Every document must contain the 7-section structure
- Required phrases must appear across the corpus: "B1 CompositionGraphResponse", "z9_review_snapshot_candidate", "no_alpha_claim", "no_trade_signal", "z2_report_node_hash", "74c27fa"
- Test and Proof Plan must enumerate ≥41 proof categories
- Review Checklist must contain ≥34 checks
- Merge Checklist must contain ≥28 checks
- Risk registers must enumerate risks with severity/likelihood/mitigation/control/rollback trigger

---

## 7. Next Legal Entry

- After OVERVIEW: proceed to SCOPE.md for detailed scope definition
- After all 14 planning docs: proceed to REVIEW_GATE.md
- After all review docs: proceed to MERGE_REVIEW.md
- Final: MERGE_CLOSEOUT.md with status Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING_MERGE_REVIEW_READY_FOR_HUMAN_DECISION

---

## Future Files (reference only — DO NOT create in this phase)

### Code:
- skillos/capability_invocation_os/research_report_node/__init__.py
- skillos/capability_invocation_os/research_report_node/constants.py
- skillos/capability_invocation_os/research_report_node/config.py
- skillos/capability_invocation_os/research_report_node/models.py
- skillos/capability_invocation_os/research_report_node/contracts.py
- skillos/capability_invocation_os/research_report_node/section_builder.py
- skillos/capability_invocation_os/research_report_node/evidence.py
- skillos/capability_invocation_os/research_report_node/degradation.py
- skillos/capability_invocation_os/research_report_node/report_builder.py
- skillos/capability_invocation_os/research_report_node/z9_snapshot.py
- skillos/capability_invocation_os/research_report_node/kill_switch.py
- skillos/capability_invocation_os/research_report_node/registry.py

### Tests:
- tests/skillos/capability_invocation_os/research_report_node/test_disabled_default.py
- tests/skillos/capability_invocation_os/research_report_node/test_models.py
- tests/skillos/capability_invocation_os/research_report_node/test_contracts.py
- tests/skillos/capability_invocation_os/research_report_node/test_section_builder.py
- tests/skillos/capability_invocation_os/research_report_node/test_evidence.py
- tests/skillos/capability_invocation_os/research_report_node/test_degradation.py
- tests/skillos/capability_invocation_os/research_report_node/test_report_builder.py
- tests/skillos/capability_invocation_os/research_report_node/test_z9_snapshot.py
- tests/skillos/capability_invocation_os/research_report_node/test_no_forbidden_imports.py
