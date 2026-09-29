import sys, os
sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')
from report_analytics import calc_all_patterns, calc_blind_patterns

p = calc_all_patterns('053', '65G 50053')
b = calc_blind_patterns('053')

print("--- PATTERNS FROM 053 ---")
for k, v in p.items():
    print(f"{k}: {v['val']} | {v.get('label', '')}")

print("\n--- BLIND PATTERNS FROM 053 ---")
for k, v in b.items():
    print(f"{k}: {v}")
