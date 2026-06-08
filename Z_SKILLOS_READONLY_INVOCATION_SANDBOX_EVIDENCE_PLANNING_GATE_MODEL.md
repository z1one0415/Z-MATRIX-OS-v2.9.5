# Z-SkillOS Readonly Invocation Sandbox Evidence Planning — GATE MODEL

## Status
Z_SKILLOS_READONLY_INVOCATION_SANDBOX_EVIDENCE_PLANNING_GATE_MODEL_READY

## Scope
This document defines the gate model for the SkillOS Readonly Invocation Sandbox. The gate model controls which invocations are permitted, at what permission tier, and under what evidence collection regime.

## Evidence
The gate model produces the following evidence artifacts per invocation attempt:
- `decision_hash` — Computed from (request_hash + permission_tier + adapter_id + source_class), binding the gating decision to the specific request
- `permission_tier` — Resolved tier after source_class and adapter_id evaluation
- `source_class` — Classified at gate entry, immutable for the invocation lifecycle

### Permission Tier Ladder

| Tier | Name | Allowed Operations | Evidence Required |
|------|------|--------------------|-------------------|
| 0 | NULL | No operations permitted | request_hash only |
| 1 | METADATA_READONLY | Read skill metadata, schema, version | Tier 0 + adapter_id |
| 2 | CONTEXT_READONLY | Read skill context, configuration | Tier 1 + permission_tier |
| 3 | INVOCATION_READONLY | Execute readonly skill invocation | Tier 2 + source_class |
| 4 | FULL_READONLY | Full readonly access within sandbox | Tier 3 + decision_hash |

### Source Classification

| Class | Value | Trust Level | Default Tier Cap |
|-------|-------|-------------|------------------|
| HUMAN | 0x01 | HIGH | 4 |
| AGENT | 0x02 | MEDIUM | 3 |
| SYSTEM | 0x04 | HIGH | 4 |
| SCHEDULED | 0x08 | MEDIUM | 2 |

## Boundary
- Gate model operates at invocation entry point only
- No gate re-evaluation during invocation execution
- Tier is fixed at gate entry for the entire invocation lifecycle
- Gate does not inspect invocation payloads (privacy boundary)
- Gate is stateless across invocations

## Forbidden
1. Dynamic tier escalation after gate entry
2. Source class mutation during invocation
3. Tier bypass via adapter_id spoofing
4. Gate model persistence to disk
5. Cross-invocation tier inheritance
6. Implicit tier elevation through adapter chaining

## Proof
- Tier ladder is total and mutually exclusive (0-4, no gaps)
- Source classification is exhaustive (4 classes, bitmask-compatible)
- Decision hash is deterministic given the same inputs
- Gate is stateless — no memory leak across invocations
- Tier cap prevents AGENT/SCHEDULED from reaching FULL_READONLY

## Next
- Validate gate model against INPUT_SOURCE_PLAN
- Ensure OUTPUT_CONTRACT_PLAN respects tier-based output restrictions
- Proceed to INPUT_SOURCE_PLAN planning document
