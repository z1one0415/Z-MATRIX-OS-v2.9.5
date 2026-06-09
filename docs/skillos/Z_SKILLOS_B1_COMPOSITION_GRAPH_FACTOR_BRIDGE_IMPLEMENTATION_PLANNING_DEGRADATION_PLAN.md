# Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING — DEGRADATION PLAN

## 1. Status

- Phase: PLANNING (docs-only)
- Seal: Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING_SEALED
- Subject: Degradation decision model for B1 composition graph

## 2. Scope

This document defines the 8 degradation decisions for the B1 composition graph.
B1 consumes A1FactorBridgeResponse ONLY. Degradation decisions are the graph's
response to invalid states. Denied context cannot become valid node.

### 2.1 Degradation Decisions

| Decision | Trigger | Severity | Recovery |
|---|---|---|---|
| DENY_GRAPH_SOURCE_FORBIDDEN | Blocked node type detected in graph | CRITICAL | Remove node, rebuild DAG |
| DENY_GRAPH_REAL_SOURCE_FORBIDDEN | Real source node detected | CRITICAL | Reject entire graph |
| DENY_GRAPH_OUTPUTS_UNSAFE | Blocked output type in evidence chain | HIGH | Filter outputs, revalidate |
| DENY_GRAPH_BRIDGE_DENIED | Bridge denied context in valid path | HIGH | Route to denied context node |
| DENY_GRAPH_DAG_INVALID | Cycle detected or structural violation | CRITICAL | Reject entire graph |
| DENY_GRAPH_EXECUTION_FORBIDDEN | Execution edge or node detected | CRITICAL | Reject entire graph |
| DISABLED_DEFAULT_NOOP | Kill switch active or default state | LOW | No-op, return empty summary |
| ALLOW_GRAPH_READONLY_SUMMARY | All validations pass | NONE | Proceed with readonly summary |

### 2.2 Decision Routing

```
Graph submitted for validation
  ├─ Kill switch active? → DISABLED_DEFAULT_NOOP
  ├─ Blocked node types? → DENY_GRAPH_SOURCE_FORBIDDEN
  ├─ Real source nodes? → DENY_GRAPH_REAL_SOURCE_FORBIDDEN
  ├─ Execution edges? → DENY_GRAPH_EXECUTION_FORBIDDEN
  ├─ DAG invalid? → DENY_GRAPH_DAG_INVALID
  ├─ Blocked outputs? → DENY_GRAPH_OUTPUTS_UNSAFE
  ├─ Bridge denied in valid path? → DENY_GRAPH_BRIDGE_DENIED
  └─ All pass? → ALLOW_GRAPH_READONLY_SUMMARY
```

### 2.3 Degradation Evidence

Each degradation decision produces:
- degradation_decision_type (the decision enum value)
- trigger_description (what caused the degradation)
- rollback_marker (set to True on any DENY_*)
- graph_node_hash (of the offending node, if applicable)
- graph_edge_hash (of the offending edge, if applicable)

### 2.4 Default State

The graph starts in DISABLED_DEFAULT_NOOP state. This means:
- No processing occurs without explicit validation pass
- The kill_switch.py module enforces this default
- Only ALLOW_GRAPH_READONLY_SUMMARY enables processing
- All other states produce empty or degraded output

## 3. Dependency / Evidence

| Dependency | Seal/Commit |
|---|---|
| A1 Bridge P0 seal | 8a975309c0edfedba84c3522e046c970ca4adeaf |
| Factor Library P1 fixture seal | af1fc9a5bfe234386984c3e5d98b7ae447a58955 |
| B1 factor-aligned planning seal | 7e0a6c956d03282b649e9908b2835ea70ddfcfd5 |
| Parent factor interface baseline | d02b60c9c7ad8500dd5403c28710f850cf11bc47 |

## 4. Boundary

- Degradation is fail-safe: any unknown state → DISABLED_DEFAULT_NOOP
- No degradation decision can enable execution
- No degradation decision can bypass blocked output filtering
- ALLOW_GRAPH_READONLY_SUMMARY is the ONLY positive decision

## 5. Forbidden Actions

- NO runtime enablement (runtime enablement is not authorized)
- NO degradation bypass mechanisms
- NO code creation in this planning document
- NO automatic recovery that skips validation

## 6. Proof / Review Requirements

- Each degradation decision must have defined trigger and severity
- DISABLED_DEFAULT_NOOP must be the default proof
- rollback_marker propagation proof
- denied bridge context proof (DENY_GRAPH_BRIDGE_DENIED triggers correctly)

## 7. Next Legal Entry

- OUTPUT_BOUNDARY_PLAN: output filtering specifications
- ROLLBACK_PLAN: rollback mechanism planning

---
