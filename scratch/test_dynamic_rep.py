import sys, os, json
sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

import report_analytics as ra
with open('draw_history.json') as f:
    records = json.load(f)

latest_rec = records[-1]
latest_tail = latest_rec["tail"]
latest_ticket = latest_rec.get("ticket", "")
latest_time = latest_rec.get("time", "1:00 PM")
latest_date = latest_rec.get("date", "2026-09-27")

# Determine next slot
if "1:00" in latest_time:
    next_slot = "Today 3:00 PM (Kerala State Lotteries)"
    next_lottery = "Kerala State Lotteries - Samrudhi (SM-74)"
elif "3:00" in latest_time:
    next_slot = "Today 6:00 PM (Sikkim State Lottery)"
    next_lottery = "Sikkim State Lottery - Dear 6 PM"
elif "6:00" in latest_time:
    next_slot = "Tonight 8:00 PM (Nagaland State Lottery)"
    next_lottery = "Nagaland State Lottery - Dear 8 PM"
else:
    next_slot = "Tomorrow 1:00 PM (Nagaland State Lottery)"
    next_lottery = "Nagaland State Lottery - Dear 1 PM"

pats = ra.calc_all_patterns(latest_tail, latest_ticket)
d1, d2, d3 = int(latest_tail[0]), int(latest_tail[1]), int(latest_tail[2])

print(f"Next Slot: {next_slot}")
print(f"Base Tail: {latest_tail}")
print("Top Picks:")
print("H18:", pats["H18_OuterBalance"]["val"])
print("H8:", pats["H8_OuterSumStep"]["val"])
print("H14:", pats["H14_PrefixDiff_615"]["val"])
print("H7:", pats["H7_DiffDiffSum"]["val"])
print("H16:", pats["H16_TwinEchoStep"]["val"])
print("P1:", pats["P1_RevDiff"]["val"])
