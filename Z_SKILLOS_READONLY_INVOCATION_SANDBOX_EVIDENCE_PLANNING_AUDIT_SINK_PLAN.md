# Z-SkillOS Readonly Invocation Sandbox Evidence Planning — AUDIT SINK PLAN

## Status
Z_SKILLOS_READONLY_INVOCATION_SANDBOX_EVIDENCE_PLANNING_AUDIT_SINK_PLAN_READY

## Scope
This document defines the in-memory audit sink design for the SkillOS Readonly Invocation Sandbox.

## Evidence
The audit sink is a transient, in-memory data structure that collects evidence bundles during their TTL window.

### Audit Sink Architecture
```
AuditSink {
  active_bundles: Map<request_hash, EvidenceBundle>
  chain_registry: Map<request_hash, HashChain>
  query_index: Map<adapter_id, Set<request_hash>>
  tier_index: Map<permission_tier, Set<request_hash>>
  source_index: Map<source_class, Set<request_hash>>
}
```

### Query Interface (In-Memory Only)
| Query | Parameters | Returns |
|-------|------------|---------|
| by_request_hash | request_hash | EvidenceBundle + HashChain |
| by_adapter | adapter_id, limit | List<EvidenceBundle> |
| by_tier | permission_tier, limit | List<EvidenceBundle> |
| by_source | source_class, limit | List<EvidenceBundle> |
| by_timerange | start_ts, end_ts, limit | List<EvidenceBundle> |
| recent | limit | List<EvidenceBundle> sorted by timestamp desc |
| chain_integrity | request_hash | VerificationResult |

### Retention Policy
- Active bundles: stored until consumer acknowledgment or TTL expiry (300 seconds)
- Expired bundles: removed immediately from all indexes
- No archival: expired data is irrecoverable
- Maximum concurrent bundles: 10,000 (safety bound)
- Eviction policy: LRU when max concurrent bundles reached

### Audit Trail Properties
1. Transient — No data survives process restart
2. Indexed — O(1) lookup by request_hash, O(log n) by other indexes
3. Verifiable — Every returned bundle can be chain-verified
4. Bounded — Memory usage bounded by max concurrent bundles
5. Ephemeral — No audit log serialization, no export capability

## Boundary
- Audit sink exists only within the sandbox process memory space
- No network exposure of audit data
- No inter-process sharing of audit sink state
- Query interface is for in-process consumers only
- Audit sink is destroyed on sandbox process termination

## Forbidden
1. Writing audit sink data to files, databases, or message queues
2. Exposing audit sink via network API
3. Cross-process audit sink state sharing
4. Archival or export of expired bundles
5. Audit sink persistence across sandbox restarts
6. Unbounded audit sink growth (hard cap at 10,000 bundles)

## Proof
- In-memory-only design guarantees no persistence by construction
- TTL-based eviction prevents unbounded memory growth
- LRU eviction provides graceful degradation under load
- Index structure supports all specified query patterns
- Chain verification is available for any active bundle

## Next
- Ensure PRIVACY_BOUNDARY_PLAN enforces audit sink isolation
- Validate audit sink capacity against expected invocation rate
- Proceed to PRIVACY_BOUNDARY_PLAN
