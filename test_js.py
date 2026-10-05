import io
import re
content = io.open('script1.js', 'r', encoding='utf-8').read()
m = re.search(r'ACTIVE BASELINE', content)
if m:
    print(content[max(0, m.start()-100):m.start()+500].encode('ascii', 'ignore').decode('ascii'))
else:
    print("Not found")
