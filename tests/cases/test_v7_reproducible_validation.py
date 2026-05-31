"""Test V7 reproducible calculation chain."""
import json, csv, io
from pathlib import Path
import pytest

W = Path(__file__).resolve().parent.parent.parent
PROC = W / "data" / "research_db" / "market_data" / "processed"
CASES = W / "runtime_reports" / "cases"

@pytest.fixture(scope="module")
def prices():
    p = {}
    for row in csv.DictReader(io.StringIO((PROC / "core12_daily_price_bar.csv").read_text())):
        t, d = row["ticker"], row["trade_date"]
        p.setdefault(t, {})[d] = float(row["close"])
    return p

@pytest.fixture(scope="module")
def benchmark():
    b = {}
    for row in csv.DictReader(io.StringIO((PROC / "benchmark_csi300_price.csv").read_text())):
        b[row["trade_date"]] = float(row["close"])
    return b

@pytest.fixture(scope="module")
def labels_json():
    return json.loads((CASES / "v7_forward_return_labels.json").read_text())

@pytest.fixture(scope="module")
def metrics_json():
    return json.loads((CASES / "v7_exploratory_factor_metrics.json").read_text())

def test_forward_label_script_not_empty():
    text = (W / "scripts" / "cases" / "build_v7_forward_return_labels.py").read_text()
    assert len(text) > 500, "Label builder is empty"
    assert "core12_daily_price_bar.csv" in text
    assert "json.dumps" in text

def test_metrics_script_not_empty():
    text = (W / "scripts" / "cases" / "calculate_v7_exploratory_factor_metrics.py").read_text()
    assert len(text) > 500, "Metrics script is empty"
    assert "pearson" in text.lower() or "spearman" in text

def test_label_formula_reproducible(prices, benchmark, labels_json):
    td = sorted(benchmark.keys())
    for lb in labels_json["labels"][:50]:  # Check first 50
        ec = prices[lb["ticker"]][lb["as_of_date"]]
        xc = prices[lb["ticker"]][lb["exit_date"]]
        expected_fsr = xc / ec - 1
        assert abs(lb["future_stock_return"] - expected_fsr) < 1e-8

def test_label_exit_after_entry(labels_json):
    for lb in labels_json["labels"]:
        assert lb["exit_date"] > lb["as_of_date"]

def test_label_not_factor_input(labels_json):
    for lb in labels_json["labels"]:
        assert lb["used_as_factor_input"] is False

def test_cross_section_size(metrics_json):
    for m in metrics_json["metrics"]:
        assert m["cross_section_size"] == 12, f"{m['factor_id']}×{m['horizon']}: cs={m['cross_section_size']}"

def test_alpha_not_validated(metrics_json):
    assert metrics_json["alpha_validated"] is False
    for m in metrics_json["metrics"]:
        assert m["alpha_validated"] is False
        assert m["ready_for_alpha_claim"] is False

def test_t60_insufficient():
    ad = json.loads((CASES / "v7_sample_adequacy_audit.json").read_text())
    assert ad["horizon_status"]["T60"] == "INSUFFICIENT"

def test_coverage_audit_written():
    cov = json.loads((CASES / "v7_label_coverage_audit.json").read_text())
    for hn in ["T1", "T5", "T10", "T20"]:
        assert cov["coverage_by_horizon"][hn]["valid_dates"] > 0

def test_v8_gate():
    g = json.loads((CASES / "v8_expanded_sample_entry_gate.json").read_text())
    assert g["ready_for_alpha_claim"] is False
    assert g["production"] == "BLOCKED"
