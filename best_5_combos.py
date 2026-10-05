def get_substrings(val_str, length=2):
    subs = set()
    for i in range(len(val_str) - length + 1):
        subs.add(val_str[i:i+length])
    if len(val_str) >= 2:
        subs.add(val_str[0] + val_str[-1])
        subs.add(val_str[-1] + val_str[0])
    return subs

# Yesterday's draws
t1, t2, t3, t4 = "197", "476", "910", "524"

# Subtractions
sub1 = str(abs(int(t1) - int(t2))).zfill(3) # 279
sub2 = str(abs(int(t2) - int(t3))).zfill(3) # 434
sub3 = str(abs(int(t3) - int(t4))).zfill(3) # 386

# Products
pairs = set()
for prev, curr in [(t2, t3), (t3, t4)]:
    v_prev = int(prev)
    r_prev = int(prev[::-1])
    r_curr = int(curr[::-1])
    m1 = str(v_prev * r_curr)
    m2 = str(r_prev * r_curr)
    p = get_substrings(m1).union(get_substrings(m2))
    p.update([x[::-1] for x in p])
    pairs.update(p)

# We want 3-digit combos ABC where:
# 1. At least one pair (AB, BC, AC) is in the 'pairs' pool.
# 2. The remaining digit(s) are in the subtraction pool (weighted heavily to sub3 and sub2).
# 3. Specifically, subtraction digit landing in B or C is better.

scores = []

sub_pool = list(sub3) * 3 + list(sub2) * 2 + list(sub1) # Weight recent ones higher
sub_counts = {d: sub_pool.count(d) for d in set(sub_pool)}

for i in range(1000):
    abc = str(i).zfill(3)
    ab, bc, ac = abc[:2], abc[1:], abc[0]+abc[2]
    
    pair_score = 0
    if ab in pairs: pair_score += 1
    if bc in pairs: pair_score += 1
    if ac in pairs: pair_score += 1
    
    # Check subtraction digits in A, B, C
    # Weights based on historical probability: C(50), B(44), A(32)
    sub_score = 0
    if abc[0] in sub_counts: sub_score += sub_counts[abc[0]] * 0.32
    if abc[1] in sub_counts: sub_score += sub_counts[abc[1]] * 0.44
    if abc[2] in sub_counts: sub_score += sub_counts[abc[2]] * 0.50
    
    if pair_score > 0: # MUST have at least one product pair
        total_score = (pair_score * 50) + sub_score
        scores.append((total_score, abc, ab in pairs, bc in pairs, ac in pairs))

scores.sort(reverse=True, key=lambda x: x[0])

print("Top 10 combinations:")
for s in scores[:10]:
    print(f"ABC: {s[1]} | Score: {s[0]:.1f} | Pairs matched: AB({s[2]}) BC({s[3]}) AC({s[4]})")
