from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline import AlphaValidationPipeline


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def emit(obj, output: str | None):
    data = json.dumps(obj, ensure_ascii=False, indent=2)
    if output:
        Path(output).write_text(data, encoding="utf-8")
    else:
        print(data)


def main():
    p = argparse.ArgumentParser(description="Z-G16A Alpha Parallel Validation CLI")
    p.add_argument("command", choices=["create_plan", "open", "mark", "decision", "settle", "coach"])
    p.add_argument("--store", required=True, help="JSONL event store path")
    p.add_argument("--payload", required=True, help="JSON payload path")
    p.add_argument("--output")
    args = p.parse_args()
    pipe = AlphaValidationPipeline(args.store)
    payload = load_json(args.payload)
    if args.command == "create_plan":
        result = pipe.create_plan(payload)
    elif args.command == "open":
        result = pipe.open_position(**payload)
    elif args.command == "mark":
        result = pipe.mark_to_market(**payload)
    elif args.command == "decision":
        result = pipe.human_decision(payload)
    elif args.command == "settle":
        result = pipe.settle(**payload)
    elif args.command == "coach":
        result = pipe.coach_report(**payload)
    else:
        raise SystemExit(2)
    emit(result, args.output)


if __name__ == "__main__":
    main()
