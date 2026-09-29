import json, sys

sys.stdout.reconfigure(encoding='utf-8')
with open('draw_history.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
print(f'Total records: {len(data)}')
for r in data:
    print(f"{r.get('id')}: {r.get('date')} {r.get('time')} | {r.get('company')} | Ticket: {r.get('ticket')} | Tail: {r.get('tail')}")
