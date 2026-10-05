import json, os, re, sqlite3
from typing import Optional
from fastapi import APIRouter, FastAPI, HTTPException, Query
from pydantic import BaseModel

DB_PATH = os.environ.get("DB_PATH", "lottery.db")      # point this at your existing lottery.db
router = APIRouter(prefix="/api/v1")

SCHEMA = """
CREATE TABLE IF NOT EXISTS slips (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  draw_date TEXT NOT NULL, slot TEXT NOT NULL, title TEXT,
  rate_3d INTEGER NOT NULL DEFAULT 30, rate_pair INTEGER NOT NULL DEFAULT 13, rate_board INTEGER NOT NULL DEFAULT 10,
  raw_json TEXT NOT NULL,
  n_3d INT, n_ab INT, n_bc INT, n_ac INT, n_abc INT, n_board INT,
  amt_3d INT, amt_ab INT, amt_bc INT, amt_ac INT, amt_abc INT, amt_board INT, amt_total INT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP, updated_at TEXT,
  UNIQUE (draw_date, slot));"""

def db():
    c = sqlite3.connect(DB_PATH); c.row_factory = sqlite3.Row; return c

def init_slips_table():
    with db() as c: c.executescript(SCHEMA)

class Raw(BaseModel):
    s3: str = ""; ab: str = ""; bc: str = ""; ac: str = ""; abc: str = ""; board: str = ""

class SlipIn(BaseModel):
    date: str; slot: str; title: str = ""
    r3: int = 30; rp: int = 13; rb: int = 10
    raw: Raw

def nums(txt: str, n: int):
    return [t for t in re.findall(r"\d+", txt or "") if len(t) == n]

def cost(s: SlipIn) -> dict:
    n3, nab, nbc, nac, nx = (len(nums(getattr(s.raw, k), n)) for k, n in
                             (("s3", 3), ("ab", 2), ("bc", 2), ("ac", 2), ("abc", 2)))
    nd = len(set(re.findall(r"\d", s.raw.board)))
    a = dict(amt_3d=n3 * s.r3, amt_ab=nab * s.rp, amt_bc=nbc * s.rp, amt_ac=nac * s.rp,
             amt_abc=nx * 3 * s.rp,            # AB.BC.AC: count x 3 x 13
             amt_board=nd * 36 * s.rb)         # All Board: 36 numbers per digit (360 at Rs 10)
    a.update(n_3d=n3, n_ab=nab, n_bc=nbc, n_ac=nac, n_abc=nx, n_board=nd,
             amt_total=sum(v for k, v in a.items() if k.startswith("amt_")))
    return a

def out(r):
    return {**{k: r[k] for k in r.keys() if k != "raw_json"}, "raw": json.loads(r["raw_json"])}

@router.post("/slips")
def save_slip(s: SlipIn):
    c_ = cost(s)                                # cost is always recomputed on the server
    cols = ["draw_date", "slot", "title", "rate_3d", "rate_pair", "rate_board", "raw_json", *c_.keys()]
    vals = [s.date, s.slot, s.title, s.r3, s.rp, s.rb, s.raw.model_dump_json(), *c_.values()]
    upd = ", ".join(f"{k}=excluded.{k}" for k in cols[2:]) + ", updated_at=CURRENT_TIMESTAMP"
    with db() as c:
        c.execute(f"INSERT INTO slips ({','.join(cols)}) VALUES ({','.join('?'*len(cols))}) "
                  f"ON CONFLICT(draw_date, slot) DO UPDATE SET {upd}", vals)
        r = c.execute("SELECT * FROM slips WHERE draw_date=? AND slot=?", (s.date, s.slot)).fetchone()
    return {"ok": True, "slip": out(r)}

@router.get("/slips")
def list_slips(date_from: str = Query("0000-00-00", alias="from"),
               date_to: str = Query("9999-12-31", alias="to"), slot: Optional[str] = None):
    q, a = "SELECT * FROM slips WHERE draw_date BETWEEN ? AND ?", [date_from, date_to]
    if slot: q += " AND slot=?"; a.append(slot)
    with db() as c: rows = c.execute(q + " ORDER BY draw_date DESC, slot DESC", a).fetchall()
    return [out(r) for r in rows]

@router.get("/slips/summary")
def summary(date_from: str = Query("0000-00-00", alias="from"), date_to: str = Query("9999-12-31", alias="to")):
    with db() as c:
        rows = c.execute("SELECT draw_date, COUNT(*) slips, SUM(amt_total) total FROM slips "
                         "WHERE draw_date BETWEEN ? AND ? GROUP BY draw_date ORDER BY draw_date DESC",
                         (date_from, date_to)).fetchall()
    return [dict(r) for r in rows]

@router.get("/slips/{sid}")
def get_slip(sid: int):
    with db() as c: r = c.execute("SELECT * FROM slips WHERE id=?", (sid,)).fetchone()
    if not r: raise HTTPException(404, "slip not found")
    return out(r)

@router.delete("/slips/{sid}")
def delete_slip(sid: int):
    with db() as c: c.execute("DELETE FROM slips WHERE id=?", (sid,))
    return {"ok": True}

app = FastAPI(title="Slips API"); init_slips_table(); app.include_router(router)