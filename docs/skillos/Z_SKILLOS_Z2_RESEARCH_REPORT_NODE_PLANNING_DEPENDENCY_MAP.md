# Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_PLANNING — DEPENDENCY_MAP

> Dependency graph and evidence chain for Z2 Research Report Node.
> Branch: plan/skillos-z2-research-report-node-planning
> Base commit: 74c27fa

---

## 1. Status

| Field | Value |
|-------|-------|
| Document | DEPENDENCY_MAP |
| Status | PLANNING |
| Created | 2026-06-09 |
| Parent | SCOPE.md |
| Dependency | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED (postmerge HEAD = 74c27fa) |

---

## 2. Scope

This document maps all dependencies of the Z2 Research Report Node, establishing:
- Which components Z2 consumes
- The access mode for each dependency
- The evidence chain from source to Z2 report output
- Forbidden dependency paths that must never be traversed

The Z2 Research Report Node consumes B1 CompositionGraphResponse as its sole structured input.
All other data arrives transitively through B1 or as static runtime context.

---

## 3. Dependency / Evidence

### 3.1 Primary Dependency Graph

```
┌─────────────────────────────────────────────────────┐
│                    Z2 Research Report Node            │
│                                                       │
│  Input: B1 CompositionGraphResponse                  │
│  Output: 12-section report + z9_review_snapshot      │
│  Hash: z2_report_node_hash                           │
└───────────────────────┬──────────────────────────────┘
                        │ consumes (readonly)
                        ▼
┌─────────────────────────────────────────────────────┐
│  B1 CompositionGraphResponse                         │
│  Source: B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_         │
│          DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED │
│  Commit: 74c27fa (postmerge HEAD)                    │
└───────────────────────┬──────────────────────────────┘
                        │ contains
                        ▼
┌─────────────────────────────────────────────────────┐
│  B1 Graph Evidence Chain                             │
│  - source_class                                      │
│  - no_real_source_flag                               │
│  - fixture_source_commit                             │
│  - request_hash / response_hash_placeholder          │
│  - factor_decision_hash / bridge_decision_hash       │
│  - graph_node_hash / graph_edge_hash                 │
│  - permission_tier                                   │
│  - forbidden_outputs_removed_hash                    │
│  - rollback_marker / privacy_marker                  │
│  - c1_handoff_marker                                 │
└───────────────────────┬──────────────────────────────┘
                        │ transits through B1
                        ▼
┌─────────────────────────────────────────────────────┐
│  A1 Bridge Evidence                                  │
│  - Available only through B1 path                    │
│  - Never accessed directly                           │
└─────────────────────────────────────────────────────┘
```

### 3.2 Optional Future Dependencies

| Dependency | Status | Access Mode | Gate |
|-----------|--------|-------------|------|
| FactorEvaluationMatrix | NOT YET AVAILABLE | Readonly handoff | Future planning doc required |
| Small Real Sample Read-Only summary | NOT YET AVAILABLE | Readonly | Future planning doc required |

### 3.3 Runtime Dependencies (Non-Data)

| Dependency | Type | Access |
|-----------|------|--------|
| User research question | Static context | Immutable at invocation |
| Report template | In-memory | Local, no external I/O |
| Degradation policy | Configuration | Loaded at init |
| Confidence policy | Configuration | Loaded at init |

---

## 4. Boundary

### Permitted Dependency Paths:
- Z2 ← B1 CompositionGraphResponse (direct)
- Z2 ← B1 evidence chain (through B1 response)
- Z2 ← A1 bridge evidence (through B1 only)
- Z2 ← Factor Library metadata (through B1/A1 readonly)

### FORBIDDEN Dependency Paths:
- Z2 ← FactorInvocationResponse (NEVER)
- Z2 ← Raw factor values (NEVER)
- Z2 ← research/factor_library files (NEVER)
- Z2 ← Broker systems (NEVER)
- Z2 ← Production systems (NEVER)
- Z2 ← Real returns / real trades (NEVER)
- Z2 ← Paper trades (NEVER)
- Z2 ← Z8 / Z9 / V3 runtime (NEVER)

---

## 5. Forbidden Actions

- Importing any module that provides direct factor invocation
- Creating any dependency path that bypasses B1
- Accessing any system marked FORBIDDEN in the dependency map
- Modifying the B1 CompositionGraphResponse after receipt
- Caching B1 responses across invocations without hash verification
- Skipping evidence chain validation before report generation

---

## 6. Proof / Review Requirements

- Dependency map must be verifiable through import analysis
- No forbidden imports may exist in the codebase (test_no_forbidden_imports.py)
- Evidence chain hashes (z2_report_node_hash, z2_report_evidence_hash) must be deterministic
- All dependency paths must be traceable from Z2 output back to B1 source
- no_alpha_claim and no_trade_signal invariants must hold regardless of input content

---

## 7. Next Legal Entry

- Proceed to INPUT_CONTRACT.md for formal input specification
- Dependency map feeds into EVIDENCE_CHAIN.md for hash propagation rules
- All forbidden paths validated in REVIEW_CHECKLIST.md
