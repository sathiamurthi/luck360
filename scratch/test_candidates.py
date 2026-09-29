import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')

with open('draw_history.json') as f:
    draws = json.load(f)

print(f"{'Draw Transition':<35} | {'Cand1 (SumDiff)':<16} | {'Cand2 (D1+D3+1,D2,D3-D1)':<24} | {'P1':<8} | Matches")
print("-" * 105)

for i in range(1, len(draws)):
    prev = draws[i-1]
    curr = draws[i]
    pt = prev['tail']
    ct = curr['tail']
    d1, d2, d3 = int(pt[0]), int(pt[1]), int(pt[2])
    
    sum_outer = d1 + d3
    diff_outer = (d3 - d1 + 10) % 10
    cand1 = f"{sum_outer}{diff_outer}"
    
    cand2 = f"{(d1+d3+1)%10}{d2}{(d3-d1+10)%10}"
    p1 = f"{d3}{d2}{(d3-d1+10)%10}"
    
    match = []
    if ct == cand1: match.append("EXACT_Cand1")
    if ct == cand2: match.append("EXACT_Cand2")
    if ct[1:] == cand2[1:]: match.append(f"BC_Cand2({cand2[1:]})")
    if ct[:2] == cand2[:2]: match.append(f"AB_Cand2({cand2[:2]})")
    if ct[1:] == p1[1:]: match.append(f"BC_P1({p1[1:]})")
    
    trans_str = f"{prev['date'][-5:]} {prev['time']} ({pt}) -> {curr['time']} ({ct})"
    print(f"{trans_str:<35} | {cand1:<16} | {cand2:<24} | {p1:<8} | {', '.join(match)}")
