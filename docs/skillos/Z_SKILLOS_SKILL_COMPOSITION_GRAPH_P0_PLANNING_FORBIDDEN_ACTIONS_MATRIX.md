# Z-SkillOS Skill Composition Graph P0 Planning — FORBIDDEN ACTIONS MATRIX

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-planning

---

## 1. Purpose

This matrix enumerates every action that is explicitly forbidden during P0 planning, graph construction,
and (future) execution. Each forbidden action is categorized by severity, detection mechanism,
and consequence. Minimum: 18 forbidden actions.

## 2. Forbidden Actions Matrix

| # | Action | Category | Severity | Detection | Consequence |
|---|--------|----------|----------|-----------|-------------|
| FA-01 | Create graph with >2 nodes | Topology | CRITICAL | Compile-time: DAG-02 | Graph rejected; DEPTH_EXCEEDED |
| FA-02 | Create graph with depth >2 | Topology | CRITICAL | Compile-time: DAG-03 | Graph rejected; DEPTH_EXCEEDED |
| FA-03 | Create self-edge (A→A) | Topology/Cycle | CRITICAL | Compile-time: EC-03 | Edge rejected; graph FORBIDDEN |
| FA-04 | Create cycle (A→B→A) | Topology/Cycle | CRITICAL | Compile-time: Kahn's algorithm | Graph rejected; CYCLE_DETECTED |
| FA-05 | Permission escalation (downstream tier > upstream) | Permission | CRITICAL | Compile-time: edge validation | Edge FORBIDDEN; graph FORBIDDEN |
| FA-06 | Use permission tier 4 (EXECUTION) | Permission | CRITICAL | Compile-time: NC-03 | Node rejected; tier out of P0 range |
| FA-07 | Use permission tier 5 (PRODUCTION) | Permission | CRITICAL | Compile-time: NC-03 | Node rejected; tier out of P0 range |
| FA-08 | Write to filesystem from any node | Side Effect | CRITICAL | Compile-time: allowed_side_effects check | Node rejected; side effect detected |
| FA-09 | Make network calls from any node | Side Effect | CRITICAL | Compile-time: allowed_side_effects check | Node rejected; side effect detected |
| FA-10 | Modify result_envelope fields | Output Boundary | HIGH | Compile-time: envelope schema validation | Graph rejected; IMMUTABLE_VIOLATION |
| FA-11 | Surface internal errors to caller | Output Boundary | HIGH | Build-time: output sanitization | Sanitized output; internal detail stripped |
| FA-12 | Dynamic graph mutation after build | DAG Policy | CRITICAL | Runtime: immutable graph object | Mutation rejected; no API available |
| FA-13 | Execute capability (real invocation) | Execution | CRITICAL | Build-time: dry-plan-only flag | Execution blocked; plan-only mode |
| FA-14 | Call Z-MATRIX API from any node | Integration | CRITICAL | Compile-time: dependency check | Node rejected; forbidden dependency |
| FA-15 | Spawn sub-agent from node capability | Agent Loop | CRITICAL | Compile-time: no_hidden_execution check | Node rejected; hidden execution |
| FA-16 | Tool recursion (capability A calls graph containing A) | Recursion | CRITICAL | Compile-time: capability call graph analysis | Graph FORBIDDEN; recursion detected |
| FA-17 | Persist evidence hashes to disk | Evidence | HIGH | Compile-time: no persistence flag | Evidence discarded; in-memory only |
| FA-18 | Propagate forbidden data fields across edge | Edge Contract | HIGH | Compile-time: EC-06 | Edge FORBIDDEN; data blocked |
| FA-19 | Omit degradation_result from node contract | Node Contract | HIGH | Compile-time: NC-06 | Node rejected; missing degradation |
| FA-20 | Exceed max_execution_time_ms without degrading | Failure | CRITICAL | Runtime: timeout watchdog (future) | Node degraded to NOOP |
| FA-21 | Fail-closed (hang/block) instead of degrading | Failure | CRITICAL | Runtime: watchdog (future) | System intervention; graph degrade |
| FA-22 | Branch topology (>1 outgoing edge from any node) | Topology | CRITICAL | Compile-time: edge count check | Graph rejected; branching forbidden |

## 3. Severity Definitions

| Severity | Definition | Response |
|----------|------------|----------|
| CRITICAL | Violates core safety invariant. Could lead to unauthorized execution or data breach. | Immediate rejection; graph FORBIDDEN |
| HIGH | Violates policy contract. Degrades functionality but not safety-critical. | Edge/node rejection; graph may degrade |
| MEDIUM | Best practice violation. Does not impact safety. | Warning in internal proof; graph proceeds |
| LOW | Style/formatting issue. No functional impact. | Logged; no action |

## 4. Detection Mechanisms

| Mechanism | When Applied | Coverage |
|-----------|-------------|----------|
| Compile-time contract validation | Node/edge contract check | FA-01 through FA-19, FA-22 |
| Build-time sanitization | Output boundary check | FA-10, FA-11 |
| Runtime watchdog (future) | Execution monitoring | FA-20, FA-21 |
| Static analysis | Capability call graph | FA-16 |

## 5. Response Protocol

For any detected forbidden action:
1. Identify the violating component (node, edge, graph)
2. Assign severity level
3. Apply consequence (reject, forbid, degrade)
4. Record in graph decision hash
5. Do NOT silently ignore
6. Do NOT auto-correct (no silent remediation)
7. Surface to caller as appropriate (degraded status, not internal detail)

---

**Sign-off**: Z2天师 — Hermes Research Kernel
**Pipeline Signature**: `Z-SKILLOS|SCG-P0|PLANNING|FORBIDDEN_ACTIONS|v1.0.0-draft`
