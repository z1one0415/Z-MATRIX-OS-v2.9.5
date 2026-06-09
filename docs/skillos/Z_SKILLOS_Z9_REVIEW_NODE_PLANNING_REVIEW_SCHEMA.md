# Z9 Review Node Planning — REVIEW SCHEMA

> Status: PLANNING | Base: 5032c4d | Branch: plan/skillos-z9-review-node-planning
> Date: 2026-06-09 | Author: Z2 天师

---

## 1. Schema Overview

The Z9 Review produces a structured document with 12 sections. Each section has standardized
metadata fields. The review consumes z9_review_snapshot_candidate and produces an explanation
quality assessment. Z9 feedback is advisory and readonly.

## 2. Section Registry (12 Sections)

| # | Section ID | Section Type | Purpose |
|---|---|---|---|
| 1 | review_header | HEADER | Review metadata and IDs |
| 2 | source_z2_report_snapshot | SOURCE | Inherited snapshot reference |
| 3 | evidence_chain_review | EVIDENCE | Hash chain validation |
| 4 | confidence_alignment_review | CONFIDENCE | Level vs evidence alignment |
| 5 | missing_evidence_review | GAPS | Identified evidence gaps |
| 6 | degradation_review | DEGRADATION | Status and implications |
| 7 | blocked_output_review | BLOCKED | Removed outputs assessment |
| 8 | explanation_quality_review | QUALITY | Primary quality label |
| 9 | risk_warning_review | RISK | Risk assessment review |
| 10 | next_validation_review | FUTURE | Future validation needs |
| 11 | z2_feedback_candidate | FEEDBACK | Advisory feedback for Z2 |
| 12 | closeout_section | CLOSEOUT | Final seal and hash |

## 3. Section Metadata (per section)

```python
@dataclass
class ReviewSection:
    section_id: str                    # Unique section identifier
    section_type: str                  # From enum above
    source_refs: list[str]            # Referenced source hashes
    evidence_refs: list[str]          # Evidence chain refs
    review_label: str                 # Section-level label
    confidence_alignment_label: str   # Alignment assessment
    degradation_status: str           # Section degradation
    blocked_outputs_removed: list[str] # Blocked in this section
    readonly_only: bool               # Always True
```

## 4. Review Header Section

Contains:
- z9_review_node_id (UUID)
- review_mode: "READONLY_EXPLANATION_REVIEW"
- source_z2_report_node_id (from input)
- source_graph_hash (inherited)
- evidence_chain_hash (inherited)
- review_scope: "EXPLANATION_QUALITY_ONLY"
- no_trade_result: True
- no_paper_trading: True
- no_broker_action: True
- no_position_change: True
- DENY_Z9_TRADE_RESULT_FORBIDDEN marker

## 5. Evidence Chain Section

Validates:
- source_graph_hash integrity
- factor_context_summary_hash presence
- evidence_chain_hash continuity
- research_summary_hash linkage
- risk_warning_hash completeness
- z9_review_node_hash (self-produced)
- z9_review_section_hash (per section)
- z9_feedback_candidate_hash (feedback)
- rollback_marker (inherited, preserved)
- privacy_marker (inherited, preserved)

## 6. z2_feedback_candidate Section

Advisory output only:
- source_z2_report_node_id
- review_label (from allowed set)
- evidence_gap_summary
- confidence_alignment_issue
- blocked_output_issue
- missing_evidence
- recommended_report_revision
- next_validation_requirement
- readonly_only: True
- requires_human_review: bool

FORBIDDEN in feedback:
- auto_patch_z2_report
- auto_update_factor_score
- auto_update_memory
- auto_trade_adjustment
- position_adjustment
- rebalance_instruction
- broker_instruction

## 7. Schema Validation Rules

- All 12 sections must be present in output
- Each section must have all metadata fields
- readonly_only must be True in every section
- No section may contain forbidden output fields
- z2_feedback_candidate must be advisory only
- DISABLED_DEFAULT_NOOP produces empty schema (no sections)
