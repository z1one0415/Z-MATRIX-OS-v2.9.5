# Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING — REVIEW_CHECKLIST

> Review checklist with ≥34 verification checks for Z2 Research Report Node.
> Branch: plan/skillos-z2-research-report-node-planning
> Base commit: 74c27fa

---

## 1. Status

| Field | Value |
|-------|-------|
| Document | REVIEW_CHECKLIST |
| Status | REVIEW_IN_PROGRESS |
| Created | 2026-06-09 |
| Parent | REVIEW_GATE.md |
| Dependency | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED (postmerge HEAD = 74c27fa) |

---

## 2. Scope

This checklist contains 36 verification checks that must ALL pass before the Z2 Research
Report Node planning can proceed to merge. Each check validates a specific aspect of the
sealed planning documents.

---

## 3. Dependency / Evidence

### Verification Checks (36 items)

| # | Check | Category | Verified |
|---|-------|----------|----------|
| 1 | All 14 planning documents exist | Completeness | ☐ |
| 2 | All planning documents ≥50 lines | Depth | ☐ |
| 3 | All documents have 7-section structure | Structure | ☐ |
| 4 | SEAL.md shows Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING_SEALED | Status | ☐ |
| 5 | CLOSEOUT.md shows READY_FOR_REVIEW | Status | ☐ |
| 6 | B1 CompositionGraphResponse is sole structured input | Input Contract | ☐ |
| 7 | no_alpha_claim = true documented as invariant | Safety | ☐ |
| 8 | no_trade_signal = true documented as invariant | Safety | ☐ |
| 9 | z2_report_node_hash computation defined | Integrity | ☐ |
| 10 | z9_review_snapshot_candidate structure complete | Z9 Handoff | ☐ |
| 11 | 74c27fa referenced as base commit | Traceability | ☐ |
| 12 | All 8 permitted inputs enumerated | Input Contract | ☐ |
| 13 | All 22 permitted outputs enumerated | Output Contract | ☐ |
| 14 | All 12 forbidden outputs enumerated | Output Contract | ☐ |
| 15 | All 12 report sections defined with metadata | Schema | ☐ |
| 16 | All 14 inherited evidence chain fields listed | Evidence | ☐ |
| 17 | All 3 Z2-generated hash fields defined | Evidence | ☐ |
| 18 | Confidence restricted to LOW/MEDIUM/HIGH_WITH_STRUCTURE_ONLY | Confidence | ☐ |
| 19 | Confidence assignment rules documented | Confidence | ☐ |
| 20 | Blocked output scanner pipeline defined | Safety | ☐ |
| 21 | All 9 degradation decisions enumerated | Degradation | ☐ |
| 22 | Degradation priority order defined | Degradation | ☐ |
| 23 | DISABLED_DEFAULT_NOOP is default state | Safety | ☐ |
| 24 | Z9 handoff has 14 allowed fields | Z9 Handoff | ☐ |
| 25 | Z9 handoff has 7 forbidden fields | Z9 Handoff | ☐ |
| 26 | 41 proof categories enumerated in TEST_AND_PROOF_PLAN | Testing | ☐ |
| 27 | Future code files listed (12 modules) | Planning | ☐ |
| 28 | Future test files listed (9 test modules) | Planning | ☐ |
| 29 | No direct access to research/factor_library files | Boundary | ☐ |
| 30 | No access to broker/production systems | Boundary | ☐ |
| 31 | No access to Z8/Z9/V3 runtime | Boundary | ☐ |
| 32 | readonly_only = true invariant documented | Safety | ☐ |
| 33 | Evidence chain hash propagation rules complete | Integrity | ☐ |
| 34 | Forbidden imports policy defined | Safety | ☐ |
| 35 | Report sections each track blocked_outputs_removed | Safety | ☐ |
| 36 | Snapshot generation gated by ALLOW decisions only | Z9 Handoff | ☐ |

---

## 4. Boundary

- ALL 36 checks must pass for review approval
- Any single FAILED check blocks merge progression
- Checks are binary: PASS or FAIL (no partial credit)
- Checker must verify against actual document content, not assumptions
- B1 CompositionGraphResponse dependency verified against sealed docs

---

## 5. Forbidden Actions

- Marking checks as passed without verification
- Removing checks from the list
- Adding exceptions or waivers
- Proceeding to merge with any check FAILED
- Delegating verification to automated tools without human confirmation
- Modifying sealed documents to pass checks

---

## 6. Proof / Review Requirements

- Each check must be independently verifiable by reading the referenced document
- Failed checks must have documented reason
- All checks relate to safety, completeness, or correctness of the Z2 node planning
- z9_review_snapshot_candidate checks verify both allowed and forbidden fields
- no_alpha_claim and no_trade_signal checks verify presence in multiple documents

---

## 7. Next Legal Entry

- After checklist: proceed to REVIEW_RISK_REGISTER.md
- Failed checks: document in REVIEW_DECISION_BRIEF.md for human review
- All passed: proceed to REVIEW_MERGE_READINESS.md assessment
