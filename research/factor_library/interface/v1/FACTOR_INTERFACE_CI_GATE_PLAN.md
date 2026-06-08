# Factor Interface CI Gate Plan

**Status**: PLANNED | **Not yet enforced in CI pipeline**

## Gate Proposals

### Gate 1: Schema Validation
- Run `python3 -m json.tool` on all `*.json` files in `research/factor_library/interface/v1/schemas/`.
- Fail if any schema is invalid JSON.

### Gate 2: Alpha Block Check
- `grep -R '"alpha_claim_allowed"[[:space:]]*:[[:space:]]*true' research/factor_library/interface/v1 && exit 1`
- Fail if any artifact allows alpha claim.

### Gate 3: Production Block Check
- `grep -R '"production"[[:space:]]*:[[:space:]]*"ALLOWED"' research/factor_library/interface/v1 && exit 1`
- Fail if any artifact allows production.

### Gate 4: Scope Boundary Check
- `git diff --name-only | grep -E 'skillos|SkillOS|broker|trading|execution|production|orders|portfolio' && exit 1`
- Fail if PR modifies protected areas.

### Gate 5: Pre-Interface Artifact Check
- If any factor has `pre_interface_artifacts: true`, confirm it does NOT enter candidate review.
- Fail if pre-interface factor is in `ready_for_candidate_review`.

## Future State
- Gates should be enforced via GitHub Actions before any factor library PR merge.
- Gate scripts should be in `.github/workflows/factor_library_ci.yml`.
- This document serves as the specification for that workflow.
