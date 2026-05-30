from __future__ import annotations

import re
from typing import Optional

from zmatrix.research_db.master_data import Exchange

_SSE_PREFIXES = frozenset({"600", "601", "603", "605", "688", "510", "511", "512", "513", "514", "515", "516", "517", "518", "588"})
_SZSE_PREFIXES = frozenset({"000", "001", "002", "003", "004", "159", "300", "301"})
_BSE_PREFIXES = frozenset({"8", "4", "920", "830", "831", "832", "833", "834", "835", "836", "837", "838", "839"})


def _guess_exchange_suffix(ticker: str) -> str:
    if len(ticker) < 3:
        return ""
    if ticker.startswith("688") or ticker.startswith("600") or ticker.startswith("601") or ticker.startswith("603") or ticker.startswith("605"):
        return ".SH"
    if ticker.startswith("000") or ticker.startswith("001") or ticker.startswith("002") or ticker.startswith("003") or ticker.startswith("300") or ticker.startswith("301"):
        return ".SZ"
    if ticker.startswith("8") or ticker.startswith("4") or ticker.startswith("920"):
        return ".BJ"
    return ""


def normalize_ticker(raw_ticker: str) -> str:
    cleaned = raw_ticker.strip().upper()
    suffix_map = {".SH": ".SH", ".SZ": ".SZ", ".BJ": ".BJ"}
    suffix = ""
    for k, v in suffix_map.items():
        if cleaned.endswith(k):
            suffix = v
            cleaned = cleaned[: -len(k)]
            break
    cleaned = re.sub(r"[^A-Z0-9]", "", cleaned)
    if suffix:
        return f"{cleaned}{suffix}"
    guessed = _guess_exchange_suffix(cleaned)
    if guessed:
        return f"{cleaned}{guessed}"
    return cleaned


def resolve_identity(ticker: str, aliases: Optional[dict[str, str]] = None) -> dict[str, Optional[str]]:
    normalized = normalize_ticker(ticker)
    base = re.sub(r"\.(SH|SZ|BJ)$", "", normalized)
    suffix = ""
    if normalized.endswith(".SH"):
        exchange = "SSE"
        suffix = ".SH"
    elif normalized.endswith(".SZ"):
        exchange = "SZSE"
        suffix = ".SZ"
    elif normalized.endswith(".BJ"):
        exchange = "BSE"
        suffix = ".BJ"
    else:
        guessed = _guess_exchange_suffix(base)
        if guessed:
            suffix = guessed
            if guessed == ".SH":
                exchange = "SSE"
            elif guessed == ".SZ":
                exchange = "SZSE"
            else:
                exchange = "BSE"
        else:
            exchange = None

    canonical_ticker = f"{base}{suffix}" if suffix else base
    status = "ACTIVE"
    if aliases is not None and ticker in aliases:
        canonical_ticker = aliases[ticker]
    if aliases is not None and normalized in aliases:
        canonical_ticker = aliases[normalized]

    return {
        "canonical_ticker": canonical_ticker,
        "display_name": base,
        "exchange": exchange,
        "status": status,
    }
