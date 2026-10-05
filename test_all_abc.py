from luck360_mcp_server import calc_all_patterns
data = [
    ("201", "754"), 
    ("197", "201"), 
    ("476", "197"), 
    ("910", "476"), 
    ("524", "910")  
]

from collections import defaultdict

a_rules = defaultdict(int)
b_rules = defaultdict(int)
c_rules = defaultdict(int)

for idx, (abc, t) in enumerate(data):
    a, b, c = int(abc[0]), int(abc[1]), int(abc[2])
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
    
    ma = set(); mb = set(); mc = set()

    keys = list(digits.keys())
    for i in range(len(keys)):
        for j in range(i, len(keys)):
            k1, k2 = keys[i], keys[j]
            v1, v2 = digits[k1], digits[k2]
            
            p_val = (v1 + v2) % 10
            m_val = abs(v1 - v2)
            
            for val, rule in [(p_val, f"({k1} + {k2})"), (m_val, f"|{k1} - {k2}|")]:
                if val == a: ma.add(rule)
                if val == b: mb.add(rule)
                if val == c: mc.add(rule)
                
                if (val + 1) % 10 == a: ma.add(f"({rule} + 1)")
                if (val - 1 + 10) % 10 == a: ma.add(f"({rule} - 1)")
                
                if (val + 1) % 10 == b: mb.add(f"({rule} + 1)")
                if (val - 1 + 10) % 10 == b: mb.add(f"({rule} - 1)")
                
                if (val + 1) % 10 == c: mc.add(f"({rule} + 1)")
                if (val - 1 + 10) % 10 == c: mc.add(f"({rule} - 1)")

    for r in ma: a_rules[r] += 1
    for r in mb: b_rules[r] += 1
    for r in mc: c_rules[r] += 1

top_a = sorted(a_rules.items(), key=lambda x: -x[1])[:3]
top_b = sorted(b_rules.items(), key=lambda x: -x[1])[:3]
top_c = sorted(c_rules.items(), key=lambda x: -x[1])[:3]

print("=== BEST RULES FOR A (1st Digit) ===")
for k, v in top_a: print(f"Hits {v}/5: {k}")
print("\n=== BEST RULES FOR B (2nd Digit) ===")
for k, v in top_b: print(f"Hits {v}/5: {k}")
print("\n=== BEST RULES FOR C (3rd Digit) ===")
for k, v in top_c: print(f"Hits {v}/5: {k}")

# Now predict for 524
p524 = calc_all_patterns('524')
print("\n=== PREDICTIONS FOR NEXT DRAW (from 524) ===")
print(f"H15={p524['H15_ShiftDiff']['val']}, H14={p524['H14_PrefixDiff_615']['val']}, H7={p524['H7_DiffDiffSum']['val']}, H16={p524['H16_TwinEchoStep']['val']}, H17={p524['H17_SumDiffKeep']['val']}")

def eval_rule(ruleStr, patterns):
    d = {
        'H15.1': int(patterns['H15_ShiftDiff']['val'][0]), 'H15.2': int(patterns['H15_ShiftDiff']['val'][1]), 'H15.3': int(patterns['H15_ShiftDiff']['val'][2]),
        'H14.1': int(patterns['H14_PrefixDiff_615']['val'][0]), 'H14.2': int(patterns['H14_PrefixDiff_615']['val'][1]), 'H14.3': int(patterns['H14_PrefixDiff_615']['val'][2]),
        'H7.1':  int(patterns['H7_DiffDiffSum']['val'][0]),  'H7.2':  int(patterns['H7_DiffDiffSum']['val'][1]),  'H7.3':  int(patterns['H7_DiffDiffSum']['val'][2]),
        'H16.1': int(patterns['H16_TwinEchoStep']['val'][0]), 'H16.2': int(patterns['H16_TwinEchoStep']['val'][1]), 'H16.3': int(patterns['H16_TwinEchoStep']['val'][2]),
        'H17.1': int(patterns['H17_SumDiffKeep']['val'][0]), 'H17.2': int(patterns['H17_SumDiffKeep']['val'][1]), 'H17.3': int(patterns['H17_SumDiffKeep']['val'][2])
    }
    import re
    # naive evaluator just for this script
    s = ruleStr.replace(' + 1)', ' + 1').replace(' - 1)', ' - 1')
    if s.startswith('('): s = s[1:]
    
    # parse simple
    base_val = 0
    if '|' in s:
        parts = re.search(r'\|(.*?) - (.*?)\|', s)
        base_val = abs(d[parts.group(1)] - d[parts.group(2)])
    else:
        parts = re.search(r'\((.*?) \+ (.*?)\)', ruleStr)
        if parts:
            base_val = (d[parts.group(1)] + d[parts.group(2)]) % 10
        else:
            parts = re.search(r'(.*?) \+ (.*?)( \+ 1| - 1|$)', s)
            if parts:
               base_val = (d[parts.group(1)] + d[parts.group(2)]) % 10
    
    if ' + 1' in ruleStr: return (base_val + 1) % 10
    if ' - 1' in ruleStr: return (base_val - 1 + 10) % 10
    return base_val

print("\nScenario 1 (Top Rules):")
print(f"A: {eval_rule(top_a[0][0], p524)}")
print(f"B: {eval_rule(top_b[0][0], p524)}")
print(f"C: {eval_rule(top_c[0][0], p524)}")

print("\nScenario 2 (2nd Best Rules):")
print(f"A: {eval_rule(top_a[1][0], p524)}")
print(f"B: {eval_rule(top_b[1][0], p524)}")
print(f"C: {eval_rule(top_c[1][0], p524)}")

print("\nScenario 3 (3rd Best Rules):")
print(f"A: {eval_rule(top_a[2][0], p524)}")
print(f"B: {eval_rule(top_b[2][0], p524)}")
print(f"C: {eval_rule(top_c[2][0], p524)}")
