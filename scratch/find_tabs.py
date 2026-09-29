import sys, os
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'switchTab' in l or 'data-tab' in l or 'id="tab-' in l or 'id="tabContent' in l or 'nav' in l.lower() and '<button' in l:
        print(f"{i+1}: {l.strip()[:120]}")
