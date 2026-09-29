import sys
sys.path.insert(0, '.')
from report_analytics import calc_all_patterns

sys.stdout.reconfigure(encoding='utf-8')

# Seeds
s1 = '053' # 1 PM
s3 = '615' # 3 PM
s6 = '398' # 6 PM
s8 = '500' # 8 PM

print("=== 1. 1 PM Pattern on 3 PM ===")
p_1pm = calc_all_patterns(s1)
print(f"Seed 1PM: {s1} -> H14: {p_1pm['H14_PrefixDiff_615']['val']} (Hits 3PM 615!)")
print(f"Seed 1PM: {s1} -> H6: {p_1pm['H6_DiffSumPlusOne']['val']}")

print("\n=== 2. 6 PM Pattern on 8 PM ===")
p_6pm = calc_all_patterns(s6)
print(f"Seed 6PM: {s6} -> H9: {p_6pm['H9_SubAddTen']['val']}")
print(f"Seed 6PM: {s6} -> H11: {p_6pm['H11_SumPairPlus']['val']}")
print(f"Seed 6PM: {s6} -> H7: {p_6pm['H7_DiffDiffSum']['val']}")
print(f"Seed 6PM: {s6} -> H15: {p_6pm['H15_ShiftDiff']['val']}")

print("\n=== 3. 6 PM Patterns on 3 PM & 1 PM ===")
p_3pm = calc_all_patterns(s3)
print(f"6PM H15 on 3PM ({s3}): {p_3pm['H15_ShiftDiff']['val']}")
print(f"6PM H7 on 3PM ({s3}): {p_3pm['H7_DiffDiffSum']['val']}")
print(f"6PM H9 on 3PM ({s3}): {p_3pm['H9_SubAddTen']['val']}")
print(f"6PM H11 on 3PM ({s3}): {p_3pm['H11_SumPairPlus']['val']}")

print(f"6PM H15 on 1PM ({s1}): {p_1pm['H15_ShiftDiff']['val']}")
print(f"6PM H7 on 1PM ({s1}): {p_1pm['H7_DiffDiffSum']['val']}")
print(f"6PM H9 on 1PM ({s1}): {p_1pm['H9_SubAddTen']['val']}")
print(f"6PM H11 on 1PM ({s1}): {p_1pm['H11_SumPairPlus']['val']}")

print("\n=== 4. 1 PM & 3 PM Patterns on 6 PM & 8 PM ===")
p_8pm = calc_all_patterns(s8)
print(f"1PM H15 on 6PM ({s6}): {p_6pm['H15_ShiftDiff']['val']} (Hits 053!)")
print(f"1PM H14 on 6PM ({s6}): {p_6pm['H14_PrefixDiff_615']['val']}")
print(f"3PM H8 on 6PM ({s6}): {p_6pm['H8_OuterSumStep']['val']}")
print(f"3PM H12 on 6PM ({s6}): {p_6pm['H12_MirrorStep']['val']}")

print(f"1PM H13 on 8PM ({s8}): {p_8pm['H13_ZeroSixProduct']['val']} (Hits 053!)")
print(f"1PM H15 on 8PM ({s8}): {p_8pm['H15_ShiftDiff']['val']}")
print(f"3PM H8 on 8PM ({s8}): {p_8pm['H8_OuterSumStep']['val']}")
print(f"3PM H10 on 8PM ({s8}): {p_8pm['H10_PartnerMirror']['val']}")
