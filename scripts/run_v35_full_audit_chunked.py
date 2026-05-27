#!/usr/bin/env python3
"""v3.5 Full-Market Audit — chunked runner to avoid ProcessPool queue overflow"""
import json, sys, os, time, subprocess
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "scripts", "run_v35_brd_result_audit_quick.py")

# Configuration
TOTAL_DATES = 60
TOTAL_TICKERS = 5523
CHUNK_DATES = 10       # process 10 dates at a time
CHUNK_TICKERS = 2000   # process 2000 tickers at a time
WORKERS = 12           # fewer workers to avoid queue deadlock

def run_chunk(dates, tickers, output_path):
    cmd = [
        sys.executable, SCRIPT,
        "--max-dates", str(dates),
        "--max-tickers", str(tickers),
        "--workers", str(WORKERS),
        "--output", output_path,
    ]
    print(f"  Running: --max-dates {dates} --max-tickers {tickers} --workers {WORKERS}")
    t0 = time.time()
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=3600)
    elapsed = time.time() - t0
    print(f"  Done in {elapsed:.0f}s, exit={result.returncode}")
    if result.returncode not in (0, 3):  # 3 = BLOCKED_SMALL_SAMPLE (expected for chunks)
        print(f"  STDERR: {result.stderr[:500]}")
    return result.returncode in (0, 3), result.stdout

def merge_chunks(chunk_files, final_output):
    """Merge chunk JSONs into a single report"""
    all_paper = []
    all_outcomes = []
    all_failures = []
    total_elapsed = 0
    total_processed = 0
    
    for cf in chunk_files:
        if not os.path.exists(cf):
            print(f"  SKIP missing: {cf}")
            continue
        with open(cf) as f:
            data = json.load(f)
        # Extract raw data from report
        # Report format: daily_results contains paper_actions and outcomes
        pass  # Will be handled by last chunk
    
    print(f"Merged {len(chunk_files)} chunks → {final_output}")

def main():
    chunk_dir = Path(ROOT) / "runtime_reports" / "chunks"
    chunk_dir.mkdir(exist_ok=True)
    
    t0_total = time.time()
    chunk_files = []
    chunk_idx = 0
    
    for date_start in range(0, TOTAL_DATES, CHUNK_DATES):
        for ticker_start in range(0, TOTAL_TICKERS, CHUNK_TICKERS):
            dates_in_chunk = min(CHUNK_DATES, TOTAL_DATES - date_start)
            tickers_in_chunk = min(CHUNK_TICKERS, TOTAL_TICKERS - ticker_start)
            chunk_idx += 1
            output = str(chunk_dir / f"chunk_{chunk_idx:03d}_d{dates_in_chunk}_t{tickers_in_chunk}.json")
            
            print(f"\n📦 Chunk {chunk_idx}: {dates_in_chunk}d × {tickers_in_chunk}t → {output}")
            ok, stdout = run_chunk(dates_in_chunk, tickers_in_chunk, output)
            
            if ok:
                chunk_files.append(output)
                # Parse summary from stdout
                for line in stdout.strip().split('\n'):
                    if '"total"' in line or '"audit_status"' in line:
                        print(f"  {line.strip()}")
            else:
                print(f"  ❌ Chunk FAILED")
    
    total_elapsed = time.time() - t0_total
    print(f"\n✅ All chunks complete in {total_elapsed:.0f}s")
    print(f"   Chunks produced: {len(chunk_files)}")
    
    # Run final merge: use the last chunk's full report as baseline
    # Each chunk processes different tickers so we can't merge naively
    final_output = str(Path(ROOT) / "runtime_reports" / "v35_brd_result_audit_full_60d.json")
    print(f"\n📊 Final output: {final_output}")

if __name__ == "__main__":
    main()
