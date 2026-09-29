import json
import sqlite3

# Let's inspect the exact transitions
# Today:
# Base 226 (Kerala 3 PM) -> 398 (Dear 6 PM)
# Base 051 (Dear 1 PM) -> 226 (Kerala 3 PM)
# Base 978 (Dear 6 PM yesterday) -> 398 (Dear 6 PM today)

transitions = [
    ("563", "457"), # 24-Sep 1PM -> 3PM
    ("457", "978"), # 24-Sep 3PM -> 6PM
    ("978", "221"), # 24-Sep 6PM -> 8PM
    ("221", "051"), # 24-Sep 8PM -> 25-Sep 1PM
    ("051", "226"), # 25-Sep 1PM -> 3PM
    ("226", "398"), # 25-Sep 3PM -> 6PM
]

kerala_seq = [
    "288", "768", "280", "763", "700", "248", "140", "599", "236", "269",
    "822", "269", "979", "635", "460", "215", "207", "384", "700", "572",
    "457", "226"
]
for i in range(len(kerala_seq)-1):
    transitions.append((kerala_seq[i], kerala_seq[i+1]))

print(f"Total transitions to test: {len(transitions)}")

# Let's analyze 226 -> 398
# d1=2, d2=2, d3=6 -> 3, 9, 8
# Notice:
# 1st digit: 3 = d1 + 1 = 2 + 1, OR (d1+d2-1)=3, OR (d3/2)=3, OR (d1+d2+d3)-7 = 3, OR (d1*d2-1)=3
# 2nd digit: 9 = (d1 + d3 + 1) = 2 + 6 + 1 = 9, OR (d1+d2+d3-1) = 2+2+6-1 = 9, OR (10-1) = 9, OR 9-complement
# 3rd digit: 8 = (d1 + d3) = 2 + 6 = 8, OR (d2 + d3) = 2 + 6 = 8, OR (d3 + 2) = 8, OR (d1+d2+d3-2) = 8

# Let's test various candidate rules:
def rule_sum_mod(b, f1, f2, f3):
    d1, d2, d3 = int(b[0]), int(b[1]), int(b[2])
    r1 = f1(d1, d2, d3) % 10
    r2 = f2(d1, d2, d3) % 10
    r3 = f3(d1, d2, d3) % 10
    return f"{r1}{r2}{r3}"

candidates = {}

# C1: (d1+1, d1+d3+1, d1+d3) -> For 226 gives (3, 9, 8) = 398!
candidates["H7_SumPairPlus"] = lambda d1, d2, d3: f"{(d1+1)%10}{(d1+d3+1)%10}{(d1+d3)%10}"

# C2: Sum of all digits minus 1 in middle: (d1+d2-1, d1+d2+d3-1, d2+d3) -> For 226 gives (3, 9, 8) = 398!
candidates["H7_DigitSumOffset"] = lambda d1, d2, d3: f"{(d1+d2-1+10)%10}{(d1+d2+d3-1+10)%10}{(d2+d3)%10}"

# C3: 9-complement rule: (9-d1, 9-d2, 9-d3) or partial 9-complement:
# For 051: 9-d1=9, 9-d2=4, 9-d3=8
# What about (d1+2, (10-d2-1)%10, d3+5)? For 051: (2, 4, 6)
# What about Half-Partner / Mirror rule (+5 on d3, +2 on d1):
# For 051 -> 226:
# d1+2 = 2. d2-3 = 2. d3+5 = 6. -> 226!
candidates["H8_MirrorOffset"] = lambda d1, d2, d3: f"{(d1+2)%10}{(d2-3+10)%10}{(d3+5)%10}"

# C4: 226 -> 398:
# (d1+1, (d1+d2+d3)-1, d3+2):
candidates["H9_TriSumStep"] = lambda d1, d2, d3: f"{(d1+1)%10}{(d1+d2+d3-1+10)%10}{(d3+2)%10}"

# C5: Kerala Cross-Add (d2, d1+d3, d3-d1):
candidates["H10_CrossDiff"] = lambda d1, d2, d3: f"{(d2)%10}{(d1+d3)%10}{(d3-d1+10)%10}"

# C6: High frequency lottery pattern: Partner / Complement 5-cycle:
# ( (d1+5)%10, (d2+5)%10, (d3+5)%10 )
candidates["H11_CutFive"] = lambda d1, d2, d3: f"{(d1+5)%10}{(d2+5)%10}{(d3+5)%10}"

# C7: (d1+d2, d2+d3, d1+d3):
candidates["H12_AdjacentSum"] = lambda d1, d2, d3: f"{(d1+d2)%10}{(d2+d3)%10}{(d1+d3)%10}"

# C8: ( (d3-d2), (d1+d3), (d2+1) ):
candidates["H13_DiffStep"] = lambda d1, d2, d3: f"{(d3-d2+10)%10}{(d1+d3)%10}{(d2+1)%10}"

# C9: (d3, d1, d2+1):
candidates["H14_RotateStep"] = lambda d1, d2, d3: f"{(d3)%10}{(d1)%10}{(d2+1)%10}"

# Let's test all candidates across all transitions:
results = {}
for name, fn in candidates.items():
    straight = 0
    box = 0
    matches = []
    for b, actual in transitions:
        d1, d2, d3 = int(b[0]), int(b[1]), int(b[2])
        pred = fn(d1, d2, d3)
        if pred == actual:
            straight += 1
            matches.append((b, actual, "STRAIGHT"))
        elif sorted(pred) == sorted(actual):
            box += 1
            matches.append((b, actual, "BOX"))
    results[name] = {"straight": straight, "box": box, "total": straight + box, "matches": matches}

for k, v in results.items():
    print(f"{k}: Straight={v['straight']}, Box={v['box']}, Total={v['total']}, Matches={v['matches']}")
