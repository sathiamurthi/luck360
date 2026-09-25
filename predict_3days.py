#!/usr/bin/env python3
"""
3-Day Pattern Prediction Engine
Generates exact 3-digit tail projections and top AB, BC, AC pairs
for the next 3 days (Sept 25, Sept 26, Sept 27, 2026) across all draw slots.
"""

import json

def transform_58(d):
    trans_map = {5: 8, 8: 5, 7: 2, 2: 7, 6: 4, 4: 6, 9: 0, 0: 9, 1: 3, 3: 1}
    return trans_map.get(d, (d + 3) % 10)

def row60_trans(d):
    if d == 7: return 5
    if d == 0: return 9
    if d == 5: return 7
    if d == 9: return 0
    return (d + 1) % 10

def calc_all(tail):
    d1 = int(tail[0])
    d2 = int(tail[1])
    d3 = int(tail[2])

    p1 = f"{(d3)}{(d2)}{(d3 - d1 + 10) % 10}"
    p2 = f"{(d1)}{(d2 + 1) % 10}{(d3 - 1 + 10) % 10}"
    p3 = f"{(d2)}{(d1)}{(d3)}"
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
        "H2_CrossSwap": h2,
        "H3_DiffRem": h3,
        "H4_FirstLast": h4_a,
        "H1_IncShift": h1,
        "P1_RevDiff": p1,
        "P2_KeepConv": p2,
        "P3_RevAB": p3,
        "Row41_Offset": r41,
        "Row60_Rule": r60
    }

def get_3day_predictions(starting_tail="221"):
    schedule = [
        # Day 1: Friday, Sept 25, 2026
        {"date": "2026-09-25", "day": "Friday", "time": "1:00 PM", "company": "Nagaland State Lottery", "lottery": "Dear Star Friday"},
        {"date": "2026-09-25", "day": "Friday", "time": "3:00 PM", "company": "Kerala State Lotteries", "lottery": "Nirmal (NR-412)"},
        {"date": "2026-09-25", "day": "Friday", "time": "6:00 PM", "company": "Sikkim State Lottery", "lottery": "Dear Supreme Friday"},
        {"date": "2026-09-25", "day": "Friday", "time": "8:00 PM", "company": "Nagaland State Lottery", "lottery": "Dear Seagull Friday"},
        
        # Day 2: Saturday, Sept 26, 2026
        {"date": "2026-09-26", "day": "Saturday", "time": "1:00 PM", "company": "Nagaland State Lottery", "lottery": "Dear Star Saturday"},
        {"date": "2026-09-26", "day": "Saturday", "time": "3:00 PM", "company": "Kerala State Lotteries", "lottery": "Karunya (KR-770)"},
        {"date": "2026-09-26", "day": "Saturday", "time": "6:00 PM", "company": "Sikkim State Lottery", "lottery": "Dear Supreme Saturday"},
        {"date": "2026-09-26", "day": "Saturday", "time": "8:00 PM", "company": "Nagaland State Lottery", "lottery": "Dear Touchdown Saturday"},
        
        # Day 3: Sunday, Sept 27, 2026
        {"date": "2026-09-27", "day": "Sunday", "time": "1:00 PM", "company": "Nagaland State Lottery", "lottery": "Dear Star Sunday"},
        {"date": "2026-09-27", "day": "Sunday", "time": "3:00 PM", "company": "Kerala State Lotteries", "lottery": "Akshaya (AK-668)"},
        {"date": "2026-09-27", "day": "Sunday", "time": "6:00 PM", "company": "Sikkim State Lottery", "lottery": "Dear Supreme Sunday"},
        {"date": "2026-09-27", "day": "Sunday", "time": "8:00 PM", "company": "Nagaland State Lottery", "lottery": "Dear Hawk Sunday"}
    ]

    curr_base = starting_tail
    predictions = []

    for slot in schedule:
        pats = calc_all(curr_base)
        
        # Main candidates
        top_h2 = pats["H2_CrossSwap"]
        top_h3 = pats["H3_DiffRem"]
        top_h4 = pats["H4_FirstLast"]
        top_h1 = pats["H1_IncShift"]

        ab_pairs = [top_h2[:2], top_h3[:2], top_h4[:2], top_h1[:2]]
        bc_pairs = [top_h2[1:], top_h3[1:], top_h4[1:], top_h1[1:]]
        ac_pairs = [f"{top_h2[0]}{top_h2[2]}", f"{top_h3[0]}{top_h3[2]}", f"{top_h4[0]}{top_h4[2]}", f"{top_h1[0]}{top_h1[2]}"]

        predictions.append({
            "date": slot["date"],
            "day": slot["day"],
            "time": slot["time"],
            "company": slot["company"],
            "lottery": slot["lottery"],
            "input_base_tail": curr_base,
            "top_3digit_guesses": [top_h2, top_h3, top_h4, top_h1],
            "all_patterns": pats,
            "top_ab_pairs": list(dict.fromkeys(ab_pairs)),
            "top_bc_pairs": list(dict.fromkeys(bc_pairs)),
            "top_ac_pairs": list(dict.fromkeys(ac_pairs))
        })
        curr_base = top_h2

    return predictions

if __name__ == "__main__":
    preds = get_3day_predictions("221")
    print(json.dumps(preds, indent=2))
