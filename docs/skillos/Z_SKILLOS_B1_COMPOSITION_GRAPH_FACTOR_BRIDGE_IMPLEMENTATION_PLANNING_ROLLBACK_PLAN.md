# Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING — ROLLBACK PLAN

## 1. Status

- Phase: PLANNING (docs-only)
- Seal: Z_SKILLOS_B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_IMPLEMENTATION_PLANNING_SEALED
- Subject: Rollback and kill-switch planning for B1 composition graph

## 2. Scope

This document defines the rollback mechanisms for the B1 composition graph.
B1 consumes A1FactorBridgeResponse ONLY. Rollback ensures the graph can be safely
disabled at any point. Denied context cannot become valid node.

### 2.1 Rollback Triggers

| Trigger ID | Condition | Action |
|---|---|---|
| RB-001 | Kill switch activated | DISABLED_DEFAULT_NOOP immediately |
| RB-002 | Blocked node type detected post-construction | Invalidate graph, set rollback_marker |
| RB-003 | Blocked edge type detected post-construction | Invalidate graph, set rollback_marker |
| RB-004 | Cycle detected in DAG | DENY_GRAPH_DAG_INVALID, set rollback_marker |
| RB-005 | Real source detected | DENY_GRAPH_REAL_SOURCE_FORBIDDEN, set rollback_marker |
| RB-006 | Blocked output passes filter | DENY_GRAPH_OUTPUTS_UNSAFE, set rollback_marker |
| RB-007 | Evidence chain break | DENY_GRAPH_DAG_INVALID, set rollback_marker |
| RB-008 | Permission escalation detected | DENY_GRAPH_SOURCE_FORBIDDEN, set rollback_marker |
| RB-009 | c1_handoff_marker missing at terminal | DENY_GRAPH_OUTPUTS_UNSAFE, set rollback_marker |
| RB-010 | Denied context in valid processing path | DENY_GRAPH_BRIDGE_DENIED, set rollback_marker |

### 2.2 Kill Switch Design

The kill_switch.py module (planned, not yet created) will:
- Default to DISABLED (DISABLED_DEFAULT_NOOP)
- Require explicit enable signal to allow ALLOW_GRAPH_READONLY_SUMMARY
- Be configurable via environment variable and config file
- Support instant disable without graph reconstruction

### 2.3 Rollback Evidence

When rollback is triggered:
- rollback_marker = True (immutable once set)
- rollback_trigger = trigger ID (RB-001 through RB-010)
- rollback_timestamp_placeholder = planned field
- graph state preserved for audit (read-only snapshot)

### 2.4 Recovery After Rollback

- Graph must be reconstructed from scratch (no in-place fix)
- All evidence hashes must be recomputed
- Validation must pass completely before re-enabling
- No partial recovery allowed

## 3. Dependency / Evidence

| Dependency | Seal/Commit |
|---|---|
| A1 Bridge P0 seal | 8a975309c0edfedba84c3522e046c970ca4adeaf |
| Factor Library P1 fixture seal | af1fc9a5bfe234386984c3e5d98b7ae447a58955 |
| B1 factor-aligned planning seal | 7e0a6c956d03282b649e9908b2835ea70ddfcfd5 |
| Parent factor interface baseline | d02b60c9c7ad8500dd5403c28710f850cf11bc47 |

## 4. Boundary

- Rollback is always safe (no data loss, no side effects)
- Kill switch is independent of graph state
- Rollback does not require human approval (automatic)
- Recovery requires full revalidation

## 5. Forbidden Actions

- NO runtime enablement (runtime enablement is not authorized)
- NO partial recovery or in-place graph fix
- NO rollback bypass mechanism
- NO code creation in this planning document

## 6. Proof / Review Requirements

- rollback marker proof: marker set correctly on all DENY decisions
- privacy marker proof: privacy preserved during rollback
- DISABLED_DEFAULT_NOOP proof: default state is disabled
- No autonomous retry proof: rollback does not auto-retry

## 7. Next Legal Entry

- TEST_AND_PROOF_PLAN: comprehensive proof categories
- CLOSEOUT: planning phase completion

---
