import itertools
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Collect all transitions
cycle_draws = [
    ("2026-09-24 1PM", "563"),
    ("2026-09-24 3PM", "457"),
    ("2026-09-24 6PM", "978"),
    ("2026-09-24 8PM", "221"),
    ("2026-09-25 1PM", "051"),
    ("2026-09-25 3PM", "226"),
    ("2026-09-25 6PM", "398")
]

kerala_draws = [
    "288", "768", "280", "763", "700", "248", "140", "599", "236", "269",
    "822", "269", "979", "635", "460", "215", "207", "384", "700", "572",
    "457", "226"
]

all_transitions = []
for i in range(len(cycle_draws)-1):
    all_transitions.append((cycle_draws[i][1], cycle_draws[i+1][1], f"Cycle {cycle_draws[i][0]} -> {cycle_draws[i+1][0]}"))

for i in range(len(kerala_draws)-1):
    all_transitions.append((kerala_draws[i], kerala_draws[i+1], f"Kerala #{i+1} -> #{i+2}"))

# Also cross-day slot transitions:
# 6PM yesterday (978) -> 6PM today (398)
all_transitions.append(("978", "398", "6PM yesterday -> 6PM today"))
# 3PM yesterday (457) -> 3PM today (226)
all_transitions.append(("457", "226", "3PM yesterday -> 3PM today"))
# 1PM yesterday (563) -> 1PM today (051)
all_transitions.append(("563", "051", "1PM yesterday -> 1PM today"))

print(f"Total transitions under test: {len(all_transitions)}")

# Define pattern generator functions:
def eval_func(d1, d2, d3, code):
    # code is a string like "d1+d2", "d1-d2+10", "d3+1", "9-d1", "d1+5", etc.
    return eval(code, {}, {"d1": d1, "d2": d2, "d3": d3}) % 10

candidate_exprs = [
    "d1", "d2", "d3",
    "d1+1", "d2+1", "d3+1",
    "d1-1+10", "d2-1+10", "d3-1+10",
    "d1+2", "d2+2", "d3+2",
    "d1-2+10", "d2-2+10", "d3-2+10",
    "d1+5", "d2+5", "d3+5",
    "9-d1", "9-d2", "9-d3",
    "d1+d2", "d2+d3", "d1+d3",
    "d1-d2+10", "d2-d1+10", "d2-d3+10", "d3-d2+10", "d3-d1+10", "d1-d3+10",
    "d1+d2+1", "d2+d3+1", "d1+d3+1",
    "d1+d2+d3", "d1+d2+d3-1+10", "d1+d2+d3+1",
    "d1*d2", "d2*d3", "d1*d3"
]

# We want 6 meaningful, distinct patterns that have strong lottery math intuition:
# 1. H7_SumPairPlus: (d1+1, d1+d3+1, d1+d3) -> Hits 226 -> 398 (Straight!)
# 2. H8_MirrorOffset: (d1+2, d2-3+10, d3+5) -> Hits 051 -> 226 (Straight!) and 457 -> 226 (Box!)
# 3. H9_TriSumStep: (d1+1, d1+d2+d3-1+10, d3+2) -> Hits 226 -> 398 (Straight!)
# 4. H10_PartnerCut: (d1+5, d2+5, d3+5) -> Classic Cut/Partner 5-shift
# 5. H11_ComplementNine: (9-d1, 9-d2, 9-d3) -> 9-Complement rule
# 6. H12_DoubleDiffEnd: (d1-d2+10, d2-d3+10, d1+d3)
# Let's search across formulas to see which ones achieve the most hits (>=3 hits):

def test_pattern(f1, f2, f3):
    straight_hits = 0
    box_hits = 0
    match_list = []
    for b, actual, desc in all_transitions:
        d1, d2, d3 = int(b[0]), int(b[1]), int(b[2])
        try:
            p1 = eval(f1, {}, {"d1": d1, "d2": d2, "d3": d3}) % 10
            p2 = eval(f2, {}, {"d1": d1, "d2": d2, "d3": d3}) % 10
            p3 = eval(f3, {}, {"d1": d1, "d2": d2, "d3": d3}) % 10
            pred = f"{p1}{p2}{p3}"
            if pred == actual:
                straight_hits += 1
                match_list.append((desc, b, actual, "STRAIGHT"))
            elif sorted(pred) == sorted(actual):
                box_hits += 1
                match_list.append((desc, b, actual, "BOX"))
        except:
            pass
    return straight_hits, box_hits, match_list

# Test a broad library of curated domain formulas
curated_patterns = [
    # Patterns that directly solve 3 PM (226) and 6 PM (398)
    ("H7_SumPairPlus", "d1+1", "d1+d3+1", "d1+d3", "D1+1, D1+D3+1, D1+D3 (Hits 226->398 Straight)"),
    ("H8_MirrorOffset", "d1+2", "d2-3+10", "d3+5", "D1+2, D2-3, D3+5 (Hits 051->226 Straight)"),
    ("H9_TriSumStep", "d1+d2-1+10", "d1+d2+d3-1+10", "d2+d3", "D1+D2-1, TriSum-1, D2+D3 (Hits 226->398)"),
    ("H10_PartnerCut", "d1+5", "d2+5", "d3+5", "Cut/Partner 5-Shift (+5,+5,+5)"),
    ("H11_CompNine", "9-d1", "9-d2", "9-d3", "9-Complement Reflection (9-D1, 9-D2, 9-D3)"),
    ("H12_CrossDiffSum", "d1-d2+10", "d2+d3", "d1+d3", "D1-D2, D2+D3, D1+D3 (Cross Diff-Sum)"),
    ("H13_RevEndAdd", "d3", "d2+1", "d1+2", "Reversed Tail with Step Offset (D3, D2+1, D1+2)"),
    ("H14_AdjacentCross", "d1+d2", "d2+d3", "d1", "Adjacent Sums + First Digit (D1+D2, D2+D3, D1)"),
    ("H15_DiffPairLast", "d3-d1+10", "d3-d2+10", "d3", "Difference from Last Digit (D3-D1, D3-D2, D3)"),
    ("H16_StepShift", "d1+2", "d2+2", "d3-1+10", "Double Step Forward, Single Back (+2, +2, -1)"),
    ("H17_CenterMirror", "d1", "9-d2", "d3", "Center Digit 9-Complement Mirror (D1, 9-D2, D3)"),
    ("H18_LastPartner", "d1", "d2", "d3+5", "Last Digit Partner 5-Shift (D1, D2, D3+5)")
]

top_star_candidates = []
for name, f1, f2, f3, desc in curated_patterns:
    s, b, matches = test_pattern(f1, f2, f3)
    total = s + b
    is_star = total >= 3
    top_star_candidates.append({
        "name": name,
        "f1": f1, "f2": f2, "f3": f3,
        "desc": desc,
        "straight": s,
        "box": b,
        "total": total,
        "star": is_star,
        "matches": matches
    })

print("\n--- RESULTS OF CANDIDATE PATTERNS ---")
for c in sorted(top_star_candidates, key=lambda x: (x['straight'], x['total']), reverse=True):
    star_badge = "★ STAR MATCH (>=3 HITS)" if c['star'] else ("HOT" if c['total'] >= 1 else "TRACK")
    print(f"\n{c['name']} [{star_badge}]: Straight={c['straight']}, Box={c['box']}, Total={c['total']}")
    print(f"  Formula: {c['desc']}")
    for m in c['matches']:
        print(f"    -> {m[3]}: {m[0]} ({m[1]} -> {m[2]})")
