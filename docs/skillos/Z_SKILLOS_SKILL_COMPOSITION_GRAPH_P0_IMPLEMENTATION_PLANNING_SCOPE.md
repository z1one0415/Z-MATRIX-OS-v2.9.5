# Z-SkillOS Skill Composition Graph P0 Implementation Planning — SCOPE

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft

---

## 1. Scope Definition

This document defines the precise boundary of the Skill Composition Graph P0 Implementation Planning
phase. P0 establishes the absolute minimum viable implementation specification: file-level plans,
data model schemas, validator contracts, and test vectors — all as documentation only.

## 2. In-Scope — P0 Implementation Planning

### 2.1 File-Level Planning
- Complete file tree under `skillos/capability_invocation_os/composition/`
- Module responsibilities and import hierarchy
- Public API surface for each module
- No code files are created; only specification documents
- All future file paths are documented with their intended content

### 2.2 Node Model Implementation Spec
- `CompositionNode` data class specification
- All 10 required fields: capability_id, module_adapter_id, permission_tier, input_schema, output_schema, degradation_result, node_id, created_at, version, metadata
- JSON Schema for input/output validation
- Tier validation rules (0-1 only in P0)
- Immutability contract post-build

### 2.3 Edge Model Implementation Spec
- `CompositionEdge` data class specification
- All 10 required fields: edge_id, upstream_node_id, downstream_node_id, allowed_data_fields, forbidden_data_fields, evidence_handoff, permission_propagation, created_at, version, metadata
- Field governance: allow-list and deny-list semantics
- Self-edge prevention enforcement
- Edge immutability post-build

### 2.4 DAG Validator Implementation Spec
- Static DAG structure validation
- Kahn's algorithm for topological sort and cycle detection
- Max depth = 2 enforcement
- Max node count = 2 enforcement
- Strict sequential topology enforcement
- All 12 DAG invariants (DAG-01 through DAG-12)
- Build-time gate: graph is valid or rejected

### 2.5 Permission Propagation Implementation Spec
- Permission tier model: Tier 0 (readonly), Tier 1 (planning)
- Monotonic non-increasing propagation: downstream_tier ≤ upstream_tier
- Escalation detection and FORBIDDEN rejection
- Write-tier blocking (Tier 4-5 never allowed in P0)
- Permission check at edge validation time
- Permission violation → whole graph FORBIDDEN

### 2.6 Evidence Propagation Implementation Spec
- SHA-256 based hash chain
- Node evidence: SHA-256(capability_id + input + output + timestamp)
- Edge evidence: SHA-256(upstream_node_hash + edge_id + timestamp)
- Graph decision: SHA-256(all_node_hashes + all_edge_hashes + plan_id)
- Canonical JSON serialization with sorted keys
- Deterministic hashing with fixed input ordering
- Test vectors for hash verification

### 2.7 Degradation Implementation Spec
- Degradation states: NOOP, PLAN_ONLY, COMPLETE
- Fail-closed is FORBIDDEN
- No blocking: degradation always produces a result
- Rollback marker on any node degradation
- Degradation propagation: upstream degradation forces downstream degradation
- Degradation result field on every node

### 2.8 Loop Prevention Implementation Spec
- Depth counter: max 2, enforced at every edge addition
- Cycle detection: Kahn's algorithm at graph build time
- Self-edge rejection: upstream_node_id != downstream_node_id
- Back-edge rejection in 2-node graphs
- No dynamic recursion
- No hidden agent loops

### 2.9 Output Boundary Implementation Spec
- Output schema enforcement per node
- Forbidden field blocking at edge handoff
- Output immutability post-build
- No result_envelope mutation
- Output truncation boundary for evidence hash computation

### 2.10 Test & Proof Plan
- ≥18 proof categories
- Test vectors for hash determinism
- Edge case coverage for all validators
- Degradation scenario testing
- Permission escalation rejection testing
- Cycle detection testing

## 3. Out of Scope — P0

### 3.1 Implementation
- No .py files are created
- No code is written, compiled, or executed
- No runtime environment is configured
- No dependencies are installed

