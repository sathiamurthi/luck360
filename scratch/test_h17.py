import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('draw_history.json', 'r', encoding='utf-8') as f:
    draws = json.load(f)

def h17(seed):
    d1, d2, d3 = int(seed[0]), int(seed[1]), int(seed[2])
    c1 = (d1 + d2) % 10
    c2 = (d1 - d2 + 10) % 10
    c3 = d3
    return f"{c1}{c2}{c3}"

print("=== USER DISCOVERY ===")
print("226 -> H17: (2+2, 2-2, 6) =", h17("226"))
print("Head 944 -> H17: (9+4, 9-4, 4) =", h17("944"))
print("Tail 406 -> H17: (4+0, 4-0, 6) =", h17("406"))

print("\n=== All Draws in History ===")
for d in draws:
    t = d.get('ticket', '')
    tokens = t.strip().split()
    if tokens:
        num = ''.join([c for c in tokens[-1] if c.isdigit()])
        if len(num) >= 5:
            head = num[:3]
            tail = num[-3:]
            print(f"Draw {d['id']} {d['date']} {d['time']}: ticket={t} | head={head} -> H17={h17(head)} | tail={tail} -> H17={h17(tail)}")
