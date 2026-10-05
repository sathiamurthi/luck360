import json
from collections import defaultdict
import report_analytics

with open('draw_history.json', 'r') as f:
    history = json.load(f)

def time_to_slot(t):
    if '1:00' in t: return 1
    if '3:00' in t: return 2
    if '6:00' in t: return 3
    if '8:00' in t: return 4
    return 0

history = sorted(history, key=lambda x: (x['date'], time_to_slot(x['time'])))

pair_rules = defaultdict(int)

for i in range(1, len(history)):
    prev = history[i-1]
    curr = history[i]
    
    prev_res = str(prev['tail']).zfill(3)[-3:]
    curr_res = str(curr['tail']).zfill(3)[-3:]
    
    pats = report_analytics.calc_all_patterns(prev_res, prev.get('ticket', ''))
    
    ab = curr_res[0:2]
    bc = curr_res[1:3]
    ac = curr_res[0] + curr_res[2]
    
    for p1_key, p1_obj in pats.items():
        for p2_key, p2_obj in pats.items():
            val1 = p1_obj['val']
            val2 = p2_obj['val']
            if not val1 or not val2: continue
            
            # Form pairs by concatenating last digits
            combo = val1[-1] + val2[-1]
            
            if combo == ab:
                pair_rules[f"{p1_key}[2] + {p2_key}[2] -> AB"] += 1
            if combo == bc:
                pair_rules[f"{p1_key}[2] + {p2_key}[2] -> BC"] += 1
            if combo == ac:
                pair_rules[f"{p1_key}[2] + {p2_key}[2] -> AC"] += 1
            
            # Form pairs by concatenating FIRST digits
            combo_first = val1[0] + val2[0]
            if combo_first == ab:
                pair_rules[f"{p1_key}[0] + {p2_key}[0] -> AB"] += 1
            if combo_first == bc:
                pair_rules[f"{p1_key}[0] + {p2_key}[0] -> BC"] += 1
            if combo_first == ac:
                pair_rules[f"{p1_key}[0] + {p2_key}[0] -> AC"] += 1

sorted_rules = sorted(pair_rules.items(), key=lambda x: x[1], reverse=True)
print("TOP 20 RULES:")
for k, v in sorted_rules[:20]:
    print(f"{k}: {v} hits")
