"""capability_mask contract — forbidden_now vs conditional_future_outputs distinction"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_capability_mask_has_explicit_aliases():
    spec = importlib.util.spec_from_file_location("zg01", "pipelines/Z-G01_数据后勤保障/gate_data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    mask = mod.capability_mask(["exact_price_zone", "paper_fill_price"], "O3")
    assert "forbidden_now" in mask, "missing forbidden_now"
    assert mask["forbidden_now"] == mask["forbidden_actions"]
    assert "re_enable_conditions" in mask, "missing re_enable_conditions"
    assert "conditional_future_outputs" in mask, "missing conditional_future_outputs"
    print(f"✅ forbidden_now={mask['forbidden_now']} re_enable={mask['re_enable_conditions']}")


def test_capability_mask_paper_probe_forbidden_when_price_zone_disabled():
    spec = importlib.util.spec_from_file_location("zg01", "pipelines/Z-G01_数据后勤保障/gate_data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    # O3: exact_price_zone disabled → PAPER_PROBE forbidden
    mask = mod.capability_mask(["exact_price_zone"], "O3")
    assert "PAPER_PROBE" in mask["forbidden_now"]
    assert "PAPER_PROBE" not in mask["allowed_outputs"], "PAPER_PROBE should not be allowed at O3"
    # But it should be in re-enable conditions
    assert any(c["output"] == "PAPER_PROBE" for c in mask["re_enable_conditions"])
    print(f"✅ O3: PAPER_PROBE forbidden_now, allowed={mask['allowed_outputs']}")


def test_capability_mask_o5_allows_paper_probe():
    spec = importlib.util.spec_from_file_location("zg01", "pipelines/Z-G01_数据后勤保障/gate_data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    mask = mod.capability_mask([], "O5")
    assert "paper_probe" in mask["allowed_outputs"], f"O5 allowed={mask['allowed_outputs']}"
    assert "PAPER_PROBE" not in mask["forbidden_now"]
    print(f"✅ O5: paper_probe allowed")


if __name__ == "__main__":
    test_capability_mask_has_explicit_aliases()
    test_capability_mask_paper_probe_forbidden_when_price_zone_disabled()
    test_capability_mask_o5_allows_paper_probe()
    print("\n🏁 capability_mask contract tests PASS")
