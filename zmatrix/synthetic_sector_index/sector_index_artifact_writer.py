# allowlist: forbidden-token-definition
from __future__ import annotations
import csv
from pathlib import Path
from zmatrix.synthetic_sector_index.schema import DEFAULT_SYNTHETIC_SECTOR_SAFETY

def write_sector_index_artifacts(*, sector_features_with_phase: dict, output_dir="runtime_reports/sector_baskets_v3511", max_git_bytes=5_000_000) -> dict:
    od = Path(output_dir); od.mkdir(parents=True,exist_ok=True)
    files=[]; ts=0; fields=["sector","trade_date","close_index","sector_return_1d","sector_return_5d","sector_return_20d","sector_return_60d","sector_phase","sector_relative_strength_vs_market","active_member_count","active_member_ratio","data_quality_status"]
    for sector,rows in (sector_features_with_phase or {}).items():
        safe=str(sector).replace("/","_").replace(" ","_"); p=od/f"{safe}.csv"
        with open(p,"w",encoding="utf-8-sig",newline="") as f:
            w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
            for r in rows: w.writerow({k:r.get(k) for k in fields})
        sz=p.stat().st_size; ts+=sz; files.append(str(p))
    return {"writer_version":"V3511_SECTOR_INDEX_ARTIFACT_WRITER_V10","output_dir":output_dir,"file_count":len(files),"total_size_bytes":ts,"git_track_allowed":ts<=max_git_bytes and not output_dir.startswith("runtime_reports"),"production_index_allowed":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SYNTHETIC_SECTOR_SAFETY)}
