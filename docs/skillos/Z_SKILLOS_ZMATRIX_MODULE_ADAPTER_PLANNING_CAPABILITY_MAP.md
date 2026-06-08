# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — CAPABILITY_MAP

> Status: _CAPABILITY_MAP_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED

## 1. Status
Phase: Wave 0 — Pre-Implementation Planning | Priority: P0


## 2. Scope

Complete capability-to-module mapping for all 19 modules across Waves A/B/C.

Wave A Capabilities (Read/Output): CAP-MEM-001 Memory Query (Z9), CAP-RPT-001 Research Output Read (Z2 Reader), CAP-RPT-002 Local Report Generate, CAP-DOC-001 Document Generate, CAP-REG-001 Capability Registry Query (Meta), CAP-GAT-001 TruthGate Validate, CAP-EVT-001 EventStore Write.

Wave B Capabilities (Research/Scoring): CAP-CHN-001 Chain Research Execute (Z2 Chain), CAP-SCR-001 Scoring Execute (Z2 Scoring), CAP-EXE-001 Execution Plan Generate (Z8), CAP-SIM-001 Survival Sandbox Run (V3), CAP-BMX-001 B-Matrix Scan, CAP-DMX-001 D-Matrix Scan, CAP-RMX-001 R-Matrix Scan, CAP-FLO-001 Flow A Execute.

Wave C Capabilities (Future): CAP-PRT-001 Portfolio Manage, CAP-BRK-001 Broker Execute, CAP-DEP-001 Production Deploy, CAP-TRD-001 Real Trade Execute.

Dependency graph: CAP-REG-001 (meta) → all others. CAP-GAT-001 → CAP-FLO-001. CAP-EVT-001 → CAP-FLO-001, CAP-SCR-001. CAP-BMX/DMX/RMX → CAP-FLO-001. CAP-CHN-001 → CAP-BMX/DMX. CAP-SCR-001 → CAP-CHN-001. CAP-EXE-001 → CAP-SCR-001. Wave C: no dependency chain yet.

## 3. Evidence / Dependency

Registration rules: 1 primary capability per adapter, up to 3 secondary. Wave A: read-only/output. Wave B: research/analysis, readonly to state. Wave C: future, not planned. No Wave C from Wave A/B. No duplicate primaries. CAP-REG-001 initialized first.

## 4. Boundary

Conflict rules: no duplicate primaries, read+write on same module = conflict, meta capability first. Capability scope: all 19 modules mapped with unique IDs. Out: implementation, runtime enforcement.

## 5. Forbidden Actions

F-CM01 Duplicate primary capabilities (CRITICAL) | F-CM02 Wave A calling Wave B (HIGH) | F-CM03 Wave B calling Wave C (HIGH) | F-CM04 Undeclared dependency (HIGH) | F-CM05 Runtime registry modification (HIGH) | F-CM06 Unregistered execution (CRITICAL) | F-CM07 Dependency chain bypass (HIGH) | F-CM08 No evidence contract (HIGH)

## 6. Proof / Requirements

R-CM01: 19 primary capabilities | R-CM02: All unique IDs | R-CM03: Wave A ≤7, all read/output | R-CM04: Wave B ≤7, all read/research | R-CM05: Wave C ≤4, all future | R-CM06: No cycles | R-CM07: CAP-REG-001 meta | R-CM08: No Wave C from A/B

## 7. Next

CONTRACT_STANDARD.md → PERMISSION_TIER_PLAN.md → READONLY_POLICY_PLAN.md → INPUT_OUTPUT_SCHEMA_PLAN.md → EVIDENCE_CONTRACT_PLAN.md → MODULE_PRIORITY_PLAN.md


**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-CAPABILITY_MAP-v1.0
