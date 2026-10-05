import io
content = io.open('index.html', 'r', encoding='utf-8').read()
import re
for m in re.finditer(r'.{0,50}Kerala.{0,50}', content):
    print(m.group(0))
