"""Test RC1 Readiness Scorecard generation and content."""
import subprocess, re
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent
SCORECARD_MD = WORKSPACE / "docs" / "rc1_audit" / "RC1_READINESS_SCORECARD.md"
GENERATE_SCRIPT = WORKSPACE / "scripts" / "generate_rc1_readiness_scorecard.py"


def test_scorecard_script_exists():
    """Verify generate_rc1_readiness_scorecard.py exists and is executable."""
    assert GENERATE_SCRIPT.exists(), f"Script not found: {GENERATE_SCRIPT}"
    content = GENERATE_SCRIPT.read_text()
    assert "def check" in content, "Missing core check function"
    assert "RC1_READINESS_SCORECARD.md" in content, "Missing scorecard path reference"


def test_scorecard_generated():
    """Run generator and verify RC1_READINESS_SCORECARD.md is created."""
    result = subprocess.run(
        ["python3", str(GENERATE_SCRIPT)],
        capture_output=True, text=True, cwd=str(WORKSPACE), timeout=120
    )
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    assert SCORECARD_MD.exists(), f"Scorecard not generated at {SCORECARD_MD}"


def test_scorecard_has_recommendation():
    """Scorecard must contain a final recommendation."""
    assert SCORECARD_MD.exists(), "Scorecard file not found"
    text = SCORECARD_MD.read_text()
    assert "Recommendation:" in text, "Missing Recommendation field"
    rec = re.search(r"Recommendation:\s*\*\*(.*?)\*\*", text)
    assert rec is not None, "Cannot parse recommendation value"
    assert rec.group(1) in (
        "RC1_READY_RECOMMENDED",
        "RC1_CONDITIONAL",
        "RC1_BLOCKED",
    ), f"Unexpected recommendation: {rec.group(1)}"


def test_scorecard_has_scores():
    """Scorecard must contain numeric score and item-level scores."""
    assert SCORECARD_MD.exists(), "Scorecard file not found"
    text = SCORECARD_MD.read_text()
    assert re.search(r"Score:\s*\*\*\d+/100\*\*", text), "Missing total score line"
    # Must have at least 6 item scores
    score_items = re.findall(r"\d+\.\s+\w+.*?(?:\d+/\d+)", text)
    assert len(score_items) >= 6, f"Expected >=6 item scores, found {len(score_items)}"


def test_scorecard_no_rc1_tag():
    """Scorecard MUST explicitly state RC1 tag NOT created."""
    assert SCORECARD_MD.exists(), "Scorecard file not found"
    text = SCORECARD_MD.read_text()
    assert "NOT created" in text or "not created" in text, \
        "Missing explicit 'NOT created' language for RC1 tag"
    assert "Production NOT enabled" in text, \
        "Missing explicit 'Production NOT enabled'"
