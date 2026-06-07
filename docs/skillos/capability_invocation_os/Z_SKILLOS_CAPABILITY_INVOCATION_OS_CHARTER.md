# Z-SkillOS Capability Invocation OS Charter

## Status

Z_SKILLOS_CAPABILITY_INVOCATION_OS_CHARTER_READY

## Purpose

Enable safe, non-drifting, auditable, permissioned invocation of Z-MATRIX capabilities through a unified Capability Invocation OS architecture.

## Scope

| Component | Scope |
|:--|:--|
| Capability Registry | Catalog all Z-MATRIX skills with schemas, risk tiers, permissions |
| Skill Contracts | Standardized input/output/side-effect/audit contracts per skill |
| Policy Router | Intent → capability selection → risk tier → policy gate → execution mode |
| Composition Engine | Safe chaining of multiple skills with evidence handoff |
| Permission/Risk Tier Model | Tier 0–5 classification (docs-only through blocked) |
| Evidence Bus | End-to-end audit trails, no deletion, versioned |
| Runtime Guard | Preflight + permission + contract + side-effect + postcondition checks |
| Module Adapters | Per-module adapters (Wave 0–4 planning) |
| Scenario Tests | End-to-end composed skill chain tests |

## Non-Scope

| Item | Status |
|:--|:--|
| Runtime implementation | NOT IN SCOPE |
| Adapter implementation | NOT IN SCOPE |
| Warning enablement | NOT IN SCOPE |
| Production/broker/real_trade | PERMANENTLY EXCLUDED |
| Level 5 (Fail-Closed) | BLOCKED |
| P1 warning implementation | NOT IN SCOPE |

## Principles

1. **Safe by default**: deny unless explicitly permitted
2. **Auditable**: every invocation leaves evidence
3. **Non-drifting**: contracts are hash-locked
4. **Reversible**: rollback path required for every skill
5. **Human-gated**: high-risk tiers require human approval
6. **Isolation**: production/broker/real_trade never reachable

## Branch

`plan/skillos-capability-invocation-os-planning`

## Level 5 Boundary

Level 5 remains BLOCKED unless separately authorized by a future explicit Level 5 planning gate.
