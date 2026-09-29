import json
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 1. Patterns from today's 1 PM tail 053 and ticket 65G 50053
tail = "053"
ticket = "65G 50053"
t_digits = [6, 5, 5, 0, 0, 5, 3] # digits in 65G 50053
d1, d2, d3 = 0, 5, 3

# Generated 3-digit targets from our 12 patterns
targets = {
    "Star H7 (Diff-Diff-Sum)": f"{(d2+1)%10}{(d1-d2-1+10)%10}{(d1+d3)%10}", # 643
    "Star H9 (Sub-Add-10)": f"{(d3-d1-1+10)%10}{(d1+d3+1)%10}{(10-d1)%10}", # 240
    "Star H8 (Outer-Sum Step)": f"{(d1+d3+1)%10}{(d1+d3+1)%10}{(d2+1)%10}", # 446
    "Star H14 (Prefix Sandwich)": f"{(d2+1)%10}{(d1+1)%10}{d2}", # 615
    "Star H13 (0-6 Product Tens)": f"{d2}{d1}{((d1*((d3+6)%10))//10)%10 if (d1*((d3+6)%10))>=10 else (d1*((d3+6)%10))%10}", # 500
    "Star H6 (Diff-Sum Plus One)": f"{(d1-d2+10)%10}{(d1+d2+1)%10}{d3}", # 563
    "Star H10 (Partner-Mirror)": f"{(d3+5)%10}{(9-d3+10)%10}{(d3-1+10)%10}", # 862
    "Pattern H11 (Sum-Pair-Plus)": f"{(d1+1)%10}{(d1+d3+1)%10}{(d1+d3)%10}", # 143
    "Star H12 (Mirror Step)": f"{(d1+2)%10}{(d2-3+10)%10}{(d3+5)%10}", # 228
    "Star H2 (Cross-Swap 5-8)": f"{(d1+d2)%10}{d3}{8 if d2==5 else (d2+3)%10}", # 538
    "H3 (Diff & Remainder)": f"{(d1-d2+10)%10}{(d1+d2+d3)%10}{(d1-d3+10)%10}", # 587
    "P3 (Reverse AB Base)": f"{d2}{d1}{d3}" # 503
}

print("="*80)
print(f"INPUT SEED: Tail '{tail}' | Full Ticket '{ticket}' (Digits: {t_digits})")
print("="*80)

ab_scores = {}

# Evaluate AB from all pattern targets
for pname, num in targets.items():
    ab = num[:2]
    ab_scores[ab] = ab_scores.get(ab, 0) + 3.0

# Evaluate AB directly from ticket structure
ticket_ab_pairs = {
    "65": "Ticket Prefix (65G)",
    "56": "Reverse Ticket Prefix (56)",
    "63": "Outer Digits (First 6, Last 3)",
    "36": "Reversed Outer Digits",
    "50": "Body Lead Pair (50053)",
    "05": "Body Reverse Pair (053)",
    "70": "Kerala Saturday Anchor (KR 700 / G=7 + 0)",
    "61": "Prefix Difference (6, 6-5=1 -> 61)"
}

for ab, reason in ticket_ab_pairs.items():
    ab_scores[ab] = ab_scores.get(ab, 0) + 2.5

# Kerala Saturday Historical Resonance Bonus
# On Sep 5 & Sep 19, Karunya Saturday draws had tail 700 (AB = 70)
ab_scores["70"] = ab_scores.get("70", 0) + 2.0
# Double-digit resonance: 22 was hit yesterday at 3 PM Kerala (RA 494226 -> 226)
ab_scores["22"] = ab_scores.get("22", 0) + 2.0
# 24 is reinforced by both H9 (240) and H7 diff-diff
ab_scores["24"] = ab_scores.get("24", 0) + 2.0
# 64 is reinforced by H7 (643) and outer ticket digits (6 & 4 from 65-1=4)
ab_scores["64"] = ab_scores.get("64", 0) + 2.0

sorted_ab = sorted(ab_scores.items(), key=lambda x: x[1], reverse=True)

print("\nRANKED TOP AB FRONT PAIRS FOR UPCOMING KERALA DRAW:")
for rank, (ab, sc) in enumerate(sorted_ab[:10], 1):
    sources = []
    for pname, num in targets.items():
        if num[:2] == ab:
            sources.append(f"{pname} ({num})")
    if ab in ticket_ab_pairs:
        sources.append(ticket_ab_pairs[ab])
    if ab == "70":
        sources.append("Kerala Saturday 700 Double Hit Resonance")
    if ab == "22":
        sources.append("Yesterday Kerala 3 PM Repeat (226)")
        
    print(f"#{rank:2d} | AB: '{ab}' | Score: {sc:4.1f} | Sources: {', '.join(sources)}")
