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

# Test cross-digit building blocks:
terms = [
    ("d1", lambda d1, d2, d3: d1),
    ("d2", lambda d1, d2, d3: d2),
    ("d3", lambda d1, d2, d3: d3),
    ("d1+d2", lambda d1, d2, d3: d1 + d2),
    ("d2+d3", lambda d1, d2, d3: d2 + d3),
    ("d1+d3", lambda d1, d2, d3: d1 + d3),
    ("d1-d2", lambda d1, d2, d3: d1 - d2),
    ("d2-d3", lambda d1, d2, d3: d2 - d3),
    ("d3-d1", lambda d1, d2, d3: d3 - d1),
    ("d1+d2+d3", lambda d1, d2, d3: d1 + d2 + d3),
    ("9-d1", lambda d1, d2, d3: 9 - d1),
    ("9-d2", lambda d1, d2, d3: 9 - d2),
    ("9-d3", lambda d1, d2, d3: 9 - d3),
    ("d1+5", lambda d1, d2, d3: d1 + 5),
    ("d2+5", lambda d1, d2, d3: d2 + 5),
    ("d3+5", lambda d1, d2, d3: d3 + 5),
]

# We want 6 new patterns: H7, H8, H9, H10, H11, H12
# Let's test a targeted set of cross-digit combinations with offsets in [-2, 2]
results = []
for t1_name, t1_fn in terms:
    for t2_name, t2_fn in terms:
        for t3_name, t3_fn in terms:
            for o1 in [-1, 0, 1]:
                for o2 in [-1, 0, 1]:
                    for o3 in [-1, 0, 1]:
                        s = 0
                        b = 0
                        matches = []
                        for base, actual, desc in all_transitions:
                            d1, d2, d3 = int(base[0]), int(base[1]), int(base[2])
                            r1 = (t1_fn(d1, d2, d3) + o1) % 10
                            r2 = (t2_fn(d1, d2, d3) + o2) % 10
                            r3 = (t3_fn(d1, d2, d3) + o3) % 10
                            pred = f"{r1}{r2}{r3}"
                            if pred == actual:
                                s += 1
                                matches.append((desc, base, actual, "STRAIGHT"))
                            elif sorted(pred) == sorted(actual):
                                b += 1
                                matches.append((desc, base, actual, "BOX"))
                        tot = s + b
                        if s >= 2 and tot >= 3:
                            lbl = f"({t1_name}{o1:+d}, {t2_name}{o2:+d}, {t3_name}{o3:+d})"
                            results.append({
                                "label": lbl,
                                "s": s, "b": b, "tot": tot,
                                "matches": matches
                            })

print(f"Found {len(results)} high-performing rules with >= 2 Straight hits and >= 3 Total hits!")
results.sort(key=lambda x: (x['s'], x['tot']), reverse=True)
seen = set()
count = 0
for r in results:
    if count >= 20: break
    sig = tuple(sorted([m[1] + m[2] for m in r['matches']]))
    if sig in seen: continue
    seen.add(sig)
    count += 1
    print(f"\nRule #{count}: {r['label']} -> Straight={r['s']}, Box={r['b']}, Total={r['tot']}")
    for m in r['matches']:
        print(f"   -> {m[3]}: {m[0]} ({m[1]} -> {m[2]})")
