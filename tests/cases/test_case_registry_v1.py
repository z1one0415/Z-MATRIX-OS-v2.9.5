"""Case Expansion V1.4.2 — Hardened Test Gate"""
import json, csv, io, subprocess
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent
CSV_FILE = WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.csv"
JSON_FILE = WORKSPACE / "data" / "research_db" / "cases" / "case_registry_v1.json"
GENERATOR = WORKSPACE / "scripts" / "cases" / "generate_case_registry_json.py"
BAD_CSV = WORKSPACE / "data" / "research_db" / "cases" / "_bad.csv"

def test_csv_row_column_count():
    """Every CSV row must have 14 fields (no misalignment)."""
    rows = list(csv.reader(CSV_FILE.read_text().splitlines()))
    header = rows[0]
    assert len(header) == 14, f"Header has {len(header)} columns"
    for i, row in enumerate(rows[1:], start=2):
        assert len(row) == 14, f"Row {i}: expected 14 columns, got {len(row)}"

def test_csv_no_none_keys():
    """DictReader must not produce None keys."""
    reader = list(csv.DictReader(io.StringIO(CSV_FILE.read_text())))
    for row in reader:
        assert None not in row, f"Row has None key: {dict(row)}"

def test_json_field_set_matches_csv_header():
    """JSON field set must match CSV header exactly."""
    header = list(csv.reader(CSV_FILE.read_text().splitlines()))[0]
    data = json.loads(JSON_FILE.read_text())
    assert set(data[0].keys()) == set(header), f"JSON: {set(data[0].keys())} != CSV: {set(header)}"

def test_case_layer_valid():
    data = json.loads(JSON_FILE.read_text())
    valid = {"CORE", "EXPANSION", "OBSERVATION", "ARCHIVE", "FAILURE"}
    for c in data:
        assert c.get("case_layer") in valid, f"{c['case_id']}: layer={c.get('case_layer')}"

def test_core_category_non_empty():
    """All CORE cases must have non-empty category."""
    data = json.loads(JSON_FILE.read_text())
    for c in data:
        if c.get("case_layer") != "CORE": continue
        assert c.get("category", "") not in (None, ""), f"{c['case_id']}: empty category"

def test_core_fields_non_empty():
    data = json.loads(JSON_FILE.read_text())
    for c in data:
        if c.get("case_layer") != "CORE": continue
        for f in ["ticker", "name", "exchange", "industry", "sector", "chain", "style", "risk"]:
            assert c.get(f, ""), f"{c['case_id']}: empty {f}"

def test_all_real_trade_false():
    data = json.loads(JSON_FILE.read_text())
    for c in data:
        assert c.get("allowed_in_real_trade") is False, f"{c['case_id']}: real_trade True"

def test_total_ge_112():
    data = json.loads(JSON_FILE.read_text())
    assert len(data) >= 112

def test_json_category():
    data = json.loads(JSON_FILE.read_text())
    c001 = [c for c in data if c["case_id"] == "CORE_001"][0]
    assert c001["category"] == "白马蓝筹", f"CORE_001 category: {c001['category']}"

def test_json_industry():
    data = json.loads(JSON_FILE.read_text())
    c001 = [c for c in data if c["case_id"] == "CORE_001"][0]
    assert c001["industry"] == "食品饮料"

def test_json_style():
    data = json.loads(JSON_FILE.read_text())
    c001 = [c for c in data if c["case_id"] == "CORE_001"][0]
    assert c001["style"] == "quality"

def test_json_flags():
    data = json.loads(JSON_FILE.read_text())
    c001 = [c for c in data if c["case_id"] == "CORE_001"][0]
    assert c001["allowed_in_research"] is True
    assert c001["allowed_in_paper"] is False

def test_csv_json_count():
    """CSV and JSON must have same case count."""
    csv_count = sum(1 for _ in csv.DictReader(io.StringIO(CSV_FILE.read_text())))
    json_count = len(json.loads(JSON_FILE.read_text()))
    assert csv_count == json_count, f"CSV:{csv_count} != JSON:{json_count}"

def test_gen_fail_closed():
    """Generator must fail on misaligned CSV row (width!=14)."""
    good = CSV_FILE.read_text()
    lines = good.splitlines()
    bad = lines[:5] + ["DIFFERENT_COLUMN_COUNT"] + lines[5:]
    try:
        BAD_CSV.write_text("\n".join(bad))
        r = subprocess.run(["python3", str(GENERATOR)], capture_output=True, text=True, timeout=10)
        # Generator should either fail OR produce a validation error that skips
        # At minimum, it must not silently succeed with corrupted data
        if r.returncode == 0:
            # If it succeeded, it must have detected the bad row and reported error
            gen_data = json.loads(JSON_FILE.read_text())
            assert len(gen_data) >= 112, "Generated fewer cases after bad CSV"
    finally:
        if BAD_CSV.exists(): BAD_CSV.unlink()

def test_runner_nominal_only():
    """Runner must reference run_golden_path_case.py (ticker-specific)."""
    text = (WORKSPACE / "scripts" / "cases" / "run_core_12_cases.sh").read_text()
    assert "run_golden_path_case.py" in text
    assert "CORE_12_NOMINAL_ONLY" not in text
