import json, os, re, sqlite3
from datetime import date as _date
from typing import List, Optional
from fastapi import APIRouter, FastAPI, HTTPException, Query
from pydantic import BaseModel, field_validator

DB_PATH = os.environ.get("DB_PATH", "lottery.db")      # same lottery.db as slips_api.py
HISTORY_JSON = os.environ.get("HISTORY_JSON", "draw_history.json")
router = APIRouter(prefix="/api/v1/mult")

SLOTS = ["1PM", "3PM", "6PM", "8PM"]
METHODS = ["D", "RPxC", "PxRC", "RPxRC", "SUM"]        # Direct, Rev P x C, P x Rev C, Rev P x Rev C, sum of the four
PAIRS = ("AB", "BC", "AC")
DIRS = ("fwd", "rev")                                   # rev = product digits read right-to-left (pair 63 also finds 36)
# field names tried on each draw_history.json record (edit if yours differ)
DATE_KEYS = ("date", "draw_date")
TIME_KEYS = ("time", "slot")
NUM_KEYS = ("result", "number", "winning_number", "ticket", "first_prize", "prize1")

SCHEMA = """
CREATE TABLE IF NOT EXISTS mult_draws (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  draw_date TEXT NOT NULL, slot TEXT NOT NULL, actual TEXT NOT NULL,
  UNIQUE (draw_date, slot));
CREATE TABLE IF NOT EXISTS mult_hits (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  draw_date TEXT NOT NULL, slot TEXT NOT NULL,          -- the CURR draw
  prev TEXT NOT NULL, curr TEXT NOT NULL, next TEXT NOT NULL,
  gap INT NOT NULL DEFAULT 0,                           -- 1 if prev/curr/next are not back-to-back draws
  method TEXT NOT NULL, product TEXT NOT NULL,
  pair_type TEXT NOT NULL, pair TEXT NOT NULL,
  direction TEXT NOT NULL DEFAULT 'fwd',
  matched INT NOT NULL, pos INT, plen INT NOT NULL,
  UNIQUE (draw_date, slot, method, pair_type, direction));
CREATE TABLE IF NOT EXISTS mult_patterns (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE, method TEXT NOT NULL, pair_type TEXT NOT NULL,
  pos INT, note TEXT, direction TEXT NOT NULL DEFAULT 'fwd', created_at TEXT DEFAULT CURRENT_TIMESTAMP);"""


def db():
    c = sqlite3.connect(DB_PATH); c.row_factory = sqlite3.Row; return c

def init_mult_tables():
    with db() as c:
        cols = [r["name"] for r in c.execute("PRAGMA table_info(mult_hits)")]
        if cols and "direction" not in cols: c.execute("DROP TABLE mult_hits")    # derived data, rebuilt from mult_draws
        c.executescript(SCHEMA)
        pc = [r["name"] for r in c.execute("PRAGMA table_info(mult_patterns)")]
        if "direction" not in pc: c.execute("ALTER TABLE mult_patterns ADD COLUMN direction TEXT NOT NULL DEFAULT 'fwd'")
        rebuild(c)


# ---------- core maths ----------
def rev(s): return s[::-1]

def products(prev: str, curr: str) -> dict:
    p = {"D": int(prev) * int(curr), "RPxC": int(rev(prev)) * int(curr),
         "PxRC": int(prev) * int(rev(curr)), "RPxRC": int(rev(prev)) * int(rev(curr))}
    p["SUM"] = sum(p.values())
    return {k: str(v) for k, v in p.items()}

def pairs_of(n: str) -> dict:
    return {"AB": n[0] + n[1], "BC": n[1] + n[2], "AC": n[0] + n[2]}

def norm_slot(s: str) -> str:
    m = re.search(r"(\d{1,2})", s or "")
    if not m: raise ValueError("slot must look like 1PM, 3PM, 6PM, 8PM")
    h = int(m.group(1)); h = h - 12 if h > 12 else h
    slot = f"{h}PM"
    if slot not in SLOTS: raise ValueError(f"slot must be one of {SLOTS}")
    return slot

