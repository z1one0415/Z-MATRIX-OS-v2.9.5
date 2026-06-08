# Z-SkillOS Skill Composition Graph P0 Planning — FAILURE DEGRADATION PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-planning

---

## 1. Failure Degradation Definition

Failure Degradation is the systematic response to any node or edge failure in the composition graph.
The core principle: **never fail-closed, never block, always degrade gracefully**. Every failure pathway
must result in a defined, bounded-time degradation outcome with no hanging, deadlocking, or undefined states.

## 2. Degradation Hierarchy

| Level | Name | Trigger | Result |
|-------|------|---------|--------|
| D1 | Degrade to NOOP | Single node failure | Node returns noop marker; other nodes unaffected |
| D2 | Degrade to PLAN_ONLY | Graph-level failure (permission, cycle, forbidden) | Entire graph returns plan structure without any execution |
| D3 | Partial Graph Invalidation | 2-node graph: node A succeeds, node B fails | A's result valid; graph invalid; B degraded |

## 3. Degradation to NOOP (D1)

### 3.1 Triggers
- Node processing exceeds `max_execution_time_ms`
- Node encounters an unhandled exception
- Node input fails schema validation
- Node capability_id not found in registry
- Node output exceeds `max_output_size_bytes`

### 3.2 NOOP Output
```json
{
  "status": "degraded",
  "reason": "noop",
  "node_id": "n001",
  "error_detail": "Execution timeout exceeded (5000ms)",
  "degradation_level": "D1"
}
```

### 3.3 Properties
- Bounded time: completes within 2 * max_execution_time_ms
- No side effects: node does not modify any external state
- Traceable: evidence hash includes degradation marker
- Non-blocking: graph continues to next node or completes

## 4. Degradation to PLAN_ONLY (D2)

### 4.1 Triggers
- Edge validation fails (FORBIDDEN)
- Permission propagation violation detected
- Cycle detected in graph
- Graph depth exceeds P0 limit (2)
- Node count exceeds P0 limit (2)
- Graph decision hash computation fails

### 4.2 PLAN_ONLY Output
```json
{
  "status": "degraded",
  "reason": "plan_only",
  "graph_id": "g001",
  "error_detail": "Permission escalation detected: node n002 tier 1 > node n001 tier 0",
  "degradation_level": "D2",
  "nodes_degraded": ["n002"],
  "plan_structure": { ... }
}
```

### 4.3 Properties
- Plan structure is still produced (for audit/debug)
- No capability is executed
- All nodes are individually evaluated but results discarded
- Graph decision hash includes the plan_only marker

## 5. Partial Graph Invalidation (D3)

Applies to two-node sequential graphs where the first node succeeds but the second fails:
- Node A's result is valid and hash-chained
- Node B degrades to NOOP
- Edge A→B is marked as PARTIAL (upstream valid, downstream degraded)
- Graph decision hash includes both: A's success hash + B's degradation hash
- Graph status: PARTIALLY_VALID (not VALID, not FORBIDDEN)

## 6. Anti-Patterns: What Degradation Must NOT Do

| Anti-Pattern | Why Forbidden |
|-------------|---------------|
| Fail-closed (system hangs) | Blocks caller indefinitely |
| Uncaught exception propagation | Bypasses degradation protocol |
| Silent failure (no degradation marker) | Undetectable corruption |
| Partial execution with hidden failures | Inconsistent state |
| Retry loops without bound | Unbounded execution time |
| Recursive degradation (degradation triggers more degradation) | Infinite regression |
| Degradation that produces side effects | Violates no-side-effect contract |
| Degradation that escalates permissions | Violates permission monotonicity |

## 7. Degradation Sequence Protocol

```
On node failure:
  1. Catch the exception (do not propagate)
  2. Determine degradation level (D1, D2, D3)
  3. Build degradation result per level
  4. Set node degraded flag = true
  5. Include degradation in node evidence hash
  6. If D2 or D3: set rollback_marker = true in graph
  7. Continue graph processing (do not abort)
  8. Return complete PlanStructure including all degradation markers
```

## 8. Time Bounds

| Operation | Max Time | On Timeout |
|-----------|----------|------------|
| Single node processing | 5000ms | Degrade to NOOP |
| Edge validation | 500ms | Mark edge FORBIDDEN |
| Graph validation | 2000ms | Degrade to PLAN_ONLY |
| Hash computation | 500ms | Use null hash (degraded) |
| Full graph build | 10000ms | Degrade to PLAN_ONLY |

---

**Sign-off**: Z2天师 — Hermes Research Kernel
**Pipeline Signature**: `Z-SKILLOS|SCG-P0|PLANNING|FAILURE_DEGRADATION|v1.0.0-draft`
