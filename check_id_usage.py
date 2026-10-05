import io
content = io.open('script1.js', 'r', encoding='utf-8').read()
import re
for mid in ["input-p1-1", "table-pattern-frequency", "top-7-rules"]:
    print(f"\n--- {mid} ---")
    for m in re.finditer(f'getElementById..{mid}.', content):
        start = max(0, m.start()-100)
        end = min(len(content), m.start()+100)
        print(content[start:end])
