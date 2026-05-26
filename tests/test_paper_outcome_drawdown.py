"""Drawdown Calculator tests — entry-relative MAE"""
import sys,os; sys.path.insert(0,'.')
from zmatrix.paper_outcome.drawdown_calculator import calc_max_drawdown, calc_entry_relative_drawdown

def test_calc_max_drawdown():
    dd = calc_max_drawdown([50,55,60,45,50,65])
    assert dd is not None and dd > 0
    print(f"✅ peak_dd={dd}%")

def test_entry_relative_mae():
    mae = calc_entry_relative_drawdown(50.0, [50,55,52,48,45,51])
    assert mae["max_adverse_excursion_pct"] == -10.0  # 45 vs 50 entry = -10%
    assert mae["max_gain_before_loss_pct"] == 10.0  # 55 vs 50 entry = +10%
    print(f"✅ entry MAE={mae['max_adverse_excursion_pct']}%")

def test_fake_winner_detection():
    mae = calc_entry_relative_drawdown(50.0, [50,56,55,54,49,48])  # peaked at +12%, ended at -4%
    assert mae["is_fake_winner"] is True
    print("✅ fake winner detected")

if __name__ == "__main__":
    test_calc_max_drawdown()
    test_entry_relative_mae()
    test_fake_winner_detection()
    print("\n🏁 Drawdown PASS")
