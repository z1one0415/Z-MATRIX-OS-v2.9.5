# Z-SkillOS v1.0-A Readiness Approval Gate

## Decision

PENDING

---

## Current State

| 指标 | 值 |
|:--|:--|
| Registered skills | 104 |
| Concrete domains | 17 |
| Framework-only domains | 0 |
| Domain routers | 17/17 concrete |
| Skill contract registry | ❌ Does not exist |
| Input schema per skill | ❌ Not enforced |
| Output schema per skill | ❌ Not enforced |
| invoke_skill schema validation | ❌ Not implemented |
| Result envelope | `skill_result_envelope.py` exists (v0.x baseline) |
| Registry validation | `validate_skill_registry.py` validates ids/domains/risks only |
| max_risk | R2_DRAFT |
| production | BLOCKED |
| broker_runtime | BLOCKED |
| real_trade | BLOCKED |

### Existing Artifacts (v0.x baseline)

| File | Role |
|:--|:--|
| `zmatrix/agent/skill_registry.py` | Skill metadata loader |
| `zmatrix/agent/skill_registry_loader.py` | Registry builder |
| `zmatrix/agent/skill_invocation.py` | Skill dispatch router |
| `zmatrix/agent/skill_result_envelope.py` | Output envelope structure |
| `zmatrix/agent/skill_domain_registry.py` | Domain→path mapping |
| `data/research_db/agent/registry/skill_registry.generated.json` | 104 skill entries |
| `scripts/skillos/validate_skill_registry.py` | id/domain/risk validator |
| `scripts/skillos/build_skill_registry.py` | Registry builder |
| `scripts/skillos/scan_skill_candidates.py` | Candidate scanner |

### What v0.x Has

- Skill discovery and registration ✅
- Domain routing ✅
- Risk level classification ✅
- Basic invocation dispatch ✅
- Result envelope (output wrapping) ✅
- Forbidden scan ✅
- Full-system verify ✅

### What v0.x Does NOT Have

- Per-skill input schema definition
- Per-skill output schema definition
- Schema validation on invocation
- `input_hash` computation
- `output_hash` computation
- `evidence_refs` tracking
- `data_snapshot_id` binding
- `safety_envelope` per invocation
- `skill_contract_registry.json`

---

## Readiness Evidence

### v1.0 Readiness Document Exists

`docs/skillos/Z_SKILLOS_V1_0_DETERMINISTIC_CONTRACT_READINESS.md` defines:
- Contract registry target schema
- Input/output schema format
- Semantic categories (DETERMINISTIC / STRUCTURED_DRAFT / NARRATIVE_RENDERER)
- Invocation validation rules
- Data snapshot binding requirements
- Future `verify_z_skillos_v1_contract.sh` requirements
- Phase decomposition (v1.0 → v1.4)

### v0.x Baseline is Stable

- Full-system verify: vFS.11 PASS
- 214 agent + 1261 research_db tests PASS
- 12 verify scripts all operational
- Gate flattening complete
- Forbidden scan fs.24 stable

### Gap Analysis

| What v1.0-A Needs | Status |
|:--|:--:|
| Contract registry schema | ✅ Defined in readiness doc |
| Input/output schema format | ✅ Defined in readiness doc |
| Existing registry data (104 skills) | ✅ Available |
| `invoke_skill` entry point | ✅ Exists, needs enforcement layer |
| `skill_result_envelope` | ✅ Exists, needs extension |
| Semantic category mapping | ⚠️ Must be derived from domain+risk |
| `input_hash`/`output_hash` function | ❌ Not yet built |
| Schema validation function | ❌ Not yet built |

---

## Proposed v1.0-A Scope

v1.0-A is the FIRST implementation batch of v1.0. It does NOT deliver the full v1.0 contract. It delivers the contract registry infrastructure — the foundation that all subsequent batches build on.

### Deliverables

