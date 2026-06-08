# Z-SkillOS Z-MATRIX Module Adapter Implementation Planning — REGISTRY_PLAN

> **Lane**: A1 — Z-MATRIX Module Adapter Implementation Planning
> **Branch**: `plan/skillos-zmatrix-module-adapter-implementation-planning` @ `3e6ce10c`
> **Date**: 2026-06-08
> **Status**: FUTURE_PLAN_ONLY | Level 5 BLOCKED

---

## §1 — Registry Purpose

The Capability Registry serves as the single source of truth for all Z-MATRIX
Module Adapters. It provides discovery, lifecycle management, version tracking,
and status monitoring. Every adapter MUST be registered before invocation.

---

## §2 — Registry Data Model

```python
@dataclass
class AdapterRegistryEntry:
    adapter_id: str                 # Unique identifier
    adapter_name: str               # Human-readable name
    version: str                    # Semver
    status: AdapterStatus           # DISABLED | ENABLED | DEGRADED | KILLED
    contract_hash: str              # SHA-256 of contract
    registered_at: datetime         # Registration timestamp
    last_verified_at: datetime      # Last contract verification
    risk_tier: int                  # 0 or 1
    dependencies: List[str]         # Adapter IDs this depends on
    evidence_enabled: bool          # Whether evidence capture is on
    invocation_count: int           # Total invocations (read-only counter)
    last_invocation_at: datetime    # Last invocation timestamp
```

---

## §3 — Registry Operations

| Operation | Permission | Description |
|-----------|-----------|-------------|
| `register` | `registry:write` | Register a new adapter |
| `discover` | `registry:read` | List all registered adapters |
| `lookup` | `registry:read` | Get adapter by ID |
| `verify` | `registry:read` | Verify contract hash integrity |
| `set_status` | `registry:admin` | Change adapter status |
| `health_check` | `registry:read` | Check adapter health |
| `audit_log` | `registry:read` | Read audit trail |

---

## §4 — Batch 1 Registration Plan

| # | Adapter ID | Initial Status | Risk Tier |
|---|-----------|---------------|-----------|
| 1 | `zmatrix.capability_registry_readonly` | DISABLED | 0 |
| 2 | `zmatrix.z9_memory_review_readonly` | DISABLED | 0 |
| 3 | `zmatrix.z2_research_output_readonly` | DISABLED | 0 |
| 4 | `zmatrix.local_report_reading` | DISABLED | 0 |
| 5 | `zmatrix.document_generation_in_memory` | DISABLED | 1 |

All five adapters start in DISABLED state. No adapter may transition to
ENABLED without passing all planning, review, and merge gates.

---

## §5 — Registry Lifecycle State Machine

```
                    ┌─────────┐
           register │DISABLED │
         ┌─────────►│         │◄──────────┐
         │          └────┬────┘           │
         │               │ enable         │ disable
         │          ┌────▼────┐           │
         │          │ ENABLED │───────────┘
         │          │         │
         │          └────┬────┘
         │               │ degrade
         │          ┌────▼────┐
         │          │DEGRADED │
         │          │         │
         │          └────┬────┘
         │               │ kill
         │          ┌────▼────┐
         │          │ KILLED  │ (terminal)
         │          │         │
         │          └─────────┘
```

---

## §6 — Registry Integrity Guarantees

1. Adapter contract hash is computed at registration and verified on every lookup.
2. Status transitions are logged immutably in the evidence chain.
3. No adapter can be removed from the registry — only status-changed.
4. Registry itself is read-only for all Batch 1 adapters.
5. Registry audit trail is append-only and hash-chained.

---

## §7 — Governance

The registry is FUTURE_PLAN_ONLY. Registration data structures, state machine,
and integrity guarantees are defined here but NOT implemented. Registry
implementation is gated behind the full planning-review-merge pipeline.

---

> **Signature**: ☯️ Z2天师 — Hermes Research Kernel
> **Pipeline**: Z-G14 | Lane A1: Registry Plan
