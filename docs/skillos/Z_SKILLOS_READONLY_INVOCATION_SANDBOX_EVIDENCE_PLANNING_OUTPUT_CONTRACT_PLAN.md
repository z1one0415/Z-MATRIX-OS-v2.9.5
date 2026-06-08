# Z-SkillOS Readonly Invocation Sandbox Evidence Planning — OUTPUT CONTRACT PLAN

## Status
Z_SKILLOS_READONLY_INVOCATION_SANDBOX_EVIDENCE_PLANNING_OUTPUT_CONTRACT_PLAN_READY

## Scope
This document defines the output contract for SkillOS Readonly Invocation Sandbox executions.

## Evidence
Output evidence is structured as an in-memory evidence bundle:

### Evidence Bundle Structure
```
EvidenceBundle {
  request_hash:       32-byte hex SHA-256
  response_hash:      placeholder (SHA-256 of expected response shape schema)
  decision_hash:      32-byte hex SHA-256
  adapter_id:         string matching ^[a-z][a-z0-9_-]{2,63}$
  permission_tier:    uint8 (0-4)
  source_class:       uint8 bitmask (0x01|0x02|0x04|0x08)
  rollback_marker:    nullable string
  invocation_status:  enum { ACCEPTED, REJECTED, COMPLETED, ROLLED_BACK, TIMED_OUT }
  evidence_timestamp: ISO-8601 UTC timestamp
  tamper_seal:        64-byte hex HMAC-SHA512 of all preceding fields
}
```

### Output Constraints
1. Evidence bundle MUST exist only in-memory
2. Bundle MUST be discarded after consumer acknowledgment or TTL expiry
3. response_hash is a placeholder; actual response is not computed at planning time
4. tamper_seal uses a per-invocation ephemeral key (never persisted)
5. Bundle serialization format is canonical JSON with sorted keys
6. Consumer receives the bundle via an in-memory callback

## Boundary
- Output contract applies to evidence bundle only, not to invocation results
- Consumer is responsible for bundle acknowledgment or timeout
- Bundle TTL is 300 seconds (5 minutes) from creation
- No bundle is retransmitted; consumer must request re-generation

## Forbidden
1. Writing evidence bundles to disk
2. Streaming evidence to network sinks
3. Bundling actual invocation payloads in evidence
4. Reusing ephemeral keys across invocations
5. Including PII or sensitive data in evidence fields
6. Consumer-side evidence persistence within sandbox scope
7. Bundle serialization with non-deterministic field ordering

## Proof
- Evidence bundle schema is total (all fields defined)
- tamper_seal covers all preceding fields
- Ephemeral key per invocation prevents cross-invocation tampering
- Canonical JSON serialization eliminates ordering attacks
- TTL enforcement prevents stale bundle replay

## Next
- Align output contract with EVIDENCE_SCHEMA_PLAN
- Ensure HASH_CHAIN_PLAN can consume bundles as chain links
- Proceed to EVIDENCE_SCHEMA_PLAN
