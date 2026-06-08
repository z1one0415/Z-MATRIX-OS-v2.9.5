# Factor Library Read-Only Adapter Planning — Validation Snapshot Plan

## Status: Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING_VALIDATION_SNAPSHOT_PLAN_READY
Branch: plan/...factor-library-adapter | Base: 22252711 | Level 5: BLOCKED

## Scope
Plan the FactorValidationSnapshot read-only adapter component. Provides validation results, coverage audits, PIT leakage checks, single-factor validation, and true-OOS execution status. No promotion indicators. Read-only.

### Snapshot Fields (future read-only)
- coverage_passed (bool: universal coverage gate passed)
- coverage_tier (T1: full, T2: partial, T3: minimum)
- pit_passed (bool: PIT leakage check passed)
- single_factor_validation_executed (bool: single-factor validation run)
- true_oos_validation_executed (bool: true out-of-sample validation run)
- ready_for_candidate_review (list: empty until explicitly populated — empty = NOT ready)
- ready_for_promotion_review (bool: false — promotion not available in read-only mode)
- promotion_allowed (const false — no factor promotion through read-only adapter)
- multi_factor_composite_built (const false — no composite building)
- weight_optimization_executed (const false — no weight optimization)
- alpha_claim_allowed (const false — no alpha claims)
- validation_timestamp (ISO8601: when validation was last executed)

### Implementation Plan (future)
- FactorValidationSnapshot class in zmatrix_adapters/factor_library/validation.py
- Methods: get_validation, list_validations, get_coverage_summary (all read-only)
- Tests in test_validation.py

## Parent Interface: d02b60c9. Batch3: F21-F34 validation snapshots.

## Boundary: No implementation. No code. Level 5 BLOCKED. promotion_allowed=false. alpha_claim_allowed=false. ready_for_candidate_review=[] semantics enforced.

## Forbidden: Same as OVERVIEW plus: no alpha_claim extraction, no promotion indicators, no weight approximations.

## Proof: All snapshot fields documented. No promotion path. Batch3 coverage tracked.

## Next: Guardrail Profile Plan.

> Factor Library | Planning | Validation Snapshot | FUTURE_PLAN_ONLY | Level 5 BLOCKED