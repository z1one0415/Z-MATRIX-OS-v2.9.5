# Z-SkillOS Capability Invocation OS Runtime Policy Router Implementation Plan

## Status
Z_SKILLOS_RUNTIME_POLICY_ROUTER_IMPLEMENTATION_PLAN_READY

## Scope
FUTURE_PLAN_ONLY. Intent-to-execution routing design. No runtime router code.

## Router Pipeline
1. Request classification: parse caller intent into structured request
2. Capability candidate lookup: match intent against registry
3. Risk tier decision: classify by T0-T5
4. Permission decision: check authorization
5. Execution mode decision: T0-T4 based on tier
6. Human gate escalation: T3/T4 → human approval required
7. Deny-by-default: unknown intent → deny, unknown skill → deny

## Tier Rules: T0 auto, T1 auto+evidence, T2 permission+evidence, T3 human+permission+evidence, T4 human+permission+evidence+rollback, T5 NEVER EXECUTE.

## Forbidden: No bypass of contract, no skip tier, no T5 override, no execution without evidence plan, no production routing.

## No runtime code. Level 5 remains BLOCKED.
