# RC1 Tag Dry-Run Manifest

## Candidate Tag

| Field | Value |
|-------|-------|
| Proposed tag | **v4.0-rc1** |
| Tag type | annotated tag |
| Tag created | **FALSE** |
| Annotation message | "Z-MATRIX-OS v4.0-rc1: research-only release candidate" |

## Target

| Field | Value |
|-------|-------|
| Repo | z1one0415/Z-MATRIX-OS-v2.9.5 |
| Branch | v4.0-batch-0-final-hardgates-scope-lock |
| Commit | f8796f714740b5e8c76ab53d768888a8de87dfdd |
| Short SHA | f8796f7 |
| Commit URL | https://github.com/z1one0415/Z-MATRIX-OS-v2.9.5/commit/f8796f714740b5e8c76ab53d768888a8de87dfdd |

## Required Pre-Tag Conditions

| Condition | Status |
|------|:------:|
| RC1 Readiness Audit | ✅ PASS |
| Scorecard | ✅ 100/100 |
| Recommendation | ✅ RC1_READY_RECOMMENDED |
| GitHub Actions CI | ✅ PASS (run 26629922144) |
| Cloud evidence lock | ✅ PASS |
| Runtime reports tracked | ✅ FALSE |
| Production | ✅ BLOCKED |
| Broker/runtime | ✅ BLOCKED |
| Real trade | ✅ BLOCKED |

## Dry-Run Commands

**Do not execute yet:**

```bash
git tag -a v4.0-rc1 f8796f714740b5e8c76ab53d768888a8de87dfdd \
  -m "Z-MATRIX-OS v4.0-rc1: research-only release candidate"
git show v4.0-rc1
git push origin v4.0-rc1
```

## Decision

| Field | Value |
|-------|-------|
| Manual approval required | **TRUE** |
| Approved by | (pending human decision) |
| Approval date | (pending) |
