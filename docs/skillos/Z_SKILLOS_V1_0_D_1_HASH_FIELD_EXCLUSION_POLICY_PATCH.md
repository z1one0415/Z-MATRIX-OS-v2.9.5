# Z-SkillOS v1.0-D.1 Hash Field Exclusion Policy Patch

## Status

Z_SKILLOS_V1_0_D_1_HASH_FIELD_EXCLUSION_POLICY_PATCH_COMPLETE

## Reason

v1.0-E `skill_hash_aware_auditor.py` constructs schema-complete output payloads by inserting computed `input_hash` and `output_hash` into the output payload before schema validation. If `compute_output_hash` includes `input_hash` and `output_hash` in its hash computation, the hash becomes circular (hash of payload that contains the hash).

## Policy Change

```
OUTPUT_HASH_EXCLUDED_FIELDS
  from: ["narrative"]
  to:   ["narrative", "input_hash", "output_hash"]
```

## Affected Files

| File | Change |
|:--|:--|
| `skill_hash_policy.py` | `OUTPUT_HASH_EXCLUDED_FIELDS` extended |
| `skill_hashing.py` | volatile set extended to match policy |
| `skillos_v1_0_d_golden_cases.json` | `excluded_output_fields` metadata updated |
| `Z_SKILLOS_V1_0_D_GOLDEN_HASH_LOCK_CLOSEOUT.md` | policy table updated |
| `Z_SKILLOS_V1_0_E_HASH_AWARE_SHADOW_AUDIT_CLOSEOUT.md` | boundary corrected |

## Golden Hash Stability

Golden expected hashes are unchanged because existing golden output payloads do not include `input_hash` or `output_hash` fields. The exclusion only affects hash computation of payloads that contain those fields.

## Scope

Hash field exclusion policy only.

## Explicit Non-Scope

- No invoke_skill integration
- No hard enforcement
- No result_envelope modification
- No runtime_reports
- No ledger
- No parent branch advancement
- No production / broker / real_trade
