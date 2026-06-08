# Z-SkillOS Z-MATRIX Module Adapter Implementation Planning — CONTRACT_PLAN

> **Lane**: A1 — Z-MATRIX Module Adapter Implementation Planning
> **Branch**: `plan/skillos-zmatrix-module-adapter-implementation-planning` @ `3e6ce10c`
> **Date**: 2026-06-08
> **Status**: FUTURE_PLAN_ONLY | Level 5 BLOCKED

---

## §1 — Contract Philosophy

Every Z-MATRIX Module Adapter operates under a deterministic, verifiable contract.
The contract defines the adapter's interface, input/output schema, permission
requirements, evidence obligations, and failure modes. No adapter may execute
without a validated contract.

---

## §2 — Contract Structure

```python
@dataclass
class AdapterContract:
    adapter_id: str                    # Unique adapter identifier
    version: str                       # Semver version
    risk_tier: int                     # 0=readonly, 1=in-memory-write
    input_schema: Dict[str, Any]       # JSON Schema for inputs
    output_schema: Dict[str, Any]      # JSON Schema for outputs
    required_permissions: List[str]    # Permission tokens required
    forbidden_actions: List[str]       # Actions explicitly prohibited
    evidence_required: bool            # Whether evidence capture is mandatory
    timeout_ms: int                    # Maximum execution time
    max_output_size_bytes: int         # Maximum output payload size
    retry_policy: Optional[Dict]       # Retry configuration
    degrade_policy: Optional[Dict]     # Degradation behavior
```

---

## §3 — Contract Per Adapter (Batch 1)

### Adapter 1: capability_registry_readonly
| Field | Value |
|-------|-------|
| risk_tier | 0 |
| required_permissions | `["skills:read", "registry:inspect"]` |
| forbidden_actions | `["write", "delete", "modify", "register"]` |
| evidence_required | True |
| timeout_ms | 5000 |
| max_output_size_bytes | 1048576 |

### Adapter 2: z9_memory_review_readonly
| Field | Value |
|-------|-------|
| risk_tier | 0 |
| required_permissions | `["skills:read", "memory:recall"]` |
| forbidden_actions | `["write", "delete", "modify", "train"]` |
| evidence_required | True |
| timeout_ms | 10000 |
| max_output_size_bytes | 5242880 |

### Adapter 3: z2_research_output_readonly
| Field | Value |
|-------|-------|
| risk_tier | 0 |
| required_permissions | `["skills:read", "research:read"]` |
| forbidden_actions | `["write", "execute", "publish"]` |
| evidence_required | True |
| timeout_ms | 30000 |
| max_output_size_bytes | 10485760 |

### Adapter 4: local_report_reading
| Field | Value |
|-------|-------|
| risk_tier | 0 |
| required_permissions | `["skills:read", "filesystem:read"]` |
| forbidden_actions | `["write", "delete", "execute", "network"]` |
| evidence_required | True |
| timeout_ms | 15000 |
| max_output_size_bytes | 20971520 |

### Adapter 5: document_generation_in_memory
| Field | Value |
|-------|-------|
| risk_tier | 1 |
| required_permissions | `["skills:read", "memory:write"]` |
| forbidden_actions | `["disk:write", "network", "execute"]` |
| evidence_required | True |
| timeout_ms | 60000 |
| max_output_size_bytes | 52428800 |

---

## §4 — Contract Validation Rules

1. Every adapter MUST declare its contract at class definition time.
2. Contract is IMMUTABLE after registration — no runtime mutation.
3. Permission check runs BEFORE adapter execution.
4. Forbidden action check runs BEFORE and DURING execution.
5. Evidence capture is MANDATORY for all adapters.
6. Timeout is a hard boundary — no extension allowed.
7. Output size violation triggers immediate truncation with evidence.

---

## §5 — Contract Enforcement Architecture

```
Invoke Request
  │
  ├──► 1. Contract Lookup (Registry)
  ├──► 2. Permission Validation (Permission Engine)
  ├──► 3. Forbidden Action Pre-Check (Policy Router)
  ├──► 4. Input Schema Validation (Schema Validator)
  ├──► 5. Execute with Timeout (Runtime Guard)
  ├──► 6. Output Schema Validation (Schema Validator)
  ├──► 7. Evidence Capture (Evidence Bus)
  └──► 8. Return AdapterResult
```

---

## §6 — Contract Violation Handling

| Violation | Severity | Action |
|-----------|----------|--------|
| Missing contract | CRITICAL | BLOCK execution |
| Permission denied | HIGH | BLOCK + evidence |
| Forbidden action detected | CRITICAL | KILL + evidence + alert |
| Input schema mismatch | MEDIUM | REJECT + evidence |
| Timeout | HIGH | KILL + evidence |
| Output size exceeded | MEDIUM | TRUNCATE + evidence |
| Output schema mismatch | HIGH | REJECT + evidence |
| Evidence capture failure | HIGH | BLOCK + alert |

---

## §7 — Governance

All contracts are FUTURE_PLAN_ONLY. No contract shall be registered or enforced
until the full planning-review-merge pipeline completes. Contracts are subject
to immutable hash verification and golden regression testing.

---

> **Signature**: ☯️ Z2天师 — Hermes Research Kernel
> **Pipeline**: Z-G14 | Lane A1: Contract Plan
