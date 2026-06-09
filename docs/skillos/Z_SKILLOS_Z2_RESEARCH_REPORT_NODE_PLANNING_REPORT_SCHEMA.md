# Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING — REPORT_SCHEMA

> 12-section report schema for Z2 Research Report Node.
> Branch: plan/skillos-z2-research-report-node-planning
> Base commit: 74c27fa

---

## 1. Status

| Field | Value |
|-------|-------|
| Document | REPORT_SCHEMA |
| Status | PLANNING |
| Created | 2026-06-09 |
| Parent | OUTPUT_CONTRACT.md |
| Dependency | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED (postmerge HEAD = 74c27fa) |

---

## 2. Scope

This document defines the 12-section report schema produced by the Z2 Research Report Node.
Each section is a self-contained unit with its own evidence references, confidence level,
and degradation status. The complete report is anchored by z2_report_node_hash.

The report is an explanatory research document consuming B1 CompositionGraphResponse.
It enforces no_alpha_claim and no_trade_signal across all 12 sections.

---

## 3. Dependency / Evidence

### 3.1 Report Sections (12)

#### Section 1: report_header
| Field | Value |
|-------|-------|
| section_id | 1 |
| section_type | report_header |
| source_refs | [research_report_node_id, source_graph_ref] |
| evidence_refs | [source_graph_hash, input_evidence_refs] |
| confidence_level | Inherited from overall report |
| degradation_status | Inherited from overall report |
| blocked_outputs_removed | [] or list of removed items |

#### Section 2: source_graph_summary
| Field | Value |
|-------|-------|
| section_id | 2 |
| section_type | source_graph_summary |
| source_refs | [B1 CompositionGraphResponse ref] |
| evidence_refs | [graph_node_hash, graph_edge_hash] |
| confidence_level | Per-section assessment |
| degradation_status | Per-section assessment |
| blocked_outputs_removed | [] or list |

#### Section 3: factor_context_summary
| Field | Value |
|-------|-------|
| section_id | 3 |
| section_type | factor_context_summary |
| source_refs | [factor_decision_hash, bridge_decision_hash] |
| evidence_refs | [factor_context_summary_hash] |
| confidence_level | Per-section |
| degradation_status | Per-section |
| blocked_outputs_removed | [] or list |

#### Section 4: evidence_chain_summary
| Field | Value |
|-------|-------|
| section_id | 4 |
| section_type | evidence_chain_summary |
| source_refs | [all evidence chain hashes] |
| evidence_refs | [z2_report_evidence_hash] |
| confidence_level | Per-section |
| degradation_status | Per-section |
| blocked_outputs_removed | [] or list |

#### Section 5: structural_readiness_summary
| Field | Value |
|-------|-------|
| section_id | 5 |
| section_type | structural_readiness_summary |
| source_refs | [permission_tier, no_real_source_flag] |
| evidence_refs | [structural assessment hashes] |
| confidence_level | Per-section |
| degradation_status | Per-section |
| blocked_outputs_removed | [] or list |

#### Section 6: research_interpretation
| Field | Value |
|-------|-------|
| section_id | 6 |
| section_type | research_interpretation |
| source_refs | [research_question, factor_context] |
| evidence_refs | [interpretation evidence hashes] |
| confidence_level | Per-section |
| degradation_status | Per-section |
| blocked_outputs_removed | [] or list |

#### Section 7: risk_warning
| Field | Value |
|-------|-------|
| section_id | 7 |
| section_type | risk_warning |
| source_refs | [degradation_status, missing evidence indicators] |
| evidence_refs | [risk assessment hashes] |
| confidence_level | Per-section |
| degradation_status | Per-section |
| blocked_outputs_removed | [] or list |

#### Section 8: missing_evidence
| Field | Value |
|-------|-------|
| section_id | 8 |
| section_type | missing_evidence |
| source_refs | [evidence_chain gaps] |
| evidence_refs | [missing evidence catalog hashes] |
| confidence_level | Per-section |
| degradation_status | Per-section |
| blocked_outputs_removed | [] or list |

#### Section 9: blocked_outputs_removed
| Field | Value |
|-------|-------|
| section_id | 9 |
| section_type | blocked_outputs_removed |
| source_refs | [output validation scan results] |
| evidence_refs | [forbidden_outputs_removed_hash] |
| confidence_level | N/A (mechanical) |
| degradation_status | N/A (mechanical) |
| blocked_outputs_removed | [list of all blocked items across all sections] |

#### Section 10: confidence_section
| Field | Value |
|-------|-------|
| section_id | 10 |
| section_type | confidence_section |
| source_refs | [all section confidence assessments] |
| evidence_refs | [confidence computation hashes] |
| confidence_level | Overall: LOW / MEDIUM / HIGH_WITH_STRUCTURE_ONLY |
| degradation_status | Overall assessment |
| blocked_outputs_removed | [] or list |

#### Section 11: z9_review_snapshot_candidate
| Field | Value |
|-------|-------|
| section_id | 11 |
| section_type | z9_review_snapshot_candidate |
| source_refs | [all report hashes] |
| evidence_refs | [z2_report_node_hash, z2_report_section_hash (all)] |
| confidence_level | Inherited |
| degradation_status | Inherited |
| blocked_outputs_removed | [] or list |

#### Section 12: next_validation_requirement
| Field | Value |
|-------|-------|
| section_id | 12 |
| section_type | next_validation_requirement |
| source_refs | [review requirements, missing evidence] |
| evidence_refs | [validation requirement hashes] |
| confidence_level | N/A |
| degradation_status | N/A |
| blocked_outputs_removed | [] or list |

---

## 4. Boundary

- All 12 sections MUST be present in every report (even if degraded/empty)
- Section ordering is fixed (1-12)
- Each section independently tracks its own blocked_outputs_removed
- Section 9 aggregates all blocked outputs across all sections
- z2_report_section_hash computed per section for integrity

---

## 5. Forbidden Actions

- Omitting any of the 12 sections
- Reordering sections
- Adding sections beyond the 12 defined
- Emitting a section without its required metadata fields
- Skipping blocked_outputs_removed for any section
- Including alpha_claim or trade_signal content in any section

---

## 6. Proof / Review Requirements

- Schema validation test must verify all 12 sections present
- Each section must pass individual field validation
- z2_report_section_hash must be verified per section
- Aggregate blocked_outputs_removed in section 9 must match union of all sections
- no_alpha_claim and no_trade_signal must hold in every section's content

---

## 7. Next Legal Entry

- Proceed to EVIDENCE_CHAIN.md for hash propagation rules
- Report schema feeds into section_builder.py implementation planning
- z9_review_snapshot_candidate (section 11) feeds into Z9_HANDOFF_PREP.md
