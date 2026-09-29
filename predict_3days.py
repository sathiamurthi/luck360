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

    # USER PATTERN H6: (D1 - D2, D1 + D2 + 1, D3)
    n1 = (d1 - d2 + 10) % 10
    n2 = (d1 + d2 + 1) % 10
    n3 = d3
    h6 = f"{n1}{n2}{n3}"

    # 6 NEW IDENTIFIED PATTERNS (H7 to H12)
    h7 = f"{(d2 + 1) % 10}{(d1 - d2 - 1 + 10) % 10}{(d1 + d3) % 10}"
    h8 = f"{(d1 + d3 + 1) % 10}{(d1 + d3 + 1) % 10}{(d2 + 1) % 10}"
    h9 = f"{(d3 - d1 - 1 + 10) % 10}{(d1 + d3 + 1) % 10}{(10 - d1) % 10}"
    h10 = f"{(d3 + 5) % 10}{(9 - d3 + 10) % 10}{(d3 - 1 + 10) % 10}"
    h11 = f"{(d1 + 1) % 10}{(d1 + d3 + 1) % 10}{(d1 + d3) % 10}"
    h12 = f"{(d1 + 2) % 10}{(d2 - 3 + 10) % 10}{(d3 + 5) % 10}"

    # USER NEW PATTERN H13: Zero-Six Product Tens (Hits 500->053 Straight)
    map_0_6 = (d3 + 6) % 10
    prod13 = d1 * map_0_6
    d3_tens = (prod13 // 10) % 10 if prod13 >= 10 else prod13 % 10
    h13 = f"{d2}{d1}{d3_tens}"

    # USER NEW PATTERN H14: Prefix Difference Sandwich / 615 Pattern (Hits 053->615)
    h14 = f"{(d2 + 1) % 10}{(d1 + 1) % 10}{d2}"

    # USER NEW PATTERN H15: Shift-Difference Rule (Hits 398->053 Straight)
    h15 = f"{(d2 + 1) % 10}{(d3 - d1 + 10) % 10}{d1}"

    # USER NEW PATTERN H16: Twin-Echo Step Rule (Hits 615->626 Straight)
    h16 = f"{d1}{(d2 + 1) % 10}{(d3 + 1) % 10}"

    return {
        "H16_TwinEchoStep": h16,
        "H15_ShiftDiff": h15,
        "H13_ZeroSixProduct": h13,
        "H14_PrefixDiff_615": h14,
        "H7_DiffDiffSum": h7,
        "H8_OuterSumStep": h8,
        "H9_SubAddTen": h9,
        "H10_PartnerMirror": h10,
        "H11_SumPairPlus": h11,
        "H12_MirrorStep": h12,
        "H6_DiffSumPlusOne": h6,
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

def get_3day_predictions(starting_tail="398"):
    schedule = [
        # Day 1: Friday, Sept 25, 2026 8 PM (Upcoming)
        {"date": "2026-09-25", "day": "Friday", "time": "8:00 PM", "company": "Nagaland State Lottery", "lottery": "Dear Seagull Friday (8 PM)"},
        
        # Day 2: Saturday, Sept 26, 2026
        {"date": "2026-09-26", "day": "Saturday", "time": "1:00 PM", "company": "Nagaland State Lottery", "lottery": "Dear Star Saturday (1 PM)"},
        {"date": "2026-09-26", "day": "Saturday", "time": "3:00 PM", "company": "Kerala State Lotteries", "lottery": "Thirvonam Bumber (BR-111)"},
        {"date": "2026-09-26", "day": "Saturday", "time": "6:00 PM", "company": "Sikkim State Lottery", "lottery": "Dear Supreme Saturday (6 PM)"},
        {"date": "2026-09-26", "day": "Saturday", "time": "8:00 PM", "company": "Nagaland State Lottery", "lottery": "Dear Touchdown Saturday (8 PM)"},
        
        # Day 3: Sunday, Sept 27, 2026
        {"date": "2026-09-27", "day": "Sunday", "time": "1:00 PM", "company": "Nagaland State Lottery", "lottery": "Dear Star Sunday (1 PM)"},
        {"date": "2026-09-27", "day": "Sunday", "time": "3:00 PM", "company": "Kerala State Lotteries", "lottery": "Samrudhi (SM-74)"},
        {"date": "2026-09-27", "day": "Sunday", "time": "6:00 PM", "company": "Sikkim State Lottery", "lottery": "Dear Supreme Sunday (6 PM)"},
        {"date": "2026-09-27", "day": "Sunday", "time": "8:00 PM", "company": "Nagaland State Lottery", "lottery": "Dear Hawk Sunday (8 PM)"}
    ]

    curr_base = starting_tail
    predictions = []

    for slot in schedule:
        pats = calc_all(curr_base)
        
        # Star candidates
        top_h7 = pats["H7_DiffDiffSum"]
        top_h8 = pats["H8_OuterSumStep"]
        top_h9 = pats["H9_SubAddTen"]
        top_h6 = pats["H6_DiffSumPlusOne"]
        top_h2 = pats["H2_CrossSwap"]

        ab_pairs = [top_h7[:2], top_h8[:2], top_h9[:2], top_h6[:2], top_h2[:2]]
        bc_pairs = [top_h7[1:], top_h8[1:], top_h9[1:], top_h6[1:], top_h2[1:]]
        ac_pairs = [f"{top_h7[0]}{top_h7[2]}", f"{top_h8[0]}{top_h8[2]}", f"{top_h9[0]}{top_h9[2]}", f"{top_h6[0]}{top_h6[2]}", f"{top_h2[0]}{top_h2[2]}"]

        predictions.append({
            "date": slot["date"],
            "day": slot["day"],
            "time": slot["time"],
            "company": slot["company"],
            "lottery": slot["lottery"],
            "input_base_tail": curr_base,
            "top_3digit_guesses": [top_h7, top_h8, top_h9, top_h6, top_h2],
            "all_patterns": pats,
            "top_ab_pairs": list(dict.fromkeys(ab_pairs)),
            "top_bc_pairs": list(dict.fromkeys(bc_pairs)),
            "top_ac_pairs": list(dict.fromkeys(ac_pairs))
        })
        curr_base = top_h7

    return predictions

if __name__ == "__main__":
    preds = get_3day_predictions("221")
    print(json.dumps(preds, indent=2))
