# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — CAPABILITY_MAP

> Status: _CAPABILITY_MAP_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED

## 1. Status
Phase: Wave 0 — Pre-Implementation Planning | Priority: P0
Mapping: 19 capabilities → 19 module adapters → 8 permission tiers → 8 evidence fields
Hardened: 2026-06-08 | 19 primary + 19 secondary mappings defined

## 2. Scope

Complete capability-to-module mapping for all 19 modules across Waves A/B/C.

Wave A Capabilities (Read/Output, 7 total):
- CAP-MEM-001: Z9 Memory Bridge — Query episodic/procedural memory, read-only
- CAP-RPT-001: Z2 Research Output Reader — Parse Z2 research outputs, read-only
- CAP-RPT-002: Local Report Generator — Generate markdown docs to local fs
- CAP-DOC-001: Document Generator — Generate structured documents, output-only
- CAP-REG-001: Capability Registry Query — Register/deregister/query capabilities (meta, T0)
- CAP-GAT-001: TruthGate Validate — Validate execution preconditions, read-only
- CAP-EVT-001: EventStore Write — Write execution events to local EventStore

Wave B Capabilities (Research/Scoring, 8 total):
- CAP-CHN-001: Z2 Chain Research Execute — Run Z2 chain research pipeline, read-only to state
- CAP-SCR-001: Z2 Scoring Execute — Run Z2 scoring pipeline, read-only to state
- CAP-EXE-001: Z8 Execution Plan Generate — Generate Z8 execution plans, read-only to state
- CAP-SIM-001: V3 Survival Sandbox Run — Run V3 survival simulation, read-only sandboxed
- CAP-BMX-001: B-Matrix Scan — Execute B-Matrix v2.1.1 scan, read-only to state
- CAP-DMX-001: D-Matrix Scan — Execute D-Matrix v2.2 scan, read-only to state
- CAP-RMX-001: R-Matrix Scan — Execute R-Matrix v1.1 scan, read-only to state
- CAP-FLO-001: Flow A RC Execute — Run Flow A RC 16-Node pipeline, read-only to state

Wave C Capabilities (Future, 4 total, NOT PLANNED):
- CAP-PRT-001: Portfolio Manage — Manage portfolio positions (FUTURE ONLY)
- CAP-BRK-001: Broker Execute — Broker order execution (FUTURE ONLY)
- CAP-DEP-001: Production Deploy — Deploy to production (FUTURE ONLY)
- CAP-TRD-001: Real Trade Execute — Execute real trades (FUTURE ONLY)

## 3. Evidence / Dependency

Dependency graph:
- CAP-REG-001 (meta, T0) → all other capabilities (registration requirement)
- CAP-GAT-001 → CAP-FLO-001 (pipeline gate validation)
- CAP-EVT-001 → CAP-FLO-001, CAP-SCR-001 (event logging)
- CAP-BMX-001 / CAP-DMX-001 / CAP-RMX-001 → CAP-FLO-001 (matrix scan → pipeline)
- CAP-CHN-001 → CAP-BMX-001 / CAP-DMX-001 (chain research feeds matrix)
- CAP-SCR-001 → CAP-CHN-001 (scoring requires research output)
- CAP-EXE-001 → CAP-SCR-001 (execution plan requires scoring)
- Wave C: NO dependency chain, NO invocation from Wave A/B, FULLY BLOCKED

Registration rules: 1 primary capability per adapter, up to 3 secondary. Wave A: read-only/output. Wave B: research/analysis, read-only to state. Wave C: future, not planned. No Wave C from Wave A/B. No duplicate primaries. CAP-REG-001 initialized first.

Evidence contract per capability: request hash (sha256 of input), response hash placeholder (blank until execution), decision hash (sha256 of decision record), module adapter id (CAP-XXX-NNN), source class (wave letter), permission tier (T0-T7), graph edge id (dependency edge key), no hidden writes (audit attestation).

## 4. Boundary

Conflict resolution matrix:
- No duplicate primary capabilities (same module = 1 primary adapter)
- Read+write on same module = CONFLICT (requires separate adapters)
- Meta capability (CAP-REG-001) must be initialized first
- Cross-wave calls forbidden (Wave A cannot call Wave B; Wave B cannot call Wave C)
- Wave C placeholder capabilities exist only for completeness, zero specification

In scope: 19 primary capability IDs, 19 module adapter bindings, dependency graph with edges, registration order, conflict rules. Out: implementation, runtime enforcement, actual capability execution, code generation.

## 5. Forbidden Actions

F-CM01 Duplicate primary capabilities (CRITICAL) | F-CM02 Wave A calling Wave B (HIGH) | F-CM03 Wave B calling Wave C (CRITICAL) | F-CM04 Undeclared dependency (HIGH) | F-CM05 Runtime registry modification (HIGH) | F-CM06 Unregistered execution (CRITICAL) | F-CM07 Dependency chain bypass (HIGH) | F-CM08 No evidence contract (HIGH) | F-CM09 Cross-wave capability leak (CRITICAL) | F-CM10 Primary-secondary mismatch (HIGH) | F-CM11 Capability without permission tier (CRITICAL) | F-CM12 Circular dependency in graph (HIGH) | F-CM13 Wave C from A/B invocation (CRITICAL) | F-CM14 Undeclared secondary capability (MEDIUM) | F-CM15 Registry mutation from non-T0 (CRITICAL) | F-CM16 Conflict resolution bypass (HIGH) | F-CM17 Capability ID collision (CRITICAL) | F-CM18 Hashless evidence block (HIGH)

## 6. Proof / Requirements

R-CM01: 19 primary capabilities with unique IDs | R-CM02: All IDs format CAP-XXX-NNN | R-CM03: Wave A ≤7, all read/output | R-CM04: Wave B ≤8, all read/research | R-CM05: Wave C ≤4, all future | R-CM06: Dependency graph has no cycles | R-CM07: CAP-REG-001 meta position verified | R-CM08: No Wave C dependency path from A/B | R-CM09: All 19 modules have at least 1 capability | R-CM10: Secondary bindings declared

## 7. Next

CONTRACT_STANDARD.md → PERMISSION_TIER_PLAN.md → READONLY_POLICY_PLAN.md → INPUT_OUTPUT_SCHEMA_PLAN.md → EVIDENCE_CONTRACT_PLAN.md → MODULE_PRIORITY_PLAN.md

**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-CAPABILITY_MAP-v1.1
