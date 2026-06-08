# Factor Library Read-Only Adapter Planning — Factor Manifest Plan

## Status: Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING_FACTOR_MANIFEST_PLAN_READY
Branch: plan/...factor-library-adapter | Base: 22252711 | Level 5: BLOCKED

## Scope
Plan the FactorManifest read-only adapter component. Provides factor listing and metadata. No execution, no alpha.

### Manifest Fields (future read-only)
- factor_id (unique identifier)
- factor_name (human-readable name)
- factor_family_id (family grouping)
- factor_status (active, monitoring, rejected, retired)
- factor_type (pricing, fundamental, alternative, sentiment)
- formula_ref (reference to factor formula)
- source_data_refs (data source references)
- universe_policy (universe filter: csi300, csi500, csi800, full_a)
- asof_policy (as-of date policy: strict, flexible, snapshot)
- horizon_policy (prediction horizon: 5d, 10d, 20d, 60d)
- lifecycle locks (cannot modify once in promotion)
- runtime boundary locks (cannot execute if production/broker/real_trade)

### Implementation Plan (future)
- FactorManifest class in skillos/capability_invocation_os/zmatrix_adapters/factor_library/
- manifest.py with display/manifest/list methods (read-only)
- tests/skillos/capability_invocation_os/zmatrix_adapters/factor_library/test_manifest.py
- No code in this planning phase.

## Parent Interface: d02b60c9. Batch3: F21-F34.

## Boundary: No implementation. No code. Level 5 BLOCKED.

## Forbidden: Same as OVERVIEW.

## Proof: Manifest fields documented. No execution implied.

## Next: Family Profile Plan.

> Factor Library | Planning | Factor Manifest | FUTURE_PLAN_ONLY | Level 5 BLOCKED