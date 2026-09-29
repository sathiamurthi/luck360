import json

with open('draw_history.json', 'r') as f:
    recs = json.load(f)

print(f"Total records: {len(recs)}")
for i, r in enumerate(recs):
    print(f"[{i:2d}] {r.get('date')} {r.get('time', ''):8s} | {r.get('company', ''):25s} | Ticket: {r.get('ticket', ''):12s} | Tail: {r.get('tail')}")
