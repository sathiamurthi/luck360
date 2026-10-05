import io
import re
content = io.open('script1.js', 'r', encoding='utf-8').read()
matches = re.findall(r'.{0,30}tk-date.{0,30}', content)
for m in set(matches):
    print(m)
