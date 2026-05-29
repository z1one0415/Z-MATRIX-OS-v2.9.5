#!/usr/bin/env python3
"""ZC Numbering & User Manual Patch Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_user_manual_exists_and_contains_all_zc_codes():
    manual = read("docs/manuals/ZMATRIX_USER_OPERATION_MANUAL_V1.md")
    for zc in ["ZC00", "ZC10", "ZC20", "ZC30", "ZC31", "ZC32", "ZC35", "ZC40", "ZC45", "ZC50", "ZSC"]:
        assert zc in manual, f"manual missing {zc}"


def test_zc_numbering_map_exists():
    zcmap = read("docs/architecture/ZC_NUMBERING_MAP_V1.md")
    for zc in ["ZC00", "ZC10", "ZC20", "ZC30", "ZC31", "ZC32", "ZC35", "ZC40", "ZC45", "ZC50", "ZSC"]:
        assert zc in zcmap, f"map missing {zc}"


def test_content_asset_index_synchronized_to_post_rc1():
    asset = read("docs/upgrade/V40_CONTENT_ASSET_INDEX.md")
    assert "V4.0-RC1_TAGGED_RESEARCH_ONLY" in asset
    assert "Release tag: v4.0-rc1" in asset
    assert "Production status: BLOCKED" in asset
    assert "Broker/runtime status: BLOCKED" in asset
    assert "Real trade status: BLOCKED" in asset


def test_zc30_multistrategy_is_deprecated():
    asset = read("docs/upgrade/V40_CONTENT_ASSET_INDEX.md")
    assert "ZC31_MULTI_STRATEGY_SLEEVE" in asset
    if "ZC30_MULTI_STRATEGY" in asset:
        assert "DEPRECATED_ALIAS_OF_ZC31" in asset


def test_autocaseforge_is_not_claimed_as_implemented():
    manual = read("docs/manuals/ZMATRIX_USER_OPERATION_MANUAL_V1.md")
    asset = read("docs/upgrade/V40_CONTENT_ASSET_INDEX.md")
    combined = manual + asset
    assert "AUTOCASEFORGE_V10" in asset
    assert "PLANNED_NOT_IMPLEMENTED" in asset or "AutoCaseForge" in manual
    assert "AutoCaseForge = IMPLEMENTED" not in combined


def test_zc35_v21_excluded_from_rc1():
    manual = read("docs/manuals/ZMATRIX_USER_OPERATION_MANUAL_V1.md")
    asset = read("docs/upgrade/V40_CONTENT_ASSET_INDEX.md")
    assert "ZC35_V21_RESEARCH_PROTOTYPE" in asset
    assert "ZC35-v2.1" in manual
    assert "ZC35-v2.1 = RC1" not in manual + asset


def test_no_forbidden_release_status():
    combined = "\n".join([
        read("docs/manuals/ZMATRIX_USER_OPERATION_MANUAL_V1.md"),
        read("docs/architecture/ZC_NUMBERING_MAP_V1.md"),
        read("docs/upgrade/V40_CONTENT_ASSET_INDEX.md"),
        read("docs/release/ZC_NUMBERING_USER_MANUAL_PATCH_CLOSEOUT.md"),
    ])
    for forbidden in [
        "Production status: READY",
        "RC1 status: APPROVED",
        "Broker/runtime status: READY",
        "Real trade status: READY",
        "Tag moved: true",
        "Tag retagged: true",
    ]:
        assert forbidden not in combined, f"Forbidden: {forbidden}"


if __name__ == "__main__":
    test_user_manual_exists_and_contains_all_zc_codes()
    test_zc_numbering_map_exists()
    test_content_asset_index_synchronized_to_post_rc1()
    test_zc30_multistrategy_is_deprecated()
    test_autocaseforge_is_not_claimed_as_implemented()
    test_zc35_v21_excluded_from_rc1()
    test_no_forbidden_release_status()
    print("✅ ZC Numbering & User Manual Patch tests PASS")
