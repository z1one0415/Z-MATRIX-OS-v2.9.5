from __future__ import annotations

import csv
from pathlib import Path

import pytest

from zmatrix.research_db.market_data.vendor_ingestion import (
    IngestionWindow,
    VendorIngestionConfig,
    build_window,
    load_symbols,
    normalize_ts_code,
    write_vendor_market_data,
)


class FakeVendorClient:
    def __init__(self):
        self.calls = []

    def query(self, api_name: str, **kwargs):
        self.calls.append((api_name, kwargs))
        if api_name == "stock_basic":
            return [{"ts_code": "601899.SH", "symbol": "601899", "name": "Zijin"}]
        if api_name == "trade_cal":
            return [{"exchange": "SSE", "cal_date": "20240102", "is_open": 1}]
        if api_name == "index_daily":
            return [{"ts_code": kwargs["ts_code"], "trade_date": "20240102", "close": 3500.0}]
        return [{"ts_code": kwargs["ts_code"], "trade_date": "20240102", "close": 10.0}]


def test_normalize_ts_code():
    assert normalize_ts_code("601899") == "601899.SH"
    assert normalize_ts_code("002472") == "002472.SZ"
    assert normalize_ts_code("430047") == "430047.BJ"
    assert normalize_ts_code("300750.SZ") == "300750.SZ"


def test_build_window_uses_five_year_span():
    import datetime as dt

    window = build_window(as_of=dt.date(2026, 6, 13), years=5)
    assert window.end_date == "20260613"
    assert window.start_date <= "20210613"
    assert window.years == 5


def test_load_symbols_from_text_file(tmp_path: Path):
    symbol_file = tmp_path / "symbols.txt"
    symbol_file.write_text("601899\n002472\n", encoding="utf-8")
    assert load_symbols(None, symbol_file) == ["601899.SH", "002472.SZ"]


def test_load_symbols_from_json_file(tmp_path: Path):
    array_file = tmp_path / "array.json"
    array_file.write_text('["601899", "002472"]', encoding="utf-8")
    assert load_symbols(None, array_file) == ["601899.SH", "002472.SZ"]

    object_file = tmp_path / "object.json"
    object_file.write_text('{"tickers": ["300750", "688981"]}', encoding="utf-8")
    assert load_symbols(None, object_file) == ["300750.SZ", "688981.SH"]


def test_ingestor_writes_manifest_and_endpoint_files(tmp_path: Path):
    client = FakeVendorClient()
    config = VendorIngestionConfig(
        symbols=["601899.SH"],
        output_root=tmp_path,
        endpoints=("stock_basic", "trade_cal", "index_daily", "daily", "adj_factor"),
        index_codes=("000300.SH",),
        window=IngestionWindow(start_date="20210101", end_date="20260613", years=5),
        delay_seconds=0,
        run_id="test-run",
    )

    manifest = write_vendor_market_data(client, config)
    run_root = tmp_path / "test-run"

    assert manifest["status"] == "VENDOR_MARKET_DATA_INGESTION_BUILT"
    assert manifest["source_vendor"] == "TUSHARE"
    assert manifest["symbol_count"] == 1
    assert manifest["runtime_guard"]["paper_only"] is True
    assert manifest["runtime_guard"]["broker_runtime"] == "BLOCKED"
    assert manifest["runtime_guard"]["real_trade"] == "BLOCKED"
    assert manifest["file_count"] == 5
    assert (run_root / "manifest.json").exists()
    assert (run_root / "daily" / "601899.SH.csv").exists()
    assert (run_root / "adj_factor" / "601899.SH.csv").exists()

    with (run_root / "daily" / "601899.SH.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["ts_code"] == "601899.SH"


def test_ingestor_records_endpoint_failures(tmp_path: Path):
    class BrokenClient(FakeVendorClient):
        def query(self, api_name: str, **kwargs):
            if api_name == "daily":
                raise RuntimeError("vendor unavailable")
            return super().query(api_name, **kwargs)

    config = VendorIngestionConfig(
        symbols=["601899.SH"],
        output_root=tmp_path,
        endpoints=("daily",),
        window=IngestionWindow(start_date="20210101", end_date="20260613", years=5),
        delay_seconds=0,
        run_id="broken-run",
    )
    manifest = write_vendor_market_data(BrokenClient(), config)
    assert manifest["file_count"] == 0
    assert manifest["failure_count"] == 1
    assert manifest["failures"][0]["endpoint"] == "daily"


def test_invalid_symbol_rejected():
    with pytest.raises(ValueError):
        normalize_ts_code("ABC")
