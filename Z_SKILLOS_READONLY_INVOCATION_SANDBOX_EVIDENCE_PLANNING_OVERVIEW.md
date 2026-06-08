# Z-SkillOS Readonly Invocation Sandbox Evidence Planning — OVERVIEW

## Status
Z_SKILLOS_READONLY_INVOCATION_SANDBOX_EVIDENCE_PLANNING_OVERVIEW_READY

## Scope
This document defines the architectural overview for the SkillOS Readonly Invocation Sandbox Evidence Planning package. The system provides a controlled, evidence-verifiable execution environment for skill invocations that MUST NOT mutate any persistent state. All operations are confined to in-memory transient execution with cryptographic evidence trails.

The planning package covers three phases:
1. **Planning Phase** — Architecture, schema, contracts, gates, privacy boundaries
2. **Review Phase** — Human-in-the-loop gate review, risk register, decision record
3. **Merge Phase** — Merge readiness, checklist verification, final human sign-off

## Evidence
The evidence model is hash-only by design:
- `request_hash` — SHA-256 of the serialized invocation request
- `response_hash` — Placeholder hash for the expected response shape (not computed at runtime)
- `decision_hash` — Hash binding the request to its permission tier and adapter identity
- `adapter_id` — Opaque identifier for the skill adapter being invoked
- `permission_tier` — Numeric tier (0-4) governing allowed operations
- `source_class` — Origin classification (HUMAN, AGENT, SYSTEM, SCHEDULED)
- `rollback_marker` — Placeholder for rollback point identification

No file-based evidence is written. All evidence chains exist only in-memory during the invocation lifecycle.

## Boundary
- **In-scope**: Readonly execution sandbox planning, evidence schema design, hash-chain specification, privacy boundary definition, gate model, audit sink design, rollback recovery planning, human review gates.
- **Out-of-scope**: Runtime implementation, actual sandbox construction, file-system evidence persistence, network-level audit forwarding, production deployment, performance benchmarking.
- **Phase boundary**: This is PLANNING ONLY. No code is written. No runtime is affected.

## Forbidden
1. NO file writes during readonly invocation evidence collection
2. NO runtime_audit persistence to disk or network
3. NO hidden persistence mechanisms (cookies, env vars, temp files, IPC state)
4. NO evidence leakage across invocation boundaries
5. NO implicit evidence collection without explicit invocation consent
6. Level 5 BLOCKED — all mutation paths are sealed at the planning level

## Proof
- Planning documents are self-consistent and cross-referenced
- Hash-only evidence model eliminates side-channel persistence risks
- Privacy boundary guarantees no cross-invocation data bleed
- Rollback plan provides deterministic recovery from any state
- Gate model enforces human review before any merge to main

## Next
1. Review and approve all 14 planning documents
2. Proceed to Review Phase (7 documents) with human gate
3. Complete Merge Phase (5 documents) with final human sign-off
4. Await WAVE0_CONTROLLED_READONLY_EXECUTION_P0_POST_MERGE_SEALED dependency resolution
