import json

data = json.load(open('draw_history.json'))

def slotOf(t):
    t = str(t or '').upper()
    return 0 if '1:00' in t else 1 if '3:00' in t else 2 if '6:00' in t else 3 if '8:00' in t else -1

import re
def tail3(r):
    t = re.sub(r'\D', '', str(r.get('tail', '')))
    if len(t) >= 3: return t[-3:]
    # skipping ticket logic for brevity
    return None

def ordOf(date, s):
    # Math.floor(Date.UTC(p[0], p[1] - 1, p[2]) / 864e5) * 4 + s
    return 0

m = {}
for r in data:
    s = slotOf(r.get('time'))
    n = tail3(r)
    if s < 0 or not n or not r.get('date'):
        print(f"Skipped: s={s}, n={n}, date={r.get('date')}")
        continue
    m[ordOf(r.get('date'), s)] = {'date': r.get('date'), 'slot': s, 'n': n}

print(f"Total: {len(m)}")
