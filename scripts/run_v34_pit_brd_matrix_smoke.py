#!/usr/bin/env python3
"""v3.4 PIT BRD Matrix Smoke — prove real data → classify_stock_role → brd_connected"""
from __future__ import annotations
import json, sys
from pathlib import Path
from zmatrix.brd_replay.pit_feature_builder import build_pit_features
from zmatrix.brd_matrix_pit.brd_input_bundle_builder import build_brd_input_bundle
from zmatrix.brd_replay.real_brd_connector import build_real_brd_classifier_connector

def main():
    connector = build_real_brd_classifier_connector()
    if connector.connector_status != "CONNECTED":
        print(f"BLOCKED: connector_status={connector.connector_status}")
        sys.exit(2)

    tickers = ["000001","002472","601899","588000","600519","000002","300001","688001","002979","603259",
               "601898","688017","002050","000977","603662"]
    replay_date = "2026-05-01"
    rows = []

    for ticker in tickers:
        features = build_pit_features(ticker=ticker, replay_date=replay_date, local_data_root=".")
        bundle = build_brd_input_bundle(ticker=ticker, replay_date=replay_date, local_data_root=".", pit_features=features)
        features["brd_input_bundle"] = bundle
        result = connector.classify(features)
        rows.append({
            "ticker": ticker,
            "feature_status": features.get("feature_status"),
            "input_ready": bundle.get("input_ready"),
            "b_status": bundle.get("b_matrix", {}).get("status"),
            "r_status": bundle.get("r_matrix", {}).get("status"),
            "brd_connected": result.get("brd_connected"),
            "role": result.get("role"),
            "fallback": result.get("fallback"),
        })

    connected = [r for r in rows if r.get("brd_connected")]
    fallback = [r for r in rows if r.get("fallback")]
    roles = {}
    for r in rows:
        roles[r.get("role", "?")] = roles.get(r.get("role", "?"), 0) + 1

    report = {
        "smoke_version": "V34_PIT_BRD_MATRIX_SMOKE_V10",
        "connector_status": connector.connector_status,
        "connector_impl": getattr(connector, "impl_name", None),
        "total_tickers": len(rows),
        "brd_connected_count": len(connected),
        "fallback_count": len(fallback),
        "fallback_rate": len(fallback) / len(rows) if rows else None,
        "role_distribution": roles,
        "rows": rows,
    }

    Path("runtime_reports").mkdir(exist_ok=True)
    Path("runtime_reports/v34_smoke.json").write_text(json.dumps(report, indent=2, ensure_ascii=False))

    for r in rows:
        print(f"  {r['ticker']}: feat={r['feature_status']} b={r['b_status']} r={r['r_status']} → {r['role']} bcd={r['brd_connected']}")

    print(f"\nconnector: {connector.connector_status} → {getattr(connector, 'impl_name', '?')}")
    print(f"brd_connected: {len(connected)}/{len(rows)}")
    print(f"fallback: {len(fallback)}/{len(rows)} ({report['fallback_rate']*100:.1f}%)" if report['fallback_rate'] else "fallback: N/A")
    print(f"roles: {roles}")

    if len(connected) == 0:
        print("BLOCKED: brd_connected_count=0")
        sys.exit(3)

    if report['fallback_rate'] and report['fallback_rate'] >= 0.05:
        print(f"BLOCKED: fallback_rate={report['fallback_rate']*100:.1f}% >= 5%")
        sys.exit(4)

    print("v3.4 PIT BRD Matrix Smoke PASS")
    print("BRD_INPUT_CHAIN_CONNECTED ✅")

if __name__ == "__main__":
    main()
