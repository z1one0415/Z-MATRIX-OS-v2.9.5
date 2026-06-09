# Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING — MERGE_DECISION_BRIEF

> Final decision brief for human merge approval — Z2 Research Report Node.
> Branch: plan/skillos-z2-research-report-node-planning
> Base commit: 74c27fa

---

## 1. Status

| Field | Value |
|-------|-------|
| Document | MERGE_DECISION_BRIEF |
| Status | MERGE_REVIEW_IN_PROGRESS |
| Created | 2026-06-09 |
| Parent | MERGE_RISK_REGISTER.md |
| Dependency | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED (postmerge HEAD = 74c27fa) |
| Decision Required | APPROVE_MERGE / REJECT_MERGE / DEFER_MERGE |

---

## 2. Scope

This brief provides the final summary for the human decision maker to approve, reject,
or defer the merge of Z2 Research Report Node planning documents.

### What Is Being Merged:
- 26 planning/review/merge documents (docs-only, no code)
- Formal specification for the Z2 Research Report Node
- Binding contract for future implementation

### What Is NOT Being Merged:
- No Python code
- No test code
- No configuration changes
- No runtime changes

### Executive Summary:
The Z2 Research Report Node is a **readonly explanatory report generator** that:
- Accepts ONLY B1 CompositionGraphResponse (from merged B1 at 74c27fa)
- Produces 12-section structured research reports
- Maintains no_alpha_claim = true ALWAYS
- Maintains no_trade_signal = true ALWAYS
- Computes z2_report_node_hash for audit integrity
- Produces z9_review_snapshot_candidate for Z9 review
- Defaults to DISABLED_DEFAULT_NOOP (safe by default)
- Has 41 planned proof categories for implementation validation

---

## 3. Dependency / Evidence

### Planning Quality Assessment:

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Completeness | HIGH | 14 planning docs, all ≥50 lines, 7-section structure |
| Safety | HIGH | 5 CRITICAL risks mitigated, kill switch planned, default disabled |
| Traceability | HIGH | Full evidence chain with 17 hash fields |
| Testability | HIGH | 41 proof categories, 9 test files planned |
| Boundary Clarity | HIGH | Exhaustive forbidden input/output lists |
| B1 Dependency | STABLE | Merged at 74c27fa, contract defined |

### Risk Summary:

| Category | Review Phase | Merge Phase | Total |
|----------|-------------|-------------|-------|
| CRITICAL | 5 | 4 | 9 (all mitigated) |
| HIGH | 7 | 5 | 12 (all have plans) |
| MEDIUM | 7 | 7 | 14 (monitoring) |
| LOW | 3 | 4 | 7 (acknowledged) |

### Key Safety Guarantees:
1. **no_alpha_claim** — Enforced at input validation, output scanner, and Z9 handoff
2. **no_trade_signal** — Enforced at input validation, output scanner, and Z9 handoff
3. **DISABLED_DEFAULT_NOOP** — Node does nothing unless explicitly enabled
4. **Kill switch** — Immediate disable path available
5. **Blocked output scanner** — 12 forbidden patterns checked on every emission

---

## 4. Boundary

- APPROVE_MERGE: Planning docs merge; implementation branch may begin
- REJECT_MERGE: Planning docs rejected; requires fundamental redesign
- DEFER_MERGE: Decision postponed; no action permitted until revisited
- Merge is docs-only — no runtime impact
- Implementation requires separate branch and separate approval

---

## 5. Forbidden Actions

- Auto-approving merge without reading this brief
- Merging planning docs and immediately writing code (separate branch required)
- Weakening safety invariants as merge condition
- Reducing proof category count below 41
- Modifying planning docs during merge decision
- Claiming merge approval covers implementation approval

---

## 6. Proof / Review Requirements

- Human must confirm understanding of no_alpha_claim / no_trade_signal invariants
- Human must confirm 74c27fa base commit is correct
- Human must acknowledge implementation will require separate approval
- z9_review_snapshot_candidate design confirmed adequate
- z2_report_node_hash specification confirmed deterministic

---

## 7. Next Legal Entry

- After APPROVE_MERGE: proceed to MERGE_CLOSEOUT.md
- MERGE_CLOSEOUT records: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING_MERGE_REVIEW_READY_FOR_HUMAN_DECISION
- Implementation begins on new branch after merge
