import json

with open('draw_history.json', 'r') as f:
    recs = json.load(f)

print("=== ANALYSIS OF BLIND / CROSS-DRAW PATTERNS ===")

# 1. Check Nagaland 1 PM -> Nagaland 8 PM
nagaland_draws = [r for r in recs if 'Nagaland' in r.get('company', '')]
print(f"Total Nagaland draws: {len(nagaland_draws)}")
for r in nagaland_draws:
    print(f"  {r.get('date')} {r.get('time')} | {r.get('ticket')} | Tail: {r.get('tail')}")

# Check 2026-09-24: 1 PM (563) -> 8 PM (221)
# Check 2026-09-25: 1 PM (051) -> 8 PM (500)

print("\n--- Sep 24: 563 -> 221 ---")
# 563: d1=5, d2=6, d3=3
# 221: 2, 2, 1
# Differences: (5-3=2, 6/3=2?, 3-2=1) or (5-3, 5-3, 3-2) = 221!
# Notice: (d1-d3, d1-d3, d3-2) = (2, 2, 1) = 221!

print("\n--- Sep 25: 051 -> 500 ---")
# 051: d1=0, d2=5, d3=1
# 500: 5, 0, 0
# Notice: d2=5, d1=0, d3-1=0 -> (5, 0, 0) = 500!
# Also: Rev-AB = 501 -> Tweak -1 on last digit = 500!
# Also: (d1+d2=5, d1=0, d3-1=0) = 500!

# Let's test all transitions in recs (both sequential and 1-PM-to-8-PM blind)
print("\n--- TESTING TWEAK FORMULAS ON ALL 1-PM TO 8-PM PAIRS ---")
days = set(r.get('date') for r in recs if r.get('date'))
for day in sorted(days):
    day_recs = {r.get('time'): r for r in recs if r.get('date') == day}
    r1 = day_recs.get('1:00 PM')
    r8 = day_recs.get('8:00 PM')
    if r1 and r8:
        t1, t8 = r1.get('tail'), r8.get('tail')
        print(f"Date: {day} | 1 PM: {t1} ({r1.get('ticket')}) -> 8 PM: {t8} ({r8.get('ticket')})")
        d1, d2, d3 = int(t1[0]), int(t1[1]), int(t1[2])
        
        # Test Blind Tweak Formulas:
        # B1: Rev-AB Tweak -1: (d2, d1, (d3-1)%10)
        b1 = f"{d2}{d1}{(d3-1)%10}"
        # B2: Rev-AB Exact: (d2, d1, d3)
        b2 = f"{d2}{d1}{d3}"
        # B3: Sum-AB Clamp: ((d1+d2)%10, d1, (d3-1)%10)
        b3 = f"{(d1+d2)%10}{d1}{(d3-1)%10}"
        # B4: Diff-Diff-Step: ((d1-d3+10)%10, (d1-d3+10)%10, (d3-2+10)%10)
        b4 = f"{(d1-d3+10)%10}{(d1-d3+10)%10}{(d3-2+10)%10}"
        # B5: Outer Tweak: (d2, (d1+d2)%10, (d3-1)%10)
        b5 = f"{d2}{(d1+d2)%10}{(d3-1)%10}"
        
        print(f"   B1 (Rev-AB Tweak -1): {b1} {'*** HIT 500! ***' if b1 == t8 else ''}")
        print(f"   B2 (Rev-AB Base):     {b2}")
        print(f"   B3 (Sum-AB Tweak -1): {b3} {'*** HIT 500! ***' if b3 == t8 else ''}")
        print(f"   B4 (Diff-Step):       {b4} {'*** HIT 221! ***' if b4 == t8 else ''}")
