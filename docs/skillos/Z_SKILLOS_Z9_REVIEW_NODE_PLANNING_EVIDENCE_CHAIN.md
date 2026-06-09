# Z9 Review Node Planning — EVIDENCE CHAIN

> Status: PLANNING | Base: 5032c4d | Branch: plan/skillos-z9-review-node-planning
> Date: 2026-06-09 | Author: Z2 天师

---

## 1. Evidence Chain Definition

The evidence chain is inherited from Z2's z9_review_snapshot_candidate. Z9 does NOT
generate new evidence — it reviews the completeness and coherence of existing evidence.
All fields are readonly. Z9 feedback is advisory and readonly.

## 2. Inherited Hash Fields

| Field | Source | Mutability | Purpose |
|---|---|---|---|
| source_graph_hash | Z2 | Immutable | Graph integrity |
| factor_context_summary_hash | Z2 | Immutable | Factor summary integrity |
| evidence_chain_hash | Z2 | Immutable | Chain integrity |
| research_summary_hash | Z2 | Immutable | Research integrity |
| risk_warning_hash | Z2 | Immutable | Risk assessment integrity |
| confidence_level | Z2 | Immutable | Confidence score |
| confidence_reason | Z2 | Immutable | Confidence explanation |
| missing_evidence | Z2 | Immutable | Known gaps |
| degradation_status | Z2 | Immutable | Degradation state |
| blocked_outputs_removed | Z2 | Immutable | Blocked outputs |
| review_required | Z2 | Immutable | Always True |
| review_reason | Z2 | Immutable | Trigger reason |
| readonly_only | Z2 | Immutable | Always True |

## 3. Z9-Produced Hashes

| Field | Producer | Purpose |
|---|---|---|
| z9_review_node_hash | Z9 | Entire review hash |
| z9_review_section_hash | Z9 | Per-section hash |
| z9_feedback_candidate_hash | Z9 | Feedback hash |
| rollback_marker | Inherited | Preserved unchanged |
| privacy_marker | Inherited | Preserved unchanged |

## 4. Chain Validation Logic

```
1. Receive z9_review_snapshot_candidate
2. Verify all hash fields are 64-char hex
3. Verify evidence_chain_hash is present
4. Verify source_graph_hash is present
5. If any hash missing → DENY_Z9_EVIDENCE_INCOMPLETE
6. If trade_result detected → DENY_Z9_TRADE_RESULT_FORBIDDEN
7. Produce z9_review_node_hash from review output
8. Produce z9_review_section_hash per section
9. Produce z9_feedback_candidate_hash for feedback
10. Append to immutable audit trail
```

## 5. Evidence Completeness Assessment

Z9 assesses whether Z2's evidence chain is complete:
- Are all required hashes present?
- Does confidence_level align with evidence depth?
- Are missing_evidence items acknowledged?
- Is degradation_status consistent with evidence gaps?
- Are blocked_outputs_removed properly listed?

## 6. Evidence Gap Identification

When gaps are found:
- evidence_gap_attribution is produced (allowed)
- missing_source_attribution is produced (allowed)
- structural_readiness_attribution is produced (allowed)
- NO pnl_attribution (FORBIDDEN)
- NO trade_attribution (FORBIDDEN)
- NO slippage_attribution (FORBIDDEN)
- no_trade_result = True always

## 7. Chain Integrity Guarantees

- Z9 never modifies inherited hashes
- Z9 never recomputes Z2 hashes
- Z9 only appends its own hashes
- Chain is append-only, never mutated
- rollback_marker preserved without modification
- privacy_marker preserved without modification
- Entire chain is auditable post-hoc
