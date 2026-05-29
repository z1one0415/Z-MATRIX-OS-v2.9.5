# Post-RC1 Release Integrity Audit Scope Lock

## Baseline

| Field | Value |
|-------|-------|
| Audit target | v4.0-rc1 |
| Tag target commit | f8796f714740b5e8c76ab53d768888a8de87dfdd |
| Docs commit | 5f3f932 |
| Branch | v4.0-batch-0-final-hardgates-scope-lock |
| Production | BLOCKED |
| Broker/runtime | BLOCKED |
| Real trade | BLOCKED |

## Allowed

1. ✅ Verify local and remote tag existence
2. ✅ Verify tag points to target commit
3. ✅ Verify release docs consistency
4. ✅ Verify evidence lock integrity
5. ✅ Re-scan safety gates (no production/runtime/broker/real trade)
6. ✅ Audit GitHub Release state (tag page vs formal release)
7. ✅ Produce post-RC1 integrity audit report

## Forbidden

1. ❌ Modify strategy code
2. ❌ Modify classifier production chain
3. ❌ Enable runtime
4. ❌ Enable broker
5. ❌ Execute real trade
6. ❌ Publish official GitHub Release
7. ❌ Merge to main/master
8. ❌ Create v4.0 stable tag
9. ❌ Modify tag

## Phases

| Phase | Item |
|:-----:|------|
| PRI-0 | Audit Scope Lock |
| PRI-1 | Tag Integrity Verification |
| PRI-2 | Release Docs Consistency Audit |
| PRI-3 | Safety Gate Re-Scan |
| PRI-4 | Remote / GitHub Release State Audit |
| PRI-5 | Post-RC1 Integrity Scorecard |
| PRI-6 | Closeout Report |
