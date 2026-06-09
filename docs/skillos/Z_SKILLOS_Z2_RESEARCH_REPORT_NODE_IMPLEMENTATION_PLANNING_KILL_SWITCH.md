# Z2 Research Report Node Implementation Planning — KILL SWITCH

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
| Confidence | HIGH_WITH_STRUCTURE_ONLY |
| Default state | DISABLED (node produces no output) |
| Activation | Explicit environment variable required |
| Degradation on active | DENY_Z2_OUTPUTS_UNSAFE |

## 2. Scope

This document specifies the kill-switch design for the Z2 Research Report Node. The kill-switch follows the disabled-by-default pattern established in upstream dependencies.

### Kill-Switch Specification

| Property | Value |
|----------|-------|
| Environment variable | Z2_RESEARCH_REPORT_NODE_ENABLED |
| Required value to enable | "true" (case-sensitive) |
| Default (unset) | DISABLED |
| Default (empty string) | DISABLED |
| Default (any other value) | DISABLED |
| Check frequency | Once per invocation (no caching) |
| Override mechanism | None (env-var is sole authority) |

### State Machine

```
┌──────────────┐     env=true      ┌─────────────┐
│   DISABLED   │ ─────────────────> │   ENABLED   │
│ (default)    │                    │ (produces    │
│ No output    │ <───────────────── │  reports)   │
└──────────────┘   env≠true/unset   └─────────────┘
       │                                    │
       v                                    v
DENY_Z2_OUTPUTS_UNSAFE          Normal report generation
```

### Kill-Switch Placement

- Check is FIRST operation in node invocation
- Before any computation
- Before any input validation
- Before any resource allocation
- Single point of control (no distributed checks)

### Integration with Degradation

When kill-switch is DISABLED:
1. Node receives invocation
2. Kill-switch check returns DISABLED
3. Node immediately returns ReportDegradationStatus
4. Mode: DENY_Z2_OUTPUTS_UNSAFE
5. Reason: "Z2 Research Report Node is disabled by kill-switch"
6. No partial data emitted
7. No side effects

## 3. Dependency

- Pattern established in B1_COMPOSITION_GRAPH_FACTOR_BRIDGE_DISABLED_DEFAULT_P0_CLEAN_MERGED_AND_SEALED
- Pattern established in A1_FACTOR_LIBRARY_BRIDGE_DISABLED_DEFAULT_P0_MERGED_AND_SEALED
- Pattern established in FACTOR_LIBRARY_READONLY_ADAPTER_DISABLED_DEFAULT_P0_MERGED_AND_SEALED
- postmerge HEAD = c5f69f5

## 4. Boundary

- Kill-switch is the ONLY env-var read by this module
- Kill-switch check has zero side effects
- Kill-switch does not log sensitive data
- Kill-switch state is not persisted
- Kill-switch cannot be overridden by input parameters
- Kill-switch cannot be overridden by config files

## 5. Forbidden

The kill-switch mechanism MUST NOT:
- Accept any of the 14 forbidden fields as input
- Emit any of the 14 forbidden fields in its degradation response
- Be bypassable via any mechanism other than the env-var
- Cache its state across invocations
- Have admin/override modes

## 6. Proof

- test_disabled_default.py verifies DISABLED when env unset (planned)
- test_disabled_default.py verifies DISABLED when env empty (planned)
- test_disabled_default.py verifies DISABLED when env = "false" (planned)
- test_disabled_default.py verifies DISABLED when env = "TRUE" (case-sensitive) (planned)
- test_disabled_default.py verifies ENABLED only when env = "true" (planned)
- test_disabled_default.py verifies DENY_Z2_OUTPUTS_UNSAFE response (planned)

## 7. Next

- kill_switch.py is Batch 1 priority (alongside models and contracts)
- test_disabled_default.py is the FIRST test written
- Kill-switch audit in every code review
- No deployment without kill-switch verification

---

**SEAL: Z_SKILLOS_Z2_RESEARCH_REPORT_NODE_IMPLEMENTATION_PLANNING_SEALED**
