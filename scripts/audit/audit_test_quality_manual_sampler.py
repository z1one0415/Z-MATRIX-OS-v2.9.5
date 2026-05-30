"""Major Audit Pack B — Test Quality Manual Sampler."""
import re, json, random
from pathlib import Path
random.seed(42)

test_dir = Path("tests/research_db")
all_tests = []
for tf in test_dir.rglob("test_*.py"):
    content = tf.read_text()
    for m in re.finditer(r'def test_\w+', content):
        rest = content[m.end():m.end()+500]
        cat = "EXISTENCE_TEST"
        if "production_allowed" in rest.lower() or "BLOCKED" in rest: cat = "SAFETY_TEST"
        elif "pytest.approx" in rest or ("compute_" in m.group(0) and "assert" in rest): cat = "REAL_LOGIC_TEST"
        elif "fixture" in rest.lower() or "sample_" in rest: cat = "FIXTURE_TEST"
        elif rest.count("assert") > 1: cat = "REAL_LOGIC_TEST"
        else: cat = "WEAK_TEST"
        all_tests.append({"file": str(tf.relative_to(test_dir.parent.parent)), "test": m.group(0), "auto_category": cat})

by_cat = {}; [by_cat.setdefault(t["auto_category"], []).append(t) for t in all_tests]
sample = []
for cat, n in [("REAL_LOGIC_TEST",30),("WEAK_TEST",50),("SAFETY_TEST",20),("FIXTURE_TEST",20),("EXISTENCE_TEST",20)]:
    pool = by_cat.get(cat, []); sample.extend(random.sample(pool, min(n, len(pool))) if pool else [])

Path("runtime_reports/audit/test_quality_manual_sample.json").write_text(json.dumps(sample, indent=2))
print(f"Sampled {len(sample)} tests from {len(all_tests)} total")
