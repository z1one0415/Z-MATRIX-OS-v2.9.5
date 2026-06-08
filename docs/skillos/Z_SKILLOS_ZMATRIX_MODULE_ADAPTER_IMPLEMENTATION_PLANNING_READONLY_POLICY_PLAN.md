# Z-SkillOS Z-MATRIX Module Adapter Implementation Planning — READONLY_POLICY_PLAN

> **Lane**: A1 — Z-MATRIX Module Adapter Implementation Planning
> **Branch**: `plan/skillos-zmatrix-module-adapter-implementation-planning` @ `3e6ce10c`
> **Date**: 2026-06-08
> **Status**: FUTURE_PLAN_ONLY | Level 5 BLOCKED

---

## §1 — Read-Only Policy Mandate

The read-only policy is the foundational safety guarantee for Batch 1 adapters.
Four of five adapters operate in strict read-only mode. The fifth
(document_generation_in_memory) is permitted only in-memory writes with no
disk, network, or subprocess access.

---

## §2 — Read-Only Enforcement Layers

| Layer | Mechanism | Scope |
|-------|-----------|-------|
| L1: Contract | AdapterContract.forbidden_actions | Per-adapter declaration |
| L2: Permission | Permission Engine deny-by-default | Runtime enforcement |
| L3: Runtime | Runtime Guard hook interception | System-call level |
| L4: Evidence | Evidence Bus audit trail | Post-hoc verification |
| L5: Policy | Policy Router configuration | Centralized policy |

---

## §3 — What Read-Only Means

| Operation | Allowed? | Condition |
|-----------|----------|-----------|
| Read file from allowed paths | ✅ | Contract-defined paths only |
| Query registry | ✅ | Read-only registry methods |
| Recall memory | ✅ | Read-only memory queries |
| Read research output | ✅ | Approved output paths |
| Generate in-memory document | ✅ (A5 only) | No disk flush |
| Write to disk | ❌ | BLOCKED at L3 |
| Open network socket | ❌ | BLOCKED at L3 |
| Execute subprocess | ❌ | BLOCKED at L3 |
| Modify registry | ❌ | BLOCKED at L2 |
| Modify memory | ❌ (A1-A4) | BLOCKED at L2 |
| Delete files | ❌ | BLOCKED at L3 |
| Send HTTP request | ❌ | BLOCKED at L3 |

---

## §4 — Allowed Read Paths

| Adapter | Allowed Paths |
|---------|--------------|
| A1: capability_registry_readonly | Registry data store (read-only) |
| A2: z9_memory_review_readonly | Z9 memory store (read-only) |
| A3: z2_research_output_readonly | `记忆宫殿/Z2信息熔炉/投资记忆银行/` |
| A4: local_report_reading | `docs/`, `记忆宫殿/`, workspace |
| A5: document_generation_in_memory | In-memory buffer only |

---

## §5 — Forbidden Paths (All Adapters)

| Path Pattern | Reason |
|-------------|--------|
| `/etc/*` | System configuration |
| `~/.ssh/*` | SSH keys |
| `~/.aws/*` | Cloud credentials |
| `~/Library/*` | macOS user data |
| `*.pem`, `*.key` | Private keys |
| `/proc/*`, `/sys/*` | System internals |
| Any path outside workspace | Scope boundary |

---

## §6 — Violation Response

| Violation | Detection Layer | Response |
|-----------|----------------|----------|
| Write attempt | L3 Runtime Guard | KILL + evidence + alert |
| Network attempt | L3 Runtime Guard | KILL + evidence + alert |
| Subprocess attempt | L3 Runtime Guard | KILL + evidence + alert |
| Unauthorized path read | L2 Permission | REJECT + evidence |
| Registry mutation | L2 Permission | REJECT + evidence |
| Memory mutation (A1-A4) | L2 Permission | REJECT + evidence |

---

## §7 — Governance

This read-only policy is FUTURE_PLAN_ONLY. All enforcement mechanisms
are defined but not active. The policy takes effect only after all planning,
review, and merge gates are passed. No adapter shall be ENABLED until the
full five-layer read-only enforcement is operational and verified.

---

> **Signature**: ☯️ Z2天师 — Hermes Research Kernel
> **Pipeline**: Z-G14 | Lane A1: Read-Only Policy Plan
