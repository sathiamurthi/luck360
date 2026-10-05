import io
import re
content = io.open('index.html', 'r', encoding='utf-8').read()
for m in re.finditer(r'.{0,50}Kerala.{0,50}', content):
    print(m.group(0).encode("ascii", "ignore").decode("ascii"))
