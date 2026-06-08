# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — FORBIDDEN_ACTIONS_MATRIX

> Status: _FORBIDDEN_ACTIONS_MATRIX_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED

## 1. Status
Phase: Wave 0 — Pre-Implementation Planning | Priority: P0 | Forbidden: 18 actions, 5 categories
Hardened: 2026-06-08

## 2. Scope

This is the definitive, non-negotiable list of FOREVER FORBIDDEN actions within this planning package.

Category 1 — Implementation Creep: FA01 Writing adapter code (.py/.rs/.ts/.js/.sh) [CRITICAL] | FA02 Importing Z-MATRIX modules [CRITICAL] | FA03 Adding runtime dependencies [HIGH] | FA04 Executable test scripts [HIGH] | FA05 Creating adapter files [CRITICAL].

Category 2 — Permission Violation: FA06 Adapter executing without permission gate [CRITICAL] | FA07 Self-promoting tier [CRITICAL] | FA08 Wave A/B invoking Wave C [CRITICAL] | FA09 Non-T0 modifying registry [CRITICAL].

Category 3 — State Mutation: FA10 Wave A/B writing to Z-MATRIX state [CRITICAL] | FA11 Wave A/B emitting trade signals [CRITICAL] | FA12 Wave A/B modifying portfolio [CRITICAL] | FA13 Wave A/B modifying config [HIGH].

Category 4 — Evidence Tampering: FA14 Adapter without evidence block [HIGH] | FA15 Fake hash in evidence [CRITICAL] | FA16 Post-generation evidence modification [CRITICAL].

Category 5 — Documentation Integrity: FA17 Documentation claiming implementation readiness [HIGH] | FA18 Documentation claiming execution authority [CRITICAL].

Detection mechanisms (5): DM1 Grep audit (import/call/execute keywords) | DM2 File extension check (.py/.rs/.ts/.js/.sh) | DM3 Contract cross-reference | DM4 Hash chain verification | DM5 Side effect audit.

Violation handling: CRITICAL → Revert commit, block merge. HIGH → Remove violation, re-review. MEDIUM → Document exception, must fix.

## 3. Evidence / Dependency

Matrix applies to ALL 26 docs. No exemption. Every planning/review/merge document must comply with all 18 forbidden actions.

## 4. Boundary

In scope: All 26 docs, all phases, all modules Waves A/B/C. Out: Documents outside this package, implementation-phase artifacts, runtime enforcement.

## 5. Forbidden Actions

F-FA01 Adapter implementation code (CRITICAL) | F-FA02 Import Z-MATRIX (CRITICAL) | F-FA03 Runtime deps (HIGH) | F-FA04 Executable tests (HIGH) | F-FA05 Adapter files (CRITICAL) | F-FA06 Permission bypass (CRITICAL) | F-FA07 Self-promote tier (CRITICAL) | F-FA08 Cross-wave call (CRITICAL) | F-FA09 Registry mutation non-T0 (CRITICAL) | F-FA10 State mutation Wave A/B (CRITICAL) | F-FA11 Trade signals Wave A/B (CRITICAL) | F-FA12 Portfolio mutation Wave A/B (CRITICAL) | F-FA13 Runtime config mutation (HIGH) | F-FA14 Missing evidence block (HIGH) | F-FA15 Fake hash (CRITICAL) | F-FA16 Post-gen evidence tamper (CRITICAL) | F-FA17 Doc claiming impl readiness (HIGH) | F-FA18 Doc claiming exec authority (CRITICAL)

## 6. Proof / Requirements

R-FA01: 18 forbidden actions | R-FA02: 5 categories | R-FA03: 3 severity levels | R-FA04: 5 detection mechanisms | R-FA05: Violation handling matrix | R-FA06: All 26 docs subject | R-FA07: No exemption clause | R-FA08: Detection testable via grep | R-FA09: CRITICAL for all impl creep | R-FA10: Category 5 covers doc integrity

## 7. Next

TEST_AND_PROOF_PLAN.md → ROLLBACK_PLAN.md → PLANNING_CLOSEOUT.md → PLANNING_SEAL.md

**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-FORBIDDEN_ACTIONS_MATRIX-v1.1