| # | Item | Type |
|:--:|------|------|
| A1 | `skill_contract_registry.json` | data file |
| A2 | `build_skill_contract_registry.py` | builder script |
| A3 | `validate_skill_contract_registry.py` | validator script |
| A4 | `test_v1_0_a_contract_registry.py` | test file |
| A5 | `Z_SKILLOS_V1_0_A_IMPLEMENTATION_CLOSEOUT.md` | closeout doc |
| A6 | `skill_contract_registry` loader in `zmatrix/agent/` | loader module |

### v1.0-A Contract Registry Content

Every entry binds:

```json
{
  "skill_id": "DOMAIN.SKILL_NAME",
  "skill_version": "1.0.0",
  "domain": "DOMAIN",
  "risk_level": "R0_READ | R1_ANNOTATE | R2_DRAFT",
  "semantic_category": "DETERMINISTIC | STRUCTURED_DRAFT | NARRATIVE_RENDERER",
  "input_schema": {},
  "output_schema": {},
  "status": "ACTIVE",
  "write_layers": [],
  "requires_human_review": true,
  "proposal_required": true
}
```

### What v1.0-A Does NOT Include

- `invoke_skill` schema enforcement (v1.0-B)
- `input_hash` / `output_hash` computation (v1.0-C)
- `evidence_refs` tracking (v1.0-D)
- `data_snapshot_id` binding (v1.4)
- Golden output regression (v1.1)
- Semantic drift regression (v1.2)
- Skill result ledger (v1.3)

---

## Allowed Files for v1.0-A if GO

### New files

```
data/research_db/agent/registry/skill_contract_registry.json
scripts/skillos/build_skill_contract_registry.py
scripts/skillos/validate_skill_contract_registry.py
tests/skillos/test_v1_0_a_contract_registry.py
docs/skillos/Z_SKILLOS_V1_0_A_IMPLEMENTATION_CLOSEOUT.md
zmatrix/agent/skill_contract_registry.py  (loader)
```

### Modified files (read-only access)

```
(None — v1.0-A does NOT modify existing runtime paths)
```

---

## Forbidden Files

```
data/research_db/agent/registry/skill_registry.generated.json  (do not modify)
zmatrix/agent/skill_invocation.py                               (do not modify)
zmatrix/agent/skill_result_envelope.py                          (do not modify)
zmatrix/agent/skill_domain_registry.py                          (do not modify)
scripts/skillos/validate_skill_registry.py                      (do not modify)
scripts/skillos/build_skill_registry.py                         (do not modify)
runtime_reports/                                                (do not create/modify)
docs/cases/                                                     (parent branch docs)
docs/skillos/Z_SKILLOS_V1_0_DETERMINISTIC_CONTRACT_READINESS.md (already approved)
```

---

## Safety Boundary

| Gate | Status |
|:--|:--|
| production | BLOCKED |
| broker_runtime | BLOCKED |
| real_trade | BLOCKED |
| alpha claim | BLOCKED |
| tag | DO NOT TAG |
| parent branch advancement | DO NOT ADVANCE |
| V12.2 / V12.3 | PARENT DOMAIN, READ-ONLY |
| max_risk | R2_DRAFT (unchanged) |
| existing verify chain | DO NOT BREAK |
| existing tests (214 + 1261) | MUST KEEP PASSING |
| existing forbidden scan | MUST KEEP PASSING |

---

## Next If GO

```
Phase: v1.0-A Implementation
Task: Build skill_contract_registry infrastructure
Boundary: Only 6 new files, zero existing file modifications
Deadline: v1.0-A closeout verified and committed
```

### GO Criteria (all must be true)

- [ ] Human explicitly says "GO" or equivalent explicit approval
- [ ] Parent branch verification chain still passes
- [ ] Working tree clean before start

---

## Next If NO-GO

```
Phase: Remain at Z_SKILLOS_V0_RECONCILE_CLOSED
Action: Wait for readiness gap resolution
No new files created
No registry built
```

---

## Decision

**PENDING** — awaiting explicit human GO / NO-GO

- [ ] GO: proceed with v1.0-A contract registry infrastructure
- [ ] NO-GO: freeze, identify blocking gaps

---

**Status**: `Z_SKILLOS_V1_0_A_READINESS_APPROVAL_GATE_READY`

**Branch**: `postmerge/skillos-v0-baseline-freeze` @ `952c115`
