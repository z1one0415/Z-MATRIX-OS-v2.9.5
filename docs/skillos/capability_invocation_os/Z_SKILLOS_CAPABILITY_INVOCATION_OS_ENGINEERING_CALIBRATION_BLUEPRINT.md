# Z-SkillOS Capability Invocation OS Engineering Calibration Blueprint

## Status

Z_SKILLOS_CAPABILITY_INVOCATION_OS_BLUEPRINT_READY

## Current State Assessment

Z-SkillOS currently does NOT satisfy safe, auditable, permissioned invocation of the full Z-MATRIX capability surface.

What IS complete:
- Governance chain (Level 0-2): documentation, audit, CI integration
- P0 disabled-default skeleton: 5 modules, 64/64 tests, strict bool True only
- P1 side-channel planning: 12 planning docs + review/merge package, merged and sealed

What is NOT yet in place:
- Capability registry for Z-MATRIX skills (Z2, Z8, Z9, V3, B/R/D-Matrix, etc.)
- Skill contracts with input/output schemas, risk tiers, permissions
- Policy router for intent classification and execution mode selection
- Composition engine for chaining skills in safe sequences
- Permission/risk tier model for distinguishing docs-only from external-write
- Evidence bus for end-to-end audit trails
- Runtime invocation guard (preflight + permission + contract + side-effect checks)
- Module adapters for Z-MATRIX capabilities
- End-to-end scenario tests across composed skill chains

## New Goal

**Capability Invocation OS**: a super-gate planning package that defines the complete architecture for safe, non-drifting, auditable, permissioned invocation of Z-MATRIX capabilities.

## Compression Strategy

Phase 1–7 from the original roadmap can be compressed into a single **docs-only planning super-gate**:

| Original Phase | Compressed Into |
|:--|:--|
| Phase 1: Registry | Capability Registry Schema |
| Phase 2: Contracts | Skill Contract Standard |
| Phase 3: Router | Policy Router Design |
| Phase 4: Composition | Composition Graph Design |
| Phase 5: Permissions | Permission Risk Tier Model |
| Phase 6: Evidence | Evidence Bus Design |
| Phase 7: Guard | Runtime Invocation Guard Design |

What CANNOT be compressed:
- Runtime implementation
- Adapter implementation (Z2/Z8/Z9/V3 integration)
- P1 warning implementation
- Production/broker/real_trade
- Warning enablement

## Baseline

| Field | Value |
|:--|:--|
| Commit | `ac9612ea57ecb7ec2d55770a216ee68ace98f7ae` |
| Branch | `plan/skillos-capability-invocation-os-planning` |
| P1 seal | `Z_SKILLOS_LEVEL4_P1_PLANNING_POST_MERGE_SEALED` |

## Capability Surface Coverage (Planned)

| Module | Adapter Status | Risk Tier |
|:--|:--|:--:|
| Z2 信息熔炉 | Planning | T2 |
| Z8 投资执行 | Planning | T3 |
| Z9 预测引擎 | Planning | T2 |
| V3 量化引擎 | Planning | T2 |
| B/R/D-Matrix | Planning | T2 |
| World Blocks OS | Planning | T2 |
| Deal Compass | Planning | T2 |
| MissNail Business Model | Planning | T2 |
| GitHub Engineering | Planning | T2 |
| Document/HTML Report Gen | Planning | T1 |

## Still Forbidden

Runtime implementation, adapter code, P1 warning implementation, caller-visible warning, result_envelope mutation, blocking, fail-closed, production/broker/real_trade, V12.x, tag, Level 5 planning.

## Level 5 Boundary

Level 5 remains BLOCKED unless separately authorized by a future explicit Level 5 planning gate.
