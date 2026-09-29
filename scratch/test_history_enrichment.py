import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from luck360_mcp_server import calc_all_patterns, calc_blind_tweak_patterns

with open('draw_history.json', 'r', encoding='utf-8') as f:
    recs = json.load(f)

print(f"Total draws: {len(recs)}")

# Process each draw to attach derived base, winning patterns, and forward patterns
for i, r in enumerate(recs):
    curr_tail = r["tail"]
    curr_sorted = "".join(sorted(curr_tail))
    
    # 1. Determine sequential previous draw
    prev_r = recs[i - 1] if i > 0 else None
    derived_from = None
    winning_pats = []
    
    if prev_r:
        prev_tail = prev_r["tail"]
        derived_from = {
            "index": i - 1,
            "date": prev_r.get("date"),
            "time": prev_r.get("time"),
            "company": prev_r.get("company"),
            "ticket": prev_r.get("ticket"),
            "tail": prev_tail,
            "relation": "Sequential Previous Draw"
        }
        
        pats = calc_all_patterns(prev_tail, prev_r.get("ticket", ""))
        for pkey, pval in pats.items():
            val = pval["val"]
            if val == curr_tail:
                winning_pats.append({"pattern": pkey, "type": "STRAIGHT", "predicted": val, "label": pval.get("label", pkey)})
            elif "".join(sorted(val)) == curr_sorted:
                winning_pats.append({"pattern": pkey, "type": "BOX", "predicted": val, "label": pval.get("label", pkey)})

    # 2. Also check Blind Cross-Draw (1 PM -> 8 PM of same day)
    if r.get("time") == "8:00 PM":
        # Find 1 PM draw of the same day
        pm1 = next((x for x in recs if x.get("date") == r.get("date") and x.get("time") == "1:00 PM"), None)
        if pm1:
            blind_data = calc_blind_tweak_patterns(pm1["tail"])
            for bkey, bobj in blind_data["blind_patterns"].items():
                if bobj["target"] == curr_tail:
                    winning_pats.append({
                        "pattern": bkey,
                        "type": "BLIND STRAIGHT HIT",
                        "predicted": bobj["target"],
                        "label": bobj["name"],
                        "source": f"Cross-Draw Leap from 1 PM ({pm1['tail']})"
                    })

    # 3. Check Day-to-Day Same Slot (Yesterday same time)
    same_slot_prev = next((x for x in reversed(recs[:i]) if x.get("time") == r.get("time")), None)
    if same_slot_prev:
        day_pats = calc_all_patterns(same_slot_prev["tail"], same_slot_prev.get("ticket", ""))
        for dkey, dval in day_pats.items():
            if dval["val"] == curr_tail:
                winning_pats.append({
                    "pattern": dkey,
                    "type": "DAY-TO-DAY STRAIGHT HIT",
                    "predicted": dval["val"],
                    "label": dval.get("label", dkey),
                    "source": f"Day's Pattern from Prev {r.get('time')} ({same_slot_prev['tail']})"
                })

    # Forward patterns for next draw
    fwd_pats = calc_all_patterns(curr_tail, r.get("ticket", ""))
    fwd_blind = calc_blind_tweak_patterns(curr_tail)

    r["derived_from"] = derived_from
    r["winning_patterns"] = winning_pats
    r["forward_patterns"] = {k: v["val"] for k, v in fwd_pats.items()}
    r["forward_blind"] = {k: v["target"] for k, v in fwd_blind["blind_patterns"].items()}

print("\n--- SUMMARY OF WINNING PATTERNS PER DRAW ---")
for i, r in enumerate(recs):
    wins = [w["pattern"] + " (" + w["type"] + ")" for w in r["winning_patterns"]]
    print(f"[{i:2d}] {r['date']} {r['time']:8s} ({r['tail']}) | Wins: {wins if wins else 'None'}")
