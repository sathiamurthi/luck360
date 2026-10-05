def get_substrings(val_str, length=2):
    subs = set()
    for i in range(len(val_str) - length + 1):
        subs.add(val_str[i:i+length])
    if len(val_str) >= 2:
        subs.add(val_str[0] + val_str[-1])
        subs.add(val_str[-1] + val_str[0])
    return subs

import json
with open('draw_history.json') as f:
    d = json.load(f)

# Group by day
days = {}
for x in d:
    date = x['date']
    if date not in days: days[date] = []
    if len(x['tail']) == 3:
        days[date].append(x)

dates = sorted(days.keys())
for i in range(1, len(dates)):
    prev_day = dates[i-1]
    curr_day = dates[i]
    
    prev_draws = days[prev_day]
    curr_draws = days[curr_day]
    
    print(f"\n=== Predicting {curr_day} using {prev_day} ===")
    # Try all adjacent pairs in prev_day to predict ALL draws in curr_day
    for j in range(len(prev_draws) - 1):
        t1 = prev_draws[j]['tail']
        t2 = prev_draws[j+1]['tail']
        
        vt1 = int(t1)
        rt2 = int(t2[::-1])
        rt1 = int(t1[::-1])
        
        m1 = str(vt1 * rt2)
        m2 = str(rt1 * rt2)
        s = str(abs(int(t1) - int(t2))).zfill(3)
        
        m1_pairs = get_substrings(m1)
        m1_pairs.update([x[::-1] for x in m1_pairs])
        m2_pairs = get_substrings(m2)
        m2_pairs.update([x[::-1] for x in m2_pairs])
        
        all_pairs = m1_pairs.union(m2_pairs)
        
        print(f"\n  Prev Pairs: {t1} ({prev_draws[j]['time']}) and {t2} ({prev_draws[j+1]['time']})")
        print(f"  M1={m1}, M2={m2}, Pairs: {all_pairs}")
        print(f"  Sub=|{t1}-{t2}|={s}")
        
        for curr_draw in curr_draws:
            t3 = curr_draw['tail']
            ab = t3[:2]; bc = t3[1:]; ac = t3[0]+t3[2]
            targets = {ab, bc, ac, ab[::-1], bc[::-1], ac[::-1]}
            
            matches = all_pairs.intersection(targets)
            hit_s = [x for x in s if x in t3]
            
            if matches or hit_s:
                match_str = ", ".join(matches) if matches else "None"
                s_str = set(hit_s) if hit_s else "None"
                print(f"    -> HIT on {curr_draw['time']} ({t3}): Pairs={match_str}, SubDigits={s_str}")

