"""Tests for V13.F5.5.4.1 Signal Materialization Inputs."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_4_1_batch1_batch2_signal_materialization")

def _l(n): return json.loads((D / n).read_text())

def test_audit_exists():
    assert (D / "v13_f5_5_4_1_signal_materialization_input_audit.json").exists()

def test_audit_pass():
    a = _l("v13_f5_5_4_1_signal_materialization_input_audit.json")
    assert a["status"] == "V13_F5_5_4_1_INPUT_AUDIT_PASS"

def test_pit_blocking():
    a = _l("v13_f5_5_4_1_signal_materialization_input_audit.json")
    assert a["materializable_factors"] == ["F04", "F10", "F11"]
    assert set(a["blocked_factors"]) == {"F14", "F15", "F16"}

def test_pit_reasons():
    a = _l("v13_f5_5_4_1_signal_materialization_input_audit.json")
    for fid in ["F14", "F15", "F16"]:
        assert a["pit_source_checks"][fid]["available"] is False
        assert "BLOCKED" in a["pit_source_checks"][fid]["reason"]

def test_price_based_pass():
    a = _l("v13_f5_5_4_1_signal_materialization_input_audit.json")
    for fid in ["F04", "F10", "F11"]:
        assert a["pit_source_checks"][fid]["available"] is True
