#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from zmatrix.synthetic_sector_index.sector_mapping_loader import load_sector_mapping
from zmatrix.synthetic_sector_index.replay_sector_feature_joiner import join_replay_sector_features
# Phase features are pre-computed in the basket report
from zmatrix.regime_sector_attribution.regime_sector_joiner import build_regime_sector_joined_rows
from zmatrix.regime_sector_attribution.joint_segment_profiler import profile_joint_segments
from zmatrix.regime_sector_attribution.sector_concentration_auditor import audit_sector_concentration
from zmatrix.regime_sector_attribution.temporal_sector_stability import audit_temporal_sector_stability
from zmatrix.regime_sector_attribution.range_bound_analyzer import analyze_range_bound_drag
from zmatrix.regime_sector_attribution.joint_separability_tester import test_joint_separability
from zmatrix.regime_sector_attribution.joint_candidate_miner import mine_joint_candidates
from zmatrix.regime_sector_attribution.policy import validate_joint_attribution_report
from zmatrix.regime_sector_attribution.schema import DEFAULT_REGIME_SECTOR_SAFETY

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-replay", default="runtime_reports/v35_brd_strategy_replay_result.json")
    ap.add_argument("--mapping-path", default="data/metadata/sector_mapping_v3510.csv")
    ap.add_argument("--output", default="runtime_reports/v3512_regime_sector_joint_attribution_report.json")
    args = ap.parse_args()
    print("Loading replay rows...", flush=True)
    rr = json.loads(Path(args.raw_replay).read_text(encoding="utf-8"))
    rows = []
    for daily in rr.get("daily_results",[]):
        for a in daily.get("paper_actions",[]):
            if a.get("role")=="B_MID_ROTATION" and a.get("paper_action") not in ("NO_ACTION","DATA_GAP",None):
                rows.append(a)
    print(f"  {len(rows)} B_MID_ROTATION rows", flush=True)
    print("Loading sector mapping...", flush=True)
    mapping = load_sector_mapping(mapping_path=args.mapping_path)
    sm = mapping.get("sector_mapping",{})
    print(f"  {len(sm)} tickers mapped", flush=True)
    # Load pre-built phase features from basket report
    print("Loading sector phases...", flush=True)
    phases = {}
    sfwp = {}
    try:
        br = json.loads(Path("runtime_reports/v3511_synthetic_sector_basket_report.json").read_text(encoding="utf-8"))
        # Read phase features from artifact files
        import csv, glob
        artifact_files = glob.glob("runtime_reports/sector_baskets_v3511/*.csv")
        if artifact_files:
            for af in artifact_files:
                sector = Path(af).stem
                sfwp[sector] = []
                with open(af,encoding="utf-8-sig") as f:
                    for r in csv.DictReader(f):
                        sfwp[sector].append({"sector":sector,"trade_date":r.get("trade_date",""),"close_index":r.get("close_index"),"sector_return_5d":r.get("sector_return_5d"),"sector_return_20d":r.get("sector_return_20d"),"sector_return_60d":r.get("sector_return_60d"),"sector_phase":r.get("sector_phase"),"sector_relative_strength_vs_market":r.get("sector_relative_strength_vs_market"),"sector_volatility_20d":_float(r.get("sector_volatility_20d"))})
        print(f"  Loaded phases from {len(sfwp)} artifact files", flush=True)
    except: pass
    print("Joining sector features...", flush=True)
    joined = join_replay_sector_features(replay_rows=rows, sector_mapping=sm, sector_features_with_phase=sfwp)
    jr = joined.get("joined_rows",[])
    print(f"  Joined: {joined['join_ready_count']}/{joined['replay_row_count']} ({joined['join_coverage']*100:.1f}%)", flush=True)
    print("Profiling...", flush=True)
    profiles = profile_joint_segments(joined_rows=jr)
    concentration = audit_sector_concentration(joined_rows=jr)
    stability = audit_temporal_sector_stability(joined_rows=jr)
    range_analysis = analyze_range_bound_drag(joined_rows=jr)
    separability = test_joint_separability(join_coverage=joined.get("join_coverage",0),segment_profiles=profiles,concentration_audit=concentration,temporal_sector_stability=stability,range_bound_analysis=range_analysis)
    candidates = mine_joint_candidates(joint_separability=separability)
    report = {"report_version":"V3512_REGIME_SECTOR_JOINT_ATTRIBUTION_REPORT_V10","mode":"PAPER_ONLY_JOINT_ATTRIBUTION","regime_sector_join":{"total_rows":joined.get("replay_row_count"),"ready_rows":joined.get("join_ready_count"),"join_coverage":joined.get("join_coverage"),"join_status":joined.get("join_status")},"joint_segment_profiles":profiles,"sector_concentration_audit":concentration,"temporal_sector_stability":stability,"range_bound_analysis":range_analysis,"joint_separability":separability,"joint_candidates":candidates,"production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False,"synthetic_sector_index_production_allowed":False,"safety":dict(DEFAULT_REGIME_SECTOR_SAFETY)}
    report["policy_violations"] = validate_joint_attribution_report(report)
    report["attribution_status"] = separability.get("joint_separability_status")
    report["recommended_next_step"] = {"JOINT_ATTRIBUTION_SEPARABLE":"v3.5.13 Regime×Sector Conditional Paper Replay","WEAKLY_JOINT_SEPARABLE":"v3.5.13 Observation Replay","NOT_JOINT_SEPARABLE":"v3.5.13 B-Matrix Reconstruction"}.get(report["attribution_status"],"Fix data")
    out = Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    s = {"attribution_status":report["attribution_status"],"join_coverage":joined["join_coverage"],"separability_status":separability["joint_separability_status"],"separability_score":separability["joint_separability_score"],"scoring":separability["scoring_breakdown"],"concentration":concentration["concentration_status"],"concentration_top":concentration["top_sector_share"],"concentration_top5":concentration["top_5_sector_share"],"temporal_sector":stability["temporal_sector_status"],"candidate_count":candidates["candidate_count"],"recommended_next_step":report["recommended_next_step"],"policy_violations":report["policy_violations"]}
    print(json.dumps(s,ensure_ascii=False,indent=2))
    if report["policy_violations"]: raise SystemExit(3)
    print("v3.5.12 done")

def _float(x):
    try:
        if x in (None,""): return None
        return float(x)
    except: return None

if __name__ == "__main__": main()
