import json
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

with open("draw_history.json", "r", encoding="utf-8") as f:
    draws = json.load(f)

print("=" * 90)
print("DUAL-STAGE ANALYSIS: 1. SELECT TARGET AB  ->  2. COMPUTE 3RD DIGIT C")
print("=" * 90)

for i in range(1, len(draws)):
    prev_d = draws[i - 1]
    curr_d = draws[i]
    t0 = prev_d["tail"]
    t1 = curr_d["tail"]
    
    a0, b0, c0 = int(t0[0]), int(t0[1]), int(t0[2])
    a1, b1, c1 = int(t1[0]), int(t1[1]), int(t1[2])
    
    # 1. How was AB1 derived from Prev?
    ab_source = []
    if f"{a1}{b1}" == f"{a0}{b0}":
        ab_source.append("Identical AB Repeat")
    elif f"{a1}{b1}" == f"{b0}{a0}":
        ab_source.append("Reversed AB Pair")
    elif a1 == (a0 - b0 + 10) % 10 and b1 == (a0 + b0 + 1) % 10:
        ab_source.append("H6 Diff-Sum Pair")
    elif a1 == (a0 + b0) % 10 and b1 == c0:
        ab_source.append("H2 Sum-C Pair")
    elif a1 == (a0 + c0 + 1) % 10 and b1 == (a0 + c0 + 1) % 10:
        ab_source.append("H8 Outer-Sum Double")
    elif a1 == (b0 + 1) % 10 and b1 == (a0 - b0 - 1 + 10) % 10:
        ab_source.append("H7 Diff-Diff Pair")
    else:
        ab_source.append(f"Shift/Offset from {a0}{b0}")

    # 2. How was C1 generated from AB?
    c_source = []
    prod1 = a1 * b1
    if prod1 > 0:
        if c1 == (prod1 // 10): c_source.append(f"Tens(A1*B1 = {prod1}) -> {c1}")
        if c1 == (prod1 % 10): c_source.append(f"Units(A1*B1 = {prod1}) -> {c1}")
    elif a1 * b1 == 0 and c1 == 0:
        c_source.append(f"Zero Product (A1*B1 = 0) -> {c1}")
        
    if c1 == abs(a1 - b1): c_source.append(f"|A1 - B1| = {c1}")
    if c1 == (10 - abs(a1 - b1)) % 10 and abs(a1 - b1) != 0: c_source.append(f"10 - |A1 - B1| = {c1}")
    if c1 == (a1 + b1) % 10: c_source.append(f"(A1 + B1)%10 = {c1}")
    if c1 == (a1 + b1 + 1) % 10: c_source.append(f"(A1 + B1 + 1)%10 = {c1}")
    if c1 == (a1 + b1 - 1 + 10) % 10: c_source.append(f"(A1 + B1 - 1)%10 = {c1}")
    
    # Check Cross Product from Prev
    prod0 = a0 * b0
    if prod0 > 0:
        if c1 == (prod0 // 10): c_source.append(f"Tens(Prev A0*B0 = {prod0}) -> {c1}")
        if c1 == (prod0 % 10): c_source.append(f"Units(Prev A0*B0 = {prod0}) -> {c1}")
    # User's mapped product rule (e.g. 500 -> 053: a0 * map(c0) = 5 * 6 = 30 -> 3)
    map_c0 = (c0 + 6) % 10
    prod_map = a0 * map_c0
    if prod_map >= 10 and c1 == (prod_map // 10):
        c_source.append(f"User Mapped Product Tens: {a0}*map({c0})={prod_map} -> {c1}")

    ab_str = ", ".join(ab_source)
    c_str = ", ".join(c_source) if c_source else "External Offset / Guard Digit"
    print(f"#{curr_d['id']:2d} | Prev: {t0} -> Curr: {t1} | Target AB: '{a1}{b1}' ({ab_str}) | 3rd Digit C={c1}: {c_str}")
