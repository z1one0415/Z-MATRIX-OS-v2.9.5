"""V13.F3.4.1 — Last sample date resolution tests."""
import json
from pathlib import Path
B = Path(__file__).resolve().parent.parent.parent.parent.parent / "runtime_reports" / "research" / "factors" / "openclaw_batch"
d = json.loads((B / "v13_f3_4_1_last_in_sample_rebalance_dates.json").read_text())
def test_resolved(): assert d.get("all_last_in_sample_dates_resolved") is True
def test_3_resolved(): assert d.get("resolved_factor_count") == 3
def test_no_na(): assert d.get("any_na_last_in_sample_date") is False
def test_f04_not_na(): r = [r for r in d["per_factor"] if r["factor_id"]=="F04"]; assert r and r[0]["last_in_sample_rebalance_date"] not in (None,"","N/A")
def test_f10_not_na(): r = [r for r in d["per_factor"] if r["factor_id"]=="F10"]; assert r and r[0]["last_in_sample_rebalance_date"] not in (None,"","N/A")
def test_f11_not_na(): r = [r for r in d["per_factor"] if r["factor_id"]=="F11"]; assert r and r[0]["last_in_sample_rebalance_date"] not in (None,"","N/A")
def test_f04_resolved(): r = [r for r in d["per_factor"] if r["factor_id"]=="F04"]; assert r[0]["resolved"] is True
def test_f10_resolved(): r = [r for r in d["per_factor"] if r["factor_id"]=="F10"]; assert r[0]["resolved"] is True
def test_f11_resolved(): r = [r for r in d["per_factor"] if r["factor_id"]=="F11"]; assert r[0]["resolved"] is True
def test_f04_date_count(): r = [r for r in d["per_factor"] if r["factor_id"]=="F04"]; assert r[0]["source_rebalance_date_count"] > 0
def test_no_oos(): assert d.get("true_oos_validation_executed") is False
def test_no_alpha(): assert d.get("alpha_claim_allowed") is False
