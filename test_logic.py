data = [
    # (Target AB, H15, H14, H7)
    ("75", "677", "685", "611"),
    ("20", "192", "130", "113"),
    ("19", "061", "029", "018"),
    ("47", "824", "857", "860"),
    ("91", "219", "201", "279"),
    ("52", "395", "362", "329")
]

from collections import defaultdict

a_rules = defaultdict(int)
b_rules = defaultdict(int)

for idx, (ab, h15, h14, h7) in enumerate(data):
    a, b = int(ab[0]), int(ab[1])
    digits = {
        'H15.first': int(h15[0]), 'H15.mid': int(h15[1]), 'H15.last': int(h15[2]),
        'H14.first': int(h14[0]), 'H14.mid': int(h14[1]), 'H14.last': int(h14[2]),
        'H7.first':  int(h7[0]),  'H7.mid':  int(h7[1]),  'H7.last':  int(h7[2])
    }
    
    matches_a = set()
    matches_b = set()
    
    def add_match(s, target, matches_set):
        matches_set.add(s)
    
    for k, v in digits.items():
        if v == a: add_match(k, a, matches_a)
        if v == b: add_match(k, b, matches_b)
        
        # +/- 1 tweaks
        if (v + 1) % 10 == a: add_match(f"({k} + 1)", a, matches_a)
        if (v - 1) % 10 == a or (v - 1 + 10) % 10 == a: add_match(f"({k} - 1)", a, matches_a)
        
        if (v + 1) % 10 == b: add_match(f"({k} + 1)", b, matches_b)
        if (v - 1) % 10 == b or (v - 1 + 10) % 10 == b: add_match(f"({k} - 1)", b, matches_b)

    keys = list(digits.keys())
    for i in range(len(keys)):
        for j in range(i, len(keys)):
            k1, k2 = keys[i], keys[j]
            v1, v2 = digits[k1], digits[k2]
            
            # Direct math
            s_plus = (v1 + v2) % 10
            s_minus = abs(v1 - v2)
            
            if s_plus == a: add_match(f"({k1} + {k2})", a, matches_a)
            if s_minus == a: add_match(f"|{k1} - {k2}|", a, matches_a)
            
            if s_plus == b: add_match(f"({k1} + {k2})", b, matches_b)
            if s_minus == b: add_match(f"|{k1} - {k2}|", b, matches_b)
            
            # Math with +/- 1
            if (s_plus + 1) % 10 == a: add_match(f"({k1} + {k2} + 1)", a, matches_a)
            if (s_plus - 1 + 10) % 10 == a: add_match(f"({k1} + {k2} - 1)", a, matches_a)
            
            if (s_plus + 1) % 10 == b: add_match(f"({k1} + {k2} + 1)", b, matches_b)
            if (s_plus - 1 + 10) % 10 == b: add_match(f"({k1} + {k2} - 1)", b, matches_b)

            if (s_minus + 1) % 10 == a: add_match(f"(|{k1} - {k2}| + 1)", a, matches_a)
            if (s_minus - 1 + 10) % 10 == a: add_match(f"(|{k1} - {k2}| - 1)", a, matches_a)

            if (s_minus + 1) % 10 == b: add_match(f"(|{k1} - {k2}| + 1)", b, matches_b)
            if (s_minus - 1 + 10) % 10 == b: add_match(f"(|{k1} - {k2}| - 1)", b, matches_b)

    for m in matches_a: a_rules[m] += 1
    for m in matches_b: b_rules[m] += 1

print("=== BEST RULES FOR FIRST DIGIT (A) ===")
for k, v in sorted(a_rules.items(), key=lambda x: -x[1])[:5]:
    print(f"Hits {v}/6 draws: {k}")

print("\n=== BEST RULES FOR SECOND DIGIT (B) ===")
for k, v in sorted(b_rules.items(), key=lambda x: -x[1])[:5]:
    print(f"Hits {v}/6 draws: {k}")
