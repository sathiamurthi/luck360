import sys, os, json
sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

import report_analytics as ra

tail = '102'
ticket = '54J 77102'
p = ra.calc_all_patterns(tail, ticket)
b = ra.calc_blind_patterns(tail)

d1, d2, d3 = int(tail[0]), int(tail[1]), int(tail[2])
h18_a = f"{(d1+d3+1)%10}{d2}{(d3-d1+10)%10}"
h18_b = f"{d1+d3}{(d3-d1+10)%10}"

print("=== 1 PM (102) TO 3 PM (KERALA SAMRUDHI SM-74) PROJECTIONS ===")
print(f"★ NEW Star H18 (Outer Balance Rule): {h18_a}")
print(f"★ Star H7 (Diff-Diff-Sum): {p['H7_DiffDiffSum']['val']}")
print(f"★ Star H8 (Outer-Sum Step): {p['H8_OuterSumStep']['val']}")
print(f"★ Star H9 (Sub-Add-10): {p['H9_SubAddTen']['val']}")
print(f"★ Star H10 (Partner-Mirror): {p['H10_PartnerMirror']['val']}")
print(f"★ Star H16 (Twin-Echo Step): {p['H16_TwinEchoStep']['val']}")
print(f"★ Star H15 (Shift-Difference): {p['H15_ShiftDiff']['val']}")
print(f"★ Star H17 (Sum-Diff-Keep): {p['H17_SumDiffKeep']['val']}")
print(f"★ Star H14 (Prefix Sandwich): {p['H14_PrefixDiff_615']['val']}")
print(f"★ Star H6 (Diff-Sum+1): {p['H6_DiffSumPlusOne']['val']}")
print(f"★ Star H2 (Cross-Swap 5-8): {p['H2_CrossSwap']['val']}")
print(f"P1 (Rev-Diff): {p['P1_RevDiff']['val']}")
print(f"P2 (Keep-Conv): {p['P2_KeepConv']['val']}")

print("\n=== BLIND PATTERNS FROM 102 ===")
for k, v in b.items():
    print(f"{v.get('name', k)}: {v['target']}")

# Also check Kerala 3 PM historical patterns:
# 2026-09-25 3 PM was 226 (Ticket RA 494226) from 051: H8 and H12 hit 226
# 2026-09-26 3 PM was 615 (Ticket TL 360615) from 053: H14 hit 615 straight!
# Notice: In both Kerala draws, H8/H12 and H14 were straight hits!
print("\n=== KERALA 3 PM HISTORICAL FAVORITES ===")
print("When 1 PM was 051 -> Kerala 3 PM was 226 (Hit by H8 & H12)")
print("When 1 PM was 053 -> Kerala 3 PM was 615 (Hit by H14)")
print(f"From 102: H8={p['H8_OuterSumStep']['val']}, H12={p['H12_MirrorStep']['val']}, H14={p['H14_PrefixDiff_615']['val']}, H18={h18_a}")
