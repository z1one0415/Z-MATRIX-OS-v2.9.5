# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.sector_mapping_ingestion.source_discovery import discover_mapping_sources
from zmatrix.sector_mapping_ingestion.mapping_normalizer import normalize_mapping_sources
from zmatrix.sector_mapping_ingestion.mapping_merger import merge_sector_mappings
from zmatrix.sector_mapping_ingestion.mapping_validator import validate_sector_mapping
from zmatrix.sector_mapping_ingestion.mapping_artifact_writer import write_sector_mapping_artifact
from zmatrix.sector_mapping_ingestion.replay_sector_join_validator import validate_replay_sector_join
from zmatrix.sector_mapping_ingestion.policy import validate_sector_mapping_ingestion_report
from zmatrix.sector_mapping_ingestion.schema import DEFAULT_SECTOR_MAPPING_SAFETY

def build_sector_mapping_ingestion_report(*, data_root=".", replay_rows: list[dict] | None = None, write_artifact=True) -> dict:
    replay_rows = replay_rows or []
    src = discover_mapping_sources(data_root=data_root)
    norm = normalize_mapping_sources(source_files=src.get("source_files",[]))
    merged = merge_sector_mappings(normalized_rows=norm.get("normalized_rows",[]))
    val = validate_sector_mapping(sector_mapping=merged.get("sector_mapping",{}))
    w = write_sector_mapping_artifact(sector_mapping=merged.get("sector_mapping",{})) if write_artifact and merged.get("sector_mapping") else {}
    rj = validate_replay_sector_join(replay_rows=replay_rows, sector_mapping=merged.get("sector_mapping",{}))
    report = {"report_version":"V3510_SECTOR_MAPPING_INGESTION_REPORT_V10","mode":"SECTOR_MAPPING_INGESTION_ONLY","source_discovery":src,"mapping_normalizer":{"normalized_count":norm.get("normalized_count")},"mapping_merger":{"merged_count":merged.get("merged_count"),"sector_ready_count":merged.get("sector_ready_count")},"mapping_validator":val,"mapping_artifact_writer":w,"replay_sector_join_validator":rj,"production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"runtime_enabled":False,"production_yaml_write_allowed":False,"production_parameter_write_allowed":False,"production_weight_adjustment_allowed":False,"synthetic_sector_index_production_allowed":False,"safety":dict(DEFAULT_SECTOR_MAPPING_SAFETY)}
    report["policy_violations"] = validate_sector_mapping_ingestion_report(report)
    ms = val.get("sector_mapping_status"); js = rj.get("join_status")
    report["ingestion_status"] = "SECTOR_MAPPING_READY" if ms=="READY" and js=="READY" else "SECTOR_MAPPING_PARTIAL" if ms in ("READY","PARTIAL") and js in ("READY","PARTIAL") else "SECTOR_MAPPING_DATA_INSUFFICIENT"
    report["recommended_next_step"] = {"SECTOR_MAPPING_READY":"v3.5.11 Synthetic Sector Basket / Sector Index Builder","SECTOR_MAPPING_PARTIAL":"v3.5.11 Sector Mapping Coverage Repair"}.get(report["ingestion_status"],"Provide local stock_basic / industry mapping data before continuing")
    return report
