# Z-SkillOS Capability Invocation OS Policy Router Implementation Plan

## Status
Z_SKILLOS_POLICY_ROUTER_IMPLEMENTATION_PLAN_READY

## Scope
FUTURE_PLAN_ONLY. Intent-to-execution routing plan. No runtime router code.

## Router Pipeline
1. Intent classification: parse caller intent into structured request
2. Skill candidate selection: match intent against registry
3. Risk tier evaluation: classify all candidate skills by tier
4. Permission decision: check caller authorization per skill
5. Execution mode selection: T0-T4 based on risk tier
6. Human gate escalation: T3/T4 require human approval
7. Execution plan generation: ordered skill sequence with evidence handoff
8. Deny-by-default: unknown intent → deny, unknown skill → deny

## Tier Execution Rules
- T0 (docs-only): auto-execute, no human gate
- T1 (analysis-only): auto-execute, evidence required
- T2 (code/local): permission + evidence required
- T3 (advisory): human approval + permission + evidence
- T4 (external): human approval + permission + evidence + rollback plan
- T5 (blocked): NEVER EXECUTE, immediate deny

## Forbidden
Router cannot bypass contract validation, skip risk tier evaluation, override T5 block, execute without evidence capture plan, or have production/broker/real_trade routing paths.

## Future Proof Plan
test_router_intent_classification, test_router_tier_escalation, test_router_human_gate, test_router_T5_deny, test_router_production_blocked

## No runtime router code. Level 5 remains BLOCKED.
