# Factor Interface Impact Review — Decision Brief

## Status: Z_SKILLOS_FACTOR_INTERFACE_IMPACT_REVIEW_DECISION_BRIEF_READY
Branch: plan/...factor-interface-impact-review-a1-b1 | Level 5: BLOCKED

## Recommendation
**APPROVE_INSERT_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING**

## Context
Factor Application Standard Interface v1 was accepted at d02b60c9 (V13.F5.1.2.1). Impact review of A1 and B1 shows both need factor-interface alignment before they can merge. A Factor Library Read-Only Adapter must be planned first to serve as the factor-facing contract layer.

## Key Findings

### A1: Z-MATRIX Module Adapter Implementation Planning
- 0/8 canonical intents covered
- 0/8 Factor Library components (Manifest, FamilyProfile, ValidationSnapshot, GuardrailProfile, ApplicationContract, EvidenceEnvelope, InvocationRequest, InvocationResponse)
- Batch3 factors F21-F34 not addressed
- Verdict: A1_NEEDS_FACTOR_INTERFACE_ALIGNMENT_HARDENING

### B1: Skill Composition Graph P0 Implementation Planning
- No FactorInvocationResponse as supported node payload
- No canonical intent permission propagation
- No blocked-output filtering on edges (alpha_claim, position_weight, buy_signal, sell_signal)
- No degraded node states for 8 DENY conditions
- Verdict: B1_NEEDS_FACTOR_INTERFACE_ALIGNMENT_HARDENING

### C1: Read-Only Invocation Sandbox Evidence
- Generic evidence schema handles all source classes
- `source_class=factor` is just one more value, no schema change needed
- Verdict: C1_ACCEPTED_AS_MERGED_NO_REWORK_REQUIRED

## Human Decision Options

| # | Option | Meaning | Consequence |
|:--:|:--|:--|:--|
| 1 | **APPROVE_INSERT_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING** | Insert Factor Library Read-Only Adapter Planning before A1/B1 merge | A1/B1 blocked until factor adapter planning sealed |
| 2 | REQUEST_A1_B1_ALIGNMENT_DETAILS | Need more detail on A1/B1 factor gap | Review branch updated before any planning |
| 3 | REJECT_FACTOR_ADAPTER_INSERTION_AND_KEEP_GENERIC | Skip factor adapter, keep generic Z-MATRIX adapter | A1/B1 can merge but factor coverage will be incomplete until refactored |
| 4 | PAUSE_SKILLOS_FACTOR_INTEGRATION | Halt all factor-related work | A1/B1 merge as-is with documented gaps |

## Recommended: Option 1 — APPROVE_INSERT_FACTOR_LIBRARY_READONLY_ADAPTER_PLANNING

### Rationale
- Factor Library is a distinct domain (8 intents, Batch3 factors, contract validation) that cannot be absorbed into A1's 5 planned adapters
- B1's composition graph will produce invalid results without canonical intent propagation and blocked-output filtering
- C1 is unaffected and remains merged
- Factor adapter planning is a docs-only phase with low risk

### Rejected Automatic Actions
These actions are NOT authorized by this decision and require separate human approval:
- Auto-create Factor Library Adapter Planning branch
- Auto-merge A1
- Auto-merge B1
- Start Factor Adapter implementation

## This is a decision document. Human must decide. No auto-decision. No auto-merge.

> Factor Interface | Impact Review | Decision Brief | Level 5 BLOCKED