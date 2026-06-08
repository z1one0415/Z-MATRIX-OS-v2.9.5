# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — EVIDENCE_CONTRACT_PLAN

> Status: _EVIDENCE_CONTRACT_PLAN_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED

## 1. Status
Phase: Wave 0 — Pre-Implementation Planning | Priority: P0 | Evidence: 8 fields, hash chain
Hardened: 2026-06-08

## 2. Scope

Evidence Block (8 mandatory fields per adapter invocation):
- request_hash (sha256): Hash of validated input payload. Computed after input validation.
- response_hash_placeholder (sha256): Pre-computed empty slot. Filled post-execution with sha256 of output.
- decision_hash (sha256): Hash of decision record, linked to human approval gate.
- module_adapter_id (string): CAP-XXX-NNN format.
- source_class (string): Wave letter (A/B/C).
- permission_tier (T0-T7): Authorization tier during execution.
- graph_edge_id (string): Dependency graph edge key.
- no_hidden_writes (boolean): Audit attestation. Default: true.

Hash chain: request_hash → response_hash → decision_hash. Missing/mismatched = violation = execution invalidated.

Evidence pipeline (6 stages): 1. Input Validation → request_hash | 2. Permission Gate → tier + edge_id | 3. Execution → response_hash | 4. Side Effect Audit → no_hidden_writes | 5. Evidence Assembly → 8-field block | 6. EventStore Write → persist with timestamp.

## 3. Evidence / Dependency

Evidence integrity rules (8):
- EI-01: request_hash = sha256 of validated input (not raw)
- EI-02: response_hash_placeholder = blank (0x0) before execution
- EI-03: decision_hash links to human decision record
- EI-04: module_adapter_id matches registered capability
- EI-05: source_class matches Wave assignment from CAPABILITY_MAP
- EI-06: permission_tier matches PERMISSION_TIER_PLAN assignment
- EI-07: graph_edge_id references valid dependency edge
- EI-08: no_hidden_writes verified by post-execution audit

## 4. Boundary

Evidence scope per wave: Wave A/B: Full 8-field evidence. Wave C: Placeholder only, no specification.

In scope: Evidence schema, hash generation rules, pipeline stages, integrity rules, verification order, EventStore integration. Out: Hash function implementation, runtime evidence generation, crypto library integration, storage format.

## 5. Forbidden Actions

F-EV01 Missing evidence block (CRITICAL) | F-EV02 request_hash from invalid input (HIGH) | F-EV03 response_hash mismatch (HIGH) | F-EV04 decision_hash bypass human gate (CRITICAL) | F-EV05 module_adapter_id not registered (HIGH) | F-EV06 source_class mismatch (MEDIUM) | F-EV07 permission_tier escalation without evidence (CRITICAL) | F-EV08 graph_edge_id nonexistent (HIGH) | F-EV09 no_hidden_writes true despite violation (CRITICAL) | F-EV10 Evidence modified post-generation (CRITICAL) | F-EV11 Missing field (HIGH) | F-EV12 Hash collision exploit (HIGH) | F-EV13 Pipeline stage bypass (HIGH) | F-EV14 Pre-execution evidence with response_hash (HIGH) | F-EV15 EventStore write fail silent (MEDIUM) | F-EV16 No timestamp (MEDIUM) | F-EV17 Replay stale evidence (MEDIUM) | F-EV18 Evidence chain gap (MEDIUM)

## 6. Proof / Requirements

R-EV01: 8 evidence fields | R-EV02: Hash chain order specified | R-EV03: 6-stage pipeline | R-EV04: 8 integrity rules | R-EV05: Forbidden >=18 | R-EV06: Wave A/B full coverage | R-EV07: Wave C placeholder | R-EV08: no_hidden_writes audit defined | R-EV09: EventStore integration | R-EV10: Evidence immutable post-generation

## 7. Next

MODULE_PRIORITY_PLAN.md → FORBIDDEN_ACTIONS_MATRIX.md → TEST_AND_PROOF_PLAN.md → ROLLBACK_PLAN.md → PLANNING_CLOSEOUT.md

**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-EVIDENCE_CONTRACT_PLAN-v1.1
