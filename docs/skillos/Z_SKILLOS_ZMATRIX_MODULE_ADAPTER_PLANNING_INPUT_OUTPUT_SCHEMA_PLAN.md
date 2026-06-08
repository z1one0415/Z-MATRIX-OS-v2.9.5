# Z_SKILLOS_ZMATRIX_MODULE_ADAPTER_PLANNING — INPUT_OUTPUT_SCHEMA_PLAN

> Status: _INPUT_OUTPUT_SCHEMA_PLAN_READY | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Branch: plan/skillos-zmatrix-module-adapter-planning | Base Commit: c7c4ac9bdd8884576fbf79b269bfdfee5c3cab86
> Dependency: WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED

## 1. Status
Phase: Wave 0 — Pre-Implementation Planning | Priority: P0


## 2. Scope

Common input types (7): StockCode (string, ^[0-9]{6}$), DateRange ({start, end}), QueryFilter, MemoryQuery, ResearchRequest, ScoringRequest, PipelineConfig.

Common output types (9): AdapterResult (mandatory wrapper: {status, data, errors, meta}), Error ({code, message, details}), Meta ({adapter, capability, tier, duration_ms, timestamp}), ResearchOutput, ScoringOutput, MatrixResult, PipelineResult, ValidationResult, MemoryResult.

Schema validation rules (8): SV-01 inputs validated before execution | SV-02 outputs validated before return | SV-03 AdapterResult wrapper mandatory | SV-04 Meta block required (5 fields) | SV-05 Error array empty on success | SV-06 Stock codes 6-digit | SV-07 Dates ISO 8601 | SV-08 Enums exact match.

Schema inheritance: BaseAdapterInput → SpecificAdapterInput. BaseAdapterOutput → SpecificAdapterOutput. Error → ExtendedError. Meta → ExtendedMeta.

## 3. Evidence / Dependency

Evolution rules: optional field → minor bump (backward compat). required field → major bump (breaking). type change → major bump. field removal → major bump. field rename → remove+add, major bump.

## 4. Boundary

Schema scope: types for 19 module adapters, validation rules, transformation patterns. Out: runtime validation implementation, JSON Schema library, serialization format.

## 5. Forbidden Actions

F-IO01 Accepting invalid input (CRITICAL) | F-IO02 Returning invalid output (CRITICAL) | F-IO03 No AdapterResult wrapper (HIGH) | F-IO04 Missing Meta block (HIGH) | F-IO05 Success with errors (HIGH) | F-IO06 Failure without errors (HIGH) | F-IO07 Breaking change no major bump (CRITICAL) | F-IO08 Untyped/any fields (HIGH) | F-IO09 Non-6-digit stock (HIGH) | F-IO10 Non-ISO date (HIGH)

## 6. Proof / Requirements

R-IO01: 7 input types | R-IO02: 9 output types | R-IO03: AdapterResult wrapper | R-IO04: 8 validation rules | R-IO05: Inheritance pattern | R-IO06: 5 evolution rules | R-IO07: Forbidden ≥10 | R-IO08: Types cover 19 modules

## 7. Next

EVIDENCE_CONTRACT_PLAN.md → FORBIDDEN_ACTIONS_MATRIX.md → MODULE_PRIORITY_PLAN.md → TEST_AND_PROOF_PLAN.md → PLANNING_CLOSEOUT.md


**Signoff**: ☯️ Z2天师 | **Pipeline**: Z-SKILLOS-ZMATRIX-MODULE-ADAPTER-PLANNING-INPUT_OUTPUT_SCHEMA_PLAN-v1.0