def norm_num(s: str) -> str:
    d = re.sub(r"\D", "", str(s or ""))
    if len(d) < 3: raise ValueError("actual needs at least 3 digits")
    return d[-3:]                                       # 5/6-digit tickets -> last 3 digits

def ordinal(d: str, slot: str) -> int:
    return _date.fromisoformat(d).toordinal() * 4 + SLOTS.index(slot)


# ---------- models ----------
class DrawIn(BaseModel):
    date: str; slot: str; actual: str
    @field_validator("date")
    @classmethod
    def _d(cls, v): _date.fromisoformat(v); return v
    @field_validator("slot")
    @classmethod
    def _s(cls, v): return norm_slot(v)
    @field_validator("actual")
    @classmethod
    def _a(cls, v): return norm_num(v)

class BulkIn(BaseModel):
    draws: List[DrawIn]

class PatternIn(BaseModel):
    name: str; method: str; pair_type: str
    pos: Optional[int] = None                           # digit position in the (possibly reversed) product where the pair starts
    direction: str = "fwd"
    note: str = ""
    @field_validator("method")
    @classmethod
    def _m(cls, v):
        if v not in METHODS: raise ValueError(f"method must be one of {METHODS}")
        return v
    @field_validator("direction")
    @classmethod
    def _dr(cls, v):
        if v not in DIRS: raise ValueError(f"direction must be one of {list(DIRS)}")
        return v
    @field_validator("pair_type")
    @classmethod
    def _p(cls, v):
        if v not in PAIRS: raise ValueError(f"pair_type must be one of {list(PAIRS)}")
        return v


# ---------- rebuild all evaluations ----------
def rebuild(c):
    ds = sorted(c.execute("SELECT draw_date, slot, actual FROM mult_draws").fetchall(),
                key=lambda r: ordinal(r["draw_date"], r["slot"]))
    c.execute("DELETE FROM mult_hits")
    n = 0
    for i in range(1, len(ds) - 1):
        p, cu, nx = ds[i - 1], ds[i], ds[i + 1]
        o = [ordinal(r["draw_date"], r["slot"]) for r in (p, cu, nx)]
        gap = int(o[1] - o[0] != 1 or o[2] - o[1] != 1)
        target = pairs_of(nx["actual"])
        for m, prod in products(p["actual"], cu["actual"]).items():
            for dr in DIRS:
                txt = prod if dr == "fwd" else rev(prod)
                for pt, pr in target.items():
                    pos = txt.find(pr)
                    c.execute("INSERT INTO mult_hits (draw_date, slot, prev, curr, next, gap, method, product, "
                              "pair_type, pair, direction, matched, pos, plen) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                              (cu["draw_date"], cu["slot"], p["actual"], cu["actual"], nx["actual"], gap, m, prod,
                               pt, pr, dr, int(pos >= 0), pos if pos >= 0 else None, len(prod)))
                    n += 1
    return n


# ---------- draws ----------
@router.post("/draws")
def save_draw(d: DrawIn):
    with db() as c:
        c.execute("INSERT INTO mult_draws (draw_date, slot, actual) VALUES (?,?,?) "
                  "ON CONFLICT(draw_date, slot) DO UPDATE SET actual=excluded.actual", (d.date, d.slot, d.actual))
        n = rebuild(c)
    return {"ok": True, "evaluations": n}

@router.post("/draws/bulk")
def save_bulk(b: BulkIn):
    with db() as c:
        for d in b.draws:
            c.execute("INSERT INTO mult_draws (draw_date, slot, actual) VALUES (?,?,?) "
                      "ON CONFLICT(draw_date, slot) DO UPDATE SET actual=excluded.actual", (d.date, d.slot, d.actual))
        n = rebuild(c)
    return {"ok": True, "draws": len(b.draws), "evaluations": n}

