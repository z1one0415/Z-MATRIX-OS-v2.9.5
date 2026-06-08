# Factor Library Read-Only Adapter Planning — Invocation Request/Response Plan

## Status: Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING_INVOCATION_REQUEST_RESPONSE_PLAN_READY
Branch: plan/...factor-library-adapter | Base: 22252711 | Level 5: BLOCKED

## Scope
Plan the FactorInvocationRequest and FactorInvocationResponse adapter components. The calling convention for requesting factor data and receiving controlled read-only responses.

### FactorInvocationRequest (future)
- request_id (UUID: unique call identifier)
- caller (str: calling adapter/agent identifier)
- intent (enum: one of 8 canonical readonly intents)
- factor_selector (dict: factor_id, family_id, or filter criteria)
- subject (str: research subject identifier)
- horizon (enum: 5d, 10d, 20d, 60d, or flexible)
- permission_tier (int: T0-T3, no execution tier)
- output_mode (enum: evidence_only, summary_only, full_profile — none allows execution)
- execution_requested (const false — rejected if true)

### FactorInvocationResponse (future)
- response_id (UUID: correlates to request_id)
- decision (enum: from SkillOS response decision set)
- factor_manifest (optional: FactorManifest if intent=REGISTRY_READ)
- factor_profile (optional: FactorFamilyProfile if intent=RESEARCH_CONTEXT)
- evidence_envelope (optional: FactorEvidenceEnvelope if intent=EVIDENCE_READ)
- validation_snapshot (optional: FactorValidationSnapshot if intent=VALIDATION_SUMMARY)
- guardrail_profile (optional: FactorGuardrailProfile if intent=GUARDRAIL_SUMMARY)
- forbidden_outputs_removed (bool: true if any output was filtered)
- degraded (bool: true if decision is DENY_*)

### SkillOS Response Decision Enum
ALLOW_REGISTRY_ONLY | ALLOW_EVIDENCE_ONLY | ALLOW_VALIDATION_SUMMARY | ALLOW_GUARDRAIL_SUMMARY | ALLOW_CANDIDATE_MONITOR | ALLOW_READONLY_CONTEXT | ALLOW_COMPOSITION_GRAPH_DRY_PLAN | DENY_FACTOR_NOT_FOUND | DENY_FACTOR_NOT_VALIDATED | DENY_PIT_FAILED | DENY_COVERAGE_FAILED | DENY_FAMILY_OVERLAP | DENY_GUARDRAIL_FAILED | DENY_PROMOTION_NOT_ALLOWED | DENY_EXECUTION_FORBIDDEN

## Boundary: No implementation. Level 5 BLOCKED.

## Next: Evidence Envelope Plan.

> Factor Library | Planning | Invocation Request/Response | FUTURE_PLAN_ONLY | Level 5 BLOCKED