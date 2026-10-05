import io
import re
content = io.open('index.html', 'r', encoding='utf-8').read()
matches = re.finditer(r'<section.*?>|CURRENTLY RUNNING|box-active-baseline', content)
for m in matches:
    print(m.group(0)[:80])
