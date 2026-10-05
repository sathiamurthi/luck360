import io
content = io.open('index.html', 'r', encoding='utf-8').read()
import re
for m in re.finditer(r'class=".*?tab-content.*?"', content):
    print(m.group(0))
