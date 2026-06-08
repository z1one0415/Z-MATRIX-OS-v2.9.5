# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — SCOPE

> Status: _SCOPE_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED

## 1. Status
Phase: Wave 0 — Pre-Implementation Planning | Priority: P0


## 2. Scope

19 Z-MATRIX-OS v2.9.5 modules organized into 3 waves.

Wave A (7 modules, Read-only + Output): Z9 Memory Bridge, Z2 Research Output Reader, Local Report Generator, Document Generator, Capability Registry, TruthGate, EventStore.

Wave B (7 modules, Research + Scoring): Z2 Chain Research Engine, Z2 Scoring Engine, Z8 Execution Plan Generator, V3 Survival Sandbox, B-Matrix v2.1.1, D-Matrix v2.2, R-Matrix v1.1, Flow A RC 16-Node.

Wave C (4 modules, Future): Portfolio Manager, Broker Adapter, Production Deployer, Real Trade Engine.

Wave A modules are read-only or output-only (filesystem writes only, no state mutation). Wave B modules perform computation/analysis but are read-only to Z-MATRIX state. Wave C modules are future and not planned in this package.

## 3. Evidence / Dependency

Upstream: WAVE0_CONTROLLED_READONLY_EXECUTION_P0, SkillOS Capability Registry, Z-MATRIX-OS v2.9.5 APIs.
In scope: interface design, schema definition, permission mapping, contract specification, proof requirements.
Out of scope: implementation code, actual module wrapping, runtime execution, deployment, real trade.

## 4. Boundary

Inclusions: adapter function signatures, permission tier assignment, read/write classification, evidence contracts, I/O schemas, forbidden actions, test strategy, rollback strategy, review gates.
Exclusions: adapter implementation in any language, importing/calling Z-MATRIX modules, modifying Z-MATRIX source, executable files, external API connections, real trade/broker operations, production configuration.

## 5. Forbidden Actions

F-S01 Implementing adapter code (CRITICAL) | F-S02 Importing zmatrix modules (HIGH) | F-S03 Adding runtime dependencies (HIGH) | F-S04 Executable test scripts (HIGH) | F-S05 .py/.rs/.ts adapter files (CRITICAL) | F-S06 Modifying Z-MATRIX source (CRITICAL) | F-S07 Connecting to production (CRITICAL) | F-S08 Bypassing permission tier (HIGH) | F-S09 State-mutating adapter code (HIGH) | F-S10 Production deployment plans (MEDIUM)

## 6. Proof / Requirements

R-S01: 19 modules with Wave assignment | R-S02: Wave A all read-only/output | R-S03: Wave B research/scoring only | R-S04: Wave C marked future | R-S05: Exclusions documented | R-S06: No implementation code | R-S07: All forbidden actions with severity

## 7. Next

CAPABILITY_MAP.md → CONTRACT_STANDARD.md → PERMISSION_TIER_PLAN.md → READONLY_POLICY_PLAN.md → INPUT_OUTPUT_SCHEMA_PLAN.md → EVIDENCE_CONTRACT_PLAN.md → MODULE_PRIORITY_PLAN.md → FORBIDDEN_ACTIONS_MATRIX.md → TEST_AND_PROOF_PLAN.md → ROLLBACK_PLAN.md → PLANNING_CLOSEOUT.md → PLANNING_SEAL.md

**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-SCOPE-v1.0
