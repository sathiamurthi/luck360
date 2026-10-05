from luck360_mcp_server import calc_all_patterns
data = [
    ("20", "754"), 
    ("19", "201"), 
    ("47", "197"), 
    ("91", "476"), 
    ("52", "910")  
]

from collections import defaultdict

a_rules = defaultdict(int)
b_rules = defaultdict(int)

for idx, (ab, t) in enumerate(data):
    a, b = int(ab[0]), int(ab[1])
    p = calc_all_patterns(t)
    h15 = p['H15_ShiftDiff']['val']
    h14 = p['H14_PrefixDiff_615']['val']
    h7  = p['H7_DiffDiffSum']['val']
    h16 = p['H16_TwinEchoStep']['val']
    h17 = p['H17_SumDiffKeep']['val']
    
    digits = {
        'H15.1': int(h15[0]), 'H15.2': int(h15[1]), 'H15.3': int(h15[2]),
        'H14.1': int(h14[0]), 'H14.2': int(h14[1]), 'H14.3': int(h14[2]),
        'H7.1':  int(h7[0]),  'H7.2':  int(h7[1]),  'H7.3':  int(h7[2]),
        'H16.1': int(h16[0]), 'H16.2': int(h16[1]), 'H16.3': int(h16[2]),
        'H17.1': int(h17[0]), 'H17.2': int(h17[1]), 'H17.3': int(h17[2])
    }
    
    ma = set(); mb = set()

    keys = list(digits.keys())
    for i in range(len(keys)):
        for j in range(i, len(keys)):
            k1, k2 = keys[i], keys[j]
            v1, v2 = digits[k1], digits[k2]
            
            p_val = (v1 + v2) % 10
            m_val = abs(v1 - v2)
            
            if p_val == a: ma.add(f"({k1} + {k2})")
            if m_val == a: ma.add(f"|{k1} - {k2}|")
            if p_val == b: mb.add(f"({k1} + {k2})")
            if m_val == b: mb.add(f"|{k1} - {k2}|")
            
            if (p_val + 1) % 10 == a: ma.add(f"({k1} + {k2} + 1)")
            if (p_val - 1 + 10) % 10 == a: ma.add(f"({k1} + {k2} - 1)")
            if (p_val + 1) % 10 == b: mb.add(f"({k1} + {k2} + 1)")
            if (p_val - 1 + 10) % 10 == b: mb.add(f"({k1} + {k2} - 1)")

            if (m_val + 1) % 10 == a: ma.add(f"(|{k1} - {k2}| + 1)")
            if (m_val - 1 + 10) % 10 == a: ma.add(f"(|{k1} - {k2}| - 1)")
            if (m_val + 1) % 10 == b: mb.add(f"(|{k1} - {k2}| + 1)")
            if (m_val - 1 + 10) % 10 == b: mb.add(f"(|{k1} - {k2}| - 1)")

    for r in ma: a_rules[r] += 1
    for r in mb: b_rules[r] += 1

print("=== REAL BEST RULES FOR NEXT DRAW'S FIRST DIGIT (A) ===")
for k, v in sorted(a_rules.items(), key=lambda x: -x[1])[:3]:
    print(f"Hits {v}/5 draws: {k}")

print("\n=== REAL BEST RULES FOR NEXT DRAW'S SECOND DIGIT (B) ===")
for k, v in sorted(b_rules.items(), key=lambda x: -x[1])[:3]:
    print(f"Hits {v}/5 draws: {k}")
