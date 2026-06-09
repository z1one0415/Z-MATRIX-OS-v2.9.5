# Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING — MERGE_CHECKLIST

> Merge checklist with ≥28 verification checks for Z2 Research Report Node.
> Branch: plan/skillos-z2-research-report-node-planning
> Base commit: 74c27fa

---

## 1. Status

| Field | Value |
|-------|-------|
| Document | MERGE_CHECKLIST |
| Status | MERGE_REVIEW_IN_PROGRESS |
| Created | 2026-06-09 |
| Parent | MERGE_REVIEW.md |
| Dependency | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED (postmerge HEAD = 74c27fa) |

---

## 2. Scope

This checklist contains 30 merge-specific verification checks that must ALL pass before
the Z2 Research Report Node planning merge can be approved. These checks validate
implementation readiness, safety guarantees, and planning completeness.

---

## 3. Dependency / Evidence

### Merge Verification Checks (30 items)

| # | Check | Category | Verified |
|---|-------|----------|----------|
| 1 | Planning phase: all 14 docs exist | Completeness | ☐ |
| 2 | Review phase: all 7 docs exist | Completeness | ☐ |
| 3 | Merge phase: all 5 docs exist | Completeness | ☐ |
| 4 | Total: 26 documents present | Completeness | ☐ |
| 5 | SEAL status confirmed | Planning | ☐ |
| 6 | B1 CompositionGraphResponse sole input documented | Input | ☐ |
| 7 | no_alpha_claim = true invariant present across docs | Safety | ☐ |
| 8 | no_trade_signal = true invariant present across docs | Safety | ☐ |
| 9 | z2_report_node_hash computation specified | Integrity | ☐ |
| 10 | z9_review_snapshot_candidate structure complete | Z9 | ☐ |
| 11 | 74c27fa referenced as base commit | Traceability | ☐ |
| 12 | 12 forbidden outputs enumerated | Safety | ☐ |
| 13 | 8 permitted inputs enumerated | Contract | ☐ |
| 14 | 22 permitted outputs enumerated | Contract | ☐ |
| 15 | 12 report sections defined | Schema | ☐ |
| 16 | 14 inherited evidence fields defined | Evidence | ☐ |
| 17 | 9 degradation decisions defined | Degradation | ☐ |
| 18 | DISABLED_DEFAULT_NOOP is default | Safety | ☐ |
| 19 | 41 proof categories enumerated | Testing | ☐ |
| 20 | REVIEW_RISK_REGISTER has ≥20 risks | Risk | ☐ |
| 21 | MERGE_RISK_REGISTER has ≥18 risks | Risk | ☐ |
| 22 | All CRITICAL risks have rollback triggers | Risk | ☐ |
| 23 | Future code files listed (12 modules) | Planning | ☐ |
| 24 | Future test files listed (9 test modules) | Planning | ☐ |
| 25 | No implementation code in planning branch | Boundary | ☐ |
| 26 | Branch is docs-only | Boundary | ☐ |
| 27 | Confidence restricted to 3 levels | Confidence | ☐ |
| 28 | Blocked output scanner pipeline defined | Safety | ☐ |
| 29 | Z9 handoff: 14 allowed + 7 forbidden fields | Z9 | ☐ |
| 30 | readonly_only = true invariant documented | Safety | ☐ |

---

## 4. Boundary

- ALL 30 checks must pass for merge approval
- Single FAILED check blocks merge
- Checks validate planning completeness, not code quality
- Merge enables implementation permission only
- no_alpha_claim and no_trade_signal are merge-blocking invariants

---

## 5. Forbidden Actions

- Marking checks as passed without verification
- Removing checks from the list
- Merging with any check FAILED
- Adding implementation code to planning branch
- Weakening safety checks for convenience
- Bypassing human approval based on checklist results

---

## 6. Proof / Review Requirements

- Each check independently verifiable by reading referenced documents
- z9_review_snapshot_candidate checks verify full structure
- B1 CompositionGraphResponse dependency confirmed via DEPENDENCY_MAP.md
- z2_report_node_hash specification confirmed via EVIDENCE_CHAIN.md
- All safety invariants confirmed across multiple documents

---

## 7. Next Legal Entry

- After checklist: proceed to MERGE_RISK_REGISTER.md
- Failed checks: document in MERGE_DECISION_BRIEF.md
- All passed: support merge approval in MERGE_CLOSEOUT.md
