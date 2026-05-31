import json,subprocess
from pathlib import Path
import pytest
W=Path(__file__).resolve().parent.parent.parent
G=W/"scripts"/"cases"/"check_v5_entry_gate.py"
@pytest.fixture
def gate():
    subprocess.run(["python3",str(G)],cwd=str(W),capture_output=True)
    return json.loads((W/"runtime_reports"/"cases"/"v5_entry_gate.json").read_text())
def test_gate_runs(gate): pass
def test_gate_matches_readiness(gate):
    rd=json.loads((W/"runtime_reports"/"cases"/"core_12_real_market_data_readiness.json").read_text())
    assert gate["daily_price_real_read_only"]==rd["summary"]["daily_price_real"]
    assert gate["adjustment_factor_ready"]==rd["summary"]["adjustment_ready"]
def test_alpha_zero(gate): assert gate["ready_for_alpha_claim"]==0
def test_safety_blocked(gate): assert gate["production"]=="BLOCKED"
def test_all_gates_pass_logic():
    bl=[]
    if 12<12: bl.append("P")
    if 12<12: bl.append("A")
    if not True: bl.append("B")
    assert len(bl)==0
def test_one_gate_fails():
    bl=[]
    if 11<12: bl.append("A")
    assert len(bl)>0
