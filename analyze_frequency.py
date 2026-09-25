import json
import os

json_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "draw_history.json")
with open(json_file, "r", encoding="utf-8") as f:
    records = json.load(f)

def transform_58(d):
    trans_map = {5: 8, 8: 5, 7: 2, 2: 7, 6: 4, 4: 6, 9: 0, 0: 9, 1: 3, 3: 1}
    return trans_map.get(d, (d + 3) % 10)

def row60_trans(d):
    if d == 7: return 5
    if d == 0: return 9
    if d == 5: return 7
    if d == 9: return 0
    return (d + 1) % 10

def calc_all_patterns(tail):
    d1 = int(tail[0])
    d2 = int(tail[1])
    d3 = int(tail[2])

    p1 = f"{d3}{d2}{(d3 - d1 + 10) % 10}"
    p2 = f"{d1}{(d2 + 1) % 10}{(d3 - 1 + 10) % 10}"
    p3 = f"{d2}{d1}{d3}"
    r41 = f"{(d1 - 2 + 10) % 10}{(d2 - 2 + 10) % 10}{(d3 + 1) % 10}"
    r60 = f"{row60_trans(d1)}{row60_trans(d2)}{row60_trans(d3)}"
    h1 = f"{(d1 + 1) % 10}{(d2 + 1) % 10}{(d3 + 1) % 10}"
    h2 = f"{(d1 + d2) % 10}{d3}{transform_58(d2)}"
    
    diff12 = (d1 - d2 + 10) % 10
    rem_digit = (d1 + d2 + d3) % 10
    diff13 = (d1 - d3 + 10) % 10
    h3 = f"{diff12}{rem_digit}{diff13}"
    h4_a = f"{d1}{d3}{d2}"
    h4_b = f"{d2}{d1}{d3}"

    return {
        "H1_IncShift": h1,
        "H2_CrossSwap": h2,
        "H3_DiffRem": h3,
        "H4_FirstLastSwap": h4_a,
        "H4_RevABLast": h4_b,
        "P1_RevDiff": p1,
        "P2_KeepConv": p2,
        "P3_RevAB": p3,
        "Row41_Offset": r41,
        "Row60_Rule": r60
    }

total_transitions = len(records) - 1
pattern_stats = {}

pattern_names = [
    "H1_IncShift", "H2_CrossSwap", "H3_DiffRem", "H4_FirstLastSwap", "H4_RevABLast",
    "P1_RevDiff", "P2_KeepConv", "P3_RevAB", "Row41_Offset", "Row60_Rule"
]

for name in pattern_names:
    pattern_stats[name] = {
        "straight_hits": 0,
        "box_hits": 0,
        "total_hits": 0,
        "last_hit_transition": None,
        "last_hit_date": None,
        "distance_age_draws": total_transitions # Draws ago since last hit
    }

for i in range(total_transitions):
    prev = records[i]
    curr = records[i + 1]
    
    pats = calc_all_patterns(prev["tail"])
    curr_tail = curr["tail"]
    curr_sorted = "".join(sorted(curr_tail))

    for name, val in pats.items():
        val_sorted = "".join(sorted(val))
        distance_ago = (total_transitions - 1) - i
        if val == curr_tail:
            pattern_stats[name]["straight_hits"] += 1
            pattern_stats[name]["total_hits"] += 1
            pattern_stats[name]["last_hit_date"] = curr["date"]
            pattern_stats[name]["last_hit_transition"] = f"Draw #{i+1} ({prev['tail']}) -> Draw #{i+2} ({curr['tail']})"
            pattern_stats[name]["distance_age_draws"] = distance_ago
        elif val_sorted == curr_sorted:
            pattern_stats[name]["box_hits"] += 1
            pattern_stats[name]["total_hits"] += 1
            pattern_stats[name]["last_hit_date"] = curr["date"]
            pattern_stats[name]["last_hit_transition"] = f"Draw #{i+1} ({prev['tail']}) -> Draw #{i+2} ({curr['tail']})"
            pattern_stats[name]["distance_age_draws"] = distance_ago

print("--- PATTERN FREQUENCY & DISTANCE (AGE) REPORT ---")
print(f"Total Evaluated Transitions: {total_transitions}")
print(json.dumps(pattern_stats, indent=2))
