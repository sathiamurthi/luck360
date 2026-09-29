import sys
sys.stdout.reconfigure(encoding='utf-8')

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

all_transitions.append(("978", "398", "6PM yesterday -> 6PM today"))
all_transitions.append(("457", "226", "3PM yesterday -> 3PM today"))
all_transitions.append(("563", "051", "1PM yesterday -> 1PM today"))

# Test all permutations of digit offsets: (d_i + c1, d_j + c2, d_k + c3)
# To find patterns that achieve >= 3 hits (straight + box)
patterns_found = []

# Let's test single-digit offsets
for p in [(0,1,2), (2,1,0), (1,0,2), (0,2,1), (1,2,0), (2,0,1)]:
    for c1 in range(-3, 4):
        for c2 in range(-3, 4):
            for c3 in range(-3, 4):
                straight = 0
                box = 0
                matches = []
                for b, actual, desc in all_transitions:
                    digits = [int(b[0]), int(b[1]), int(b[2])]
                    r1 = (digits[p[0]] + c1 + 10) % 10
                    r2 = (digits[p[1]] + c2 + 10) % 10
                    r3 = (digits[p[2]] + c3 + 10) % 10
                    pred = f"{r1}{r2}{r3}"
                    if pred == actual:
                        straight += 1
                        matches.append((desc, b, actual, "STRAIGHT"))
                    elif sorted(pred) == sorted(actual):
                        box += 1
                        matches.append((desc, b, actual, "BOX"))
                total = straight + box
                if total >= 3 and straight >= 1:
                    name = f"Perm({p[0]+1},{p[1]+1},{p[2]+1})_Offset({c1:+d},{c2:+d},{c3:+d})"
                    patterns_found.append({
                        "name": name,
                        "p": p, "c1": c1, "c2": c2, "c3": c3,
                        "straight": straight,
                        "box": box,
                        "total": total,
                        "matches": matches
                    })

print(f"Total Star Patterns Found (>=3 hits): {len(patterns_found)}")
patterns_found.sort(key=lambda x: (x['straight'], x['total']), reverse=True)
for pf in patterns_found[:15]:
    print(f"{pf['name']}: Straight={pf['straight']}, Box={pf['box']}, Total={pf['total']}")
    for m in pf['matches']:
        print(f"   -> {m[3]}: {m[0]} ({m[1]} -> {m[2]})")
