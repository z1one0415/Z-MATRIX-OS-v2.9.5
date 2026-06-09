# Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING — REVIEW_DECISION_BRIEF

> Decision brief for human reviewer — Z2 Research Report Node planning.
> Branch: plan/skillos-z2-research-report-node-planning
> Base commit: 74c27fa

---

## 1. Status

| Field | Value |
|-------|-------|
| Document | REVIEW_DECISION_BRIEF |
| Status | REVIEW_IN_PROGRESS |
| Created | 2026-06-09 |
| Parent | REVIEW_RISK_REGISTER.md |
| Dependency | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED (postmerge HEAD = 74c27fa) |
| Decision Required | APPROVE / REJECT / REQUEST_CHANGES |

---

## 2. Scope

This brief summarizes the Z2 Research Report Node planning for human decision-making.

### Executive Summary:
The Z2 Research Report Node is a **readonly explanatory report generator** that:
- Consumes B1 CompositionGraphResponse as its sole structured input
- Produces 12-section structured research reports
- Enforces no_alpha_claim = true (NEVER generates investment advice)
- Enforces no_trade_signal = true (NEVER generates trade signals)
- Produces z9_review_snapshot_candidate for downstream Z9 review
- Defaults to DISABLED_DEFAULT_NOOP (safe by default)
- Computes z2_report_node_hash for full audit trail

### Key Design Decisions:
1. **Input restricted to B1 only** — prevents scope creep and forbidden data access
2. **12 forbidden outputs explicitly blocked** — scanner runs on every emission
3. **3 confidence levels only** — prevents confidence inflation
4. **9 degradation decisions** — graduated response to input quality issues
5. **41 proof categories** — comprehensive test coverage planned

---

## 3. Dependency / Evidence

### Risk Summary for Decision Maker:

| Severity | Count | Key Risks |
|----------|-------|-----------|
| CRITICAL | 5 | Forbidden output leakage, alpha_claim, trade signal, real data, position weight, broker action |
| HIGH | 7 | Non-B1 input, evidence integrity, hash determinism, degradation bypass, default override, forbidden imports, implementation drift |
| MEDIUM | 7 | Z9 forbidden field, confidence inflation, section omission, blocked_outputs_removed, Z9 under DENY, template injection, coverage |
| LOW | 3 | Stale input, hash collision, minor gaps |

### Mitigation Confidence:
- All CRITICAL risks have multiple independent controls
- All HIGH risks have dedicated test coverage planned
- DISABLED_DEFAULT_NOOP ensures safe startup
- Kill switch available for immediate disable

### Dependencies Verified:
- B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED confirmed merged at 74c27fa
- B1 CompositionGraphResponse contract stable
- No new external dependencies introduced

---

## 4. Boundary

- Decision affects planning approval only (not implementation)
- Implementation cannot begin until MERGE phase completes
- APPROVE allows progression to MERGE_REVIEW.md
- REJECT returns to planning with specific feedback
- REQUEST_CHANGES allows targeted modifications (requires re-seal)

---

## 5. Forbidden Actions

- Auto-approving without reading this brief
- Approving with unaddressed CRITICAL risks
- Proceeding to implementation without merge phase
- Modifying the decision brief after decision is recorded
- Reducing risk severity without justification

---

## 6. Proof / Review Requirements

- Human must read REVIEW_CHECKLIST.md (36 checks)
- Human must review REVIEW_RISK_REGISTER.md (22 risks)
- Decision recorded in REVIEW_DECISION_RECORD.md
- z9_review_snapshot_candidate design reviewed for completeness
- no_alpha_claim and no_trade_signal invariants confirmed understood

---

## 7. Next Legal Entry

- Record decision in REVIEW_DECISION_RECORD.md
- If APPROVED: proceed to REVIEW_MERGE_READINESS.md
- If REJECTED: document reasons, return to planning
- If REQUEST_CHANGES: document required changes, re-seal after modification
