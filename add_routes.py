import io

routes = '''
# -------------------------------------------------------------
# Ticket History Endpoints
# -------------------------------------------------------------

@app.get("/api/v1/tickets", tags=["Tickets"])
async def get_tickets():
    conn = sqlite3.connect(os.path.join(WORKSPACE_DIR, "lottery.db"))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM tickets ORDER BY id ASC").fetchall()
    conn.close()
    
    result = []
    for r in rows:
        d = dict(r)
        d["rates"] = json.loads(d["rates"]) if d["rates"] else {}
        d["breakdown"] = json.loads(d["breakdown"]) if d["breakdown"] else []
        d["repeats"] = bool(d["repeats"])
        result.append(d)
    return result

@app.post("/api/v1/tickets", tags=["Tickets"])
async def save_ticket(request: Request):
    data = await request.json()
    conn = sqlite3.connect(os.path.join(WORKSPACE_DIR, "lottery.db"))
    conn.execute("""
        INSERT OR REPLACE INTO tickets (id, date, slot, result, cost, win, net, text, rates, repeats, breakdown)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("id"),
        data.get("date"),
        data.get("slot"),
        data.get("result"),
        data.get("cost"),
        data.get("win"),
        data.get("net"),
        data.get("text"),
        json.dumps(data.get("rates", {})),
        1 if data.get("repeats") else 0,
        json.dumps(data.get("breakdown", []))
    ))
    conn.commit()
    conn.close()
    return {"ok": True}

@app.delete("/api/v1/tickets/{ticket_id}", tags=["Tickets"])
async def delete_ticket(ticket_id: int):
    conn = sqlite3.connect(os.path.join(WORKSPACE_DIR, "lottery.db"))
    conn.execute("DELETE FROM tickets WHERE id=?", (ticket_id,))
    conn.commit()
    conn.close()
    return {"ok": True}
'''

content = io.open('luck360_api_server.py', 'r', encoding='utf-8').read()
content = content.replace('# Main Runner', routes + '\n# Main Runner')
io.open('luck360_api_server.py', 'w', encoding='utf-8').write(content)
