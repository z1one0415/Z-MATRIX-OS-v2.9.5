#!/usr/bin/env python3
"""V11 Semantic Audit: V10 thesis ↔ V11 watchlist + snapshot consistency."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def main():
    tp = json.loads((C / "v10_candidate_factor_thesis_pack.json").read_text())
    wl = json.loads((C / "v11_candidate_factor_watchlist.json").read_text())
    snap_data = json.loads((C / "v11_paper_signal_snapshot.json").read_text())

    mm = []
    lk = []
    bv = []
    sv = []
    mv = []

    # V10 ↔ V11 watchlist
    for wi in wl["watch_items"]:
        fid = wi["factor_id"]
        v10 = next(
            (
                c
                for c in tp["candidates"]
                if c["factor_id"] == fid and c["horizon"] == wi["horizon"]
            ),
            {},
        )
        v10e = v10.get("supporting_evidence", {})
        for k in [
            "rankic_direction",
            "decay_pattern",
            "decay_pattern_basis",
            "raw_rankic_trend",
        ]:
            vv = v10e.get(k)
            wv = wi.get(k)
            if vv is not None and wv is not None and vv != wv:
                mm.append(f"{fid}.{k}:V10={vv} V11={wv}")
        dp = wi.get("decay_pattern", "")
        if dp in ("MONOTONIC_INCREASING", "MONOTONIC_DECREASING"):
            lk.append(f"{fid}.decay_pattern={dp}")
        rd = wi.get("rankic_direction")
        bu = wi.get("bucket_direction")
        if rd == "NEGATIVE" and bu != "LOW_FACTOR_VALUE_FAVORED":
            bv.append(f"{fid}:NEGATIVE bkt={bu}")
        if rd == "POSITIVE" and bu != "HIGH_FACTOR_VALUE_FAVORED":
            bv.append(f"{fid}:POSITIVE bkt={bu}")

    # V11 watchlist ↔ signal snapshot
    for sn in snap_data["snapshots"]:
        wid = sn["watch_id"]
        rd = sn.get("rankic_direction")
        wi = next(
            (w for w in wl["watch_items"] if w["watch_id"] == wid), {}
        )
        if wi.get("rankic_direction") != rd:
            sv.append(
                f"{wid}: WL={wi.get('rankic_direction')} SN={rd}"
            )
        # MIXED must have zero buckets
        if rd in ("MIXED", "MISSING"):
            if sn.get("favored_bucket_size", 0) > 0:
                mv.append(
                    f"{wid}: MIXED favored_bucket_size={sn['favored_bucket_size']}"
                )
            if sn.get("comparison_bucket_size", 0) > 0:
                mv.append(
                    f"{wid}: MIXED comp_bucket_size={sn['comparison_bucket_size']}"
                )
            if sn.get("favored_bucket") != []:
                mv.append(f"{wid}: MIXED favored_bucket not empty")
            if sn.get("comparison_bucket") != []:
                mv.append(f"{wid}: MIXED comp_bucket not empty")
            if sn.get("bucket_policy") != "OBSERVATION_ONLY_NO_PREFERRED_DIRECTION":
                mv.append(
                    f"{wid}: MIXED bucket_policy={sn.get('bucket_policy')}"
                )

    ok = (
        len(mm) == 0
        and len(lk) == 0
        and len(bv) == 0
        and len(sv) == 0
        and len(mv) == 0
    )
    sa = {
        "status": "V11_WATCHLIST_SEMANTIC_AUDIT_PASS" if ok else "FAIL",
        "checked_watch_items": len(wl["watch_items"]),
        "checked_signal_snapshots": len(snap_data["snapshots"]),
        "semantic_mismatch_count": len(mm),
        "semantic_missing_count": len(
            wl.get("semantic_missing_fields", [])
        ),
        "raw_monotonic_leaks": lk,
        "bucket_direction_violations": bv,
        "snapshot_direction_violations": sv,
        "mixed_bucket_violations": mv,
        "ready_for_v11_closeout": ok,
    }
    json.dump(
        sa,
        open(C / "v11_watchlist_semantic_audit.json", "w"),
        indent=2,
    )
    print(
        f"Semantic audit: {'PASS' if ok else 'FAIL'} "
        f"| mm={len(mm)} lk={len(lk)} bv={len(bv)} sv={len(sv)} mv={len(mv)}"
    )


if __name__ == "__main__":
    main()
