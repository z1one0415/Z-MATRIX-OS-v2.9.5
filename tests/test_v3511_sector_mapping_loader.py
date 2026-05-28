from zmatrix.synthetic_sector_index.sector_mapping_loader import load_sector_mapping
def test_mapping_loaded(): r=load_sector_mapping(); assert r["load_status"]=="READY"; assert r["ticker_count"]>5000
