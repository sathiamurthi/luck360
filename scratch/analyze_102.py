import sys, os, json
sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

# 1. Check same-slot progression
print("=== 1 PM SAME-SLOT PROGRESSION ===")
history_1pm = [
    {"date": "2026-09-24", "ticket": "73G 69563", "tail": "563"},
    {"date": "2026-09-25", "ticket": "84L 10051", "tail": "051"},
    {"date": "2026-09-26", "ticket": "65G 50053", "tail": "053"},
    {"date": "2026-09-27", "ticket": "54J 77102", "tail": "102"},
]
for h in history_1pm:
    print(f"{h['date']}: Ticket={h['ticket']}, Tail={h['tail']}")

# Ticket number features
print("\n=== TICKET NUMBER ANALYSIS ===")
# 2026-09-25: 84L 10051 -> Head=100, Tail=051
# 2026-09-26: 65G 50053 -> Head=500, Tail=053
# 2026-09-27: 54J 77102 -> Head=771, Tail=102
# Notice:
# 25-Sep Ticket body: 10051 -> Has '10' at front, '051' at back
# 26-Sep Ticket body: 50053 -> Has '500' at front (which was 25-Sep 8 PM tail 500!), '053' at back
# 27-Sep Ticket body: 77102 -> Has '77' at front, '102' at back!

# 2. Check Predictions for today 1 PM from predict_3days.py and report_analytics.py
import report_analytics as ra
p_406 = ra.calc_all_patterns('406', '50E 94406')
b_406 = ra.calc_blind_patterns('406')

print("\n=== WHAT WE PREDICTED FROM 406 (Yesterday 8 PM) ===")
# What were the top candidates in predict_3days?
# In predict_3days: top_h7, top_h8, top_h9, top_h6, top_h2
# Let's check them:
top_star = ["H7_DiffDiffSum", "H8_OuterSumStep", "H9_SubAddTen", "H6_DiffSumPlusOne", "H2_CrossSwap", "H15_ShiftDiff", "H16_TwinEchoStep", "H17_SumDiffKeep"]
for pat in top_star:
    info = p_406.get(pat, {})
    val = info.get('val', '')
    print(f"{pat}: {val}")

print("\n=== PAIR COVERAGE ===")
print("Actual Tail: 102 (AB=10, BC=02, AC=12)")
hits = []
for k, v in p_406.items():
    val = v['val']
    ab = val[:2]
    bc = val[1:]
    ac = val[0] + val[2]
    matched = []
    if ab == '10': matched.append('AB=10')
    if bc == '02': matched.append('BC=02')
    if ac == '12': matched.append('AC=12')
    if ab == '01': matched.append('RevAB=01')
    if bc == '20': matched.append('RevBC=20')
    if ac == '21': matched.append('RevAC=21')
    if matched:
        hits.append(f"{k} ({val}): {', '.join(matched)}")

for h in hits:
    print(h)
