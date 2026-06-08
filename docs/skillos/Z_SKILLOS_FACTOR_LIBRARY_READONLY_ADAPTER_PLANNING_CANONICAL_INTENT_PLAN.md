# Factor Library Read-Only Adapter Planning — Canonical Intent Plan

## Status: Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING_CANONICAL_INTENT_PLAN_READY
Branch: plan/...factor-library-adapter | Base: 22252711 | Level 5: BLOCKED

## Scope
Plan the canonical intent mapping for the factor library read-only adapter. Map 8 canonical intents, legacy aliases, and forbid 7 intents. No implicit translation at runtime.

### Canonical Intents (8)
| # | Canonical | Legacy Alias | Action |
|:--:|:--|:--|:--|
| 1 | REGISTRY_READ | — | Factor registry listing |
| 2 | EVIDENCE_READ | RESEARCH_EVIDENCE_READ | Evidence retrieval |
| 3 | VALIDATION_SUMMARY | VALIDATION_SUMMARY_READ | Validation snapshot |
| 4 | GUARDRAIL_SUMMARY | GUARDRAIL_SUMMARY_READ | Guardrail profile |
| 5 | CANDIDATE_MONITOR | MONITORING_READ | Candidate monitoring |
| 6 | RESEARCH_CONTEXT | — | Family context |
| 7 | SCORING_CONTEXT_DRY_PLAN | — | Scoring dry plan |
| 8 | COMPOSITION_GRAPH_DRY_PLAN | — | Composition dry plan |

### Forbidden Intents (7)
ALPHA_SIGNAL, PORTFOLIO_WEIGHT, ORDER_SIGNAL, PAPER_TRADING, BROKER_RUNTIME, REAL_TRADE, PRODUCTION

### Legacy Alias Coverage (4)
RESEARCH_EVIDENCE_READ → redirect to EVIDENCE_READ
VALIDATION_SUMMARY_READ → redirect to VALIDATION_SUMMARY
GUARDRAIL_SUMMARY_READ → redirect to GUARDRAIL_SUMMARY
MONITORING_READ → redirect to CANDIDATE_MONITOR

### Rules
- No implicit translation at runtime — legacy aliases are explicitly mapped in adapter config
- No legacy mode in adapter output — all responses use canonical intent names
- Forbidden intents return DENY immediately — no processing
- Canonical intent determines which data fields are populated in response
- intent→action mapping is 1:1 — no composite intents

## Boundary: No implementation. Level 5 BLOCKED.

## Next: Permission and Output Filter Plan.

> Factor Library | Planning | Canonical Intent | FUTURE_PLAN_ONLY | Level 5 BLOCKED