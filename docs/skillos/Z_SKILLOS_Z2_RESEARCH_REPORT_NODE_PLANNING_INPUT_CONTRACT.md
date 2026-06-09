# Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING — INPUT_CONTRACT

> Formal input contract for Z2 Research Report Node.
> Branch: plan/skillos-z2-research-report-node-planning
> Base commit: 74c27fa

---

## 1. Status

| Field | Value |
|-------|-------|
| Document | INPUT_CONTRACT |
| Status | PLANNING |
| Created | 2026-06-09 |
| Parent | DEPENDENCY_MAP.md |
| Dependency | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED (postmerge HEAD = 74c27fa) |

---

## 2. Scope

This document defines the complete and exhaustive list of inputs that the Z2 Research Report Node
may accept. Any input not listed here is FORBIDDEN and must trigger DENY_Z2_SOURCE_FORBIDDEN.

The primary input is B1 CompositionGraphResponse. All other inputs are either transitive
through B1 or static runtime context. The node enforces no_alpha_claim and no_trade_signal
at the input validation stage — if any input suggests trade intent, the node must reject.

---

## 3. Dependency / Evidence

### 3.1 Permitted Inputs (Exhaustive List)

| # | Input | Source | Mode | Required |
|---|-------|--------|------|----------|
| 1 | B1 CompositionGraphResponse | B1 postmerge (74c27fa) | Structured data | YES |
| 2 | B1 graph evidence chain | Embedded in B1 response | Inherited | YES |
| 3 | A1 bridge evidence through B1 | Transitive via B1 | Readonly | CONDITIONAL |
| 4 | Factor Library readonly metadata | Through B1/A1 path | Readonly | OPTIONAL |
| 5 | FactorEvaluationMatrix readonly handoff | Future optional | Readonly | FUTURE |
| 6 | Small Real Sample Read-Only summary | Future optional | Readonly | FUTURE |
| 7 | Static user research question context | Runtime parameter | Immutable | YES |
| 8 | Local in-memory report template | Internal config | Immutable | YES |

### 3.2 Input Validation Rules

Each input must be validated before processing:

1. **B1 CompositionGraphResponse**:
   - Must contain valid graph_node_hash and graph_edge_hash
   - Must contain source_class field
   - Must contain no_real_source_flag
   - Must contain permission_tier
   - response_hash_placeholder must be present (placeholder until real hash)

2. **B1 graph evidence chain**:
   - All hash fields must be non-empty strings
   - fixture_source_commit must match known fixture set
   - rollback_marker must be FALSE for report generation to proceed

3. **A1 bridge evidence**:
   - bridge_decision_hash must be present and non-empty
   - Must arrive ONLY through B1 CompositionGraphResponse (never direct)

4. **Factor Library metadata**:
   - readonly access only — no write capability
   - Must arrive through B1/A1 path only

5. **User research question**:
   - Must be a non-empty string
   - Must not contain trade instructions or position requests
   - Must not request alpha claims or return predictions

---

## 4. Boundary

### Input Size Limits:
- B1 CompositionGraphResponse: max 500KB serialized
- User research question: max 2000 characters
- Evidence chain: max 100 nodes, 500 edges

### Input Freshness:
- B1 response must reference fixture_source_commit traceable to 74c27fa lineage
- Stale inputs (>24h from generation) trigger degradation to ALLOW_Z2_DEGRADED_REPORT

---

## 5. Forbidden Actions

### DIRECTLY FORBIDDEN Inputs:
| Forbidden Input | Reason | Detection |
|----------------|--------|-----------|
| FactorInvocationResponse | Not in input contract | Type check at entry |
| Raw factor values | Not in input contract | Schema validation |
| research/factor_library files | Direct access forbidden | Import guard |
| Broker data | Production safety | Import guard + schema |
| Production system data | Production safety | Import guard + schema |
| Real returns | Production safety | Field name blocklist |
| Real trades | Production safety | Field name blocklist |
| Paper trades | Production safety | Field name blocklist |
| Z2 runtime internals | Circular dependency | Import guard |
| Z8 data | Out of scope | Import guard |
| Z9 data | Out of scope (Z9 is downstream) | Import guard |
| V3 data | Out of scope | Import guard |

### Input Rejection Triggers:
- Any field matching forbidden output names in input payload → DENY_Z2_SOURCE_FORBIDDEN
- Any real_source indicator when no_real_source_flag should be TRUE → DENY_Z2_REAL_SOURCE_FORBIDDEN
- Missing mandatory evidence chain fields → DENY_Z2_EVIDENCE_INCOMPLETE

---

## 6. Proof / Review Requirements

- Input contract must be tested with valid B1 CompositionGraphResponse fixture
- Each forbidden input must have a dedicated rejection test
- Input validation must produce deterministic z2_report_node_hash
- Evidence chain inheritance from B1 must be verified hash-by-hash
- z9_review_snapshot_candidate preparation must trace all inputs

---

## 7. Next Legal Entry

- Proceed to OUTPUT_CONTRACT.md for formal output specification
- Input contract validation feeds into DEGRADATION_POLICY.md
- Input hash computation feeds into EVIDENCE_CHAIN.md