### 3.2 Dynamic Behavior
- No dynamic graph modification post-build
- No runtime node addition/removal
- No conditional branching based on node output
- No feedback loops or iterative composition

### 3.3 Execution
- No real capability invocation
- No Z-MATRIX module calls
- No tool execution of any kind
- No side effects (file writes, network calls, database queries)

### 3.4 Advanced Topology
- No branching, fan-out, fan-in, or merge nodes
- No >2 node graphs
- No >2 depth graphs
- No parallel execution

### 3.5 Persistence
- No database integration
- No file-based graph storage
- No serialization format beyond JSON Schema specification
- No evidence log or audit trail persistence

## 4. FORBIDDEN Actions — ≥18 Items

| # | Forbidden Action | Rationale |
|---|------------------|-----------|
| 1 | Real capability execution | P0 is plan-only; no tool invocation |
| 2 | Hidden tool calls | All capability paths must be explicit in contracts |
| 3 | Dynamic graph modification | Graph is immutable post-build |
| 4 | Recursive composition | No cycles, no self-referencing graphs |
| 5 | Auto-permission escalation | Permission tier must not increase downstream |
| 6 | Result envelope mutation | Outputs are immutable after node completion |
| 7 | Fail-closed behavior | Degradation must produce a result, never block |
| 8 | Z-MATRIX integration | This is standalone SkillOS infrastructure |
| 9 | Persistent evidence storage | All evidence is ephemeral in P0 |
| 10 | Network calls | No external service integration |
| 11 | File system writes | No side effects of any kind |
| 12 | Database queries | No persistence layer |
| 13 | Sub-agent spawning | No hidden agent loops |
| 14 | Unregistered capability paths | All capabilities must be in the registry |
| 15 | Write-tier node execution | Tier 4-5 never allowed in P0 |
| 16 | Dynamic depth interpretation | Depth is compile-time constant |
| 17 | Conditional topology | All topology is fully known at build time |
| 18 | Evidence hash mutation | Hashes are immutable after computation |
| 19 | Non-deterministic serialization | All JSON must use sorted keys |
| 20 | Circular dependency | Kahn's algorithm catch-all |

## 5. Future Code Files

All implementation targets reside at `skillos/capability_invocation_os/composition/`:
- `__init__.py`: Package initialization, public API exports
- `models/node.py`: CompositionNode with full contract validation
- `models/edge.py`: CompositionEdge with field governance
- `models/graph.py`: CompositionGraph with build-time assembly
- `validators/dag_validator.py`: Kahn's algorithm, topology checks
- `validators/permission_validator.py`: Tier enforcement
- `validators/evidence_validator.py`: SHA-256 hash chain
- `policies/permission_propagation.py`: Monotonic non-increasing rule
- `policies/evidence_propagation.py`: Hash chain propagation
- `policies/loop_prevention.py`: Depth and cycle guards
- `policies/output_boundary.py`: Schema enforcement
- `degradation/degradation_controller.py`: Degradation state machine
- `tests/test_composition_graph.py`: Comprehensive test suite

## 6. Success Criteria

1. All 26 documents meet line count minimums (planning ≥30, review ≥35, merge ≥30)
2. Review Risk Register has ≥12 risks documented
3. Merge Risk Register has ≥10 risks documented
4. Review Checklist has ≥18 items
5. Merge Checklist has ≥15 items
6. Test & Proof Plan has ≥18 proof categories
7. FORBIDDEN actions matrix has ≥18 items
8. Every document follows the 7-section structure
9. Planning Seal finalizes the package as immutable
10. All documents are docs-only, no implementation files

## 7. Governance

- **Level 5 BLOCKED**: Highest restriction; no code, no execution, no integration.
- **FUTURE_PLAN_ONLY**: These specifications are forward-looking; no runtime exists.
- **Immutable After Seal**: The PLANNING_SEAL document locks this package.
- **Branch**: `plan/skillos-skill-composition-graph-p0-implementation-planning` @ `3e6ce10c`.
- **Parent**: P0 Planning Package (branch `plan/skillos-skill-composition-graph-p0-planning`).
