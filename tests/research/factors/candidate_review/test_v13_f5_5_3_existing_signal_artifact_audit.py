"""Tests for V13.F5.5.3 Existing Signal Artifact Audit."""
import json
from pathlib import Path

D = Path("research/factor_library/reviews/batch_003/f5_5_3_signal_score_restoration")


def _l(n):
    return json.loads((D / n).read_text())


def test_audit_exists():
    assert (D / "v13_f5_5_3_existing_signal_artifact_audit.json").exists()


def test_audit_status():
    a = _l("v13_f5_5_3_existing_signal_artifact_audit.json")
    assert a["pipeline_signature"] == "Z2-V13-F5-5-3-EXISTING-SIGNAL-ARTIFACT-AUDIT"
    assert a["status"] == "V13_F5_5_3_EXISTING_SIGNAL_ARTIFACT_AUDIT_COMPLETE"
    assert a["frozen_candidates_audited"] == 10


def test_data_source_restrictions():
    a = _l("v13_f5_5_3_existing_signal_artifact_audit.json")
    r = a["data_source_restrictions"]
    assert r["runtime_reports_read"] is False
    assert r["feature_store_read"] is False
    assert r["broker_read"] is False
    assert r["trading_read"] is False
    assert r["execution_read"] is False
    assert r["external_data_read"] is False


def test_no_signal_scores_anywhere():
    a = _l("v13_f5_5_3_existing_signal_artifact_audit.json")
    for r in a["factor_audit_results"]:
        assert r["signal_scores_csv_exists"] is False
        assert r["bucket_assignments_csv_exists"] is False


def test_batch3_have_manifests():
    a = _l("v13_f5_5_3_existing_signal_artifact_audit.json")
    batch3 = [r for r in a["factor_audit_results"]
              if r["factor_id"] in ["F21", "F24", "F30", "F31"]]
    for r in batch3:
        assert r["factor_directory_exists"] is True
        assert r["manifest_exists"] is True
        assert r["restoration_class"] == "REQUIRES_SIGNAL_SCORE_MATERIALIZATION"


def test_batch1_2_blocked():
    a = _l("v13_f5_5_3_existing_signal_artifact_audit.json")
    batch12 = [r for r in a["factor_audit_results"]
               if r["factor_id"] in ["F04", "F10", "F11", "F14", "F15", "F16"]]
    for r in batch12:
        assert r["factor_directory_exists"] is False
        assert r["restoration_class"] == "BLOCKED_NO_SOURCE"
