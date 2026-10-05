import json
from collections import defaultdict

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

for i in range(len(dates)-3, len(dates)):
    prev_day = dates[i-1]
    curr_day = dates[i]
    
    prev_draws = days[prev_day]
    curr_draws = days[curr_day]
    
    if len(prev_draws) < 2:
        continue
        
    pairs = set()
    sub_pool = []
    
    for j in range(len(prev_draws) - 1):
        t1 = prev_draws[j]['tail']
        t2 = prev_draws[j+1]['tail']
        
        v1, r1, r2 = int(t1), int(t1[::-1]), int(t2[::-1])
        m1 = str(v1 * r2)
        m2 = str(r1 * r2)
        
        p = get_substrings(m1).union(get_substrings(m2))
        p.update([x[::-1] for x in p])
        pairs.update(p)
        
        s = str(abs(int(t1) - int(t2))).zfill(3)
        weight = j + 1
        sub_pool.extend(list(s) * weight)
        
    sub_counts = {digit: sub_pool.count(digit) for digit in set(sub_pool)}
    
    scores = []
    for num in range(1000):
        abc = str(num).zfill(3)
        ab, bc, ac = abc[:2], abc[1:], abc[0]+abc[2]
        
        pair_score = 0
        if ab in pairs: pair_score += 1
        if bc in pairs: pair_score += 1
        if ac in pairs: pair_score += 1
        
        if pair_score == 0:
            continue
            
        sub_score = 0
        if abc[0] in sub_counts: sub_score += sub_counts[abc[0]] * 0.32
        if abc[1] in sub_counts: sub_score += sub_counts[abc[1]] * 0.44
        if abc[2] in sub_counts: sub_score += sub_counts[abc[2]] * 0.50
        
        total_score = (pair_score * 50) + sub_score
        scores.append((total_score, abc, ab in pairs, bc in pairs, ac in pairs))
        
    scores.sort(reverse=True, key=lambda x: x[0])
    top_5 = scores[:5]
    
    output.append(f"\n=== PREDICTING {curr_day} USING {prev_day} ===")
    output.append(f"1. Yesterday's Draws: {', '.join([x['tail'] for x in prev_draws])}")
    
    hot_subs = sorted(sub_counts.items(), key=lambda x: -x[1])[:3]
    output.append(f"2. Hot Subtraction Digits (Weighted): {', '.join([f'{k}(w:{v})' for k,v in hot_subs])}")
    
    output.append(f"3. Top 5 Generated Targets:")
    for s in top_5:
        output.append(f"   -> [{s[1]}] (Score {s[0]:.1f}) | Pairs Built: AB({s[1][:2]}) BC({s[1][1:]}) AC({s[1][0]+s[1][2]})")
        
    output.append(f"4. ACTUAL RESULTS ON {curr_day}:")
    for curr_draw in curr_draws:
        t3 = curr_draw['tail']
        t_ab, t_bc, t_ac = t3[:2], t3[1:], t3[0]+t3[2]
        
        matches = []
        for s in top_5:
            pred = s[1]
            p_ab, p_bc, p_ac = pred[:2], pred[1:], pred[0]+pred[2]
            
            if p_ab == t_ab: matches.append(f"[{pred}] hit AB pair '{t_ab}'!")
            if p_bc == t_bc: matches.append(f"[{pred}] hit BC pair '{t_bc}'!")
            if p_ac == t_ac: matches.append(f"[{pred}] hit AC pair '{t_ac}'!")
            
        if matches:
            output.append(f"   [HIT] {curr_draw['time']} Result: {t3} -> {', '.join(matches)}")
        else:
            output.append(f"   [MISS] {curr_draw['time']} Result: {t3} -> No pairs matched from Top 5.")

print("\n".join(output))