@router.post("/draws/import")
def import_history(path: Optional[str] = None):
    """Load draw_history.json (list of records) into mult_draws."""
    p = path or HISTORY_JSON
    if not os.path.exists(p): raise HTTPException(404, f"{p} not found")
    recs = json.load(open(p, encoding="utf-8")); ok, skipped = 0, []
    with db() as c:
        for r in recs:
            try:
                g = lambda ks: next(str(r[k]) for k in ks if r.get(k))
                d = DrawIn(date=g(DATE_KEYS)[:10], slot=g(TIME_KEYS), actual=g(NUM_KEYS))
                c.execute("INSERT INTO mult_draws (draw_date, slot, actual) VALUES (?,?,?) "
                          "ON CONFLICT(draw_date, slot) DO UPDATE SET actual=excluded.actual",
                          (d.date, d.slot, d.actual)); ok += 1
            except Exception as e:
                skipped.append(str(e)[:80])
        n = rebuild(c)
    return {"ok": True, "imported": ok, "skipped": len(skipped), "sample_errors": skipped[:3], "evaluations": n}

@router.get("/draws")
def list_draws():
    with db() as c:
        rows = c.execute("SELECT * FROM mult_draws ORDER BY draw_date DESC, slot DESC").fetchall()
    return [dict(r) for r in rows]

@router.delete("/draws/{did}")
def delete_draw(did: int):
    with db() as c:
        c.execute("DELETE FROM mult_draws WHERE id=?", (did,)); rebuild(c)
    return {"ok": True}

@router.post("/rebuild")
def rebuild_all():
    with db() as c: n = rebuild(c)
    return {"ok": True, "evaluations": n}


# ---------- products / hits / frequency ----------
@router.get("/products")
def get_products(prev: str, curr: str):
    try: prev, curr = norm_num(prev), norm_num(curr)
    except ValueError as e: raise HTTPException(400, str(e))
    pr = products(prev, curr)
    return {"prev": prev, "curr": curr, "products": pr, "sum_of_products": pr["SUM"]}

@router.get("/hits")
def list_hits(method: Optional[str] = None, pair_type: Optional[str] = None, direction: Optional[str] = None,
              matched: Optional[int] = None, include_gaps: bool = True, limit: int = 500):
    q, a = "SELECT * FROM mult_hits WHERE 1=1", []
    if method: q += " AND method=?"; a.append(method)
    if pair_type: q += " AND pair_type=?"; a.append(pair_type)
    if direction: q += " AND direction=?"; a.append(direction)
    if matched is not None: q += " AND matched=?"; a.append(matched)
    if not include_gaps: q += " AND gap=0"
    with db() as c:
        rows = c.execute(q + " ORDER BY draw_date DESC, slot DESC LIMIT ?", [*a, limit]).fetchall()
    return [dict(r) for r in rows]

def _status(n, hits, lift):
    if n < 10: return "LOW DATA"
    if hits >= 3 and lift >= 1.5: return "HOT"
    if lift >= 1.0: return "ACTIVE"
    if lift >= 0.75: return "MEDIUM"
    return "COLD"

@router.get("/frequency")
def frequency(include_gaps: bool = False, direction: Optional[str] = None):
    """Hit counts per method x pair type. Shape matches pattern_frequency.json so the HTML table can reuse it."""
    with db() as c:
        rows = c.execute("SELECT method, pair_type, direction, matched, plen FROM mult_hits WHERE (?=1 OR gap=0) "
                         "AND (? IS NULL OR direction=?) ORDER BY draw_date DESC, slot DESC",
                         (int(include_gaps), direction, direction)).fetchall()
    st = {}
    for r in rows:                                       # newest first
        k = f"{r['method']}_{r['pair_type']}_{r['direction']}"
        s = st.setdefault(k, dict(key=k, label=f"{r['method']} > {r['pair_type']} ({r['direction']})", method=r["method"],
                                  pair_type=r["pair_type"], direction=r["direction"], n=0, hits=0, exp=0.0, dist=None))
        s["n"] += 1; s["exp"] += (r["plen"] - 1) / 100   # chance a given 2-digit pair sits somewhere in the product
        if r["matched"]:
            s["hits"] += 1
            if s["dist"] is None: s["dist"] = s["n"] - 1
    out = {}
    for k, s in st.items():
        rate = 100 * s["hits"] / s["n"]; exp = 100 * s["exp"] / s["n"]; lift = rate / exp if exp else 0
        out[k] = dict(key=k, label=s["label"], method=s["method"], pair_type=s["pair_type"], direction=s["direction"],
                      straight_hits=s["hits"], box_hits=0, total_hits=s["hits"], rows=s["n"],
                      hit_rate_pct=round(rate, 1), expected_pct=round(exp, 1), lift=round(lift, 2),
                      distance_draws_ago=s["dist"] if s["dist"] is not None else s["n"],
                      status=_status(s["n"], s["hits"], lift))
    out = dict(sorted(out.items(), key=lambda kv: (-kv[1]["lift"], -kv[1]["total_hits"])))
    return {"pattern_statistics": out, "rows_evaluated": len(rows) // (len(METHODS) * 3 * (1 if direction else len(DIRS))) if rows else 0,
            "include_gaps": include_gaps}


