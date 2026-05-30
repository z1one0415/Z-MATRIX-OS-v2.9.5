"""Data Supply tests — connector registry, reliability, PIT store, lineage, corporate actions."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import pytest

from zmatrix.research_db.data_supply.connector_registry import ConnectorEntry, ConnectorRegistry, SUPPORTED_SOURCES
from zmatrix.research_db.data_supply.source_reliability import SourceReliabilityTracker
from zmatrix.research_db.data_supply.pit_store import PITRecord, PITStore
from zmatrix.research_db.data_supply.data_lineage import LineageEntry, DataLineage
from zmatrix.research_db.data_supply.corporate_actions import CorporateAction, ActionType, adjust_price


# ============ ConnectorEntry tests ============

class TestConnectorEntry:
    def test_create_valid_entry(self):
        e = ConnectorEntry(source="akshare", module_path="a.b", class_name="Foo")
        assert e.source == "akshare"
        assert e.module_path == "a.b"
        assert e.class_name == "Foo"
        assert e.enabled is True
        assert e.priority == 0
        assert e.metadata == {}

    def test_default_production_allowed_false(self):
        e = ConnectorEntry(source="tushare", module_path="x", class_name="Y")
        assert e.production_allowed is False

    def test_rejects_unsupported_source(self):
        with pytest.raises(ValueError, match="Unsupported source"):
            ConnectorEntry(source="invalid_src", module_path="x", class_name="Y")

    def test_metadata_defaults_to_empty_dict(self):
        e = ConnectorEntry(source="yahoo", module_path="y", class_name="Z", metadata={"key": "val"})
        assert e.metadata == {"key": "val"}

    def test_priority_settable(self):
        e = ConnectorEntry(source="fred", module_path="f", class_name="G", priority=5)
        assert e.priority == 5

    def test_disabled_entry(self):
        e = ConnectorEntry(source="stooq", module_path="s", class_name="T", enabled=False)
        assert e.enabled is False


# ============ ConnectorRegistry tests ============

class TestConnectorRegistry:
    def test_registry_initialized_empty(self):
        r = ConnectorRegistry()
        assert r.count() == 0

    def test_register_entry(self):
        r = ConnectorRegistry()
        rid = r.register(ConnectorEntry(source="akshare", module_path="a.b", class_name="Foo"))
        assert rid == "akshare:Foo"
        assert r.count() == 1
        assert r.count("akshare") == 1

    def test_register_multiple_same_source(self):
        r = ConnectorRegistry()
        r.register(ConnectorEntry(source="akshare", module_path="a", class_name="One"))
        r.register(ConnectorEntry(source="akshare", module_path="b", class_name="Two"))
        assert r.count("akshare") == 2
        assert r.count() == 2

    def test_register_multiple_sources(self):
        r = ConnectorRegistry()
        r.register(ConnectorEntry(source="akshare", module_path="a", class_name="A"))
        r.register(ConnectorEntry(source="tushare", module_path="t", class_name="T"))
        assert r.count("akshare") == 1
        assert r.count("tushare") == 1
        assert r.count() == 2

    def test_get_by_class_name_returns_entry(self):
        r = ConnectorRegistry()
        r.register(ConnectorEntry(source="akshare", module_path="a.b", class_name="Foo"))
        e = r.get("akshare", "Foo")
        assert e is not None
        assert e.class_name == "Foo"

    def test_get_returns_none_for_missing(self):
        r = ConnectorRegistry()
        assert r.get("akshare", "NoExist") is None

    def test_get_returns_list_without_class_name(self):
        r = ConnectorRegistry()
        r.register(ConnectorEntry(source="akshare", module_path="a", class_name="One"))
        r.register(ConnectorEntry(source="akshare", module_path="b", class_name="Two"))
        result = r.get("akshare")
        assert isinstance(result, list)
        assert len(result) == 2

    def test_get_none_for_unknown_source(self):
        r = ConnectorRegistry()
        assert r.get("nonexistent") is None

    def test_count_zero_for_unknown_source(self):
        r = ConnectorRegistry()
        assert r.count("nonexistent") == 0

    def test_list_all_sorted_by_priority(self):
        r = ConnectorRegistry()
        r.register(ConnectorEntry(source="akshare", module_path="a", class_name="Low", priority=0))
        r.register(ConnectorEntry(source="yahoo", module_path="y", class_name="High", priority=10))
        r.register(ConnectorEntry(source="fred", module_path="f", class_name="Mid", priority=5))
        entries = r.list_all()
        assert entries[0].class_name == "High"
        assert entries[1].class_name == "Mid"

    def test_list_sources_returns_six(self):
        r = ConnectorRegistry()
        sources = r.list_sources()
        assert len(sources) == 6
        for s in ["akshare", "tushare", "baostock", "yahoo", "fred", "stooq"]:
            assert s in sources

    def test_rejects_register_unsupported_source(self):
        r = ConnectorRegistry()
        with pytest.raises(ValueError, match="Unsupported source"):
            r.register(ConnectorEntry(source="bogus", module_path="x", class_name="Y"))


# ============ SourceReliabilityTracker tests ============

class TestSourceReliabilityTracker:
    def test_initial_state(self):
        t = SourceReliabilityTracker(source="akshare")
        assert t.source == "akshare"
        assert t.success_count == 0
        assert t.failure_count == 0
        assert t.total_attempts == 0
        assert t.compute_score() == 1.0

    def test_production_allowed_false(self):
        t = SourceReliabilityTracker(source="yahoo")
        assert t.production_allowed is False

    def test_record_success_increments(self):
        t = SourceReliabilityTracker(source="tushare")
        t.record_success()
        assert t.success_count == 1
        assert t.total_attempts == 1

    def test_record_failure_increments(self):
        t = SourceReliabilityTracker(source="baostock")
        t.record_failure()
        assert t.failure_count == 1
        assert t.total_attempts == 1

    def test_compute_score_perfect(self):
        t = SourceReliabilityTracker(source="fred")
        t.record_success()
        t.record_success()
        assert t.compute_score() == 1.0

    def test_compute_score_mixed(self):
        t = SourceReliabilityTracker(source="stooq")
        t.record_success()
        t.record_failure()
        t.record_success()
        assert t.compute_score() == 2.0 / 3.0

    def test_reliability_property(self):
        t = SourceReliabilityTracker(source="akshare")
        t.record_success()
        t.record_failure()
        assert t.reliability == 0.5

    def test_is_healthy_true(self):
        t = SourceReliabilityTracker(source="yahoo")
        for _ in range(9):
            t.record_success()
        t.record_failure()
        assert t.is_healthy is True

    def test_is_healthy_false(self):
        t = SourceReliabilityTracker(source="tushare")
        t.record_success()
        for _ in range(5):
            t.record_failure()
        assert t.is_healthy is False

    def test_last_success_timestamp(self):
        t = SourceReliabilityTracker(source="baostock")
        t.record_success("2025-01-01T00:00:00Z")
        assert t.last_success == "2025-01-01T00:00:00Z"

    def test_last_failure_timestamp(self):
        t = SourceReliabilityTracker(source="fred")
        t.record_failure("2025-06-01T12:00:00Z")
        assert t.last_failure == "2025-06-01T12:00:00Z"

    def test_reset_clears_all(self):
        t = SourceReliabilityTracker(source="stooq")
        t.record_success()
        t.record_failure()
        t.reset()
        assert t.success_count == 0
        assert t.failure_count == 0
        assert t.total_attempts == 0
        assert t.last_success == ""
        assert t.last_failure == ""
        assert t.compute_score() == 1.0


# ============ PITRecord / PITStore tests ============

class TestPITRecord:
    def test_create_pit_record(self):
        r = PITRecord(ticker="000001", field_name="close", value=12.5, snapshot_date="2025-01-15")
        assert r.ticker == "000001"
        assert r.field_name == "close"
        assert r.value == 12.5
        assert r.snapshot_date == "2025-01-15"

    def test_production_allowed_false(self):
        r = PITRecord(ticker="X", field_name="Y", value=1.0, snapshot_date="2025-01-01")
        assert r.production_allowed is False

    def test_has_recorded_at(self):
        r = PITRecord(ticker="A", field_name="B", value=0.0, snapshot_date="2025-01-01")
        assert r.recorded_at != ""


class TestPITStore:
    def test_store_starts_empty(self):
        s = PITStore()
        assert s.count() == 0

    def test_add_record_returns_pit_record(self):
        s = PITStore()
        r = s.add_record("000001", "close", 10.0, "2025-01-01")
        assert isinstance(r, PITRecord)
        assert s.count() == 1

    def test_query_as_of_exact_match(self):
        s = PITStore()
        s.add_record("000001", "close", 10.0, "2025-01-10")
        results = s.query_as_of("000001", "close", "2025-01-10")
        assert len(results) == 1
        assert results[0].value == 10.0

    def test_query_as_of_later_date_includes_earlier(self):
        s = PITStore()
        s.add_record("000001", "close", 10.0, "2025-01-10")
        s.add_record("000001", "close", 11.0, "2025-01-12")
        results = s.query_as_of("000001", "close", "2025-01-15")
        assert len(results) == 2

    def test_query_as_of_blocks_future_access(self):
        s = PITStore()
        s.add_record("000001", "close", 10.0, "2025-01-20")
        results = s.query_as_of("000001", "close", "2025-01-10")
        assert len(results) == 0

    def test_query_as_of_wrong_ticker(self):
        s = PITStore()
        s.add_record("000001", "close", 10.0, "2025-01-10")
        results = s.query_as_of("000002", "close", "2025-01-15")
        assert len(results) == 0

    def test_query_as_of_wrong_field(self):
        s = PITStore()
        s.add_record("000001", "close", 10.0, "2025-01-10")
        results = s.query_as_of("000001", "open", "2025-01-15")
        assert len(results) == 0

    def test_get_latest_returns_most_recent(self):
        s = PITStore()
        s.add_record("000001", "close", 10.0, "2025-01-01")
        s.add_record("000001", "close", 12.0, "2025-01-03")
        s.add_record("000001", "close", 11.0, "2025-01-02")
        latest = s.get_latest("000001", "close", "2025-01-10")
        assert latest is not None
        assert latest.value == 12.0

    def test_get_latest_blocks_future(self):
        s = PITStore()
        s.add_record("000001", "close", 10.0, "2025-01-10")
        assert s.get_latest("000001", "close", "2025-01-05") is None

    def test_get_latest_no_records(self):
        s = PITStore()
        assert s.get_latest("000001", "close", "2025-01-10") is None

    def test_list_all_returns_all(self):
        s = PITStore()
        s.add_record("A", "x", 1.0, "2025-01-01")
        s.add_record("B", "y", 2.0, "2025-01-02")
        assert len(s.list_all()) == 2


# ============ LineageEntry / DataLineage tests ============

class TestLineageEntry:
    def test_create_lineage_entry(self):
        e = LineageEntry(factor_id="F1", source="akshare", transform="raw")
        assert e.factor_id == "F1"
        assert e.source == "akshare"
        assert e.transform == "raw"
        assert e.input_fields == []
        assert e.output_field == ""
        assert e.upstream_factor_ids == []

    def test_production_allowed_false(self):
        e = LineageEntry(factor_id="F1", source="y", transform="z")
        assert e.production_allowed is False

    def test_with_upstream(self):
        e = LineageEntry(factor_id="F2", source="tushare", transform="calc",
                         input_fields=["close"], output_field="sma",
                         upstream_factor_ids=["F1"])
        assert "F1" in e.upstream_factor_ids
        assert e.input_fields == ["close"]
        assert e.output_field == "sma"


class TestDataLineage:
    def test_starts_empty(self):
        dl = DataLineage()
        assert dl.count() == 0

    def test_add_entry(self):
        dl = DataLineage()
        fid = dl.add_entry(LineageEntry(factor_id="F1", source="akshare", transform="raw"))
        assert fid == "F1"
        assert dl.count() == 1

    def test_get_entry(self):
        dl = DataLineage()
        dl.add_entry(LineageEntry(factor_id="F1", source="a", transform="b"))
        e = dl.get_entry("F1")
        assert e is not None
        assert e.factor_id == "F1"

    def test_get_entry_missing(self):
        dl = DataLineage()
        assert dl.get_entry("NOPE") is None

    def test_trace_leaf_node(self):
        dl = DataLineage()
        dl.add_entry(LineageEntry(factor_id="F1", source="akshare", transform="raw"))
        trace = dl.trace("F1")
        assert len(trace) == 1
        assert trace[0].factor_id == "F1"

    def test_trace_missing_returns_empty(self):
        dl = DataLineage()
        assert dl.trace("NOPE") == []

    def test_trace_chain_of_three(self):
        dl = DataLineage()
        dl.add_entry(LineageEntry(factor_id="F1", source="akshare", transform="raw"))
        dl.add_entry(LineageEntry(factor_id="F2", source="derived", transform="calc",
                                   upstream_factor_ids=["F1"]))
        dl.add_entry(LineageEntry(factor_id="F3", source="derived", transform="smooth",
                                   upstream_factor_ids=["F2"]))
        trace = dl.trace("F3")
        ids = {e.factor_id for e in trace}
        assert ids == {"F1", "F2", "F3"}

    def test_trace_branching_dag(self):
        dl = DataLineage()
        dl.add_entry(LineageEntry(factor_id="RAW", source="akshare", transform="raw"))
        dl.add_entry(LineageEntry(factor_id="SMA", source="calc", transform="sma",
                                   upstream_factor_ids=["RAW"]))
        dl.add_entry(LineageEntry(factor_id="EMA", source="calc", transform="ema",
                                   upstream_factor_ids=["RAW"]))
        dl.add_entry(LineageEntry(factor_id="MACD", source="calc", transform="macd",
                                   upstream_factor_ids=["SMA", "EMA"]))
        trace = dl.trace("MACD")
        ids = {e.factor_id for e in trace}
        assert ids == {"RAW", "SMA", "EMA", "MACD"}

    def test_downstream_returns_children(self):
        dl = DataLineage()
        dl.add_entry(LineageEntry(factor_id="F1", source="a", transform="x"))
        dl.add_entry(LineageEntry(factor_id="F2", source="b", transform="y",
                                   upstream_factor_ids=["F1"]))
        children = dl.downstream("F1")
        assert children == ["F2"]

    def test_downstream_empty_for_leaf(self):
        dl = DataLineage()
        dl.add_entry(LineageEntry(factor_id="F1", source="a", transform="x"))
        dl.add_entry(LineageEntry(factor_id="F2", source="b", transform="y",
                                   upstream_factor_ids=["F1"]))
        assert dl.downstream("F2") == []

    def test_list_all_returns_entries(self):
        dl = DataLineage()
        dl.add_entry(LineageEntry(factor_id="F1", source="a", transform="x"))
        dl.add_entry(LineageEntry(factor_id="F2", source="b", transform="y"))
        assert len(dl.list_all()) == 2


# ============ CorporateAction tests ============

class TestCorporateAction:
    def test_create_dividend_action(self):
        a = CorporateAction(ticker="000001", action_type=ActionType.DIVIDEND,
                            ex_date="2025-06-01", cash_per_share=0.5)
        assert a.action_type == ActionType.DIVIDEND
        assert a.cash_per_share == 0.5

    def test_production_allowed_false(self):
        a = CorporateAction(ticker="X", action_type=ActionType.SPLIT, ex_date="2025-01-01")
        assert a.production_allowed is False


class TestAdjustPrice:
    def test_split_forward(self):
        a = CorporateAction(ticker="X", action_type=ActionType.SPLIT,
                            ex_date="2025-01-01", ratio=2.0)
        assert a.adjust_price(100.0, forward=True) == 50.0

    def test_split_backward(self):
        a = CorporateAction(ticker="X", action_type=ActionType.SPLIT,
                            ex_date="2025-01-01", ratio=2.0)
        assert a.adjust_price(50.0, forward=False) == 100.0

    def test_dividend_forward(self):
        a = CorporateAction(ticker="X", action_type=ActionType.DIVIDEND,
                            ex_date="2025-01-01", cash_per_share=2.0)
        assert a.adjust_price(50.0, forward=True) == 48.0

    def test_dividend_backward(self):
        a = CorporateAction(ticker="X", action_type=ActionType.DIVIDEND,
                            ex_date="2025-01-01", cash_per_share=2.0)
        assert a.adjust_price(48.0, forward=False) == 50.0

    def test_bonus_forward(self):
        a = CorporateAction(ticker="X", action_type=ActionType.BONUS,
                            ex_date="2025-01-01", ratio=0.5)
        assert a.adjust_price(150.0, forward=True) == 100.0

    def test_bonus_backward(self):
        a = CorporateAction(ticker="X", action_type=ActionType.BONUS,
                            ex_date="2025-01-01", ratio=0.5)
        assert a.adjust_price(100.0, forward=False) == 150.0

    def test_rights_forward(self):
        a = CorporateAction(ticker="X", action_type=ActionType.RIGHTS,
                            ex_date="2025-01-01", ratio=0.5)
        result = a.adjust_price(100.0, forward=True)
        expected = (100.0 * 1.0 + 0.5) / (1.0 + 0.5)
        assert abs(result - expected) < 0.01

    def test_rights_backward(self):
        a = CorporateAction(ticker="X", action_type=ActionType.RIGHTS,
                            ex_date="2025-01-01", ratio=0.5)
        forward_price = (100.0 * 1.0 + 0.5) / (1.0 + 0.5)
        restored = a.adjust_price(forward_price, forward=False)
        assert abs(restored - 100.0) < 0.01

    def test_delist_returns_zero(self):
        a = CorporateAction(ticker="X", action_type=ActionType.DELIST,
                            ex_date="2025-01-01")
        assert a.adjust_price(100.0) == 0.0

    def test_suspend_returns_zero(self):
        a = CorporateAction(ticker="X", action_type=ActionType.SUSPEND,
                            ex_date="2025-01-01")
        assert a.adjust_price(100.0) == 0.0

    def test_adjust_price_standalone_function(self):
        a = CorporateAction(ticker="X", action_type=ActionType.SPLIT,
                            ex_date="2025-01-01", ratio=3.0)
        assert adjust_price(a, 90.0, forward=True) == 30.0

    def test_split_3_for_1(self):
        a = CorporateAction(ticker="X", action_type=ActionType.SPLIT,
                            ex_date="2025-01-01", ratio=3.0)
        assert a.adjust_price(300.0, forward=True) == 100.0


# ============ Integration / __init__ tests ============

class TestInit:
    def test_all_imports_available(self):
        from zmatrix.research_db.data_supply import (
            ConnectorEntry, ConnectorRegistry,
            SourceReliabilityTracker,
            PITRecord, PITStore,
            LineageEntry, DataLineage,
            CorporateAction, ActionType, adjust_price,
        )
        assert ConnectorRegistry is not None

    def test_module_docstring(self):
        import zmatrix.research_db.data_supply as ds
        assert ds.__doc__ is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
