import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(330, 420):
    print(f"{i+1}: {lines[i].strip()}")

print("\n--- JavaScript pattern logic search ---")
for i, line in enumerate(lines):
    if i > 1200 and any(k in line for k in ['h13', 'h14', 'h15', 'renderDrawHistory', 'draw_history', 'checklist_targets', 'renderChecklist', 'ab_pairs', 'renderPatterns']):
        print(f"L{i+1}: {line.strip()[:110]}")