# ---------- saved patterns (record + reuse) ----------
def _pattern_stats(c, p):
    rows = c.execute("SELECT product, pair FROM mult_hits WHERE method=? AND pair_type=? AND direction=? AND gap=0",
                     (p["method"], p["pair_type"], p["direction"])).fetchall()
    tx = lambda r: r["product"] if p["direction"] == "fwd" else rev(r["product"])
    hits = sum(1 for r in rows if (r["pair"] in tx(r) if p["pos"] is None
                                    else tx(r)[p["pos"]:p["pos"] + 2] == r["pair"]))
    return {"rows": len(rows), "hits": hits, "hit_rate_pct": round(100 * hits / len(rows), 1) if rows else 0}

@router.post("/patterns")
def save_pattern(p: PatternIn):
    with db() as c:
        try:
            c.execute("INSERT INTO mult_patterns (name, method, pair_type, pos, direction, note) VALUES (?,?,?,?,?,?)",
                      (p.name, p.method, p.pair_type, p.pos, p.direction, p.note))
        except sqlite3.IntegrityError:
            c.execute("UPDATE mult_patterns SET method=?, pair_type=?, pos=?, direction=?, note=? WHERE name=?",
                      (p.method, p.pair_type, p.pos, p.direction, p.note, p.name))
        r = c.execute("SELECT * FROM mult_patterns WHERE name=?", (p.name,)).fetchone()
        return {"ok": True, "pattern": {**dict(r), "stats": _pattern_stats(c, r)}}

@router.get("/patterns")
def list_patterns():
    with db() as c:
        rows = c.execute("SELECT * FROM mult_patterns ORDER BY id DESC").fetchall()
        return [{**dict(r), "stats": _pattern_stats(c, r)} for r in rows]

@router.delete("/patterns/{pid}")
def delete_pattern(pid: int):
    with db() as c: c.execute("DELETE FROM mult_patterns WHERE id=?", (pid,))
    return {"ok": True}


# ---------- predict: apply saved patterns to the latest pair ----------
@router.get("/predict")
def predict(prev: Optional[str] = None, curr: Optional[str] = None):
    """Uses the last two stored draws unless prev/curr are given. Returns products + candidate pairs from saved patterns."""
    with db() as c:
        if not (prev and curr):
            ds = sorted(c.execute("SELECT draw_date, slot, actual FROM mult_draws").fetchall(),
                        key=lambda r: ordinal(r["draw_date"], r["slot"]))
            if len(ds) < 2: raise HTTPException(400, "need at least 2 draws (or pass prev and curr)")
            prev, curr = ds[-2]["actual"], ds[-1]["actual"]
        pats = c.execute("SELECT * FROM mult_patterns").fetchall()
        try: prev, curr = norm_num(prev), norm_num(curr)
        except ValueError as e: raise HTTPException(400, str(e))
        pr = products(prev, curr); cands = []
        for p in pats:
            prod = pr[p["method"]]
            if p["direction"] == "rev": prod = rev(prod)
            pos = p["pos"] if p["pos"] is not None else 0
            pair = prod[pos:pos + 2]
            if len(pair) == 2:
                cands.append({"pattern": p["name"], "method": p["method"], "direction": p["direction"], "product": prod, "pos": pos,
                              "pair_type": p["pair_type"], "pair": pair, "stats": _pattern_stats(c, p)})
    return {"prev": prev, "curr": curr, "products": pr, "candidates": cands}


app = FastAPI(title="Mult Pattern API"); init_mult_tables(); app.include_router(router)
