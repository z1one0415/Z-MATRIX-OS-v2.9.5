# Golden Path Hash Stability Fix Note

## Issue

Golden Path audit hash originally included dynamic timestamps (`created_at`, `run_at`, ledger entry timestamps), causing non-reproducible hashes across audit runs.

## Fix

Changed `golden_path_runner.py` hash computation to cover only stable research data:

```python
hash_keys = ["factor", "outcome", "attribution", "replay", "council"]
stable_data = {k: stages[k] for k in hash_keys if k in stages}
h = hashlib.sha256(json.dumps(stable_data, sort_keys=True, default=str).encode()).hexdigest()[:16]
```

## Boundaries

- ✅ Does NOT change research results
- ✅ Does NOT change report content
- ✅ Does NOT change any trade/execution status
- ✅ Does NOT add new capability modules
- ⚠️ Excludes idea/decision/memory/run_at from hash — these should be re-evaluated for inclusion with stable fields only

## Verification

- 3x dry-run: hash `ff772079f3923586` stable across all runs
- Factor/outcome/attribution changes → hash changes (verified)
- Timestamp-only changes → hash unchanged (verified)

## Registered

Audit-discovered code change. Registered in Major Audit Pack A closeout.
