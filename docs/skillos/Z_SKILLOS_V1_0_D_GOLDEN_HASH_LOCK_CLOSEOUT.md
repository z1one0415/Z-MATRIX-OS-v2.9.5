# Z-SkillOS v1.0-D Golden Hash Policy + Golden I/O Lock — Closeout

## Status

Z_SKILLOS_V1_0_D_GOLDEN_HASH_LOCK_COMPLETE

## Scope

Golden hash policy + golden I/O lock only.

## Delivered

| # | File | Role |
|:--:|------|------|
| D1 | `zmatrix/agent/skill_hash_policy.py` | Static hash policy manifest |
| D2 | `data/.../golden/skillos_v1_0_d_golden_cases.json` | 4 golden cases with expected hashes |
| D3 | `scripts/skillos/audit_golden_hash_lock.py` | Golden hash lock auditor |
| D4 | `tests/skillos/test_v1_0_d_golden_hash_lock.py` | 14 tests |
| D5 | `docs/skillos/Z_SKILLOS_V1_0_D_GOLDEN_HASH_LOCK_CLOSEOUT.md` | Closeout |

## Hash Policy

| Field | Value |
|:--|:--|
| hash_algorithm | SHA-256 |
| canonical_json | sort_keys=True, separators=[",", ":"], ensure_ascii=False |
| output_hash_excluded_fields | ["narrative", "input_hash", "output_hash"] |
| dynamic_fields | None |

## v1.0-D.1 Policy Evolution

v1.0-E required schema-complete output payloads containing `input_hash` and `output_hash`. These hash fields are now treated as volatile/circular and excluded from output hash computation. See `Z_SKILLOS_V1_0_D_1_HASH_FIELD_EXCLUSION_POLICY_PATCH.md` for full rationale. Golden expected hashes are unchanged because existing golden output payloads do not include hash fields.

## Golden Audit Results

| Check | Result |
|:--|:--|
| input_hash_match | 4/4 |
| output_hash_match | 4/4 |
| narrative_change_same_hash | yes |
| non_narrative_change_diff_hash | yes |

## Explicit Non-Scope

No invoke_skill / hard enforcement / schema enforcement / result_envelope / runtime_reports / ledger / parent branch advancement / production / broker / real_trade.

## Verification

compileall PASS, all existing tests PASS (214 agent + 1261 research_db).

## Next

v1.0-E Hash-aware Shadow Audit.
