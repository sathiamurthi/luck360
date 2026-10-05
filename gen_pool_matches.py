import json

def get_substrings(val_str, length=2):
    subs = set()
    for i in range(len(val_str) - length + 1):
        subs.add(val_str[i:i+length])
    if len(val_str) >= 2:
        subs.add(val_str[0] + val_str[-1])
        subs.add(val_str[-1] + val_str[0])
    return subs

with open('draw_history.json') as f:
    d = json.load(f)

days = {}
for x in d:
    date = x['date']
    if date not in days: days[date] = []
    if len(x['tail']) == 3:
        days[date].append(x)

dates = sorted(days.keys())

output = []
output.append("=== CROSS-DAY RAW PAIR POOL MATCHES (Last 5 Days) ===")
output.append("*(Checking if Yesterday's M1/M2 Multiplication Pool contained the exact AB, BC, or AC of Today's results)*\n")

for i in range(len(dates)-5, len(dates)):
    prev_day = dates[i-1]
    curr_day = dates[i]
    
    prev_draws = days[prev_day]
    curr_draws = days[curr_day]
    
    if len(prev_draws) < 2:
        continue
        
    pairs = set()
    for j in range(len(prev_draws) - 1):
        t1 = prev_draws[j]['tail']
        t2 = prev_draws[j+1]['tail']
        
        v1, r1, r2 = int(t1), int(t1[::-1]), int(t2[::-1])
        m1 = str(v1 * r2)
        m2 = str(r1 * r2)
        
        p = get_substrings(m1).union(get_substrings(m2))
        p.update([x[::-1] for x in p])
        pairs.update(p)
        
    output.append(f"[\ud83d\udcc6 Predicting {curr_day} using {prev_day}]")
    output.append(f"  \u2794 Yesterday's Draws: {', '.join([x['tail'] for x in prev_draws])}")
    output.append(f"  \u2794 Generated Pair Pool: {len(pairs)} unique pairs.")
    
    for curr_draw in curr_draws:
        t3 = curr_draw['tail']
        t_ab, t_bc, t_ac = t3[:2], t3[1:], t3[0]+t3[2]
        
        hits = []
        if t_ab in pairs: hits.append(f"AB '{t_ab}'")
        if t_bc in pairs: hits.append(f"BC '{t_bc}'")
        if t_ac in pairs: hits.append(f"AC '{t_ac}'")
        
        if hits:
            output.append(f"     \u2705 {curr_draw['time']} Result '{t3}' -> HIT! Found {', '.join(hits)} in the pool!")
        else:
            output.append(f"     \u274c {curr_draw['time']} Result '{t3}' -> Missed.")
    output.append("")

print("\n".join(output))
