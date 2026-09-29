import sys
sys.path.insert(0, '.')
from report_analytics import calc_all_patterns
from luck360_mcp_server import calc_blind_tweak_patterns

sys.stdout.reconfigure(encoding='utf-8')

s_6pm = '626'
s_3pm = '615'
s_1pm = '053'

print("=== 1. HOW 626 WAS FORMED ===")
# From 3PM 615:
# d1=6, d2=1, d3=5
# 626: d1=6, d2=2, d3=6
# Middle and Last increment by +1: (d1, d2+1, d3+1) = 626!
print("From 3PM 615 -> 626:")
print("  Rule: Keep D1, increment D2 and D3 by +1 -> (6, 1+1, 5+1) = 626")
print("  Pattern Family: P2 Keep + Convert variant (d1, d2+1, d3+1) = 626")
print("  Structure: 6-2-6 is an Outer-Twin Palindrome (AB=62, BC=26, AC=66)")

# From 1PM 053:
# d1=0, d2=5, d3=3
# d1 = d2 + 1 = 6 (Prefix Step)
# d2 = d3 - 1 = 2 (Suffix Step -1)
# d3 = d2 + 1 = 6 (Prefix Step)
print("\nFrom 1PM 053 -> 626:")
print("  Rule: Twin-Prefix Echo (d2+1, d3-1, d2+1) = (5+1, 3-1, 5+1) = 626!")

print("\n=== 2. PATTERNS GENERATED FROM SEED 626 FOR 8:00 PM ===")
p_626 = calc_all_patterns(s_6pm)
for k, v in p_626.items():
    val = v['val']
    print(f"{k:25}: {val} (AB: {val[:2]}) - {v.get('desc', '')}")

print("\n=== 3. 8 PM BLIND LEAPS FROM 1 PM 053 (HISTORICAL 8PM BEHAVIOR) ===")
blind_1pm = calc_blind_tweak_patterns(s_1pm)['blind_patterns']
for k, b in blind_1pm.items():
    print(f"{b['name']:32}: {b['target']} (AB: {b['pairs']['AB']}) - {b['description']}")

print("\n=== 4. 8 PM BLIND LEAPS FROM 6 PM 626 ===")
blind_6pm = calc_blind_tweak_patterns(s_6pm)['blind_patterns']
for k, b in blind_6pm.items():
    print(f"{b['name']:32}: {b['target']} (AB: {b['pairs']['AB']}) - {b['description']}")



