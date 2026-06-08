# Z-SkillOS Readonly Invocation Sandbox Evidence Planning — EVIDENCE SCHEMA PLAN

## Status
Z_SKILLOS_READONLY_INVOCATION_SANDBOX_EVIDENCE_PLANNING_EVIDENCE_SCHEMA_PLAN_READY

## Scope
This document defines the evidence schema — the cryptographic structure, linking mechanism, and tamper-detection design for all evidence artifacts.

## Evidence
The evidence schema is hash-only with seven core fields.

### Schema Fields
| Field | Type | Size | Description |
|-------|------|------|-------------|
| request_hash | hex | 64 chars | SHA-256 of canonical request serialization |
| response_hash | hex (placeholder) | 64 chars | SHA-256 of expected response shape schema |
| decision_hash | hex | 64 chars | hash(request_hash || permission_tier || adapter_id || source_class) |
| adapter_id | string | 3-64 chars | Opaque skill adapter identifier |
| permission_tier | uint8 | 1 byte | Resolved permission tier (0-4) |
| source_class | uint8 | 1 byte | Origin classification bitmask |
| rollback_marker | nullable string | 0-128 chars | Opaque rollback point identifier |

### Tamper Detection Chain
Each evidence record is linked to its predecessor via a hash chain:
```
E_0 = hash(request_hash_0 || decision_hash_0 || tamper_seal_0)
E_n = hash(E_{n-1} || request_hash_n || decision_hash_n || tamper_seal_n)
```

### Evidence Lifecycle
1. Creation — Evidence record created at gate entry
2. Linking — Each subsequent evidence event appends to the chain
3. Sealing — Final tamper_seal computed over complete chain
4. Delivery — Bundle delivered to consumer via in-memory callback
5. Destruction — All evidence destroyed after acknowledgment or TTL expiry

## Boundary
- Schema applies to evidence metadata only
- No invocation payloads, no response bodies, no context data
- Evidence is ephemeral (in-memory only, TTL-bound)
- Schema is forward-compatible via version field (future)

## Forbidden
1. Including invocation arguments in evidence fields
2. Including response data in evidence fields
3. Including timestamps beyond evidence_timestamp
4. Including adapter internal state or configuration
5. Evidence records that outlive the invocation TTL
6. Schema fields with unbounded size

## Proof
- All fields have bounded, known sizes
- Hash chain is cryptographically sound (SHA-256)
- Tamper detection covers the full chain
- Ephemeral design eliminates persistence attack surface
- Schema is minimal — no superfluous fields to exploit

## Next
- Align schema with HASH_CHAIN_PLAN
- Validate against AUDIT_SINK_PLAN for query compatibility
- Proceed to HASH_CHAIN_PLAN
