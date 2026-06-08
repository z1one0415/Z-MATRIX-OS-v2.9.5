# Factor Library Read-Only Adapter Planning — Overview

## Status: Z_SKILLOS_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING_OVERVIEW_READY
Branch: plan/...factor-library-readonly-adapter-planning | Base: postmerge @ 22252711 | Level 5: BLOCKED

## Purpose
FUTURE_PLAN_ONLY. Docs-only. Plan the Factor Library Read-Only Adapter — a dedicated adapter for reading factor library data through the WAVE0 controlled read-only execution framework. This adapter is the required prerequisite for A1 (Z-MATRIX Module Adapter) and B1 (Skill Composition Graph) alignment hardening. It cannot be absorbed into A1's 5 planned generic adapters because factor library data requires specialized contract validation, canonical intent routing, and blocked-output filtering.

## Scope
- FactorManifest: list available factors with metadata and lifecycle status
- FactorFamilyProfile: retrieve family-grouping, overlap detection, orthogonality rules
- FactorValidationSnapshot: validation results, coverage, PIT, single-factor, true-OOS
- FactorGuardrailProfile: guardrail state (passed/failed/not_run), risk flags
- FactorApplicationContract: allowed modes 8/8, blocked modes 7/7, blocked outputs 5/5, blocked downstream 4/4
- FactorEvidenceEnvelope: source_commit, artifact_refs, evidence hashes (manifest, formula, validation, guardrail, contract)
- FactorInvocationRequest / FactorInvocationResponse: calling convention, decision enum, forbidden output removal
- Canonical intent mapping: 8 intents with legacy alias coverage
- Permission and output filtering: alpha_claim removal, position_weight removal, buy/sell signal removal

## Parent Interface Dependencies
- Parent factor interface baseline: d02b60c9 (V13.F5.1.2.1_INTERFACE_VOCABULARY_NORMALIZATION_ACCEPTED)
- Impact review post-merge seal: 22252711
- Impact review recommendations: C1 accepted, A1/B1 blocked until this adapter is planned

## Canonical Readonly Intents (8)
1. REGISTRY_READ (factor listing)
2. EVIDENCE_READ (evidence retrieval)
3. VALIDATION_SUMMARY (validation snapshots)
4. GUARDRAIL_SUMMARY (guardrail profiles)
5. CANDIDATE_MONITOR (monitor candidate state)
6. RESEARCH_CONTEXT (family context)
7. SCORING_CONTEXT_DRY_PLAN (scoring — dry plan only)
8. COMPOSITION_GRAPH_DRY_PLAN (composition — dry plan only)

## Batch3 Factors Covered
F21, F22, F24, F26, F27, F30, F31, F34

## Boundary
No implementation. No code change. No test change. No research file change. No runtime enablement. No adapter execution enablement. No capability execution. No real factor call. No real Z-MATRIX module call. No network call. No file read/write. No production/broker/real_trade. No alpha claim. No paper trading. No result_envelope mutation. No warning enablement. No blocking/fail-closed. No tag. Level 5 remains BLOCKED.

## Forbidden Actions
Implementation code | Code/test changes | Research file changes | Runtime enablement | Adapter execution enablement | Capability execution | Real factor call | Real Z-MATRIX call | Network call | File write | External publish | Production/broker/real_trade | Alpha claim | Paper trading | Tag | Level 5 planning

## Proof / Review Requirements
24 proof categories defined in TEST_AND_PROOF_PLAN: docs-only, no code, no tests, no research, no runtime enablement, no adapter execution, no capability execution, no real factor call, no Z-MATRIX call, canonical intent coverage (8), legacy alias coverage (4), blocked modes 7/7, blocked outputs 5/5, blocked downstream 4/4, execution_requested=false, promotion_allowed=false, alpha_claim_allowed=false, production/broker/real_trade BLOCKED, FactorEvidenceEnvelope source_commit, C1 evidence dependency, A1 alignment dependency, B1 alignment dependency, no result_envelope mutation, no Level 5.

## Next Legal Entry
Human merge approval decision only. After merge: A1 factor-interface alignment hardening, then B1 FactorInvocationResponse alignment hardening.

> Factor Library | Planning | Overview | FUTURE_PLAN_ONLY | Level 5 BLOCKED