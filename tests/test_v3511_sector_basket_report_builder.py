from zmatrix.synthetic_sector_index.sector_basket_report_builder import build_synthetic_sector_basket_report
def test_report(): r=build_synthetic_sector_basket_report(data_root=".",replay_rows=[],write_artifacts=False); assert r["policy_violations"]==[]; assert r["real_trade_allowed"]==False
