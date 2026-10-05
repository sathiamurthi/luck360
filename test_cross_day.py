import json
from collections import defaultdict

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

total_curr_draws = 0
hit_any_pair = 0
hit_any_sub = 0

sub_position_counts = {'A': 0, 'B': 0, 'C': 0}

for i in range(1, len(dates)):
    prev_day = dates[i-1]
    curr_day = dates[i]
    
    prev_draws = days[prev_day]
    curr_draws = days[curr_day]
    
    # Calculate yesterday's pools
    yesterday_pairs = set()
    yesterday_sub_digits = set()
    
    for j in range(len(prev_draws) - 1):
        t1 = prev_draws[j]['tail']
        t2 = prev_draws[j+1]['tail']
        
        vt1 = int(t1)
        rt2 = int(t2[::-1])
        rt1 = int(t1[::-1])
        
        m1 = str(vt1 * rt2)
        m2 = str(rt1 * rt2)
        s = str(abs(int(t1) - int(t2))).zfill(3)
        
        # Add to pairs pool
        def add_subs(val_str):
            for k in range(len(val_str) - 1):
                yesterday_pairs.add(val_str[k:k+2])
                yesterday_pairs.add(val_str[k:k+2][::-1])
            if len(val_str) >= 2:
                yesterday_pairs.add(val_str[0] + val_str[-1])
                yesterday_pairs.add(val_str[-1] + val_str[0])
        add_subs(m1)
        add_subs(m2)
        
        # Add to sub digits pool
        yesterday_sub_digits.update(list(s))
        
    # Now check today's draws against yesterday's pools
    for curr_draw in curr_draws:
        total_curr_draws += 1
        t3 = curr_draw['tail']
        
        ab = t3[:2]; bc = t3[1:]; ac = t3[0]+t3[2]
        targets = {ab, bc, ac, ab[::-1], bc[::-1], ac[::-1]}
        
        if targets.intersection(yesterday_pairs):
            hit_any_pair += 1
            
        a, b, c = t3[0], t3[1], t3[2]
        
        hit_sub = False
        if a in yesterday_sub_digits:
            sub_position_counts['A'] += 1
            hit_sub = True
        if b in yesterday_sub_digits:
            sub_position_counts['B'] += 1
            hit_sub = True
        if c in yesterday_sub_digits:
            sub_position_counts['C'] += 1
            hit_sub = True
            
        if hit_sub:
            hit_any_sub += 1

print(f"Total draws analyzed (excluding first day): {total_curr_draws}")
print(f"Draws where Yesterday's M1/M2 contained AB, BC, or AC: {hit_any_pair} ({hit_any_pair/total_curr_draws*100:.1f}%)")
print(f"Draws where Yesterday's Subtraction contained a winning digit: {hit_any_sub} ({hit_any_sub/total_curr_draws*100:.1f}%)")
print(f"  -> Hits in Position A (1st Digit): {sub_position_counts['A']} times ({sub_position_counts['A']/total_curr_draws*100:.1f}%)")
print(f"  -> Hits in Position B (2nd Digit): {sub_position_counts['B']} times ({sub_position_counts['B']/total_curr_draws*100:.1f}%)")
print(f"  -> Hits in Position C (3rd Digit): {sub_position_counts['C']} times ({sub_position_counts['C']/total_curr_draws*100:.1f}%)")

