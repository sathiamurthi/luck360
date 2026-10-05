data = [
    ("75", "887", "887", "892"),
    ("20", "677", "685", "611"),
    ("19", "192", "130", "113"),
    ("47", "061", "029", "018"),
    ("91", "824", "857", "860"),
    ("52", "219", "201", "279")
]

from collections import defaultdict
a_rules = defaultdict(int)
b_rules = defaultdict(int)

for ab, h15, h14, h7 in data:
    a, b = int(ab[0]), int(ab[1])
    digits = {
        'H15.front': int(h15[0]), 'H15.mid': int(h15[1]), 'H15.last': int(h15[2]),
        'H14.front': int(h14[0]), 'H14.mid': int(h14[1]), 'H14.last': int(h14[2]),
        'H7.front':  int(h7[0]),  'H7.mid':  int(h7[1]),  'H7.last':  int(h7[2])
    }
    
    matches_a = set()
    matches_b = set()
    
    for k, v in digits.items():
        if v == a: matches_a.add(f"{k}")
        if v == b: matches_b.add(f"{k}")
        
    for k1, v1 in digits.items():
        for k2, v2 in digits.items():
            if k1 >= k2: continue
            if (v1 + v2) % 10 == a: matches_a.add(f"({k1} + {k2})")
            if (v1 + v2) % 10 == b: matches_b.add(f"({k1} + {k2})")
            if abs(v1 - v2) == a: matches_a.add(f"|{k1} - {k2}|")
            if abs(v1 - v2) == b: matches_b.add(f"|{k1} - {k2}|")
            
    for m in matches_a: a_rules[m] += 1
    for m in matches_b: b_rules[m] += 1

print("Top rules for AB First Digit (A):")
for k, v in sorted(a_rules.items(), key=lambda x: -x[1])[:10]:
    print(f"  {v} hits: {k}")
    
print("\nTop rules for AB Second Digit (B):")
for k, v in sorted(b_rules.items(), key=lambda x: -x[1])[:10]:
    print(f"  {v} hits: {k}")
