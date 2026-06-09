# Z9 Review Node Planning — Z2 FEEDBACK POLICY

> Status: PLANNING | Base: 5032c4d | Branch: plan/skillos-z9-review-node-planning
> Date: 2026-06-09 | Author: Z2 天师

---

## 1. Feedback Nature

Z9 feedback is advisory and readonly. The z2_feedback_candidate is produced as a
suggestion for Z2 to consider in future report revisions. It has NO automatic effect.
It does NOT modify Z2 state. It does NOT trigger any execution.

## 2. Allowed Feedback Fields

| Field | Type | Purpose |
|---|---|---|
| source_z2_report_node_id | str | Which Z2 report was reviewed |
| review_label | str | From allowed REVIEW_LABEL values |
| evidence_gap_summary | str | Summary of identified gaps |
| confidence_alignment_issue | str | Alignment problems found |
| blocked_output_issue | str | Blocked output concerns |
| missing_evidence | list[str] | Specific missing items |
| recommended_report_revision | str | Suggested improvements |
| next_validation_requirement | str | Future validation needs |
| readonly_only | bool | Always True |
| requires_human_review | bool | Whether human should review |

## 3. FORBIDDEN Feedback Fields

| Field | Reason | Gate |
|---|---|---|
| auto_patch_z2_report | No automatic patching | z2_feedback contract |
| auto_update_factor_score | No factor manipulation | z2_feedback contract |
| auto_update_memory | DENY_Z9_MEMORY_MUTATION_FORBIDDEN | kill_switch |
| auto_trade_adjustment | No trade authority | kill_switch |
| position_adjustment | No position authority | kill_switch |
| rebalance_instruction | No rebalance authority | kill_switch |
| broker_instruction | No broker authority | kill_switch |

## 4. Feedback Delivery

The z2_feedback_candidate is:
- Produced as a frozen dataclass
- Hashed (z9_feedback_candidate_hash)
- Stored in review output
- Available for human inspection
- NOT automatically applied to Z2
- NOT triggering any pipeline
- NOT modifying any state
- no_trade_result = True always

## 5. Feedback Scope

Z9 can suggest:
- "Evidence for sector X is missing" (evidence gap)
- "Confidence level seems high given missing data" (alignment)
- "Consider adding research_summary for Y" (improvement)
- "Risk warning may need expansion" (risk)

Z9 CANNOT suggest:
- "Buy more of X" (trade instruction)
- "Reduce position in Y" (position change)
- "Expected return is Z%" (performance claim)
- "Alpha decayed by N%" (trade attribution)

## 6. Feedback Validation

Before z2_feedback_candidate is emitted:
1. Verify all fields are from allowed list
2. Verify no forbidden fields present
3. Verify readonly_only = True
4. Verify no trade terminology in free-text fields
5. Hash the feedback → z9_feedback_candidate_hash
6. Include in z9_review_node_hash
7. Append to audit trail

## 7. Feedback Testing

Future tests must verify:
- z2_feedback_candidate contains only allowed fields
- Forbidden fields trigger rejection
- Free-text fields don't contain trade language
- readonly_only is always True
- Feedback does not modify Z2 state
- DENY_Z9_TRADE_RESULT_FORBIDDEN if trade terms in feedback
- z9_review_snapshot_candidate is the sole input source
- Integration test: feedback does not trigger any pipeline
