from luck360_mcp_server import calc_all_patterns

data = [
    ("20", "754", "3:00 PM -> 6:00 PM"), 
    ("19", "201", "6:00 PM -> 8:00 PM"), 
    ("47", "197", "8:00 PM -> 1:00 PM"), 
    ("91", "476", "1:00 PM -> 3:00 PM"), 
    ("52", "910", "3:00 PM -> 6:00 PM")  
]

print("=== GOLDEN PAIR REVERSE LOGIC GRID ===\n")
print("Target Master Formula for NEXT AB:")
print("A (First Digit): (H15.mid + H16.last) % 10")
print("B (Second Digit): |H7.mid - H7.last|")
print("-" * 60)

for ab, tail, label in data:
    p = calc_all_patterns(tail)
    h15 = p['H15_ShiftDiff']['val']
    h16 = p['H16_TwinEchoStep']['val']
    h7  = p['H7_DiffDiffSum']['val']
    
    a_calc = (int(h15[1]) + int(h16[2])) % 10
    b_calc = abs(int(h7[1]) - int(h7[2]))
    
    a_match = "? MATCH" if str(a_calc) == ab[0] else "? Miss"
    b_match = "? MATCH" if str(b_calc) == ab[1] else "? Miss"
    
    print(f"[{label}] Base Seed: {tail} -> Target AB: {ab}")
    print(f"  Generated Patterns -> H15: {h15} | H16: {h16} | H7: {h7}")
    print(f"  Calculated A: ({h15[1]} + {h16[2]}) = {a_calc} {a_match}")
    print(f"  Calculated B: |{h7[1]} - {h7[2]}| = {b_calc} {b_match}")
    print(f"  Predicted Pair: {a_calc}{b_calc}")
    print("-" * 60)
