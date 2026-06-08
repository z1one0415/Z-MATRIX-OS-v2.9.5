# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — REVIEW CHECKLIST

> Status: _REVIEW_CHECKLIST_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Checks: 18 required | Checked By: HUMAN REVIEWER (PENDING)

## 1. Status
Phase: Wave 0 — Review Phase | Priority: P0 | 18 checks across 5 categories
Hardened: 2026-06-08

## 2. Scope

18 mandatory checks for human reviewer:

Cat A — Structural Completeness (C01-C04):
- [ ] C01 File Count: 26 docs exist. `ls | wc -l` = 26. ___
- [ ] C02 Planning Depth: 14 planning >=30 lines. `wc -l` per planning doc. ___
- [ ] C03 Review Depth: 7 review >=35 lines. `wc -l` per review doc. ___
- [ ] C04 Merge Depth: 5 merge >=30 lines. `wc -l` per merge doc. ___

Cat B — Constraint Compliance (C05-C08):
- [ ] C05 Level 5 BLOCKED: All docs. `grep -L "Level 5 BLOCKED"`. Output empty. ___
- [ ] C06 FUTURE_PLAN_ONLY: All docs. `grep -L "FUTURE_PLAN_ONLY"`. Output empty. ___
- [ ] C07 WAVE0 Dep: All docs. `grep -L "WAVE0_CONTROLLED"`. Output empty. ___
- [ ] C08 No Code: Zero .py/.rs/.ts/.js/.sh. `find -name "*.py"`. Output empty. ___

Cat C — Content Quality (C09-C12):
- [ ] C09 Seven-Section: All 26 have ## 1-7. `grep -c "^## [1-7]\."` per file = 7. ___
- [ ] C10 Forbidden >=18: Count F-FA entries in FORBIDDEN_ACTIONS_MATRIX. ___
- [ ] C11 Risks: Review >=12, Merge >=10. Count table rows. ___
- [ ] C12 Proof Categories: TEST_AND_PROOF >=18 PC entries. ___

Cat D — Evidence Integrity (C13-C15):
- [ ] C13 Status Markers: _PLANNING_SEALED, _PLANNING_READY_FOR_REVIEW, _MERGE_REVIEW_READY_FOR_HUMAN_DECISION. ___
- [ ] C14 Decision PENDING: 10 PENDING fields in REVIEW_DECISION_RECORD. ___
- [ ] C15 Evidence Fields: 8 evidence fields in EVIDENCE_CONTRACT_PLAN. ___

Cat E — Risk and Safety (C16-C18):
- [ ] C16 Risk Columns: All risks have Sev/Lik/Mitigation. Manual inspection. ___
- [ ] C17 No Exec Auth: No doc claims authorize execute/implement/deploy. `grep`. ___
- [ ] C18 Tier Correct: Wave A=T0/T1/T2, B=T3/T4, C=T5/T6/T7. Cross-ref. ___

## 3. Evidence / Dependency

Each check PASS/FAIL with reviewer initials and date. FAIL items require remediation plan. Review evidence committed.

## 4. Boundary

18 checks, 5 categories, 26 docs. Does NOT authorize implementation, test adapters, access Z-MATRIX.

## 5. Forbidden Actions

F-RC01 Skip checks (CRITICAL) | F-RC02 PASS without verification (HIGH) | F-RC03 Review not all 18 (MEDIUM) | F-RC04 Auto-fill by AI (CRITICAL) | F-RC05 Modify mid-review (MEDIUM) | F-RC06 Claim validate code (CRITICAL) | F-RC07 No reviewer ID (MEDIUM) | F-RC08 FAIL no remediation (MEDIUM) | F-RC09 No evidence commit (MEDIUM) | F-RC10 Bypass review gate (CRITICAL) | F-RC11 Authorize merge direct (CRITICAL) | F-RC12 Unverified PASS depth (HIGH) | F-RC13 Sealed docs modified (HIGH) | F-RC14 Non-planning docs (MEDIUM) | F-RC15 Claim adapter capabilities exist (CRITICAL) | F-RC16 <18 checks (MEDIUM) | F-RC17 No PC verification (MEDIUM) | F-RC18 Non-human sign (CRITICAL)

## 6. Proof / Requirements

R-RC01: 18 checks 5 categories | R-RC02: Each with verification | R-RC03: PASS/FAIL with ID | R-RC04: Evidence requirement | R-RC05: Forbidden >=18 | R-RC06: All 26 covered | R-RC07: HUMAN REVIEWER explicit | R-RC08: No auto-fill | R-RC09: Category structure A-E | R-RC10: Remediation for FAIL

## 7. Next

REVIEW_RISK_REGISTER.md → REVIEW_DECISION_BRIEF.md → REVIEW_DECISION_RECORD.md → REVIEW_MERGE_READINESS.md → REVIEW_CLOSEOUT.md

**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-REVIEW_CHECKLIST-v1.1
