# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — CONTRACT_STANDARD

> Status: _CONTRACT_STANDARD_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED

## 1. Status
Phase: Wave 0 — Pre-Implementation Planning | Priority: P0
Contract Version: v1.0 | Sections: 8 mandatory + 2 optional
Hardened: 2026-06-08

## 2. Scope

Every Z-MATRIX Module Adapter must conform to a standardized SkillOS contract with 8 mandatory sections:

(1) Header — Adapter name, version, capability ID, wave assignment, permission tier, status marker. Must include FUTURE_PLAN_ONLY and Level 5 BLOCKED for all planning-phase adapters.

(2) Preconditions — All conditions required before execution, each with: condition_id, description, check_method, on_failure_action. Must cover: permission tier check, dependency satisfaction, input completeness, sandbox boundaries, readonly enforcement.

(3) Input Schema — Strict type and validation using: type (object), required fields array, properties with types and constraints. All stock codes must match ^[0-9]{6}$. All dates must be ISO 8601.

(4) Output Schema — Strict type and validation using: type (object), required fields array, properties with types. Must use AdapterResult wrapper: {status: "success"|"error", data: object|null, errors: array, meta: object}.

(5) Error Contract — All error states with: error_code (unique), condition (trigger), handling (mitigation), retryable (boolean). Minimum error taxonomy: VALIDATION_ERROR, PERMISSION_DENIED, DEPENDENCY_MISSING, STATE_ACCESS_VIOLATION, SANDBOX_ESCAPE, INTERNAL_ERROR.

(6) Dependencies — Upstream capabilities with: capability_id, required (boolean), version_constraint, reason_for_dependency. All dependencies must be declared before execution.

(7) Side Effects — All state mutations listed explicitly. For Wave A/B: side_effects array must be empty or contain only allowed filesystem writes. For Wave C: declare all state mutations. Template: {type, target, idempotent, reversible}.

(8) Evidence Requirements — What constitutes provably successful execution: request_hash (sha256 of validated input), response_hash (sha256 of output), decision_hash (sha256 of decision), module_adapter_id, source_class, permission_tier, graph_edge_id, no_hidden_writes audit trail.

Optional sections: (9) Performance Budget — maximum duration, memory ceiling, retry budget. (10) Observability Hooks — metrics emissions, log level, event publishing configuration.

## 3. Evidence / Dependency

8 enforcement rules: CE-01 All adapters need valid contract | CE-02 Exhaustive preconditions | CE-03 Input schema rejects invalid inputs | CE-04 Output schema validates outputs | CE-05 Error contract covers all failure modes | CE-06 Declarative verifiable dependencies | CE-07 Explicit side effects | CE-08 Testable proof requirements.

8-stage validation pipeline: 1. Contract Definition → 2. Schema Validation → 3. Dependency Check → 4. Precondition Verification → 5. Permission Gate → 6. Execution → 7. Output Validation → 8. Side Effect Audit + Evidence Generation.

## 4. Boundary

Contract versioning: Major bump (schema breaking, new required field, removed property, type change). Minor bump (backward-compatible: new optional field, new error code, additional proof). Patch (documentation-only).

In scope: contract structure, enforcement rules, validation pipeline, versioning policy, field definitions, error taxonomy, evidence block specification. Out: runtime validation implementation, contract parser, storage format.

## 5. Forbidden Actions

F-CS01 Adapter without contract (CRITICAL) | F-CS02 Missing mandatory sections (HIGH) | F-CS03 Arbitrary input types (HIGH) | F-CS04 Output schema mismatch (HIGH) | F-CS05 Missing error modes (HIGH) | F-CS06 Undeclared dependency (CRITICAL) | F-CS07 Undeclared side effect (CRITICAL) | F-CS08 Untestable proof (HIGH) | F-CS09 Contract modification without version bump (HIGH) | F-CS10 Bypassing validation pipeline (CRITICAL) | F-CS11 Evidence block with missing hash (HIGH) | F-CS12 Undocumented precondition (MEDIUM) | F-CS13 Self-referencing dependency (HIGH) | F-CS14 Contract claiming implementation readiness (CRITICAL) | F-CS15 Circular contract dependencies (HIGH) | F-CS16 Output without AdapterResult wrapper (HIGH) | F-CS17 Error contract with fewer than 6 codes (MEDIUM) | F-CS18 Evidence field count below 8 (MEDIUM)

## 6. Proof / Requirements

R-CS01: 8 mandatory sections defined | R-CS02: Valid contract template structure | R-CS03: 8 enforcement rules enumerated | R-CS04: 8-stage validation pipeline | R-CS05: Versioning policy all three levels | R-CS06: Forbidden actions >=18 | R-CS07: Error taxonomy >=6 codes | R-CS08: Side effects declaration required | R-CS09: Evidence block >=8 fields | R-CS10: Precondition template with 4 sub-fields

## 7. Next

PERMISSION_TIER_PLAN.md → READONLY_POLICY_PLAN.md → INPUT_OUTPUT_SCHEMA_PLAN.md → EVIDENCE_CONTRACT_PLAN.md → MODULE_PRIORITY_PLAN.md

**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-CONTRACT_STANDARD-v1.1
