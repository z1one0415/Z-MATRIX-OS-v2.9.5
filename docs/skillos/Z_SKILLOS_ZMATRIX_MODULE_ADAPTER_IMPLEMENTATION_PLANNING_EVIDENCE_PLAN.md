# Z-SkillOS Z-MATRIX Module Adapter Implementation Planning — EVIDENCE_PLAN

> **Lane**: A1 — Z-MATRIX Module Adapter Implementation Planning
> **Branch**: `plan/skillos-zmatrix-module-adapter-implementation-planning` @ `3e6ce10c`
> **Date**: 2026-06-08
> **Status**: FUTURE_PLAN_ONLY | Level 5 BLOCKED

---

## §1 — Evidence Philosophy

Every Z-MATRIX Module Adapter invocation produces an immutable evidence record.
Evidence provides the traceability backbone for audit, debugging, regression
testing, and compliance verification. Evidence is mandatory — not optional.

---

## §2 — Evidence Record Structure

```python
@dataclass
class EvidenceRecord:
    evidence_id: str               # UUID v4
    invocation_id: str             # Links to invocation
    adapter_id: str                # Which adapter
    contract_hash: str             # Contract version at invocation
    timestamp: datetime            # Invocation start time
    duration_ms: int               # Execution duration
    status: AdapterStatus          # SUCCESS | REJECTED | TIMEOUT | ERROR | KILLED
    input_hash: str                # SHA-256 of serialized input
    output_hash: str               # SHA-256 of serialized output
    permission_checks: List[Dict]  # Each permission check result
    forbidden_checks: List[Dict]   # Each forbidden action check
    schema_validations: List[Dict] # Input/output schema validation results
    errors: List[Dict]             # Any errors encountered
    warnings: List[Dict]           # Any warnings raised
    previous_evidence_hash: str    # Hash chain link
    parent_invocation_id: str      # Parent invocation (for chained calls)
```

---

## §3 — Evidence Hash Chain

Each evidence record links to the previous record via `previous_evidence_hash`,
forming an append-only hash chain:

```
E0 → E1 → E2 → E3 → ... → En

Where: En.previous_evidence_hash = SHA-256(En-1)
```

The genesis block (E0) has `previous_evidence_hash = "genesis"`.
Any gap or mismatch in the chain is detectable and triggers an integrity alert.

---

## §4 — Evidence Capture Points

| Capture Point | When | What |
|--------------|------|------|
| CP1: Pre-invoke | Before execution | Input, contract hash, timestamp |
| CP2: Permission | After permission check | Permission check results |
| CP3: Schema-in | After input validation | Input schema validation |
| CP4: Schema-out | After output validation | Output schema validation |
| CP5: Post-execute | After execution | Output hash, duration, status |
| CP6: Error | On error/exception | Error details, stack trace |
| CP7: Warning | On warning | Warning details |

---

## §5 — Evidence Storage

| Tier | Storage | Retention |
|------|---------|-----------|
| Hot | In-memory buffer | Last 1000 records |
| Warm | Local evidence store | 30 days |
| Cold | Evidence archive | 365 days |
| Audit | Immutable audit log | Permanent |

Evidence records are immutable once written. No deletion or modification
is permitted. The evidence store is itself read-only for Batch 1 adapters.

---

## §6 — Evidence Privacy Boundary

1. Evidence records never contain raw input/output data — only hashes.
2. PII and sensitive data are redacted before hashing.
3. Full input/output data available only via separate authorized access.
4. Evidence store access requires `evidence:read` permission.
5. Evidence chain integrity is verifiable without accessing raw data.

---

## §7 — Governance

This evidence plan is FUTURE_PLAN_ONLY. The evidence record structure,
hash chain, capture points, and storage architecture are defined but not
implemented. Evidence capture is gated behind the full planning-review-merge
pipeline. All adapters are DISABLED until evidence infrastructure is operational.

---

> **Signature**: ☯️ Z2天师 — Hermes Research Kernel
> **Pipeline**: Z-G14 | Lane A1: Evidence Plan
