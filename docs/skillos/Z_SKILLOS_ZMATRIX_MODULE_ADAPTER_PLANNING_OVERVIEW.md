# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — OVERVIEW

> Status: _OVERVIEW_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED

## 1. Status
Phase: Wave 0 — Pre-Implementation Planning | Priority: P0


## 2. Scope

The Z-MATRIX Module Adapter is a SkillOS-compatible interface layer wrapping all Z-MATRIX-OS v2.9.5 modules into standardized, capability-registered, permission-gated, evidence-contracted adapters. This package defines 26 documents: 14 planning, 7 review, 5 merge covering 19 modules across Waves A (read-only), B (research), and C (future).

Wave A modules are read-only or output-only (filesystem writes only, no state mutation). Wave B modules perform computation/analysis but are read-only to Z-MATRIX state. Wave C modules are future and not planned in this package.

## 3. Evidence / Dependency

Upstream: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED (permission tiers, readonly policy, execution sandbox), Z-MATRIX-OS v2.9.5 (B/D/R Matrix, Flow A RC, TruthGate, EventStore), AGENTS.md (engineering constitution), SOUL.md (Z2 constraints).

## 4. Boundary

In scope: adapter interface design, permission tier assignment, readonly policy, I/O schemas, evidence contracts, forbidden actions, test strategy, rollback.
Out of scope: implementation code, imports, function calls, real trade, broker integration, production deployment.

## 5. Forbidden Actions

F-01 Writing implementation code | F-02 Importing Z-MATRIX modules | F-03 Calling Z-MATRIX functions | F-04 Modifying Z-MATRIX source | F-05 Real trade/broker | F-06 Generating .py/.rs/.ts | F-07 pip install | F-08 Executables | F-09 External APIs | F-10 Production configs. All S1/S2 severity.

## 6. Proof / Requirements

R-01: 26 docs with correct naming | R-02: Planning >=30 lines | R-03: Review >=35 lines | R-04: Merge >=30 lines | R-05: 7-section structure | R-06: FUTURE_PLAN_ONLY + Level 5 BLOCKED | R-07: WAVE0 reference | R-08: Wave A/B/C priority | R-09: Committed to correct branch | R-10: Pushed to remote

## 7. Next

SCOPE.md → CAPABILITY_MAP.md → CONTRACT_STANDARD.md → PERMISSION_TIER_PLAN.md → READONLY_POLICY_PLAN.md → INPUT_OUTPUT_SCHEMA_PLAN.md → EVIDENCE_CONTRACT_PLAN.md → MODULE_PRIORITY_PLAN.md → FORBIDDEN_ACTIONS_MATRIX.md → TEST_AND_PROOF_PLAN.md → ROLLBACK_PLAN.md → PLANNING_CLOSEOUT.md → PLANNING_SEAL.md

**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-OVERVIEW-v1.0
