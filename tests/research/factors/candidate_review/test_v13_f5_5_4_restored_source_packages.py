"""Tests for V13.F5.5.4 Restored Source Packages."""
import json
from pathlib import Path

SOURCES = Path("research/factor_library/sources")
FACTORS = ["F04", "F10", "F11", "F14", "F15", "F16"]
REQUIRED_FILES = ["factor_manifest.json", "formula_contract.json",
                  "signal_materialization_requirements.json", "source_provenance.json"]
FORBIDDEN_FILES = ["signal_scores.csv", "bucket_assignments.csv"]


def test_all_directories_exist():
    for fid in FACTORS:
        assert (SOURCES / fid).exists()


def test_all_required_files():
    for fid in FACTORS:
        for fname in REQUIRED_FILES:
            assert (SOURCES / fid / fname).exists(), f"Missing {fid}/{fname}"


def test_no_forbidden_files():
    for fid in FACTORS:
        for fname in FORBIDDEN_FILES:
            assert not (SOURCES / fid / fname).exists(), f"Forbidden {fid}/{fname}"


def test_manifests_valid():
    for fid in FACTORS:
        m = json.loads((SOURCES / fid / "factor_manifest.json").read_text())
        assert m["factor_id"] == fid
        assert m["factor_status"] == "RESTORED_FOR_SIGNAL_MATERIALIZATION"
        assert m["promotion_allowed"] is False
        assert m["alpha_claim_allowed"] is False
        assert m["production"] == "BLOCKED"


def test_formula_contracts_valid():
    for fid in FACTORS:
        f = json.loads((SOURCES / fid / "formula_contract.json").read_text())
        assert f["factor_id"] == fid
        assert f["output_role"] == "FACTOR_SIGNAL_ONLY"
        assert "forward_return" in f["forbidden_outputs"]
        assert "trade_signal" in f["forbidden_outputs"]


def test_materialization_requirements():
    for fid in FACTORS:
        r = json.loads((SOURCES / fid / "signal_materialization_requirements.json").read_text())
        assert r["factor_id"] == fid
        assert r["constraints"]["signal_role"] == "FACTOR_SIGNAL_ONLY"
        assert r["constraints"]["no_forward_return_input"] is True


def test_source_provenance():
    for fid in FACTORS:
        p = json.loads((SOURCES / fid / "source_provenance.json").read_text())
        assert p["factor_id"] == fid
        assert p["no_signal_scores_included"] is True
        assert p["no_bucket_assignments_included"] is True
