import json

with open('draw_history.json', 'r') as f:
    draws = json.load(f)

tails = [d['tail'] for d in draws if len(d.get('tail','')) == 3]

def get_pairs(val_str):
    if len(val_str) < 2:
        return set()
    pairs = set()
    pairs.add(val_str[-2:]) # last 2
    pairs.add(val_str[-2:][::-1]) # rev last 2
    pairs.add(val_str[:2]) # first 2
    pairs.add(val_str[:2][::-1]) # rev first 2
    pairs.add(val_str[0] + val_str[-1]) # first + last
    pairs.add(val_str[-1] + val_str[0]) # last + first
    return pairs

stats = {
    'P1 (Prev x RevCurr)': {'hits': 0, 'total': 0},
    'P2 (RevPrev x RevCurr)': {'hits': 0, 'total': 0},
    'P3 (Prev x Curr)': {'hits': 0, 'total': 0},
    'P4 (RevPrev x Curr)': {'hits': 0, 'total': 0}
}

sub_stats = {
    'Sub (abs(Prev - Curr)) matches 1 digit': {'hits': 0, 'total': 0}
}

print("=== RECENT DRAWS ANALYSIS ===")
for i in range(len(tails) - 2):
    t1 = tails[i]
    t2 = tails[i+1]
    t3 = tails[i+2]
    
    ab3 = t3[:2]
    
    vt1 = int(t1)
    vt2 = int(t2)
    rt1 = int(t1[::-1])
    rt2 = int(t2[::-1])
    
    p1 = str(vt1 * rt2)
    p2 = str(rt1 * rt2)
    p3 = str(vt1 * vt2)
    p4 = str(rt1 * vt2)
    
    s = str(abs(vt1 - vt2)).zfill(3)
    
    p1_pairs = get_pairs(p1)
    p2_pairs = get_pairs(p2)
    p3_pairs = get_pairs(p3)
    p4_pairs = get_pairs(p4)
    
    hit_p1 = ab3 in p1_pairs
    hit_p2 = ab3 in p2_pairs
    hit_p3 = ab3 in p3_pairs
    hit_p4 = ab3 in p4_pairs
    
    # Check if any digit in `s` matches any digit in `ab3` (Wait, user says "any one digit matching for the next result")
    # Next result is `t3` (all 3 digits) or `ab3`? I'll check `t3`.
    hit_sub = any(d in t3 for d in s)
    
    stats['P1 (Prev x RevCurr)']['total'] += 1
    stats['P2 (RevPrev x RevCurr)']['total'] += 1
    stats['P3 (Prev x Curr)']['total'] += 1
    stats['P4 (RevPrev x Curr)']['total'] += 1
    sub_stats['Sub (abs(Prev - Curr)) matches 1 digit']['total'] += 1
    
    if hit_p1: stats['P1 (Prev x RevCurr)']['hits'] += 1
    if hit_p2: stats['P2 (RevPrev x RevCurr)']['hits'] += 1
    if hit_p3: stats['P3 (Prev x Curr)']['hits'] += 1
    if hit_p4: stats['P4 (RevPrev x Curr)']['hits'] += 1
    if hit_sub: sub_stats['Sub (abs(Prev - Curr)) matches 1 digit']['hits'] += 1
    
    # Just print the last 5 draws for visibility
    if i >= len(tails) - 7:
        print(f"\n[Prev: {t1}, Curr: {t2}] -> Next: {t3} (AB={ab3})")
        print(f"  P1 ({vt1}x{rt2})={p1} -> Pairs: {p1_pairs} | Hit AB: {hit_p1}")
        print(f"  P2 ({rt1}x{rt2})={p2} -> Pairs: {p2_pairs} | Hit AB: {hit_p2}")
        print(f"  Sub ({vt1}-{vt2})={s} -> Digits: {set(s)} | Intersect Next({t3}): {set(s).intersection(set(t3))} | Hit 1 digit: {hit_sub}")

print("\n=== AGGREGATE STATS (All Time) ===")
for k, v in stats.items():
    print(f"{k}: {v['hits']}/{v['total']} ({v['hits']/v['total']*100:.1f}%)")

for k, v in sub_stats.items():
    print(f"{k}: {v['hits']}/{v['total']} ({v['hits']/v['total']*100:.1f}%)")

# Predict for the CURRENT situation (Next draw)
t1 = tails[-2]
t2 = tails[-1]
vt1 = int(t1)
vt2 = int(t2)
rt1 = int(t1[::-1])
rt2 = int(t2[::-1])

print(f"\n=== PREDICTION FOR NEXT DRAW ===")
print(f"Prev: {t1} | Curr: {t2}")
print(f"P1 (Prev x RevCurr): {vt1} x {rt2} = {vt1 * rt2} -> Extracted ABs: {get_pairs(str(vt1*rt2))}")
print(f"P2 (RevPrev x RevCurr): {rt1} x {rt2} = {rt1 * rt2} -> Extracted ABs: {get_pairs(str(rt1*rt2))}")
s_next = str(abs(vt1 - vt2)).zfill(3)
print(f"Sub (abs(Prev - Curr)): abs({vt1} - {vt2}) = {s_next} -> Hot single digits: {set(s_next)}")

