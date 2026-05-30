#!/usr/bin/env python3
"""Phase 2-B.1: Schema Alignment Tests — verify master_schema.py + standard fields + re-export."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent


def test_master_schema_py_exists():
    assert (WORKSPACE / "zmatrix" / "research_db" / "master_data" / "master_schema.py").exists()


def test_init_is_re_export_shim():
    init = (WORKSPACE / "zmatrix" / "research_db" / "master_data" / "__init__.py").read_text()
    assert "from .master_schema import" in init
    assert "__all__" in init


def test_import_from_master_data_works():
    from zmatrix.research_db.master_data import SecurityMaster, Exchange, DataStatus, QualityStatus, AssetType
    assert SecurityMaster is not None
    assert DataStatus.SYNTHETIC_FIXTURE.value == "SYNTHETIC_FIXTURE"


def test_security_master_has_phase2_standard_fields():
    from zmatrix.research_db.master_data import SecurityMaster, Exchange, AssetType
    sm = SecurityMaster(
        ticker="600519", name="Kweichow Moutai", exchange=Exchange.SSE,
        board="MAIN", asset_type=AssetType.STOCK,
        list_date="2001-08-27", currency="CNY", country="CN",
        data_status="PUBLIC_REFERENCE", quality_status="VALIDATED",
        source_file="sample_fixture.csv", version=1,
        effective_from="2024-01-01",
    )
    assert sm.board == "MAIN"
    assert sm.list_date == "2001-08-27"
    assert sm.currency == "CNY"
    assert sm.country == "CN"
    assert sm.data_status == "PUBLIC_REFERENCE"
    assert sm.quality_status == "VALIDATED"
    assert sm.source_file == "sample_fixture.csv"


def test_backward_compatible_aliases():
    from zmatrix.research_db.master_data import SecurityMaster, Exchange
    sm = SecurityMaster(ticker="600519", name="MT", exchange=Exchange.SSE, list_date="2001-08-27", list_status="LISTED")
    assert sm.listing_date == "2001-08-27"
    assert sm.listing_status == "LISTED"


def test_production_allowed_blocked_even_when_true_passed():
    from zmatrix.research_db.master_data import SecurityMaster, Exchange
    sm = SecurityMaster(ticker="X", name="X", exchange=Exchange.SSE, production_allowed=True)  # type: ignore
    assert sm.production_allowed is False


def test_data_status_enum_values():
    from zmatrix.research_db.master_data import DataStatus
    assert len(list(DataStatus)) >= 5
    assert DataStatus.SYNTHETIC_FIXTURE.value == "SYNTHETIC_FIXTURE"
    assert DataStatus.VENDOR_EXPORT.value == "VENDOR_EXPORT"


def test_quality_status_enum_values():
    from zmatrix.research_db.master_data import QualityStatus
    assert len(list(QualityStatus)) >= 4
    assert QualityStatus.VALIDATED.value == "VALIDATED"
    assert QualityStatus.BLOCKED.value == "BLOCKED"


def test_asset_type_enum_values():
    from zmatrix.research_db.master_data import AssetType
    assert len(list(AssetType)) >= 5
    assert AssetType.STOCK.value == "STOCK"
    assert AssetType.ETF.value == "ETF"


def test_security_master_has_governance_fields():
    from zmatrix.research_db.master_data import SecurityMaster, Exchange
    sm = SecurityMaster(ticker="X", name="X", exchange=Exchange.SSE)
    for f in ["data_status", "quality_status", "source_file", "version", "effective_from", "effective_to"]:
        assert hasattr(sm, f), f"missing field: {f}"


def test_security_master_has_board_field():
    from zmatrix.research_db.master_data import SecurityMaster, Exchange
    sm = SecurityMaster(ticker="X", name="X", exchange=Exchange.SSE, board="MAIN")
    assert sm.board == "MAIN"


def test_existing_p2a_tests_still_importable():
    from zmatrix.research_db.master_data import (
        Exchange, ListingStatus, AliasType, Confidence,
        SecurityMaster, TickerAlias, IndustryMapping,
        SectorMapping, ChainTaxonomy, ChainNodeMapping,
    )
    assert len(list(Exchange)) >= 3
    assert len(list(ListingStatus)) >= 3


if __name__ == "__main__":
    import pytest; pytest.main([__file__, "-v"])
