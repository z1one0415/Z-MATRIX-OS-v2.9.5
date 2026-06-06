# Z-SkillOS v1.1-C Coverage Selection Policy

## Status

Z_SKILLOS_V1_1_C_COVERAGE_SELECTION_POLICY_READY

## Core Rule

All selected skill_ids must be registry-exact. No aspirational names. No silent substitution.

## Tier Priority

| Tier | Risk Level | Max % | Rationale |
|:--|:--|:--:|------|
| 1 | R0_READ | 60% | DETERMINISTIC, lowest drift risk |
| 2 | R1_ANNOTATE | 25% | STRUCTURED_DRAFT, moderate risk |
| 3 | R2_DRAFT | 15% | May include write/proposal, higher risk |

## Excluded Skills

| Category | Reason |
|:--|------|
| Narrative renderer | LLM output hash unstable |
| write_layers non-empty | Requires human review context |
| proposal_required=true | Cannot auto-validate |
| VERDICT/RUNTIME skills | Beyond R2_DRAFT boundary |
| Report/Narrative skills | Semantic drift too high |

## Domain Coverage Priority

Already covered (12): AUTOCASE, BMATRIX, CASEFORGE, COCKPIT, COUNCIL, DATAFORGE, DMATRIX, FACTOR, GOVERNANCE, MEMORY, PORTFOLIO, RESEARCHDB

Remaining domains: REPORT, REPORTING, SYSTEM, SYSTEM_VERIFY, WORKFLOW, ZC35, Z_G16_PHYSICAL

Priority: fill remaining domains first, then double up on existing.

## Hash Generation

Expected hashes computed via v1.0-C `skill_hashing.py` at build time. No manual hash values.

## Baseline Update

New baseline snapshot created alongside expanded cases. Old baseline preserved.

## CI Integration

After standalone verification, one line added to `verify_skillos_v1_1_ci_audit.sh`:

```bash
python3 scripts/skillos/audit_golden_regression.py
```

Already present — regression audit uses expanded cases automatically.
