# Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING — Z9_HANDOFF_PREP

> Z9 review snapshot candidate preparation for Z2 Research Report Node.
> Branch: plan/skillos-z2-research-report-node-planning
> Base commit: 74c27fa

---

## 1. Status

| Field | Value |
|-------|-------|
| Document | Z9_HANDOFF_PREP |
| Status | PLANNING |
| Created | 2026-06-09 |
| Parent | DEGRADATION_POLICY.md |
| Dependency | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED (postmerge HEAD = 74c27fa) |

---

## 2. Scope

This document defines the z9_review_snapshot_candidate structure that Z2 Research Report
Node produces for downstream Z9 consumption. The snapshot is a self-contained summary
enabling Z9 to review the report without accessing Z2 internals.

The snapshot enforces no_alpha_claim and no_trade_signal by design — it contains only
structural and evidence metadata, never trade-related fields.

---

## 3. Dependency / Evidence

### 3.1 Z9 Handoff ALLOWED Fields

| # | Field | Type | Source |
|---|-------|------|--------|
| 1 | report_node_id | UUID | Z2 generated (= research_report_node_id) |
| 2 | source_graph_hash | Hash | From B1 CompositionGraphResponse |
| 3 | factor_context_summary_hash | Hash | Computed from factor_context_summary |
| 4 | evidence_chain_hash | Hash | = z2_report_evidence_hash |
| 5 | research_summary_hash | Hash | Computed from research_summary |
| 6 | risk_warning_hash | Hash | Computed from risk_warning section |
| 7 | confidence_level | Enum | LOW / MEDIUM / HIGH_WITH_STRUCTURE_ONLY |
| 8 | confidence_reason | String | Human-readable explanation |
| 9 | missing_evidence | List[String] | Catalog of missing evidence items |
| 10 | degradation_status | Enum | Current degradation decision |
| 11 | blocked_outputs_removed | List[Object] | All blocked output records |
| 12 | review_required | Boolean | Whether Z9 review is needed |
| 13 | review_reason | String | Why review is required |
| 14 | readonly_only | Boolean | Always TRUE |

### 3.2 Z9 Handoff FORBIDDEN Fields

| # | Forbidden Field | Category | Reason |
|---|----------------|----------|--------|
| 1 | trade_result | Trade | Z9 handoff must not contain trade results |
| 2 | paper_trade_result | Trade | Z9 handoff must not contain paper trade data |
| 3 | broker_result | Execution | Z9 handoff must not contain broker outcomes |
| 4 | real_pnl | Production | Z9 handoff must not contain real P&L |
| 5 | position_change | Portfolio | Z9 handoff must not contain position changes |
| 6 | automatic_rebalance | Portfolio | Z9 handoff must not contain rebalance actions |
| 7 | execution_feedback | Execution | Z9 handoff must not contain execution feedback |

### 3.3 Snapshot Generation Rules

1. Snapshot is generated ONLY when degradation_status is ALLOW_* (not DENY_*)
2. Snapshot is generated AFTER blocked_outputs_removed scan completes
3. Snapshot includes z2_report_node_hash for Z9 to verify integrity
4. Snapshot is self-contained — Z9 does not need to access Z2 internals
5. review_required is TRUE when confidence_level is LOW or degradation is active
6. review_reason explains what Z9 should focus on

### 3.4 Snapshot Hash Integrity

The z9_review_snapshot_candidate itself is included in z2_report_node_hash computation.
This creates a commitment: once the snapshot is generated, it cannot be modified without
invalidating the report hash. This prevents post-hoc modification of review data.

---

## 4. Boundary

- Snapshot ONLY generated under ALLOW decisions
- Snapshot contains ONLY hashes and metadata, never raw report content
- Snapshot is readonly — Z9 cannot write back to Z2 through this channel
- no_alpha_claim = true in every snapshot
- no_trade_signal = true in every snapshot
- z2_report_node_hash anchors snapshot integrity

---

## 5. Forbidden Actions

- Generating snapshot under DENY degradation decisions
- Including any of the 7 forbidden Z9 handoff fields
- Including raw report content (only hashes permitted for content fields)
- Allowing Z9 to modify Z2 state through the snapshot
- Omitting review_required/review_reason when conditions warrant review
- Computing snapshot hash after report hash (must be included in report hash)

---

## 6. Proof / Review Requirements

- Test snapshot generation under each ALLOW decision
- Test snapshot rejection under each DENY decision
- Test all 7 forbidden fields are absent from snapshot
- Test all 14 allowed fields are present when applicable
- Verify snapshot hash is included in z2_report_node_hash
- Verify review_required logic triggers correctly

---

## 7. Next Legal Entry

- Proceed to TEST_AND_PROOF_PLAN.md for comprehensive test enumeration
- Z9 handoff feeds into REVIEW_CHECKLIST.md verification
- Snapshot integrity verified in MERGE_CHECKLIST.md
