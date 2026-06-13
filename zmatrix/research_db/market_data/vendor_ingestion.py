"""Vendor market data ingestion helpers for ResearchDB local stores."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import time
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Callable


DEFAULT_OUTPUT_ROOT = Path("data/research_db/market_data/vendor/tushare_5y")
DEFAULT_ENDPOINTS = (
    "stock_basic",
    "trade_cal",
    "index_daily",
    "daily",
    "adj_factor",
    "daily_basic",
    "income",
    "balancesheet",
    "cashflow",
    "fina_indicator",
    "dividend",
)
DEFAULT_INDEX_CODES = ("000300.SH", "000905.SH", "000852.SH", "399006.SZ", "000688.SH")


@dataclass(frozen=True)
class IngestionWindow:
    start_date: str
    end_date: str
    years: int


@dataclass
class VendorIngestionConfig:
    symbols: list[str]
    output_root: Path = DEFAULT_OUTPUT_ROOT
    endpoints: tuple[str, ...] = DEFAULT_ENDPOINTS
    index_codes: tuple[str, ...] = DEFAULT_INDEX_CODES
    window: IngestionWindow = field(default_factory=lambda: build_window())
    delay_seconds: float = 0.25
    run_id: str = ""

    def _normalized_run_id(self) -> str:
        if self.run_id:
            return self.run_id
        suffix = hashlib.sha256(
            f"{','.join(self.symbols)}|{self.window.start_date}|{self.window.end_date}".encode("utf-8")
        ).hexdigest()[:8]
        return f"{self.window.end_date}_{suffix}"


def build_window(*, as_of: date | None = None, years: int = 5) -> IngestionWindow:
    anchor = as_of or date.today()
    start = anchor - timedelta(days=years * 365 + 10)
    return IngestionWindow(start_date=start.strftime("%Y%m%d"), end_date=anchor.strftime("%Y%m%d"), years=years)


def normalize_ts_code(symbol: str) -> str:
    value = symbol.strip().upper()
    if "." in value:
        return value
    if len(value) != 6 or not value.isdigit():
        raise ValueError(f"unsupported symbol: {symbol}")
    if value.startswith(("0", "2", "3")):
        return f"{value}.SZ"
    if value.startswith(("4", "8", "9")):
        return f"{value}.BJ"
    return f"{value}.SH"


def default_symbol_seed() -> list[str]:
    return [
        "601899",
        "002472",
        "588000",
        "300750",
        "600519",
        "300308",
        "688256",
        "002594",
        "688981",
        "603986",
    ]


def load_symbols(symbols: str | None, symbol_file: str | Path | None) -> list[str]:
    if symbols:
        return [normalize_ts_code(item) for item in symbols.split(",") if item.strip()]
    if symbol_file:
        path = Path(symbol_file)
        if path.suffix.lower() == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
            raw = data.get("tickers", []) if isinstance(data, dict) else data
            return [normalize_ts_code(str(item)) for item in raw]
        return [normalize_ts_code(line.strip()) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return [normalize_ts_code(item) for item in default_symbol_seed()]


def build_client_from_env(env_key: str = "TUSHARE_TOKEN") -> Any:
    token = os.environ.get(env_key, "").strip()
    if not token:
        raise RuntimeError(f"{env_key} is required for vendor ingestion")
    try:
        import tushare as ts  # type: ignore
    except ImportError as exc:  # pragma: no cover - depends on local environment
        raise RuntimeError("tushare package is required for vendor ingestion") from exc
    ts.set_token(token)
    return ts.pro_api()


def write_vendor_market_data(client: Any, config: VendorIngestionConfig) -> dict[str, Any]:
    return VendorIngestor(client)._write_local_store(config)


class VendorIngestor:
    def __init__(self, client: Any, *, sleep_fn: Callable[[float], None] = time.sleep):
        self.client = client
        self.sleep_fn = sleep_fn

    def _write_local_store(self, config: VendorIngestionConfig) -> dict[str, Any]:
        run_root = config.output_root / config._normalized_run_id()
        run_root.mkdir(parents=True, exist_ok=True)
        manifest: dict[str, Any] = {
            "status": "VENDOR_MARKET_DATA_INGESTION_BUILT",
            "source_vendor": "TUSHARE",
            "write_scope": "LOCAL_VENDOR_STORE_ONLY",
            "runtime_guard": {
                "paper_only": True,
                "broker_runtime": "BLOCKED",
                "real_trade": "BLOCKED",
                "repository_commit_allowed": False,
            },
            "window": {
                "start_date": config.window.start_date,
                "end_date": config.window.end_date,
                "years": config.window.years,
            },
            "symbol_count": len(config.symbols),
            "endpoints": {},
            "files": [],
            "failures": [],
        }

        self._ingest_global_endpoints(config, run_root, manifest)
        self._ingest_index_endpoints(config, run_root, manifest)
        self._ingest_symbol_endpoints(config, run_root, manifest)

        manifest["file_count"] = len(manifest["files"])
        manifest["failure_count"] = len(manifest["failures"])
        manifest_path = run_root / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return manifest

    def _ingest_global_endpoints(self, config: VendorIngestionConfig, run_root: Path, manifest: dict[str, Any]) -> None:
        if "stock_basic" in config.endpoints:
            self._query_to_file(
                "stock_basic",
                run_root / "stock_basic.csv",
                manifest,
                exchange="",
                list_status="L",
                fields="ts_code,symbol,name,area,industry,market,list_date",
            )
        if "trade_cal" in config.endpoints:
            self._query_to_file(
                "trade_cal",
                run_root / "trade_cal.csv",
                manifest,
                exchange="SSE",
                start_date=config.window.start_date,
                end_date=config.window.end_date,
            )

    def _ingest_index_endpoints(self, config: VendorIngestionConfig, run_root: Path, manifest: dict[str, Any]) -> None:
        if "index_daily" not in config.endpoints:
            return
        for code in config.index_codes:
            self._query_to_file(
                "index_daily",
                run_root / "index_daily" / f"{code}.csv",
                manifest,
                ts_code=code,
                start_date=config.window.start_date,
                end_date=config.window.end_date,
            )
            self.sleep_fn(config.delay_seconds)

    def _ingest_symbol_endpoints(self, config: VendorIngestionConfig, run_root: Path, manifest: dict[str, Any]) -> None:
        endpoint_kwargs = {
            "daily": {"start_date": config.window.start_date, "end_date": config.window.end_date},
            "adj_factor": {"start_date": config.window.start_date, "end_date": config.window.end_date},
            "daily_basic": {"start_date": config.window.start_date, "end_date": config.window.end_date},
            "income": {"start_date": config.window.start_date, "end_date": config.window.end_date},
            "balancesheet": {"start_date": config.window.start_date, "end_date": config.window.end_date},
            "cashflow": {"start_date": config.window.start_date, "end_date": config.window.end_date},
            "fina_indicator": {"start_date": config.window.start_date, "end_date": config.window.end_date},
            "dividend": {"start_date": config.window.start_date, "end_date": config.window.end_date},
        }
        for symbol in config.symbols:
            for endpoint, kwargs in endpoint_kwargs.items():
                if endpoint not in config.endpoints:
                    continue
                self._query_to_file(
                    endpoint,
                    run_root / endpoint / f"{symbol}.csv",
                    manifest,
                    ts_code=symbol,
                    **kwargs,
                )
                self.sleep_fn(config.delay_seconds)

    def _query_to_file(self, endpoint: str, output_path: Path, manifest: dict[str, Any], **kwargs: Any) -> None:
        try:
            frame = self.client.query(endpoint, **kwargs)
            row_count = _write_frame_csv(frame, output_path)
            file_info = {
                "endpoint": endpoint,
                "path": output_path.as_posix(),
                "rows": row_count,
                "sha256": _sha256_file(output_path),
            }
            manifest["files"].append(file_info)
            stats = manifest["endpoints"].setdefault(endpoint, {"files": 0, "rows": 0})
            stats["files"] += 1
            stats["rows"] += row_count
        except Exception as exc:  # pragma: no cover - exercised by integration usage
            manifest["failures"].append({"endpoint": endpoint, "target": output_path.as_posix(), "reason": str(exc)[:160]})


def _write_frame_csv(frame: Any, output_path: Path) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if hasattr(frame, "to_csv"):
        frame.to_csv(output_path, index=False, encoding="utf-8-sig")
        return _count_csv_rows(output_path)
    rows = list(frame or [])
    if not rows:
        output_path.write_text("", encoding="utf-8")
        return 0
    fieldnames = sorted({key for row in rows for key in row})
    with output_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _count_csv_rows(path: Path) -> int:
    if not path.exists() or path.stat().st_size == 0:
        return 0
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return max(sum(1 for _ in csv.reader(f)) - 1, 0)
