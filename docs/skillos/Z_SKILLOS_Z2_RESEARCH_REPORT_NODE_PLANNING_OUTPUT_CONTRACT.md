# Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING — OUTPUT_CONTRACT

> Formal output contract for Z2 Research Report Node.
> Branch: plan/skillos-z2-research-report-node-planning
> Base commit: 74c27fa

---

## 1. Status

| Field | Value |
|-------|-------|
| Document | OUTPUT_CONTRACT |
| Status | PLANNING |
| Created | 2026-06-09 |
| Parent | INPUT_CONTRACT.md |
| Dependency | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED (postmerge HEAD = 74c27fa) |

---

## 2. Scope

This document defines the complete and exhaustive list of output fields that the Z2 Research
Report Node may emit. Any output not listed in the ALLOWED section is FORBIDDEN and must
trigger DENY_Z2_OUTPUTS_UNSAFE if detected in the output payload.

The Z2 Research Report Node produces explanatory research reports only. It enforces
no_alpha_claim and no_trade_signal at the output validation stage. The z2_report_node_hash
anchors every report instance for audit trail purposes.

---

## 3. Dependency / Evidence

### 3.1 ALLOWED Output Fields (Exhaustive)

| # | Field | Type | Description |
|---|-------|------|-------------|
| 1 | research_report_node_id | UUID | Unique identifier for this report instance |
| 2 | report_mode | Enum | READONLY_REPORT / DEGRADED_REPORT |
| 3 | source_graph_ref | String | Reference to source B1 CompositionGraphResponse |
| 4 | source_graph_hash | Hash | Hash of the consumed B1 graph |
| 5 | input_evidence_refs | List[Hash] | References to all input evidence items |
| 6 | factor_context_summary | String | Human-readable factor context explanation |
| 7 | factor_family_context_summary | String | Factor family grouping summary |
| 8 | research_question | String | The user's research question (echoed) |
| 9 | research_summary | String | Explanatory research summary |
| 10 | factor_role | String | Role of factors in the graph structure |
| 11 | applicable_scenario | String | When this research applies |
| 12 | risk_warning | String | Mandatory risk disclosure |
| 13 | confidence_level | Enum | LOW / MEDIUM / HIGH_WITH_STRUCTURE_ONLY |
| 14 | confidence_reason | String | Why this confidence level was assigned |
| 15 | evidence_refs | List[Hash] | All evidence hashes for this report |
| 16 | blocked_outputs_removed | List[String] | Names of outputs that were blocked |
| 17 | degradation_status | Enum | Degradation decision applied |
| 18 | z9_review_snapshot_candidate | Object | Snapshot for Z9 review consumption |
| 19 | readonly_only | Boolean | Always TRUE |
| 20 | no_alpha_claim | Boolean | Always TRUE |
| 21 | no_trade_signal | Boolean | Always TRUE |
| 22 | no_position_weight | Boolean | Always TRUE |

### 3.2 Output Invariants

- readonly_only MUST be TRUE in every output
- no_alpha_claim MUST be TRUE in every output
- no_trade_signal MUST be TRUE in every output
- no_position_weight MUST be TRUE in every output
- blocked_outputs_removed MUST be a non-empty list (even if empty means "[]")
- z2_report_node_hash must be computable from the output fields

---

## 4. Boundary

### FORBIDDEN Output Fields (Exhaustive):

| # | Forbidden Field | Category | Reason |
|---|----------------|----------|--------|
| 1 | alpha_claim | Trade signal | Regulatory/safety |
| 2 | expected_return_claim | Trade signal | Regulatory/safety |
| 3 | buy_signal | Trade signal | Regulatory/safety |
| 4 | sell_signal | Trade signal | Regulatory/safety |
| 5 | position_weight | Portfolio mgmt | Scope violation |
| 6 | order_signal | Execution | Production safety |
| 7 | trade_instruction | Execution | Production safety |
| 8 | paper_trade_order | Execution | Production safety |
| 9 | broker_action | Execution | Production safety |
| 10 | portfolio_rebalance | Portfolio mgmt | Production safety |
| 11 | real_trade_order | Execution | Production safety |
| 12 | production_decision | Production | Production safety |

### Output Validation Pipeline:
1. Generate report sections
2. Compute section hashes (z2_report_section_hash per section)
3. Run forbidden output scan on all fields
4. Populate blocked_outputs_removed with any detected forbidden content
5. Compute z2_report_evidence_hash
6. Compute z2_report_node_hash
7. Emit validated output

---

## 5. Forbidden Actions

- Emitting any field from the FORBIDDEN Output Fields list
- Emitting output without running blocked_outputs_removed validation
- Emitting output without computing z2_report_node_hash
- Emitting confidence_level outside {LOW, MEDIUM, HIGH_WITH_STRUCTURE_ONLY}
- Setting readonly_only to FALSE
- Setting no_alpha_claim to FALSE
- Setting no_trade_signal to FALSE
- Bypassing z9_review_snapshot_candidate generation

---

## 6. Proof / Review Requirements

- Every allowed output field must have a test verifying its presence in valid reports
- Every forbidden output field must have a test verifying its absence/rejection
- Output invariants must be tested as property-based tests
- z2_report_node_hash determinism must be verified with fixture data
- blocked_outputs_removed must be tested with deliberately injected forbidden content

---

## 7. Next Legal Entry

- Proceed to REPORT_SCHEMA.md for the 12-section report structure
- Output contract feeds into BLOCKED_OUTPUT_POLICY.md
- Output hashes feed into EVIDENCE_CHAIN.md and Z9_HANDOFF_PREP.md
