"""Tests for V13.F5.5.3.1 Signal Materialization Inputs."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_3_1_signal_materialization")


def _l(n):
    return json.loads((D / n).read_text())


def test_audit_exists():
    assert (D / "v13_f5_5_3_1_signal_materialization_input_audit.json").exists()


def test_audit_pass():
    a = _l("v13_f5_5_3_1_signal_materialization_input_audit.json")
    assert a["status"] == "V13_F5_5_3_1_INPUT_AUDIT_PASS"
    assert a["violation_count"] == 0


def test_inputs():
    a = _l("v13_f5_5_3_1_signal_materialization_input_audit.json")
    assert a["checks"]["label_ticker_count"] == 5
    assert a["checks"]["price_bars_readable"] is True
    assert a["checks"]["pre_rebalance_history_available"] is True
    assert a["checks"]["forward_return_not_used_for_signal"] is True


def test_manifests():
    a = _l("v13_f5_5_3_1_signal_materialization_input_audit.json")
    for f in ["F21", "F24", "F30", "F31"]:
        assert a["checks"][f"{f}_manifest_exists"] is True
        assert a["checks"][f"{f}_formula_ref_exists"] is True
