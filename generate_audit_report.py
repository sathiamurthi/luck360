#!/usr/bin/env python3
"""
Pattern Matching Audit Report Generator
Analyzes all historical draws in lottery.db and generates a detailed audit report:
WHEN (Date/Time), WHAT (Ticket/Tail), FOR WHAT PATTERN (Winning Pattern Name), HOW (Step-by-step math proof).
"""

import json
import sqlite3
import os

from db_manager import calc_all_patterns, sync_json

def generate_report():
    records = sync_json()
    audit_entries = []

    for i in range(len(records) - 1):
        prev = records[i]
        curr = records[i + 1]

        prev_tail = prev["tail"]
        curr_tail = curr["tail"]

        pats = calc_all_patterns(prev_tail)
        curr_sorted = "".join(sorted(curr_tail))

        for pat_name, pat_val in pats.items():
            pat_sorted = "".join(sorted(pat_val))
            match_type = None

            if pat_val == curr_tail:
                match_type = "EXACT STRAIGHT MATCH"
            elif pat_sorted == curr_sorted:
                match_type = "BOX PERMUTATION MATCH"

            if match_type:
                # Build HOW explanation
                d1, d2, d3 = int(prev_tail[0]), int(prev_tail[1]), int(prev_tail[2])
                how_desc = ""

                if "H2" in pat_name:
                    how_desc = f"1st digit = ({d1}+{d2})%10 = {(d1+d2)%10}, middle = {d3}, 2nd digit {d2} transformed to last"
                elif "H3" in pat_name:
                    how_desc = f"1st digit = ({d1}-{d2})%10 = {(d1-d2+10)%10}, middle = remainder digit {(d1+d2+d3)%10}, last digit = ({d1}-{d3})%10 = {(d1-d3+10)%10}"
                elif "H6" in pat_name:
                    how_desc = f"1st digit = ({d1}-{d2})%10 = {(d1-d2+10)%10}, 2nd digit = ({d1}+{d2}+1)%10 = {(d1+d2+1)%10}, 3rd digit = {d3} kept as it is"
                elif "H7" in pat_name:
                    how_desc = f"1st digit = ({d2}+1)%10 = {(d2+1)%10}, 2nd digit = ({d1}-{d2}-1)%10 = {(d1-d2-1+10)%10}, 3rd digit = ({d1}+{d3})%10 = {(d1+d3)%10}"
                elif "H8" in pat_name:
                    how_desc = f"1st digit = ({d1}+{d3}+1)%10 = {(d1+d3+1)%10}, 2nd digit = ({d1}+{d3}+1)%10 = {(d1+d3+1)%10}, 3rd digit = ({d2}+1)%10 = {(d2+1)%10}"
                elif "H9" in pat_name:
                    how_desc = f"1st digit = ({d3}-{d1}-1)%10 = {(d3-d1-1+10)%10}, 2nd digit = ({d1}+{d3}+1)%10 = {(d1+d3+1)%10}, 3rd digit = (10-{d1})%10 = {(10-d1)%10}"
                elif "H10" in pat_name:
                    how_desc = f"1st digit = ({d3}+5)%10 = {(d3+5)%10}, 2nd digit = (9-{d3})%10 = {(9-d3+10)%10}, 3rd digit = ({d3}-1)%10 = {(d3-1+10)%10}"
                elif "H11" in pat_name:
                    how_desc = f"1st digit = ({d1}+1)%10 = {(d1+1)%10}, 2nd digit = ({d1}+{d3}+1)%10 = {(d1+d3+1)%10}, 3rd digit = ({d1}+{d3})%10 = {(d1+d3)%10}"
                elif "H12" in pat_name:
                    how_desc = f"1st digit = ({d1}+2)%10 = {(d1+2)%10}, 2nd digit = ({d2}-3)%10 = {(d2-3+10)%10}, 3rd digit = ({d3}+5)%10 = {(d3+5)%10}"
                elif "P1" in pat_name:
                    how_desc = f"Reverse last 2 digits ({d3}{d2}) + difference ({d3}-{d1})%10 = {(d3-d1+10)%10}"
                elif "H4" in pat_name:
                    how_desc = f"First digit {d1} + Last digit {d3} + Middle {d2} OR Reverse AB pair ({d2}{d1}) + Last {d3}"
                else:
                    how_desc = f"Pattern conversion rule applied on base tail {prev_tail}"

                audit_entries.append({
                    "when": f"{curr['date']} ({curr['time']})",
                    "what": f"{curr['lottery']} -> Ticket {curr['ticket']} (Tail {curr_tail}) derived from previous tail {prev_tail}",
                    "pattern": f"{pat_name} ({match_type})",
                    "predicted": pat_val,
                    "actual": curr_tail,
                    "how": how_desc
                })

    return audit_entries

if __name__ == "__main__":
    report = generate_report()
    print("--- PATTERN MATCHING AUDIT REPORT ---")
    print(json.dumps(report, indent=2))
