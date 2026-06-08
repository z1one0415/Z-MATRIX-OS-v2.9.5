# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — ROLLBACK_PLAN

> Status: _ROLLBACK_PLAN_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED

## 1. Status
Phase: Wave 0 — Pre-Implementation Planning | Priority: P0 | Rollback: 8 triggers, 6 scenarios
Hardened: 2026-06-08

## 2. Scope

Git-based document rollback (docs-only, no code, no state, no DB).

8 Rollback Triggers: RT1 Forbidden action violation | RT2 Permission tier inconsistency | RT3 Dependency graph cycle | RT4 Evidence hash chain broken | RT5 Review gate rejection | RT6 Merge conflict corruption | RT7 Stale contamination | RT8 Branch divergence.

6 Scenarios: A Single doc error → fix in-place | B Multi-doc inconsistency → fix/revert subset | C CRITICAL forbidden → full branch revert | D Review rejection → leave at reviewable commit | E Merge contamination → reset to pre-merge | F Branch corruption → recreate from origin.

## 3. Evidence / Dependency

Decision authority: Author (Z2) → Scenarios A/B. Reviewer → Scenarios C/D. Author only → E/F (git ops).

Rollback evidence: reason, affected_docs, commit_range, verification_after_rollback.

Safe reversion (8 steps): 1. Identify commit range | 2. Identify affected docs | 3. Choose scenario | 4. Execute rollback | 5. Verify PC01-PC18 | 6. Document in ROLLBACK_LOG | 7. Re-run review gate | 8. Re-seal.

## 4. Boundary

Git operations only. No DB/state/deployment rollback. No Z-MATRIX touched. All artifacts immutable text in git.

## 5. Forbidden Actions

F-RB01 Code rollback no code exists (HIGH) | F-RB02 State rollback no state (MEDIUM) | F-RB03 Undocumented rollback (MEDIUM) | F-RB04 Force-push (CRITICAL) | F-RB05 Bypass review gate (HIGH) | F-RB06 Undocumented reason (MEDIUM) | F-RB07 New forbidden actions introduced (CRITICAL) | F-RB08 Branch delete no backup (HIGH) | F-RB09 Claim execute code (CRITICAL) | F-RB10 Mask error instead of fix (MEDIUM) | F-RB11 Partial rollback inconsistent (HIGH) | F-RB12 No re-verification (MEDIUM) | F-RB13 Auto rollback scripts (CRITICAL) | F-RB14 Modify Z-MATRIX source (CRITICAL) | F-RB15 No commit message (MEDIUM) | F-RB16 Claim implementation fix (HIGH) | F-RB17 Silent no evidence (MEDIUM) | F-RB18 Beyond planning boundary into WAVE0 (CRITICAL)

## 6. Proof / Requirements

R-RB01: 8 triggers | R-RB02: 6 scenarios | R-RB03: Authority documented | R-RB04: 8-step procedure | R-RB05: Git only | R-RB06: Forbidden >=18 | R-RB07: Evidence for rollback | R-RB08: No code/state/DB claims | R-RB09: Scenario→trigger mapping | R-RB10: Re-verification step

## 7. Next

PLANNING_CLOSEOUT.md → PLANNING_SEAL.md

**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-ROLLBACK_PLAN-v1.1
