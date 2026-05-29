# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.synthetic_sector_index.sector_mapping_loader import load_sector_mapping
from zmatrix.synthetic_sector_index.sector_return_builder import build_sector_daily_returns
from zmatrix.synthetic_sector_index.sector_index_builder import build_synthetic_sector_indexes
from zmatrix.synthetic_sector_index.market_benchmark_loader import load_market_benchmark
from zmatrix.synthetic_sector_index.sector_feature_builder import build_sector_features
from zmatrix.synthetic_sector_index.sector_phase_classifier import add_sector_phases
from zmatrix.synthetic_sector_index.replay_sector_feature_joiner import join_replay_sector_features
from zmatrix.synthetic_sector_index.sector_index_artifact_writer import write_sector_index_artifacts
from zmatrix.synthetic_sector_index.policy import validate_synthetic_sector_report
from zmatrix.synthetic_sector_index.schema import DEFAULT_SYNTHETIC_SECTOR_SAFETY

def build_synthetic_sector_basket_report(*, data_root=".", replay_rows=None, mapping_path="data/metadata/sector_mapping_v3510.csv", write_artifacts=True) -> dict:
    replay_rows = replay_rows or []
    mapping = load_sector_mapping(mapping_path=mapping_path)
    returns = build_sector_daily_returns(sector_mapping=mapping.get("sector_mapping",{}), data_root=data_root)
    indexes = build_synthetic_sector_indexes(sector_daily_returns=returns.get("sector_daily_returns",{}))
    benchmark = load_market_benchmark(data_root=data_root)
    features = build_sector_features(sector_indexes=indexes.get("sector_indexes",{}), benchmark_bars=benchmark.get("bars",[]))
    phases = add_sector_phases(sector_features=features.get("sector_features",{}))
    joined = join_replay_sector_features(replay_rows=replay_rows, sector_mapping=mapping.get("sector_mapping",{}), sector_features_with_phase=phases.get("sector_features_with_phase",{}))
    w = write_sector_index_artifacts(sector_features_with_phase=phases.get("sector_features_with_phase",{})) if write_artifacts else {}
    report = {"report_version":"V3511_SYNTHETIC_SECTOR_BASKET_REPORT_V10","mode":"PAPER_ONLY_SYNTHETIC_SECTOR_INDEX","sector_mapping_loader":{"load_status":mapping.get("load_status"),"ticker_count":mapping.get("ticker_count"),"sector_count":mapping.get("sector_count")},"sector_daily_return_builder":{"sector_count":returns.get("sector_count"),"missing_price_file_count":returns.get("missing_price_file_count")},"synthetic_sector_index_builder":{"sector_index_count":indexes.get("sector_index_count"),"synthetic_sector_index":True,"production_index_allowed":False},"market_benchmark_loader":{"benchmark_status":benchmark.get("benchmark_status"),"benchmark_code":benchmark.get("benchmark_code")},"sector_feature_builder":{"sector_feature_count":features.get("sector_feature_count")},"sector_phase_builder":{"sector_phase_count":phases.get("sector_phase_count")},"replay_sector_feature_joiner":{"replay_row_count":joined.get("replay_row_count"),"join_ready_count":joined.get("join_ready_count"),"join_coverage":joined.get("join_coverage"),"join_status":joined.get("join_status")},"sector_index_artifact_writer":w,"production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False,"production_yaml_write_allowed":False,"production_parameter_write_allowed":False,"synthetic_sector_index_production_allowed":False,"safety":dict(DEFAULT_SYNTHETIC_SECTOR_SAFETY)}
    report["policy_violations"] = validate_synthetic_sector_report(report)
    js = joined.get("join_status"); sic = indexes.get("sector_index_count",0)
    report["basket_status"] = "SYNTHETIC_SECTOR_BASKET_READY" if js=="READY" and sic>0 else "SYNTHETIC_SECTOR_BASKET_PARTIAL" if js=="PARTIAL" else "DATA_INSUFFICIENT"
    report["recommended_next_step"] = {"SYNTHETIC_SECTOR_BASKET_READY":"v3.5.12 Regime × Sector Joint Attribution","SYNTHETIC_SECTOR_BASKET_PARTIAL":"v3.5.12 Sector Basket Coverage Repair"}.get(report["basket_status"],"Fix sector basket data")
    return report
