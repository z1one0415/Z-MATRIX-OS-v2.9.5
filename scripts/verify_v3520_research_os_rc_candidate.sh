#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v3.5.20 Research OS RC Final Closeout Verification ═══"

PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines 2>&1 | tail -1

# Module smoke tests
PYTHONPATH=. python3 -c "
from zmatrix.research_os_rc.safety_gate_auditor import audit_safety_gates
from zmatrix.research_os_rc.evidence_chain_auditor import audit_evidence_chain
from zmatrix.research_os_rc.rc_verdict_builder import build_rc_verdict
from zmatrix.research_os_rc.policy import validate_research_os_rc_report, collect_policy_violations
print('  ✅ all modules importable')
"

PYTHONPATH=. python3 -c "
from zmatrix.research_os_rc.policy import validate_research_os_rc_report
r = {'version_ceiling':'v3.5.20','next_version_allowed':False,'production_strategy_modified':False,'real_trade_allowed':False,'broker_order_allowed':False,'safety':{'real_trade_allowed':False}}
e = validate_research_os_rc_report(r)
assert e == [], f'unexpected errors: {e}'
print('  ✅ policy validation')
"

PYTHONPATH=. python3 -c "
from zmatrix.research_os_rc.policy import collect_policy_violations
v = collect_policy_violations(safety_audit={'safety_gate_status':'FAIL','violations':[{'report':'test','field':'real_trade_allowed'}]},namespace_audit={'namespace_status':'PASS'},evidence_audit={'evidence_chain_status':'READY'})
assert len(v)>0, 'should detect safety violations'
print('  ✅ policy violation detection')
"

# P0-1 FIX: v3.6 grep — no anti-filter
echo "  Checking v3.6 references..."
if grep -r "v3\.6" zmatrix tests --exclude-dir=__pycache__ 2>/dev/null; then
    echo "❌ v3.6 reference detected. Version ceiling is v3.5.20."
    exit 2
fi
echo "  ✅ Zero v3.6 references"

git diff --check
if git ls-files runtime_reports | grep .; then echo "❌ runtime_reports must not be tracked"; exit 1; fi
echo "  ✅ runtime_reports not tracked"

echo "═══ v3.5.20 Research OS RC Final Closeout PASS ═══"
