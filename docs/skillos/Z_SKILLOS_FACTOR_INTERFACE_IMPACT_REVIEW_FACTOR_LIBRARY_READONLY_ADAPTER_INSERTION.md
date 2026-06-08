# Factor Interface Impact Review — Factor Library Read-Only Adapter Insertion

## Status: Z_SKILLOS_FACTOR_INTERFACE_IMPACT_REVIEW_FACTOR_LIBRARY_READONLY_ADAPTER_INSERTION_READY
Branch: plan/...factor-interface-impact-review-a1-b1 | Level 5: BLOCKED

## Question
Should a Factor Library Read-Only Adapter Planning phase be inserted before A1/B1 merge?

## Analysis
A1 currently plans for 5 adapters: capability_registry_readonly, z9_memory_review_readonly, z2_research_output_readonly, local_report_reading, document_generation_in_memory. None of these cover the Factor Library domain. The parent interface baseline (d02b60c9) defines 8 canonical readonly intents that map to factor operations such as REGISTRY_READ, EVIDENCE_READ, VALIDATION_SUMMARY, GUARDRAIL_SUMMARY, CANDIDATE_MONITOR, RESEARCH_CONTEXT, SCORING_CONTEXT_DRY_PLAN, COMPOSITION_GRAPH_DRY_PLAN.

A1 cannot absorb Factor Library Read-Only Adapter without significant scope expansion. The factor interface requires specialized handling:
- FactorApplicationContract verification (readonly intent checking, blocked output filtering)
- FactorEvidenceEnvelope construction (request_hash, response_hash, decision_hash with factor-specific fields)
- Canonical intent routing (mapping intent to factor operation)
- Forbidden intent blocking (ALPHA_SIGNAL, ORDER_SIGNAL, PORTFOLIO_WEIGHT, PAPER_TRADING, BROKER_RUNTIME, REAL_TRADE, PRODUCTION)
- Batch3 factor-specific coverage (F21-F34)
- Degraded response for validation failures

B1 similarly cannot process FactorInvocationResponse payloads or apply blocked-output filtering without factor-specific node type support.

## Verdict: YES_INSERT_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING

## Recommended Sequence
1. Create `plan/skillos-factor-library-readonly-adapter-planning` branch (separate human decision)
2. Plan factor adapter covering all 8 canonical intents + Batch3 factors
3. After factor adapter planning is sealed, harden A1 with factor-interface dependency
4. Harden B1 with FactorInvocationResponse payload and blocked-output filtering
5. Then merge A1, then B1 in sequence

## Not Recommended
- Skipping factor adapter planning (would miss factor-specific contract validation)
- Absorbing factor adapter into A1 (scope too large, would delay A1)
- Merging A1/B1 now without factor alignment (would create technical debt)

## Boundary
No implementation. No code change. No merge. No branch creation without human decision. Level 5 BLOCKED.

> Factor Interface | Impact Review | Factor Library Insertion | Level 5 BLOCKED