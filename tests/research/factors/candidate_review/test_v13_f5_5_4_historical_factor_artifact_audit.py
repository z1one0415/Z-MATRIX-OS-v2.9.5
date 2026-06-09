"""Tests for V13.F5.5.4 Historical Factor Artifact Audit."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_4_signal_source_recovery")


def _l(n):
    return json.loads((D / n).read_text())


def test_audit_exists():
    assert (D / "v13_f5_5_4_historical_factor_artifact_audit.json").exists()


def test_audit_complete():
    a = _l("v13_f5_5_4_historical_factor_artifact_audit.json")
    assert a["status"] == "V13_F5_5_4_HISTORICAL_ARTIFACT_AUDIT_COMPLETE"
    assert a["factors_audited"] == 6
    assert a["restorable_count"] == 6
    assert a["blocked_count"] == 0


def test_all_safe_to_restore():
    a = _l("v13_f5_5_4_historical_factor_artifact_audit.json")
    for r in a["factor_results"]:
        assert r["safe_to_restore"] is True
        assert r["in_unified_candidate_registry"] is True
        assert r["blocked_reasons"] == []


def test_data_restrictions():
    a = _l("v13_f5_5_4_historical_factor_artifact_audit.json")
    assert a["data_source_restrictions"]["runtime_reports_read"] is False
    assert a["data_source_restrictions"]["broker_read"] is False
    assert a["data_source_restrictions"]["execution_read"] is False
