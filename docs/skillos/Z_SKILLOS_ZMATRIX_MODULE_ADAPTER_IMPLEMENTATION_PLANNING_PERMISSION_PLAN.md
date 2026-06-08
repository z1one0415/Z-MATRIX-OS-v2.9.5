# Z-SkillOS Z-MATRIX Module Adapter Implementation Planning — PERMISSION_PLAN

> **Lane**: A1 — Z-MATRIX Module Adapter Implementation Planning
> **Branch**: `plan/skillos-zmatrix-module-adapter-implementation-planning` @ `3e6ce10c`
> **Date**: 2026-06-08
> **Status**: FUTURE_PLAN_ONLY | Level 5 BLOCKED

---

## §1 — Permission Model Overview

The Z-MATRIX Module Adapter permission model enforces least-privilege access
for all adapter invocations. Every adapter declares required permissions in
its contract, and the Permission Engine validates these before execution.

---

## §2 — Permission Taxonomy

| Permission Token | Description | Risk Level |
|-----------------|-------------|------------|
| `skills:read` | Read skill definitions and metadata | LOW |
| `registry:inspect` | Inspect capability registry | LOW |
| `registry:read` | Read registry entries | LOW |
| `memory:recall` | Recall from memory stores | LOW |
| `memory:write` | Write to in-memory stores | MEDIUM |
| `research:read` | Read research outputs | LOW |
| `filesystem:read` | Read local files | LOW |
| `filesystem:write` | Write to filesystem | HIGH |
| `network:outbound` | Make outbound network calls | HIGH |
| `execute:subprocess` | Execute subprocesses | CRITICAL |
| `execute:trade` | Execute trades | FORBIDDEN |
| `publish:external` | Publish to external systems | FORBIDDEN |

---

## §3 — Permission Matrix (Batch 1)

| Permission | A1 | A2 | A3 | A4 | A5 |
|-----------|----|----|----|----|-----|
| `skills:read` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `registry:inspect` | ✅ | | | | |
| `memory:recall` | | ✅ | | | |
| `memory:write` | | | | | ✅ |
| `research:read` | | | ✅ | | |
| `filesystem:read` | | | | ✅ | |
| `filesystem:write` | | | | | |
| `network:outbound` | | | | | |
| `execute:subprocess` | | | | | |
| `execute:trade` | | | | | |
| `publish:external` | | | | | |

---

## §4 — Permission Enforcement Flow

```
Adapter Invocation
  │
  ├──► 1. Extract required_permissions from contract
  ├──► 2. Check caller's granted permissions
  ├──► 3. If caller lacks ANY required permission:
  │       └──► REJECT with PermissionDenied evidence
  ├──► 4. Check forbidden_actions against caller permissions
  ├──► 5. If caller has ANY forbidden permission:
  │       └──► REJECT with ForbiddenActionDetected evidence
  └──► 6. Proceed to execution
```

---

## §5 — Permission Escalation Policy

Permission escalation is EXPLICITLY FORBIDDEN. No adapter may:
1. Request permissions beyond its declared contract.
2. Dynamically escalate permissions at runtime.
3. Inherit permissions from caller beyond contract scope.
4. Chain-invoke another adapter to bypass permission checks.

Any violation triggers immediate KILL + evidence + audit alert.

---

## §6 — Default Deny

All permissions default to DENIED. An adapter has exactly zero permissions
unless explicitly granted in its contract. Even the `skills:read` permission
must be explicitly declared. There is no "default allow" or "inherit all"
mechanism.

---

## §7 — Governance

This permission model is FUTURE_PLAN_ONLY. The Permission Engine, token
taxonomy, and enforcement flow are defined but not implemented. All adapters
are DISABLED by default, and permission enforcement is inactive until the
full planning-review-merge pipeline is satisfied.

---

> **Signature**: ☯️ Z2天师 — Hermes Research Kernel
> **Pipeline**: Z-G14 | Lane A1: Permission Plan
