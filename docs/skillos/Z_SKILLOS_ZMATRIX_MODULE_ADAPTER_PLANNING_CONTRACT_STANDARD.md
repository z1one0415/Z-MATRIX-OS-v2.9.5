# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — CONTRACT_STANDARD

> Status: _CONTRACT_STANDARD_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED

## 1. Status
Phase: Wave 0 — Pre-Implementation Planning | Priority: P0


## 2. Scope

Every Z-MATRIX Module Adapter must conform to a standardized SkillOS contract with 8 mandatory sections: (1) Header — adapter name, version, capability ID, wave, status. (2) Preconditions — all conditions before execution with condition/check/on_failure. (3) Input Schema — strict type and validation (type:object, required, properties). (4) Output Schema — strict type and validation. (5) Error Contract — all error states with code/condition/handling/retryable. (6) Dependencies — upstream capabilities with capability_id/required/reason. (7) Side Effects — all state mutations (empty for read-only). (8) Proof Requirements — what constitutes successful execution.

## 3. Evidence / Dependency

Enforcement rules: CE-01 All adapters need valid contract | CE-02 Exhaustive preconditions | CE-03 Input schema rejects invalid inputs | CE-04 Output schema validates outputs | CE-05 Error contract covers all failure modes | CE-06 Declarative verifiable dependencies | CE-07 Explicit side effects | CE-08 Testable proof requirements.

Validation pipeline (8 stages): Contract Definition → Schema Validation → Dependency Check → Precondition Check → Execution → Output Validation → Side Effect Audit → Proof Verification.

## 4. Boundary

Contract versioning: Major bump (schema change, new required field, removed capability). Minor bump (new optional field, new error code, new proof). Patch (docs, descriptions). In: contract structure and rules. Out: implementation, runtime enforcement engine, storage format.

## 5. Forbidden Actions

F-CS01 Adapter without contract (CRITICAL) | F-CS02 Missing mandatory sections (HIGH) | F-CS03 Arbitrary input types (HIGH) | F-CS04 Output schema mismatch (HIGH) | F-CS05 Missing error modes (HIGH) | F-CS06 Undeclared dependency (CRITICAL) | F-CS07 Undeclared side effect (CRITICAL) | F-CS08 Untestable proof (HIGH)

## 6. Proof / Requirements

R-CS01: 8 mandatory sections | R-CS02: Valid contract template | R-CS03: 8 enforcement rules | R-CS04: 8-stage validation pipeline | R-CS05: Versioning for all levels | R-CS06: Forbidden ≥8 | R-CS07: Error taxonomy | R-CS08: Side effects required

## 7. Next

PERMISSION_TIER_PLAN.md → READONLY_POLICY_PLAN.md → INPUT_OUTPUT_SCHEMA_PLAN.md → EVIDENCE_CONTRACT_PLAN.md → MODULE_PRIORITY_PLAN.md


**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-CONTRACT_STANDARD-v1.0
