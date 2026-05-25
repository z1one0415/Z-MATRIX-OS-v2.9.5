"""Sector Stage contract tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.investment.sector_stage import detect_sector_stage, SECTOR_STAGES

def test_unknown_default():
    r = detect_sector_stage({"ticker": "002472"})
    assert r["sector_stage"] == "UNKNOWN"
    assert r["mid_rotation_allowed"] is False
    print("✅ sector_stage: UNKNOWN default")


def test_confirmation_allows_mid():
    r = detect_sector_stage({"ticker": "002472", "sector_stage": "CONFIRMATION"})
    assert r["mid_rotation_allowed"] is True
    assert r["new_position_allowed"] is True
    print("✅ sector_stage: CONFIRMATION → rotation allowed")


def test_retreat_blocks_new():
    r = detect_sector_stage({"ticker": "002472", "sector_stage": "RETREAT"})
    assert r["mid_rotation_allowed"] is False
    assert r["new_position_allowed"] is False
    print("✅ sector_stage: RETREAT → no new positions")


def test_climax_no_new():
    r = detect_sector_stage({"ticker": "002472", "sector_stage": "CLIMAX"})
    assert r["new_position_allowed"] is False
    print("✅ sector_stage: CLIMAX → no new positions")


if __name__ == "__main__":
    test_unknown_default(); test_confirmation_allows_mid(); test_retreat_blocks_new(); test_climax_no_new()
    print("\n🏁 Sector Stage — tests PASS")
