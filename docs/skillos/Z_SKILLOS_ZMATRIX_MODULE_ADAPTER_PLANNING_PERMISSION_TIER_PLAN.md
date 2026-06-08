# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — PERMISSION_TIER_PLAN

> Status: _PERMISSION_TIER_PLAN_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED

## 1. Status
Phase: Wave 0 — Pre-Implementation Planning | Priority: P0


## 2. Scope

8-tier permission model for all 19 Z-MATRIX module adapters:
T0 Meta: Capability Registry — register/deregister/query capabilities.
T1 Read-Only: Z9 Memory Bridge, TruthGate, Z2 Research Reader — query memory, parse research, validate.
T2 Output-Only: Document Generator, EventStore, Local Report Generator — generate documents, write events.
T3 Analysis: Z2 Chain Research, Z2 Scoring, V3 Survival Sandbox, B/D/R Matrix — research, scoring, simulation.
T4 Execution: Z8 Execution Plan Generator, Flow A RC 16-Node — generate plans, run pipelines.
T5 Portfolio: Portfolio Manager — manage portfolio state (Wave C).
T6 Trade: Broker Adapter, Real Trade Engine — broker operations (Wave C).
T7 Deploy: Production Deployer — production deployment (Wave C).

Wave-to-Tier: Wave A = T0/T1/T2, Wave B = T3/T4, Wave C = T5/T6/T7.
Inheritance: T0 manages all. T1 base. T2 inherits T1. T3 inherits T1. T4 inherits T3. T5 inherits T2,T4. T6 inherits T5. T7 inherits T6.

## 3. Evidence / Dependency

8 enforcement points: Capability Registration (T0), Memory Access (T1+), Report Generation (T2+), Research Execution (T3+), Pipeline Execution (T4+), Portfolio Modification (T5+), Trade Execution (T6+), Production Deployment (T7).
Tier transitions: no self-promotion, downgrade needs T0 approval, tier change triggers contract revalidation, cross-tier calls pass permission gate.

## 4. Boundary

T0-T2: Wave A first (read/output-only). T3-T4: Wave B second (analysis, no state mutation). T5-T7: Wave C future (not implemented this phase).

## 5. Forbidden Actions

F-PT01 T1 adapter attempting write (CRITICAL) | F-PT02 T2 bypassing read (HIGH) | F-PT03 T3 modifying state (CRITICAL) | F-PT04 T4 executing trades (CRITICAL) | F-PT05 Self-promotion (CRITICAL) | F-PT06 Bypassing permission gate (CRITICAL) | F-PT07 Wave A/B calling Wave C (CRITICAL) | F-PT08 No tier assignment (HIGH) | F-PT09 Downgrade without revalidation (HIGH) | F-PT10 Direct tier bypass (CRITICAL)

## 6. Proof / Requirements

R-PT01: 19 modules with tier | R-PT02: 8 tiers T0-T7 | R-PT03: Wave A only T0-T2 | R-PT04: Wave B only T3-T4 | R-PT05: Wave C only T5-T7 | R-PT06: Acyclic inheritance | R-PT07: 8 enforcement points | R-PT08: Forbidden ≥10

## 7. Next

READONLY_POLICY_PLAN.md → INPUT_OUTPUT_SCHEMA_PLAN.md → EVIDENCE_CONTRACT_PLAN.md → FORBIDDEN_ACTIONS_MATRIX.md → MODULE_PRIORITY_PLAN.md


**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-PERMISSION_TIER_PLAN-v1.0
