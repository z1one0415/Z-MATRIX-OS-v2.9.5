# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — MERGE RISK REGISTER

> Status: _MERGE_RISK_REGISTER_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED
> Risks: 10 enumerated | Severity: C=CRITICAL, H=HIGH, M=MEDIUM, L=LOW | Likelihood: H/M/L

## 1. Status
Phase: Wave 0 — Merge Review Phase | Priority: P0
Register: 10 risks across 4 categories | All risks have severity, likelihood, mitigation
Hardened: 2026-06-08

## 2. Scope

Merge-specific risk register for the Z-MATRIX Module Adapter planning package. These risks are specific to the merge operation itself — they supplement the review risk register (RR1-RR12) with merge-phase risks.

### Merge Risk Register Table

| # | Risk | Category | Sev | Lik | Impact | Mitigation |
|:--|:--|:--|:--:|:--:|:--|:--|
| MR1 | Merge to Wrong Branch | Git | C | L | Planning docs merged to incorrect target branch. WAVE0 or other packages contaminated. Unauthorized docs in main. | Pre-merge verify target: `git branch --show-current`. Confirm target = plan/skillos-zmatrix-module-adapter-planning. |
| MR2 | Force-Push Overwrites History | Git | C | L | Force-push destroys commit history, breaks evidence chain, invalidates seals. Planning evidence trail lost. | No `--force` flag on push. Protected branch rules if available. Backup branch before merge. |
| MR3 | Non-Doc Creep on Merge | Artifact | H | L | Non-documentation files (code, config, scripts) included in merge. Violates docs-only constraint. Implementation artifacts contaminate repo. | `git diff --stat c7c4ac9..HEAD` — verify only .md files. MERGE_CHECKLIST M09. |
| MR4 | Regression of Upstream Docs | Upstream | H | L | Merge overwrites or conflicts with WAVE0 or other upstream documentation. Existing planning packages damaged. | Baseline check: compare merge diff against c7c4ac9. Only new docs/skillos/ files added. |
| MR5 | Concurrent Merge Conflict | Concurrency | M | L | Another developer merges to same target simultaneously. Merge conflict requires manual resolution, risking doc corruption. | Sequential merge policy. Coordinate merge window. Resolve conflicts preserving both sides' integrity. |
| MR6 | Docs Stale After Review | Freshness | M | M | Time elapsed between review and merge. Docs become stale relative to upstream changes. Evidence references outdated. | Commit SHA in seal documents. Re-verify PC01-PC18 immediately before merge. |
| MR7 | Merge Commit Message Unclear | Audit | L | L | Merge commit message insufficiently descriptive. Future auditors cannot determine what was merged or why. | Standard merge template: "merge: SkillOS Z-MATRIX Module Adapter Planning (26 docs, FUTURE_PLAN_ONLY, Level 5 BLOCKED)". |
| MR8 | Implementation Creep Post-Merge | Boundary | C | L | After merge, docs are misinterpreted as implementation authorization. Downstream developers begin implementing adapters. | FUTURE_PLAN_ONLY on every doc. Level 5 BLOCKED on every doc. FORBIDDEN_ACTIONS_MATRIX. No authorized enablement. |
| MR9 | Seal Chain Broken | Evidence | H | L | Merge process breaks seal chain. PLANNING_SEAL or REVIEW_CLOSEOUT status markers lost or modified. Evidence trail invalidated. | Verify seals post-merge: grep status markers. MERGE_CHECKLIST M13. |
| MR10 | Pre-Review Implementation Authorized | Governance | H | M | Merge review gate bypassed. Planning docs merged without review phase completion. Unreviewed docs enter main branch. | Gate flow: PLANNING_SEALED → REVIEW_GATE → REVIEW_CLOSEOUT → MERGE_REVIEW → MERGE_CLOSEOUT. Sequential enforcement. |

## 3. Evidence / Dependency

Risk severity definitions (same as review register):
- CRITICAL: Violates fundamental constraint. Package or merge invalid if present.
- HIGH: Undermines merge integrity. Could cause major downstream issues.
- MEDIUM: Quality or process concern. Should fix but may not block merge.
- LOW: Minor. Acceptable with documentation.

Mitigation verification: Each mitigation strategy is verified by a corresponding MERGE_CHECKLIST item. MR1→M04, MR2→M03, MR3→M09, MR4→M02, MR5→M01 (clean branch), MR6→sha verification, MR7→template, MR8→M10/M11, MR9→M13, MR10→M14.

## 4. Boundary

Register scope: Merge-phase risks only. Covers git operations, artifact integrity, and post-merge governance.
Register does NOT cover: Planning content risks (covered by REVIEW_RISK_REGISTER), implementation risks (no implementation exists), runtime risks (no runtime exists).

## 5. Forbidden Actions

F-MR1 Merge risk register with fewer than 10 risks (MEDIUM) | F-MR2 Risk without mitigation linked to checklist (MEDIUM) | F-MR3 Register claiming risks are resolved without evidence (MEDIUM) | F-MR4 Critical risk accepted without mitigation (CRITICAL) | F-MR5 Register bypassing merge review gate (HIGH) | F-MR6 Register modified after merge closeout (MEDIUM) | F-MR7 Register claiming to cover implementation risks (MEDIUM) | F-MR8 Risk severity downgraded to bypass merge (MEDIUM) | F-MR9 Register with duplicate risk entries (MEDIUM) | F-MR10 Register with blank impact descriptions (LOW) | F-MR11 Risk accepted without approver review (HIGH) | F-MR12 Register used as merge authorization (CRITICAL) | F-MR13 Register referencing non-existent docs (MEDIUM) | F-MR14 Register implying implementation follows merge (CRITICAL) | F-MR15 Auto-generated risks without human validation (MEDIUM) | F-MR16 Register without severity/likelihood definitions (MEDIUM) | F-MR17 Register without checklist cross-reference (MEDIUM) | F-MR18 Register claiming post-merge execution readiness (CRITICAL)

## 6. Proof / Requirements

R-MR01: 10 risks enumerated with unique IDs (MR1-MR10) | R-MR02: All risks have severity (C/H/M/L) assigned | R-MR03: All risks have likelihood (H/M/L) assigned | R-MR04: All risks have mitigation strategy | R-MR05: All risks have impact description | R-MR06: Mitigation→Checklist cross-reference provided | R-MR07: Severity/likelihood definitions documented | R-MR08: Forbidden actions >=18 | R-MR09: 4 risk categories used | R-MR10: Boundary clear (merge-phase only)

## 7. Next

MERGE_DECISION_BRIEF.md → MERGE_CLOSEOUT.md


**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-MERGE_RISK_REGISTER-v1.1
