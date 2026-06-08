# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — OVERVIEW

> Status: _OVERVIEW_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED

## 1. Status
Phase: Wave 0 — Pre-Implementation Planning | Priority: P0
Artifacts: 26 documents (14 planning + 7 review + 5 merge)
Hardened: 2026-06-08 | All docs docs-only, no code, no imports, no calls
State Machine: PLANNING → REVIEW → MERGE_REVIEW → HUMAN_DECISION

## 2. Scope

The Z-MATRIX Module Adapter is a SkillOS-compatible interface layer wrapping all Z-MATRIX-OS v2.9.5 modules into standardized, capability-registered, permission-gated, evidence-contracted adapters. This package defines 26 documents: 14 planning, 7 review, 5 merge covering 19 modules across Waves A (read-only), B (research), and C (future).

Wave A modules are read-only or output-only (filesystem writes only, no state mutation). Wave B modules perform computation/analysis but are read-only to Z-MATRIX state. Wave C modules are future and not planned in this package.

Module Capability Map (19 modules across 3 waves):
- Wave A (7): Z9 Memory Bridge (read-only memory), Z2 Research Output Reader (read-only output), Local Report Generator (output-only to local fs), Document Generator (output-only), Capability Registry (meta, T0), TruthGate (read-only validation), EventStore (output-only local write)
- Wave B (7): Z2 Chain Research Engine (read-only research), Z2 Scoring Engine (read-only scoring), Z8 Execution Plan Generator (read-only plan gen), V3 Survival Sandbox (read-only simulation), B-Matrix v2.1.1 (read-only scan), D-Matrix v2.2 (read-only scan), R-Matrix v1.1 (read-only scan), Flow A RC 16-Node (read-only pipeline)
- Wave C (4): Portfolio Manager (future), Broker Adapter (future), Production Deployer (future), Real Trade Engine (future)

## 3. Evidence / Dependency

Upstream: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED (permission tiers, readonly policy, execution sandbox), Z-MATRIX-OS v2.9.5 (B/D/R Matrix, Flow A RC, TruthGate, EventStore), AGENTS.md (engineering constitution), SOUL.md (Z2 constraints).

Evidence contract requirements: request hash, response hash placeholder, decision hash, module adapter id, source class, permission tier, graph edge id, no hidden writes. All evidence blocks are 8-field minimum.

## 4. Boundary

In scope: adapter interface design, permission tier assignment, readonly policy, I/O schemas, evidence contracts, forbidden actions, test strategy, rollback.
Out of scope: implementation code, imports, function calls, real trade, broker integration, production deployment.

Absolute constraints: No import of any Z-MATRIX module, no call to any Z-MATRIX function, no execution of any code, no writes to Z-MATRIX state, no persistence beyond local filesystem docs, no hidden network connections. These constraints apply FOREVER within this planning package.

## 5. Forbidden Actions

F-01 Writing implementation code (CRITICAL) | F-02 Importing Z-MATRIX modules (CRITICAL) | F-03 Calling Z-MATRIX functions (CRITICAL) | F-04 Modifying Z-MATRIX source (CRITICAL) | F-05 Real trade/broker (CRITICAL) | F-06 Generating .py/.rs/.ts (CRITICAL) | F-07 pip install (HIGH) | F-08 Executables (HIGH) | F-09 External APIs (HIGH) | F-10 Production configs (CRITICAL) | F-11 Hidden writes (CRITICAL) | F-12 Unregistered execution (CRITICAL) | F-13 Permission bypass (CRITICAL) | F-14 State mutation outside Wave C (CRITICAL) | F-15 Self-promotion of permission tier (CRITICAL) | F-16 Undeclared dependency (HIGH) | F-17 Non-docs file addition (MEDIUM) | F-18 Capability registry runtime modification (HIGH)

## 6. Proof / Requirements

R-01: 26 docs with correct naming | R-02: Planning >=30 lines each | R-03: Review >=35 lines each | R-04: Merge >=30 lines each | R-05: 7-section structure throughout | R-06: FUTURE_PLAN_ONLY + Level 5 BLOCKED on every doc | R-07: WAVE0 reference on every doc | R-08: Wave A/B/C priority explicit | R-09: Committed to correct branch | R-10: Pushed to remote | R-11: Forbidden >=18 actions | R-12: Test & Proof >=18 categories | R-13: Review Checklist >=18 checks | R-14: Merge Checklist >=15 checks | R-15: Review Risk Register >=12 risks | R-16: Merge Risk Register >=10 risks | R-17: PLANNING_SEALED status set | R-18: PLANNING_READY_FOR_REVIEW status set

## 7. Next

SCOPE.md → CAPABILITY_MAP.md → CONTRACT_STANDARD.md → PERMISSION_TIER_PLAN.md → READONLY_POLICY_PLAN.md → INPUT_OUTPUT_SCHEMA_PLAN.md → EVIDENCE_CONTRACT_PLAN.md → MODULE_PRIORITY_PLAN.md → FORBIDDEN_ACTIONS_MATRIX.md → TEST_AND_PROOF_PLAN.md → ROLLBACK_PLAN.md → PLANNING_CLOSEOUT.md → PLANNING_SEAL.md

**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-OVERVIEW-v1.1
