"""G09/G14 R-Matrix consistency — same service, same result"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_g09_g14_same_version_and_fields():
    # Verify both G09 and G14 reference r_matrix_service
    for name, path in [("G09", "pipelines/Z-G09_全局轮动筛选/gate_pipeline.py"),
                        ("G14", "pipelines/Z-G14_月度全量选股/gate_pipeline.py")]:
        s = open(path).read()
        assert "r_matrix_service" in s, f"{name} doesn't use r_matrix_service"
        assert "v2.0-cycle-four-king" in s, f"{name} doesn't reference v2.0"
    
    # Verify G14 _real_r_score returns proper fields
    spec = importlib.util.spec_from_file_location("zg14", "pipelines/Z-G14_月度全量选股/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    
    import zmatrix.scoring.r_matrix.r_matrix_service as rms
    orig = rms.evaluate_r_matrix_cycle
    rms.evaluate_r_matrix_cycle = lambda t, p, **kw: {
        "ticker": t, "version": "v2.0-cycle-four-king", "status": "PASS",
        "r_score": 7.0, "r_resonance_status": "CYCLE_RESONANCE_ENTRY",
        "r_action_cap": "WATCH_ENTRY", "entry_action_cap": "WATCH_ENTRY",
        "exit_alert": "NONE", "hard_blocks": [], "conflicts": [],
        "kings": {}, "sell_decision": None, "errors": [], "warnings": [],
        "legacy_fallback": False, "data_lineage": {"source": "test"},
    }
    try:
        r = mod._real_r_score("002472", "test", [10]*300)
        assert r["r_version"] == "v2.0-cycle-four-king"
        assert "r_resonance_status" in r
        assert "r_action_cap" in r
        print(f"✅ G14 returns: v={r['r_version']} resonance={r['r_resonance_status']} cap={r['r_action_cap']}")
    finally:
        rms.evaluate_r_matrix_cycle = orig

if __name__ == "__main__":
    test_g09_g14_same_version_and_fields()
    print("\n🏁 G09/G14 R-Matrix consistency tests PASS")
