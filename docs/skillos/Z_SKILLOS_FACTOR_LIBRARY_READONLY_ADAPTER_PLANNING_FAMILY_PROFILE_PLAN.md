# Factor Library Read-Only Adapter Planning — Family Profile Plan

## Status: Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING_FAMILY_PROFILE_PLAN_READY
Branch: plan/...factor-library-adapter | Base: 22252711 | Level 5: BLOCKED

## Scope
Plan the FactorFamilyProfile read-only adapter component. Family grouping and overlap detection.

### Profile Fields (future read-only)
- family_id (unique family identifier)
- family_group (classification group: momentum, value, quality, growth, low_vol, size, sentiment)
- overlap_group (overlap detection group)
- orthogonality_required (whether family requires orthogonality check)
- max_active_candidates_per_family (max number of simultaneous active candidates)
- new_family_requires_review (flag: new families go through review gate)
- rejected_factor_preservation (rejected factors preserved in archive)
- family_overlap_denial (deny if family overlap detected)

### Implementation Plan (future)
- FactorFamilyProfile class in zmatrix_adapters/factor_library/family.py
- get_profile / list_families methods (read-only)
- Tests in test_family.py

## Parent Interface: d02b60c9. Batch3 factors family groups tracked.

## Boundary: No implementation. No code. Level 5 BLOCKED.

## Forbidden: Same as OVERVIEW.

## Proof: All profile fields documented. Overlap gate concept defined.

## Next: Validation Snapshot Plan.

> Factor Library | Planning | Family Profile | FUTURE_PLAN_ONLY | Level 5 BLOCKED
> Factor Library | Hardening v2 | Level 5 BLOCKED
