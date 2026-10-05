import io
import re
content = io.open('index.html', 'r', encoding='utf-8').read()
for m in re.finditer(r'<section.*?id="container-.*?">', content):
    print(m.group(0))
