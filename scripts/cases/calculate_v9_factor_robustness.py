#!/usr/bin/env python3
"""V9-C: Calculate factor robustness across years, regimes, and industries."""
import json
import math
import csv
import io
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
LARGE = W / "runtime_reports" / "cases" / "v8_large_data"
CASES = W / "runtime_reports" / "cases"
PROC = W / "data" / "research_db" / "market_data" / "processed"


def spearman(xs, ys):
    n = len(xs)
    if n < 2:
        return None
    ux = sorted(set(xs))
    uy = sorted(set(ys))
    rx = {v: i for i, v in enumerate(ux)}
    ry = {v: i for i, v in enumerate(uy)}
    # Pearson on ranks
    xs_r = [rx[x] for x in xs]
    ys_r = [ry[y] for y in ys]
    mx = sum(xs_r) / n
    my = sum(ys_r) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs_r) / (n - 1))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys_r) / (n - 1))
    if sx == 0 or sy == 0:
        return None
    return sum((x - mx) * (y - my) for x, y in zip(xs_r, ys_r)) / ((n - 1) * sx * sy)


def main():
    # Load V8 large data
    factors = json.loads(
        (LARGE / "v8_expanded_factor_values.json").read_text()
    )
    labels = json.loads(
        (LARGE / "v8_forward_return_labels.json").read_text()
    )

    # Pre-index
    fv_by = {
        (r["as_of_date"], r["ticker"]): r["factor_values"]
        for r in factors["records"]
    }
    lab_by = {}
    for l in labels["labels"]:
        lab_by[(l["as_of_date"], l["ticker"], l["horizon"])] = l[
            "future_relative_return"
        ]

    # Load benchmark for regime
    bm_data = {}
    bf = PROC / "v8_benchmark_csi300_price.csv"
    if bf.exists():
        for row in csv.DictReader(io.StringIO(bf.read_text())):
            bm_data[row["trade_date"]] = float(row["close"])

    bm_dates = sorted(bm_data.keys())
    bm_60d_ret = {}
    bm_60d_vol = {}
    for idx, ad in enumerate(bm_dates):
        if idx < 60:
            continue
        past = bm_dates[idx - 60 : idx + 1]
        if bm_data.get(past[0]) and bm_data.get(past[-1]) and bm_data[past[0]] > 0:
            bm_60d_ret[ad] = bm_data[past[-1]] / bm_data[past[0]] - 1
        dr = []
        for j in range(len(past) - 1):
            if (
                bm_data.get(past[j])
                and bm_data[past[j]] > 0
                and bm_data.get(past[j + 1])
            ):
                dr.append(bm_data[past[j + 1]] / bm_data[past[j]] - 1)
        if len(dr) > 10:
            m = sum(dr) / len(dr)
            bm_60d_vol[ad] = math.sqrt(
                sum((x - m) ** 2 for x in dr) / (len(dr) - 1)
            )

    vol_vals = sorted(bm_60d_vol.values())
    vol_median = vol_vals[len(vol_vals) // 2] if vol_vals else 0

    def regime(ad):
        r = bm_60d_ret.get(ad, 0)
        v = bm_60d_vol.get(ad, vol_median)
        if r > 0.05:
            mr = "BULL"
        elif r < -0.05:
            mr = "BEAR"
        else:
            mr = "SIDEWAYS"
        mv = "HIGH_VOL" if v > vol_median else "LOW_VOL"
        return f"{mr}_{mv}"

    # Load stability for factor IDs
    stability = json.loads(
        (CASES / "v9_formal_factor_stability.json").read_text()
    )
    fids = sorted(set(m["factor_id"] for m in stability["metrics"]))
    ads = sorted(set(r["as_of_date"] for r in factors["records"]))
    tickers = sorted(set(r["ticker"] for r in factors["records"]))
    h = "T20"

    # Registry for industry
    REG = json.loads(
        (W / "data" / "research_db" / "cases" / "case_registry_v1.json").read_text()
    )
    industries = set(c.get("industry", "") for c in REG if c.get("industry"))

    results = []
    for fid in fids:
        # Year robustness
        yr_rics = {}
        for yr in ["2021", "2022", "2023", "2024"]:
            yrics = []
            for ad in ads:
                if not ad.startswith(yr):
                    continue
                xs = []
                ys = []
                for tk in tickers:
                    fv = fv_by.get((ad, tk))
                    yv = lab_by.get((ad, tk, h))
                    if fv and fid in fv and yv is not None:
                        xs.append(fv[fid]["value"])
                        ys.append(yv)
                if len(xs) < 30:
                    continue
                ric = spearman(xs, ys)
                if ric is not None:
                    yrics.append(ric)
            if len(yrics) >= 20:
                yr_rics[yr] = {
                    "mean_rankic": round(sum(yrics) / len(yrics), 4),
                    "valid_dates": len(yrics),
                }

        # Regime robustness
        reg_rics = {}
        for ad in ads:
            rg = regime(ad)
            reg_rics.setdefault(rg, [])
            xs = []
            ys = []
            for tk in tickers:
                fv = fv_by.get((ad, tk))
                yv = lab_by.get((ad, tk, h))
                if fv and fid in fv and yv is not None:
                    xs.append(fv[fid]["value"])
                    ys.append(yv)
            if len(xs) < 30:
                continue
            ric = spearman(xs, ys)
            if ric is not None:
                reg_rics[rg].append(ric)

        reg_out = {}
        for rg, vals in reg_rics.items():
            if len(vals) >= 10:
                reg_out[rg] = {
                    "mean_rankic": round(sum(vals) / len(vals), 4),
                    "valid_dates": len(vals),
                }

        # Grade
        yr_vals = [v["mean_rankic"] for v in yr_rics.values()] if yr_rics else []
        sign_consistent = (
            all(v >= 0 for v in yr_vals) or all(v <= 0 for v in yr_vals)
            if yr_vals
            else False
        )
        if sign_consistent and len(yr_rics) >= 3:
            grade = "ROBUST"
        elif len(yr_rics) >= 2:
            grade = "REVIEW"
        elif len(yr_rics) >= 1:
            grade = "WEAK"
        else:
            grade = "REJECT"

        results.append(
            {
                "factor_id": fid,
                "horizon": h,
                "year_robustness": yr_rics,
                "regime_robustness": reg_out,
                "industry_warning": len(industries) > 3,
                "robustness_grade": grade,
                "ready_for_alpha_claim": False,
                "alpha_validated": False,
            }
        )

    out = {
        "status": "V9_FACTOR_ROBUSTNESS_BUILT",
        "regime_count": len(set(regime(ad) for ad in ads if ad in bm_60d_ret)),
        "robustness_results": results,
        "alpha_validated": False,
    }
    (CASES / "v9_factor_robustness.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False)
    )
    grades = set(r["robustness_grade"] for r in results)
    print(
        f"Robustness: {len(results)} factors, "
        f"grades={grades}, regimes={out['regime_count']}"
    )


if __name__ == "__main__":
    main()
