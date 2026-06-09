# Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING — CONFIDENCE_POLICY

> Confidence level assignment policy for Z2 Research Report Node.
> Branch: plan/skillos-z2-research-report-node-planning
> Base commit: 74c27fa

---

## 1. Status

| Field | Value |
|-------|-------|
| Document | CONFIDENCE_POLICY |
| Status | PLANNING |
| Created | 2026-06-09 |
| Parent | EVIDENCE_CHAIN.md |
| Dependency | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED (postmerge HEAD = 74c27fa) |

---

## 2. Scope

This document defines how confidence_level and confidence_reason are determined for each
Z2 Research Report Node output. Confidence is restricted to three levels only:
LOW, MEDIUM, HIGH_WITH_STRUCTURE_ONLY.

The confidence policy ensures that no_alpha_claim and no_trade_signal are maintained
regardless of confidence level. Even HIGH_WITH_STRUCTURE_ONLY does not imply any
investment recommendation — it only means the structural evidence is complete.

---

## 3. Dependency / Evidence

### 3.1 Confidence Levels (Exhaustive)

| Level | Meaning | Conditions |
|-------|---------|------------|
| LOW | Insufficient evidence for meaningful interpretation | Missing >30% of evidence chain fields, OR degradation active, OR B1 source incomplete |
| MEDIUM | Partial evidence supports structural interpretation | All mandatory evidence present, some optional gaps, no degradation blocking |
| HIGH_WITH_STRUCTURE_ONLY | Complete structural evidence available | All evidence chain fields present, no degradation, all sections populated, z2_report_node_hash valid |

### 3.2 Confidence Assignment Rules

1. Start at HIGH_WITH_STRUCTURE_ONLY
2. Degrade to MEDIUM if:
   - Any optional evidence field is missing
   - FactorEvaluationMatrix not available (future dependency)
   - Small Real Sample summary not available (future dependency)
   - Any section has degraded content
3. Degrade to LOW if:
   - Any mandatory evidence chain field is missing
   - Degradation status is DENY_* (any deny variant)
   - B1 CompositionGraphResponse validation fails
   - rollback_marker is TRUE
   - permission_tier is insufficient

### 3.3 Confidence Reason Generation

confidence_reason must be a human-readable string explaining:
- Which evidence was present/absent
- Which degradation rules were triggered
- Why the assigned level was chosen over adjacent levels

Example: "MEDIUM: All mandatory B1 evidence present. Optional FactorEvaluationMatrix not yet available. No degradation blocking. Structure complete but optional context missing."

---

## 4. Boundary

- Confidence level MUST be one of exactly three values: LOW, MEDIUM, HIGH_WITH_STRUCTURE_ONLY
- No other confidence values are permitted
- HIGH_WITH_STRUCTURE_ONLY does NOT mean "high confidence in investment outcome"
- HIGH_WITH_STRUCTURE_ONLY means ONLY "structural evidence is complete"
- Confidence NEVER implies trade recommendation regardless of level
- no_alpha_claim = true at ALL confidence levels
- no_trade_signal = true at ALL confidence levels

---

## 5. Forbidden Actions

- Assigning confidence levels outside {LOW, MEDIUM, HIGH_WITH_STRUCTURE_ONLY}
- Implying investment confidence through confidence_level naming
- Using confidence_level to suggest trade actions
- Assigning HIGH_WITH_STRUCTURE_ONLY when any evidence is missing
- Omitting confidence_reason from output
- Using confidence as input to any trading decision system
- Propagating confidence to z9_review_snapshot_candidate as trade signal

---

## 6. Proof / Review Requirements

- Test each confidence level assignment with fixture data triggering that level
- Test boundary conditions between LOW/MEDIUM and MEDIUM/HIGH_WITH_STRUCTURE_ONLY
- Verify confidence_reason contains substantive explanation (not empty/placeholder)
- Verify z2_report_node_hash includes confidence_level in computation
- Verify z9_review_snapshot_candidate contains confidence_level correctly

---

## 7. Next Legal Entry

- Proceed to BLOCKED_OUTPUT_POLICY.md for output blocking rules
- Confidence feeds into z9_review_snapshot_candidate (Z9_HANDOFF_PREP.md)
- Confidence validation is part of REVIEW_CHECKLIST.md
