import json
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

with open("draw_history.json", "r", encoding="utf-8") as f:
    draws = json.load(f)

print("KERALA DRAWS IN HISTORY:")
for d in draws:
    if "Kerala" in d.get("company", "") or "3:00" in d.get("time", ""):
        print(f"ID {d['id']:2d} | Date: {d['date']} | {d.get('lottery')} | Ticket: {d.get('ticket')} | Tail: {d.get('tail')}")

print("\nALL PREVIOUS FULL TICKETS & RECENT DRAWS:")
for d in draws[-6:]:
    print(f"ID {d['id']:2d} | {d['date']} {d.get('time'):7s} | {d.get('lottery')} | Full Ticket: {d.get('ticket')} | Tail: {d.get('tail')}")
