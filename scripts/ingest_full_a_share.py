#!/usr/bin/env python3
"""全A股批量采集 — 3年日K线 + 财务快照"""
import sys, os, time, json, csv
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pipelines", "Z-G01_数据后勤保障"))
from pathlib import Path
from datetime import datetime, timedelta
import tushare as ts

token = open(Path.home() / ".tushare" / "token").read().strip()
ts.set_token(token)
pro = ts.pro_api()

ROOT = Path(__file__).resolve().parents[1]
BAR_DIR = ROOT / "data" / "price_bars"
FIN_DIR = ROOT / "data" / "fundamentals"
BAR_DIR.mkdir(parents=True, exist_ok=True)
FIN_DIR.mkdir(parents=True, exist_ok=True)

# 加载股票列表
with open(ROOT / "data" / "universe" / "a_share_all.json") as f:
    tickers = json.load(f)["tickers"]

print(f"全A股: {len(tickers)} 只, 3年日K, 每只约750行")
print(f"输出: {BAR_DIR}/ 和 {FIN_DIR}/")
print("开始采集... (0.35s间隔，防限流)")
print()

ok = 0
fail = 0
skip = 0
start_time = time.time()

for i, ticker in enumerate(tickers, 1):
    suffix = "SZ" if ticker[0] in "03" else "SH"
    ts_code = f"{ticker}.{suffix}"
    bar_path = BAR_DIR / f"{ticker}.csv"
    fin_path = FIN_DIR / f"{ticker}_fin.csv"

    # 续传检查：已有日K和财务则跳过
    if bar_path.exists() and fin_path.exists():
        skip += 1
        if i % 500 == 0:
            elapsed = time.time() - start_time
            print(f"[{i}/{len(tickers)}] SKIP={skip} OK={ok} FAIL={fail} {elapsed/60:.0f}min")
        continue

    try:
        # 日K线
        if not bar_path.exists():
            end = "20260526"
            start = "20230526"  # 3年
            df = pro.daily(ts_code=ts_code, start_date=start, end_date=end)
            if df is not None and not df.empty:
                df = df.sort_values("trade_date")
                df.to_csv(bar_path, index=False, encoding="utf-8-sig")
                ok += 1
            else:
                fail += 1
                bar_path.write_text("date,open,high,low,close,vol,amount\n")

        # 财务快照
        if not fin_path.exists():
            try:
                fin = pro.fina_indicator(ts_code=ts_code, start_date="20251231")
                if fin is not None and not fin.empty:
                    fin.head(1).to_csv(fin_path, index=False, encoding="utf-8-sig")
            except Exception:
                pass

    except Exception as e:
        fail += 1
        if i % 100 == 0:
            print(f"[{i}] {ticker} FAIL: {str(e)[:60]}")

    time.sleep(0.35)

    if i % 500 == 0 or i == len(tickers):
        elapsed = time.time() - start_time
        bar_count = len(list(BAR_DIR.glob("*.csv")))
        fin_count = len(list(FIN_DIR.glob("*.csv")))
        print(f"[{i}/{len(tickers)}] bars={bar_count} fin={fin_count} ok={ok} fail={fail} skip={skip} {elapsed/60:.0f}min")

elapsed = time.time() - start_time
bar_count = len(list(BAR_DIR.glob("*.csv")))
fin_count = len(list(FIN_DIR.glob("*.csv")))
size = sum(f.stat().st_size for f in BAR_DIR.glob("*.csv")) + sum(f.stat().st_size for f in FIN_DIR.glob("*.csv"))
print(f"\n完成: {elapsed/60:.0f}分钟")
print(f"日K: {bar_count}/{len(tickers)} 财务: {fin_count}/{len(tickers)}")
print(f"总数据量: {size/1024/1024:.0f}MB")
