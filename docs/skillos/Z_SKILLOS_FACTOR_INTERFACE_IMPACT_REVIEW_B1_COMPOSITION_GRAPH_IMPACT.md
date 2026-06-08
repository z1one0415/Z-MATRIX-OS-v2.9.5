# Factor Interface Impact Review — B1 Composition Graph Impact

## Status: Z_SKILLOS_FACTOR_INTERFACE_IMPACT_REVIEW_B1_COMPOSITION_GRAPH_IMPACT_READY
Branch: plan/...factor-interface-impact-review-a1-b1 | Level 5: BLOCKED

## Scope
Evaluate B1 (Skill Composition Graph P0 Implementation Planning @ 01cf80ff) against the parent Factor Interface baseline d02b60c9.

## Coverage Check

| B1 Capability | Factor Interface Support | Verdict |
|:--|:--|:--:|
| Single-node dry plan | No FactorInvocationResponse payload | MISSING |
| Two-node sequential plan | No FactorInvocationResponse in edge contract | MISSING |
| Node contract (capability_id, module adapter id) | No factor-specific node type | MISSING |
| Evidence propagation (node evidence hash) | No FactorEvidenceEnvelope hash support | MISSING |
| Permission propagation | No canonical intent propagation | MISSING |
| Degradation to noop/plan-only | No degraded state for denied factor | MISSING |
| Output boundary | No blocked-output filtering | MISSING |
| No cyclic graph | Not impacted | PASS |
| No result_envelope mutation | Already in B1 | PASS |
| No fail-closed | Already in B1 | PASS |

## Verdict: B1_NEEDS_FACTOR_INTERFACE_ALIGNMENT_HARDENING

### Missing Items Required for Alignment
- FactorInvocationResponse as supported node payload type
- FactorEvidenceEnvelope hash computation in evidence propagation
- Canonical intent permission propagation (T1-T4 mapping to 8 intents)
- blocked-output filtering on graph edge (remove alpha/signal/weight)
- alpha_claim removal from any node output
- degraded node state for:
  - DENY_FACTOR_NOT_FOUND
  - DENY_FACTOR_NOT_VALIDATED
  - DENY_PIT_FAILED
  - DENY_COVERAGE_FAILED
  - DENY_FAMILY_OVERLAP
  - DENY_GUARDRAIL_FAILED
  - DENY_PROMOTION_NOT_ALLOWED
  - DENY_EXECUTION_FORBIDDEN
- No-cyclic-graph still enforced
- No result_envelope mutation still enforced

### SkillOS Response Decision Enum (Recommended Minimum)
`ALLOW_REGISTRY_ONLY`, `ALLOW_EVIDENCE_ONLY`, `ALLOW_VALIDATION_SUMMARY`, `ALLOW_GUARDRAIL_SUMMARY`, `ALLOW_CANDIDATE_MONITOR`, `ALLOW_READONLY_CONTEXT`, `ALLOW_COMPOSITION_GRAPH_DRY_PLAN`, `DENY_FACTOR_NOT_FOUND`, `DENY_FACTOR_NOT_VALIDATED`, `DENY_PIT_FAILED`, `DENY_COVERAGE_FAILED`, `DENY_FAMILY_OVERLAP`, `DENY_GUARDRAIL_FAILED`, `DENY_PROMOTION_NOT_ALLOWED`, `DENY_EXECUTION_FORBIDDEN`

## Recommendation
Hardening B1 after Factor Library Read-Only Adapter is defined. The composition graph needs to understand factor evidence and factor permission tiers to propagate them correctly through multi-node plans.

## Boundary
No implementation. No code change. No merge. Level 5 BLOCKED.

> Factor Interface | Impact Review | B1 Impact | Level 5 BLOCKED