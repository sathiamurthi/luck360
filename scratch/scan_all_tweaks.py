import json

with open('draw_history.json', 'r') as f:
    recs = json.load(f)

print("=== CHECKING ALL CROSS-DRAW & TWEAK FREQUENCIES ===")

# Test all pairs of draws (i < j) where company is same OR slot leap
same_company_pairs = []
for i in range(len(recs)):
    for j in range(i+1, len(recs)):
        r1, r2 = recs[i], recs[j]
        c1, c2 = r1.get('company', ''), r2.get('company', '')
        t1, t2 = r1.get('tail', ''), r2.get('tail', '')
        if len(t1) == 3 and len(t2) == 3:
            d1, d2, d3 = int(t1[0]), int(t1[1]), int(t1[2])
            
            # Check B1: Rev-AB Tweak -1
            b1 = f"{d2}{d1}{(d3-1)%10}"
            # Check B1+1: Rev-AB Tweak +1
            b1_plus = f"{d2}{d1}{(d3+1)%10}"
            # Check B1_base: Rev-AB
            b1_base = f"{d2}{d1}{d3}"
            
            if t2 in (b1, b1_plus, b1_base):
                match_type = "Tweak -1" if t2 == b1 else ("Tweak +1" if t2 == b1_plus else "Exact Rev-AB")
                same_comp = "SAME COMPANY" if c1 == c2 else "Cross-Company"
                dist = j - i
                print(f"Match [{match_type}]: {r1.get('date')} {r1.get('time')} ({c1}, {t1}) -> {r2.get('date')} {r2.get('time')} ({c2}, {t2}) [Draw gap: {dist}, {same_comp}]")
