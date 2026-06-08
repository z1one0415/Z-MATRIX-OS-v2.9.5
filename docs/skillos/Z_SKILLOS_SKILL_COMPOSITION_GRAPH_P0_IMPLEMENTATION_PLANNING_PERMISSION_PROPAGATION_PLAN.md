# Z-SkillOS Skill Composition Graph P0 Implementation Planning — PERMISSION PROPAGATION PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft

---

## 1. Purpose

This document defines the implementation specification for permission propagation across the
composition graph. Covers the monotonic non-increasing rule, escalation detection, write-tier
blocking, effective tier computation, and the full permission validation pipeline.

## 2. Permission Tier Model

### 2.1 Tier Definitions (P0 Subset)

| Tier | Name | Description | Allowed Actions |
|------|------|-------------|-----------------|
| 0 | READONLY | Read-only capability | Read files, inspect data, analyze |
| 1 | PLANNING | Planning-only | Create plans, define schemas, validate contracts |

### 2.2 Core Rule: Monotonic Non-Increasing

```
For all edges in graph: edge.downstream.permission_tier <= edge.upstream.permission_tier
```

### 2.3 Propagation Matrix (P0)

| Upstream Tier | Downstream Tier | Allowed? | Rationale |
|:---:|:---:|:---:|------|
| 0 | 0 | YES | Equal readonly |
| 1 | 1 | YES | Equal planning |
| 1 | 0 | YES | De-escalation: planning -> readonly |
| 0 | 1 | NO | ESCALATION FORBIDDEN |
| 0 | 2+ | NO | Write escalation FORBIDDEN |
| 1 | 2+ | NO | Write escalation FORBIDDEN |

## 3. Escalation Detection

### 3.1 Detection Algorithm

```python
def check_monotonic(upstream_tier: int, downstream_tier: int) -> bool:
    return downstream_tier <= upstream_tier
```

### 3.2 Escalation Response
When escalation is detected:
1. Edge marked with permission_propagation.is_valid = False
2. Entire graph marked FORBIDDEN
3. PermissionEscalationError raised
4. Graph degrades to PLAN_ONLY or NOOP

## 4. Write-Tier Blocking

### 4.1 Blocked Tiers in P0

| Tier | Name | P0 Policy |
|------|------|-----------|
| 2 | RESEARCH | Blocked |
| 3 | ADVISORY | Blocked |
| 4 | EXECUTION | Permanently forbidden |
| 5 | PRODUCTION | Permanently forbidden |

```python
def validate_node_tier(tier: int) -> Optional[WriteTierBlockedError]:
    if tier > 1:
        return WriteTierBlockedError(f"Tier {tier} blocked in P0. Max: 1")
    return None
```

## 5. Effective Tier Computation

```python
def compute_effective_tier(graph: CompositionGraph) -> int:
    if not graph.nodes: return 0
    return min(node.permission_tier for node in graph.nodes)
```

## 6. Permission Validation Pipeline

```python
def validate_all_permissions(graph: CompositionGraph) -> List[PermissionError]:
    errors = []
    for node in graph.nodes:
        err = validate_node_tier(node.permission_tier)
        if err: errors.append(err)
    for edge in graph.edges:
        upstream = graph.get_node(edge.upstream_node_id)
        downstream = graph.get_node(edge.downstream_node_id)
        if not check_monotonic(upstream.permission_tier, downstream.permission_tier):
            errors.append(PermissionEscalationError(
                f"Escalation: Tier {upstream.permission_tier} -> Tier {downstream.permission_tier}"
            ))
    if errors:
        graph.status = "FORBIDDEN"
    return errors
```

## 7. Permission Propagation Policy Rules (PP-01 through PP-06)

| Rule ID | Rule | Enforcement |
|---------|------|-------------|
| PP-01 | No node may have tier > 1 in P0 | NC-04 at node validation |
| PP-02 | Downstream tier <= upstream tier for all edges | EC-08 at edge validation |
| PP-03 | Escalation -> whole graph FORBIDDEN | Build-time enforcement |
| PP-04 | Effective tier = min(all node tiers) | Computed at graph build |
| PP-05 | No dynamic tier adjustment | Immutable post-build |
| PP-06 | Write-tier nodes permanently forbidden in P0 | Immediate rejection |
