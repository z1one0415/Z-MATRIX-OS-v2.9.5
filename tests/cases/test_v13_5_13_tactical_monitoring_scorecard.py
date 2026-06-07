"""V13.5.13 Tactical Monitoring Scorecard — tests."""
import json;from pathlib import Path
C=Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"cases"
def L(n):return json.loads((C/n).read_text())if (C/n).exists()else{}
s=L("v13_5_13_tactical_monitoring_scorecard.json")
def test_exists():assert s
def test_grade():assert s.get("monitoring_grade")in("RETAINED","WEAKENED","SUSPENSION_REVIEW")
def test_alpha():assert s.get("alpha_claim_allowed")is False
def test_prod():assert s.get("production")=="BLOCKED"
