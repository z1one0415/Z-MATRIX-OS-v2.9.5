# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — MERGE CHECKLIST

> Status: _MERGE_CHECKLIST_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED
> Checks: 15 required | Checked By: HUMAN APPROVER (PENDING) | Checked Date: PENDING

## 1. Status
Phase: Wave 0 — Merge Review Phase | Priority: P0
Checklist: 15 checks across 4 categories | All checks PENDING human approver
Hardened: 2026-06-08

## 2. Scope

This checklist is the mandatory verification tool for merge review. All 15 checks must be completed and marked PASS/FAIL before merge can proceed. Checks cover git integrity, document completeness, constraint compliance, and evidence integrity.

MERGE CHECKLIST — 15 CHECKS FOR HUMAN APPROVER:

Category A: Git Integrity (Checks M01-M04)
- [ ] M01 — Branch Clean: `git status` shows no uncommitted changes, no untracked files outside docs/skillos/. Output must be clean or docs-only. ___
- [ ] M02 — Base Commit Verified: HEAD ancestry traceable to c7c4ac9. `git merge-base --is-ancestor c7c4ac9 HEAD` returns 0. ___
- [ ] M03 — No Force-Push: Branch history is linear from c7c4ac9. `git log --oneline` shows no rewritten history. ___
- [ ] M04 — Target Branch: Merging to correct integration branch. Target branch confirmed as intended destination. ___

Category B: Document Completeness (Checks M05-M08)
- [ ] M05 — 26 Docs Present: All 26 files exist with correct naming. `ls -1 Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING_*.md | wc -l` = 26. ___
- [ ] M06 — Planning Depth: All 14 planning docs >=30 lines. Verify with `wc -l`. No planning doc < 30 lines. ___
- [ ] M07 — Review Depth: All 7 review docs >=35 lines. Verify with `wc -l`. No review doc < 35 lines. ___
- [ ] M08 — Merge Depth: All 5 merge docs >=30 lines. Verify with `wc -l`. No merge doc < 30 lines. ___

Category C: Constraint Compliance (Checks M09-M12)
- [ ] M09 — 26 Docs-Only: No code files in the merge. `git diff --stat c7c4ac9..HEAD` shows only .md files. Zero .py/.rs/.ts/.js/.sh/.java/.go. ___
- [ ] M10 — FUTURE_PLAN_ONLY: All 26 docs contain "FUTURE_PLAN_ONLY". `grep -L "FUTURE_PLAN_ONLY" Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING_*.md` returns empty. ___
- [ ] M11 — Level 5 BLOCKED: All 26 docs contain "Level 5 BLOCKED". `grep -L "Level 5 BLOCKED" Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING_*.md` returns empty. ___
- [ ] M12 — No Implementation: Zero import/call/execute claims. `grep -r "import zmatrix\|from zmatrix\|execute\|implement" Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING_*.md` reviewed manually — no authoritative execution claims. ___

Category D: Evidence Integrity (Checks M13-M15)
- [ ] M13 — Seals Unchanged: PLANNING_SEAL shows _PLANNING_SEALED. REVIEW_CLOSEOUT shows _REVIEW_READY_FOR_HUMAN_DECISION. MERGE_CLOSEOUT shows _MERGE_REVIEW_READY_FOR_HUMAN_DECISION. Verify status markers in each. ___
- [ ] M14 — Decision Record Populated: REVIEW_DECISION_RECORD has all 10 fields populated (no PENDING values). Decision is GO_FOR_MERGE_REVIEW or CONDITIONAL_GO (conditions met). ___
- [ ] M15 — Risks Registered: MERGE_RISK_REGISTER has >=10 risks with severity/likelihood/mitigation. All risks evaluated and accepted/mitigated. ___

## 3. Evidence / Dependency

Checklist completion evidence: Each check marked PASS/FAIL with approver initials and date. All FAIL items require documented reason and remediation. PASS items require verification trace.

Merge evidence: After all 15 checks complete, approver signs with: approver_name, approver_role, approval_date, merge_decision (APPROVE/CONDITIONAL/REJECT). Checklist evidence committed as part of merge.

## 4. Boundary

Checklist scope: 15 mandatory checks across 4 categories. Covers merge safety, git integrity, document completeness, and evidence verification.
Checklist does NOT: Authorize implementation, validate adapter functionality, test Z-MATRIX integration, predict post-merge behavior.

## 5. Forbidden Actions

F-MC01 Skipping checklist items (CRITICAL) | F-MC02 Marking PASS without verification (HIGH) | F-MC03 Merging without all 15 checks completed (CRITICAL) | F-MC04 Auto-filling checklist (CRITICAL) | F-MC05 Modifying checklist mid-merge-review (MEDIUM) | F-MC06 Checklist claiming to validate code (CRITICAL) | F-MC07 FAIL item without remediation (MEDIUM) | F-MC08 Merge evidence not committed (MEDIUM) | F-MC09 CHECKLIST bypassing merge review gate (CRITICAL) | F-MC10 Checklist authorizing implementation (CRITICAL) | F-MC11 Unverified PASS on depth check (HIGH) | F-MC12 Merge with modified planning docs (HIGH) | F-MC13 Checklist with fewer than 15 checks (MEDIUM) | F-MC14 Non-human checklist completion (CRITICAL) | F-MC15 Checklist applied to non-merge artifacts (MEDIUM) | F-MC16 Approve merge with known violation (CRITICAL) | F-MC17 Checklist signed without review evidence (MEDIUM) | F-MC18 Merge checklist pretending review is optional (MEDIUM)

## 6. Proof / Requirements

R-MC01: 15 checks enumerated across 4 categories | R-MC02: Each check has verification method specified | R-MC03: PASS/FAIL marking with approver identification | R-MC04: Merge evidence requirement documented | R-MC05: Forbidden actions >=18 | R-MC06: All 26 docs covered by checklist | R-MC07: HUMAN APPROVER requirement explicit | R-MC08: No auto-fill allowed | R-MC09: Category structure clear (A-D) | R-MC10: Remediation required for FAIL items

## 7. Next

MERGE_RISK_REGISTER.md → MERGE_DECISION_BRIEF.md → MERGE_CLOSEOUT.md


**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-MERGE_CHECKLIST-v1.1
