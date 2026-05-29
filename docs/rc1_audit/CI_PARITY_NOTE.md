# CI Parity Note — RA-2

**Date**: 2026-05-29  
**Audit Stage**: RA-2 — CI / Cloud Verification Parity

## Status

GitHub Actions CI workflow created at `.github/workflows/v40-rc1-audit.yml`.

## Combined Status

Combined status will populate after first push to branch `v4.0-batch-0-final-hardgates-scope-lock`.

## Workflow Steps

1. **Checkout** — actions/checkout@v4
2. **Set up Python** — Python 3.11 via actions/setup-python@v5
3. **Install test dependencies** — pytest
4. **Compile** — `python -m compileall zmatrix tests scripts`
5. **Hardening-B** — `scripts/verify_v40_hardening_b.sh`
6. **Hardening-C2** — `scripts/verify_v40_hardening_c2_all.sh`
7. **Hardening-C3** — `scripts/verify_v40_hardening_c3_all.sh`
8. **Full tests** — `PYTHONPATH=. python -m pytest -q tests/`

## Triggers

- **Push** to `v4.0-batch-0-final-hardgates-scope-lock`
- **Manual** via `workflow_dispatch`

## Local Verification

Local parity tests pass in `tests/rc1_audit/test_github_actions_ci.py` (6 tests):

- `test_ci_workflow_exists`
- `test_ci_has_hardening_b`
- `test_ci_has_hardening_c2`
- `test_ci_has_hardening_c3`
- `test_ci_has_full_tests`
- `test_ci_uses_branch`
