import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')

with open('draw_history.json') as f:
    draws = json.load(f)

print("--- Testing H18 Formula A: ((d1+d3+1)%10, d2, (d3-d1)%10) ---")
for i in range(1, len(draws)):
    prev = draws[i-1]
    curr = draws[i]
    p = prev['tail']
    c = curr['tail']
    d1, d2, d3 = int(p[0]), int(p[1]), int(p[2])
    
    h18_a = f"{(d1+d3+1)%10}{d2}{(d3-d1+10)%10}"
    h18_b = f"{d1+d3}{(d3-d1+10)%10}"
    
    matches = []
    if c == h18_a: matches.append("H18_A Straight Hit")
    if c == h18_b: matches.append("H18_B Straight Hit")
    if c[1:] == h18_a[1:]: matches.append(f"BC Pair Hit ({h18_a[1:]})")
    if c[:2] == h18_a[:2]: matches.append(f"AB Pair Hit ({h18_a[:2]})")
    
    if matches:
        print(f"Draw {i}: {prev['date']} {prev['time']} ({p}) -> {curr['date']} {curr['time']} ({c}) => {', '.join(matches)}")
