import json
from pathlib import Path
import pytest
W = Path(__file__).resolve().parent.parent.parent
@pytest.fixture
def packet():
    return json.loads((W/"runtime_reports/cases/v5_core12_real_return_packet.json").read_text())
def test_packet_status(packet):
    assert "CONFIRMED" in packet["status"]
def test_packet_12_cases(packet):
    assert packet["core_12_cases"] == 12
def test_packet_zero_alpha(packet):
    assert packet["predictive_alpha_claim_count"] == 0
def test_packet_zero_bs(packet):
    assert packet["buy_sell_instruction_count"] == 0
def test_packet_blocked(packet):
    assert packet["production"] == "BLOCKED"
def test_packet_horizons(packet):
    assert packet["horizons"] == ["T1","T5","T10","T20","T60"]
