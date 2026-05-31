#!/usr/bin/env python3
"""V7-B: Calculate exploratory IC/RankIC from factor snapshots and forward labels."""
import json, math
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
CASES = W / "runtime_reports" / "cases"

def pearson(xs, ys):
    n = len(xs)
    if n < 2: return None
    mx = sum(xs) / n; my = sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs) / (n - 1))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys) / (n - 1))
    if sx == 0 or sy == 0: return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / ((n - 1) * sx * sy)

def spearman(xs, ys):
    n = len(xs)
    if n < 2: return None
    ux = sorted(set(xs)); uy = sorted(set(ys))
    rx = {v: i for i, v in enumerate(ux)}; ry = {v: i for i, v in enumerate(uy)}
    return pearson([rx[x] for x in xs], [ry[y] for y in ys])

def main():
    fv = json.loads((CASES / "v6b_price_only_factor_values.json").read_text())
    labels = json.loads((CASES / "v7_forward_return_labels.json").read_text())

    factor_ids = list(fv["records"][0]["factor_values"].keys()) if fv["records"] else []
    horizons = labels["horizons"]
    as_of_dates = sorted(set(r["as_of_date"] for r in fv["records"]))

    metrics = []
    for fid in factor_ids:
        for hn in horizons:
            ics = []; rics = []; date_count = 0
            for ad in as_of_dates:
                xs = []; ys = []
                for r in fv["records"]:
                    if r["as_of_date"] != ad: continue
                    if fid not in r["factor_values"]: continue
                    match = [l for l in labels["labels"]
                             if l["as_of_date"] == ad and l["ticker"] == r["ticker"] and l["horizon"] == hn]
                    if not match: continue
                    lab = match[0]
                    xv = r["factor_values"][fid]["value"]
                    yv = lab["future_relative_return"]
                    if yv is None: continue
                    xs.append(xv); ys.append(yv)
                if len(xs) < 8: continue  # minimum cross-section
                ic = pearson(xs, ys); ric = spearman(xs, ys)
                if ic is not None: ics.append(ic)
                if ric is not None: rics.append(ric)
                date_count += 1

            if not ics: continue
            nics = len(ics); nrics = len(rics)
            m = {
                "factor_id": fid, "horizon": hn,
                "label_type": "future_relative_return",
                "valid_date_count": date_count,
                "cross_section_size": 12,
                "mean_rankic": round(sum(rics) / nrics, 4) if nrics else None,
                "median_rankic": round(sorted(rics)[nrics // 2], 4) if nrics else None,
                "positive_rankic_ratio": round(sum(1 for v in rics if v > 0) / nrics, 4) if nrics else None,
                "mean_ic": round(sum(ics) / nics, 4) if nics else None,
                "positive_ic_ratio": round(sum(1 for v in ics if v > 0) / nics, 4) if nics else None,
                "sample_warning": "SMALL_SAMPLE_EXPLORATORY_ONLY",
                "alpha_validated": False,
                "ready_for_alpha_claim": False,
            }
            metrics.append(m)

    out = {
        "status": "V7_EXPLORATORY_FACTOR_METRICS_BUILT",
        "validation_type": "SMALL_SAMPLE_EXPLORATORY_ONLY",
        "alpha_validated": False,
        "ready_for_alpha_claim": False,
        "metrics": metrics,
    }
    (CASES / "v7_exploratory_factor_metrics.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"Exploratory metrics: {len(metrics)} factor×horizon combos | alpha_validated=False")

if __name__ == "__main__":
    main()
