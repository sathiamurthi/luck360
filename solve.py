data = [
    # (AB, H15, H14, H7)
    # 29th 3 PM -> 6 PM (754 -> AB 75)
    ("75", "887", "887", "892"),
    # 29th 6 PM -> 8 PM (201 -> AB 20)
    ("20", "677", "685", "611"),
    # 29th 8 PM -> 30th 1 PM (197 -> AB 19)
    ("19", "192", "130", "113"),
    # 30th 1 PM -> 3 PM (476 -> AB 47)
    ("47", "061", "029", "018"),
    # 30th 3 PM -> 6 PM (910 -> AB 91)
    ("91", "824", "857", "860"),
    # 30th 6 PM -> 8 PM (524 -> AB 52)
    ("52", "219", "201", "279")
]

def get_digits(s):
    return [int(c) for c in s]

def eval_combinations():
    for ab, h15, h14, h7 in data:
        print(f"Target AB: {ab} from {h15}, {h14}, {h7}")
        a, b = int(ab[0]), int(ab[1])
        d15 = get_digits(h15)
        d14 = get_digits(h14)
        d7 = get_digits(h7)
        
        digits = {
            'H15[0]': d15[0], 'H15[1]': d15[1], 'H15[2]': d15[2],
            'H14[0]': d14[0], 'H14[1]': d14[1], 'H14[2]': d14[2],
            'H7[0]': d7[0], 'H7[1]': d7[1], 'H7[2]': d7[2],
        }
        
        # Look for single digit matches
        for k, v in digits.items():
            if v == a: print(f"  A ({a}) == {k}")
            if v == b: print(f"  B ({b}) == {k}")
            
        # Look for sums % 10
        for k1, v1 in digits.items():
            for k2, v2 in digits.items():
                if k1 >= k2: continue
                if (v1 + v2) % 10 == a: print(f"  A ({a}) == ({k1} + {k2}) % 10")
                if (v1 + v2) % 10 == b: print(f"  B ({b}) == ({k1} + {k2}) % 10")
                if abs(v1 - v2) == a: print(f"  A ({a}) == abs({k1} - {k2})")
                if abs(v1 - v2) == b: print(f"  B ({b}) == abs({k1} - {k2})")

eval_combinations()
