# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — PERMISSION_TIER_PLAN

> Status: _PERMISSION_TIER_PLAN_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED

## 1. Status
Phase: Wave 0 — Pre-Implementation Planning | Priority: P0 | Tiers: 8 (T0-T7) | Modules: 19
Hardened: 2026-06-08

## 2. Scope

8-tier permission model for all 19 Z-MATRIX module adapters:

T0 Meta: Capability Registry — Register/deregister/query capabilities. Administrative. Only tier allowed to modify registry. CAP-REG-001.

T1 Read-Only Query: Z9 Memory Bridge, TruthGate, Z2 Research Reader — Query memory, parse research, validate preconditions. No writes to any system. CAP-MEM-001, CAP-GAT-001, CAP-RPT-001.

T2 Output-Only Generation: Document Generator, EventStore, Local Report Generator — Filesystem writes ONLY to approved memory palace paths. No Z-MATRIX state mutation. Inherits T1 read. CAP-DOC-001, CAP-EVT-001, CAP-RPT-002.

T3 Research/Analysis: Z2 Chain Research, Z2 Scoring, V3 Survival Sandbox, B/D/R Matrix — Execute research pipelines, scoring, simulations. Read-only to Z-MATRIX state. All results computed in-memory, output to local fs. CAP-CHN-001, CAP-SCR-001, CAP-SIM-001, CAP-BMX-001, CAP-DMX-001, CAP-RMX-001.

T4 Pipeline Execution: Z8 Execution Plan Generator, Flow A RC 16-Node — Generate plans, run pipelines. Read-only to state. Outputs plans as documents. CAP-EXE-001, CAP-FLO-001.

T5 Portfolio Management: Portfolio Manager — Manage portfolio positions. Wave C FUTURE ONLY. CAP-PRT-001.

T6 Trade Execution: Broker Adapter, Real Trade Engine — Broker operations. Wave C FUTURE ONLY. CAP-BRK-001, CAP-TRD-001.

T7 Production Deployment: Production Deployer — Production deployment. Wave C FUTURE ONLY. CAP-DEP-001.

Wave-to-Tier: Wave A = T0/T1/T2. Wave B = T3/T4. Wave C = T5/T6/T7.

## 3. Evidence / Dependency

8 enforcement points: EP1 Capability Registration (T0) | EP2 Memory Access (T1+) | EP3 Report Generation (T2+) | EP4 Research Execution (T3+) | EP5 Pipeline Execution (T4+) | EP6 Portfolio Modification (T5+) | EP7 Trade Execution (T6+) | EP8 Production Deployment (T7+).

Tier transitions: No self-promotion. Downgrade requires T0 approval + contract revalidation. Cross-tier calls pass permission gate for both tiers. Tier change triggers full evidence contract regeneration.

Permission inheritance: T0 → T1 → T2 (T1+output) → T3 (T1+analysis) → T4 (T3+pipeline) → T5 (T2+T4+portfolio) → T6 (T5+trade) → T7 (T6+deploy). No circular inheritance.

## 4. Boundary

T0-T2: Wave A first — read/output. Filesystem writes to memory palace only. T0 manages registry; T1 reads; T2 writes local-only.
T3-T4: Wave B second — analysis/pipeline, no state mutation. All computation in-memory.
T5-T7: Wave C future — state-mutating. NOT PLANNED. Level 5 BLOCKED.

## 5. Forbidden Actions

F-PT01 T1 adapter attempting write (CRITICAL) | F-PT02 T2 bypassing read check (HIGH) | F-PT03 T3 modifying state (CRITICAL) | F-PT04 T4 executing trades (CRITICAL) | F-PT05 Self-promotion (CRITICAL) | F-PT06 Bypassing permission gate (CRITICAL) | F-PT07 Wave A/B calling Wave C (CRITICAL) | F-PT08 No tier assignment (HIGH) | F-PT09 Downgrade without revalidation (HIGH) | F-PT10 Direct tier bypass (CRITICAL) | F-PT11 Output outside approved paths (CRITICAL) | F-PT12 Pipeline triggering state mutation (CRITICAL) | F-PT13 Research emitting trade signals (CRITICAL) | F-PT14 T0 registry mutation without audit (HIGH) | F-PT15 Cross-tier inheritance violation (HIGH) | F-PT16 Execution without permission gate check (CRITICAL) | F-PT17 Tier change without evidence regeneration (HIGH) | F-PT18 Unauthorized tier elevation (CRITICAL)

## 6. Proof / Requirements

R-PT01: 19 modules with tier | R-PT02: 8 tiers T0-T7 | R-PT03: Wave A only T0-T2 | R-PT04: Wave B only T3-T4 | R-PT05: Wave C only T5-T7 | R-PT06: Acyclic inheritance | R-PT07: 8 enforcement points | R-PT08: Forbidden >=18 | R-PT09: Tier transition rules explicit | R-PT10: EP1-EP8 gate checks defined

## 7. Next

READONLY_POLICY_PLAN.md → INPUT_OUTPUT_SCHEMA_PLAN.md → EVIDENCE_CONTRACT_PLAN.md → FORBIDDEN_ACTIONS_MATRIX.md → MODULE_PRIORITY_PLAN.md

**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-PERMISSION_TIER_PLAN-v1.1
