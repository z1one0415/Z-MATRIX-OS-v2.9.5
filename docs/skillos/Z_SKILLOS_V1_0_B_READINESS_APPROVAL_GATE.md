# Z-SkillOS v1.0-B Readiness Approval Gate

## Status

Z_SKILLOS_V1_0_B_READINESS_APPROVAL_GATE_PENDING

---

## Current Baseline

| Metric | Value |
|:--|:--|
| v1.0-A status | APPROVED |
| v1.0-A approved commit | `0f3fa90` |
| v1.0-A approval commit | `d74df48` |
| contract registry | 104 entries, 20 registry domains, 17 concrete domains |
| contract loader | Read-only, no enforcement |
| invoke_skill | Unmodified v0.x dispatch |
| result_envelope | Unmodified v0.x envelope |
| runtime schema validation | None |
| production | BLOCKED |
| broker_runtime | BLOCKED |
| real_trade | BLOCKED |

---

## Proposed v1.0-B Scope

v1.0-B must NOT be a direct `invoke_skill` hard-enforcement change.

v1.0-B must be: **shadow/audit-only schema validation scaffold**.

### What shadow/audit-only means

- A standalone validator reads the contract registry
- On each `invoke_skill` call, the validator checks input_schema and output_schema against the contract
- The validator produces an audit report — it does NOT block the invocation
- v0.x runtime behavior is completely unchanged
- If the audit reveals gaps, the contract is refined before any hard enforcement is considered

### Distinguished from hard enforcement

| Aspect | Shadow/Audit | Hard Enforcement |
|:--|:--|:--|
| Blocks invocation on failure | No | Yes |
| Modifies invoke_skill | No (wrapper/hook) | Yes (inline) |
| Produces output | Audit report only | Error response |
| v0.x runtime impact | Zero | Can break existing calls |
| Safety if contract is wrong | Safe | Dangerous |

---

## Questions To Approve

Answer each with explicit rationale. All default to "no" unless approved.

| # | Question | Default | Impact |
|:--:|------|:--:|------|
| Q1 | Allow v1.0-B to touch invoke_skill? | **No** | If yes: modifies dispatch path |
| Q2 | Allow shadow/audit-only mode? | **Yes** | If no: v1.0-B has nothing to do |
| Q3 | Allow hard-fail enforcement? | **No** | If yes: risky, contract not battle-tested |
| Q4 | Limit to 3-5 sample skills? | **Yes** | Prevents scope creep |
| Q5 | Allow standalone validator/wrapper? | **Yes** | No existing path modification |
| Q6 | Allow result_envelope modification? | **No** | v0.x envelope is stable |
| Q7 | Allow runtime_reports write? | **No** | Audit result goes to log, not reports |
| Q8 | Maintain production/broker/real_trade BLOCKED? | **Yes** | Non-negotiable |
| Q9 | Fail-closed on schema violation? | **N/A** | Not applicable in audit-only mode |
| Q10 | Allow hard enforcement after audit verified? | **No** | Requires separate v1.0-C gate |

---

## Proposed Sample Skills

If Q4 is approved, v1.0-B pilot targets:

| Skill | Domain | Risk | Reason |
|:--|:--|:--:|------|
| `SYSTEM.GET_SKILLOS_STATUS` | SYSTEM | R0_READ | Simplest deterministic GET pattern |
| `GOVERNANCE.GET_VERIFY_STATUS` | GOVERNANCE | R0_READ | Low-risk read-only |
| `RESEARCHDB.GET_SCHEMA` | RESEARCHDB | R0_READ | Typical data-layer read |
| `COCKPIT.GET_SKILLOS_STATUS` | COCKPIT | R0_READ | Cross-domain structural variety |
| `FACTOR.LIST_REGISTERED_FACTORS` | FACTOR | R0_READ | Domain-specific schema test |

Selection criteria:
- All R0_READ (minimum risk)
- All DETERMINISTIC semantic category
- Covers 5 different domains
- None have write_layers
- None touch result_envelope in non-trivial ways

---

## Proposed Deliverables if GO

| # | File | Type |
|:--:|------|------|
| B1 | `zmatrix/agent/skill_schema_validator.py` | New standalone validator |
| B2 | `scripts/skillos/audit_schema_compliance.py` | Audit runner |
| B3 | `tests/skillos/test_v1_0_b_shadow_audit.py` | Tests |
| B4 | `docs/skillos/Z_SKILLOS_V1_0_B_SHADOW_AUDIT_CLOSEOUT.md` | Closeout |

All 4 files are NEW. Zero existing files modified.

---

## Proposed Forbidden for v1.0-B

```
zmatrix/agent/skill_invocation.py          (do not modify)
zmatrix/agent/skill_result_envelope.py     (do not modify)
zmatrix/agent/skill_registry.py            (do not modify)
zmatrix/agent/skill_registry_loader.py     (do not modify)
zmatrix/agent/skill_domain_registry.py     (do not modify)
data/research_db/agent/registry/skill_registry.generated.json  (do not modify)
data/research_db/agent/registry/skill_contract_registry.json   (read-only)
runtime_reports/                           (do not write)
docs/cases/                                (parent branch)
production / broker / real_trade           (remain BLOCKED)
```

---

## Decision

**PENDING**

- [ ] GO: proceed with shadow/audit-only schema validation scaffold
- [ ] NO-GO: remain at Z_SKILLOS_V1_0_A_APPROVED, identify blocking gaps

---

## Next If GO

```
Phase: v1.0-B Shadow Schema Validation Scaffold
Task: Standalone validator + audit runner + tests
Boundary: 4 new files, zero existing file modifications
Mode: audit-only, no hard enforcement
```

## Next If NO-GO

```
Phase: Remain at Z_SKILLOS_V1_0_A_APPROVED
Action: Resolve blocking gaps, resubmit gate
```

---

**Branch**: `feature/skillos-v1-0-a-contract-registry-infra`  
**Base**: `d74df48`
