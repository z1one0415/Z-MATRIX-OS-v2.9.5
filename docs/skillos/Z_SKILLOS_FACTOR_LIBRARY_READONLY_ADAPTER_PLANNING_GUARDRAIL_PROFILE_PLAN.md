# Factor Library Read-Only Adapter Planning — Guardrail Profile Plan

## Status: Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING_GUARDRAIL_PROFILE_PLAN_READY
Branch: plan/...factor-library-adapter | Base: 22252711 | Level 5: BLOCKED

## Scope
Plan the FactorGuardrailProfile read-only adapter component. Guardrail state and risk flags for factor safety assessment. No execution. Read-only.

### Guardrail Fields (future read-only)
- required_guardrails (list: which guardrails must pass for this factor)
- risk_flags (dict: risk flag name → {passed: bool, details: str, severity: low/med/high/critical})
- guardrail_state (enum: passed/failed/not_run)
- failure_mode (str: description of guardrail failure if failed)
- promotion_denial (bool: true if guardrail failure blocks promotion)
- crowding_gate (passed/failed: asset crowding within factor)
- turnover_gate (passed/failed: turnover rate within bounds)
- cost_gate (passed/failed: transaction cost within limits)
- pit_leakage_gate (passed/failed: no PIT leakage detected)
- disclosure_staleness_gate (passed/failed: disclosure recency meets threshold)

### Guardrail Denial Logic
If ANY guardrail_failed=True → DENY_GUARDRAIL_FAILED response
If crowding_gate=failed → DENY_CROWDING_EXCEEDED
If turnover_gate=failed → DENY_TURNOVER_EXCEEDED
All DENY responses return degraded state (DENY_NOOP), never blocking.

### Implementation Plan (future)
- FactorGuardrailProfile class in zmatrix_adapters/factor_library/guardrails.py
- Methods: get_guardrails, get_risk_flags (read-only)
- Tests in test_guardrails.py

## Parent Interface: d02b60c9. Guardrail profile for Batch3 factors.

## Boundary: No implementation. Level 5 BLOCKED.

## Forbidden: Same as OVERVIEW. No guardrail bypass. No silenced guardrails.

## Proof: Guardrail fields documented. Guardrail denial states defined.

## Next: Application Contract Plan.

> Factor Library | Planning | Guardrail Profile | FUTURE_PLAN_ONLY | Level 5 BLOCKED