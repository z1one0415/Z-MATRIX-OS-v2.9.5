"""ResearchDB Account Truth — missing data detector."""
from __future__ import annotations


def detect_missing_dates(snapshots: list[dict], start_date: str, end_date: str) -> dict:
    """Detect trading days missing from the snapshot series."""
    from datetime import datetime, timedelta
    dates_present = {s.get("date", "") for s in snapshots}
    missing = []
    current = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    while current <= end:
        ds = current.strftime("%Y-%m-%d")
        if ds not in dates_present:
            missing.append(ds)
        current += timedelta(days=1)
    return {
        "start_date": start_date,
        "end_date": end_date,
        "expected_dates": (end - datetime.strptime(start_date, "%Y-%m-%d")).days + 1,
        "present_dates": len(dates_present),
        "missing_dates": len(missing),
        "missing_list": missing[:20],
    }


def detect_missing_fields(records: list[dict], required_fields: list[str]) -> dict:
    """Detect which records are missing required fields."""
    issues = []
    for i, r in enumerate(records):
        missing = [f for f in required_fields if not r.get(f)]
        if missing:
            issues.append({"row": i, "missing_fields": missing})
    return {"status": "PASS" if not issues else "HAS_ISSUES", "issue_count": len(issues), "issues": issues[:10]}
