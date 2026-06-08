# Z-SkillOS Skill Composition Graph P0 Implementation Planning — PERMISSION PROPAGATION PLAN

> Status: FUTURE_PLAN_ONLY | Level 5 BLOCKED | docs-only | No implementation | No execution | No Z-MATRIX call
> Branch: plan/skillos-skill-composition-graph-p0-implementation-planning
> Pipeline: Lane B1 — Skill Composition Graph P0 Implementation Planning
> Version: v1.0.0-draft

---

## 1. Purpose

This document defines the implementation specification for permission propagation across the
composition graph. It covers the monotonic non-increasing rule, escalation detection and rejection,
write-tier blocking, effective tier computation, and the full permission validation pipeline.

## 2. Permission Tier Model

### 2.1 Tier Definitions (P0 Subset)

| Tier | Name | Description | Allowed Actions |
|------|------|-------------|-----------------|
| 0 | READONLY | Read-only capability; no state modification | Read files, inspect data, analyze |
| 1 | PLANNING | Planning-only; creates plans but does not execute | Create plans, define schemas, validate contracts |

### 2.2 Core Rule: Monotonic Non-Increasing

```
∀ edge ∈ graph: edge.downstream.permission_tier ≤ edge.upstream.permission_tier
```

A downstream node must never have a higher permission tier than its upstream node.
Permission can only stay the same or decrease; it can never increase.

### 2.3 Propagation Matrix (P0)

| Upstream Tier | Downstream Tier | Allowed? | Rationale |
|:---:|:---:|:---:|------|
| 0 | 0 | ✅ | Equal readonly |
| 1 | 1 | ✅ | Equal planning |
| 1 | 0 | ✅ | De-escalation: planning → readonly |
| 0 | 1 | ❌ | ESCALATION FORBIDDEN |
| 0 | 2+ | ❌ | Write escalation FORBIDDEN |
| 1 | 2+ | ❌ | Write escalation FORBIDDEN |

## 3. Escalation Detection

### 3.1 Detection Algorithm

```python
def check_monotonic(upstream_tier: int, downstream_tier: int) -> bool:
    """Returns True if propagation is valid (monotonic non-increasing)."""
    return downstream_tier <= upstream_tier
```

### 3.2 Escalation Response

When escalation is detected:
1. The edge is marked with `permission_propagation.is_valid = False`
2. The escalation reason is recorded in `permission_propagation.reason`
3. The entire graph is marked `FORBIDDEN` — it cannot proceed to execution
4. A `PermissionEscalationError` is raised
5. The graph degrades to `PLAN_ONLY` or `NOOP`

### 3.3 Escalation Scenarios

| Scenario | Detection | Response |
|----------|-----------|----------|
| Upstream Tier 0, Downstream Tier 1 | EC-08 violation | FORBIDDEN, escalate error |
| Upstream Tier 1, Downstream Tier 4 | Write tier blocked | FORBIDDEN, write_blocked error |
| Two-node graph, first node escalated | At edge validation | Whole graph FORBIDDEN |
| Single-node graph, Tier > 1 | NC-04 violation | Node rejected individually |

## 4. Write-Tier Blocking

### 4.1 Blocked Tiers in P0

| Tier | Name | P0 Policy |
|------|------|-----------|
| 2 | RESEARCH | Blocked — never allowed in P0 |
| 3 | ADVISORY | Blocked — never allowed in P0 |
| 4 | EXECUTION | Blocked — permanently forbidden |
| 5 | PRODUCTION | Blocked — permanently forbidden |

### 4.2 Blocking Enforcement

```python
def validate_node_tier(tier: int) -> Optional[WriteTierBlockedError]:
    P0_MAX_TIER = 1
    if tier > P0_MAX_TIER:
        return WriteTierBlockedError(
            f"Tier {tier} is blocked in P0. Maximum allowed: {P0_MAX_TIER}"
        )
    return None
```

## 5. Effective Tier Computation

The effective tier of the graph is the minimum permission tier across all nodes.
This determines what the graph as a whole is allowed to do.

```python
def compute_effective_tier(graph: CompositionGraph) -> int:
    if not graph.nodes:
        return 0
    return min(node.permission_tier for node in graph.nodes)
```

### 5.1 Effective Tier Examples

| Nodes | Effective Tier | Graph Allowed |
|-------|:---:|------|
| [Tier 1, Tier 0] | 0 | Readonly only |
| [Tier 1, Tier 1] | 1 | Planning only |
| [Tier 0] | 0 | Readonly only |
| [Tier 1] | 1 | Planning only |

## 6. Permission Validation Pipeline

```python
def validate_all_permissions(graph: CompositionGraph) -> List[PermissionError]:
    errors = []

    # Step 1: Validate individual node tiers
    for node in graph.nodes:
        err = validate_node_tier(node.permission_tier)
        if err:
            errors.append(err)

    # Step 2: Validate edge permission propagation
    for edge in graph.edges:
        upstream = graph.get_node(edge.upstream_node_id)
        downstream = graph.get_node(edge.downstream_node_id)
        if not check_monotonic(upstream.permission_tier, downstream.permission_tier):
            errors.append(PermissionEscalationError(
                f"Escalation: Tier {upstream.permission_tier} → Tier {downstream.permission_tier}"
            ))

    # Step 3: If any errors, mark graph FORBIDDEN
    if errors:
        graph.status = "FORBIDDEN"

    return errors
```

## 7. Permission Propagation Policy

### 7.1 Policy Rules (PP-01 through PP-06)

| Rule ID | Rule | Enforcement |
|---------|------|-------------|
| PP-01 | No node may have tier > 1 in P0 | NC-04 at node validation |
| PP-02 | Downstream tier ≤ upstream tier for all edges | EC-08 at edge validation |
| PP-03 | Escalation → whole graph FORBIDDEN | Build-time enforcement |
| PP-04 | Effective tier = min(all node tiers) | Computed at graph build |
| PP-05 | No dynamic tier adjustment | Immutable post-build |
| PP-06 | Write-tier nodes permanently forbidden in P0 | Immediate rejection |

### 7.2 Degradation on Permission Failure

When permission validation fails:
1. Graph status → `FORBIDDEN`
2. Degradation state → `PLAN_ONLY` (if graph structure is valid) or `NOOP` (if structure invalid)
3. Rollback marker is set
4. No execution is attempted
5. Error details are captured in graph metadata
