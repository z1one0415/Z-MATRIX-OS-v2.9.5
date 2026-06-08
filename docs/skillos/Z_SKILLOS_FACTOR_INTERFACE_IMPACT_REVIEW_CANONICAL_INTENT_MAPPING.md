# Factor Interface Impact Review — Canonical Intent Mapping

## Status: Z_SKILLOS_FACTOR_INTERFACE_IMPACT_REVIEW_CANONICAL_INTENT_MAPPING_READY
Branch: plan/...factor-interface-impact-review-a1-b1 | Level 5: BLOCKED

## Canonical Readonly Intent Set (8)
| # | Canonical Intent | Legacy Alias | Factor Operation | A1 Coverage | B1 Coverage |
|:--:|:--|:--|:--|:--:|:--:|
| 1 | REGISTRY_READ | — | FactorManifest listing | MISSING | MISSING |
| 2 | EVIDENCE_READ | RESEARCH_EVIDENCE_READ | FactorEvidenceEnvelope retrieval | MISSING | MISSING |
| 3 | VALIDATION_SUMMARY | VALIDATION_SUMMARY_READ | FactorValidationSnapshot | MISSING | MISSING |
| 4 | GUARDRAIL_SUMMARY | GUARDRAIL_SUMMARY_READ | FactorGuardrailProfile | MISSING | MISSING |
| 5 | CANDIDATE_MONITOR | MONITORING_READ | Factor monitor cache | MISSING | MISSING |
| 6 | RESEARCH_CONTEXT | — | FactorFamilyProfile | MISSING | MISSING |
| 7 | SCORING_CONTEXT_DRY_PLAN | — | FactorScoringContext | MISSING | MISSING |
| 8 | COMPOSITION_GRAPH_DRY_PLAN | — | CompositionGraphInput | MISSING | PARTIAL |

## Forbidden Intent (7)
| Intent | Blocked By | Enforcement |
|:--|:--|:--|
| ALPHA_SIGNAL | FactorApplicationContract, blocked_outputs | CI + runtime |
| ORDER_SIGNAL | blocked_outputs | CI + runtime |
| PORTFOLIO_WEIGHT | blocked_outputs | CI + runtime |
| PAPER_TRADING | blocked_application_modes | CI + runtime |
| BROKER_RUNTIME | blocked_application_modes | CI + runtime |
| REAL_TRADE | blocked_application_modes, production/broker/real_trade | CI + runtime |
| PRODUCTION | blocked_application_modes, Level 5 BLOCKED | CI + runtime |

## SkillOS Response Decision Enum (Recommended)
### ALLOW Responses
| Decision | Condition | Permission Tier |
|:--|:--|:--:|
| ALLOW_REGISTRY_ONLY | Factor exists in registry | T1 |
| ALLOW_EVIDENCE_ONLY | Factor validated and evidence available | T2 |
| ALLOW_VALIDATION_SUMMARY | Factor validation snapshot ready | T2 |
| ALLOW_GUARDRAIL_SUMMARY | Guardrail passed | T2 |
| ALLOW_CANDIDATE_MONITOR | Candidate in watchlist | T2 |
| ALLOW_READONLY_CONTEXT | Family context resolved | T3 |
| ALLOW_COMPOSITION_GRAPH_DRY_PLAN | All gates pass | T4 |

### DENY Responses
| Decision | Condition | Fallback |
|:--|:--|:--|
| DENY_FACTOR_NOT_FOUND | Factor not in registry | DENY_NOOP |
| DENY_FACTOR_NOT_VALIDATED | Validation not run | DENY_NOOP |
| DENY_PIT_FAILED | PIT leakage detected | PLAN_ONLY |
| DENY_COVERAGE_FAILED | Coverage insufficient | PLAN_ONLY |
| DENY_FAMILY_OVERLAP | Family overlap detected | DENY_NOOP |
| DENY_GUARDRAIL_FAILED | Guardrail triggered | DENY_NOOP |
| DENY_PROMOTION_NOT_ALLOWED | alpha_claim blocked | DENY_NOOP |
| DENY_EXECUTION_FORBIDDEN | execution_requested const false | DENY_NOOP |

## Mapping to WAVE0 P0 Gate Model
| Gate | Impact | Action |
|:--|:--|:--|
| Permission gate | Factor canonical intent as permission tier | Extend permission schema |
| Evidence gate | FactorEvidenceEnvelope in evidence schema | Add factor evidence fields |
| Individual adapter gate | Factor library as new adapter type | Add to adapter registry |

## Boundary
No implementation. No code change. Level 5 BLOCKED.

> Factor Interface | Impact Review | Canonical Intent Mapping | Level 5 BLOCKED