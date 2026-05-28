from zmatrix.synthetic_sector_index.sector_return_builder import build_sector_daily_returns
from zmatrix.synthetic_sector_index.sector_mapping_loader import load_sector_mapping
def test_returns(): m=load_sector_mapping(); r=build_sector_daily_returns(sector_mapping=m["sector_mapping"],data_root="."); assert r["sector_count"]>50
