import io
import re

content = io.open('script1.js', 'r', encoding='utf-8').read()
m = re.search(r'ACTIVE BASELINE', content)
if m:
    print(content[m.start():m.start()+2000].encode('ascii', 'ignore').decode('ascii'))
