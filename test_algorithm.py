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

total_curr_draws = 0
hit_ab = 0
hit_bc = 0
hit_ac = 0
hit_any_pair = 0
hit_exact = 0

# Keep track of exact hits to print them out!
exact_hits_log = []

for i in range(1, len(dates)):
    prev_day = dates[i-1]
    curr_day = dates[i]
    
    prev_draws = days[prev_day]
    curr_draws = days[curr_day]
    
    if len(prev_draws) < 2:
        continue
        
    pairs = set()
    sub_pool = []
    
    # Weight recent draws higher
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
        weight = j + 1 # more recent = higher weight
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
        scores.append((total_score, abc, ab, bc, ac))
        
    scores.sort(reverse=True, key=lambda x: x[0])
    top_5 = [s[1] for s in scores[:5]]
    
    # Evaluate against today's draws
    for curr_draw in curr_draws:
        total_curr_draws += 1
        t3 = curr_draw['tail']
        t_ab, t_bc, t_ac = t3[:2], t3[1:], t3[0]+t3[2]
        
        match_ab = False
        match_bc = False
        match_ac = False
        match_exact = False
        
        for pred in top_5:
            p_ab, p_bc, p_ac = pred[:2], pred[1:], pred[0]+pred[2]
            
            if p_ab == t_ab: match_ab = True
            if p_bc == t_bc: match_bc = True
            if p_ac == t_ac: match_ac = True
            
            # Also allow reverse matching for pairs? The user asked for AB, BC, AC match. Let's stick to exact position first, or both? 
            # Usually AB means exact first two digits. I'll stick to exact positional pairs for strictness.
            
            if pred == t3: 
                match_exact = True
                exact_hits_log.append(f"[{curr_day} {curr_draw['time']}] Predicted {pred} perfectly!")
                
        if match_ab: hit_ab += 1
        if match_bc: hit_bc += 1
        if match_ac: hit_ac += 1
        if match_ab or match_bc or match_ac: hit_any_pair += 1
        if match_exact: hit_exact += 1

print("=== HISTORICAL BACKTEST RESULTS ===")
print(f"Total draws evaluated: {total_curr_draws}")
print(f"\n--- PAIR MATCHES (From the Top 5 Predictions) ---")
print(f"AB Pair Hit: {hit_ab}/{total_curr_draws} ({hit_ab/total_curr_draws*100:.1f}%)")
print(f"BC Pair Hit: {hit_bc}/{total_curr_draws} ({hit_bc/total_curr_draws*100:.1f}%)")
print(f"AC Pair Hit: {hit_ac}/{total_curr_draws} ({hit_ac/total_curr_draws*100:.1f}%)")
print(f"ANY Pair Hit: {hit_any_pair}/{total_curr_draws} ({hit_any_pair/total_curr_draws*100:.1f}%)")
print(f"\n--- EXACT 3-DIGIT MATCHES ---")
print(f"Exact ABC Hit: {hit_exact}/{total_curr_draws} ({hit_exact/total_curr_draws*100:.1f}%)")
for log in exact_hits_log:
    print(f"  \u2b50 {log}")

