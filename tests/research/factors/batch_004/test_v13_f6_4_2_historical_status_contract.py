"""Test V13.F6.4.2 Historical Status Contract."""
import json
from pathlib import Path
D = Path("research/factor_library/reviews/batch_004/f6_4_2_historical_status_preservation")
def _l(n): return json.loads((D / n).read_text())

def test_contract_exists():
    assert (D / "v13_f6_4_2_historical_status_contract.json").exists()

def test_rejected_preserved():
    c = _l("v13_f6_4_2_historical_status_contract.json")
    assert c["preserved_statuses"]["rejected"] == ["F02", "F03", "F05"]

def test_hypothesis_sidecar():
    c = _l("v13_f6_4_2_historical_status_contract.json")
    assert "F03R" in c["preserved_statuses"]["hypothesis_only_sidecar"]

def test_source_audit():
    c = _l("v13_f6_4_2_historical_status_contract.json")
    assert c["preserved_statuses"]["source_audit_completed"] == ["F17","F18","F19","F20"]

def test_no_demotion():
    c = _l("v13_f6_4_2_historical_status_contract.json")
    assert c["status_change_rule"] == "PROMOTE_ONLY: blocked→materialized allowed. REJECTED→RESERVED forbidden."
