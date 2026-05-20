#!/usr/bin/env python3
"""☯️ Universe Provider — 统一股票池契约

所有"全局筛选"管线(G09/G10/G14)必须通过此模块获取股票池。
没有 universe_contract.is_global=True，就不能叫"全局筛选"。

Sources:
  A_SHARE_ALL  — baostock全A股 → cache → index basket fallback → DATA_GAP
  INDEX_300    — 沪深300成分股
  INDEX_500    — 中证500成分股
  INDEX_1000   — 中证1000成分股
  WATCHLIST    — MEMORY.md 持仓/自选
  PRESET_DEV   — 开发调试固定池 (is_global=False, 不得进入生产全局管线)
  FILE         — 本地 universe 文件
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
import json, os, re

WORKSPACE = Path(__file__).resolve().parent.parent
DATA_DIR = WORKSPACE / "data" / "universe"
DATA_DIR.mkdir(parents=True, exist_ok=True)
MEMORY_MD = WORKSPACE.parent / "MEMORY.md"

TZ = timezone(timedelta(hours=8))

# Dev preset — explicitly NOT global
_DEV_PRESET = [
    "002463", "002472", "002837", "002881", "002979", "000977", "000988",
    "300308", "300394", "300502", "300620", "300687", "300499",
    "600519", "601899", "601898",
    "688041", "688111", "688160", "688256", "688322", "688608", "688981",
]

_MIN_GLOBAL_COUNT = 4000  # A_SHARE_ALL must have >= this many to claim FULL_MARKET


@dataclass
class UniverseResult:
    status: str
    source: str
    tickers: list[str]
    count: int
    is_global: bool
    universe_level: str
    fallback_used: bool = False
    fallback_source: str | None = None
    as_of: str | None = None
    cache_path: str | None = None
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


# ============================================================
# Source implementations
# ============================================================

def _a_share_all(allow_fallback: bool) -> dict:
    """A股全市场 — baostock.query_all_stock → local cache → index basket → DATA_GAP"""
    today = datetime.now(TZ).strftime("%Y-%m-%d")
    warnings = []

    # 1. Try baostock live
    tickers = _bs_all_stock(today)
    if tickers and len(tickers) >= _MIN_GLOBAL_COUNT:
        return _make_result("PASS", "A_SHARE_ALL", tickers, True, "FULL_MARKET",
                            as_of=today, warnings=warnings)

    # 2. Try local cache (≤30 days old)
    cache_path = DATA_DIR / "a_share_all.json"
    tickers, cache_date = _read_cache(cache_path, max_age_days=30)
    if tickers and len(tickers) >= _MIN_GLOBAL_COUNT:
        warnings.append(f"using cache from {cache_date}")
        return _make_result("PASS", "A_SHARE_ALL", tickers, True, "FULL_MARKET",
                            fallback_used=True, fallback_source="CACHE_A_SHARE_ALL",
                            as_of=cache_date, cache_path=str(cache_path), warnings=warnings)

    # 3. If allow_fallback: merge INDEX_300+500+1000
    if allow_fallback:
        idx_tickers = set()
        for src in ["INDEX_300", "INDEX_500", "INDEX_1000"]:
            r = _index_basket(src)
            if r["tickers"]:
                idx_tickers.update(r["tickers"])
        tickers = sorted(idx_tickers)
        if tickers:
            warnings.append("A_SHARE_ALL unavailable, fallback to INDEX_BASKET")
            return _make_result("DEGRADED", "A_SHARE_ALL", tickers, False, "INDEX_BASKET",
                                fallback_used=True, fallback_source="INDEX_BASKET",
                                as_of=today, warnings=warnings)

    # 4. DATA_GAP
    return _make_result("DATA_GAP", "A_SHARE_ALL", [], False, "FULL_MARKET",
                        warnings=["A_SHARE_ALL unavailable, no cache, no fallback"])


def _index_basket(source: str) -> dict:
    """指数成分股 — baostock/akshare → local cache → DATA_GAP"""
    today = datetime.now(TZ).strftime("%Y-%m-%d")

    # Try baostock specialized APIs
    tickers = _bs_index_constituents(source)
    if tickers:
        return _make_result("PASS", source, tickers, False, source,
                            as_of=today)

    # Try akshare
    try:
        tickers = _ak_index_constituents(source)
        if tickers:
            return _make_result("PASS", source, tickers, False, source,
                                as_of=today)
    except ImportError:
        pass

    # Try local cache
    cache_name = source.lower() + ".json"
    cache_path = DATA_DIR / cache_name
    tickers, cache_date = _read_cache(cache_path, max_age_days=90)
    if tickers:
        return _make_result("PASS", source, tickers, False, source,
                            fallback_used=True, fallback_source=f"CACHE_{source}",
                            as_of=cache_date, cache_path=str(cache_path))

    return _make_result("DATA_GAP", source, [], False, source)


def _watchlist() -> dict:
    """MEMORY.md 持仓/自选"""
    tickers = []
    as_of = "unknown"
    if MEMORY_MD.exists():
        as_of = datetime.fromtimestamp(MEMORY_MD.stat().st_mtime, TZ).strftime("%Y-%m-%d")
        for m in re.finditer(r'\b(00\d{4}|30\d{4}|60\d{4}|68\d{4})\b', open(MEMORY_MD).read()):
            c = m.group(1)
            if c not in tickers:
                tickers.append(c)
    return _make_result("PASS" if tickers else "DATA_GAP", "WATCHLIST", tickers,
                        False, "WATCHLIST", as_of=as_of)


def _preset_dev() -> dict:
    """开发调试池 — 不得进入全局管线"""
    return _make_result("PASS", "PRESET_DEV", list(_DEV_PRESET),
                        False, "DEV_SAMPLE", as_of="static",
                        warnings=["DEV_SAMPLE_NOT_GLOBAL"])


# ============================================================
# Helper functions
# ============================================================

def _bs_all_stock(today: str) -> list[str]:
    """baostock.query_all_stock — filter to valid A-shares"""
    try:
        import baostock as bs
        bs.login()
        rs = bs.query_all_stock(day=today)
        tickers = []
        while rs.next():
            r = rs.get_row_data()
            if len(r) < 3:
                continue
            code_full = r[0]  # e.g. sh.600000
            name = r[2] if len(r) > 2 else ""
            if "ST" in name or "退" in name:
                continue
            if "." in code_full:
                code = code_full.split(".")[1]
                if code[:2] in ("00", "30", "60", "68"):
                    tickers.append(code)
        bs.logout()
        return sorted(set(tickers))
    except Exception:
        return []


def _bs_index_constituents(source: str) -> list[str]:
    """baostock index constituent queries"""
    try:
        import baostock as bs
        bs.login()
        if source == "INDEX_300":
            rs = bs.query_hs300_stocks()
        elif source == "INDEX_500":
            rs = bs.query_zz500_stocks()
        else:
            bs.logout()
            return []
        tickers = []
        while rs.next():
            r = rs.get_row_data()
            if r and len(r) > 1:
                code = r[1].replace("sh.", "").replace("sz.", "")
                tickers.append(code)
        bs.logout()
        return sorted(set(tickers))
    except Exception:
        return []


def _ak_index_constituents(source: str) -> list[str]:
    """akshare index constituent fallback"""
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("akshare not installed")

    index_map = {
        "INDEX_300": "000300",
        "INDEX_500": "000905",
        "INDEX_1000": "000852",
    }
    code = index_map.get(source)
    if not code:
        return []
    df = ak.index_stock_cons_weight_csindex(code)
    if df is None or df.empty:
        return []
    return sorted(set(c.replace("sh.", "").replace("sz.", "") for c in df["成分券代码"].tolist()))


def _read_cache(path: Path, max_age_days: int) -> tuple[list[str] | None, str | None]:
    """Read cached ticker list if fresh enough"""
    if not path.exists():
        return None, None
    try:
        data = json.loads(path.read_text())
        as_of = data.get("as_of", "")
        if as_of:
            cache_date = datetime.strptime(as_of, "%Y-%m-%d").replace(tzinfo=TZ)
            age = (datetime.now(TZ) - cache_date).days
            if age > max_age_days:
                return None, None
        return data.get("tickers", []), as_of
    except Exception:
        return None, None


def _make_result(status, source, tickers, is_global, universe_level, **kw) -> dict:
    return UniverseResult(
        status=status, source=source, tickers=tickers, count=len(tickers),
        is_global=is_global, universe_level=universe_level, **kw,
    ).to_dict()


# ============================================================
# Public API
# ============================================================

def load_universe(source: str = "A_SHARE_ALL", allow_fallback: bool = False,
                  min_count: int | None = None) -> dict:
    """Load stock universe by source.

    Returns UniverseResult as dict with mandatory fields:
      status, source, tickers, count, is_global, universe_level,
      fallback_used, fallback_source, as_of, cache_path, warnings
    """
    if source == "A_SHARE_ALL":
        uni = _a_share_all(allow_fallback=allow_fallback)
    elif source in ("INDEX_300", "INDEX_500", "INDEX_1000"):
        uni = _index_basket(source)
    elif source == "WATCHLIST":
        uni = _watchlist()
    elif source == "PRESET_DEV":
        uni = _preset_dev()
    elif source == "FILE":
        uni = _make_result("DATA_GAP", "FILE", [], False, "FILE",
                           warnings=["FILE source not yet implemented, specify path"])
    else:
        uni = _make_result("DATA_GAP", source, [], False, "UNKNOWN",
                           warnings=[f"unknown source: {source}"])

    # Enforce min_count
    if min_count and uni["count"] < min_count:
        uni["status"] = "DATA_GAP"
        uni["warnings"].append(f"count={uni['count']} < min_count={min_count}")
        uni["is_global"] = False

    return uni
