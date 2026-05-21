"""L2.5 macro contract — proxy_level, transmission, no ~/.openclaw path"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_l25_macro_is_keyword_proxy():
    spec = importlib.util.spec_from_file_location("zg01", "pipelines/Z-G01_数据后勤保障/gate_data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.l25_macro()
    assert r["proxy_level"] == "KEYWORD_PROXY"
    assert r["transmission"] == "NOT_FULL_MACRO_TRANSMISSION"
    assert "memory_source" in r
    print(f"✅ proxy={r['proxy_level']} filled={r['filled']}/{r['total']}")


def test_l25_macro_no_absolute_openclaw_path():
    spec = importlib.util.spec_from_file_location("zg01", "pipelines/Z-G01_数据后勤保障/gate_data.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = mod.l25_macro()
    assert "~/.openclaw" not in r.get("memory_source", ""), f"still uses absolute path: {r.get('memory_source')}"
    print(f"✅ memory_source: {r['memory_source'][:50]}...")


if __name__ == "__main__":
    test_l25_macro_is_keyword_proxy()
    test_l25_macro_no_absolute_openclaw_path()
    print("\n🏁 L2.5 macro contract tests PASS")
