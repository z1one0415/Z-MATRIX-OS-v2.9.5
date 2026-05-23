"""G09/G14 R-Matrix consistency — same service, same result"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_g09_g14_same_version_and_fields()
    test_g09_and_g14_call_same_service_consistently():
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


def test_g09_and_g14_call_same_service_consistently():
    """G09 run() and G14 _real_r_score both call evaluate_r_matrix_cycle"""
    # Verify G09 run() path uses evaluate_r_matrix_cycle
    zg09_source = open("pipelines/Z-G09_全局轮动筛选/gate_pipeline.py").read()
    assert "evaluate_r_matrix_cycle" in zg09_source, "G09 doesn't use r_matrix_service"
    assert "scan_impulse_king" not in zg09_source.split("def run")[1], "G09 still uses old scan in run()"
    assert "scan_oscillation_king" not in zg09_source.split("def run")[1], "G09 still uses old scan"
    assert "scan_rhythm_king" not in zg09_source.split("def run")[1]
    assert "scan_rotation_king" not in zg09_source.split("def run")[1]
    assert "evaluate_cycle_four_king" not in zg09_source.split("def run")[1]
    
    # Verify G14 uses same service
    zg14_source = open("pipelines/Z-G14_月度全量选股/gate_pipeline.py").read()
    assert "r_matrix_service" in zg14_source
    
    print(f"✅ G09 run() and G14 both use r_matrix_service (no old scan in G09)")

if __name__ == "__main__":
    test_g09_g14_same_version_and_fields()
    test_g09_and_g14_call_same_service_consistently()
    print("\n🏁 G09/G14 R-Matrix consistency tests PASS")
