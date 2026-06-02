#!/usr/bin/env python3
"""
CODING AUTOPILOT — Task router + pre-commit safety gate.
Usage:
  python3 scripts/cases/autopilot.py "task description"    # classify + route
  python3 scripts/cases/autopilot.py --check               # pre-commit safety
"""
import sys, subprocess
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent
BRANCH = "v4.0-batch-0-final-hardgates-scope-lock"

KEYWORDS = {
    "NEW_MODULE": ["new script", "new .py", "create .py", "新增脚本"],
    "BATCH_IMPL": ["one-shot", "batch", "phase", "一次执行", "Vx-A/B/C"],
    "BATCH_TEST": ["test files", "批量测试", "新增测试"],
    "FIX_ONLY": ["fix", "修复", "语法错误", "空壳", "局部"],
    "DOC_ONLY": ["closeout", "report", "doc", "文档", "报告"],
}

def classify(desc):
    d = desc.lower()
    best, best_score = "NEW_MODULE", 0
    for cat, kws in KEYWORDS.items():
        s = sum(1 for kw in kws if kw.lower() in d)
        if s > best_score: best, best_score = cat, s
    return best

def safety():
    errors = []
    for d in ["scripts", "zmatrix", "tests"]:
        r = subprocess.run(["python3","-m","compileall","-q",d], capture_output=True, text=True, cwd=str(WORKSPACE))
        if "SyntaxError" in r.stdout: errors.append(f"compileall {d}")
    r = subprocess.run(["git","branch","--show-current"], capture_output=True, text=True, cwd=str(WORKSPACE))
    if r.stdout.strip() != BRANCH: errors.append(f"branch={r.stdout.strip()}")
    return errors

def main():
    if len(sys.argv) < 2:
        print("Usage: autopilot.py '<task>'  OR  autopilot.py --check")
        sys.exit(1)

    if sys.argv[1] == "--check":
        print("=" * 50)
        print("[AUTOPILOT] Pre-commit Safety Check")
        print("=" * 50)
        r = subprocess.run(["git","branch","--show-current"], capture_output=True, text=True, cwd=str(WORKSPACE))
        b = r.stdout.strip()
        print(f"  Branch: {b} {'OK' if b==BRANCH else 'WRONG'}")
        errs = safety()
        if errs:
            for e in errs: print(f"  FAIL: {e}")
            sys.exit(1)
        else:
            print("  compileall: PASS")
            print("  Safety: ALL CLEAR")
        return

    task = sys.argv[1]
    cat = classify(task)
    print("=" * 50)
    print("[AUTOPILOT] Task Router")
    print("=" * 50)
    r = subprocess.run(["git","branch","--show-current"], capture_output=True, text=True, cwd=str(WORKSPACE))
    print(f"  Branch: {r.stdout.strip()}")
    print(f"  Task: {task[:80]}...")
    print(f"  Category: {cat}")

    use_oc = cat in ("NEW_MODULE", "BATCH_IMPL", "BATCH_TEST")
    oc_ok = subprocess.run(["which","opencode"], capture_output=True, text=True, cwd=str(WORKSPACE)).returncode == 0
    print(f"  opencode: {'AVAILABLE' if oc_ok else 'NOT FOUND'}")
    print(f"  Route: {'OPENCODE' if (use_oc and oc_ok) else 'MANUAL'}")

    if use_oc and oc_ok:
        print()
        print("  Delegating to opencode...")
        r = subprocess.run(["opencode","run",task,"--model","deepseek/deepseek-v4-pro"], cwd=str(WORKSPACE))
        print(f"  opencode exit: {r.returncode}")
        print("  Run: autopilot.py --check before commit.")
    elif use_oc and not oc_ok:
        print("  opencode not installed — manual mode.")
    else:
        print(f"  '{cat}' → manual. Run: autopilot.py --check before commit.")

if __name__ == "__main__":
    main()
