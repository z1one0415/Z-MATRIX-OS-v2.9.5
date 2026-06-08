# Z-SkillOS Skill Composition Graph P0 Planning — OUTPUT BOUNDARY PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-planning

---

## 1. Output Boundary Definition

The Output Boundary defines what the composition graph can and cannot produce as visible output
to the caller. The core principle: **internal proof only, no caller-visible mutation, no user-visible
side effects**. The graph's output is a sanitized, immutable PlanStructure; nothing else.

## 2. result_envelope Immutability

### 2.1 Definition
The `result_envelope` is the outer container that wraps the graph's output. It has a fixed schema
that NO graph node may modify.

### 2.2 Envelope Schema (Immutable)
```json
{
  "result_envelope": {
    "plan_id": "string (immutable)",
    "status": "string (immutable: valid | degraded | forbidden)",
    "decision_hash": "string (immutable)",
    "plan_structure": { ... },
    "evidence": { ... }
  }
}
```

### 2.3 Mutation Rules
- No node may add fields to `result_envelope`
- No node may remove fields from `result_envelope`
- No node may change the type of any `result_envelope` field
- No edge may filter or modify `result_envelope` fields
- The envelope schema is defined at graph build time and never changes

## 3. No Caller-Visible Warning

### 3.1 Principle
Any errors, warnings, or degradation events are internal to the graph. The caller receives
only the standard `result_envelope`. The caller does NOT see:
- Stack traces
- Internal error messages
- Degradation reasons at the code level
- Permission violation details
- Node execution logs

### 3.2 What the Caller Sees
```json
{
  "result_envelope": {
    "plan_id": "g001",
    "status": "degraded",
    "decision_hash": "sha256:...",
    "plan_structure": {
      "nodes": [ ... ],
      "edges": [ ... ],
      "graph_valid": false
    },
    "evidence": {
      "graph_evidence_hash": "sha256:...",
      "degradation_detected": true
    }
  }
}
```

The caller knows the graph was degraded but not why at a detailed level.
Detailed evidence is internal proof only.

## 4. Internal Proof Only

### 4.1 Internal Evidence
Internal evidence includes:
- Full node evidence hashes for every node
- Full edge evidence hashes for every edge
- Detailed degradation reasons
- Permission violation specifics
- Cycle detection details (if any)

### 4.2 Not Surfaced to Caller
These details exist in the graph's internal state but are NOT included in the caller-visible
`result_envelope`. They are available for:
- Post-hoc audit (when evidence persistence is implemented in future phases)
- Debug trace reconstruction
- Compliance verification

## 5. No User-Visible Side Effects

The graph execution (which is dry-plan only in P0) must produce zero user-visible side effects:

| Side Effect | P0 Status |
|------------|-----------|
| Console output (stdout/stderr) | FORBIDDEN |
| File writes | FORBIDDEN |
| Database writes | FORBIDDEN |
| Network calls | FORBIDDEN |
| Log file creation | FORBIDDEN |
| Environment variable modification | FORBIDDEN |
| Signal emission (events, webhooks) | FORBIDDEN |
| UI rendering or popup | FORBIDDEN |
| Notification delivery | FORBIDDEN |
| External service invocation | FORBIDDEN |

### 5.1 Verification
Every node contract's `allowed_side_effects` field must be `[]` (empty array).
This is enforced at compile time for all P0 nodes.

## 6. Output Sanitization Protocol

```
function build_caller_output(internal_state):
  result = {
    result_envelope: {
      plan_id: internal_state.plan_id,
      status: map_internal_status(internal_state.status),
      decision_hash: internal_state.decision_hash,
      plan_structure: sanitize_plan(internal_state.plan_structure),
      evidence: {
        graph_evidence_hash: internal_state.evidence.graph_hash,
        degradation_detected: internal_state.degradation_detected
      }
    }
  }
  
  # Strip internal details
  # No stack traces, no error messages, no permission specifics
  # No node-level evidence hashes (these are internal proof)
  
  return result
```

## 7. Boundary Enforcement

| Enforcement Point | Mechanism |
|------------------|-----------|
| Compile-time | Node contract `allowed_side_effects` must be `[]` |
| Compile-time | `result_envelope` schema validation |
| Build-time | Output sanitization before returning to caller |
| Post-build | No API to modify output after sanitization |
| Edge validation | No edge can carry side-effect data fields |

---

**Sign-off**: Z2天师 — Hermes Research Kernel
**Pipeline Signature**: `Z-SKILLOS|SCG-P0|PLANNING|OUTPUT_BOUNDARY|v1.0.0-draft`
