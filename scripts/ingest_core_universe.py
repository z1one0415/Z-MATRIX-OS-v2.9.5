#!/usr/bin/env python3
"""批量采集脚本 — 将 Z-G01 查询结果持久化到 data/ 目录

用法:
  python3 scripts/ingest_core_universe.py                    # 采集核心池
  python3 scripts/ingest_core_universe.py --tickers 002472,601899  # 指定股票
  python3 scripts/ingest_core_universe.py --years 5          # 5年历史
  python3 scripts/ingest_core_universe.py --dry-run          # 只显示要采集的股票
"""
from __future__ import annotations
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path
from datetime import datetime, timedelta

# 导入 Z-G01
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipelines" / "Z-G01_数据后勤保障"))
from gate_data import _ts_kline, _ts_finance, _disk_cache_save, _DATA_CACHE_DIRS


def load_core_universe() -> list[str]:
    """加载核心股票池"""
    # 来源1: data/universe/core_universe.json 缓存
    cache_path = Path("data/universe/core_universe.json")
    if cache_path.exists():
        data = json.loads(cache_path.read_text())
        tickers = data.get("tickers", [])
        if tickers:
            return tickers

    # 来源2: 持仓 + 观察池
    tickers = [
        "002472",  # 双环传动
        "601899",  # 紫金矿业
        "588000",  # 科创50ETF
        "002979",  # 雷赛智能
        "688017",  # 绿的谐波
        "300580",  # 贝斯特
        "603662",  # 柯力传感
        "688322",  # 奥比中光
        "003021",  # 兆威机电
        "603667",  # 五洲新春
        "002050",  # 三花智控
        "000977",  # 浪潮信息
        "601898",  # 中煤能源
    ]
    return tickers


def ingest_kline(ticker: str, years: int = 3) -> dict:
    """采集单只股票的日K线并持久化"""
    days = years * 365
    result = _ts_kline(ticker, days, adjust="qfq")
    if result.get("error"):
        return {"ticker": ticker, "status": "FAILED", "reason": result["error"]}

    # 持久化到 CSV
    dates = result.get("dates", [])
    n = len(dates)
    rows = []
    for i in range(n):
        rows.append({
            "date": dates[i],
            "open": str(result["open"][i]) if i < len(result.get("open", [])) else "",
            "high": str(result["high"][i]) if i < len(result.get("high", [])) else "",
            "low": str(result["low"][i]) if i < len(result.get("low", [])) else "",
            "close": str(result["close"][i]) if i < len(result.get("close", [])) else "",
            "volume": str(result["volume"][i]) if i < len(result.get("volume", [])) else "",
            "amount": str(result["amount"][i]) if i < len(result.get("amount", [])) else "",
        })
    _disk_cache_save("price_bars", ticker, rows)
    return {"ticker": ticker, "status": "OK", "bars": n, "source": result.get("source", "tushare")}


def ingest_financial(ticker: str) -> dict:
    """采集单只股票财务数据并持久化"""
    import csv
    fin = _ts_finance(ticker)
    path = _DATA_CACHE_DIRS["fundamentals"] / f"{ticker}_fin.csv"
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(fin.keys()))
        w.writeheader()
        w.writerow(fin)
    has = fin.get("has_finance", False)
    return {"ticker": ticker, "status": "OK" if has else "PARTIAL", "source": "tushare"}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="批量采集核心股票数据")
    parser.add_argument("--tickers", help="指定股票代码(逗号分隔), 默认用核心池")
    parser.add_argument("--years", type=int, default=3, help="历史年数")
    parser.add_argument("--dry-run", action="store_true", help="只预览不采集")
    parser.add_argument("--kline", action="store_true", default=True, help="采集日K线")
    parser.add_argument("--financial", action="store_true", default=True, help="采集财务数据")
    parser.add_argument("--delay", type=float, default=0.3, help="API调用的间隔秒数(限流)")
    args = parser.parse_args()

    if args.tickers:
        tickers = [t.strip() for t in args.tickers.split(",")]
    else:
        tickers = load_core_universe()

    print(f"核心股票池: {len(tickers)} 只")
    if args.dry_run:
        for t in tickers:
            print(f"  {t}")
        print("--dry-run: 未实际采集")
        return

    results = {"kline_ok": 0, "kline_fail": 0, "fin_ok": 0, "fin_fail": 0}

    for i, ticker in enumerate(tickers):
        print(f"[{i+1}/{len(tickers)}] {ticker}...", end=" ", flush=True)

        if args.kline:
            r = ingest_kline(ticker, args.years)
            print(f"K线:{r['status']}({r.get('bars','?')}条)", end=" ", flush=True)
            if r["status"] == "OK":
                results["kline_ok"] += 1
            else:
                results["kline_fail"] += 1

        if args.financial:
            r = ingest_financial(ticker)
            print(f"财务:{r['status']}", end=" ", flush=True)
            if r["status"] == "OK":
                results["fin_ok"] += 1
            else:
                results["fin_fail"] += 1

        print(flush=True)
        time.sleep(args.delay)  # API限流保护

    print(f"\n完成: 日K线 {results['kline_ok']}/{len(tickers)} 财务 {results['fin_ok']}/{len(tickers)}")
    if results["kline_fail"] or results["fin_fail"]:
        print(f"失败: {results['kline_fail']}/{results['fin_fail']}")


if __name__ == "__main__":
    main()
