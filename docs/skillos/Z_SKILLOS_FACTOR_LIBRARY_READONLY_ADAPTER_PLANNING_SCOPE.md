# Factor Library Read-Only Adapter Planning — Scope

## Status: Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING_SCOPE_READY
Branch: plan/...factor-library-adapter | Base: 22252711 | Level 5: BLOCKED

## Scope
FUTURE_PLAN_ONLY. Docs-only. This adapter is for reading factor library data only. No execution, no trading, no alpha generation.

### Allowed Adapter Methods
1. `list_factors` — list available factors with metadata
2. `get_factor_profile` — retrieve FactorFamilyProfile
3. `get_factor_evidence` — retrieve FactorEvidenceEnvelope
4. `monitor_candidates` — read candidate monitor state
5. `build_research_context` — compose read-only research context

### Forbidden Method Names
execute | run | call | invoke | trade | optimize | backtest_live | generate_alpha | execute_trade | submit_order | deploy_to_production | run_broker

## Parent Interface Dependency
- Factor Interface baseline d02b60c9
- Impact Review post-merge seal 22252711
- Batch3: F21, F22, F24, F26, F27, F30, F31, F34

## Boundary
No implementation. No code. No tests. No research files. No enablement. Level 5 BLOCKED.

## Forbidden
Same as OVERVIEW plus: no research/factor_library file read in this phase (planning only), no skillos/ code changes.

## Proof
24 proof categories. All scope items documented.

## Next
Factor Manifest → Family Profile → Validation Snapshot → Guardrail Profile → Application Contract → Invocation Request/Response → Evidence Envelope → Canonical Intent → Permission & Output Filter → Test & Proof → Closeout → Seal

> Factor Library | Planning | Scope | FUTURE_PLAN_ONLY | Level 5 BLOCKED