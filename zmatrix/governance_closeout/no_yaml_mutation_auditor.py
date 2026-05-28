from __future__ import annotations
import subprocess
from zmatrix.governance_closeout.schema import DEFAULT_GOVERNANCE_SAFETY

SENSITIVE_PATTERNS = [".yaml",".yml","params","parameter","threshold","production","b_matrix","r_matrix","d_matrix","brd","pipeline"]

def _git_changed(b="6d5f624",h="HEAD"):
    try: return [x.strip() for x in subprocess.check_output(["git","diff","--name-only",b,h],text=True).splitlines() if x.strip()]
    except: return []

def audit_no_yaml_mutation(*, base_ref="6d5f624", head_ref="HEAD") -> dict:
    ch = _git_changed(base_ref,head_ref)
    sen = []
    for f in ch:
        lo = f.lower()
        if any(p in lo for p in SENSITIVE_PATTERNS):
            if lo.endswith((".yaml",".yml")) or "params" in lo or "threshold" in lo or "production" in lo: sen.append(f)
    return {"audit_version":"V357_NO_YAML_MUTATION_AUDIT_V10","base_ref":base_ref,"head_ref":head_ref,"changed_files":ch,"sensitive_changed_files":sen,"yaml_mutation_detected":bool(sen),"audit_status":"PASS" if not sen else "BLOCKED_YAML_OR_PARAMETER_MUTATION","production_yaml_write_allowed":False,"production_parameter_write_allowed":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_GOVERNANCE_SAFETY)}
