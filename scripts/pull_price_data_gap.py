#!/usr/bin/env python3
"""
补拉日K数据缺口 — tushare pro
目标: 002472.SZ / 601899.SH 从 20250426 到最新
"""

import os, sys, csv
from datetime import datetime, date

# 读取 token
token_path = os.path.expanduser("~/.tushare/token")
with open(token_path) as f:
    token = f.read().strip()

import tushare as ts
ts.set_token(token)
pro = ts.pro_api()

DATA_ROOT = os.path.expanduser("~/Documents/Z-MATRIX-OS v2.9.5/data/price_bars")

TICKERS = ["002472.SZ", "601899.SH"]
START_DATE = "20250426"
END_DATE = (date.today()).strftime("%Y%m%d")

def pull_and_append(ticker: str):
    csv_path = os.path.join(DATA_ROOT, ticker.split(".")[0] + ".csv")
    if not os.path.exists(csv_path):
        print(f"  ⚠️  CSV not found: {csv_path}")
        return

    # 读取已有数据，找到最后日期
    existing_dates = set()
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if row and len(row) >= 2:
                existing_dates.add(row[1])  # trade_date at index 1

    # 拉取新数据
    print(f"  📡 拉取 {ticker} {START_DATE}→{END_DATE} ...")
    try:
        df = pro.daily(ts_code=ticker, start_date=START_DATE, end_date=END_DATE)
    except Exception as e:
        print(f"  ❌ API error: {e}")
        return

    if df is None or len(df) == 0:
        print(f"  ⚠️  无新数据")
        return

    # 过滤已存在的日期 (tushare的trade_date是YYYYMMDD格式)
    new_rows = df[~df["trade_date"].isin(existing_dates)]
    if len(new_rows) == 0:
        print(f"  ✅ 数据已最新, 无新行")
        return

    # 按日期升序排列（tushare返回的是降序）
    new_rows = new_rows.sort_values("trade_date")

    # 映射到CSV列: ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount,date,volume
    csv_rows = []
    for _, row in new_rows.iterrows():
        td = row["trade_date"]  # YYYYMMDD
        td_fmt = f"{td[:4]}-{td[4:6]}-{td[6:8]}"  # YYYY-MM-DD
        csv_rows.append([
            row.get("ts_code", ticker),
            td,
            row.get("open", ""),
            row.get("high", ""),
            row.get("low", ""),
            row.get("close", ""),
            row.get("pre_close", ""),
            row.get("change", ""),
            row.get("pct_chg", ""),
            row.get("vol", ""),
            row.get("amount", ""),
            td_fmt,
            row.get("volume", ""),
        ])

    # 追加到CSV
    with open(csv_path, "a") as f:
        writer = csv.writer(f, lineterminator="\n")
        for row in csv_rows:
            writer.writerow(row)

    print(f"  ✅ 追加 {len(csv_rows)} 行 ({csv_rows[0][1]} → {csv_rows[-1][1]})")

    # 清理：去重+排序
    clean_csv(csv_path)


def clean_csv(csv_path: str):
    """去重并按trade_date排序"""
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        rows = [row for row in reader if row and row[1] and row[1].isdigit()]

    # 按trade_date去重（保留第一次出现）
    seen = set()
    unique = []
    for row in rows:
        if row[1] not in seen:
            seen.add(row[1])
            unique.append(row)

    # 按trade_date排序
    unique.sort(key=lambda r: r[1])

    with open(csv_path, "w") as f:
        writer = csv.writer(f, lineterminator="\n")
        if header:
            writer.writerow(header)
        for row in unique:
            writer.writerow(row)


if __name__ == "__main__":
    print(f"🔧 数据缺口补拉 {START_DATE} → {END_DATE}")
    print(f"   目标: {TICKERS}")
    for t in TICKERS:
        pull_and_append(t)
    print("\\n✅ 完成")
