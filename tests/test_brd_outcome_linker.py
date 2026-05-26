"""Outcome Linker tests"""
import sys,os,tempfile,csv; sys.path.insert(0,'.')
from pathlib import Path
from zmatrix.brd_replay.outcome_linker import build_outcome_for_paper_action

def _write(path):
    path.parent.mkdir(parents=True,exist_ok=True)
    with open(path,"w",newline="",encoding="utf-8") as f:
        csv.writer(f).writerows([["trade_date","close"]]+[[f"2024{601+i:02d}",str(10+i*0.1)] for i in range(30)])

def test_outcome_linker():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        _write(root/"data"/"price_bars"/"000001.csv")
        r = build_outcome_for_paper_action(paper_action={"paper_id":"p1","ticker":"000001","entry_date":"2024-06-01","entry_price":10,
            "paper_action":"PAPER_WATCH_CORE","max_loss_plan":8},local_data_root=str(root))
        assert r["outcome_status"] == "READY"
        assert r["real_trade_allowed"] is False

if __name__ == "__main__":
    test_outcome_linker()
    print("\n🏁 Outcome Linker PASS")
