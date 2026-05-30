from __future__ import annotations

import re
from typing import Optional

from zmatrix.research_db.master_data import Exchange

_SH_BOARDS: dict[str, str] = {}
for _p in ["600", "601", "603", "605"]:
    _SH_BOARDS[_p] = "MAIN"
for _p in ["688"]:
    _SH_BOARDS[_p] = "STAR"
for _p in ["510", "511", "512", "513", "514", "515", "516", "517", "518", "588"]:
    _SH_BOARDS[_p] = "MAIN"

_SZ_BOARDS: dict[str, str] = {}
for _p in ["000", "001", "002", "003", "004"]:
    _SZ_BOARDS[_p] = "MAIN"
for _p in ["159"]:
    _SZ_BOARDS[_p] = "MAIN"
for _p in ["300", "301"]:
    _SZ_BOARDS[_p] = "CHINEXT"

_BJ_BOARDS: dict[str, str] = {}
for _p in ["4", "8", "920", "830", "831", "832", "833", "834", "835", "836", "837", "838", "839"]:
    _BJ_BOARDS[_p] = "BSE"


def _strip_suffix(ticker: str) -> str:
    cleaned = ticker.strip().upper()
    for sfx in (".SH", ".SZ", ".BJ"):
        if cleaned.endswith(sfx):
            return cleaned[: -len(sfx)]
    return cleaned


def classify_exchange(ticker: str) -> Optional[Exchange]:
    base = _strip_suffix(ticker)
    if not base or len(base) < 3:
        return None
    p3 = base[:3]
    p1 = base[:1]
    if p3 in _SH_BOARDS:
        return Exchange.SSE
    if p3 in _SZ_BOARDS:
        return Exchange.SZSE
    if p1 in {"4", "8"} or p3 in {"920", "830", "831", "832", "833", "834", "835", "836", "837", "838", "839"}:
        return Exchange.BSE
    return None


def detect_board(ticker: str) -> Optional[str]:
    base = _strip_suffix(ticker)
    if not base or len(base) < 3:
        return None
    p3 = base[:3]
    p1 = base[:1]
    if p3 in _SH_BOARDS:
        return _SH_BOARDS[p3]
    if p3 in _SZ_BOARDS:
        return _SZ_BOARDS[p3]
    if p1 in {"4", "8"} or p3 in {"920", "830", "831", "832", "833", "834", "835", "836", "837", "838", "839"}:
        return "BSE"
    return None


def is_ticker_format_valid(ticker: str) -> bool:
    base = _strip_suffix(ticker)
    if not base or not re.fullmatch(r"[A-Za-z0-9]+", base):
        return False
    if not (len(base) == 6 or len(base) == 3):
        return False
    return classify_exchange(base) is not None
