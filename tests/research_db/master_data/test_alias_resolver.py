#!/usr/bin/env python3
"""Phase 2-B: Alias Resolver Tests."""
from __future__ import annotations

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from zmatrix.research_db.master_data import AliasType
from zmatrix.research_db.master_data.alias_resolver import AliasRegistry

FIXTURE_DIR = Path(__file__).resolve().parent.parent.parent / "fixtures" / "master_data"
ALIAS_CSV = str(FIXTURE_DIR / "sample_ticker_alias.csv")


def test_resolve_alias_english_name():
    reg = AliasRegistry(ALIAS_CSV)
    assert reg.resolve_alias("MOUTAI") == "600519"


def test_resolve_alias_short_name():
    reg = AliasRegistry(ALIAS_CSV)
    assert reg.resolve_alias("茅台") == "600519"


def test_resolve_alias_not_found():
    reg = AliasRegistry(ALIAS_CSV)
    assert reg.resolve_alias("NONEXISTENT") is None


def test_get_aliases():
    reg = AliasRegistry(ALIAS_CSV)
    aliases = reg.get_aliases("600519")
    assert len(aliases) == 2
    alias_strs = {a.alias for a in aliases}
    assert alias_strs == {"MOUTAI", "茅台"}


def test_get_aliases_no_aliases():
    reg = AliasRegistry(ALIAS_CSV)
    assert reg.get_aliases("999999") == []


def test_add_alias():
    reg = AliasRegistry(ALIAS_CSV)
    reg.add_alias("600519", "贵州", "SHORT_NAME")
    assert reg.resolve_alias("贵州") == "600519"
    aliases = reg.get_aliases("600519")
    assert any(a.alias == "贵州" for a in aliases)


def test_add_alias_new_ticker():
    reg = AliasRegistry(ALIAS_CSV)
    reg.add_alias("999999", "TEST", "ENGLISH_NAME")
    assert reg.resolve_alias("TEST") == "999999"


def test_empty_registry():
    reg = AliasRegistry()
    assert reg.resolve_alias("ANYTHING") is None
    assert reg.get_aliases("600519") == []


def test_all_aliases_production_allowed_false():
    reg = AliasRegistry(ALIAS_CSV)
    for ticker in ["600519", "002472", "688981"]:
        for alias in reg.get_aliases(ticker):
            assert alias.production_allowed is False


if __name__ == "__main__":
    test_resolve_alias_english_name()
    test_resolve_alias_short_name()
    test_resolve_alias_not_found()
    test_get_aliases()
    test_get_aliases_no_aliases()
    test_add_alias()
    test_add_alias_new_ticker()
    test_empty_registry()
    test_all_aliases_production_allowed_false()
    print("✅ Phase 2-B Alias Resolver tests PASS")
