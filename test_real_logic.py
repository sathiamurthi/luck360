data = [
    ("20", "677", "685", "611"), 
    ("19", "192", "130", "113"), 
    ("47", "061", "029", "018"), 
    ("91", "824", "857", "860"), 
    ("52", "219", "201", "279")  
]

from collections import defaultdict

a_rules = defaultdict(int)
b_rules = defaultdict(int)

for idx, (ab, h15, h14, h7) in enumerate(data):
    a, b = int(ab[0]), int(ab[1])
    digits = {
        'H15.1': int(h15[0]), 'H15.2': int(h15[1]), 'H15.3': int(h15[2]),
        'H14.1': int(h14[0]), 'H14.2': int(h14[1]), 'H14.3': int(h14[2]),
        'H7.1':  int(h7[0]),  'H7.2':  int(h7[1]),  'H7.3':  int(h7[2])
    }
    
    ma = set(); mb = set()
    
    for k, v in digits.items():
        if v == a: ma.add(k)
        if v == b: mb.add(k)
        if (v + 1) % 10 == a: ma.add(f"({k} + 1)")
        if (v - 1 + 10) % 10 == a: ma.add(f"({k} - 1)")
        if (v + 1) % 10 == b: mb.add(f"({k} + 1)")
        if (v - 1 + 10) % 10 == b: mb.add(f"({k} - 1)")

    keys = list(digits.keys())
    for i in range(len(keys)):
        for j in range(i, len(keys)):
            k1, k2 = keys[i], keys[j]
            v1, v2 = digits[k1], digits[k2]
            
            p = (v1 + v2) % 10
            m = abs(v1 - v2)
            
            if p == a: ma.add(f"({k1} + {k2})")
            if m == a: ma.add(f"|{k1} - {k2}|")
            if p == b: mb.add(f"({k1} + {k2})")
            if m == b: mb.add(f"|{k1} - {k2}|")
            
            if (p + 1) % 10 == a: ma.add(f"({k1} + {k2} + 1)")
            if (p - 1 + 10) % 10 == a: ma.add(f"({k1} + {k2} - 1)")
            if (p + 1) % 10 == b: mb.add(f"({k1} + {k2} + 1)")
            if (p - 1 + 10) % 10 == b: mb.add(f"({k1} + {k2} - 1)")

            if (m + 1) % 10 == a: ma.add(f"(|{k1} - {k2}| + 1)")
            if (m - 1 + 10) % 10 == a: ma.add(f"(|{k1} - {k2}| - 1)")
            if (m + 1) % 10 == b: mb.add(f"(|{k1} - {k2}| + 1)")
            if (m - 1 + 10) % 10 == b: mb.add(f"(|{k1} - {k2}| - 1)")

    for r in ma: a_rules[r] += 1
    for r in mb: b_rules[r] += 1

print("=== REAL BEST RULES FOR NEXT DRAW'S FIRST DIGIT (A) ===")
for k, v in sorted(a_rules.items(), key=lambda x: -x[1])[:3]:
    print(f"Hits {v}/5 draws: {k}")

print("\n=== REAL BEST RULES FOR NEXT DRAW'S SECOND DIGIT (B) ===")
for k, v in sorted(b_rules.items(), key=lambda x: -x[1])[:3]:
    print(f"Hits {v}/5 draws: {k}")
