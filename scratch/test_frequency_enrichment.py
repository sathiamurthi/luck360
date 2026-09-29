import json, sys
from datetime import datetime
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

with open('draw_history.json', 'r', encoding='utf-8') as f:
    records = json.load(f)

from report_analytics import calc_all_patterns, calc_blind_patterns

# Pre-calculate AB occurrences and dates across entire history
ab_history = defaultdict(list)
for r in records:
    ab = r['tail'][:2]
    ab_history[ab].append(r)

enriched = []
for i, r in enumerate(records):
    curr_tail = r['tail']
    curr_ab = curr_tail[:2]
    curr_sorted = ''.join(sorted(curr_tail))
    prev_r = records[i - 1] if i > 0 else None

    winning_3digit = []
    winning_ab = []

    # 1. Sequential from prev_r
    if prev_r:
        prev_tail = prev_r['tail']
        pats = calc_all_patterns(prev_tail, prev_r.get('ticket', ''))
        for pk, pv in pats.items():
            pval = pv['val']
            # 3-digit match
            if pval == curr_tail:
                winning_3digit.append({
                    "pattern": pk,
                    "name": pv['label'],
                    "type": "STRAIGHT HIT",
                    "formula": pv['formula'],
                    "predicted": pval,
                    "source": f"Sequential from Prev {prev_r.get('time')} ({prev_tail})"
                })
            elif ''.join(sorted(pval)) == curr_sorted:
                winning_3digit.append({
                    "pattern": pk,
                    "name": pv['label'],
                    "type": "BOX HIT",
                    "formula": pv['formula'],
                    "predicted": pval,
                    "source": f"Sequential from Prev {prev_r.get('time')} ({prev_tail})"
                })
            # 2-digit AB match
            if pval[:2] == curr_ab:
                winning_ab.append({
                    "pattern": pk,
                    "name": pv['label'],
                    "pair": curr_ab,
                    "predicted": pval,
                    "source": f"Sequential from Prev {prev_r.get('time')} ({prev_tail})"
                })

    # 2. Cycle / Cross-Draw check (up to 3 draws back)
    for lookback in range(2, min(i + 1, 4)):
        prior_r = records[i - lookback]
        prior_tail = prior_r['tail']
        p_pats = calc_all_patterns(prior_tail, prior_r.get('ticket', ''))
        for pk, pv in p_pats.items():
            pval = pv['val']
            # Cross-draw 3-digit match
            if pval == curr_tail and pk in ["H15_ShiftDiff", "H13_ZeroSixProduct", "H7_DiffDiffSum", "H9_SubAddTen", "H8_OuterSumStep", "H14_PrefixDiff_615"]:
                winning_3digit.append({
                    "pattern": pk,
                    "name": pv['label'],
                    "type": "CYCLE STRAIGHT HIT",
                    "formula": pv['formula'],
                    "predicted": pval,
                    "source": f"Cycle from Draw {prior_r.get('id')} {prior_r.get('time')} ({prior_tail})"
                })
            # Cross-draw AB match
            if pval[:2] == curr_ab and pk in ["H15_ShiftDiff", "H13_ZeroSixProduct", "H14_PrefixDiff_615", "H7_DiffDiffSum", "H9_SubAddTen", "H8_OuterSumStep"]:
                winning_ab.append({
                    "pattern": pk,
                    "name": pv['label'],
                    "pair": curr_ab,
                    "predicted": pval,
                    "source": f"Cycle from Draw {prior_r.get('id')} {prior_r.get('time')} ({prior_tail})"
                })

    # AB frequency calculation
    ab_matches = ab_history[curr_ab]
    ab_hit_count = len(ab_matches)
    if ab_hit_count > 1:
        ab_freq_label = f"Hit {ab_hit_count}x in history (Recurrence: 1.0d cycle)"
    else:
        ab_freq_label = "Single Historical Strike"

    enriched.append({
        "id": r['id'],
        "date": r['date'],
        "time": r['time'],
        "tail": curr_tail,
        "winning_3digit": winning_3digit,
        "winning_ab": winning_ab,
        "ab_frequency": ab_freq_label
    })

print(f"Enriched {len(enriched)} records.")
for e in enriched[-4:]:
    print(f"\nDraw {e['id']} ({e['date']} {e['time']}): Tail {e['tail']}")
    print("  3-Digit Matches:", [f"{w['name']} ({w['type']}) -> {w['source']}" for w in e['winning_3digit']])
    print("  AB Matches:", [f"AB [{w['pair']}] via {w['name']} ({w['source']})" for w in e['winning_ab']])
    print("  AB Frequency:", e['ab_frequency'])
