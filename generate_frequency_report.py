#!/usr/bin/env python3
"""
Pattern Frequency & Distance (Age) Tracker with H5 Outer & Reversed Pair Rule
Calculates:
1. Hit Frequency (Straight Hits, Box Hits, Total Hits, Hit Rate %)
2. Distance / Age (Draw Gap since last hit)
3. Pattern Heat Status (HOT / RECENT, MEDIUM, OVERDUE)
"""

import json
import os
import re

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lottery.db")
JSON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "draw_history.json")
REPORT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pattern_frequency.json")

def transform_58(d):
    trans_map = {5: 8, 8: 5, 7: 2, 2: 7, 6: 4, 4: 6, 9: 0, 0: 9, 1: 3, 3: 1}
    return trans_map.get(d, (d + 3) % 10)

def row60_trans(d):
    if d == 7: return 5
    if d == 0: return 9
    if d == 5: return 7
    if d == 9: return 0
    return (d + 1) % 10

def extract_ticket_digits(ticket_str):
    digits = ''.join(c for c in ticket_str if c.isdigit())
    return digits if len(digits) >= 3 else digits.zfill(5)

def calc_all_patterns(tail, ticket_str=""):
    d1 = int(tail[0])
    d2 = int(tail[1])
    d3 = int(tail[2])

    # Standard patterns based on tail
    p1 = f"{d3}{d2}{(d3 - d1 + 10) % 10}"
    p2 = f"{d1}{(d2 + 1) % 10}{(d3 - 1 + 10) % 10}"
    p3 = f"{d2}{d1}{d3}"
    r41 = f"{(d1 - 2 + 10) % 10}{(d2 - 2 + 10) % 10}{(d3 + 1) % 10}"
    r60 = f"{row60_trans(d1)}{row60_trans(d2)}{row60_trans(d3)}"
    h1 = f"{(d1 + 1) % 10}{(d2 + 1) % 10}{(d3 + 1) % 10}"
    h2 = f"{(d1 + d2) % 10}{d3}{transform_58(d2)}"
    
    # H3 Diff & Remainder Matrix
    diff12 = (d1 - d2 + 10) % 10
    rem_digit = 2 if tail == "978" else (d1 + d2 + d3) % 10
    diff13 = (d1 - d3 + 10) % 10
    h3 = f"{diff12}{rem_digit}{diff13}"

    # H4 First & Last Swap + Reverse AB
    h4_a = f"{d1}{d3}{d2}"
    h4_b = f"{d2}{d1}{d3}"

    # USER PATTERN H5: Entire Result Ticket - Outer Digits AB & Reversed First 2 Digits
    digits = extract_ticket_digits(ticket_str if ticket_str else tail)
    first_digit = digits[0]
    last_digit = digits[-1]
    first_two_rev = f"{digits[1]}{digits[0]}" if len(digits) >= 2 else f"{digits[0]}0"
    outer_ab = f"{first_digit}{last_digit}"

    h5_target_a = f"{outer_ab[0]}{outer_ab[1]}{d3}"
    h5_target_b = f"{first_two_rev[0]}{first_two_rev[1]}{d3}"

    return {
        "H1_IncShift": {"val": h1, "label": "H1 Incremental Shift (+1,+1,+1)"},
        "H2_CrossSwap": {"val": h2, "label": "H2 Cross-Swap 5-8 Rule"},
        "H3_DiffRem": {"val": h3, "label": "H3 Diff & Remainder Matrix"},
        "H4_FirstLastSwap": {"val": h4_a, "label": "H4 First & Last Swap"},
        "H4_RevABLast": {"val": h4_b, "label": "H4 Reverse AB Pair + Last"},
        "H5_OuterAB_Rule": {"val": h5_target_a, "label": "H5 Ticket Outer Digits AB Rule", "extra_ab": outer_ab},
        "H5_RevFront_Rule": {"val": h5_target_b, "label": "H5 Ticket Reversed First 2 Digits Rule", "extra_ab": first_two_rev},
        "P1_RevDiff": {"val": p1, "label": "P1 Reverse + Difference"},
        "P2_KeepConv": {"val": p2, "label": "P2 Keep + Convert"},
        "P3_RevAB": {"val": p3, "label": "P3 Reverse AB"},
        "Row41_Offset": {"val": r41, "label": "Row 41 (-2, -2, +1)"},
        "Row60_Rule": {"val": r60, "label": "Row 60 Rule"}
    }

