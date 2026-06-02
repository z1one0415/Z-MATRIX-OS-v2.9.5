import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_sem_audit_pass():
    d=json.loads((W/"runtime_reports/cases/v11_watchlist_semantic_audit.json").read_text())
    assert d["status"]=="V11_WATCHLIST_SEMANTIC_AUDIT_PASS"
    assert d["semantic_mismatch_count"]==0
    assert d["semantic_missing_count"]==0
    assert d["raw_monotonic_leaks"]==[]
