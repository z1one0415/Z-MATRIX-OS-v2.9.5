from __future__ import annotations

def normalize_return_display_value(x) -> dict:
    if x is None:
        return {"raw_value": None, "display_pct": None, "unit": "percentage_point"}
    v = float(x)
    return {"raw_value": v, "display_pct": v, "display_text": f"{v:+.2f}%", "unit": "percentage_point", "must_not_multiply_by_100": True}

def assert_return_unit_not_double_scaled(metrics: dict) -> list[str]:
    errors = []
    for key in ("mean", "median", "trimmed_mean_5pct", "winsorized_mean_5pct"):
        v = metrics.get(key)
        if v is None: continue
        if abs(float(v)) > 5000:
            errors.append(f"{key} suspiciously large: {v}")
    return errors
