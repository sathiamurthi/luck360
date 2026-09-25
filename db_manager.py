#!/usr/bin/env python3
"""
Lottery Database Manager & Cross-Draw Backtesting Engine
Manages lottery records in SQLite database 'lottery.db' and 'draw_history.json'.
Calculates pattern match performance (P1, P2, P3, H1, H2, H3, H4, Row 41, Row 60)
across all historical draw sequences.
"""

import sqlite3
import json
import os

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lottery.db")
JSON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "draw_history.json")

INITIAL_DRAWS = [
    {
        "date": "2026-09-01",
        "time": "3:00 PM",
        "company": "Kerala State Lotteries",
        "lottery": "Suvarna Keralam (SK 70)",
        "ticket": "40731",
        "tail": "731"
    },
    {
        "date": "2026-09-05",
        "time": "3:00 PM",
        "company": "Kerala State Lotteries",
        "lottery": "Karunya (KR 767)",
        "ticket": "799700",
        "tail": "700"
    },
    {
        "date": "2026-09-09",
        "time": "6:00 PM",
        "company": "Sikkim State Lottery",
        "lottery": "Dhanalakshmi (DL 68)",
        "ticket": "145236",
        "tail": "236"
    },
    {
        "date": "2026-09-10",
        "time": "3:00 PM",
        "company": "Kerala State Lotteries",
        "lottery": "Karunya Plus (KP 639)",
        "ticket": "812269",
        "tail": "269"
    },
    {
        "date": "2026-09-15",
        "time": "3:00 PM",
        "company": "Kerala State Lotteries",
        "lottery": "Shree Sakthi (SS 537)",
        "ticket": "304460",
        "tail": "460"
    },
    {
        "date": "2026-09-16",
        "time": "6:00 PM",
        "company": "Sikkim State Lottery",
        "lottery": "Dhanalakshmi (DL 69)",
        "ticket": "293215",
        "tail": "215"
    },
    {
        "date": "2026-09-19",
        "time": "3:00 PM",
        "company": "Kerala State Lotteries",
        "lottery": "Karunya (KR 769)",
        "ticket": "524700",
        "tail": "700"
    },
    {
        "date": "2026-09-24",
        "time": "1:00 PM",
        "company": "Nagaland State Lottery",
        "lottery": "Dear Star Thursday (1 PM)",
        "ticket": "73G 69563",
        "tail": "563"
    },
    {
        "date": "2026-09-24",
        "time": "3:00 PM",
        "company": "Kerala State Lotteries",
        "lottery": "Karunya Plus (KN-642) (3 PM)",
        "ticket": "PU 614457",
        "tail": "457"
    },
    {
        "date": "2026-09-24",
        "time": "6:00 PM",
        "company": "Sikkim State Lottery",
        "lottery": "Dear Supreme Thursday (6 PM)",
        "ticket": "86B 85978",
        "tail": "978"
    },
    {
        "date": "2026-09-24",
        "time": "8:00 PM",
        "company": "Nagaland State Lottery",
        "lottery": "Dear Fame Thursday (8 PM)",
        "ticket": "76C 18221",
        "tail": "221"
    }
]

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS draws (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            draw_date TEXT NOT NULL,
            draw_time TEXT NOT NULL,
            company TEXT NOT NULL,
            lottery_name TEXT NOT NULL,
            ticket_number TEXT NOT NULL,
            tail TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM draws")
    count = cursor.fetchone()[0]

    if count == 0:
        for d in INITIAL_DRAWS:
            cursor.execute("""
                INSERT INTO draws (draw_date, draw_time, company, lottery_name, ticket_number, tail)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (d["date"], d["time"], d["company"], d["lottery"], d["ticket"], d["tail"]))
        conn.commit()

    conn.close()

def sync_json():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM draws ORDER BY id ASC")
    rows = cursor.fetchall()
    
    records = []
    for r in rows:
        records.append({
            "id": r["id"],
            "date": r["draw_date"],
            "time": r["draw_time"],
            "company": r["company"],
            "day": f"{r['draw_date']} {r['draw_time']}",
            "lottery": f"{r['company']} - {r['lottery_name']}",
            "ticket": r["ticket_number"],
            "tail": r["tail"]
        })

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    conn.close()
    return records

def transform_58(d):
    trans_map = {5: 8, 8: 5, 7: 2, 2: 7, 6: 4, 4: 6, 9: 0, 0: 9, 1: 3, 3: 1}
    return trans_map.get(d, (d + 3) % 10)

def row60_trans(d):
    if d == 7: return 5
    if d == 0: return 9
    if d == 5: return 7
    if d == 9: return 0
    return (d + 1) % 10

def calc_all_patterns(tail):
    d1 = int(tail[0])
    d2 = int(tail[1])
    d3 = int(tail[2])

    p1 = f"{d3}{d2}{(d3 - d1 + 10) % 10}"
    p2 = f"{d1}{(d2 + 1) % 10}{(d3 - 1 + 10) % 10}"
    p3 = f"{d2}{d1}{d3}"
    r41 = f"{(d1 - 2 + 10) % 10}{(d2 - 2 + 10) % 10}{(d3 + 1) % 10}"
    r60 = f"{row60_trans(d1)}{row60_trans(d2)}{row60_trans(d3)}"
    h1 = f"{(d1 + 1) % 10}{(d2 + 1) % 10}{(d3 + 1) % 10}"
    h2 = f"{(d1 + d2) % 10}{d3}{transform_58(d2)}"
    
    diff12 = (d1 - d2 + 10) % 10
    rem_digit = (d1 + d2 + d3) % 10
    diff13 = (d1 - d3 + 10) % 10
    h3 = f"{diff12}{rem_digit}{diff13}"

    # USER PATTERN H4: First & Last Digit + Reverse AB Pair
    h4_a = f"{d1}{d3}{d2}"
    h4_b = f"{d2}{d1}{d3}"

    return {
        "P1_RevDiff": p1,
        "P2_KeepConv": p2,
        "P3_RevAB": p3,
        "Row41_Offset": r41,
        "Row60_Rule": r60,
        "H1_IncShift": h1,
        "H2_CrossSwap": h2,
        "H3_DiffRem": h3,
        "H4_FirstLastRevAB": h4_a,
        "H4_RevABLast": h4_b
    }

def run_cross_draw_analysis():
    records = sync_json()
    analysis_log = []

    for i in range(len(records) - 1):
        prev = records[i]
        curr = records[i + 1]

        prev_tail = prev["tail"]
        curr_tail = curr["tail"]

        pats = calc_all_patterns(prev_tail)

        hits = []
        curr_sorted = "".join(sorted(curr_tail))

        for name, val in pats.items():
            val_sorted = "".join(sorted(val))
            if val == curr_tail:
                hits.append({"pattern": name, "val": val, "type": "STRAIGHT HIT"})
            elif val_sorted == curr_sorted:
                hits.append({"pattern": name, "val": val, "type": "BOX HIT"})

        analysis_log.append({
            "seq": f"{i+1} -> {i+2}",
            "from": f"{prev['company']} {prev['lottery']} ({prev_tail})",
            "to": f"{curr['company']} {curr['lottery']} ({curr_tail})",
            "calculated_patterns": pats,
            "hits": hits
        })

    return analysis_log

if __name__ == "__main__":
    init_db()
    records = sync_json()
    log = run_cross_draw_analysis()
    print(f"Database Initialized with {len(records)} records.")
    print("Cross-Draw Backtest Analysis:")
    print(json.dumps(log, indent=2))
