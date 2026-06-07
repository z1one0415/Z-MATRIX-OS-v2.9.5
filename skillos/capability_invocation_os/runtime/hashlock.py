"""Deterministic hashing — pure functions, no I/O, no network."""
import hashlib, json

def stable_hash_dict(data: dict) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()

def stable_hash_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def verify_hash(expected: str, actual: str) -> bool:
    return expected == actual
