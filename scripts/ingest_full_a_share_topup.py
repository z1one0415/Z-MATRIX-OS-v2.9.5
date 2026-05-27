#!/usr/bin/env python3
"""全A股增量补丁 — 把3年扩展到5年（补2021→2023）"""
import sys, os, time, json, csv
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path
import tushare as ts

token = open(Path.home() / ".tushare" / "token").read().strip()
ts.set_token(token)
pro = ts.pro_api()

ROOT = Path(__file__).resolve().parents[1]
BAR_DIR = ROOT / "data" / "price_bars"

# 加载股票列表
with open(ROOT / "data" / "universe" / "a_share_all.json") as f:
    tickers = json.load(f)["tickers"]

print(f"全A股: {len(tickers)} 只，补前2年日K (20210526→20230526)")
print()

ok, fail, skip = 0, 0, 0
start_time = time.time()

for i, ticker in enumerate(tickers, 1):
    suffix = "SZ" if ticker[0] in "03" else "SH"
    ts_code = f"{ticker}.{suffix}"
    bar_path = BAR_DIR / f"{ticker}.csv"

    if not bar_path.exists():
        skip += 1
        continue

    try:
        # 读取现有数据，检查最早日期
        rows = []
        with open(bar_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)

        if not rows:
            skip += 1
            continue

        earliest = min(r["trade_date"] if "trade_date" in r else r["date"] for r in rows)
        
        # 如果最早日期已经是2021年，跳过（已有5年）
        if earliest <= "20210526":
            skip += 1
            continue

        # 需要补2021→当前最早之间的数据
        end = earliest.replace("-", "")
        start = "20210526"
        df = pro.daily(ts_code=ts_code, start_date=start, end_date=end)
        if df is not None and not df.empty:
            df = df.sort_values("trade_date")
            # 去重合并
            existing_dates = set(r["trade_date"] if "trade_date" in r else r["date"] for r in rows)
            new_rows = []
            for _, r in df.iterrows():
                if r["trade_date"] not in existing_dates:
                    new_rows.append(r)
            if new_rows:
                import pandas as pd
                new_df = pd.DataFrame(new_rows)
                combined = pd.concat([new_df, pd.DataFrame(rows)]).sort_values("trade_date").drop_duplicates(subset=["trade_date"])
                combined.to_csv(bar_path, index=False, encoding="utf-8-sig")
                ok += 1
        else:
            fail += 1

    except Exception as e:
        fail += 1

    time.sleep(0.35)

    if i % 500 == 0:
        elapsed = time.time() - start_time
        print(f"[{i}/{len(tickers)}] ok={ok} fail={fail} skip={skip} {elapsed/60:.0f}min")

elapsed = time.time() - start_time
print(f"\n完成: {elapsed/60:.0f}分钟")
print(f"已补: {ok} 跳过: {skip} 失败: {fail}")
