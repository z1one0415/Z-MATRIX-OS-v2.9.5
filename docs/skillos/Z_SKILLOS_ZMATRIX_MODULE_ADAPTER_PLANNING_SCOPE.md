# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — SCOPE

> Status: _SCOPE_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED

## 1. Status
Phase: Wave 0 — Pre-Implementation Planning | Priority: P0
Scope Boundary: docs-only interface design across 3 waves, 19 modules
Hardened: 2026-06-08 | FUTURE_PLAN_ONLY | Level 5 BLOCKED

## 2. Scope

19 Z-MATRIX-OS v2.9.5 modules organized into 3 waves.

Wave A (7 modules, Read-only + Output): Z9 Memory Bridge, Z2 Research Output Reader, Local Report Generator, Document Generator, Capability Registry, TruthGate, EventStore. All Wave A modules are STRICTLY read-only to Z-MATRIX state. Output modules write to local filesystem only (memory palace), never to Z-MATRIX database or state. Capability Registry is meta (T0) and manages all capability registrations.

Wave B (7 modules, Research + Scoring): Z2 Chain Research Engine, Z2 Scoring Engine, Z8 Execution Plan Generator, V3 Survival Sandbox, B-Matrix v2.1.1, D-Matrix v2.2, R-Matrix v1.1, Flow A RC 16-Node. Wave B modules perform computation/analysis but are read-only to Z-MATRIX state. No modifications to portfolio, no execution orders, no mutation of any system state.

Wave C (4 modules, Future): Portfolio Manager, Broker Adapter, Production Deployer, Real Trade Engine. These are marked FUTURE_ONLY. No planning detail, no specification, no schema for Wave C beyond placeholder existence. Wave C is Level 5 BLOCKED indefinitely.

## 3. Evidence / Dependency

Upstream: WAVE0_CONTROLLED_READONLY_EXECUTION_P0, SkillOS Capability Registry, Z-MATRIX-OS v2.9.5 APIs.
In scope: interface design, schema definition, permission mapping, contract specification, proof requirements, forbidden actions enumeration, test strategy, rollback strategy, review gate design, merge decision framework.
Out of scope: implementation code, actual module wrapping, runtime execution, deployment, real trade, broker operations, production configuration, any file ending in .py/.rs/.ts/.js/.sh, any pip/npm/cargo install, any external API call.

Schema context: All 19 modules must comply with Capability Registration (8-field evidence), Permission Tier (T0-T7), Readonly Policy (7 write classifications), I/O Schema (7 input types, 9 output types), and Evidence Contract (9-field template with hashes).

## 4. Boundary

Inclusions:
- Adapter function signatures and interface definitions
- Permission tier assignment for all 19 modules
- Read/write classification with explicit write taxonomy
- Evidence contracts with hash-based accountability
- I/O schemas with strict type validation
- Forbidden actions matrix with severity classification
- Test strategy (planning-level, no executable test code)
- Rollback strategy (planning-level, no executable rollback)
- Review gate design with 18+ checklist items
- Merge decision framework with 15+ checklist items

Exclusions:
- Adapter implementation in any programming language
- Importing or calling Z-MATRIX modules
- Modifying Z-MATRIX source code
- Executable files (no .py, .rs, .ts, .js, .sh)
- External API connections
- Real trade or broker operations
- Production configuration or deployment scripts
- Runtime enforcement engine
- Any form of code execution
- Database connection or state mutation

## 5. Forbidden Actions

F-S01 Implementing adapter code (CRITICAL) | F-S02 Importing zmatrix modules (CRITICAL) | F-S03 Adding runtime dependencies (HIGH) | F-S04 Executable test scripts (HIGH) | F-S05 .py/.rs/.ts adapter files (CRITICAL) | F-S06 Modifying Z-MATRIX source (CRITICAL) | F-S07 Connecting to production (CRITICAL) | F-S08 Bypassing permission tier (CRITICAL) | F-S09 State-mutating adapter code (CRITICAL) | F-S10 Production deployment plans (HIGH) | F-S11 Hidden network calls (CRITICAL) | F-S12 Undeclared persistence (HIGH) | F-S13 Capability registration bypass (CRITICAL) | F-S14 Cross-wave capability call violation (CRITICAL) | F-S15 Self-promotion of permission tier (CRITICAL) | F-S16 Adapter execution without evidence contract (HIGH) | F-S17 Filesystem write outside approved paths (HIGH) | F-S18 Documentation claiming implementation readiness (MEDIUM)

## 6. Proof / Requirements

R-S01: 19 modules with Wave assignment | R-S02: Wave A all read-only/output | R-S03: Wave B research/scoring only | R-S04: Wave C marked future | R-S05: Exclusions documented with 18 items | R-S06: No implementation code anywhere | R-S07: All forbidden actions with severity (>=18) | R-S08: Inclusions enumerated (>=10) | R-S09: Evidence block references | R-S10: Pipelines signature validates

## 7. Next

CAPABILITY_MAP.md → CONTRACT_STANDARD.md → PERMISSION_TIER_PLAN.md → READONLY_POLICY_PLAN.md → INPUT_OUTPUT_SCHEMA_PLAN.md → EVIDENCE_CONTRACT_PLAN.md → MODULE_PRIORITY_PLAN.md → FORBIDDEN_ACTIONS_MATRIX.md → TEST_AND_PROOF_PLAN.md → ROLLBACK_PLAN.md → PLANNING_CLOSEOUT.md → PLANNING_SEAL.md

**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-SCOPE-v1.1
