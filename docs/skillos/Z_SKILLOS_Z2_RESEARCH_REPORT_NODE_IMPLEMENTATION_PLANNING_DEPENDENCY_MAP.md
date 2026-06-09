# Z2 Research Report Node Implementation Planning — DEPENDENCY MAP

> Status: PLANNING_COMPLETE
> Seal: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED
> Date: 2026-06-09
> Branch: plan/skillos-z2-research-report-node-implementation-planning
> Base: c5f69f5

---

## 1. Status

| Field | Value |
|-------|-------|
| Phase | Planning (docs-only) |
| All dependencies | MERGED_AND_SEALED |
| postmerge HEAD | c5f69f5 |
| Confidence | HIGH_WITH_STRUCTURE_ONLY |

## 2. Scope

This document maps all upstream, lateral, and downstream dependencies for the Z2 Research Report Node implementation.

### Upstream Dependencies (Consumed)

| # | Dependency | Seal Marker | Provides |
|---|-----------|-------------|----------|
| 1 | Z2 Research Report Node Planning | Z2_RESEARCH_REPORT_NODE_PLANNING_CLEAN_MERGED_AND_SEALED | Architecture, model schemas, contract definitions |
| 2 | Z9 Review Node Planning | Z9_REVIEW_NODE_PLANNING_MERGED_AND_SEALED | z9_review_snapshot_candidate interface spec |
| 3 | B1 Composition Graph Factor Bridge | B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED | B1 CompositionGraphResponse structure |
| 4 | A1 Factor Library Bridge | A1_FACTOR_LIBRARY_BRIDGE_DISABLED_DEFAULT_P0_MERGED_AND_SEALED | Factor data access patterns |
| 5 | Factor Library Readonly Adapter | FACTOR_LIBRARY_READONLY_ADAPTER_DISABLED_DEFAULT_P0_MERGED_AND_SEALED | Read-only factor consumption interface |

### Lateral Dependencies (Shared Infrastructure)

| # | Component | Role |
|---|-----------|------|
| 1 | SkillOS capability_invocation_os registry | Node registration pattern |
| 2 | Kill-switch infrastructure | Disabled-by-default enforcement |
| 3 | Pydantic BaseModel | Model validation foundation |
| 4 | Python 3.11+ typing | Type annotation system |

### Downstream Dependencies (Consumers)

| # | Consumer | Interface | Status |
|---|----------|-----------|--------|
| 1 | Z9 Review Node | z9_review_snapshot_candidate | Planned (Z9 sealed) |
| 2 | SkillOS orchestrator | ResearchReportNodeResponse | Planned |
| 3 | Event store | Report archival | Future |

## 3. Dependency

### Dependency Resolution Order

```
FACTOR_LIBRARY_READONLY_ADAPTER (sealed)
    └── A1_FACTOR_LIBRARY_BRIDGE (sealed)
         └── B1_COMPOSITION_GRAPH_FACTOR_BRIDGE (sealed)
              └── Z2_RESEARCH_REPORT_NODE_PLANNING (sealed)
                   └── Z9_REVIEW_NODE_PLANNING (sealed)
                        └── THIS IMPLEMENTATION (planning)
```

### Version Pinning

| Dependency | Pinned At |
|-----------|-----------|
| postmerge HEAD | c5f69f5 |
| Python | ≥3.11 |
| Pydantic | ≥2.0 |

## 4. Boundary

- No dependency on external APIs or services
- No dependency on database state
- No dependency on file system state
- All dependencies resolved at import time via registry
- Circular dependency detection: none found in planned graph
- No optional dependencies — all are required for node operation

## 5. Forbidden

- No dependency on trading libraries
- No dependency on broker APIs
- No dependency on portfolio management systems
- No dependency on real-time market data feeds
- No dependency on order management systems
- Forbidden fields cannot appear in any dependency interface

## 6. Proof

- All 5 upstream dependencies verified as MERGED_AND_SEALED
- postmerge HEAD c5f69f5 confirmed
- Dependency graph is acyclic (DAG verified)
- No missing dependencies identified
- No version conflicts detected
- Downstream interface contracts are well-defined

## 7. Next

- Implementation will import from sealed upstream contracts only
- No new external dependencies will be added without review
- Dependency health check will be part of CI pipeline
- Any dependency change requires re-review of this map

---

**SEAL: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED**
