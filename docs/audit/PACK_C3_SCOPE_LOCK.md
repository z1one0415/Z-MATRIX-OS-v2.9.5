# Pack C.3 Scope Lock

## Allowed
- `docs/audit/PACK_C3_BLOCKING_RISK_FIX_PLAN.md`
- `docs/audit/MAJOR_AUDIT_PACK_C3_CLOSEOUT.md`
- `runtime_reports/audit/pack_c3_blocking_risk_fix_plan.json`
- `tests/audit/test_major_audit_pack_c3_fix_plan.py`
- `docs/audit/PACK_C3_SCOPE_LOCK.md`
- `tests/audit/test_pack_c3_scope_clean.py`

## Forbidden
- Agent Kernel docs/modules
- Research Cockpit docs
- Frontend Workbench
- Proposal Approval Center
- Skill Invocation Console
- Broker/Runtime/RealTrade
- Production enablement

## Violation Record
- C.3 commit contained Cockpit V2.1→V2.2 rename — REVERTED
- Scope contamination severity: LOW (1 file rename)
