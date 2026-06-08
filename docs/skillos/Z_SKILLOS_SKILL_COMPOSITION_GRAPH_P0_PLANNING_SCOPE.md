# Z-SkillOS Skill Composition Graph P0 Planning — SCOPE

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-planning
> Pipeline: Lane B — Skill Composition Graph P0
> Version: v1.0.0-draft

---

## 1. Scope Definition

This document defines the precise boundary of the Skill Composition Graph P0 Planning phase.
P0 establishes the absolute minimum viable composition capability: a static, compile-time-validated DAG
with ≤2 nodes in strictly sequential topology.

## 2. In-Scope — P0

### 2.1 Graph Topology
- Single-node dry plan: one capability node, no edges, validated but not executed
- Two-node sequential plan: node A → node B, single edge with contract validation
- Static DAG: topology is fully known and immutable at build time
- Compile-time cycle detection: any cycle detected before graph reaches build completion

### 2.2 Node Contract
- `capability_id`: unique identifier for the capability this node represents
- `module_adapter_id`: adapter path in the capability invocation OS
- `permission_tier`: integer tier (0=readonly, 1=planning, 2=research, 3=advisory); P0 only uses 0-1
- `input_schema`: typed input specification (JSON Schema)
- `output_schema`: typed output specification (JSON Schema)
- `degradation_result`: what this node returns on failure (noop marker, error envelope)

### 2.3 Edge Contract
- `upstream_node_id`: source node
- `downstream_node_id`: target node
- `allowed_data_fields`: explicit allow-list of data fields permitted to flow
- `forbidden_data_fields`: explicit deny-list of data fields blocked from flow
- `evidence_handoff`: hash of upstream output that downstream receives
- `permission_propagation`: downstream tier ≤ upstream tier enforcement

### 2.4 DAG Policy
- Max graph depth: 2 (nodes in longest path)
- Max node count: 2
- Topology constraint: strictly sequential (no branching, no fan-out, no fan-in, no merge)
- No cycles: enforced at graph build time
- No dynamic recursion: graph is fully flattened before any processing
- No hidden agent loops: no node can spawn sub-agents or loop internally

### 2.5 Permission Propagation
- Downstream permission tier ≤ upstream permission tier (monotonic non-increasing)
- If upstream permission tier is violated, whole graph is forbidden from execution
- No write propagation: Tier 0 and Tier 1 only (readonly + planning)
- No production/broker/real_trade tiers accessible in P0
- Permission check is enforced at edge validation time

### 2.6 Evidence Propagation
- Every node produces a `node_evidence_hash`: SHA-256 of (capability_id + input + output + timestamp)
- Every edge produces an `edge_evidence_hash`: SHA-256 of (upstream_node_hash + edge_id + timestamp)
- Graph produces a `graph_decision_hash`: SHA-256 of (all_node_hashes + all_edge_hashes + plan_id)
- Rollback marker: if any node degrades, a `rollback_marker` field is set in decision hash input
- No persistence: all hashes are ephemeral, in-memory only

### 2.7 Failure Degradation
- Primary degradation: node failure → degrade to `noop` (node returns null/marker)
- Secondary degradation: node failure → degrade to `plan-only` (entire graph returns plan without execution)
- Partial graph invalidation: if node B fails in A→B, A's result is still valid but graph is invalid
- No fail-closed: system never hangs, blocks, or deadlocks on failure
- No blocking: all degradation paths complete in bounded time

### 2.8 Loop Prevention
- Static DAG only: no runtime graph mutation
- Max depth = 2: enforced at graph validation
- No self-edge: node cannot connect to itself
- No circular dependency: A→B→A is prohibited
- No tool recursion: node capabilities cannot recursively call themselves through the graph
- Compile-time detection of all loop types

### 2.9 Output Boundary
- `result_envelope` is immutable: no graph node can modify the outer result envelope
- No caller-visible warnings: any errors are internal proof only
- Internal proof only: evidence is generated but never surfaced to caller
- No user-visible side effects: no file writes, no console output, no network calls
- Dry plan output: the graph produces a `PlanStructure` object only

## 3. Out of Scope — P0

| Category | Excluded | Reason |
|----------|----------|--------|
| Graph topology | >2 nodes | P0 minimum; P1 expands |
| Graph topology | Branching (fan-out) | Requires multi-path validation |
| Graph topology | Merging (fan-in) | Requires aggregation semantics |
| Graph topology | Conditional edges | Requires runtime evaluation |
| Execution | Real capability invocation | P0 is plan-only |
| Execution | Async/concurrent nodes | Single-threaded sequential only |
| Persistence | State storage | Ephemeral in-memory only |
| Persistence | Evidence storage | No audit log persistence |
| Network | Remote capability calls | All local, in-process |
| Network | Cross-process communication | Single-process only |
| Security | Production tokens | No production access |
| Security | Broker integration | No real-trade pathways |
| Monitoring | Telemetry | No metrics emission |
| Monitoring | Alerting | No alert side channels |

## 4. Explicit Exclusions

The following are explicitly excluded from P0 and must not appear in any planning document
as in-scope:

1. No real execution of any capability (dry plan generation only)
2. No Z-MATRIX integration or invocation
3. No production deployment artifacts
4. No runtime scheduling or dispatch
5. No dynamic graph construction
6. No agent-in-the-loop execution models
7. No feedback edges or adaptive planning
8. No multi-agent coordination

## 5. Future Phases (Out of P0)

| Phase | Scope | Dependencies |
|-------|-------|--------------|
| P1 | Multi-node branching, fan-out, fan-in | P0 contracts validated |
| P2 | Conditional edges, runtime path selection | P1 topology proven |
| P3 | Parallel execution, async orchestration | P2 conditionals stable |
| P4 | Dynamic graph mutation, agent feedback | P3 concurrency proven |
| P5 | Cross-process, distributed composition | P4 dynamics stable |

---

**Sign-off**: Z2天师 — Hermes Research Kernel
**Pipeline Signature**: `Z-SKILLOS|SCG-P0|PLANNING|SCOPE|v1.0.0-draft`
**Next**: NODE_CONTRACT_PLAN.md
