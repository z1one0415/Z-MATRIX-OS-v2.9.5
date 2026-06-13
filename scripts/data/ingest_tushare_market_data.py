#!/usr/bin/env python3
"""CLI wrapper for local vendor market data ingestion."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from zmatrix.research_db.market_data.vendor_ingestion import (
    DEFAULT_ENDPOINTS,
    VendorIngestionConfig,
    build_client_from_env,
    build_window,
    load_symbols,
    write_vendor_market_data,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest vendor market data into the local ResearchDB vendor store")
    parser.add_argument("--symbols", help="Comma-separated symbols, e.g. 601899,002472,300750")
    parser.add_argument("--symbol-file", help="Text or JSON symbol list")
    parser.add_argument("--years", type=int, default=5)
    parser.add_argument("--end-date", help="YYYYMMDD end date; defaults to today")
    parser.add_argument("--output-root", default="data/research_db/market_data/vendor/tushare_5y")
    parser.add_argument("--endpoints", default=",".join(DEFAULT_ENDPOINTS))
    parser.add_argument("--delay", type=float, default=0.25)
    parser.add_argument("--run-id", default="")
    parser.add_argument("--env-key", default="TUSHARE_TOKEN")
    parser.add_argument("--dry-plan", action="store_true", help="Print the plan without calling the vendor")
    args = parser.parse_args()

    import datetime as _dt

    as_of = _dt.datetime.strptime(args.end_date, "%Y%m%d").date() if args.end_date else None
    symbols = load_symbols(args.symbols, args.symbol_file)
    window = build_window(as_of=as_of, years=args.years)
    endpoints = tuple(item.strip() for item in args.endpoints.split(",") if item.strip())
    config = VendorIngestionConfig(
        symbols=symbols,
        output_root=Path(args.output_root),
        endpoints=endpoints,
        window=window,
        delay_seconds=args.delay,
        run_id=args.run_id,
    )
    plan = {
        "status": "VENDOR_MARKET_DATA_INGESTION_PLAN",
        "source_vendor": "TUSHARE",
        "symbols": symbols,
        "symbol_count": len(symbols),
        "window": {"start_date": window.start_date, "end_date": window.end_date, "years": window.years},
        "endpoints": endpoints,
        "output_root": str(config.output_root),
        "run_id": config._normalized_run_id(),
        "paper_only": True,
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }
    if args.dry_plan:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0

    client = build_client_from_env(args.env_key)
    manifest = write_vendor_market_data(client, config)
    print(json.dumps({"status": manifest["status"], "file_count": manifest["file_count"], "failure_count": manifest["failure_count"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
