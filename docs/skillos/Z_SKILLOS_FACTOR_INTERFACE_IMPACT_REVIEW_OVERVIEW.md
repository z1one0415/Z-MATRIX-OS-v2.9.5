# Factor Interface Impact Review — Overview

## Status: Z_SKILLOS_FACTOR_INTERFACE_IMPACT_REVIEW_STARTED
Branch: plan/...factor-interface-impact-review-a1-b1 | Base: postmerge @ be845735 | Level 5: BLOCKED

## Purpose
FUTURE_PLAN_ONLY. Docs-only. Review the impact of the Factor Application Standard Interface v1 (accepted at d02b60c9, V13.F5.1.2.1_INTERFACE_VOCABULARY_NORMALIZATION_ACCEPTED) on SkillOS A1 (Z-MATRIX Module Adapter Implementation Planning) and B1 (Skill Composition Graph P0 Implementation Planning). Determine whether A1/B1 need factor-interface alignment hardening, whether a Factor Library Read-Only Adapter Planning phase must be inserted, and whether C1 requires any rework.

## Scope
- Review parent interface baseline: Batch3 F21/F22/F24/F26/F27/F30/F31/F34 with canonical readonly intent
- Map 8 canonical intents (REGISTRY_READ through COMPOSITION_GRAPH_DRY_PLAN) to A1 capabilities
- Evaluate B1's FactorInvocationResponse node payload support
- Assess insertion requirement for Factor Library Read-Only Adapter Planning
- Answer 6 specific questions about A1, B1, C1, and next steps

## Out of Scope
Implementation. Code changes. Test changes. A1/B1 hardening (that's future). Factor Library Adapter branch creation (that requires separate human decision). Runtime enablement. Adapter execution. Capability execution. Real factor calls. Real Z-MATRIX calls.

## Dependency
- Parent interface baseline: d02b60c9 (INTERFACE_VOCABULARY_NORMALIZATION_ACCEPTED)
- Batch3 factors: F21, F22, F24, F26, F27, F30, F31, F34
- A1 branch: plan/...zmatrix-module-adapter-implementation-planning @ 0ad10a6d
- B1 branch: plan/...skill-composition-graph-p0-implementation-planning @ 01cf80ff
- C1: Already merged and sealed (be845735)

## Canonical Readonly Intent Set
| # | Intent | Legacy Alias | Forbidden? |
|:--:|:--|:--|:--:|
| 1 | REGISTRY_READ | — | No |
| 2 | EVIDENCE_READ | RESEARCH_EVIDENCE_READ | No |
| 3 | VALIDATION_SUMMARY | VALIDATION_SUMMARY_READ | No |
| 4 | GUARDRAIL_SUMMARY | GUARDRAIL_SUMMARY_READ | No |
| 5 | CANDIDATE_MONITOR | MONITORING_READ | No |
| 6 | RESEARCH_CONTEXT | — | No |
| 7 | SCORING_CONTEXT_DRY_PLAN | — | No |
| 8 | COMPOSITION_GRAPH_DRY_PLAN | — | No |

## Boundary
No implementation. No code change. No test change. No runtime enablement. No adapter execution enablement. No capability execution. No real factor call. No real Z-MATRIX call. No network call. No file read/write. No production/broker/real_trade. No alpha claim. No paper trading. No result_envelope mutation. Level 5 remains BLOCKED.

## Next Legal Entry
Human Factor Interface Impact Review Decision. Then: Factor Library Read-Only Adapter Planning or A1/B1 alignment hardening or both.

> Factor Interface | Impact Review | Overview | FUTURE_PLAN_ONLY | Level 5 BLOCKED