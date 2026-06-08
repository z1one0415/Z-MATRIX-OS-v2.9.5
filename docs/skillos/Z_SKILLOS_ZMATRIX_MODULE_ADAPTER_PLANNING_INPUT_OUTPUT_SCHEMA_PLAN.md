# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — INPUT_OUTPUT_SCHEMA_PLAN

> Status: _INPUT_OUTPUT_SCHEMA_PLAN_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED

## 1. Status
Phase: Wave 0 — Pre-Implementation Planning | Priority: P0 | Schemas: 7 input + 9 output types
Hardened: 2026-06-08

## 2. Scope

Input types (7): StockCode (^[0-9]{6}$), DateRange ({start, end} ISO8601), QueryFilter, MemoryQuery, ResearchRequest, ScoringRequest, PipelineConfig.

Output types (9): AdapterResult (MANDATORY: {status, data, errors, meta}), Error ({code, message, details, retryable}), Meta ({adapter_id, capability_id, tier, duration_ms, timestamp}), ResearchOutput, ScoringOutput, MatrixResult, PipelineResult, ValidationResult, MemoryResult.

Validation rules (8): SV-01 inputs validated before execution | SV-02 outputs validated before return | SV-03 AdapterResult mandatory | SV-04 Meta block 5 fields | SV-05 Error array empty on success | SV-06 Stock codes 6-digit | SV-07 Dates ISO 8601 | SV-08 Enums exact match.

Inheritance: BaseAdapterInput → SpecificAdapterInput, BaseAdapterOutput → SpecificAdapterOutput, Error → ExtendedError, Meta → ExtendedMeta.

## 3. Evidence / Dependency

Evolution rules (5): ER1 optional field → MINOR bump | ER2 required field → MAJOR bump | ER3 type change → MAJOR bump | ER4 field removal → MAJOR bump | ER5 rename → remove+add, MAJOR bump.

## 4. Boundary

Schema scope: Types for 19 modules, validation rules, inheritance patterns, evolution policy. Out: runtime validation, JSON Schema integration, serialization format, storage mechanism.

Type safety: No `any` fields. All explicit types. Enums list allowed values. Numerics have min/max. Strings have pattern/maxLength.

## 5. Forbidden Actions

F-IO01 Accepting invalid input (CRITICAL) | F-IO02 Returning invalid output (CRITICAL) | F-IO03 No AdapterResult wrapper (HIGH) | F-IO04 Missing Meta block (HIGH) | F-IO05 Success with errors (HIGH) | F-IO06 Failure without errors (HIGH) | F-IO07 Breaking change no major bump (CRITICAL) | F-IO08 Untyped/any fields (HIGH) | F-IO09 Non-6-digit stock (HIGH) | F-IO10 Non-ISO date (HIGH) | F-IO11 Enum partial match (MEDIUM) | F-IO12 Output bypass schema validation (CRITICAL) | F-IO13 No type constraint (HIGH) | F-IO14 Input validated after execution (MEDIUM) | F-IO15 Required→optional without bump (HIGH) | F-IO16 Nested object no schema (MEDIUM) | F-IO17 Circular type references (HIGH) | F-IO18 AdapterResult unpopulated duration_ms (MEDIUM)

## 6. Proof / Requirements

R-IO01: 7 input types | R-IO02: 9 output types | R-IO03: AdapterResult mandatory | R-IO04: 8 validation rules | R-IO05: Inheritance 4 base types | R-IO06: 5 evolution rules | R-IO07: Forbidden >=18 | R-IO08: Types cover 19 modules | R-IO09: Meta 5 fields | R-IO10: StockCode regex explicit

## 7. Next

EVIDENCE_CONTRACT_PLAN.md → FORBIDDEN_ACTIONS_MATRIX.md → MODULE_PRIORITY_PLAN.md → TEST_AND_PROOF_PLAN.md → PLANNING_CLOSEOUT.md

**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-INPUT_OUTPUT_SCHEMA_PLAN-v1.1
