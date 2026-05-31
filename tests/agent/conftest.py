"""Test isolation: redirect all runtime paths to temp dirs before import."""
import os
import tempfile
import atexit
import shutil

_TMP = tempfile.mkdtemp(prefix="zagent_")
atexit.register(lambda: shutil.rmtree(_TMP, ignore_errors=True))

_ledgers = os.path.join(_TMP, "ledgers")
_registry = os.path.join(_TMP, "registry")
os.makedirs(_ledgers, exist_ok=True)
os.makedirs(_registry, exist_ok=True)

os.environ.setdefault("Z_PROPOSAL_LEDGER_PATH", os.path.join(_ledgers, "p.jsonl"))
os.environ.setdefault("Z_APPROVAL_LEDGER_PATH", os.path.join(_ledgers, "a.jsonl"))
os.environ.setdefault("Z_EXECUTION_LEDGER_PATH", os.path.join(_ledgers, "e.jsonl"))
os.environ.setdefault("Z_AUDIT_LEDGER_PATH", os.path.join(_ledgers, "au.jsonl"))
os.environ.setdefault("Z_COMMAND_LEDGER_PATH", os.path.join(_ledgers, "c.jsonl"))
os.environ.setdefault("Z_ACTION_QUEUE_PATH", os.path.join(_ledgers, "aq.jsonl"))
