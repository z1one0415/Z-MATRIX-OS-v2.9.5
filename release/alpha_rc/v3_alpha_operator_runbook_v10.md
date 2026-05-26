# v3.0-alpha Operator Runbook

## Allowed

- Run verification scripts.
- Run dry-run rehearsal.
- Review generated reports.
- Inspect EventStore sample chain.
- Review Approval records.

## Forbidden

- Do not connect broker.
- Do not enable runtime.
- Do not write Hermes memory.
- Do not write Z9.
- Do not auto-calibrate.
- Do not inject Prompt.
- Do not place real orders.

## Recommended command

bash scripts/verify_v3_alpha_rc_candidate.sh
