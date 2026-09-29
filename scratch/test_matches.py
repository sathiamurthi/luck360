import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from predict_3days import calc_all

with open('draw_history.json', 'r', encoding='utf-8') as f:
    draws = json.load(f)

print(f"Total draws in history: {len(draws)}")

# We have 6 patterns: H7, H9, H8, H11, H13, H6
patterns_to_check = [
    ('H7_DiffDiffSum', 'Star H7 (AB: 24)'),
    ('H9_SubAddTen', 'Star H9 (AB: 82)'),
    ('H8_OuterSumStep', 'Star H8 (AB: 22)'),
    ('H11_SumPairPlus', 'Pattern H11 (AB: 72)'),
    ('H13_ZeroSixProduct', 'Star H13 (AB: 16)'),
    ('H6_DiffSumPlusOne', 'Star H6 (AB: 58)')
]

for p_key, p_name in patterns_to_check:
    print(f"\n=== {p_name} ({p_key}) ===")
    matches = []
    for i in range(len(draws) - 1):
        prev_d = draws[i]
        curr_d = draws[i+1]
        prev_tail = prev_d['tail']
        curr_tail = curr_d['tail']
        projs = calc_all(prev_tail)
        pred = projs.get(p_key)
        
        # Check straight or box or AB pair match
        is_straight = (pred == curr_tail)
        is_box = sorted(pred) == sorted(curr_tail)
        ab_match = (pred[:2] == curr_tail[:2]) if pred else False
        
        if is_straight:
            matches.append({
                'transition': f"{prev_tail} -> {curr_tail}",
                'type': 'STRAIGHT HIT',
                'predicted': pred,
                'draw': f"{curr_d['date']} {curr_d['time']} ({curr_d['lottery'].split('-')[0].strip()})",
                'tail': curr_tail
            })
        elif is_box:
            matches.append({
                'transition': f"{prev_tail} -> {curr_tail}",
                'type': 'BOX HIT',
                'predicted': pred,
                'draw': f"{curr_d['date']} {curr_d['time']}",
                'tail': curr_tail
            })
        elif ab_match:
            matches.append({
                'transition': f"{prev_tail} -> {curr_tail}",
                'type': f"AB FRONT PAIR HIT ({pred[:2]})",
                'predicted': pred,
                'draw': f"{curr_d['date']} {curr_d['time']}",
                'tail': curr_tail
            })

    print(f"Total historical matches: {len(matches)}")
    for m in matches[-5:]:
        print(f"  * Tail {m['tail']} ({m['type']}) on {m['draw']} [from {m['transition']}, pred: {m['predicted']}]")
