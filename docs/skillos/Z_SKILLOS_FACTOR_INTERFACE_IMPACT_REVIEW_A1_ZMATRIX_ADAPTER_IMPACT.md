# Factor Interface Impact Review — A1 Z-MATRIX Module Adapter Impact

## Status: Z_SKILLOS_FACTOR_INTERFACE_IMPACT_REVIEW_A1_ZMATRIX_ADAPTER_IMPACT_READY
Branch: plan/...factor-interface-impact-review-a1-b1 | Level 5: BLOCKED

## Scope
Evaluate A1 (Z-MATRIX Module Adapter Implementation Planning @ 0ad10a6d) against the parent Factor Interface baseline d02b60c9.

## Coverage Check

| Factor Interface Component | A1 Coverage | Verdict |
|:--|:--:|:--:|
| FactorManifest | NOT_IN_A1_SCOPE | MISSING |
| FactorFamilyProfile | NOT_IN_A1_SCOPE | MISSING |
| FactorValidationSnapshot | NOT_IN_A1_SCOPE | MISSING |
| FactorGuardrailProfile | NOT_IN_A1_SCOPE | MISSING |
| FactorApplicationContract | NOT_IN_A1_SCOPE | MISSING |
| FactorEvidenceEnvelope | NOT_IN_A1_SCOPE | MISSING |
| FactorInvocationRequest | NOT_IN_A1_SCOPE | MISSING |
| FactorInvocationResponse | NOT_IN_A1_SCOPE | MISSING |
| Canonical readonly intent set (8) | NOT_IN_A1_SCOPE | MISSING |
| Batch3 factors F21-F34 | NOT_IN_A1_SCOPE | MISSING |
| production/broker/real_trade blocked | Already in A1 | PASS |
| alpha_claim blocked | Already in A1 | PASS |

## Verdict: A1_NEEDS_FACTOR_INTERFACE_ALIGNMENT_HARDENING

### Reasoning
A1 plans for 5 first-batch adapters:
1. capability_registry_readonly
2. z9_memory_review_readonly
3. z2_research_output_readonly
4. local_report_reading
5. document_generation_in_memory

None of these cover the Factor Library domain. A1 needs a separate `factor_library_readonly` adapter that implements:
- FactorManifest parsing
- FactorFamilyProfile lookup
- FactorApplicationContract verification
- FactorEvidenceEnvelope construction
- Canonical intent filtering
- blocked-output enforcement
- alpha_claim removal

### Missing Items Required for Alignment
- FactorManifest adapter capability
- FactorFamilyProfile query capability
- FactorContract validation hook
- FactorEvidenceEnvelope in evidence schema
- Canonical intent routing (8 intents)
- Forbidden intent blocking (7 forbidden)
- Batch3 factor-specific coverage
- downgraded permission for failed validation
- degraded response for guardrail/pit/coverage failures

## Recommendation
Insert Factor Library Read-Only Adapter Planning as a separate phase before A1 finalizes its adapter suite. After the factor adapter is planned, harden A1 with the factor-interface dependency and batch3 coverage.

## Boundary
No implementation. No code change. No merge. Level 5 BLOCKED.

> Factor Interface | Impact Review | A1 Impact | Level 5 BLOCKED