"""G08 Narrative Radar adapter — bridge narrative evidence into G18."""
from __future__ import annotations


def load_narrative_evidence() -> dict:
    """Load narrative evidence from Z-G08 output. Returns standardized dict."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "zg08_gate", "pipelines/Z-G08_叙事雷达深度/gate_pipeline.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        result = mod.run()
        themes = result.get("themes", [])
        l16 = result.get("l16", {})

        # Compute aggregate narrative heat
        if themes:
            max_heat = max(t.get("heat", 0) for t in themes)
            active = sum(1 for t in themes if t.get("heat", 0) > 5)
        else:
            max_heat = 0
            active = 0

        if max_heat > 8:
            narrative_heat = "OVERHEATED" if active <= 2 else "HIGH"
        elif max_heat > 5:
            narrative_heat = "MEDIUM"
        else:
            narrative_heat = "LOW"

        return {
            "available": True,
            "narrative_heat": narrative_heat,
            "max_theme_heat": max_heat,
            "active_themes": active,
            "l16_verdict": l16.get("verdict", "UNKNOWN"),
            "catalyst_score": round(max_heat * 10, 1),
            "data_quality": "PASS" if themes else "DATA_GAP",
        }
    except Exception:
        return {"available": False, "data_quality": "DATA_GAP"}
