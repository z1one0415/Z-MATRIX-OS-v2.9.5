# allowlist: forbidden-token-definition
from __future__ import annotations
from collections import Counter
from zmatrix.regime_sector_attribution.schema import DEFAULT_REGIME_SECTOR_SAFETY, JOINT_THRESHOLDS

def audit_sector_concentration(*, joined_rows: list[dict]) -> dict:
    sectors_all = [r.get("sector") for r in joined_rows or [] if r.get("sector")]
    sc = Counter(sectors_all); total = len(sectors_all)
    top = sc.most_common(1); top5 = sc.most_common(5)
    ts = top[0][1]/total if top and total else None
    t5 = sum(x[1] for x in top5)/total if total else None
    reasons = []
    if ts and ts>JOINT_THRESHOLDS["max_top_sector_share"]: reasons.append("SECTOR_CONCENTRATION_RISK")
    if t5 and t5>JOINT_THRESHOLDS["max_top_5_sector_share"]: reasons.append("TOP5_SECTOR_CONCENTRATION_RISK")
    return {"auditor_version":"V3512_SECTOR_CONCENTRATION_AUDITOR_V10","total_kept":total,"sector_count":len(sc),"top_sector":top[0][0] if top else None,"top_sector_share":ts,"top_5_sector_share":t5,"top_10_sectors":sc.most_common(10),"concentration_status":"PASS" if not reasons else "WARNING","reasons":reasons,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_SECTOR_SAFETY)}
