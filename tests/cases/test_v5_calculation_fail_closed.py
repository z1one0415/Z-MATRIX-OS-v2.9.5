"""V5.1: Test fail-closed behavior and formula correctness."""
import json, csv, io
from pathlib import Path
import pytest

W = Path(__file__).resolve().parent.parent.parent
PROC = W / "data" / "research_db" / "market_data" / "processed"
CASES = W / "runtime_reports" / "cases"

# Load data for ground-truth checks
@pytest.fixture(scope="module")
def prices():
    data = {}
    for row in csv.DictReader(io.StringIO((PROC / "core12_daily_price_bar.csv").read_text())):
        data.setdefault(row["ticker"], {})[row["trade_date"]] = float(row["close"])
    return data

@pytest.fixture(scope="module")
def bench():
    data = {}
    for row in csv.DictReader(io.StringIO((PROC / "benchmark_csi300_price.csv").read_text())):
        data[row["trade_date"]] = float(row["close"])
    return data

@pytest.fixture(scope="module")
def trade_dates():
    return sorted({row["trade_date"] for row in csv.DictReader(io.StringIO((PROC / "core12_daily_price_bar.csv").read_text()))})

ENTRY_DATE = "20240102"
HORIZONS = {"T1": 1, "T5": 5, "T10": 10, "T20": 20, "T60": 60}

def fwd(start, n, td):
    idx = td.index(start) if start in td else -1
    return td[idx + n] if idx >= 0 and idx + n < len(td) else None

@pytest.fixture(scope="module")
def stock_json():
    return json.loads((CASES / "core_12_real_returns.json").read_text())

@pytest.fixture(scope="module")
def bench_json():
    return json.loads((CASES / "csi300_benchmark_returns.json").read_text())

@pytest.fixture(scope="module")
def rel_json():
    return json.loads((CASES / "core_12_benchmark_relative_returns.json").read_text())

# ═══ Entry Date ═══
def test_fixed_entry_date(stock_json, bench_json):
    assert stock_json["entry_date"] == "2024-01-02"
    assert bench_json["entry_date"] == "2024-01-02"

# ═══ Date Format ═══
def test_all_dates_yyyy_mm_dd(stock_json):
    for c in stock_json["cases"]:
        assert "-" in c["entry_date"], f"{c['case_id']}: date format"
        for hk, r in c["returns"].items():
            if r["exit_date"]:
                assert "-" in r["exit_date"], f"{c['case_id']} {hk}: {r['exit_date']}"

# ═══ Trading Day Forward ═══
def test_exit_dates_are_forward_trading_days(stock_json, trade_dates):
    for c in stock_json["cases"]:
        for hk, r in c["returns"].items():
            if r["truth_status"] == "REAL_READ_ONLY":
                n = HORIZONS[hk]
                expected = fwd(ENTRY_DATE, n, trade_dates)
                expected_norm = f"{expected[:4]}-{expected[4:6]}-{expected[6:]}" if expected else None
                assert r["exit_date"] == expected_norm, f"{c['case_id']} {hk}: got {r['exit_date']} expected {expected_norm}"

# ═══ Return Formula ═══
def test_return_formula_correct(stock_json, prices):
    for c in stock_json["cases"]:
        ticker = c["ticker"]
        ps = prices.get(ticker, {})
        for hk, r in c["returns"].items():
            if r["truth_status"] == "REAL_READ_ONLY":
                expected = ps[r["exit_date"].replace("-", "")] / ps[ENTRY_DATE] - 1
                assert abs(round(r["return"], 10) - round(expected, 10)) < 1e-8, f"{c['case_id']} {hk}: {r['return']} vs {expected}"

# ═══ Benchmark Formula ═══
def test_benchmark_formula_correct(bench_json, bench, trade_dates):
    for hk, r in bench_json["returns"].items():
        if r["truth_status"] == "REAL_READ_ONLY":
            n = HORIZONS[hk]
            fd = fwd(ENTRY_DATE, n, trade_dates)
            expected = bench[fd] / bench[ENTRY_DATE] - 1
            assert abs(round(r["return"], 10) - round(expected, 10)) < 1e-8, f"{hk}: {r['return']} vs {expected}"

# ═══ Date Alignment ═══
def test_stock_benchmark_exit_dates_aligned(stock_json, bench_json):
    for c in stock_json["cases"]:
        for hk in bench_json["horizons"]:
            se = c["returns"][hk].get("exit_date")
            be = bench_json["returns"][hk].get("exit_date")
            assert se == be, f"{c['case_id']} {hk}: stock {se} vs bench {be}"

# ═══ Relative Return Formula ═══
def test_relative_return_formula(rel_json):
    for c in rel_json["cases"]:
        for hk in rel_json["horizons"]:
            r = c["relative_returns"][hk]
            if r["truth_status"] == "REAL_READ_ONLY":
                expected = r["stock_return"] - r["benchmark_return"]
                assert abs(r["benchmark_relative_return"] - expected) < 1e-12, f"{c['case_id']} {hk}"

# ═══ Date Aligned Flag ═══
def test_date_aligned_flag(rel_json):
    for c in rel_json["cases"]:
        for hk, r in c["relative_returns"].items():
            assert r["date_aligned"] is True, f"{c['case_id']} {hk}: date_aligned={r['date_aligned']}"

# ═══ Fail-closed: no predictive alpha ═══
def test_no_predictive_alpha(rel_json):
    for c in rel_json["cases"]:
        for hk, r in c["relative_returns"].items():
            assert r["can_interpret_as_predictive_alpha"] is False

# ═══ Fail-closed: no buy/sell ═══
def test_no_buy_sell_safety():
    for fn in ["core_12_real_returns.json", "csi300_benchmark_returns.json", "core_12_benchmark_relative_returns.json"]:
        text = (CASES / fn).read_text()
        for word in ["BUY", "SELL", "PLACE_ORDER", "AUTO_EXECUTE"]:
            assert word not in text, f"{fn} contains {word}"

# ═══ Entry/Exit close > 0 ═══
def test_entry_close_positive(stock_json):
    for c in stock_json["cases"]:
        if c["entry_close"] is not None:
            assert c["entry_close"] > 0, f"{c['case_id']}: entry_close={c['entry_close']}"

def test_horizon_count(stock_json):
    assert stock_json["total_cases"] == 12
    assert len(stock_json["horizons"]) == 5

def test_all_horizons_have_formula(stock_json):
    for c in stock_json["cases"]:
        for hk, r in c["returns"].items():
            assert r["calculation_formula"] == "exit_close / entry_close - 1"
            assert "truth_status" in r