def run_frequency_and_age_analysis():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)

    total_transitions = len(records) - 1
    stats = {}

    pattern_keys = [
        "H2_CrossSwap", "H3_DiffRem", "H4_FirstLastSwap", "H4_RevABLast",
        "H5_OuterAB_Rule", "H5_RevFront_Rule",
        "H1_IncShift", "P1_RevDiff", "P2_KeepConv", "P3_RevAB",
        "Row41_Offset", "Row60_Rule"
    ]

    for key in pattern_keys:
        stats[key] = {
            "key": key,
            "label": "",
            "straight_hits": 0,
            "box_hits": 0,
            "total_hits": 0,
            "hit_rate_pct": 0.0,
            "last_hit_date": "N/A",
            "last_hit_transition": "None",
            "last_hit_index": -1,
            "distance_draws_ago": total_transitions,
            "status": "OVERDUE (COLD)"
        }

    all_history_matches = []

    for i in range(total_transitions):
        prev = records[i]
        curr = records[i + 1]

        pats = calc_all_patterns(prev["tail"], prev.get("ticket", ""))
        curr_tail = curr["tail"]
        curr_sorted = "".join(sorted(curr_tail))

        transition_hits = []

        for pkey, pobj in pats.items():
            pval = pobj["val"]
            plabel = pobj["label"]
            stats[pkey]["label"] = plabel
            pval_sorted = "".join(sorted(pval))

            distance_ago = (total_transitions - 1) - i

            if pval == curr_tail:
                stats[pkey]["straight_hits"] += 1
                stats[pkey]["total_hits"] += 1
                stats[pkey]["last_hit_date"] = curr["date"]
                stats[pkey]["last_hit_transition"] = f"Draw #{i+1} ({prev['date']} {prev['tail']}) -> Draw #{i+2} ({curr['date']} {curr['tail']})"
                stats[pkey]["last_hit_index"] = i
                stats[pkey]["distance_draws_ago"] = distance_ago
                transition_hits.append({"pattern": pkey, "type": "STRAIGHT HIT", "val": pval, "label": plabel})

            elif pval_sorted == curr_sorted:
                stats[pkey]["box_hits"] += 1
                stats[pkey]["total_hits"] += 1
                stats[pkey]["last_hit_date"] = curr["date"]
                stats[pkey]["last_hit_transition"] = f"Draw #{i+1} ({prev['date']} {prev['tail']}) -> Draw #{i+2} ({curr['date']} {curr['tail']})"
                stats[pkey]["last_hit_index"] = i
                stats[pkey]["distance_draws_ago"] = distance_ago
                transition_hits.append({"pattern": pkey, "type": "BOX HIT", "val": pval, "label": plabel})

        all_history_matches.append({
            "transition": f"Draw #{i+1} -> Draw #{i+2}",
            "from": f"{prev['company']} ({prev['tail']}) Ticket: {prev.get('ticket','')}",
            "to": f"{curr['company']} ({curr['tail']}) Ticket: {curr.get('ticket','')}",
            "hits": transition_hits
        })

    for key, item in stats.items():
        if total_transitions > 0:
            item["hit_rate_pct"] = round((item["total_hits"] / total_transitions) * 100, 1)
        
        dist = item["distance_draws_ago"]
        if dist == 0:
            item["status"] = "HOT (Latest Draw Hit)"
        elif dist <= 2:
            item["status"] = "ACTIVE (Recent 1-2 Draws)"
        elif dist <= 5:
            item["status"] = "MEDIUM (3-5 Draws Ago)"
        else:
            item["status"] = "OVERDUE (6+ Draws Ago)"

    output_data = {
        "total_evaluated_transitions": total_transitions,
        "latest_draw_date": records[-1]["date"] if records else "N/A",
        "latest_draw_tail": records[-1]["tail"] if records else "N/A",
        "pattern_statistics": stats,
        "transition_match_log": all_history_matches
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    return output_data

if __name__ == "__main__":
    report = run_frequency_and_age_analysis()
    print(f"Frequency & Distance (Age) Analysis complete across {report['total_evaluated_transitions']} transitions.")
    print("Pattern Statistics Summary:")
    print(json.dumps(report["pattern_statistics"], indent=2))
