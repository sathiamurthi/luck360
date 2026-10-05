import json
import datetime
data = json.load(open('draw_history.json'))

def slotOf(t):
    t = str(t or '').upper()
    return 0 if '1:00' in t else 1 if '3:00' in t else 2 if '6:00' in t else 3 if '8:00' in t else -1

import re
def tail3(r):
    t = re.sub(r'\D', '', str(r.get('tail', '')))
    if len(t) >= 3: return t[-3:]
    return None

def ordOf(date, s):
    p = [int(x) for x in date.split('-')]
    dt = datetime.datetime(p[0], p[1], p[2], tzinfo=datetime.timezone.utc)
    return int(dt.timestamp() / 86400) * 4 + s

m = {}
for r in data:
    s = slotOf(r.get('time'))
    n = tail3(r)
    if s < 0 or not n or not r.get('date'):
        print(f"Skipped: s={s}, n={n}, date={r.get('date')}")
        continue
    m[ordOf(r.get('date'), s)] = {'date': r.get('date'), 'slot': s, 'n': n}

print(f"Total: {len(m)}")
