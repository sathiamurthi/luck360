import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('draw_history.json', 'r', encoding='utf-8') as f:
    records = json.load(f)

print(f"Total draws in history: {len(records)}")

def calc_h15(tail):
    d1, d2, d3 = int(tail[0]), int(tail[1]), int(tail[2])
    n1 = (d2 + 1) % 10
    n2 = (d3 - d1 + 10) % 10
    n3 = d1
    return f"{n1}{n2}{n3}"

for i in range(len(records)):
    r = records[i]
    tail = r['tail']
    h15 = calc_h15(tail)
    next_tail = records[i+1]['tail'] if i+1 < len(records) else None
    print(f"Draw {r['id']} ({r['date']} {r['time']}): Tail={tail} -> H15={h15} (Next was: {next_tail})")
